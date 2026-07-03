from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip()
if version != "r016":
    print(f"r016 calendar owner handoff check skipped for current version {version}")
else:
    raise SystemExit("This historical r016 check should be run from the r016 archive, not from a later detached-calendar build.")
