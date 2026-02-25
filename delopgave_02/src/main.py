
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


def route_logs_dynamic_levels(in_path: Path, out_dir: Path, suffix: str = ".log") -> None:

    # --- validate input file ---
    fin = safe_open(in_path, "r")
    if fin is None:
        return  # error message already printed by safe_open

    # --- prepare output directory ---
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"ERROR: Could not create output directory {out_dir}: {e}")
        fin.close()
        return

    # --- open malformed file ---
    malformed_path = out_dir / "malformed.log"
    malformed = safe_open(malformed_path, "a")
    if malformed is None:
        fin.close()
        return

    # --- dynamic output file store ---
    open_files: dict[str, any] = {}

    try:
        with fin:
            for line in fin:
                # --- parse log line ---
                try:
                    entry = parse_log_line(line)
                except Exception:
                    malformed.write(line)
                    continue

                level = entry.level.upper()
                
                # --- lazy open per-level file ---
                if level not in open_files:
                    out_path = out_dir / f"{level.lower()}{suffix}"
                    f = safe_open(out_path, "a")
                    if f is None:
                        malformed.write(f"Failed to open output file for level {level}: {line}")
                        continue
                    open_files[level] = f

                # --- write entry ---
                try:
                    open_files[level].write(
                        f"{entry.timestamp:%Y-%m-%d %H:%M:%S} {entry.level} {entry.message}\n"
                    )
                except Exception as e:
                    malformed.write(f"Failed to write to level {level}: {e} | {line}")

    finally:
        # close malformed
        malformed.close()
        # close all level-based files
        for f in open_files.values():
            try:
                f.close()
            except Exception:
                pass


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
