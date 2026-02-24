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


# delopgave 1.1
print(names_sorted_by_char)
print(names_sorted_by_len)
print(my_char_dict)
print(my_char_dict.get('a', 0))


# delopgave 1.2
# Frekvensanalyse
items = sorted(my_char_dict.items(), key=lambda x: x[1], reverse=True)
keys, values = zip(*items)


# Bar chart over bogstaver og deres frekvens
plt.figure()
plt.bar(keys, values)
plt.show(block=False)

# Wordcloud over navne og deres frekvens
wc = WordCloud(
    width=800,
    height=400,
    background_color="white"
).generate(txt_string)

plt.figure()
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show(block=False)

# histogram over navnelængde og deres frekvens
name_length_freguency = txt_reader.get_name_length_frequencies(names)

items = sorted(name_length_freguency.items())
lengths, counts = zip(*items)

mean_length = txt_reader.mean_name_length(names)
print(f"Mean name length: {mean_length:.2f}")
median_length = txt_reader.median_name_length(names)
print(f"Median name length: {median_length}")

plt.figure()
plt.bar(lengths, counts)
# Add mean line
plt.axvline(mean_length,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Mean = {mean_length:.2f}")
# Add median line
plt.axvline(median_length,
            color="green",
            linestyle="-.",
            linewidth=2,
            label=f"Median = {median_length}")

plt.xlabel('Navnelængde')
plt.ylabel('Frekvens')
plt.title('Histogram over navnelængde')
plt.show()

print("Number of names:", len(names))
print("Number of unique names:", len(list(set(names))))
