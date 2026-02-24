import sys
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Go from src → delopgave_01 → uge4
project_root = Path(__file__).resolve().parents[2]
# Add uge4 to sys.path
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
import helper_functions.txt_reader as txt_reader



# Current file's directory
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
file_path = parent_dir/'data'/'Navneliste.txt'

txt_string = txt_reader.get_string_from_file(file_path)
names = txt_reader.get_list_of_names_from_string(txt_string)
names_sorted_by_char = txt_reader.sort_names_by_char(names)
names_sorted_by_len = txt_reader.sort_names_by_len(names)
my_char_dict = txt_reader.count_characters(names)


print(names_sorted_by_char)
print(names_sorted_by_len)
print(my_char_dict)
print(my_char_dict.get('a', 0))


items = sorted(my_char_dict.items(), key=lambda x: x[1], reverse=True)

keys, values = zip(*items)

plt.bar(keys, values)


wc = WordCloud(
    width=800,
    height=400,
    background_color="white"
).generate(txt_string)

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
