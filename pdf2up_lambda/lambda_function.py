from __future__ import annotations

import json
import os
from argparse import ArgumentParser
from pathlib import Path
from pprint import pformat
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import httpx
from arxiv_utils import ArxivPaper
from log_utils import logger
from pdf2up.conversion import pdf2png
from s3_utils import S3Config, S3UrlMappedPaths

S3Config.stage = os.environ.get("STAGE", "dev")
PDF2UP_DEFAULTS = {"box": None, "all_pages": False, "skip": None}


def lambda_handler(event: dict[str, str], context=None) -> dict:
    try:
        logger.info("PARSING EVENT")
        if event.get("body") == "[object Object]":
            raise ValueError(f"The event body is {event['body']}")
        event_body = json.loads(event.get("body", "{}"))
        if not (url := event_body.get("url")):
            raise ValueError("Expected a URL")
        logger.info("CHECKING FOR PDF2UP CONFIG AND/OR SETTING DEFAULTS")
        pdf2up_kwargs = {k: event_body.get(k, PDF2UP_DEFAULTS[k]) for k in PDF2UP_DEFAULTS}
        output = {"source_url": url, **pdf2up_kwargs}
        paper = ArxivPaper.from_url(url)
        output.update({"arx_id": paper.arx_id, "pdf_url": paper.pdf_export_url})
        logger.info(f"INITIALISED: arX⠶{paper.arx_id} stage⠶{S3Config.stage}")
        req = httpx.get(paper.pdf_export_url)
        req.raise_for_status()
        logger.info(f"SUCCESSFULLY RETRIEVED URL")
        with TemporaryDirectory() as d:
            pdf_tmp_path = Path(d) / f"{paper.arx_id}.pdf"
            pdf_tmp_path.write_bytes(req.content)
            logger.info(f"NOW IMAGING THE PDF WITH PDF2UP")
            png_out_paths = pdf2png(input_file=str(pdf_tmp_path), **pdf2up_kwargs)
            logger.info(f"NOW UPLOADING THE PNG FILES TO S3")
            s3_mapped_paths = S3UrlMappedPaths(paths=png_out_paths)
            output.update({"images": s3_mapped_paths.urls})
            s3_mapped_paths.upload()
    except Exception as e:
        logger.info(event)
        output = {"message": repr(e)}
    finally:
        logger.info(pformat(output, sort_dicts=False))
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "*,authorization",
                "Access-Control-Allow-Origin": "https://qrx.spin.systems",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
            },
            "body": json.dumps(output),
        }
    return response


# For local testing
if __name__ == "__main__":
    S3Config.testing = True
    parser = ArgumentParser()
    parser.add_argument("event")
    parser.add_argument("ctx", nargs="?", default=None)
    parser.add_argument("--stage", nargs="?", default="dev")
    args = parser.parse_args()
    event = json.loads(args.event)
    context = json.loads(ctx) if (ctx := args.ctx) else ctx
    S3Config.stage = args.stage
    lambda_handler(event=event, context=context)
