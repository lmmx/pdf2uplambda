# pdf2uplambda

An AWS Lambda function for pdf2up (2021)

Proof of concept:

```sh
python lambda_function.py --stage=dev '{"url": "https://arxiv.org/abs/2111.00396"}
```
⇣
```
[INFO] INITIALISED: arX⠶2111.00396
[INFO] SUCCESSFULLY RETRIEVED URL
100%|█████████████████████████████████████████████████████████████| 4/4 [00:02<00:00,  1.33it/s]
[INFO] (TESTING) SKIPPING UPLOAD of pdf2up/dev/hires_2111.00396_0.png TO filestore.spin.systems
[INFO] (TESTING) SKIPPING UPLOAD of pdf2up/dev/hires_2111.00396_1.png TO filestore.spin.systems
[INFO] (TESTING) SKIPPING UPLOAD of pdf2up/dev/hires_2111.00396_2.png TO filestore.spin.systems
[INFO] (TESTING) SKIPPING UPLOAD of pdf2up/dev/hires_2111.00396_3.png TO filestore.spin.systems
[INFO] {'source_url': 'https://arxiv.org/abs/2111.00396',
 'box': None,
 'all_pages': False,
 'skip': None,
 'arx_id': '2111.00396',
 'pdf_url': 'https://export.arxiv.org/pdf/2111.00396.pdf',
 'images':
['https://filestore.spin.systems.s3.eu-west-1.amazonaws.com/pdf2up/dev/hires_2111.00396_0.png',
 'https://filestore.spin.systems.s3.eu-west-1.amazonaws.com/pdf2up/dev/hires_2111.00396_1.png',
 'https://filestore.spin.systems.s3.eu-west-1.amazonaws.com/pdf2up/dev/hires_2111.00396_2.png',
 'https://filestore.spin.systems.s3.eu-west-1.amazonaws.com/pdf2up/dev/hires_2111.00396_3.png']}
```
