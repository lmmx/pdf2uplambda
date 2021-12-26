from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import boto3
import pdf2up
import httpx


def id_from_arx_url(url: str) -> str:
    parsed = urlparse(url)
    subpath = Path(parsed.path)
    pdf_suff = subpath.suffix == "pdf"
    arx_id = subpath.stem if pdf_suff else subpath.name
    return arx_id


def arx_url_from_id(arx_id: str) -> str:
    """
    Prepare a URL at the proper export subdomain of arxiv.org so that PDF requests don't return a 403 error when pulled by a non-browser viewer.
    """
    return f"https://export.arxiv.org/{arx_id}.pdf"


def lambda_handler(event, context=None):
    print(type(event))
    print(event)
    if not (url := event.get("url")):
        raise ValueError("Expected a URL")
    parsed = urlparse(url)
    exp_loc = "export.arxiv.org"
    loc_check = parsed.netloc != exp_loc
    pdf_suff = parsed.path.endswith(".pdf")
    if not (loc_check and pdf_suff):
        if parsed.netloc != "arxiv.org":
            raise ValueError("Not an arXiv URL")
        arx_id = id_from_arx_url(url)
        url = arx_url_from_id(arx_id)
    req = httpx.get(url)
    req.raise_for_status()
    out_path = Path() / f"{arx_id}.pdf"
    out_path.write_bytes(req.content)
    s3 = boto3.resource("s3")
    key=str(out_path.resolve())
    s3.upload_file(bucket="bucket-name", key=key)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event")
    parser.add_argument("ctx", nargs="?", default=None)
    args = parser.parse_args()
    event = json.loads(args.event)
    context = json.loads(ctx) if (ctx := args.ctx) else ctx
    lambda_handler(event=event, context=context)
