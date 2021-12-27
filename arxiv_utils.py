from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

__all__ = ["ArxivPaper"]


class ArxivPaper:
    """
    This class is completely 'offline', and just handles URLs.
    """

    arx_id: str
    root_netloc: str = "arxiv.org"

    def __init__(self, arx_id: str):
        self.arx_id = arx_id

    def __repr__(self):
        return f"arX⠶{self.arx_id}"

    def url_base(self, export=False, secure=True):
        """The main domain or the export domain"""
        protocol = f"http{'s' if secure else ''}://"
        return f"{protocol}{'export.' if export else ''}{self.root_netloc}"

    @classmethod
    def from_url(cls, url: str) -> ArxivPaper:
        parsed = urlparse(url)
        # URL must be on arxiv.org
        if parsed.netloc.rsplit(".", maxsplit=2)[-2:] != ["arxiv", "org"]:
            raise ValueError("Not an arXiv URL")
        subpath = Path(parsed.path)
        arx_id = subpath.stem if subpath.suffix == ".pdf" else subpath.name
        return cls(arx_id=arx_id)

    @property
    def abs_url(self) -> str:
        base = self.url_base(export=False, secure=True)
        return "/".join([base, "abs", self.arx_id])

    @property
    def pdf_url(self) -> str:
        base = self.url_base(export=False, secure=True)
        return "/".join([base, "pdf", f"{self.arx_id}.pdf"])

    @property
    def pdf_export_url(self) -> str:
        """
        Prepare a URL at the proper export subdomain of arxiv.org so that PDF requests don't
        return a 403 error when pulled by a non-browser viewer.
        """
        return "/".join([self.url_base(export=True), "pdf", f"{self.arx_id}.pdf"])
