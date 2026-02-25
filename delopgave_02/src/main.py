from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


path = Path(__file__).resolve().parents[2]
log_file_01 = path / "data" / "app_log_01.txt"
log_file_02 = path / "data" / "app_log_02.txt"
log_file_03 = path / "data" / "app_log_03.txt"
log_file_04 = path / "data" / "app_log_04.txt"
path_out = path / "data" / "log_output"


@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str


def parse_log_line(line: str) -> LogEntry:
    """
    Parse a line like: '2024-02-25 09:15:32 INFO Application start'
    Returns a LogEntry; raises ValueError for malformed lines.
    """
    line = line.rstrip("\n")
    print(f"Parsing line: {line!r}")
    # Split into at most 4 parts: date, time, level, message (rest)
    parts = line.split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Malformed log line (expected 4 fields): {line!r}")

    date_str, time_str, level, message = parts
    # fromisoformat accepts 'YYYY-MM-DD HH:MM:SS'
    timestamp = datetime.fromisoformat(f"{date_str} {time_str}")
    return LogEntry(timestamp=timestamp, level=level, message=message)


def route_logs_dynamic_levels(in_path: Path, out_dir: Path, suffix: str = ".log") -> None:
    # -------------------------
    # Check input file first
    # -------------------------
    try:
        with in_path.open("r", encoding="utf-8") as f:
            pass  # Just to check if we can open the file
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {in_path}")
        return
    except PermissionError:
        print(f"ERROR: No permission to read: {in_path}")
        return

    # -----------------------------
    # Prepare output directory
    # -----------------------------
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"ERROR: Could not create output directory {out_dir}: {e}")
        return

    # -----------------------------
    # Malformed lines file (append)
    # -----------------------------
    malformed_path = out_dir / "malformed.log"
    try:
        malformed = malformed_path.open("a", encoding="utf-8")
    except Exception as e:
        print(f"ERROR: Could not open malformed log file {malformed_path}: {e}")
        malformed.close()
        return

    open_files: dict[str, any] = {}

    try:
        with in_path.open("r", encoding="utf-8") as fin:
            for line in fin:
                try:
                    entry = parse_log_line(line)
                except Exception:
                    malformed.write(line)
                    continue

                level = entry.level.upper()
                if level not in open_files:
                    # Lazily open a new file for this level
                    outfile = out_dir / f"{level.lower()}{suffix}"
                    open_files[level] = outfile.open("a", encoding="utf-8")

                f = open_files[level]
                try:
                    f.write(f"{entry.timestamp:%Y-%m-%d %H:%M:%S} {entry.level} {entry.message}\n")
                except Exception:
                    malformed.write(f"Failed to write to {level} file: {line}")
    finally:
        # Ensure all files are closed even if an error occurs
        malformed.close()
        for f in open_files.values():
            try:
                f.close()
            except Exception:
                pass


# Example usage
route_logs_dynamic_levels(log_file_01, path_out)
route_logs_dynamic_levels(log_file_02, path_out)
route_logs_dynamic_levels(log_file_03, path_out)
route_logs_dynamic_levels(log_file_04, path_out)