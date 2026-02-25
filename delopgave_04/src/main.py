import pandas as pd

from pathlib import Path

path = Path(__file__).resolve().parents[2]
print(path)

source_file_01 = path / "data" / "source_data.csv"
source_file_02 = path / "data" / "write_protect_source_data.csv"
path_out = path / "data" / "csv_output"

df = pd.read_csv(
    source_file_01,
    encoding="utf-8",
    sep=",",
    header=0,
    index_col=False,
    on_bad_lines='warn',
)

df.to_csv(path_out / "output.csv", index=False)