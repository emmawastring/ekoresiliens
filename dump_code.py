import pathlib

INCLUDE = [".py", ".html", ".yml"]
EXCLUDE = ["__pycache__", ".git", "node_modules"]

for f in sorted(pathlib.Path(".").rglob("*")):
    if f.is_file() and f.suffix in INCLUDE:
        if not any(e in str(f) for e in EXCLUDE):
            print(f"\n{'='*60}\n{f}\n{'='*60}")
            print(f.read_text(encoding="utf-8", errors="ignore"))