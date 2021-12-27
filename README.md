# pdf2uplambda

An AWS Lambda function for pdf2up (2021)

Reproducible on replit but requires poppler (replit doesn't seem to support)

Proof of concept:

```sh
python lambda_function.py '{"url": "https://arxiv.org/abs/2111.00396"}'
```
⇣
```
[INFO]- INITIALISED: {'source_url': 'https://arxiv.org/abs/2111.00396', 'box': None, 'all_pages':
False, 'skip': None, 'arx_id': '2111.00396', 'pdf_url':
'https://export.arxiv.org/pdf/2111.00396.pdf'}
[INFO]- SUCCESSFULLY RETRIEVED URL
100%|████████████████████████████████████████████████████████████████████████████████████████████|
4/4 [00:02<00:00,  1.34it/s]
[INFO]- {'source_url': 'https://arxiv.org/abs/2111.00396',
 'box': None,
 'all_pages': False,
 'skip': None,
 'arx_id': '2111.00396',
 'pdf_url': 'https://export.arxiv.org/pdf/2111.00396.pdf',
 'images': ['2111.00396_0.png',
            '2111.00396_1.png',
            '2111.00396_2.png',
            '2111.00396_3.png']}
```
