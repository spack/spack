# Copyright (c) 2014-2021, Simon Percivall and Spack Project Developers.
#
# SPDX-License-Identifier: Python-2.0

"Usage: unparse.py <path to source file>"
from __future__ import print_function, unicode_literals

import ast
import sys
from contextlib import contextmanager

import six
from six import StringIO


# TODO: if we require Python 3.7, use its `nullcontext()`
@contextmanager
def nullcontext():
    yield


# Large float and imaginary literals get turned into infinities in the AST.
# We unparse those infinities to INFSTR.
INFSTR = "1e" + repr(sys.float_info.max_10_exp + 1)


class _Precedence:
    """Precedence table that originated from python grammar."""

    TUPLE = 0
    YIELD = 1     # 'yield', 'yield from'
    TEST = 2      # 'if'-'else', 'lambda'
    OR = 3        # 'or'
    AND = 4       # 'and'
    NOT = 5       # 'not'
    CMP = 6       # '<', '>', '==', '>=', '<=', '!=', 'in', 'not in', 'is', 'is not'
    EXPR = 7
    BOR = EXPR    # '|'
    BXOR = 8      # '^'
    BAND = 9      # '&'
    SHIFT = 10    # '<<', '>>'
    ARITH = 11    # '+', '-'
    TERM = 12     # '*', '@', '/', '%', '//'
    FACTOR = 13   # unary '+', '-', '~'
    POWER = 14    # '**'
    AWAIT = 15    # 'await'
    ATOM = 16


def pnext(precedence):
    return min(precedence + 1, _Precedence.ATOM)


def interleave(inter, f, seq):
    """Call f on each item in seq, calling inter() in between.
    """
    seq = iter(seq)
    try:
        f(next(seq))
    except StopIteration:
        pass
    else:
        for x in seq:
            inter()
            f(x)


