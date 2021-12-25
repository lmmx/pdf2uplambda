import argparse
import json
import pdf2up

def lambda_handler(event, context=None):
  print(type(event))
  print(event)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("event")
  parser.add_argument("ctx", nargs="?", default=None)
  args = parser.parse_args()
  event = json.loads(args.event)
  context = json.loads(args.ctx) if args.ctx else args.ctx
  lambda_handler(event=event, context=context)
