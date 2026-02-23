from pathlib import Path


# Current file's directory
current_dir = Path(__file__).parent

parent_dir = current_dir.parent.parent

file_path = parent_dir/'data'/'Navneliste.txt'

print(file_path)


with open(file_path, encoding="utf-8") as f:
    read_data = f.read()

names: list[str] = [name.strip() for name in read_data.split(',')]
names_sorted_by_char = sorted(names, key=str.lower)
names_sorted_by_len = sorted(names, key=len)

my_char_dict = {}

for name in names:
    for char in name:
        char = char.lower()
        if char not in my_char_dict:
            my_char_dict[char] = 1
        else:
            my_char_dict[char] += 1
print(my_char_dict)
print(my_char_dict.get('a', 0))
