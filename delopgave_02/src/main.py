from pathlib import Path

print("Hello from delopgave 02!")

path = Path(__file__).resolve().parents[2]
print(path)

data_file = path / 'data' / 'ERROR.txt'
print(data_file)

# INFO, WARNING, ERROR, SUCCES | OTHER?? (CRITICAL)
# 2024-02-25 09:15:32 INFO Application start

# take log file path as input
# check log file exists, if not throw error
# check format is as expected, if not throw error
# read log file, extract log level and timestamp, store in list of tuples?


try:
    with data_file.open('w') as f:
        f.write("This is a test error file.")
except FileNotFoundError:
    print(f"Error: Could not find {data_file}")
    log_data = []


path = Path(__file__).resolve().parents[2]
data_file = path / "data" / "app_log (logfil analyse) - random.txt"
try:
    with open(data_file, "r") as f:
        log_data = f.readlines()
except FileNotFoundError:
    print(f"Error: Could not find {data_file}")
    log_data = []

print(log_data[:5])


log_file = path / "data" / "app_log (logfil analyse) - random.txt"






from dataclasses import dataclass
from datetime import datetime

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
    # Split into at most 4 parts: date, time, level, message (rest)
    parts = line.split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Malformed log line (expected 4 fields): {line!r}")

    date_str, time_str, level, message = parts
    # fromisoformat accepts 'YYYY-MM-DD HH:MM:SS'
    timestamp = datetime.fromisoformat(f"{date_str} {time_str}")
    return LogEntry(timestamp=timestamp, level=level, message=message)


from pathlib import Path

def route_logs_dynamic_levels(in_path: Path, out_dir: Path, suffix: str = ".log") -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    open_files: dict[str, any] = {}
    malformed = (out_dir / "malformed.log").open("w", encoding="utf-8")

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
                    open_files[level] = outfile.open("w", encoding="utf-8")

                f = open_files[level]
                f.write(f"{entry.timestamp:%Y-%m-%d %H:%M:%S} {entry.level} {entry.message}\n")
    finally:
        # Ensure all files are closed even if an error occurs
        malformed.close()
        for f in open_files.values():
            try:
                f.close()
            except Exception:
                pass

# Example usage
# route_logs_dynamic_levels(Path("app.log"), Path("out"))
``
