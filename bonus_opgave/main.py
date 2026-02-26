from pathlib import Path


def load_and_calc_housing_data(path_housing: Path) -> tuple[float, int]:
    '''Load housing data from a CSV file and calculate total purchase amount and count for villas.
    args:
        path_housing (Path): The path to the CSV file containing housing data.
    '''
    total_villa_purchaseAmt: float = 0.0
    total_villa_count: int = 0
    with open(path_housing, "r", encoding="utf-8") as f:
        lines = (line for line in f)
        list_line = (s.rstrip().split(",") for s in lines)
        cols = next(list_line)
        housing_dicts = (dict(zip(cols, data)) for data in list_line)
        purchase_price = (
            float(housing_dict["purchase_price"])
            for housing_dict in housing_dicts
            if housing_dict["house_type"] == "Villa"
        )
        for price in purchase_price:
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
