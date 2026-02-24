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


def get_name_length_frequencies(names: list[str]) -> dict[int, int]:
    '''Calculate the frequency of each name length in the list.
    Takes a list of names. Finds the length of each name and counts
    number of names of that length.
    Args:
        names (list of str): A list of names.
        Returns: A dictionary where the keys are name lengths and the values
        are the frequencies of those lengths.
    '''
    name_length_freguency = {}
    for name in names:
        length = len(name)
        if length not in name_length_freguency:
            name_length_freguency[length] = 1
        else:
            name_length_freguency[length] += 1
    return name_length_freguency


def mean_name_length(names):
    '''Calculate the mean length of names in the list.
    Takes list of names. Finds sum of length of each name and divides by
    number of names.
    Args:
        names (list of str): A list of names.
        Returns: The mean length of the names in the list.
    '''
    if not names:
        raise ValueError("The names list is empty.")

    total_length = sum(len(name) for name in names)
    mean_length = total_length / len(names)
    return mean_length


def median_name_length(names):
    '''Calculate the median length of names in the list.
    Takes list if name. Finds length of each name and sorts them.
    If the number of names is odd, returns the middle length
    in the sorted list.
    If even, returns the average of the two middle lengths in the sorted list.
    Args:
        names (list of str): A list of names.
        Returns: The median length of the names in the list.
    '''
    if not names:
        raise ValueError("The names list is empty.")

    lengths = sorted(len(name) for name in names)
    n = len(lengths)
    mid = n // 2

    if n % 2 == 1:
        # Odd count gives one remainder → middle element
        return lengths[mid]
    else:
        # Even count → average of the two middle elements
        return (lengths[mid - 1] + lengths[mid]) / 2
