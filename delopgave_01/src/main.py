from pathlib import Path
import matplotlib.pyplot as plt
import txt_reader

# Current file's directory
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
file_path = parent_dir/'data'/'Navneliste.txt'

names = txt_reader.read_names_from_file(file_path)
names_sorted_by_char = txt_reader.sort_names_by_char(names)
names_sorted_by_len = txt_reader.sort_names_by_len(names)
my_char_dict = txt_reader.count_characters(names)


print(names_sorted_by_char)
print(names_sorted_by_len)
print(my_char_dict)
print(my_char_dict.get('a', 0))
