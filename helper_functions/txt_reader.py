def get_string_from_file(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        read_data = f.read()
    return read_data


def get_list_of_names_from_string(txt: str) -> list[str]:
    names: list[str] = [name.strip() for name in txt.split(',')]
    return names


def sort_names_by_char(names: list[str]) -> list[str]:
    names_sorted_by_char = sorted(names, key=str.lower)
    return names_sorted_by_char


def sort_names_by_len(names: list[str]) -> list[str]:
    names_sorted_by_len = sorted(names, key=len)
    return names_sorted_by_len


def count_characters(names: list[str]) -> dict[str, int]:
    my_char_dict = {}
    for name in names:
        for char in name:
            char = char.lower()
            if char not in my_char_dict:
                my_char_dict[char] = 1
            else:
                my_char_dict[char] += 1
    return my_char_dict
