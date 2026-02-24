from pathlib import Path

print("Hello from delopgave 02!")

path = Path(__file__).resolve().parents[2]

print(path)

data_file = path / "data" / "app_log (logfil analyse) - random.txt"
with open(data_file, "r") as f:
    log_data = f.readlines()
print(log_data[:5])
