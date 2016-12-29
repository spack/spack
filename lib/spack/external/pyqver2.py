#!/usr/bin/env python
#
# pyqver2.py
# by Greg Hewgill
# https://github.com/ghewgill/pyqver
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the author be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# Copyright (c) 2009-2013 Greg Hewgill http://hewgill.com
#

import compiler
import platform
import sys

StandardModules = {
    "__future__":       (2, 1),
    "abc":              (2, 6),
# skip argparse now that it's in lib/spack/external
#    "argparse":         (2, 7),
    "ast":              (2, 6),
    "atexit":           (2, 0),
    "bz2":              (2, 3),
    "cgitb":            (2, 2),
    "collections":      (2, 4),
    "contextlib":       (2, 5),
    "cookielib":        (2, 4),
    "cProfile":         (2, 5),
    "csv":              (2, 3),
    "ctypes":           (2, 5),
    "datetime":         (2, 3),
    "decimal":          (2, 4),
    "difflib":          (2, 1),
    "DocXMLRPCServer":  (2, 3),
    "dummy_thread":     (2, 3),
    "dummy_threading":  (2, 3),
    "email":            (2, 2),
    "fractions":        (2, 6),
    "functools":        (2, 5),
    "future_builtins":  (2, 6),
    "hashlib":          (2, 5),
    "heapq":            (2, 3),
    "hmac":             (2, 2),
    "hotshot":          (2, 2),
    "HTMLParser":       (2, 2),
# skip importlib until we can conditionally skip for pytest.
# pytest tries to import this and catches the exception, but
# the test will still fail.
# TODO: can we excelude with a comment like '# flake: noqa?'
#    "importlib":        (2, 7),
    "inspect":          (2, 1),
    "io":               (2, 6),
    "itertools":        (2, 3),
    "json":             (2, 6),
    "logging":          (2, 3),
    "modulefinder":     (2, 3),
    "msilib":           (2, 5),
    "multiprocessing":  (2, 6),
    "netrc":            (1, 5, 2),
    "numbers":          (2, 6),
    "optparse":         (2, 3),
    "ossaudiodev":      (2, 3),
    "pickletools":      (2, 3),
    "pkgutil":          (2, 3),
    "platform":         (2, 3),
    "pydoc":            (2, 1),
    "runpy":            (2, 5),
    "sets":             (2, 3),
    "shlex":            (1, 5, 2),
    "SimpleXMLRPCServer": (2, 2),
    "spwd":             (2, 5),
    "sqlite3":          (2, 5),
    "ssl":              (2, 6),
    "stringprep":       (2, 3),
    "subprocess":       (2, 4),
    "sysconfig":        (2, 7),
    "tarfile":          (2, 3),
    "textwrap":         (2, 3),
    "timeit":           (2, 3),
    "unittest":         (2, 1),
    "uuid":             (2, 5),
    "warnings":         (2, 1),
    "weakref":          (2, 1),
    "winsound":         (1, 5, 2),
    "wsgiref":          (2, 5),
    "xml.dom":          (2, 0),
    "xml.dom.minidom":  (2, 0),
    "xml.dom.pulldom":  (2, 0),
    "xml.etree.ElementTree": (2, 5),
    "xml.parsers.expat":(2, 0),
    "xml.sax":          (2, 0),
    "xml.sax.handler":  (2, 0),
    "xml.sax.saxutils": (2, 0),
    "xml.sax.xmlreader":(2, 0),
    "xmlrpclib":        (2, 2),
    "zipfile":          (1, 6),
    "zipimport":        (2, 3),
    "_ast":             (2, 5),
    "_winreg":          (2, 0),
}

Functions = {
    "all":                      (2, 5),
    "any":                      (2, 5),
    "collections.Counter":      (2, 7),
    "collections.defaultdict":  (2, 5),
    "collections.OrderedDict":  (2, 7),
    "functools.total_ordering": (2, 7),
    "enumerate":                (2, 3),
    "frozenset":                (2, 4),
    "itertools.compress":       (2, 7),
    "math.erf":                 (2, 7),
    "math.erfc":                (2, 7),
    "math.expm1":               (2, 7),
    "math.gamma":               (2, 7),
    "math.lgamma":              (2, 7),
    "memoryview":               (2, 7),
    "next":                     (2, 6),
    "os.getresgid":             (2, 7),
    "os.getresuid":             (2, 7),
    "os.initgroups":            (2, 7),
    "os.setresgid":             (2, 7),
    "os.setresuid":             (2, 7),
    "reversed":                 (2, 4),
    "set":                      (2, 4),
    "subprocess.check_call":    (2, 5),
    "subprocess.check_output":  (2, 7),
    "sum":                      (2, 3),
    "symtable.is_declared_global": (2, 7),
    "weakref.WeakSet":          (2, 7),
}

