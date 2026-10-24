"""CLI wrapper; reusable evaluation logic lives in agent_eval.py."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.agent_eval import main,grade

if __name__=='__main__':
    raise SystemExit(main())