class Unparser:
    """Methods in this class recursively traverse an AST and
    output source code for the abstract syntax; original formatting
    is disregarded. """

    def __init__(self, py_ver_consistent=False):
        """Traverse an AST and generate its source.

        Arguments:
            py_ver_consistent (bool): if True, generate unparsed code that is
                consistent between Python 2.7 and 3.5-3.10.

        Consistency is achieved by:
            1. Ensuring that *args and **kwargs are always the last arguments,
               regardless of the python version, because Python 2's AST does not
               have sufficient information to reconstruct star-arg order.
            2. Always unparsing print as a function.
            3. Unparsing Python3 unicode literals the way Python 2 would.

        Without these changes, the same source can generate different code for Python 2
        and Python 3, depending on subtle AST differences.  The first of these two
        causes this module to behave differently from Python 3.8+'s `ast.unparse()`

        One place where single source will generate an inconsistent AST is with
        multi-argument print statements, e.g.::

            print("foo", "bar", "baz")

        In Python 2, this prints a tuple; in Python 3, it is the print function with
        multiple arguments.  Use ``from __future__ import print_function`` to avoid
        this inconsistency.

        """
        self.future_imports = []
        self._indent = 0
        self._py_ver_consistent = py_ver_consistent
        self._precedences = {}

    def visit(self, tree, output_file):
        """Traverse tree and write source code to output_file."""
        self.f = output_file
        self.dispatch(tree)
        self.f.flush()

    def fill(self, text=""):
        "Indent a piece of text, according to the current indentation level"
        self.f.write("\n" + "    " * self._indent + text)

    def write(self, text):
        "Append a piece of text to the current line."
        self.f.write(six.text_type(text))

    class _Block:
        """A context manager for preparing the source for blocks. It adds
        the character ':', increases the indentation on enter and decreases
        the indentation on exit."""
        def __init__(self, unparser):
            self.unparser = unparser

        def __enter__(self):
            self.unparser.write(":")
            self.unparser._indent += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.unparser._indent -= 1

    def block(self):
        return self._Block(self)

    @contextmanager
    def delimit(self, start, end):
        """A context manager for preparing the source for expressions. It adds
         *start* to the buffer and enters, after exit it adds *end*."""

        self.write(start)
        yield
        self.write(end)

    def delimit_if(self, start, end, condition):
        if condition:
            return self.delimit(start, end)
        else:
            return nullcontext()

    def require_parens(self, precedence, t):
        """Shortcut to adding precedence related parens"""
        return self.delimit_if("(", ")", self.get_precedence(t) > precedence)

    def get_precedence(self, t):
        return self._precedences.get(t, _Precedence.TEST)

    def set_precedence(self, precedence, *nodes):
        for t in nodes:
            self._precedences[t] = precedence

    def dispatch(self, tree):
        "Dispatcher function, dispatching tree type T to method _T."
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return
        meth = getattr(self, "_" + tree.__class__.__name__)
        meth(tree)

    #
    # Unparsing methods
    #
    # There should be one method per concrete grammar type Constructors
    # should be # grouped by sum type. Ideally, this would follow the order
    # in the grammar, but currently doesn't.

    def _Module(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Interactive(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Expression(self, tree):
        self.dispatch(tree.body)

    # stmt
    def _Expr(self, tree):
        self.fill()
        self.set_precedence(_Precedence.YIELD, tree.value)
        self.dispatch(tree.value)

    def _NamedExpr(self, tree):
        with self.require_parens(_Precedence.TUPLE, tree):
            self.set_precedence(_Precedence.ATOM, tree.target, tree.value)
            self.dispatch(tree.target)
            self.write(" := ")
            self.dispatch(tree.value)

    def _Import(self, t):
        self.fill("import ")
        interleave(lambda: self.write(", "), self.dispatch, t.names)

    def _ImportFrom(self, t):
        # A from __future__ import may affect unparsing, so record it.
        if t.module and t.module == '__future__':
            self.future_imports.extend(n.name for n in t.names)

        self.fill("from ")
        self.write("." * t.level)
        if t.module:
            self.write(t.module)
        self.write(" import ")
        interleave(lambda: self.write(", "), self.dispatch, t.names)

    def _Assign(self, t):
        self.fill()
        for target in t.targets:
            self.dispatch(target)
            self.write(" = ")
        self.dispatch(t.value)

    def _AugAssign(self, t):
        self.fill()
        self.dispatch(t.target)
        self.write(" " + self.binop[t.op.__class__.__name__] + "= ")
        self.dispatch(t.value)

    def _AnnAssign(self, t):
        self.fill()
        with self.delimit_if(
                "(", ")", not t.simple and isinstance(t.target, ast.Name)):
            self.dispatch(t.target)
        self.write(": ")
        self.dispatch(t.annotation)
        if t.value:
            self.write(" = ")
            self.dispatch(t.value)

    def _Return(self, t):
        self.fill("return")
        if t.value:
            self.write(" ")
            self.dispatch(t.value)

    def _Pass(self, t):
        self.fill("pass")

    def _Break(self, t):
        self.fill("break")

    def _Continue(self, t):
        self.fill("continue")

    def _Delete(self, t):
        self.fill("del ")
        interleave(lambda: self.write(", "), self.dispatch, t.targets)

    def _Assert(self, t):
        self.fill("assert ")
        self.dispatch(t.test)
        if t.msg:
            self.write(", ")
            self.dispatch(t.msg)

    def _Exec(self, t):
        self.fill("exec ")
        self.dispatch(t.body)
        if t.globals:
            self.write(" in ")
            self.dispatch(t.globals)
        if t.locals:
            self.write(", ")
            self.dispatch(t.locals)

    def _Print(self, t):
        # Use print function so that python 2 unparsing is consistent with 3
        if self._py_ver_consistent:
            self.fill("print(")
        else:
            self.fill("print ")

        do_comma = False
        if t.dest:
            self.write(">>")
            self.dispatch(t.dest)
            do_comma = True
        for e in t.values:
            if do_comma:
                self.write(", ")
            else:
                do_comma = True
            self.dispatch(e)
        if not t.nl:
            self.write(",")

        if self._py_ver_consistent:
            self.write(")")

    def _Global(self, t):
        self.fill("global ")
        interleave(lambda: self.write(", "), self.write, t.names)

    def _Nonlocal(self, t):
        self.fill("nonlocal ")
        interleave(lambda: self.write(", "), self.write, t.names)

    def _Await(self, t):
        with self.require_parens(_Precedence.AWAIT, t):
            self.write("await")
            if t.value:
                self.write(" ")
                self.set_precedence(_Precedence.ATOM, t.value)
                self.dispatch(t.value)

    def _Yield(self, t):
        with self.require_parens(_Precedence.YIELD, t):
            self.write("yield")
            if t.value:
                self.write(" ")
                self.set_precedence(_Precedence.ATOM, t.value)
                self.dispatch(t.value)

    def _YieldFrom(self, t):
        with self.require_parens(_Precedence.YIELD, t):
            self.write("yield from")
            if t.value:
                self.write(" ")
                self.set_precedence(_Precedence.ATOM, t.value)
                self.dispatch(t.value)

    def _Raise(self, t):
        self.fill("raise")
        if six.PY3:
            if not t.exc:
                assert not t.cause
                return
            self.write(" ")
            self.dispatch(t.exc)
            if t.cause:
                self.write(" from ")
                self.dispatch(t.cause)
        else:
            self.write(" ")
            if t.type:
                self.dispatch(t.type)
            if t.inst:
                self.write(", ")
                self.dispatch(t.inst)
            if t.tback:
                self.write(", ")
                self.dispatch(t.tback)

    def _Try(self, t):
        self.fill("try")
        with self.block():
            self.dispatch(t.body)
        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            self.fill("else")
            with self.block():
                self.dispatch(t.orelse)
        if t.finalbody:
            self.fill("finally")
            with self.block():
                self.dispatch(t.finalbody)

    def _TryExcept(self, t):
        self.fill("try")
        with self.block():
            self.dispatch(t.body)

        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            self.fill("else")
            with self.block():
                self.dispatch(t.orelse)

    def _TryFinally(self, t):
        if len(t.body) == 1 and isinstance(t.body[0], ast.TryExcept):
            # try-except-finally
            self.dispatch(t.body)
        else:
            self.fill("try")
            with self.block():
                self.dispatch(t.body)

        self.fill("finally")
        with self.block():
            self.dispatch(t.finalbody)

    def _ExceptHandler(self, t):
        self.fill("except")
        if t.type:
            self.write(" ")
            self.dispatch(t.type)
        if t.name:
            self.write(" as ")
            if six.PY3:
                self.write(t.name)
            else:
                self.dispatch(t.name)
        with self.block():
            self.dispatch(t.body)

    def _ClassDef(self, t):
        self.write("\n")
        for deco in t.decorator_list:
            self.fill("@")
            self.dispatch(deco)
        self.fill("class " + t.name)
        if six.PY3:
            with self.delimit("(", ")"):
                comma = False
                for e in t.bases:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.dispatch(e)
                for e in t.keywords:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.dispatch(e)
                if sys.version_info[:2] < (3, 5):
                    if t.starargs:
                        if comma:
                            self.write(", ")
                        else:
                            comma = True
                        self.write("*")
                        self.dispatch(t.starargs)
                    if t.kwargs:
                        if comma:
                            self.write(", ")
                        else:
                            comma = True
                        self.write("**")
                        self.dispatch(t.kwargs)
        elif t.bases:
            with self.delimit("(", ")"):
                for a in t.bases[:-1]:
                    self.dispatch(a)
                    self.write(", ")
                self.dispatch(t.bases[-1])
        with self.block():
            self.dispatch(t.body)

    def _FunctionDef(self, t):
        self.__FunctionDef_helper(t, "def")

    def _AsyncFunctionDef(self, t):
        self.__FunctionDef_helper(t, "async def")

    def __FunctionDef_helper(self, t, fill_suffix):
        self.write("\n")
        for deco in t.decorator_list:
            self.fill("@")
            self.dispatch(deco)
        def_str = fill_suffix + " " + t.name
        self.fill(def_str)
        with self.delimit("(", ")"):
            self.dispatch(t.args)
        if getattr(t, "returns", False):
            self.write(" -> ")
            self.dispatch(t.returns)
        with self.block():
            self.dispatch(t.body)

    def _For(self, t):
        self.__For_helper("for ", t)

    def _AsyncFor(self, t):
        self.__For_helper("async for ", t)

    def __For_helper(self, fill, t):
        self.fill(fill)
        self.dispatch(t.target)
        self.write(" in ")
        self.dispatch(t.iter)
        with self.block():
            self.dispatch(t.body)
        if t.orelse:
            self.fill("else")
            with self.block():
                self.dispatch(t.orelse)

    def _If(self, t):
        self.fill("if ")
        self.dispatch(t.test)
        with self.block():
            self.dispatch(t.body)
        # collapse nested ifs into equivalent elifs.
        while (t.orelse and len(t.orelse) == 1 and
               isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.fill("elif ")
            self.dispatch(t.test)
            with self.block():
                self.dispatch(t.body)
        # final else
        if t.orelse:
            self.fill("else")
            with self.block():
                self.dispatch(t.orelse)

    def _While(self, t):
        self.fill("while ")
        self.dispatch(t.test)
        with self.block():
            self.dispatch(t.body)
        if t.orelse:
            self.fill("else")
            with self.block():
                self.dispatch(t.orelse)

    def _generic_With(self, t, async_=False):
        self.fill("async with " if async_ else "with ")
        if hasattr(t, 'items'):
            interleave(lambda: self.write(", "), self.dispatch, t.items)
        else:
            self.dispatch(t.context_expr)
            if t.optional_vars:
                self.write(" as ")
                self.dispatch(t.optional_vars)
        with self.block():
            self.dispatch(t.body)

    def _With(self, t):
        self._generic_With(t)

    def _AsyncWith(self, t):
        self._generic_With(t, async_=True)

    # expr
    def _Bytes(self, t):
        self.write(repr(t.s))

    def _Str(self, tree):
        if six.PY3:
            # Python 3.5, 3.6, and 3.7 can't tell if something was written as a
            # unicode constant. Try to make that consistent with 'u' for '\u- literals
            if self._py_ver_consistent and repr(tree.s).startswith("'\\u"):
                self.write("u")
            self._write_constant(tree.s)
        elif self._py_ver_consistent:
            self.write(repr(tree.s))  # just do a python 2 repr for consistency
        else:
            # if from __future__ import unicode_literals is in effect,
            # then we want to output string literals using a 'b' prefix
            # and unicode literals with no prefix.
            if "unicode_literals" not in self.future_imports:
                self.write(repr(tree.s))
            elif isinstance(tree.s, str):
                self.write("b" + repr(tree.s))
            elif isinstance(tree.s, unicode):  # noqa
                self.write(repr(tree.s).lstrip("u"))
            else:
                assert False, "shouldn't get here"

    def _JoinedStr(self, t):
        # JoinedStr(expr* values)
        self.write("f")
        string = StringIO()
        self._fstring_JoinedStr(t, string.write)
        # Deviation from `unparse.py`: Try to find an unused quote.
        # This change is made to handle _very_ complex f-strings.
        v = string.getvalue()
        if '\n' in v or '\r' in v:
            quote_types = ["'''", '"""']
        else:
            quote_types = ["'", '"', '"""', "'''"]
        for quote_type in quote_types:
            if quote_type not in v:
                v = "{quote_type}{v}{quote_type}".format(quote_type=quote_type, v=v)
                break
        else:
            v = repr(v)
        self.write(v)

    def _FormattedValue(self, t):
        # FormattedValue(expr value, int? conversion, expr? format_spec)
        self.write("f")
        string = StringIO()
        self._fstring_JoinedStr(t, string.write)
        self.write(repr(string.getvalue()))

    def _fstring_JoinedStr(self, t, write):
        for value in t.values:
            meth = getattr(self, "_fstring_" + type(value).__name__)
            meth(value, write)

    def _fstring_Str(self, t, write):
        value = t.s.replace("{", "{{").replace("}", "}}")
        write(value)

    def _fstring_Constant(self, t, write):
        assert isinstance(t.value, str)
        value = t.value.replace("{", "{{").replace("}", "}}")
        write(value)

    def _fstring_FormattedValue(self, t, write):
        write("{")

        expr = StringIO()
        unparser = type(self)(py_ver_consistent=self._py_ver_consistent)
        unparser.set_precedence(pnext(_Precedence.TEST), t.value)
        unparser.visit(t.value, expr)
        expr = expr.getvalue().rstrip("\n")

        if expr.startswith("{"):
            write(" ")  # Separate pair of opening brackets as "{ {"
        write(expr)
        if t.conversion != -1:
            conversion = chr(t.conversion)
            assert conversion in "sra"
            write("!{conversion}".format(conversion=conversion))
        if t.format_spec:
            write(":")
            meth = getattr(self, "_fstring_" + type(t.format_spec).__name__)
            meth(t.format_spec, write)
        write("}")

    def _Name(self, t):
        self.write(t.id)

    def _NameConstant(self, t):
        self.write(repr(t.value))

    def _Repr(self, t):
        self.write("`")
        self.dispatch(t.value)
        self.write("`")

    def _write_constant(self, value):
        if isinstance(value, (float, complex)):
            # Substitute overflowing decimal literal for AST infinities.
            self.write(repr(value).replace("inf", INFSTR))
        elif isinstance(value, str) and self._py_ver_consistent:
            # emulate a python 2 repr with raw unicode escapes
            # see _Str for python 2 counterpart
            raw = repr(value.encode("raw_unicode_escape")).lstrip('b')
            if raw.startswith(r"'\\u"):
                raw = "'\\" + raw[3:]
            self.write(raw)
        else:
            self.write(repr(value))

    def _Constant(self, t):
        value = t.value
        if isinstance(value, tuple):
            with self.delimit("(", ")"):
                if len(value) == 1:
                    self._write_constant(value[0])
                    self.write(",")
                else:
                    interleave(lambda: self.write(", "), self._write_constant, value)
        elif value is Ellipsis:  # instead of `...` for Py2 compatibility
            self.write("...")
        else:
            if t.kind == "u":
                self.write("u")
            self._write_constant(t.value)

    def _Num(self, t):
        repr_n = repr(t.n)
        if six.PY3:
            self.write(repr_n.replace("inf", INFSTR))
        else:
            # Parenthesize negative numbers, to avoid turning (-1)**2 into -1**2.
            with self.require_parens(pnext(_Precedence.FACTOR), t):
                if "inf" in repr_n and repr_n.endswith("*j"):
                    repr_n = repr_n.replace("*j", "j")
                # Substitute overflowing decimal literal for AST infinities.
                self.write(repr_n.replace("inf", INFSTR))

    def _List(self, t):
        with self.delimit("[", "]"):
            interleave(lambda: self.write(", "), self.dispatch, t.elts)

    def _ListComp(self, t):
        with self.delimit("[", "]"):
            self.dispatch(t.elt)
            for gen in t.generators:
                self.dispatch(gen)

    def _GeneratorExp(self, t):
        with self.delimit("(", ")"):
            self.dispatch(t.elt)
            for gen in t.generators:
                self.dispatch(gen)

    def _SetComp(self, t):
        with self.delimit("{", "}"):
            self.dispatch(t.elt)
            for gen in t.generators:
                self.dispatch(gen)

    def _DictComp(self, t):
        with self.delimit("{", "}"):
            self.dispatch(t.key)
            self.write(": ")
            self.dispatch(t.value)
            for gen in t.generators:
                self.dispatch(gen)

    def _comprehension(self, t):
        if getattr(t, 'is_async', False):
            self.write(" async for ")
        else:
            self.write(" for ")
        self.set_precedence(_Precedence.TUPLE, t.target)
        self.dispatch(t.target)
        self.write(" in ")
        self.set_precedence(pnext(_Precedence.TEST), t.iter, *t.ifs)
        self.dispatch(t.iter)
        for if_clause in t.ifs:
            self.write(" if ")
            self.dispatch(if_clause)

    def _IfExp(self, t):
        with self.require_parens(_Precedence.TEST, t):
            self.set_precedence(pnext(_Precedence.TEST), t.body, t.test)
            self.dispatch(t.body)
            self.write(" if ")
            self.dispatch(t.test)
            self.write(" else ")
            self.set_precedence(_Precedence.TEST, t.orelse)
            self.dispatch(t.orelse)

    def _Set(self, t):
        assert(t.elts)  # should be at least one element
        with self.delimit("{", "}"):
            interleave(lambda: self.write(", "), self.dispatch, t.elts)

    def _Dict(self, t):
        def write_key_value_pair(k, v):
            self.dispatch(k)
            self.write(": ")
            self.dispatch(v)

        def write_item(item):
            k, v = item
            if k is None:
                # for dictionary unpacking operator in dicts {**{'y': 2}}
                # see PEP 448 for details
                self.write("**")
                self.set_precedence(_Precedence.EXPR, v)
                self.dispatch(v)
            else:
                write_key_value_pair(k, v)

        with self.delimit("{", "}"):
            interleave(lambda: self.write(", "), write_item, zip(t.keys, t.values))

    def _Tuple(self, t):
        with self.delimit("(", ")"):
            if len(t.elts) == 1:
                elt = t.elts[0]
                self.dispatch(elt)
                self.write(",")
            else:
                interleave(lambda: self.write(", "), self.dispatch, t.elts)

    unop = {
        "Invert": "~",
        "Not": "not",
        "UAdd": "+",
        "USub": "-"
    }

    unop_precedence = {
        "~": _Precedence.FACTOR,
        "not": _Precedence.NOT,
        "+": _Precedence.FACTOR,
        "-": _Precedence.FACTOR,
    }

    def _UnaryOp(self, t):
        operator = self.unop[t.op.__class__.__name__]
        operator_precedence = self.unop_precedence[operator]
        with self.require_parens(operator_precedence, t):
            self.write(operator)
            # factor prefixes (+, -, ~) shouldn't be separated
            # from the value they belong, (e.g: +1 instead of + 1)
            if operator_precedence != _Precedence.FACTOR:
                self.write(" ")
            self.set_precedence(operator_precedence, t.operand)

            if (six.PY2 and
                isinstance(t.op, ast.USub) and isinstance(t.operand, ast.Num)):
                # If we're applying unary minus to a number, parenthesize the number.
                # This is necessary: -2147483648 is different from -(2147483648) on
                # a 32-bit machine (the first is an int, the second a long), and
                # -7j is different from -(7j).  (The first has real part 0.0, the second
                # has real part -0.0.)
                with self.delimit("(", ")"):
                    self.dispatch(t.operand)
            else:
                self.dispatch(t.operand)

    binop = {
        "Add": "+",
        "Sub": "-",
        "Mult": "*",
        "MatMult": "@",
        "Div": "/",
        "Mod": "%",
        "LShift": "<<",
        "RShift": ">>",
        "BitOr": "|",
        "BitXor": "^",
        "BitAnd": "&",
        "FloorDiv": "//",
        "Pow":  "**",
    }

    binop_precedence = {
        "+": _Precedence.ARITH,
        "-": _Precedence.ARITH,
        "*": _Precedence.TERM,
        "@": _Precedence.TERM,
        "/": _Precedence.TERM,
        "%": _Precedence.TERM,
        "<<": _Precedence.SHIFT,
        ">>": _Precedence.SHIFT,
        "|": _Precedence.BOR,
        "^": _Precedence.BXOR,
        "&": _Precedence.BAND,
        "//": _Precedence.TERM,
        "**": _Precedence.POWER,
    }

    binop_rassoc = frozenset(("**",))

    def _BinOp(self, t):
        operator = self.binop[t.op.__class__.__name__]
        operator_precedence = self.binop_precedence[operator]
        with self.require_parens(operator_precedence, t):
            if operator in self.binop_rassoc:
                left_precedence = pnext(operator_precedence)
                right_precedence = operator_precedence
            else:
                left_precedence = operator_precedence
                right_precedence = pnext(operator_precedence)

            self.set_precedence(left_precedence, t.left)
            self.dispatch(t.left)
            self.write(" %s " % operator)
            self.set_precedence(right_precedence, t.right)
            self.dispatch(t.right)

    cmpops = {
        "Eq": "==",
        "NotEq": "!=",
        "Lt": "<",
        "LtE": "<=",
        "Gt": ">",
        "GtE": ">=",
        "Is": "is",
        "IsNot": "is not",
        "In": "in",
        "NotIn": "not in",
    }

    def _Compare(self, t):
        with self.require_parens(_Precedence.CMP, t):
            self.set_precedence(pnext(_Precedence.CMP), t.left, *t.comparators)
            self.dispatch(t.left)
            for o, e in zip(t.ops, t.comparators):
                self.write(" " + self.cmpops[o.__class__.__name__] + " ")
                self.dispatch(e)

    boolops = {
        "And": "and",
        "Or": "or",
    }

    boolop_precedence = {
        "and": _Precedence.AND,
        "or": _Precedence.OR,
    }

    def _BoolOp(self, t):
        operator = self.boolops[t.op.__class__.__name__]

        # use a dict instead of nonlocal for Python 2 compatibility
        op = {"precedence": self.boolop_precedence[operator]}

        def increasing_level_dispatch(t):
            op["precedence"] = pnext(op["precedence"])
            self.set_precedence(op["precedence"], t)
            self.dispatch(t)

        with self.require_parens(op["precedence"], t):
            s = " %s " % operator
            interleave(lambda: self.write(s), increasing_level_dispatch, t.values)

    def _Attribute(self, t):
        self.set_precedence(_Precedence.ATOM, t.value)
        self.dispatch(t.value)
        # Special case: 3.__abs__() is a syntax error, so if t.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if (isinstance(t.value, getattr(ast, 'Constant', getattr(ast, 'Num', None))) and
            isinstance(t.value.n, int)):
            self.write(" ")
        self.write(".")
        self.write(t.attr)

    def _Call(self, t):
        self.set_precedence(_Precedence.ATOM, t.func)
        self.dispatch(t.func)
        with self.delimit("(", ")"):
            comma = False

            # starred arguments last in Python 3.5+, for consistency w/earlier versions
            star_and_kwargs = []
            move_stars_last = sys.version_info[:2] >= (3, 5)

            for e in t.args:
                if move_stars_last and isinstance(e, ast.Starred):
                    star_and_kwargs.append(e)
                else:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.dispatch(e)

            for e in t.keywords:
                # starting from Python 3.5 this denotes a kwargs part of the invocation
                if e.arg is None and move_stars_last:
                    star_and_kwargs.append(e)
                else:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.dispatch(e)

            if move_stars_last:
                for e in star_and_kwargs:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.dispatch(e)

            if sys.version_info[:2] < (3, 5):
                if t.starargs:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.write("*")
                    self.dispatch(t.starargs)
                if t.kwargs:
                    if comma:
                        self.write(", ")
                    else:
                        comma = True
                    self.write("**")
                    self.dispatch(t.kwargs)

    def _Subscript(self, t):
        self.set_precedence(_Precedence.ATOM, t.value)
        self.dispatch(t.value)
        with self.delimit("[", "]"):
            self.dispatch(t.slice)

    def _Starred(self, t):
        self.write("*")
        self.set_precedence(_Precedence.EXPR, t.value)
        self.dispatch(t.value)

    # slice
    def _Ellipsis(self, t):
        self.write("...")

    def _Index(self, t):
        self.set_precedence(_Precedence.TUPLE, t.value)
        self.dispatch(t.value)

    def _Slice(self, t):
        if t.lower:
            self.dispatch(t.lower)
        self.write(":")
        if t.upper:
            self.dispatch(t.upper)
        if t.step:
            self.write(":")
            self.dispatch(t.step)

    def _ExtSlice(self, t):
        interleave(lambda: self.write(', '), self.dispatch, t.dims)

    # argument
    def _arg(self, t):
        self.write(t.arg)
        if t.annotation:
            self.write(": ")
            self.dispatch(t.annotation)

    # others
    def _arguments(self, t):
        first = True
        # normal arguments
        all_args = getattr(t, 'posonlyargs', []) + t.args
        defaults = [None] * (len(all_args) - len(t.defaults)) + t.defaults
        for index, elements in enumerate(zip(all_args, defaults), 1):
            a, d = elements
            if first:
                first = False
            else:
                self.write(", ")
            self.dispatch(a)
            if d:
                self.write("=")
                self.dispatch(d)
            if index == len(getattr(t, 'posonlyargs', ())):
                self.write(", /")

        # varargs, or bare '*' if no varargs but keyword-only arguments present
        if t.vararg or getattr(t, "kwonlyargs", False):
            if first:
                first = False
            else:
                self.write(", ")
            self.write("*")
            if t.vararg:
                if hasattr(t.vararg, 'arg'):
                    self.write(t.vararg.arg)
                    if t.vararg.annotation:
                        self.write(": ")
                        self.dispatch(t.vararg.annotation)
                else:
                    self.write(t.vararg)
                    if getattr(t, 'varargannotation', None):
                        self.write(": ")
                        self.dispatch(t.varargannotation)

        # keyword-only arguments
        if getattr(t, "kwonlyargs", False):
            for a, d in zip(t.kwonlyargs, t.kw_defaults):
                if first:
                    first = False
                else:
                    self.write(", ")
                self.dispatch(a),
                if d:
                    self.write("=")
                    self.dispatch(d)

        # kwargs
        if t.kwarg:
            if first:
                first = False
            else:
                self.write(", ")
            if hasattr(t.kwarg, 'arg'):
                self.write("**" + t.kwarg.arg)
                if t.kwarg.annotation:
                    self.write(": ")
                    self.dispatch(t.kwarg.annotation)
            else:
                self.write("**" + t.kwarg)
                if getattr(t, 'kwargannotation', None):
                    self.write(": ")
                    self.dispatch(t.kwargannotation)

    def _keyword(self, t):
        if t.arg is None:
            # starting from Python 3.5 this denotes a kwargs part of the invocation
            self.write("**")
        else:
            self.write(t.arg)
            self.write("=")
        self.dispatch(t.value)

    def _Lambda(self, t):
        with self.require_parens(_Precedence.TEST, t):
            self.write("lambda ")
            self.dispatch(t.args)
            self.write(": ")
            self.set_precedence(_Precedence.TEST, t.body)
            self.dispatch(t.body)

    def _alias(self, t):
        self.write(t.name)
        if t.asname:
            self.write(" as " + t.asname)

    def _withitem(self, t):
        self.dispatch(t.context_expr)
        if t.optional_vars:
            self.write(" as ")
            self.dispatch(t.optional_vars)
