import spack.package as sp


class variant_set:

    def __init__(self):
        self.libraries = dict()

    def add(self, name, default=None, buildable=None, conflicts=[], requires=[], **kwargs):
        """
        Create a spack.Variant with extra logic to handle the cases a library
        should be compiled (i.e., passed to b2 via --with-libraries)

        Args:
         name (str): name of the variant

         default (str,bool,None):  The default value for the variant

                                    By default, each variant is enabled. A value of
                                    'None' is converted to 'True'. This is done so
                                    that each variants.add can omit a default
                                    value. The inversion is done because
                                    spack.Variant assumes a default value of
                                    'False'.

         buildable (str): The version string indicating which versions
                          for which the library should be compiled or `None`

         conflicts (list): The variant's conflicts

                           Each conflict is a dict with keys 'when' and 'msg'
                           that are identical to the values for the spack
                           'conflicts' directive.

         requires (list): The variant's requires

                           Each requirement is a dict with keys 'spec', 'when', and
                           'msg' that are identical to the values for the spack
                           'requires' directive.

         kwargs (dict): The rest of the arguments forwarded on to the
                        spack.Variant constructor

                        This should include 'when' which indicates the version
                        range for which the variant is valid. This is distinct
                        from 'buildable' as the latter only indicates when the
                        library should be compiled.

                        For example, the coroutine2 library was introduced in
                        version 1.59.0, but was converted to header-only in version
                        1.64.0. In this case, when="@1.59.0:" and
                        buildable="@1.59.0:1.64.0".

                        Conversely, the exception library was introduced in 1.36.0
                        as header-only, but required compilation after 1.47.0. In
                        this case, when="@1.36.0:" and buildable="@1.47.0:".
        """

        if default is None:
            default = True

        if "sticky" not in kwargs:
            kwargs["sticky"] = True

        sp.variant(name, default=default, **kwargs)

        for c in conflicts:
            sp.conflicts(f"+{name}", when=c["when"], msg=c["msg"])

        for r in requires:
            sp.requires(r["spec"], when=r["when"], msg=r["msg"])

        if buildable is not None:
            self.libraries[name] = buildable

    def libraries_to_build(self, spec):
        """
        The set of libraries that need to be passed to b2 via --with-libraries to be compiled
        """
        libs = list()

        for name, version in self.libraries.items():
            if spec.satisfies("+{0:s} {1:s}".format(name, version)):
                libs.append(name)

        return sorted(libs)

    def all_libraries(self):
        return self.libraries.keys()


# fmt: off

