from pathlib import Path

OUT = Path(__file__).parent / "docs"
OUT.mkdir(parents=True, exist_ok=True)

for i in range(1, 11):
    (OUT / f"synthetic_{i}.txt").write_text(
        f"Synthetic operations note {i}. Entity relationships and timeline references for evaluation benchmark use.\n",
        encoding="utf-8",
    )

print("Generated synthetic sample documents.")
