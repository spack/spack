# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""String manipulation functions that do not have other dependencies than Python
standard library
"""

from typing import Any, List, Optional, Sequence


def comma_list(sequence: Sequence[Any], article: str = "") -> str:
    """Create a comma-separated list out of a sequence of stringifiable objects.

    Arguments:
        sequence: objects to be stringified
        article: optionally use an article (e.g., 'and' or 'or' to separate the last two elements).
            With two elements, only the article is used as a separator. With three or more, use
            an Oxford comma (as everyone should).
    """
    if type(sequence) is not list:
        sequence = list(sequence)

    if not sequence:
        return ""
    if len(sequence) == 1:
        return sequence[0]

    out = ", ".join(str(s) for s in sequence[:-1])
    if len(sequence) != 2:
        out += ","  # oxford comma
    out += " "
    if article:
        out += article + " "
    out += str(sequence[-1])
    return out


def comma_or(sequence: Sequence[Any]) -> str:
    """Create a comma-separated list with a final ``"or"`` (foo, bar, or baz).

    Arguments:
        sequence: objects in the list
    """
    return comma_list(sequence, "or")


def comma_and(sequence: Sequence[Any]) -> str:
    """Create a comma-separated list with a final ``"and"`` (foo, bar, and baz).

    Arguments:
        sequence: objects in the list
    """
    return comma_list(sequence, "and")


def ordinal(number: int) -> str:
    """Return the ordinal representation (1st, 2nd, 3rd, etc.) for the provided number.

    Args:
        number: int to convert to ordinal number

    Returns: number's corresponding ordinal
    """
    idx = (number % 10) << 1
    tens = number % 100 // 10
    suffix = "th" if tens == 1 or idx > 6 else "thstndrd"[idx : idx + 2]
    return f"{number}{suffix}"


def quote(sequence: Sequence[Any], q: str = "'") -> List[str]:
    """Returns a list of quoted strings made from each item in the input list.

    Arguments:
        sequence: a sequence of anything that can be turned into a string
        q: quote character to use
    """
    return [f"{q}{e}{q}" for e in sequence]


def plural(n: int, singular: str, plural: Optional[str] = None, show_n: bool = True) -> str:
    """Pluralize <singular> word by adding an s if n != 1.

    Arguments:
        n: number of things there are
        singular: singular form of word
        plural: optional plural form, for when it's not just singular + 's'
        show_n: whether to include n in the result string (default True)

    Returns:
        "1 thing" if n == 1 or "n things" if n != 1
    """
    number = f"{n} " if show_n else ""
    if n == 1:
        return f"{number}{singular}"
    elif plural is not None:
        return f"{number}{plural}"
    else:
        return f"{number}{singular}s"
