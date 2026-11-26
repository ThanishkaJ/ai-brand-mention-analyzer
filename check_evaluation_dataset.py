
import json
from pathlib import Path

dataset_path = Path("tests/evaluation_cases.json")

with dataset_path.open("r", encoding="utf-8") as file:
    cases = json.load(file)

print("Total test cases:", len(cases))

categories = {}

for case in cases:
    category = case["category"]
    categories[category] = categories.get(category, 0) + 1

print("\nCases by category:")

for category, count in categories.items():
    print(f"{category}: {count}")

print("\nDataset loaded successfully!")