Identifiers = {
    "False":        (2, 2),
    "True":         (2, 2),
}

def uniq(a):
    if len(a) == 0:
        return []
    else:
        return [a[0]] + uniq([x for x in a if x != a[0]])

class NodeChecker(object):
    def __init__(self):
        self.vers = dict()
        self.vers[(2,0)] = []
    def add(self, node, ver, msg):
        if ver not in self.vers:
            self.vers[ver] = []
        self.vers[ver].append((node.lineno, msg))
    def default(self, node):
        for child in node.getChildNodes():
            self.visit(child)
    def visitCallFunc(self, node):
        def rollup(n):
            if isinstance(n, compiler.ast.Name):
                return n.name
            elif isinstance(n, compiler.ast.Const):
                return type(n.value).__name__
            elif isinstance(n, compiler.ast.Getattr):
                r = rollup(n.expr)
                if r:
                    return r + "." + n.attrname
        name = rollup(node.node)
        if name:
            # Special handling for empty format strings, which aren't
            # allowed in Python 2.6
            if name in ('unicode.format', 'str.format'):
                n = node.node
                if isinstance(n, compiler.ast.Getattr):
                    n = n.expr
                    if isinstance(n, compiler.ast.Const):
                        if '{}' in n.value:
                            self.add(node, (2,7), name + ' with {} format string')

            v = Functions.get(name)
            if v is not None:
                self.add(node, v, name)
        self.default(node)
    def visitClass(self, node):
        if node.bases:
            self.add(node, (2,2), "new-style class")
        if node.decorators:
            self.add(node, (2,6), "class decorator")
        self.default(node)
    def visitDictComp(self, node):
        self.add(node, (2,7), "dictionary comprehension")
        self.default(node)
    def visitFloorDiv(self, node):
        self.add(node, (2,2), "// operator")
        self.default(node)
    def visitFrom(self, node):
        v = StandardModules.get(node.modname)
        if v is not None:
            self.add(node, v, node.modname)
        for n in node.names:
            name = node.modname + "." + n[0]
            v = Functions.get(name)
            if v is not None:
                self.add(node, v, name)
    def visitFunction(self, node):
        if node.decorators:
            self.add(node, (2,4), "function decorator")
        self.default(node)
    def visitGenExpr(self, node):
        self.add(node, (2,4), "generator expression")
        self.default(node)
    def visitGetattr(self, node):
        if (isinstance(node.expr, compiler.ast.Const)
            and isinstance(node.expr.value, str)
            and node.attrname == "format"):
            self.add(node, (2,6), "string literal .format()")
        self.default(node)
    def visitIfExp(self, node):
        self.add(node, (2,5), "inline if expression")
        self.default(node)
    def visitImport(self, node):
        for n in node.names:
            v = StandardModules.get(n[0])
            if v is not None:
                self.add(node, v, n[0])
        self.default(node)
    def visitName(self, node):
        v = Identifiers.get(node.name)
        if v is not None:
            self.add(node, v, node.name)
        self.default(node)
    def visitSet(self, node):
        self.add(node, (2,7), "set literal")
        self.default(node)
    def visitSetComp(self, node):
        self.add(node, (2,7), "set comprehension")
        self.default(node)
    def visitTryFinally(self, node):
        # try/finally with a suite generates a Stmt node as the body,
        # but try/except/finally generates a TryExcept as the body
        if isinstance(node.body, compiler.ast.TryExcept):
            self.add(node, (2,5), "try/except/finally")
        self.default(node)
    def visitWith(self, node):
        if isinstance(node.body, compiler.ast.With):
            self.add(node, (2,7), "with statement with multiple contexts")
        else:
            self.add(node, (2,5), "with statement")
        self.default(node)
    def visitYield(self, node):
        self.add(node, (2,2), "yield expression")
        self.default(node)

