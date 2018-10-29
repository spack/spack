# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


def comma_list(sequence, article=''):
    if type(sequence) != list:
        sequence = list(sequence)

    if not sequence:
        return
    elif len(sequence) == 1:
        return sequence[0]
    else:
        out = ', '.join(str(s) for s in sequence[:-1])
        if len(sequence) != 2:
            out += ','   # oxford comma
        out += ' '
        if article:
            out += article + ' '
        out += str(sequence[-1])
        return out


def comma_or(sequence):
    return comma_list(sequence, 'or')


def comma_and(sequence):
    return comma_list(sequence, 'and')


def quote(sequence, q="'"):
    return ['%s%s%s' % (q, e, q) for e in sequence]


def plural(n, singular, plural=None):
    """Pluralize <singular> word by adding an s if n != 1.

    Arguments:
        n (int): number of things there are
        singular (str): singular form of word
        plural (str, optional): optional plural form, for when it's not just
            singular + 's'

    Returns:
        (str): "1 thing" if n == 1 or "n things" if n != 1
    """
    if n == 1:
        return "%d %s" % (n, singular)
    elif plural is not None:
        return "%d %s" % (n, plural)
    else:
        return "%d %ss" % (n, singular)
