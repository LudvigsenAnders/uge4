from pathlib import Path


def parse_housing_csv(path_housing: Path):
    """Generator that parses housing CSV and yields dictionaries."""
    with open(path_housing, "r", encoding="utf-8") as f:
        print("FILE OPENED")  # Opens once here
        cols = next(line.rstrip().split(",") for line in f)     
        for line in f:
            data = line.rstrip().split(",")
            yield dict(zip(cols, data))
        print("FILE CLOSED")  # Closes after all yields are consumed


def filter_villas(housing_data):
    """Generator that filters villas and yields purchase prices."""
    for house in housing_data:
        if house["house_type"] == "Villa":
            yield float(house["purchase_price"])


def load_and_calc_housing_data(path_housing: Path) -> tuple[float, int]:
    """Calculate villa statistics using parsers."""
    housing_data = parse_housing_csv(path_housing)
    villa_prices = filter_villas(housing_data)

    total_villa_purchaseAmt = 0
    total_villa_count = 0

    for price in villa_prices:
        total_villa_purchaseAmt += price
        total_villa_count += 1

    return total_villa_purchaseAmt, total_villa_count


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1]
    print(path)

    path_housing = path / "data" / "DKHousingPricesSample100k.csv"
    total_villa_purchaseAmt, total_villa_count = load_and_calc_housing_data(path_housing)
    avg_villa_price = total_villa_purchaseAmt / total_villa_count if total_villa_count > 0 else 0

    print(f"Total villa purchase amount: DKK {total_villa_purchaseAmt}")
    print(f"Total villa count: {total_villa_count}")
    print(f"Average villa purchase price: DKK {avg_villa_price}")
