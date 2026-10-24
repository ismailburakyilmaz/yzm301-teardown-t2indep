import argparse
import asyncio
import json
from .agent import answer,create_backend,ModelUnavailable


def main():
    parser = argparse.ArgumentParser(description='Türkçe t2-indep araç ajanı; model erişimi gerekir.')
    parser.add_argument('question')
    parser.add_argument('--model')
    parser.add_argument('--provider',choices=['gemini','openai','groq'],default='gemini')
    args = parser.parse_args()
    try:
        result = asyncio.run(answer(args.question,create_backend(args.provider,args.model)))
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
        return 0
    except ModelUnavailable as error:
        data = {'error':str(error)}
        if error.receipt:
            data['model_receipt'] = error.receipt
        print(json.dumps(data,ensure_ascii=False))
        return 2
