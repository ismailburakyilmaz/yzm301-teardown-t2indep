"""Derive a non-Windows install lock without changing any other pinned version."""
from pathlib import Path
import argparse
import sys

def derive(text, platform):
    lines=text.splitlines(keepends=True)
    if platform=='win32': return text
    return ''.join(line for line in lines if line.strip()!='pywin32==312')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('destination',type=Path)
    args=parser.parse_args()
    args.destination.write_text(derive(args.source.read_text(encoding='utf-8'),sys.platform),encoding='utf-8',newline='')
