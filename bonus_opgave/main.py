from pathlib import Path

path = Path(__file__).resolve().parents[1]
print(path)

path_housing = path / "data" / "DKHousingPricesSample100k.csv"


def safe_open(path: Path, mode: str, encoding="utf-8"):
    """Try opening a file, return file or None."""
    try:
        return path.open(mode, encoding=encoding)
    except Exception as e:
        print(f"ERROR: Cannot open {path}: {e}")
        return None


fin = safe_open(path_housing, mode="r")
if fin is not None:
    print("File opened successfully.")
else:
    print("Failed to open file.")

lines = (line for line in fin)

list_line = (s.rstrip().split(",") for s in lines)

cols = next(list_line)

housing_dicts = (dict(zip(cols, data)) for data in list_line)

purchase_price = (
    float(housing_dict["purchase_price"])
    for housing_dict in housing_dicts
    if housing_dict["house_type"] == "Villa"
)


total_villa_purchaseAmt = 0
total_villa_count = 0

for price in purchase_price:
    total_villa_purchaseAmt += price
    total_villa_count += 1

avg_villa_price = total_villa_purchaseAmt / total_villa_count if total_villa_count > 0 else 0
print(f"Total villa purchase amount: DKK {total_villa_purchaseAmt}")
print(f"Total villa count: {total_villa_count}")
print(f"Average villa purchase price: DKK {avg_villa_price}")

fin.close()