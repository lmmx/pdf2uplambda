from __future__ import annotations
import argparse
import json
import pdf2up
from urllib.parse import urlparse


def prepare_arxiv_url(arx_id: str) -> str:
    """
    Prepare a URL at the proper export subdomain of arxiv.org so that PDF requests don't return a 403 error when pulled by a non-browser viewer.
    """
    return f"https://export.arxiv.org/{arx_id}.pdf"

def id_from_arx_url(url: str) -> str:
    parsed = urlparse(url)
    subpath = Path(parsed.path)
    pdf_suff = subpath.suffix == 'pdf'
    arx_id = subpath.stem if pdf_suff else subpath.name
    return arx_id

def lambda_handler(event, context=None):
    print(type(event))
    print(event)
    if "url" not in event:
        raise ValueError("Expected a URL")
    parsed = urlparse(url)
    exp_loc = 'export.arxiv.org'
    loc_check = parsed.netloc != exp_loc
    pdf_suff = parsed.path.endswith(".pdf")
    if not (loc_check and pdf_suff):
        if parsed.netloc != 'arxiv.org':
            raise ValueError("Not an arXiv URL")
        arx_id = id_from_arx_url(url)
        url = arx_url_from_id(arx_id)
    req = httpx.get(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event")
    parser.add_argument("ctx", nargs="?", default=None)
    args = parser.parse_args()
    event = json.loads(args.event)
    context = json.loads(ctx) if (ctx := args.ctx) else ctx
    lambda_handler(event=event, context=context)
