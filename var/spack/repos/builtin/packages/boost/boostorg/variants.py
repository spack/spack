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
        "math",
        when="@1.23.0:",
        buildable="@1.23.0:",
        conflicts=[
            {"when": "~octonions", "msg": "Boost.Math requires Boost.Octonions"},
            {"when": "~quaternions", "msg": "Boost.Math requires Boost.Quaternions"},
        ],
        description=(
            "Extensive collection of integer, real, and complex mathematical operations"
        ),
    )
    variants.add(
        "octonions",
        when="@1.23.0:",
        description="Octonions",
    )
    variants.add(
        "quaternions",
        when="@1.23.0:",
        description="Quaternions",
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
        "iostreams",
        when="@1.33.0:",
        buildable="@1.33.0:",
        description="Streams, stream buffers, and i/o filters",
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
        "exception",
        when="@1.36.0:",
        buildable="@1.47.0:",
        description=(
            "Transport arbitrary data in exceptions, and exceptions between threads"
        ),
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
        "log",
        when="@1.54.0:",
        buildable="@1.54.0:",
        description="Simple, extensible, and fast logging",
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
        "context-impl",
        when="@1.65.0:",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="The backend for Boost.Context",
    )
    variants.add(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy, and print backtraces",
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