def get_versions(source):
    """Return information about the Python versions required for specific features.

    The return value is a dictionary with keys as a version number as a tuple
    (for example Python 2.6 is (2,6)) and the value are a list of features that
    require the indicated Python version.
    """
    tree = compiler.parse(source)
    checker = compiler.walk(tree, NodeChecker())
    return checker.vers

def v27(source):
    if sys.version_info >= (2, 7):
        return qver(source)
    else:
        print >>sys.stderr, "Not all features tested, run --test with Python 2.7"
        return (2, 7)

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print "hello world"')
    (2, 0)
    >>> qver('class test(object): pass')
    (2, 2)
    >>> qver('yield 1')
    (2, 2)
    >>> qver('a // b')
    (2, 2)
    >>> qver('True')
    (2, 2)
    >>> qver('enumerate(a)')
    (2, 3)
    >>> qver('total = sum')
    (2, 0)
    >>> qver('sum(a)')
    (2, 3)
    >>> qver('(x*x for x in range(5))')
    (2, 4)
    >>> qver('class C:\\n @classmethod\\n def m(): pass')
    (2, 4)
    >>> qver('y if x else z')
    (2, 5)
    >>> qver('import hashlib')
    (2, 5)
    >>> qver('from hashlib import md5')
    (2, 5)
    >>> qver('import xml.etree.ElementTree')
    (2, 5)
    >>> qver('try:\\n try: pass;\\n except: pass;\\nfinally: pass')
    (2, 0)
    >>> qver('try: pass;\\nexcept: pass;\\nfinally: pass')
    (2, 5)
    >>> qver('from __future__ import with_statement\\nwith x: pass')
    (2, 5)
    >>> qver('collections.defaultdict(list)')
    (2, 5)
    >>> qver('from collections import defaultdict')
    (2, 5)
    >>> qver('"{0}".format(0)')
    (2, 6)
    >>> qver('memoryview(x)')
    (2, 7)
    >>> v27('{1, 2, 3}')
    (2, 7)
    >>> v27('{x for x in s}')
    (2, 7)
    >>> v27('{x: y for x in s}')
    (2, 7)
    >>> qver('from __future__ import with_statement\\nwith x:\\n with y: pass')
    (2, 5)
    >>> v27('from __future__ import with_statement\\nwith x, y: pass')
    (2, 7)
    >>> qver('@decorator\\ndef f(): pass')
    (2, 4)
    >>> qver('@decorator\\nclass test:\\n pass')
    (2, 6)

    #>>> qver('0o0')
    #(2, 6)
    #>>> qver('@foo\\nclass C: pass')
    #(2, 6)
    """
    return max(get_versions(source).keys())


if __name__ == '__main__':

    Verbose = False
    MinVersion = (2, 3)
    Lint = False

    files = []
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--test":
            import doctest
            doctest.testmod()
            sys.exit(0)
        if a == "-v" or a == "--verbose":
            Verbose = True
        elif a == "-l" or a == "--lint":
            Lint = True
        elif a == "-m" or a == "--min-version":
            i += 1
            MinVersion = tuple(map(int, sys.argv[i].split(".")))
        else:
            files.append(a)
        i += 1

    if not files:
        print >>sys.stderr, """Usage: %s [options] source ...

        Report minimum Python version required to run given source files.

        -m x.y or --min-version x.y (default 2.3)
            report version triggers at or above version x.y in verbose mode
        -v or --verbose
            print more detailed report of version triggers for each version
    """ % sys.argv[0]
        sys.exit(1)

    for fn in files:
        try:
            f = open(fn)
            source = f.read()
            f.close()
            ver = get_versions(source)
            if Verbose:
                print fn
                for v in sorted([k for k in ver.keys() if k >= MinVersion], reverse=True):
                    reasons = [x for x in uniq(ver[v]) if x]
                    if reasons:
                        # each reason is (lineno, message)
                        print "\t%s\t%s" % (".".join(map(str, v)), ", ".join([x[1] for x in reasons]))
            elif Lint:
                for v in sorted([k for k in ver.keys() if k >= MinVersion], reverse=True):
                    reasons = [x for x in uniq(ver[v]) if x]
                    for r in reasons:
                        # each reason is (lineno, message)
                        print "%s:%s: %s %s" % (fn, r[0], ".".join(map(str, v)), r[1])
            else:
                print "%s\t%s" % (".".join(map(str, max(ver.keys()))), fn)
        except SyntaxError, x:
            print "%s: syntax error compiling with Python %s: %s" % (fn, platform.python_version(), x)
