def sort(my_list):
    return sorted(my_list)


def find(my_list, value):
    try:
        return my_list.index(value)
    except ValueError:
        return -1


def find_sequence(my_list, sequence):
    for i in range(len(my_list) - len(sequence) + 1):
        if my_list[i:i + len(sequence)] == sequence:
            return i
    return -1


def find_first_5_minimums(my_list):
    return sorted(my_list)[:5]


def find_first_5_maximums(my_list):
    return sorted(my_list, reverse=True)[:5]


def average(my_list):
    if len(my_list) == 0:
        return 0
    return sum(my_list) / len(my_list)


def remove_duplicates(my_list):
    seen = set()
    no_duplicates = []
    for item in my_list:
        if item not in seen:
            no_duplicates.append(item)
            seen.add(item)
    return no_duplicates
