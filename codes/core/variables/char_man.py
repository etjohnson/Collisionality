

def capital_first_letter(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, got {string.type}"
        )
    result = string.capitalize()

    return result


def capital_all_first_letter(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = ' '.join(elem.capitalize() for elem in string.split())

    return result


def capital_all_letter(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = string.upper()

    return result


def lower_first_letter(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = string[0].lower() + string[1:]

    return result


def lower_all_first_letter(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = ' '.join(elem.lower() for elem in string.split())

    return result


def lower_all_letter(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, got {string.type}"
        )

    result = string.lower()

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
    result = string[:l - 1]

    return result


def remove_begin(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            "Argument passed is a not string, instead "
            f" got {string.type}."
        )

    result = string[1:]

    return result


def add_space_front(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            "Argument passed is a not string, instead "
            f" got {string.type}."
        )

    res = string + ' '

    return res


def add_space_end(
        string,
):
    if not isinstance(string, str):
        raise ValueError(
            "Argument passed is a not string, instead "
            f" got {string.type}."
        )

    res = ' ' + string

    return res


