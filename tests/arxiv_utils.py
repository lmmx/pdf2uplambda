from pytest import mark


@mark.parametrize(
    "url",
    [
        "http://arxiv.org/abs/2111.00396",
        "https://arxiv.org/abs/2111.00396",
        "http://arxiv.org/pdf/2111.00396.pdf",
        "https://arxiv.org/pdf/2111.00396.pdf",
        "https://export.arxiv.org/pdf/2111.00396.pdf",
    ],
)
@mark.parametrize("expected", "2111.00396")
def test_arxiv_paper_recognition(url, expected):
    paper = ArxivPaper.from_url(url)
    assert paper.arx_id == expected
