##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################


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
