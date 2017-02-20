##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import textwrap

import jinja2
import spack

#: Directories where to search for templates
template_dirs = spack.template_dirs


def make_environment(dirs=None):
    if dirs is None:
        dirs = template_dirs
    # Loader for the templates
    loader = jinja2.FileSystemLoader(dirs)
    # Environment of the template engine
    env = jinja2.Environment(loader=loader, trim_blocks=True)
    # Custom filters
    _set_filters(env)
    return env


def prepend_to_line(text, token):
    """Prepends a token to each line in text"""
    return [token + line for line in text]


def quote(text):
    """Quotes each line in text"""
    return ['"{0}"'.format(line) for line in text]


def _set_filters(env):
    """Sets custom filters to the template engine environment"""
    env.filters['textwrap'] = textwrap.wrap
    env.filters['prepend_to_line'] = prepend_to_line
    env.filters['join'] = '\n'.join
    env.filters['quote'] = quote
