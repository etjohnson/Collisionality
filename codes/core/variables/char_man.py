

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


def jws(
        a,
        b,
        c=False,
        d=False,
        e=False,
        f=False,
        g=False,
        h=False,
        i=False,
        j=False,
        k=False,
        l=False,
        m=False,
):
    if not isinstance(a and b, str):
        raise TypeError(
            f"Arguments must be strings, instead got string_a: {a.type} "
            f"and string_b: {b.type}."
        )

    for arg_name in (c, d, e, f, g, h, i, j, k, l, m):
        if not isinstance(arg_name, (str, bool)):
            raise TypeError(
                f"Argument '{arg_name}' must be a string,"
                f" instead got type {arg_name.type}."
            )

    arg_ = ' '.join([a, b])

    for default_val in (c, d, e, f, g, h, i, j, k, l, m):
        if not default_val:
            break
        else:
            arg_ = ' '.join([arg_, default_val])

    res = arg_

    return res


def jwos(
        a,
        b,
        c=False,
        d=False,
        e=False,
        f=False,
        g=False,
        h=False,
        i=False,
        j=False,
        k=False,
        l=False,
        m=False,
):
    if not isinstance(a and b, str):
        raise TypeError(
            f"Arguments must be strings, instead got string_a: {a.type} "
            f"and string_b: {b.type}."
        )

    for arg_name in (c, d, e, f, g, h, i, j, k, l, m):
        if not isinstance(arg_name, (str, bool)):
            raise TypeError(
                f"Argument '{arg_name}' must be a string,"
                f" instead got type {arg_name.type}."
            )

    arg_ = ''.join([a, b])

    for default_val in (c, d, e, f, g, h, i, j, k, l, m):
        if not default_val:
            break
        else:
            arg_ = ''.join([arg_, default_val])

    res = arg_

    return res


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


def slash_check(
        string,
):
    if not isinstance(string, str):
        raise TypeError(
            f"Argument passed is not a string, "
            f"instead got {type(string)}"
        )

    if string.endswith("/") or string.endswith(r"\/"):
        res = string
    else:
        if '/' in string:
            res = jws(string, '/')
        elif r"\/" in string:
            res = jws(string, r"\/")
        else:
            raise ValueError(
                "Error: No slash in string."
            )
        
    return res