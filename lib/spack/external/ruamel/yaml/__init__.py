# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

# install_requires of ruamel.base is not really required but the old
# ruamel.base installed __init__.py, and thus a new version should
# be installed at some point

_package_data = dict(
    full_package_name="ruamel.yaml",
    version_info=(0, 11, 15),
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order",  # NOQA
    entry_points=None,
    install_requires=dict(
        any=[],
        py26=["ruamel.ordereddict"],
        py27=["ruamel.ordereddict"]
    ),
    ext_modules=[dict(
        name="_ruamel_yaml",
        src=["ext/_ruamel_yaml.c", "ext/api.c", "ext/writer.c", "ext/dumper.c",
                "ext/loader.c", "ext/reader.c", "ext/scanner.c", "ext/parser.c",
                "ext/emitter.c"],
        lib=[],
        # test='#include "ext/yaml.h"\n\nint main(int argc, char* argv[])\n{\nyaml_parser_t parser;\nparser = parser;  /* prevent warning */\nreturn 0;\n}\n'  # NOQA
        )
    ],
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: Jython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup"
    ],
    windows_wheels=True,
    read_the_docs='yaml',
    many_linux='libyaml-devel',
)


# < from ruamel.util.new import _convert_version
def _convert_version(tup):
    """create a PEP 386 pseudo-format conformant string from tuple tup"""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val


# <
version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version

try:
    from .cyaml import *                               # NOQA
    __with_libyaml__ = True
except (ImportError, ValueError):  # for Jython
    __with_libyaml__ = False


# body extracted to main.py
try:
    from .main import *                               # NOQA
except ImportError:
    from ruamel.yaml.main import *                               # NOQA