def load():

    variants = variant_set()

    # ----------------------------------------------------------------------
    #  Boost-level configurations
    #
    #    These variants affect every library.
    # ----------------------------------------------------------------------
    variants.add(
        "clanglibcpp",
        default=False,
        when="@1.73.0:",
        conflicts=[
            # Boost 1.85.0 stacktrace added a hard compilation error that has to
            # explicitly be suppressed on some platforms:
            # https://github.com/boostorg/stacktrace/issues/163
            {"when": "@1.85: +stacktrace", "msg": "Stacktrace cannot be used with libc++"},
            # gcc doesn't support libc++
            {"when": "%gcc", "msg": "gcc doesn't support libc++"},
        ],
        description="Compile with clang's libc++ instead of libstdc++",
    )
    variants.add(
        "cxxstd",
        default="14",
        values=(
            "98",
            "03",
            "11",
            "14",
            sp.conditional("17", when="@1.63.0:"),
            sp.conditional("2a", when="@1.73.0:"),
            sp.conditional("20", when="@1.77.0:"),
            sp.conditional("23", when="@1.79.0:"),
            sp.conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        description="C++ standard",
    )
    variants.add(
        "debug",
        default=False,
        description="Build in debug mode",
    )
    variants.add(
        "icu",
        default=False,
        conflicts=[
            {"when": "cxxstd=98", "msg": "ICU requires at least c++11"},
            {"when": "cxxstd=03", "msg": "ICU requires at least c++11"},
        ],
        description="Enable Unicode support via ICU",
    )
    variants.add(
        "pic",
        description="Generate binaries with position-independent code",
    )
    variants.add(
        "shared",
        conflicts=[
            {"when": "~pic", "msg": "Cannot build non-PIC shared libraries"},
        ],
        description="Generate shared libraries (DSO, DLL, etc.)",
    )
    variants.add(
        "multithreaded",
        description="Enable use of multiple threads",
    )
    variants.add(
        "singlethreaded",
        default=False,
        description="Disable use of multiple threads",
    )
    variants.add(
        "taggedlayout",
        default=False,
        when="@1.40.0:",
        conflicts=[
            {"when": "+versionedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library names with build options",
    )
    variants.add(
        "versionedlayout",
        default=False,
        conflicts=[
            {"when": "+taggedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library layout with versioned subdirs",
    )
    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    variants.add(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        when="@1.69.0:",
        description="Default symbol visibility in compiled libraries",
    )
    variants.add(
        "numpy",
        when="@1.63.0:",
        default=False,
        conflicts=[
            {"when": "~python", "msg": "Numpy requires python support"}
        ],
        description="Enable numpy support in Boost.Python",
    )

    # ----------------------------------------------------------------------
    #  Library-level configurations
    #
    #  These variants are specific to a particular library.
    #
    #  mpi and python are not enabled by default because they pull in many
    #  dependencies and/or because there is a great deal of customization
    #  possible (and it would be difficult to choose sensible defaults).
    # ----------------------------------------------------------------------

    variants.add(
        "integer",
        when="@1.9.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.integer requires cxxstd >= 03"},
        ],
        description="Type traits and math functions for integral values",
    )
    variants.add(
        "operators",
        when="@1.9.0:",
        conflicts=[
            {"when": "cxxstd=2a", "msg": "Boost.Operators requires cxxstd <= 17"},
            {"when": "cxxstd=20", "msg": "Boost.Operators requires cxxstd <= 17"},
            {"when": "cxxstd=23", "msg": "Boost.Operators requires cxxstd <= 17"},
            {"when": "cxxstd=26", "msg": "Boost.Operators requires cxxstd <= 17"},
        ],
        description="CRTP helpers to define arithmetic operators for a class",
    )
    variants.add(
        "timer",
        when="@1.9.0:",
        buildable="@1.48.0:",
        description="Timers for measuring wallclock and CPU times",
    )
    variants.add(
        "random",
        when="@1.15.0:",
        buildable="@1.43.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.random requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.random requires cxxstd >= 11"},
        ],
        description="A complete system for random number generation",
    )
    variants.add(
        "regex",
        when="@1.18.0:",
        buildable="@1.18.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.regex requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.regex requires cxxstd >= 11"},
        ],
        description="Perl and POSIX regular expressions",
    )
    variants.add(
        "graph",
        when="@1.18.0:",
        buildable="@1.18.0:",
        description=(
            "Generic components for mathematical graphs (collections of nodes and edges)."
        ),
    )
    variants.add(
        "property_map",
        when="@1.19.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PropertyMap requires cxxstd >= 03"},
        ],
        description="Concepts defining interfaces which map key objects to value objects",
    )
    variants.add(
        "python",
        default=False,
        sticky=False,
        when="@1.19.0:",
        buildable="@1.19.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.python requires cxxstd >= 03"},
        ],
        description="C++ wrapper for interacting with Python.",
    )
    variants.add(
        "conversion",
        when="@1.20.0:",
        description="Extensions to standard casting operators",
    )
    variants.add(
        "lexical_cast",
        when="@1.20.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.LexicalCast requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.LexicalCast requires cxxstd >= 11"},
            {"when": "@:1.76.0 ~math", "msg": "Boost.LexicalCast requires Boost.Math"},
        ],
        description="Type-safe text <-> value conversions",
    )
    variants.add(
        "test",
        when="@1.21.0:",
        buildable="@1.21.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.test requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.test requires cxxstd >= 11"},
        ],
        description=(
            "Simple program testing, full unit testing, and program execution monitoring"
        ),
    )
    variants.add(
        "any",
        when="@1.23.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.any requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.any requires cxxstd >= 11"},
        ],
        description="Safe, generic container for single values of different value types",
    )
    variants.add(
        "function",
        when="@1.23.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.function requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.function requires cxxstd >= 11"},
        ],
        description="Function object wrappers for deferred calls or callbacks",
    )
    variants.add(
        "math",
        when="@1.23.0:",
        buildable="@1.23.0:",
        conflicts=[
            {"when": "~octonions", "msg": "Boost.Math requires Boost.Octonions"},
            {"when": "~quaternions", "msg": "Boost.Math requires Boost.Quaternions"},
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.Math requires at least c++11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.Math requires at least c++11"},
        ],
        description=(
            "Extensive collection of integer, real, and complex mathematical operations"
        ),
    )
    variants.add(
        "octonions",
        when="@1.23.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.math_octonion requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.math_octonion requires cxxstd >= 11"},
        ],
        description="Octonions",
    )
    variants.add(
        "quaternions",
        when="@1.23.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.math_quaternion requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.math_quaternion requires cxxstd >= 11"},
        ],
        description="Quaternions",
    )
    variants.add(
        "bind",
        when="@1.25.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.bind requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.bind requires cxxstd >= 11"},
        ],
        description="Generalizations of the std::bind and std::mem_fn family",
    )
    variants.add(
        "thread",
        when="@1.25.0:",
        buildable="@1.25.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.thread requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.thread requires cxxstd >= 11"},
        ],
        description="Portable C++ multi-threading",
    )
    variants.add(
        "preprocessor",
        when="@1.26.0:",
        conflicts=[
            {"when": "@1.75.0: cxxstd=98", "msg": "Boost.Preprocessor requires cxxstd >= 11"},
            {"when": "@1.75.0: cxxstd=03", "msg": "Boost.Preprocessor requires cxxstd >= 11"},
        ],
        description="Preprocessor metaprogramming tools including repetition and recursion",
    )
    variants.add(
        "date_time",
        when="@1.29.0:",
        buildable="@1.29.0:",
        description="Calculate, format, and convert dates and times",
    )
    variants.add(
        "signals",
        default=False,
        when="@1.29.0:1.68.0",
        buildable="@1.29.0:1.68.0",
        conflicts=[
            {"when": "@1.69.0:", "msg": "Boost.signals was removed in 1.68.0"}
        ],
        requires=[
            {
                "spec": "+signals",
                "when": "platform=windows @1.29.0:1.68.0",
                "msg": "Boost.Signals is requires on Windows"
            }
        ],
        description="Managed signals & slots callback implementation",
    )
    variants.add(
        "filesystem",
        when="@1.30.0:",
        buildable="@1.30.0:",
        description=(
            "Portable facilities to query and manipulate paths, files, and directories"
        ),
    )
    variants.add(
        "spirit",
        when="@1.30.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Spirit requires cxxstd >= 03"}
        ],
        description="LL parser framework using EBNF grammars",
    )
    variants.add(
        "program_options",
        when="@1.32.0:",
        buildable="@1.32.0:",
        description=(
            "Parse command-line options similar to POSIX getops or from config files"
        ),
    )
    variants.add(
        "serialization",
        when="@1.32.0:",
        buildable="@1.32.0:",
        description="Serialization for persistence and marshalling",
    )
    variants.add(
        "container_hash",
        when="@1.33.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.container_hash requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.container_hash requires cxxstd >= 11"},
        ],
        description="Hash function objects for user-defined types",
    )
    variants.add(
        "iostreams",
        when="@1.33.0:",
        buildable="@1.33.0:",
        description="Streams, stream buffers, and i/o filters",
    )
    variants.add(
        "parameter",
        when="@1.33.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Parameter requires at least c++03"},
        ],
        description="Write functions that accept arguments by name",
    )
    variants.add(
        "wave",
        when="@1.33.0:",
        buildable="@1.33.0:",
        conflicts=[
            {"when": "@1.79.0: cxxstd=98", "msg": "Boost.Wave requires cxxstd >= 11"},
            {"when": "@1.79.0: cxxstd=03", "msg": "Boost.Wave requires cxxstd >= 11"},
        ],
        description="Highly configurable implementation of the mandatory C99/C++ preprocessor",
    )
    variants.add(
        "typeof",
        when="@1.34.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.typeof requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.typeof requires cxxstd >= 11"},
        ],
        description="Typeof operator emulation",
    )
    variants.add(
        "asio",
        when="@1.35.0:",
        description="Portable networking and other low-level I/O",
    )
    variants.add(
        "gil",
        when="@1.35.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.GIL requires at least c++11"},
            {"when": "cxxstd=03", "msg": "Boost.GIL requires at least c++11"},
        ],
        description="Generic Image Library",
    )
    variants.add(
        "mpi",
        default=False,
        sticky=False,
        when="@1.35.0:",
        buildable="@1.35.0:",
        conflicts=[
            # 1.64 uses out-dated APIs (https://github.com/spack/spack/issues/3963)
            {"when": "@1.64.0 +python", "msg": "Boost.MPI@1.64.0 does not support python"},
            {"when": "@1.72.0 cxxstd=98", "msg": "Boost.MPI@1.72.0 does not support C++98"},
            {"when": "@1.87.0: ~python", "msg": "Boost.MPI requires Boost.Numpy"},
        ],
        description=(
            "C++ wrapper to the Message Passing Interface for distributed-memory parallelism"
        ),
    )
    variants.add(
        "system",
        when="@1.35.0:",
        buildable="@1.35.0:",
        conflicts=[
            # gcc on Darwin incorrectly detects 'mutex'
            # https://github.com/STEllAR-GROUP/hpx/issues/5442#issuecomment-878889166
            {"when": "platform=darwin %gcc @:1.76", "msg": "Boost.System bug"}
        ],
        description="Extensible error reporting",
    )
    variants.add(
        "exception",
        when="@1.36.0:",
        buildable="@1.47.0:",
        description=(
            "Transport arbitrary data in exceptions, and exceptions between threads"
        ),
    )
    variants.add(
        "unordered",
        when="@1.36.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.unordered requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.unordered requires cxxstd >= 11"},
        ],
        description="Unordered associative containers",
    )
    variants.add(
        "signals2",
        when="@1.39.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Signals2 requires cxxstd >= 03"}
        ],
        requires=[
            {
                "spec": "+signals2",
                "when": "platform=windows @1.68.0:",
                "msg": "Boost.Signals2 is requires on Windows"
            }
        ],
        description="Thread-safe managed signals & slots callback implementation",
    )
    variants.add(
        "graph_parallel",
        default=False,
        when="@1.40.0:",
        buildable="@1.40.0:",
        conflicts=[
            {"when": "~mpi", "msg": "Boost.GraphParallel requires Boost.MPI"},
            {"when": "~graph", "msg": "Boost.GraphParallel requires Boost.Graph"},
        ],
        description="Scalable parallel version of Boost.Graph using MPI multiprocessing",
    )
    variants.add(
        "property_tree",
        when="@1.41.0:",
        description="Structured storage of configuration data",
    )
    variants.add(
        "functional_factory",
        when="@1.43.0:",
        description="Dynamic and static creation of function objects",
    )
    variants.add(
        "functional_forward",
        when="@1.43.0:",
        description="Allow arbitrary arguments in function objects",
    )
    variants.add(
        "msm",
        when="@1.44.0:",
        description="Meta-State Machine: expressive UML2 finite state machines",
    )
    variants.add(
        "polygon",
        when="@1.44.0:",
        description="Voronoi diagram manipulations for planar polygons",
    )
    variants.add(
        "icl",
        when="@1.46.0:",
        description="Interval sets and maps",
    )
    variants.add(
        "chrono",
        when="@1.47.0:",
        buildable="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.chrono requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.chrono requires cxxstd >= 11"},
        ],
        description="Extended version of C++11 time utilities",
    )
    variants.add(
        "geometry",
        when="@1.47.0:",
        conflicts=[
            {"when": "@1.75.0: cxxstd=98", "msg": "Boost.Geometry requires cxxstd >= 14"},
            {"when": "@1.75.0: cxxstd=03", "msg": "Boost.Geometry requires cxxstd >= 14"},
            {"when": "@1.75.0: cxxstd=11", "msg": "Boost.Geometry requires cxxstd >= 14"},
        ],
        description="Geometric algorithms, primitives, and spatial indices.",
    )
    variants.add(
        "phoenix",
        when="@1.47.0:",
        description="Functional programming for C++",
    )
    variants.add(
        "ratio",
        when="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Ratio requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Ratio requires cxxstd >= 11"},
        ],
        description="Compile-time rational arithmetic",
    )
    variants.add(
        "container",
        when="@1.48.0:",
        buildable="@1.56.0:",  # Extended Allocators need to be compiled
        description="Standard library containers and extensions",
    )
    variants.add(
        "locale",
        default=False,
        when="@1.48.0:",
        buildable="@1.48.0:",
        conflicts=[
            {"when": "~icu", "msg": "Boost.Locale requires Unicode support"}
        ],
        description="Localization and Unicode facilities",
    )
    variants.add(
        "move",
        when="@1.48.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Move requires cxxstd >= 03"},
        ],
        description="Portable move semantics for C++03",
    )
    variants.add(
        "heap",
        when="@1.49.0:",
        description="Priority queue data structures",
    )
    variants.add(
        "algorithm",
        when="@1.50.0:",
        description="A collection of useful generic algorithms",
    )
    variants.add(
        "functional_overloaded_function",
        when="@1.50.0:",
        description="Overload different functions into a single function object",
    )
    variants.add(
        "identity_type",
        when="@1.50.0:",
        description="Safely pass user-defined types as macro parameters",
    )
    variants.add(
        "local_function",
        when="@1.50.0:",
        description="Declare and use functions in a local scope",
    )
    variants.add(
        "context",
        when="@1.51.0:",
        buildable="@1.51.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="Cooperative multitasking on a single thread",
    )
    variants.add(
        "atomic",
        when="@1.53.0:",
        buildable="@1.53.0:",
        description="C++11-style atomic<>.",
    )
    variants.add(
        "coroutine",
        when="@1.53.0:",
        buildable="@1.54.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Coroutine requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Coroutine requires cxxstd >= 11"},
            {"when": "~context", "msg": "Boost.Coroutine requires Boost.Context"},
        ],
        description="DEPRECATED use coroutine2",
    )
    variants.add(
        "lockfree",
        when="@1.53.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.LockFree requires cxxstd >= 03"}
        ],
        description="Lockfree queue, stack, and SP/SC queue",
    )
    variants.add(
        "multiprecision",
        when="@1.53.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.Multiprecision requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.Multiprecision requires cxxstd >= 11"},
        ],
        description=(
            "Extended precision arithmetic for floating point, integer, and rational types"
        ),
    )
    variants.add(
        "odeint",
        when="@1.53.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Odeint requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Odeint requires cxxstd >= 11"},
            {"when": "~math", "msg": "Boost.Odeint requires Boost.Math"}
        ],
        description="Solver for ordinary differential equations",
    )
    variants.add(
        "log",
        when="@1.54.0:",
        buildable="@1.54.0:",
        description="Simple, extensible, and fast logging",
    )
    variants.add(
        "tti",
        when="@1.54.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.tti requires cxxstd >= 03"}
        ],
        description="Type Traits Introspection",
    )
    variants.add(
        "type_erasure",
        when="@1.54.0:",
        buildable="@1.60.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.TypeErasure requires cxxstd >= 03"}
        ],
        description="Runtime polymorphism based on concepts",
    )
    variants.add(
        "predef",
        when="@1.55.0:",
        description="Macros to identify compilers and their versions",
    )
    variants.add(
        "align",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Align requires cxxstd >= 03"}
        ],
        description="Memory alignment facilities",
    )
    variants.add(
        "core",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.core requires cxxstd >= 03"},
        ],
        description="Simple core utilities with minimal dependencies",
    )
    variants.add(
        "throw_exception",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.ThrowException requires cxxstd >= 03"}
        ],
        description="Enhanced exception handling, including source locations",
    )
    variants.add(
        "type_index",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.TypeIndex requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.TypeIndex requires cxxstd >= 11"},
        ],
        description="Runtime/compile-time copyable type info",
    )
    variants.add(
        "endian",
        when="@1.58.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Endian requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Endian requires cxxstd >= 11"},
        ],
        description="Manipulate the endianness of integers and user-defined types"
    )
    variants.add(
        "sort",
        when="@1.58.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Sort requires cxxstd >= 03"}
        ],
        description="High-performance sorting routines",
    )
    variants.add(
        "convert",
        when="@1.59.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Convert requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Convert requires cxxstd >= 11"},
        ],
        description="An extensible and configurable type-conversion framework",
    )
    variants.add(
        "coroutine2",
        when="@1.59.0:",
        buildable="@1.59.0:1.64.0",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Coroutine2 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Coroutine2 requires cxxstd >= 11"},
            {"when": "~context", "msg": "Boost.Coroutine2 requires Boost.Context"}
        ],
        description=(
            "Subroutines that allow suspending and resuming execution at certain locations"
        ),
    )
    variants.add(
        "vmd",
        when="@1.60.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.VMD requires cxxstd >= 03"},
            {"when": "~preprocessor", "msg": "Boost.VMD requires Boost.Preprocessor"}
        ],
        description="Variadic macros for Boost.Preprocessor",
    )
    variants.add(
        "compute",
        when="@1.61.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Compute requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Compute requires cxxstd >= 11"},
        ],
        description="Multi-core CPU and GPGPU computing based on OpenCL",
    )
    variants.add(
        "dll",
        when="@1.61.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.dll requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.dll requires cxxstd >= 11"},
        ],
        description="Load plugins from DLLs or DSOs",
    )
    variants.add(
        "hana",
        when="@1.61.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Hana requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Hana requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Hana requires cxxstd >= 14"},
        ],
        description=(
            "Modern metaprogramming suited for computations on both types and values"
        ),
    )
    variants.add(
        "metaparse",
        when="@1.61.0:1.65.1",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.MetaParse requires cxxstd >= 03"}
        ],
        description="Generate compile-time parsers for embedded DSL code",
    )
    variants.add(
        "fiber",
        when="@1.62.0:",
        buildable="@1.62.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Fiber requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Fiber requires cxxstd >= 11"},
            {"when": "~context", "msg": "Boost.Fiber requires Boost.Context"}
        ],
        description="Lightweight userland threads",
    )
    variants.add(
        "qvm",
        when="@1.62.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.QVM requires cxxstd >= 03"},
        ],
        description="Generic operations for Quaternions, Vectors, and Matrices",
    )
    variants.add(
        "process",
        when="@1.64.0:",
        buildable="@1.64.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Process requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Process requires cxxstd >= 11"},
        ],
        description="Portable process creation and management",
    )
    variants.add(
        "context-impl",
        when="@1.65.0:",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="The backend for Boost.Context",
    )
    variants.add(
        "poly_collection",
        when="@1.65.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PolyCollection requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.PolyCollection requires cxxstd >= 11"},
        ],
        description="Fast containers of polymorphic objects",
    )
    variants.add(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy, and print backtraces",
    )
    variants.add(
        "beast",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Beast requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Beast requires cxxstd >= 11"},
            {"when": "~asio", "msg": "Boost.Beast requires Boost.Asio"},
        ],
        description="Portable HTTP, WebSocket, and network operations using Boost.Asio",
    )
    variants.add(
        "callable_traits",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.CallableTraits requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.CallableTraits requires cxxstd >= 11"},
        ],
        description="Compile-time inspection and manipulation of callable types",
    )
    variants.add(
        "mp11",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.MP11 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.MP11 requires cxxstd >= 11"},
        ],
        description="C++11 metaprogramming",
    )
    variants.add(
        "contract",
        when="@1.67.0:",
        buildable="@1.67.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Contract requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Contract requires cxxstd >= 11"},
        ],
        description=(
            "Contract programming with subcontracting, class invariants, and pre/postconditions."
        ),
    )
    variants.add(
        "hof",
        when="@1.67.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.HoF requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.HoF requires cxxstd >= 11"},
        ],
        description="Higher-order functions",
    )
    variants.add(
        "yap",
        when="@1.68.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.YAP requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.YAP requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.YAP requires cxxstd >= 14"},
        ],
        description="Expression-template concepts and composable algorithms",
    )
    variants.add(
        "parameter_python",
        default=False,
        when="@1.69.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Parameter python bindings require cxxstd >= 03"},
            {"when": "~python", "msg": "Parameter Python bindings require python support"},
            {"when": "~parameter", "msg": "Parameter Python bindings require Boost.Parameter"}
        ],
        description="Python bindings for Boost.Parameter",
    )
    variants.add(
        "safe_numerics",
        when="@1.69.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.SafeNumerics requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.SafeNumerics requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.SafeNumerics requires cxxstd >= 14"},
        ],
        description="Guaranteed correct integer arithmetic",
    )
    variants.add(
        "spirit_repository",
        when="@1.69.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.SpiritRepository requires cxxstd >= 03"}
        ],
        description="Reusable components for Qi parsers and Karma generators",
    )
    variants.add(
        "histogram",
        when="@1.70.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "@1.71.0: ~variant2", "msg": "Boost.Histogram requires Boost.Variant2"},
        ],
        description="Fast multi-dimensional histogram",
    )
    variants.add(
        "outcome",
        when="@1.70.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Outcome requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Outcome requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Outcome requires cxxstd >= 14"},
        ],
        description=(
            "Deterministic failure handling, partially simulating lightweight exceptions"
        ),
    )
    variants.add(
        "string_ref",
        when="@1.71.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.StringRef requires cxxstd >= 03"},
        ],
        description="Non-owning reference to a string",
    )
    variants.add(
        "variant2",
        when="@1.71.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Variant2 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Variant2 requires cxxstd >= 11"},
        ],
        description="A never-valueless, strong-guarantee tagged union",
    )
    variants.add(
        "nowide",
        default=False,
        when="@1.73.0:",
        buildable="@1.73.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Nowide requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Nowide requires cxxstd >= 11"},
        ],
        description="Standard library functions with UTF-8 API on Windows",
    )
    variants.add(
        "static_string",
        when="@1.73.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.StaticString requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.StaticString requires cxxstd >= 11"},
        ],
        description="A fixed-capacity, dynamically-sized string",
    )
    variants.add(
        "stl_interfaces",
        when="@1.74.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.STLInterfaces requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.STLInterfaces requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.STLInterfaces requires cxxstd >= 14"},
        ],
        description="Simplifies writing STL-compliant containers and ranges",
    )
    variants.add(
        "json",
        when="@1.75.0:",
        buildable="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.JSON requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.JSON requires cxxstd >= 11"},
        ],
        description="JSON parsing, serialization, and DOM in C++11",
    )
    variants.add(
        "leaf",
        when="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.LEAF requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.LEAF requires cxxstd >= 11"},
        ],
        description="Lightweight error-handling",
    )
    variants.add(
        "pfr",
        when="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PFR requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.PFR requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.PFR requires cxxstd >= 14"},
        ],
        description="Basic reflection for user-defined types",
    )
    variants.add(
        "describe",
        when="@1.77.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Describe requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Describe requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Describe requires cxxstd >= 14"},
        ],
        description="Advanced reflection for user-defined types",
    )
    variants.add(
        "lambda2",
        when="@1.77.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.lambda2 requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.lambda2 requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.lambda2 requires cxxstd >= 14"},
        ],
        description="Adds std::bind features to C++14 lambdas",
    )
    variants.add(
        "property_map_parallel",
        default=False,
        when="@1.77.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PropertyMapParallel requires cxxstd >= 03"},
            {
                "when": "~graph_parallel",
                "msg": "Boost.PropertyMap (Parallel) requires Boost.GraphParallel"
            },
            {
                "when": "~property_map",
                "msg": "Boost.PropertyMap (Parallel) requires Boost.PropertyMap"
            }
        ],
        description="Parallel extensions to Property Map for use with Parallel Graph",
    )
    variants.add(
        "url",
        when="@1.81.0:",
        buildable="@1.81.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.URL requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.URL requires cxxstd >= 11"},
            {"when": "~variant2", "msg": "Boost.url requires Boost.variant2"},
        ],
        description="Portable model for parsing URLs and URIs",
    )
    variants.add(
        "cobalt",
        default=False,
        when="@1.84.0:",
        buildable="@1.84.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=03", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=11", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=14", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=17", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "~leaf", "msg": "Boost.cobalt requires Boost.leaf"},
            {"when": "~variant2", "msg": "Boost.cobalt requires Boost.variant2"},
        ],
        description=(
            "Simple single-threaded asynchronicity akin to node.js and asyncio in python"
        ),
    )
    variants.add(
        "charconv",
        when="@1.85.0:",
        buildable="@1.85.0:",
        description="An implementation of C++20's <charconv> in C++11",
    )

    return variants
