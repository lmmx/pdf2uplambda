from __future__ import annotations

import json
import os
from argparse import ArgumentParser
from pathlib import Path
from pprint import pformat
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import httpx
from pdf2up.conversion import pdf2png

from arxiv_utils import ArxivPaper
from console_log import logger
from s3_utils import S3Config, S3Url, S3Urls

S3Config.STAGE = os.environ.get("STAGE", "dev")
S3Config.TESTING = True
PDF2UP_DEFAULTS = {"box": None, "all_pages": False, "skip": None}


def lambda_handler(event: dict[str, str], context=None) -> dict:
    if not (url := event.get("url")):
        raise ValueError("Expected a URL")
    pdf2up_kwargs = {k: event.get(k, PDF2UP_DEFAULTS[k]) for k in PDF2UP_DEFAULTS}
    output = {"source_url": url, **pdf2up_kwargs}
    paper = ArxivPaper.from_url(url)
    output.update({"arx_id": paper.arx_id, "pdf_url": paper.pdf_export_url})
    logger.info(f"INITIALISED: arX⠶{paper.arx_id}")
    req = httpx.get(paper.pdf_export_url)
    req.raise_for_status()
    logger.info(f"SUCCESSFULLY RETRIEVED URL")
    with TemporaryDirectory() as d:
        pdf_tmp_path = Path(d) / f"{paper.arx_id}.pdf"
        pdf_tmp_path.write_bytes(req.content)
        # Handle the PDF with pdf2up
        png_out_paths = pdf2png(input_file=str(pdf_tmp_path), **pdf2up_kwargs)
        # Now handle S3 upload here
        stage_subpath = ["dev"] if S3Config.STAGE == "dev" else []
        path_base = Path(S3Config.dir_name, *stage_subpath)
        png_keys = [f"{path_base / ('pdf2up_' + png.name)}" for png in png_out_paths]
        s3_urls = S3Urls.from_keys(png_keys)
    output.update({"images": s3_urls})
    if S3Config.TESTING:
        logger.info(pformat(output, sort_dicts=False))
    return output


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("event")
    parser.add_argument("ctx", nargs="?", default=None)
    args = parser.parse_args()
    event = json.loads(args.event)
    context = json.loads(ctx) if (ctx := args.ctx) else ctx
    lambda_handler(event=event, context=context)
