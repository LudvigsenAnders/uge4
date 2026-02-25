
import csv
from pathlib import Path

def copy_csv(in_path: Path, out_path: Path, encoding: str = "utf-8") -> None:
    """
    Read a CSV file and write to a new CSV (headers preserved).
    Includes error handling for input/output and ensures files are closed.
    """
    # ---------- Validate input file ----------
    try:
        fin = in_path.open("r", encoding=encoding, newline="")
    except FileNotFoundError:
        print(f"ERROR: Input CSV not found: {in_path}")
        return
    except PermissionError:
        print(f"ERROR: No permission to read input CSV: {in_path}")
        return
    except OSError as e:
        print(f"ERROR opening input CSV {in_path}: {e}")
        return

    # ---------- Prepare output directory ----------
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"ERROR: Could not create output directory {out_path.parent}: {e}")
        fin.close()
        return

    # ---------- Open output file ----------
    try:
        fout = out_path.open("w", encoding=encoding, newline="")
    except PermissionError:
        print(f"ERROR: No permission to write output CSV: {out_path}")
        fin.close()
        return
    except OSError as e:
        print(f"ERROR opening output CSV {out_path}: {e}")
        fin.close()
        return

    try:
        with fin, fout:
            reader = csv.reader(fin)
            writer = csv.writer(fout)

            try:
                header = next(reader)  # may raise StopIteration on empty file
            except StopIteration:
                print(f"WARNING: Input CSV is empty: {in_path}. Creating empty output.")
                return

            # Write header
            writer.writerow(header)

            # Copy rows safely; if a row is malformed, skip and continue
            for idx, row in enumerate(reader, start=2):  # header is line 1
                try:
                    writer.writerow(row)
                except Exception as e:
                    # Log and skip problematic row
                    print(f"WARNING: Failed to write row {idx}: {e}. Row content: {row!r}")

    finally:
        # Context managers already close files, this is just extra safety if above returned early
        try:
            fout.close()
        except Exception:
            pass
        # fin is closed by the with-statement above

path = Path(__file__).resolve().parents[2]
source_file_01 = path / "data" / "source_data.csv"
source_file_02 = path / "data" / "write_protect_source_data.csv"
path_out = path / "data" / "csv_output"

# Example usage
copy_csv(source_file_01, path_out / "output_01.csv")
copy_csv(source_file_02, path_out / "output_02.csv")

