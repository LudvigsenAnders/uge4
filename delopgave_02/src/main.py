
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str


def parse_log_line(line: str) -> LogEntry:
    parts = line.rstrip("\n").split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Malformed log line: {line!r}")
    date_str, time_str, level, message = parts
    ts = datetime.fromisoformat(f"{date_str} {time_str}")
    return LogEntry(ts, level, message)


def safe_open(path: Path, mode: str, encoding="utf-8"):
    """Try opening a file, return file or None."""
    try:
        return path.open(mode, encoding=encoding)
    except Exception as e:
        print(f"ERROR: Cannot open {path}: {e}")
        return None


def get_or_create_level_file(level: str, out_dir: Path, open_files: dict, suffix: str) -> bool:
    """Get or create output file for a log level. Returns True if successful."""
    if level not in open_files:
        out_path = out_dir / f"{level.lower()}{suffix}"
        f = safe_open(out_path, "a")
        if f is None:
            return False
        open_files[level] = f
    return True


def handle_malformed_line(malformed, line: str, msg: str = ""):
    """Write malformed line to file with optional message."""
    if msg:
        malformed.write(f"{msg}: {line}")
    else:
        malformed.write(line)


def write_log_entry(open_files, level, entry, malformed, line):
    """Write log entry to the appropriate file, handle errors."""
    try:
        open_files[level].write(
            f"{entry.timestamp:%Y-%m-%d %H:%M:%S} {entry.level} {entry.message}\n"
        )
    except Exception as e:
        handle_malformed_line(malformed, line, f"Failed to write to level {level}: {e}")


def process_log_line(line: str, open_files: dict, malformed, out_dir: Path, suffix: str) -> None:
    """Process a single log line and route to appropriate output file."""
    try:
        entry = parse_log_line(line)
    except Exception:
        handle_malformed_line(malformed, line)
        return

    level = entry.level.upper()
    if not get_or_create_level_file(level, out_dir, open_files, suffix):
        handle_malformed_line(malformed, line, f"Failed to open output file for level {level}")
        return

    write_log_entry(open_files, level, entry, malformed, line)


def validate_and_prepare_files(in_path: Path, out_dir: Path) -> tuple:
    """Validate input file and prepare output directory and malformed file."""
    fin = safe_open(in_path, "r")
    if fin is None:
        return None, None, None

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"ERROR: Could not create output directory {out_dir}: {e}")
        fin.close()
        return None, None, None

    malformed_path = out_dir / "malformed.log"
    malformed = safe_open(malformed_path, "a")
    if malformed is None:
        fin.close()
        return None, None, None

    return fin, malformed, malformed_path


def close_files(malformed, open_files):
    """Close malformed and level-based files."""
    try:
        malformed.close()
    except Exception:
        pass
    for f in open_files.values():
        try:
            f.close()
        except Exception:
            pass


def route_logs_dynamic_levels(in_path: Path, out_dir: Path, suffix: str = ".log") -> None:
    fin, malformed, _ = validate_and_prepare_files(in_path, out_dir)
    if fin is None or malformed is None:
        return

    open_files: dict[str, any] = {}

    try:
        with fin:
            for line in fin:
                process_log_line(line, open_files, malformed, out_dir, suffix)
    finally:
        close_files(malformed, open_files)


path = Path(__file__).resolve().parents[2]
log_file_01 = path / "data" / "app_log_01.txt"
log_file_02 = path / "data" / "app_log_02.txt"
log_file_03 = path / "data" / "app_log_03.txt"
log_file_04 = path / "data" / "app_log_04.txt"
path_out = path / "data" / "log_output"

# Example usage
route_logs_dynamic_levels(log_file_01, path_out)
route_logs_dynamic_levels(log_file_02, path_out)
route_logs_dynamic_levels(log_file_03, path_out)
route_logs_dynamic_levels(log_file_04, path_out)
