from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import txt_reader


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