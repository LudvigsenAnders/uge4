import csv
from pathlib import Path


# ---------- Validation helpers ----------
def validate_input_file(in_path: Path, encoding: str) -> bool:
    """Ensure input CSV can be opened for reading."""
    try:
        with in_path.open("r", encoding=encoding, newline=""):
            return True
    except FileNotFoundError:
        print(f"ERROR: Input CSV not found: {in_path}")
    except PermissionError:
        print(f"ERROR: No permission to read input CSV: {in_path}")
    except OSError as e:
        print(f"ERROR opening input CSV {in_path}: {e}")
    return False


def ensure_output_directory(out_path: Path) -> bool:
    """Ensure the output directory exists."""
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"ERROR: Could not create output directory {out_path.parent}: {e}")
        return False


def validate_output_file(out_path: Path, encoding: str) -> bool:
    """
    Ensure the output CSV can be opened for writing.
    NOTE: Only opens it briefly; actual writing happens later.
    """
    try:
        with out_path.open("w", encoding=encoding, newline=""):
            return True
    except PermissionError:
        print(f"ERROR: No permission to write output CSV: {out_path}")
    except OSError as e:
        print(f"ERROR opening output CSV {out_path}: {e}")
    return False


# ---------- CSV logic ----------
def write_csv_rows(reader: csv.reader, writer: csv.writer) -> None:
    """Write all rows from reader to writer with error handling."""
    for idx, row in enumerate(reader, start=2):
        try:
            writer.writerow(row)
        except Exception as e:
            print(f"WARNING: Could not write row {idx}: {e}. Row: {row!r}")


def copy_csv_contents(in_path: Path, out_path: Path, encoding: str) -> None:
    """Copy header + rows from input CSV to output CSV."""

    with in_path.open("r", encoding=encoding, newline="") as fin, \
         out_path.open("w", encoding=encoding, newline="") as fout:

        reader = csv.reader(fin)
        writer = csv.writer(fout)

        # Header
        try:
            header = next(reader)
        except StopIteration:
            print(f"WARNING: Input CSV is empty: {in_path}. Creating empty output.")
            return

        writer.writerow(header)

        # Rows
        write_csv_rows(reader, writer)
        print(f"Successfully copied CSV from {in_path} to {out_path}")


# ---------- Orchestrator ----------
def copy_csv(in_path: Path, out_path: Path, encoding: str = "utf-8") -> None:
    """High-level CSV copy process with validation."""

    if not validate_input_file(in_path, encoding):
        return

    if not ensure_output_directory(out_path):
        return

    if not validate_output_file(out_path, encoding):
        return

    # If all validations pass, perform the actual copy
    copy_csv_contents(in_path, out_path, encoding)


def main() -> None:
    # Example usage
    copy_csv(source_file_01, path_out / "output_01.csv")
    copy_csv(source_file_02, path_out / "output_02.csv")


path = Path(__file__).resolve().parents[2]
source_file_01 = path / "data" / "source_data.csv"
source_file_02 = path / "data" / "write_protect_source_data.csv"
path_out = path / "data" / "csv_output"


if __name__ == "__main__":
    main()
