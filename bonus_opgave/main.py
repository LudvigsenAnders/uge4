from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import matplotlib.pyplot as plt
import time
import tracemalloc


@dataclass
class HousingEntry:
    date: str
    quarter: str
    house_id: int
    house_type: str
    sales_type: str
    year_build: int
    purchase_price: float
    change_between_offer_and_purchase: float
    no_rooms: int
    sqm: float
    sqm_price: float
    address: str
    zip_code: str
    city: str
    area: str
    region: str
    nom_interest_rate: float
    dk_ann_infl_rate: float
    yield_on_mortgage_credit_bonds: float


def _sanitize_column(col: str) -> str:
    """Convert a CSV header into a valid Python attribute name."""
    name = col.strip().strip('%')                    # drop surrounding percent signs
    name = re.sub(r'[^0-9A-Za-z_]', '_', name)       # replace illegal chars with _
    name = re.sub(r'__+', '_', name)                 # collapse runs of underscores
    name = name.lstrip('_')                          # don’t start with _
    if not name:
        raise ValueError(f"cannot sanitise column {col!r}")
    return name


def parse_housing_csv(path_housing: Path):
    """Generator that parses housing CSV and yields dictionaries."""
    with open(path_housing, "r", encoding="utf-8") as f:
        print("FILE OPENED")  # Opens once here
        cols = next(line.rstrip().split(",") for line in f)
        col_names = [_sanitize_column(c) for c in cols]
        for line in f:
            data = line.rstrip().split(",")
            record = dict(zip(col_names, data))
            yield HousingEntry(**record)  # Yield dataclass instance instead of dict
        print("FILE CLOSED")  # Closes after all yields are consumed


def house_price_pairs(housing_data: HousingEntry, allowed_types: list[str]):
    """Yield purchase_price for entries whose house_type is in `allowed_types`."""
    allowed = set(allowed_types)          # make membership test cheap
    for house in housing_data:            # housing_data is the parser generator
        if house.house_type in allowed:
            yield str(house.house_type), float(house.purchase_price)


def aggregate_price_by_house_type(
        path_housing: Path,
        allowed_types: list[str]) -> tuple[dict[str, float], dict[str, int]]:
    """Calculate house statistics using parsers."""
    housing_data: HousingEntry = parse_housing_csv(path_housing)
    prices = house_price_pairs(housing_data, allowed_types)

    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    sum_sqs: dict[str, float] = defaultdict(float) 

    for house_type, price in prices:
        totals[house_type] += price
        counts[house_type] += 1
        sum_sqs[house_type] += price * price

    stats = calculate_statistics(totals, counts, sum_sqs)

    return stats


def calculate_statistics(
        totals: dict[str, float],
        counts: dict[str, int],
        sum_sqs: dict[str, float]) -> dict[str, tuple[float, float]]:
    """Calculate average and standard deviation for each house type."""
    stats = {}
    for house_type in totals:
        total = totals[house_type]
        count = counts[house_type]
        sum_sq = sum_sqs[house_type]
        avg = total / count if count else 0
        stddev = ((sum_sq - (total * total) / count) / (count - 1)) ** 0.5 if count else 0  # sample stddev (count - 1)
        stats[house_type] = (count, total, avg, stddev)
    return stats


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1]
    print(path)

    path_housing = path / "data" / "DKHousingPricesSample100k.csv"
    allowed = ["Villa", "Apartment", "Summerhouse", "Townhouse", "Farm"]
    
    # start measurement
    tracemalloc.start()
    start = time.perf_counter()

    stats = aggregate_price_by_house_type(path_housing, allowed)

    # stop measurement
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nElapsed time   : {end - start:.6f} seconds")
    print(f"Memory current : {current / 1024:.1f} KiB")
    print(f"Memory peak    : {peak / 1024:.1f} KiB")

    for house_type, (count, total, avg, stddev) in stats.items():
        print(f"{house_type}: count={count}, total={total:.2f}, avg={avg:.2f}, stddev={stddev:.2f}")

    # --- plotting ---------------------------------------------------------
    types = list(stats.keys())
    counts = [stats[t][0] for t in types]
    avgs = [stats[t][2] for t in types]
    stds = [stats[t][3] for t in types]

    # average price ± stddev
    fig1, ax1 = plt.subplots()
    ax1.bar(types, avgs, yerr=stds, capsize=4)
    ax1.set_ylabel("Average purchase price (DKK)")
    ax1.set_title("Average price per house type")
    ax1.set_xticks(range(len(types)))
    ax1.set_xticklabels(types, rotation=45, ha="right")
    fig1.tight_layout()

    # counts
    fig2, ax2 = plt.subplots()
    ax2.bar(types, counts)
    ax2.set_ylabel("Number of records")
    ax2.set_title("Count per house type")
    ax2.set_xticks(range(len(types)))
    ax2.set_xticklabels(types, rotation=45, ha="right")
    fig2.tight_layout()

    plt.show()
