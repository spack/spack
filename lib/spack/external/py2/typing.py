# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This is a fake set of symbols to allow spack to import typing in python
versions where we do not support type checking (<3)
"""
from collections import defaultdict

# (1) Unparameterized types.
Annotated = object
Any = object
AnyStr = object
ByteString = object
Counter = object
Final = object
Hashable = object
NoReturn = object
Sized = object
SupportsAbs = object
SupportsBytes = object
SupportsComplex = object
SupportsFloat = object
SupportsIndex = object
SupportsInt = object
SupportsRound = object

# (2) Parameterized types.
AbstractSet = defaultdict(lambda: object)
AsyncContextManager = defaultdict(lambda: object)
AsyncGenerator = defaultdict(lambda: object)
AsyncIterable = defaultdict(lambda: object)
AsyncIterator = defaultdict(lambda: object)
Awaitable = defaultdict(lambda: object)
Callable = defaultdict(lambda: object)
ChainMap = defaultdict(lambda: object)
ClassVar = defaultdict(lambda: object)
Collection = defaultdict(lambda: object)
Container = defaultdict(lambda: object)
ContextManager = defaultdict(lambda: object)
Coroutine = defaultdict(lambda: object)
DefaultDict = defaultdict(lambda: object)
Deque = defaultdict(lambda: object)
Dict = defaultdict(lambda: object)
ForwardRef = defaultdict(lambda: object)
FrozenSet = defaultdict(lambda: object)
Generator = defaultdict(lambda: object)
Generic = defaultdict(lambda: object)
ItemsView = defaultdict(lambda: object)
Iterable = defaultdict(lambda: object)
Iterator = defaultdict(lambda: object)
KeysView = defaultdict(lambda: object)
List = defaultdict(lambda: object)
Literal = defaultdict(lambda: object)
Mapping = defaultdict(lambda: object)
MappingView = defaultdict(lambda: object)
MutableMapping = defaultdict(lambda: object)
MutableSequence = defaultdict(lambda: object)
MutableSet = defaultdict(lambda: object)
NamedTuple = defaultdict(lambda: object)
Optional = defaultdict(lambda: object)
OrderedDict = defaultdict(lambda: object)
Reversible = defaultdict(lambda: object)
Sequence = defaultdict(lambda: object)
Set = defaultdict(lambda: object)
Tuple = defaultdict(lambda: object)
Type = defaultdict(lambda: object)
TypedDict = defaultdict(lambda: object)
Union = defaultdict(lambda: object)
ValuesView = defaultdict(lambda: object)

# (3) Type variable declarations.
TypeVar = lambda *args, **kwargs: None

# (4) Functions.
cast = lambda _type, x: x
get_args = None
get_origin = None
get_type_hints = None
no_type_check = None
no_type_check_decorator = None

## typing_extensions
# We get a ModuleNotFoundError when attempting to import anything from typing_extensions
# if we separate this into a separate typing_extensions.py file for some reason.

# (1) Unparameterized types.
IntVar = object
Literal = object
NewType = object
Text = object

# (2) Parameterized types.
Protocol = defaultdict(lambda: object)

# (3) Macro for avoiding evaluation except during type checking.
TYPE_CHECKING = False

# (4) Decorators.
final = lambda x: x
overload = lambda x: x
runtime_checkable = lambda x: x
