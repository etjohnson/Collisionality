def capital_first_letter(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            f"Argument passed is not a string, got {string.type}"
        )
    result = string.capitalize()

    return result


def capital_all_first_letter(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = ' '.join(elem.capitalize() for elem in string.split())

    return result


def capital_all_letter(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = string.upper()

    return result


def lower_first_letter(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = string[0].lower() + string[1:]

    return result


def lower_all_first_letter(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = ' '.join(elem.lower() for elem in string.split())

    return result


def lower_all_letter(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = string.lower()

    return result


def join_w_space(
        string_a,
        string_b,
):
    if not isinstance(string_a and string_b, str):
        raise ValueError(
            "Arguments passed are not strings, for string_a"
            f" got {string_a.type}, and string_b got {string_b.type}."
        )

    string_c = ' '.join([string_a, string_b])

    return string_c


def join_wo_space(
        string_a,
        string_b,
):
    if not isinstance(string_a and string_b, str):
        raise ValueError(
            "Arguments passed are not strings, for string_a"
            f" got {string_a.type}, and string_b got {string_b.type}."
        )

    string_c = ''.join([string_a, string_b])

    return string_c


def add_to_end(
        string,
        addition,
):
    if not isinstance(string and addition, str):
        raise ValueError(
            "Arguments passed are not strings, for string_a"
            f" got {string.type}, and string_b got {addition.type}."
        )

    result = string + addition

    return result


def add_to_begin(
        string,
        addition,
):
    if not isinstance(string and addition, str):
        raise ValueError(
            "Arguments passed are not strings, for string_a"
            f" got {string.type}, and string_b got {addition.type}."
        )

    result = addition + string

    return result

def remove_end(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            "Argument passed is a not string, instead "
            f" got {string.type}."
        )
    l = len(string)
    result = string[:l-1]

    return result