%=============================================================================
% Generate
%=============================================================================

%-----------------------------------------------------------------------------
% Environments
%-----------------------------------------------------------------------------
%
% Nodes in the concretized graph are identified by (Package, Env) --
% where available environments come from hardware.yaml, and which
% environment a node is built for depends on whether it is a build
% dependency or a link/run/test dependency.
%

%-----------------------------------------------------------------------------
% Version semantics
%-----------------------------------------------------------------------------

% versions are declared w/priority -- declared with priority implies declared
version_declared(Package, Version) :- version_declared(Package, Version, _).

% Every node in the graph has exactly one version
1 { version(Package, Version) : version_possible(Package, Version) } 1
 :- node(Package).

% If a version is declared but conflicted, it's not possible.
version_possible(Package, Version)
 :- version_declared(Package, Version), not version_conflict(Package, Version).

version_weight(Package, Version, Weight)
 :- version(Package, Version), version_declared(Package, Version, Weight).

#defined version_conflict/2.

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(Package, Dependency) :- depends_on(Package, Dependency, _).

% declared dependencies are real if they're not virtual
depends_on(Package, Dependency, Type)
 :- declared_dependency(Package, Dependency, Type), not virtual(Dependency),
    node(Package).

% if you declare a dependency on a virtual, you depend on one of its providers
1 {
  depends_on(Package, Provider, Type)
  : provides_virtual(Provider, Virtual)
} 1
 :- declared_dependency(Package, Virtual, Type),
    virtual(Virtual),
    node(Package).

% if a virtual was required by some root spec, one provider is in the DAG
1 { node(Package) : provides_virtual(Package, Virtual) } 1
 :- virtual_node(Virtual).

% for any virtual, there can be at most one provider in the DAG
provider(Package, Virtual)
 :- node(Package), provides_virtual(Package, Virtual).
0 { provider(Package, Virtual) : node(Package) } 1 :- virtual(Virtual).

% give dependents the virtuals they want
provider_weight(Dependency, Weight)
 :- virtual(Virtual), depends_on(Package, Dependency),
    provider(Dependency, Virtual),
    pkg_provider_preference(Package, Virtual, Dependency, Weight).
provider_weight(Dependency, Weight)
 :- virtual(Virtual), depends_on(Package, Dependency),
    provider(Dependency, Virtual),
    not pkg_provider_preference(Package, Virtual, Dependency, _),
    default_provider_preference(Virtual, Dependency, Weight).

% if there's no preference for something, it costs 100 to discourage its
% use with minimization
provider_weight(Dependency, 100)
 :- virtual(Virtual),
    provider(Dependency, Virtual),
    depends_on(Package, Dependency),
    not pkg_provider_preference(Package, Virtual, Dependency, _),
    not default_provider_preference(Virtual, Dependency, _).

% all nodes must be reachable from some root
needed(Package) :- root(Package), node(Package).
needed(Dependency) :- root(Package), depends_on(Package, Dependency).
needed(Dependency)
 :- needed(Package), depends_on(Package, Dependency), node(Package).
:- node(Package), not needed(Package).

% real dependencies imply new nodes.
node(Dependency) :- node(Package), depends_on(Package, Dependency).

% do not warn if generated program contains none of these.
#defined depends_on/3.
#defined declared_dependency/3.
#defined virtual/1.
#defined virtual_node/1.
#defined provides_virtual/2.
#defined pkg_provider_preference/4.
#defined default_provider_preference/3.
#defined root/1.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% one variant value for single-valued variants.
1 {
  variant_value(Package, Variant, Value)
  : variant_possible_value(Package, Variant, Value)
} 1
 :- node(Package),
    variant(Package, Variant),
    variant_single_value(Package, Variant).

% at least one variant value for multi-valued variants.
1 {
 variant_value(Package, Variant, Value)
 : variant_possible_value(Package, Variant, Value)
}
 :- node(Package),
    variant(Package, Variant),
    not variant_single_value(Package, Variant).

% if a variant is set to anything, it is considered 'set'.
variant_set(Package, Variant) :- variant_set(Package, Variant, _).

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(Package, Variant, Value)
 :- node(Package),
    variant(Package, Variant),
    variant_set(Package, Variant, Value).

% prefer default values.
variant_not_default(Package, Variant, Value, 1)
 :- variant_value(Package, Variant, Value),
    not variant_default_value(Package, Variant, Value),
    node(Package).

variant_not_default(Package, Variant, Value, 0)
 :- variant_value(Package, Variant, Value),
    variant_default_value(Package, Variant, Value),
    node(Package).

% suppress wranings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant/2.
#defined variant_set/3.
#defined variant_single_value/2.
#defined variant_default_value/3.
#defined variant_possible_value/3.

%-----------------------------------------------------------------------------
% Platform/OS semantics
%-----------------------------------------------------------------------------
% one platform, os per node
% TODO: convert these to use optimization, like targets.
1 { node_platform(Package, Platform) : node_platform(Packagee, Platform) } 1
  :- node(Package).
1 { node_os(Package, OS) : node_os(Package, OS) } 1 :- node(Package).

% arch fields for pkg P are set if set to anything
node_platform_set(Package) :- node_platform_set(Package, _).
node_os_set(Package) :- node_os_set(Package, _).

% if no platform/os is set, fall back to the defaults
node_platform(Package, Platform)
 :- node(Package),
    not node_platform_set(Package),
    node_platform_default(Platform).
node_os(Package, OS)
  :- node(Package), not node_os_set(Package), node_os_default(OS).

% setting os/platform on a node is a hard constraint
node_platform(Package, Platform)
 :- node(Package), node_platform_set(Package, Platform).
node_os(Package, OS) :- node(Package), node_os_set(Package, OS).

% avoid info warnings (see variants)
#defined node_platform_set/2.
#defined node_os_set/2.

%-----------------------------------------------------------------------------
% Target semantics
%-----------------------------------------------------------------------------
% one target per node -- optimization will pick the "best" one
1 { node_target(Package, Target) : target(Target) } 1 :- node(Package).

% can't use targets on node if the compiler for the node doesn't support them
:- node_target(Package, Target),
   not compiler_supports_target(Compiler, Version, Target),
   node_compiler(Package, Compiler),
   node_compiler_version(Package, Compiler, Version).

% if a target is set explicitly, respect it
node_target(Package, Target)
 :- node(Package), node_target_set(Package, Target).

% each node has the weight of its assigned target
node_target_weight(Package, Weight)
 :- node(Package), node_target(Package, Target), target_weight(Target, Weight).

#defined node_target_set/2.

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------

% one compiler per node
1 { node_compiler(Package, Compiler) : compiler(Compiler) } 1 :- node(Package).
1 { node_compiler_version(Package, Compiler, Version)
    : compiler_version(Compiler, Version) } 1 :- node(Package).
1 { compiler_weight(Package, Weight) : compiler_weight(Package, Weight) } 1
 :- node(Package).

% dependencies imply we should try to match hard compiler constraints
% todo: look at what to do about intersecting constraints here. we'd
% ideally go with the "lowest" pref in the DAG
node_compiler_match_pref(Package, Compiler)
 :- node_compiler_hard(Package, Compiler).
node_compiler_match_pref(Dependency, Compiler)
 :- depends_on(Package, Dependency),
    node_compiler_match_pref(Package, Compiler),
    not node_compiler_hard(Dependency, _).
compiler_match(Package, 1)
 :- node_compiler(Package, Compiler),
    node_compiler_match_pref(Package, Compiler).

node_compiler_version_match_pref(Package, Compiler, V)
 :- node_compiler_version_hard(Package, Compiler, V).
node_compiler_version_match_pref(Dependency, Compiler, V)
 :- depends_on(Package, Dependency),
    node_compiler_version_match_pref(Package, Compiler, V),
    not node_compiler_version_hard(Dependency, Compiler, _).
compiler_version_match(Package, 1)
 :- node_compiler_version(Package, Compiler, V),
    node_compiler_version_match_pref(Package, Compiler, V).

#defined node_compiler_hard/2.
#defined node_compiler_version_hard/3.

% compilers weighted by preference acccording to packages.yaml
compiler_weight(Package, Weight)
 :- node_compiler(Package, Compiler),
    node_compiler_version(Package, Compiler, V),
    node_compiler_preference(Package, Compiler, V, Weight).
compiler_weight(Package, Weight)
 :- node_compiler(Package, Compiler),
    node_compiler_version(Package, Compiler, V),
    not node_compiler_preference(Package, Compiler, _, _),
    default_compiler_preference(Compiler, V, Weight).
compiler_weight(Package, 100)
 :- node_compiler(Package, Compiler),
    node_compiler_version(Package, Compiler, Version),
    not node_compiler_preference(Package, Compiler, _, _),
    not default_compiler_preference(Compiler, _, _).

#defined node_compiler_preference/4.
#defined default_compiler_preference/3.

%-----------------------------------------------------------------------------
% Compiler flags
%-----------------------------------------------------------------------------
% propagate flags when compilers match
inherit_flags(Package, Dependency)
 :- depends_on(Package, Dependency),
    node_compiler(Package, Compiler),
    node_compiler(Dependency, Compiler),
    compiler(Compiler), flag_type(FlagType).
node_flag_inherited(Dependency, FlagType, Flag)
 :- node_flag_set(Package, FlagType, Flag), inherit_flags(Package, Dependency).
node_flag_inherited(Dependency, FlagType, Flag)
 :- node_flag_inherited(Package, FlagType, Flag),
    inherit_flags(Package, Dependency).

% node with flags set to anythingg is "set"
node_flag_set(Package) :- node_flag_set(Package, _, _).

% remember where flags came from
node_flag_source(Package, Package) :- node_flag_set(Package).
node_flag_source(Dependency, Q)
 :- node_flag_source(Package, Q), inherit_flags(Package, Dependency).

% compiler flags from compilers.yaml are put on nodes if compiler matches
node_flag(Package, FlagType, Flag),
node_flag_compiler_default(Package)
 :- not node_flag_set(Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler(Package, Compiler),
    node_compiler_version(Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

% if a flag is set to something or inherited, it's included
node_flag(Package, FlagType, Flag) :- node_flag_set(Package, FlagType, Flag).
node_flag(Package, FlagType, Flag)
 :- node_flag_inherited(Package, FlagType, Flag).

% if no node flags are set for a type, there are no flags.
no_flags(Package, FlagType)
 :- not node_flag(Package, FlagType, _), node(Package), flag_type(FlagType).

#defined compiler_version_flag/4.
#defined node_flag/3.
#defined node_flag_set/3.

%-----------------------------------------------------------------------------
% How to optimize the spec (high to low priority)
%-----------------------------------------------------------------------------
% weight root preferences higher
%
% TODO: how best to deal with this issue?  It's not clear how best to
% weight all the constraints. Without this root preference, `spack solve
% hdf5` will pick mpich instead of openmpi, even if openmpi is the
% preferred provider, because openmpi has a version constraint on hwloc.
% It ends up choosing between settling for an old version of hwloc, or
% picking the second-best provider.  This workaround weights root
% preferences higher so that hdf5's prefs are more important, but it's
% not clear this is a general solution.  It would be nice to weight by
% distance to root, but that seems to slow down the solve a lot.
%
% One option is to make preferences hard constraints.  Or maybe we need
% to look more closely at where a constraint came from and factor that
% into our weights.  e.g., a non-default variant resulting from a version
% constraint counts like a version constraint.  Needs more thought later.
%
root(Package, 2) :- root(Package), node(Package).
root(Dependency, 1) :- not root(Dependency), node(Dependency).

% prefer default variants
#minimize {
    Weight*R@10,Package,Variant,Value
    : variant_not_default(Package, Variant, Value, Weight), root(Package, R)
}.

% pick most preferred virtual providers
#minimize{
    Weight*R@9,Provider : provider_weight(Provider, Weight), root(Package, R)
}.

% prefer more recent versions.
#minimize{
    Weight@8,Package,Version : version_weight(Package, Version, Weight)
}.

% compiler preferences
#maximize{ Weight@7,Package : compiler_match(Package, Weight) }.
#minimize{ Weight@6,Package : compiler_weight(Package, Weight) }.

% fastest target for node

% TODO: if these are slightly different by compiler (e.g., skylake is
% best, gcc supports skylake and broadweell, clang's best is haswell)
% things seem to get really slow.
#minimize{ Weight@5,Package : node_target_weight(Package, Weight) }.

%============================================================================
% General Constraints
%============================================================================

%----------------------------------------------------------------------------
% Available compilers
%----------------------------------------------------------------------------
compiler("clang").
compiler_version("clang", "10.0.0-apple") :- compiler("clang").
compiler("gcc").
compiler_version("gcc", "8.2.0") :- compiler("gcc").

%----------------------------------------------------------------------------
% Default compiler preferences
%----------------------------------------------------------------------------
default_compiler_preference("clang", "10.0.0-apple", 0).
default_compiler_preference("gcc", "8.2.0", 1).

%----------------------------------------------------------------------------
% Default architecture
%----------------------------------------------------------------------------
node_platform_default("darwin").
node_os_default("mojave").
node_target_default("skylake").

%----------------------------------------------------------------------------
% Target compatibility
%----------------------------------------------------------------------------
compiler_supports_target("gcc", "8.2.0", "skylake").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "broadwell").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "haswell").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "ivybridge").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "sandybridge").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "westmere").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "nehalem").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "core2").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "nocona").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("gcc", "8.2.0", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "skylake").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "broadwell").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "haswell").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "ivybridge").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "sandybridge").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "westmere").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "nehalem").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "core2").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "nocona").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
compiler_supports_target("clang", "10.0.0-apple", "x86_64").
target("skylake").
target_family("skylake", "x86_64").
target_parent("skylake", "broadwell").
target_weight("skylake", 0).

target("broadwell").
target_family("broadwell", "x86_64").
target_parent("broadwell", "haswell").
target_weight("broadwell", 1).

target("haswell").
target_family("haswell", "x86_64").
target_parent("haswell", "ivybridge").
target_weight("haswell", 2).

target("ivybridge").
target_family("ivybridge", "x86_64").
target_parent("ivybridge", "sandybridge").
target_weight("ivybridge", 3).

target("sandybridge").
target_family("sandybridge", "x86_64").
target_parent("sandybridge", "westmere").
target_weight("sandybridge", 4).

target("westmere").
target_family("westmere", "x86_64").
target_parent("westmere", "nehalem").
target_weight("westmere", 5).

target("nehalem").
target_family("nehalem", "x86_64").
target_parent("nehalem", "core2").
target_weight("nehalem", 6).

target("core2").
target_family("core2", "x86_64").
target_parent("core2", "nocona").
target_weight("core2", 7).

target("nocona").
target_family("nocona", "x86_64").
target_parent("nocona", "x86_64").
target_weight("nocona", 8).

target("x86_64").
target_family("x86_64", "x86_64").
target_weight("x86_64", 9).


%----------------------------------------------------------------------------
% Virtual providers
%----------------------------------------------------------------------------
virtual("awk").
provides_virtual("gawk", "awk").
provides_virtual("mawk", "awk").
virtual("blas").
provides_virtual("atlas", "blas").
provides_virtual("blis", "blas").
provides_virtual("blis", "blas").
provides_virtual("cray-libsci", "blas").
provides_virtual("essl", "blas").
provides_virtual("intel-mkl", "blas").
provides_virtual("intel-parallel-studio", "blas").
provides_virtual("netlib-lapack", "blas").
provides_virtual("netlib-xblas", "blas").
provides_virtual("openblas", "blas").
provides_virtual("veclibfort", "blas").
virtual("gl").
provides_virtual("mesa", "gl").
provides_virtual("opengl", "gl").
provides_virtual("opengl", "gl").
provides_virtual("opengl", "gl").
provides_virtual("opengl", "gl").
provides_virtual("opengl", "gl").
provides_virtual("opengl", "gl").
provides_virtual("opengl", "gl").
virtual("java").
provides_virtual("ibm-java", "java").
provides_virtual("icedtea", "java").
provides_virtual("jdk", "java").
provides_virtual("jdk", "java").
provides_virtual("jdk", "java").
provides_virtual("jdk", "java").
provides_virtual("jdk", "java").
provides_virtual("jdk", "java").
provides_virtual("openjdk", "java").
provides_virtual("openjdk", "java").
virtual("jpeg").
provides_virtual("libjpeg", "jpeg").
provides_virtual("libjpeg-turbo", "jpeg").
virtual("lapack").
provides_virtual("atlas", "lapack").
provides_virtual("cray-libsci", "lapack").
provides_virtual("intel-mkl", "lapack").
provides_virtual("intel-parallel-studio", "lapack").
provides_virtual("libflame", "lapack").
provides_virtual("netlib-lapack", "lapack").
provides_virtual("openblas", "lapack").
provides_virtual("veclibfort", "lapack").
virtual("mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("charmpp", "mpi").
provides_virtual("fujitsu-mpi", "mpi").
provides_virtual("intel-mpi", "mpi").
provides_virtual("intel-parallel-studio", "mpi").
provides_virtual("mpich", "mpi").
provides_virtual("mpich", "mpi").
provides_virtual("mpich", "mpi").
provides_virtual("mpilander", "mpi").
provides_virtual("mpt", "mpi").
provides_virtual("mpt", "mpi").
provides_virtual("mpt", "mpi").
provides_virtual("mvapich2", "mpi").
provides_virtual("mvapich2", "mpi").
provides_virtual("mvapich2", "mpi").
provides_virtual("openmpi", "mpi").
provides_virtual("openmpi", "mpi").
provides_virtual("openmpi", "mpi").
provides_virtual("openmpi", "mpi").
provides_virtual("spectrum-mpi", "mpi").
virtual("pkgconfig").
provides_virtual("pkg-config", "pkgconfig").
provides_virtual("pkgconf", "pkgconfig").
virtual("szip").
provides_virtual("libaec", "szip").
provides_virtual("libszip", "szip").

%----------------------------------------------------------------------------
% Default virtual providers
%----------------------------------------------------------------------------
default_provider_preference("awk", "gawk", 0).
default_provider_preference("blas", "openblas", 0).
default_provider_preference("gl", "mesa+opengl", 0).
default_provider_preference("gl", "opengl", 1).
default_provider_preference("java", "openjdk", 0).
default_provider_preference("java", "jdk", 1).
default_provider_preference("java", "ibm-java", 2).
default_provider_preference("jpeg", "libjpeg-turbo", 0).
default_provider_preference("jpeg", "libjpeg", 1).
default_provider_preference("lapack", "openblas", 0).
default_provider_preference("mpi", "openmpi", 0).
default_provider_preference("mpi", "mpich", 1).
default_provider_preference("pkgconfig", "pkgconf", 0).
default_provider_preference("pkgconfig", "pkg-config", 1).
default_provider_preference("szip", "libszip", 0).
default_provider_preference("szip", "libaec", 1).

%----------------------------------------------------------------------------
% Compiler flag defaults
%----------------------------------------------------------------------------
flag_type("cflags").
flag_type("cxxflags").
flag_type("fflags").
flag_type("ldflags").
flag_type("ldlibs").
flag_type("cppflags").


%============================================================================
% Package Constraints
%============================================================================

%----------------------------------------------------------------------------
% Package: alsa-lib
%----------------------------------------------------------------------------
version_declared("alsa-lib", "1.1.4.1", 0).


%----------------------------------------------------------------------------
% Package: at-spi2-atk
%----------------------------------------------------------------------------
version_declared("at-spi2-atk", "2.26.2", 0).
version_declared("at-spi2-atk", "2.26.1", 1).

variant("at-spi2-atk", "buildtype").
variant_single_value("at-spi2-atk", "buildtype").
variant_default_value("at-spi2-atk", "buildtype", "release").
variant_possible_value("at-spi2-atk", "buildtype", "debug").
variant_possible_value("at-spi2-atk", "buildtype", "debugoptimized").
variant_possible_value("at-spi2-atk", "buildtype", "minsize").
variant_possible_value("at-spi2-atk", "buildtype", "plain").
variant_possible_value("at-spi2-atk", "buildtype", "release").

declared_dependency("at-spi2-atk", "at-spi2-core", "build").
declared_dependency("at-spi2-atk", "at-spi2-core", "link").
node("at-spi2-core") :- depends_on("at-spi2-atk", "at-spi2-core"), node("at-spi2-atk").

declared_dependency("at-spi2-atk", "atk", "build").
declared_dependency("at-spi2-atk", "atk", "link").
node("atk") :- depends_on("at-spi2-atk", "atk"), node("at-spi2-atk").
1 { version("atk", "2.28.1"); version("atk", "2.30.0") } 1 :- depends_on("at-spi2-atk", "atk"), node("at-spi2-atk").

declared_dependency("at-spi2-atk", "meson", "build").
node("meson") :- depends_on("at-spi2-atk", "meson"), node("at-spi2-atk").

declared_dependency("at-spi2-atk", "ninja", "build").
node("ninja") :- depends_on("at-spi2-atk", "ninja"), node("at-spi2-atk").

declared_dependency("at-spi2-atk", "pkgconfig", "build").
node("pkgconfig") :- depends_on("at-spi2-atk", "pkgconfig"), node("at-spi2-atk").


%----------------------------------------------------------------------------
% Package: at-spi2-core
%----------------------------------------------------------------------------
version_declared("at-spi2-core", "2.28.0", 0).

variant("at-spi2-core", "buildtype").
variant_single_value("at-spi2-core", "buildtype").
variant_default_value("at-spi2-core", "buildtype", "release").
variant_possible_value("at-spi2-core", "buildtype", "debug").
variant_possible_value("at-spi2-core", "buildtype", "debugoptimized").
variant_possible_value("at-spi2-core", "buildtype", "minsize").
variant_possible_value("at-spi2-core", "buildtype", "plain").
variant_possible_value("at-spi2-core", "buildtype", "release").

declared_dependency("at-spi2-core", "dbus", "build").
declared_dependency("at-spi2-core", "dbus", "link").
node("dbus") :- depends_on("at-spi2-core", "dbus"), node("at-spi2-core").
1 { version("dbus", "1.12.8") } 1 :- depends_on("at-spi2-core", "dbus"), node("at-spi2-core").

declared_dependency("at-spi2-core", "fixesproto", "build").
node("fixesproto") :- depends_on("at-spi2-core", "fixesproto"), node("at-spi2-core").

declared_dependency("at-spi2-core", "gettext", "build").
declared_dependency("at-spi2-core", "gettext", "link").
node("gettext") :- depends_on("at-spi2-core", "gettext"), node("at-spi2-core").

declared_dependency("at-spi2-core", "glib", "build").
declared_dependency("at-spi2-core", "glib", "link").
node("glib") :- depends_on("at-spi2-core", "glib"), node("at-spi2-core").
1 { version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1 :- depends_on("at-spi2-core", "glib"), node("at-spi2-core").

declared_dependency("at-spi2-core", "inputproto", "build").
node("inputproto") :- depends_on("at-spi2-core", "inputproto"), node("at-spi2-core").

declared_dependency("at-spi2-core", "libx11", "build").
declared_dependency("at-spi2-core", "libx11", "link").
node("libx11") :- depends_on("at-spi2-core", "libx11"), node("at-spi2-core").

declared_dependency("at-spi2-core", "libxi", "build").
declared_dependency("at-spi2-core", "libxi", "link").
node("libxi") :- depends_on("at-spi2-core", "libxi"), node("at-spi2-core").

declared_dependency("at-spi2-core", "libxtst", "build").
node("libxtst") :- depends_on("at-spi2-core", "libxtst"), node("at-spi2-core").

declared_dependency("at-spi2-core", "meson", "build").
node("meson") :- depends_on("at-spi2-core", "meson"), node("at-spi2-core").

declared_dependency("at-spi2-core", "ninja", "build").
node("ninja") :- depends_on("at-spi2-core", "ninja"), node("at-spi2-core").

declared_dependency("at-spi2-core", "pkgconfig", "build").
node("pkgconfig") :- depends_on("at-spi2-core", "pkgconfig"), node("at-spi2-core").

declared_dependency("at-spi2-core", "python", "build").
node("python") :- depends_on("at-spi2-core", "python"), node("at-spi2-core").

declared_dependency("at-spi2-core", "recordproto", "build").
node("recordproto") :- depends_on("at-spi2-core", "recordproto"), node("at-spi2-core").


%----------------------------------------------------------------------------
% Package: atk
%----------------------------------------------------------------------------
version_declared("atk", "2.30.0", 0).
version_declared("atk", "2.28.1", 1).
version_declared("atk", "2.20.0", 2).
version_declared("atk", "2.14.0", 3).

declared_dependency("atk", "gettext", "build").
declared_dependency("atk", "gettext", "link").
node("gettext") :- depends_on("atk", "gettext"), node("atk").

declared_dependency("atk", "glib", "build").
declared_dependency("atk", "glib", "link").
node("glib") :- depends_on("atk", "glib"), node("atk").

declared_dependency("atk", "gobject-introspection", "build").
declared_dependency("atk", "gobject-introspection", "link").
node("gobject-introspection") :- depends_on("atk", "gobject-introspection"), node("atk").

declared_dependency("atk", "libffi", "build").
declared_dependency("atk", "libffi", "link").
node("libffi") :- depends_on("atk", "libffi"), node("atk").

declared_dependency("atk", "meson", "build") :- node("atk"), 1 { version("atk", "2.28.1"); version("atk", "2.30.0") } 1.
node("meson") :- depends_on("atk", "meson"), node("atk"), 1 { version("atk", "2.28.1"); version("atk", "2.30.0") } 1.
declared_dependency("atk", "meson", "build") :- node("atk"), 1 { version("atk", "2.30.0") } 1.
node("meson") :- depends_on("atk", "meson"), node("atk"), 1 { version("atk", "2.30.0") } 1.
1 { version("meson", "0.49.0"); version("meson", "0.49.1") } 1 :- depends_on("atk", "meson"), node("atk"), 1 { version("atk", "2.30.0") } 1.

declared_dependency("atk", "pkgconfig", "build").
node("pkgconfig") :- depends_on("atk", "pkgconfig"), node("atk").


%----------------------------------------------------------------------------
% Package: atlas
%----------------------------------------------------------------------------
version_declared("atlas", "3.10.3", 0).
version_declared("atlas", "3.11.41", 1).
version_declared("atlas", "3.11.39", 2).
version_declared("atlas", "3.11.34", 3).
version_declared("atlas", "3.10.2", 4).

variant("atlas", "shared").
variant_single_value("atlas", "shared").
variant_default_value("atlas", "shared", "True").
variant_possible_value("atlas", "shared", "False").
variant_possible_value("atlas", "shared", "True").

variant("atlas", "threads").
variant_single_value("atlas", "threads").
variant_default_value("atlas", "threads", "none").
variant_possible_value("atlas", "threads", "none").
variant_possible_value("atlas", "threads", "pthreads").

variant("atlas", "tune_cpu").
variant_single_value("atlas", "tune_cpu").
variant_default_value("atlas", "tune_cpu", -1).
variant_possible_value("atlas", "tune_cpu", -1).


%----------------------------------------------------------------------------
% Package: autoconf
%----------------------------------------------------------------------------
version_declared("autoconf", "2.69", 0).
version_declared("autoconf", "2.62", 1).
version_declared("autoconf", "2.59", 2).
version_declared("autoconf", "2.13", 3).

declared_dependency("autoconf", "m4", "build").
declared_dependency("autoconf", "m4", "run").
node("m4") :- depends_on("autoconf", "m4"), node("autoconf").

declared_dependency("autoconf", "perl", "build").
declared_dependency("autoconf", "perl", "run").
node("perl") :- depends_on("autoconf", "perl"), node("autoconf").


%----------------------------------------------------------------------------
% Package: automake
%----------------------------------------------------------------------------
version_declared("automake", "1.16.1", 0).
version_declared("automake", "1.15.1", 1).
version_declared("automake", "1.15", 2).
version_declared("automake", "1.14.1", 3).
version_declared("automake", "1.13.4", 4).
version_declared("automake", "1.11.6", 5).

declared_dependency("automake", "autoconf", "build").
node("autoconf") :- depends_on("automake", "autoconf"), node("automake").

declared_dependency("automake", "perl", "build").
declared_dependency("automake", "perl", "run").
node("perl") :- depends_on("automake", "perl"), node("automake").


%----------------------------------------------------------------------------
% Package: bdftopcf
%----------------------------------------------------------------------------
version_declared("bdftopcf", "1.0.5", 0).

declared_dependency("bdftopcf", "fontsproto", "build").
node("fontsproto") :- depends_on("bdftopcf", "fontsproto"), node("bdftopcf").

declared_dependency("bdftopcf", "libxfont", "build").
declared_dependency("bdftopcf", "libxfont", "link").
node("libxfont") :- depends_on("bdftopcf", "libxfont"), node("bdftopcf").

declared_dependency("bdftopcf", "pkgconfig", "build").
node("pkgconfig") :- depends_on("bdftopcf", "pkgconfig"), node("bdftopcf").

declared_dependency("bdftopcf", "util-macros", "build").
node("util-macros") :- depends_on("bdftopcf", "util-macros"), node("bdftopcf").

declared_dependency("bdftopcf", "xproto", "build").
node("xproto") :- depends_on("bdftopcf", "xproto"), node("bdftopcf").


%----------------------------------------------------------------------------
% Package: bdw-gc
%----------------------------------------------------------------------------
version_declared("bdw-gc", "8.0.0", 0).
version_declared("bdw-gc", "7.6.0", 1).
version_declared("bdw-gc", "7.4.4", 2).

variant("bdw-gc", "libatomic-ops").
variant_single_value("bdw-gc", "libatomic-ops").
variant_default_value("bdw-gc", "libatomic-ops", "True").
variant_possible_value("bdw-gc", "libatomic-ops", "False").
variant_possible_value("bdw-gc", "libatomic-ops", "True").

variant("bdw-gc", "threads").
variant_single_value("bdw-gc", "threads").
variant_default_value("bdw-gc", "threads", "none").
variant_possible_value("bdw-gc", "threads", "dgux386").
variant_possible_value("bdw-gc", "threads", "none").
variant_possible_value("bdw-gc", "threads", "posix").

declared_dependency("bdw-gc", "libatomic-ops", "build") :- node("bdw-gc"), variant_value("bdw-gc", "libatomic-ops", "True").
declared_dependency("bdw-gc", "libatomic-ops", "link") :- node("bdw-gc"), variant_value("bdw-gc", "libatomic-ops", "True").
node("libatomic-ops") :- depends_on("bdw-gc", "libatomic-ops"), node("bdw-gc"), variant_value("bdw-gc", "libatomic-ops", "True").


%----------------------------------------------------------------------------
% Package: binutils
%----------------------------------------------------------------------------
version_declared("binutils", "2.33.1", 0).
version_declared("binutils", "2.32", 1).
version_declared("binutils", "2.31.1", 2).
version_declared("binutils", "2.29.1", 3).
version_declared("binutils", "2.28", 4).
version_declared("binutils", "2.27", 5).
version_declared("binutils", "2.26", 6).
version_declared("binutils", "2.25.1", 7).
version_declared("binutils", "2.25", 8).
version_declared("binutils", "2.24", 9).
version_declared("binutils", "2.23.2", 10).
version_declared("binutils", "2.20.1", 11).

variant("binutils", "gold").
variant_single_value("binutils", "gold").
variant_default_value("binutils", "gold", "True").
variant_possible_value("binutils", "gold", "False").
variant_possible_value("binutils", "gold", "True").

variant("binutils", "headers").
variant_single_value("binutils", "headers").
variant_default_value("binutils", "headers", "False").
variant_possible_value("binutils", "headers", "False").
variant_possible_value("binutils", "headers", "True").

variant("binutils", "libiberty").
variant_single_value("binutils", "libiberty").
variant_default_value("binutils", "libiberty", "False").
variant_possible_value("binutils", "libiberty", "False").
variant_possible_value("binutils", "libiberty", "True").

variant("binutils", "nls").
variant_single_value("binutils", "nls").
variant_default_value("binutils", "nls", "True").
variant_possible_value("binutils", "nls", "False").
variant_possible_value("binutils", "nls", "True").

variant("binutils", "plugins").
variant_single_value("binutils", "plugins").
variant_default_value("binutils", "plugins", "False").
variant_possible_value("binutils", "plugins", "False").
variant_possible_value("binutils", "plugins", "True").

declared_dependency("binutils", "bison", "build") :- node("binutils"), 1 { version("binutils", "2.20.1"); version("binutils", "2.23.2"); version("binutils", "2.24"); version("binutils", "2.25"); version("binutils", "2.25.1"); version("binutils", "2.26"); version("binutils", "2.27"); version("binutils", "2.28"); version("binutils", "2.29.1") } 1, variant_value("binutils", "gold", "True").
node("bison") :- depends_on("binutils", "bison"), node("binutils"), 1 { version("binutils", "2.20.1"); version("binutils", "2.23.2"); version("binutils", "2.24"); version("binutils", "2.25"); version("binutils", "2.25.1"); version("binutils", "2.26"); version("binutils", "2.27"); version("binutils", "2.28"); version("binutils", "2.29.1") } 1, variant_value("binutils", "gold", "True").

declared_dependency("binutils", "gettext", "build") :- node("binutils"), variant_value("binutils", "nls", "True").
declared_dependency("binutils", "gettext", "link") :- node("binutils"), variant_value("binutils", "nls", "True").
node("gettext") :- depends_on("binutils", "gettext"), node("binutils"), variant_value("binutils", "nls", "True").

declared_dependency("binutils", "m4", "build") :- node("binutils"), 1 { version("binutils", "2.20.1"); version("binutils", "2.23.2"); version("binutils", "2.24"); version("binutils", "2.25"); version("binutils", "2.25.1"); version("binutils", "2.26"); version("binutils", "2.27"); version("binutils", "2.28"); version("binutils", "2.29.1") } 1, variant_value("binutils", "gold", "True").
node("m4") :- depends_on("binutils", "m4"), node("binutils"), 1 { version("binutils", "2.20.1"); version("binutils", "2.23.2"); version("binutils", "2.24"); version("binutils", "2.25"); version("binutils", "2.25.1"); version("binutils", "2.26"); version("binutils", "2.27"); version("binutils", "2.28"); version("binutils", "2.29.1") } 1, variant_value("binutils", "gold", "True").

declared_dependency("binutils", "zlib", "build").
declared_dependency("binutils", "zlib", "link").
node("zlib") :- depends_on("binutils", "zlib"), node("binutils").


%----------------------------------------------------------------------------
% Package: bison
%----------------------------------------------------------------------------
version_declared("bison", "3.4.2", 0).
version_declared("bison", "3.0.5", 1).
version_declared("bison", "3.0.4", 2).
version_declared("bison", "2.7", 3).

declared_dependency("bison", "diffutils", "build").
node("diffutils") :- depends_on("bison", "diffutils"), node("bison").

declared_dependency("bison", "help2man", "build").
node("help2man") :- depends_on("bison", "help2man"), node("bison").

declared_dependency("bison", "m4", "build").
declared_dependency("bison", "m4", "run").
node("m4") :- depends_on("bison", "m4"), node("bison").

declared_dependency("bison", "perl", "build").
node("perl") :- depends_on("bison", "perl"), node("bison").


%----------------------------------------------------------------------------
% Package: blis
%----------------------------------------------------------------------------
version_declared("blis", "0.6.1", 0).
version_declared("blis", "0.6.0", 1).
version_declared("blis", "0.5.0", 2).
version_declared("blis", "0.4.0", 3).
version_declared("blis", "0.3.2", 4).
version_declared("blis", "0.3.1", 5).
version_declared("blis", "0.3.0", 6).
version_declared("blis", "0.2.2", 7).
version_declared("blis", "master", 8).

variant("blis", "blas").
variant_single_value("blis", "blas").
variant_default_value("blis", "blas", "True").
variant_possible_value("blis", "blas", "False").
variant_possible_value("blis", "blas", "True").

variant("blis", "cblas").
variant_single_value("blis", "cblas").
variant_default_value("blis", "cblas", "True").
variant_possible_value("blis", "cblas", "False").
variant_possible_value("blis", "cblas", "True").

variant("blis", "shared").
variant_single_value("blis", "shared").
variant_default_value("blis", "shared", "True").
variant_possible_value("blis", "shared", "False").
variant_possible_value("blis", "shared", "True").

variant("blis", "static").
variant_single_value("blis", "static").
variant_default_value("blis", "static", "True").
variant_possible_value("blis", "static", "False").
variant_possible_value("blis", "static", "True").

variant("blis", "threads").
variant_single_value("blis", "threads").
variant_default_value("blis", "threads", "none").
variant_possible_value("blis", "threads", "none").
variant_possible_value("blis", "threads", "openmp").
variant_possible_value("blis", "threads", "pthreads").

declared_dependency("blis", "python", "build").
declared_dependency("blis", "python", "run").
node("python") :- depends_on("blis", "python"), node("blis").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("blis", "python"), node("blis").


%----------------------------------------------------------------------------
% Package: boost
%----------------------------------------------------------------------------
version_declared("boost", "1.72.0", 0).
version_declared("boost", "1.71.0", 1).
version_declared("boost", "1.70.0", 2).
version_declared("boost", "1.69.0", 3).
version_declared("boost", "1.68.0", 4).
version_declared("boost", "1.67.0", 5).
version_declared("boost", "1.66.0", 6).
version_declared("boost", "1.65.1", 7).
version_declared("boost", "1.65.0", 8).
version_declared("boost", "1.64.0", 9).
version_declared("boost", "1.63.0", 10).
version_declared("boost", "1.62.0", 11).
version_declared("boost", "1.61.0", 12).
version_declared("boost", "1.60.0", 13).
version_declared("boost", "1.59.0", 14).
version_declared("boost", "1.58.0", 15).
version_declared("boost", "1.57.0", 16).
version_declared("boost", "1.56.0", 17).
version_declared("boost", "1.55.0", 18).
version_declared("boost", "1.54.0", 19).
version_declared("boost", "1.53.0", 20).
version_declared("boost", "1.52.0", 21).
version_declared("boost", "1.51.0", 22).
version_declared("boost", "1.50.0", 23).
version_declared("boost", "1.49.0", 24).
version_declared("boost", "1.48.0", 25).
version_declared("boost", "1.47.0", 26).
version_declared("boost", "1.46.1", 27).
version_declared("boost", "1.46.0", 28).
version_declared("boost", "1.45.0", 29).
version_declared("boost", "1.44.0", 30).
version_declared("boost", "1.43.0", 31).
version_declared("boost", "1.42.0", 32).
version_declared("boost", "1.41.0", 33).
version_declared("boost", "1.40.0", 34).
version_declared("boost", "1.39.0", 35).
version_declared("boost", "1.38.0", 36).
version_declared("boost", "1.37.0", 37).
version_declared("boost", "1.36.0", 38).
version_declared("boost", "1.35.0", 39).
version_declared("boost", "1.34.1", 40).
version_declared("boost", "1.34.0", 41).
version_declared("boost", "develop", 42).

variant("boost", "atomic").
variant_single_value("boost", "atomic").
variant_default_value("boost", "atomic", "True").
variant_possible_value("boost", "atomic", "False").
variant_possible_value("boost", "atomic", "True").

variant("boost", "chrono").
variant_single_value("boost", "chrono").
variant_default_value("boost", "chrono", "True").
variant_possible_value("boost", "chrono", "False").
variant_possible_value("boost", "chrono", "True").

variant("boost", "clanglibcpp").
variant_single_value("boost", "clanglibcpp").
variant_default_value("boost", "clanglibcpp", "False").
variant_possible_value("boost", "clanglibcpp", "False").
variant_possible_value("boost", "clanglibcpp", "True").

variant("boost", "context").
variant_single_value("boost", "context").
variant_default_value("boost", "context", "False").
variant_possible_value("boost", "context", "False").
variant_possible_value("boost", "context", "True").

variant("boost", "coroutine").
variant_single_value("boost", "coroutine").
variant_default_value("boost", "coroutine", "False").
variant_possible_value("boost", "coroutine", "False").
variant_possible_value("boost", "coroutine", "True").

variant("boost", "cxxstd").
variant_single_value("boost", "cxxstd").
variant_default_value("boost", "cxxstd", "98").
variant_possible_value("boost", "cxxstd", "11").
variant_possible_value("boost", "cxxstd", "14").
variant_possible_value("boost", "cxxstd", "17").
variant_possible_value("boost", "cxxstd", "98").

variant("boost", "date_time").
variant_single_value("boost", "date_time").
variant_default_value("boost", "date_time", "True").
variant_possible_value("boost", "date_time", "False").
variant_possible_value("boost", "date_time", "True").

variant("boost", "debug").
variant_single_value("boost", "debug").
variant_default_value("boost", "debug", "False").
variant_possible_value("boost", "debug", "False").
variant_possible_value("boost", "debug", "True").

variant("boost", "exception").
variant_single_value("boost", "exception").
variant_default_value("boost", "exception", "True").
variant_possible_value("boost", "exception", "False").
variant_possible_value("boost", "exception", "True").

variant("boost", "fiber").
variant_single_value("boost", "fiber").
variant_default_value("boost", "fiber", "False").
variant_possible_value("boost", "fiber", "False").
variant_possible_value("boost", "fiber", "True").

variant("boost", "filesystem").
variant_single_value("boost", "filesystem").
variant_default_value("boost", "filesystem", "True").
variant_possible_value("boost", "filesystem", "False").
variant_possible_value("boost", "filesystem", "True").

variant("boost", "graph").
variant_single_value("boost", "graph").
variant_default_value("boost", "graph", "True").
variant_possible_value("boost", "graph", "False").
variant_possible_value("boost", "graph", "True").

variant("boost", "icu").
variant_single_value("boost", "icu").
variant_default_value("boost", "icu", "False").
variant_possible_value("boost", "icu", "False").
variant_possible_value("boost", "icu", "True").

variant("boost", "iostreams").
variant_single_value("boost", "iostreams").
variant_default_value("boost", "iostreams", "True").
variant_possible_value("boost", "iostreams", "False").
variant_possible_value("boost", "iostreams", "True").

variant("boost", "locale").
variant_single_value("boost", "locale").
variant_default_value("boost", "locale", "True").
variant_possible_value("boost", "locale", "False").
variant_possible_value("boost", "locale", "True").

variant("boost", "log").
variant_single_value("boost", "log").
variant_default_value("boost", "log", "True").
variant_possible_value("boost", "log", "False").
variant_possible_value("boost", "log", "True").

variant("boost", "math").
variant_single_value("boost", "math").
variant_default_value("boost", "math", "True").
variant_possible_value("boost", "math", "False").
variant_possible_value("boost", "math", "True").

variant("boost", "mpi").
variant_single_value("boost", "mpi").
variant_default_value("boost", "mpi", "False").
variant_possible_value("boost", "mpi", "False").
variant_possible_value("boost", "mpi", "True").

variant("boost", "multithreaded").
variant_single_value("boost", "multithreaded").
variant_default_value("boost", "multithreaded", "True").
variant_possible_value("boost", "multithreaded", "False").
variant_possible_value("boost", "multithreaded", "True").

variant("boost", "numpy").
variant_single_value("boost", "numpy").
variant_default_value("boost", "numpy", "False").
variant_possible_value("boost", "numpy", "False").
variant_possible_value("boost", "numpy", "True").

variant("boost", "pic").
variant_single_value("boost", "pic").
variant_default_value("boost", "pic", "False").
variant_possible_value("boost", "pic", "False").
variant_possible_value("boost", "pic", "True").

variant("boost", "program_options").
variant_single_value("boost", "program_options").
variant_default_value("boost", "program_options", "True").
variant_possible_value("boost", "program_options", "False").
variant_possible_value("boost", "program_options", "True").

variant("boost", "python").
variant_single_value("boost", "python").
variant_default_value("boost", "python", "False").
variant_possible_value("boost", "python", "False").
variant_possible_value("boost", "python", "True").

variant("boost", "random").
variant_single_value("boost", "random").
variant_default_value("boost", "random", "True").
variant_possible_value("boost", "random", "False").
variant_possible_value("boost", "random", "True").

variant("boost", "regex").
variant_single_value("boost", "regex").
variant_default_value("boost", "regex", "True").
variant_possible_value("boost", "regex", "False").
variant_possible_value("boost", "regex", "True").

variant("boost", "serialization").
variant_single_value("boost", "serialization").
variant_default_value("boost", "serialization", "True").
variant_possible_value("boost", "serialization", "False").
variant_possible_value("boost", "serialization", "True").

variant("boost", "shared").
variant_single_value("boost", "shared").
variant_default_value("boost", "shared", "True").
variant_possible_value("boost", "shared", "False").
variant_possible_value("boost", "shared", "True").

variant("boost", "signals").
variant_single_value("boost", "signals").
variant_default_value("boost", "signals", "True").
variant_possible_value("boost", "signals", "False").
variant_possible_value("boost", "signals", "True").

variant("boost", "singlethreaded").
variant_single_value("boost", "singlethreaded").
variant_default_value("boost", "singlethreaded", "False").
variant_possible_value("boost", "singlethreaded", "False").
variant_possible_value("boost", "singlethreaded", "True").

variant("boost", "system").
variant_single_value("boost", "system").
variant_default_value("boost", "system", "True").
variant_possible_value("boost", "system", "False").
variant_possible_value("boost", "system", "True").

variant("boost", "taggedlayout").
variant_single_value("boost", "taggedlayout").
variant_default_value("boost", "taggedlayout", "False").
variant_possible_value("boost", "taggedlayout", "False").
variant_possible_value("boost", "taggedlayout", "True").

variant("boost", "test").
variant_single_value("boost", "test").
variant_default_value("boost", "test", "True").
variant_possible_value("boost", "test", "False").
variant_possible_value("boost", "test", "True").

variant("boost", "thread").
variant_single_value("boost", "thread").
variant_default_value("boost", "thread", "True").
variant_possible_value("boost", "thread", "False").
variant_possible_value("boost", "thread", "True").

variant("boost", "timer").
variant_single_value("boost", "timer").
variant_default_value("boost", "timer", "True").
variant_possible_value("boost", "timer", "False").
variant_possible_value("boost", "timer", "True").

variant("boost", "versionedlayout").
variant_single_value("boost", "versionedlayout").
variant_default_value("boost", "versionedlayout", "False").
variant_possible_value("boost", "versionedlayout", "False").
variant_possible_value("boost", "versionedlayout", "True").

variant("boost", "visibility").
variant_single_value("boost", "visibility").
variant_default_value("boost", "visibility", "hidden").
variant_possible_value("boost", "visibility", "global").
variant_possible_value("boost", "visibility", "hidden").
variant_possible_value("boost", "visibility", "protected").

variant("boost", "wave").
variant_single_value("boost", "wave").
variant_default_value("boost", "wave", "True").
variant_possible_value("boost", "wave", "False").
variant_possible_value("boost", "wave", "True").

declared_dependency("boost", "bzip2", "build") :- node("boost"), variant_value("boost", "iostreams", "True").
declared_dependency("boost", "bzip2", "link") :- node("boost"), variant_value("boost", "iostreams", "True").
node("bzip2") :- depends_on("boost", "bzip2"), node("boost"), variant_value("boost", "iostreams", "True").

declared_dependency("boost", "icu4c", "build") :- node("boost"), variant_value("boost", "icu", "True").
declared_dependency("boost", "icu4c", "link") :- node("boost"), variant_value("boost", "icu", "True").
node("icu4c") :- depends_on("boost", "icu4c"), node("boost"), variant_value("boost", "icu", "True").

declared_dependency("boost", "mpi", "build") :- node("boost"), variant_value("boost", "mpi", "True").
declared_dependency("boost", "mpi", "link") :- node("boost"), variant_value("boost", "mpi", "True").
node("mpi") :- depends_on("boost", "mpi"), node("boost"), variant_value("boost", "mpi", "True").

declared_dependency("boost", "py-numpy", "build") :- node("boost"), variant_value("boost", "numpy", "True").
declared_dependency("boost", "py-numpy", "run") :- node("boost"), variant_value("boost", "numpy", "True").
node("py-numpy") :- depends_on("boost", "py-numpy"), node("boost"), variant_value("boost", "numpy", "True").

declared_dependency("boost", "python", "build") :- node("boost"), variant_value("boost", "python", "True").
declared_dependency("boost", "python", "link") :- node("boost"), variant_value("boost", "python", "True").
node("python") :- depends_on("boost", "python"), node("boost"), variant_value("boost", "python", "True").

declared_dependency("boost", "zlib", "build") :- node("boost"), variant_value("boost", "iostreams", "True").
declared_dependency("boost", "zlib", "link") :- node("boost"), variant_value("boost", "iostreams", "True").
node("zlib") :- depends_on("boost", "zlib"), node("boost"), variant_value("boost", "iostreams", "True").


%----------------------------------------------------------------------------
% Package: bzip2
%----------------------------------------------------------------------------
version_declared("bzip2", "1.0.8", 0).
version_declared("bzip2", "1.0.7", 1).
version_declared("bzip2", "1.0.6", 2).

variant("bzip2", "shared").
variant_single_value("bzip2", "shared").
variant_default_value("bzip2", "shared", "True").
variant_possible_value("bzip2", "shared", "False").
variant_possible_value("bzip2", "shared", "True").

declared_dependency("bzip2", "diffutils", "build").
node("diffutils") :- depends_on("bzip2", "diffutils"), node("bzip2").


%----------------------------------------------------------------------------
% Package: cairo
%----------------------------------------------------------------------------
version_declared("cairo", "1.16.0", 0).
version_declared("cairo", "1.14.12", 1).
version_declared("cairo", "1.14.8", 2).
version_declared("cairo", "1.14.0", 3).

variant("cairo", "X").
variant_single_value("cairo", "X").
variant_default_value("cairo", "X", "False").
variant_possible_value("cairo", "X", "False").
variant_possible_value("cairo", "X", "True").

variant("cairo", "fc").
variant_single_value("cairo", "fc").
variant_default_value("cairo", "fc", "False").
variant_possible_value("cairo", "fc", "False").
variant_possible_value("cairo", "fc", "True").

variant("cairo", "ft").
variant_single_value("cairo", "ft").
variant_default_value("cairo", "ft", "False").
variant_possible_value("cairo", "ft", "False").
variant_possible_value("cairo", "ft", "True").

variant("cairo", "gobject").
variant_single_value("cairo", "gobject").
variant_default_value("cairo", "gobject", "False").
variant_possible_value("cairo", "gobject", "False").
variant_possible_value("cairo", "gobject", "True").

variant("cairo", "pdf").
variant_single_value("cairo", "pdf").
variant_default_value("cairo", "pdf", "False").
variant_possible_value("cairo", "pdf", "False").
variant_possible_value("cairo", "pdf", "True").

variant("cairo", "png").
variant_single_value("cairo", "png").
variant_default_value("cairo", "png", "False").
variant_possible_value("cairo", "png", "False").
variant_possible_value("cairo", "png", "True").

variant("cairo", "svg").
variant_single_value("cairo", "svg").
variant_default_value("cairo", "svg", "False").
variant_possible_value("cairo", "svg", "False").
variant_possible_value("cairo", "svg", "True").

declared_dependency("cairo", "autoconf", "build").
node("autoconf") :- depends_on("cairo", "autoconf"), node("cairo").

declared_dependency("cairo", "automake", "build").
node("automake") :- depends_on("cairo", "automake"), node("cairo").

declared_dependency("cairo", "fontconfig", "build") :- node("cairo"), variant_value("cairo", "fc", "True").
declared_dependency("cairo", "fontconfig", "link") :- node("cairo"), variant_value("cairo", "fc", "True").
node("fontconfig") :- depends_on("cairo", "fontconfig"), node("cairo"), variant_value("cairo", "fc", "True").

declared_dependency("cairo", "freetype", "build") :- node("cairo"), variant_value("cairo", "ft", "True").
declared_dependency("cairo", "freetype", "link") :- node("cairo"), variant_value("cairo", "ft", "True").
node("freetype") :- depends_on("cairo", "freetype"), node("cairo"), variant_value("cairo", "ft", "True").

declared_dependency("cairo", "glib", "build").
declared_dependency("cairo", "glib", "link").
node("glib") :- depends_on("cairo", "glib"), node("cairo").

declared_dependency("cairo", "libpng", "build") :- node("cairo"), variant_value("cairo", "png", "True").
declared_dependency("cairo", "libpng", "link") :- node("cairo"), variant_value("cairo", "png", "True").
node("libpng") :- depends_on("cairo", "libpng"), node("cairo"), variant_value("cairo", "png", "True").

declared_dependency("cairo", "librsvg", "build") :- node("cairo"), variant_value("cairo", "svg", "True").
declared_dependency("cairo", "librsvg", "link") :- node("cairo"), variant_value("cairo", "svg", "True").
node("librsvg") :- depends_on("cairo", "librsvg"), node("cairo"), variant_value("cairo", "svg", "True").

declared_dependency("cairo", "libtool", "build").
node("libtool") :- depends_on("cairo", "libtool"), node("cairo").

declared_dependency("cairo", "libx11", "build") :- node("cairo"), variant_value("cairo", "X", "True").
declared_dependency("cairo", "libx11", "link") :- node("cairo"), variant_value("cairo", "X", "True").
node("libx11") :- depends_on("cairo", "libx11"), node("cairo"), variant_value("cairo", "X", "True").

declared_dependency("cairo", "libxcb", "build") :- node("cairo"), variant_value("cairo", "X", "True").
declared_dependency("cairo", "libxcb", "link") :- node("cairo"), variant_value("cairo", "X", "True").
node("libxcb") :- depends_on("cairo", "libxcb"), node("cairo"), variant_value("cairo", "X", "True").

declared_dependency("cairo", "libxext", "build") :- node("cairo"), variant_value("cairo", "X", "True").
declared_dependency("cairo", "libxext", "link") :- node("cairo"), variant_value("cairo", "X", "True").
node("libxext") :- depends_on("cairo", "libxext"), node("cairo"), variant_value("cairo", "X", "True").

declared_dependency("cairo", "libxrender", "build") :- node("cairo"), variant_value("cairo", "X", "True").
declared_dependency("cairo", "libxrender", "link") :- node("cairo"), variant_value("cairo", "X", "True").
node("libxrender") :- depends_on("cairo", "libxrender"), node("cairo"), variant_value("cairo", "X", "True").

declared_dependency("cairo", "m4", "build").
node("m4") :- depends_on("cairo", "m4"), node("cairo").

declared_dependency("cairo", "pixman", "build").
declared_dependency("cairo", "pixman", "link").
node("pixman") :- depends_on("cairo", "pixman"), node("cairo").

declared_dependency("cairo", "pkgconfig", "build").
node("pkgconfig") :- depends_on("cairo", "pkgconfig"), node("cairo").

declared_dependency("cairo", "python", "build") :- node("cairo"), variant_value("cairo", "X", "True").
node("python") :- depends_on("cairo", "python"), node("cairo"), variant_value("cairo", "X", "True").


%----------------------------------------------------------------------------
% Package: charmpp
%----------------------------------------------------------------------------
version_declared("charmpp", "6.9.0", 0).
version_declared("charmpp", "6.8.2", 1).
version_declared("charmpp", "6.8.1", 2).
version_declared("charmpp", "6.8.0", 3).
version_declared("charmpp", "6.7.1", 4).
version_declared("charmpp", "6.7.0", 5).
version_declared("charmpp", "6.6.1", 6).
version_declared("charmpp", "6.6.0", 7).
version_declared("charmpp", "6.5.1", 8).
version_declared("charmpp", "develop", 9).

variant("charmpp", "backend").
variant_single_value("charmpp", "backend").
variant_default_value("charmpp", "backend", "netlrts").
variant_possible_value("charmpp", "backend", "gni").
variant_possible_value("charmpp", "backend", "mpi").
variant_possible_value("charmpp", "backend", "multicore").
variant_possible_value("charmpp", "backend", "netlrts").
variant_possible_value("charmpp", "backend", "ofi").
variant_possible_value("charmpp", "backend", "pami").
variant_possible_value("charmpp", "backend", "pamilrts").
variant_possible_value("charmpp", "backend", "verbs").

variant("charmpp", "build-target").
variant_single_value("charmpp", "build-target").
variant_default_value("charmpp", "build-target", "LIBS").
variant_possible_value("charmpp", "build-target", "AMPI").
variant_possible_value("charmpp", "build-target", "LIBS").
variant_possible_value("charmpp", "build-target", "charm++").

variant("charmpp", "cuda").
variant_single_value("charmpp", "cuda").
variant_default_value("charmpp", "cuda", "False").
variant_possible_value("charmpp", "cuda", "False").
variant_possible_value("charmpp", "cuda", "True").

variant("charmpp", "omp").
variant_single_value("charmpp", "omp").
variant_default_value("charmpp", "omp", "False").
variant_possible_value("charmpp", "omp", "False").
variant_possible_value("charmpp", "omp", "True").

variant("charmpp", "papi").
variant_single_value("charmpp", "papi").
variant_default_value("charmpp", "papi", "False").
variant_possible_value("charmpp", "papi", "False").
variant_possible_value("charmpp", "papi", "True").

variant("charmpp", "production").
variant_single_value("charmpp", "production").
variant_default_value("charmpp", "production", "True").
variant_possible_value("charmpp", "production", "False").
variant_possible_value("charmpp", "production", "True").

variant("charmpp", "pthreads").
variant_single_value("charmpp", "pthreads").
variant_default_value("charmpp", "pthreads", "False").
variant_possible_value("charmpp", "pthreads", "False").
variant_possible_value("charmpp", "pthreads", "True").

variant("charmpp", "shared").
variant_single_value("charmpp", "shared").
variant_default_value("charmpp", "shared", "True").
variant_possible_value("charmpp", "shared", "False").
variant_possible_value("charmpp", "shared", "True").

variant("charmpp", "smp").
variant_single_value("charmpp", "smp").
variant_default_value("charmpp", "smp", "True").
variant_possible_value("charmpp", "smp", "False").
variant_possible_value("charmpp", "smp", "True").

variant("charmpp", "syncft").
variant_single_value("charmpp", "syncft").
variant_default_value("charmpp", "syncft", "False").
variant_possible_value("charmpp", "syncft", "False").
variant_possible_value("charmpp", "syncft", "True").

variant("charmpp", "tcp").
variant_single_value("charmpp", "tcp").
variant_default_value("charmpp", "tcp", "False").
variant_possible_value("charmpp", "tcp", "False").
variant_possible_value("charmpp", "tcp", "True").

variant("charmpp", "tracing").
variant_single_value("charmpp", "tracing").
variant_default_value("charmpp", "tracing", "False").
variant_possible_value("charmpp", "tracing", "False").
variant_possible_value("charmpp", "tracing", "True").

declared_dependency("charmpp", "autoconf", "build") :- node("charmpp"), 1 { version("charmpp", "develop") } 1.
declared_dependency("charmpp", "autoconf", "link") :- node("charmpp"), 1 { version("charmpp", "develop") } 1.
node("autoconf") :- depends_on("charmpp", "autoconf"), node("charmpp"), 1 { version("charmpp", "develop") } 1.

declared_dependency("charmpp", "automake", "build") :- node("charmpp"), 1 { version("charmpp", "develop") } 1.
declared_dependency("charmpp", "automake", "link") :- node("charmpp"), 1 { version("charmpp", "develop") } 1.
node("automake") :- depends_on("charmpp", "automake"), node("charmpp"), 1 { version("charmpp", "develop") } 1.

declared_dependency("charmpp", "cuda", "build") :- node("charmpp"), variant_value("charmpp", "cuda", "True").
declared_dependency("charmpp", "cuda", "link") :- node("charmpp"), variant_value("charmpp", "cuda", "True").
node("cuda") :- depends_on("charmpp", "cuda"), node("charmpp"), variant_value("charmpp", "cuda", "True").

declared_dependency("charmpp", "mpi", "build") :- node("charmpp"), variant_value("charmpp", "backend", "mpi").
declared_dependency("charmpp", "mpi", "link") :- node("charmpp"), variant_value("charmpp", "backend", "mpi").
node("mpi") :- depends_on("charmpp", "mpi"), node("charmpp"), variant_value("charmpp", "backend", "mpi").

declared_dependency("charmpp", "papi", "build") :- node("charmpp"), variant_value("charmpp", "papi", "True").
declared_dependency("charmpp", "papi", "link") :- node("charmpp"), variant_value("charmpp", "papi", "True").
node("papi") :- depends_on("charmpp", "papi"), node("charmpp"), variant_value("charmpp", "papi", "True").


%----------------------------------------------------------------------------
% Package: cmake
%----------------------------------------------------------------------------
version_declared("cmake", "3.16.2", 0).
version_declared("cmake", "3.16.1", 1).
version_declared("cmake", "3.16.0", 2).
version_declared("cmake", "3.15.5", 3).
version_declared("cmake", "3.15.4", 4).
version_declared("cmake", "3.15.3", 5).
version_declared("cmake", "3.15.2", 6).
version_declared("cmake", "3.15.1", 7).
version_declared("cmake", "3.15.0", 8).
version_declared("cmake", "3.14.5", 9).
version_declared("cmake", "3.14.4", 10).
version_declared("cmake", "3.14.3", 11).
version_declared("cmake", "3.14.2", 12).
version_declared("cmake", "3.14.1", 13).
version_declared("cmake", "3.14.0", 14).
version_declared("cmake", "3.13.4", 15).
version_declared("cmake", "3.13.3", 16).
version_declared("cmake", "3.13.2", 17).
version_declared("cmake", "3.13.1", 18).
version_declared("cmake", "3.13.0", 19).
version_declared("cmake", "3.12.4", 20).
version_declared("cmake", "3.12.3", 21).
version_declared("cmake", "3.12.2", 22).
version_declared("cmake", "3.12.1", 23).
version_declared("cmake", "3.12.0", 24).
version_declared("cmake", "3.11.4", 25).
version_declared("cmake", "3.11.3", 26).
version_declared("cmake", "3.11.2", 27).
version_declared("cmake", "3.11.1", 28).
version_declared("cmake", "3.11.0", 29).
version_declared("cmake", "3.10.3", 30).
version_declared("cmake", "3.10.2", 31).
version_declared("cmake", "3.10.1", 32).
version_declared("cmake", "3.10.0", 33).
version_declared("cmake", "3.9.6", 34).
version_declared("cmake", "3.9.4", 35).
version_declared("cmake", "3.9.0", 36).
version_declared("cmake", "3.8.2", 37).
version_declared("cmake", "3.8.1", 38).
version_declared("cmake", "3.8.0", 39).
version_declared("cmake", "3.7.2", 40).
version_declared("cmake", "3.7.1", 41).
version_declared("cmake", "3.6.1", 42).
version_declared("cmake", "3.6.0", 43).
version_declared("cmake", "3.5.2", 44).
version_declared("cmake", "3.5.1", 45).
version_declared("cmake", "3.5.0", 46).
version_declared("cmake", "3.4.3", 47).
version_declared("cmake", "3.4.0", 48).
version_declared("cmake", "3.3.1", 49).
version_declared("cmake", "3.1.0", 50).
version_declared("cmake", "3.0.2", 51).
version_declared("cmake", "2.8.10.2", 52).

variant("cmake", "doc").
variant_single_value("cmake", "doc").
variant_default_value("cmake", "doc", "False").
variant_possible_value("cmake", "doc", "False").
variant_possible_value("cmake", "doc", "True").

variant("cmake", "ncurses").
variant_single_value("cmake", "ncurses").
variant_default_value("cmake", "ncurses", "True").
variant_possible_value("cmake", "ncurses", "False").
variant_possible_value("cmake", "ncurses", "True").

variant("cmake", "openssl").
variant_single_value("cmake", "openssl").
variant_default_value("cmake", "openssl", "True").
variant_possible_value("cmake", "openssl", "False").
variant_possible_value("cmake", "openssl", "True").

variant("cmake", "ownlibs").
variant_single_value("cmake", "ownlibs").
variant_default_value("cmake", "ownlibs", "True").
variant_possible_value("cmake", "ownlibs", "False").
variant_possible_value("cmake", "ownlibs", "True").

variant("cmake", "qt").
variant_single_value("cmake", "qt").
variant_default_value("cmake", "qt", "False").
variant_possible_value("cmake", "qt", "False").
variant_possible_value("cmake", "qt", "True").

declared_dependency("cmake", "bzip2", "build") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "bzip2", "link") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
node("bzip2") :- depends_on("cmake", "bzip2"), node("cmake"), variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "curl", "build") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "curl", "link") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
node("curl") :- depends_on("cmake", "curl"), node("cmake"), variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "expat", "build") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "expat", "link") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
node("expat") :- depends_on("cmake", "expat"), node("cmake"), variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "libarchive", "build") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libarchive", "link") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
node("libarchive") :- depends_on("cmake", "libarchive"), node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libarchive", "build") :- node("cmake"), 1 { version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libarchive", "link") :- node("cmake"), 1 { version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
node("libarchive") :- depends_on("cmake", "libarchive"), node("cmake"), 1 { version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
1 { version("libarchive", "3.4.1") } 1 :- depends_on("cmake", "libarchive"), node("cmake"), 1 { version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "libuv", "build") :- node("cmake"), 1 { version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libuv", "link") :- node("cmake"), 1 { version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3") } 1, variant_value("cmake", "ownlibs", "False").
node("libuv") :- depends_on("cmake", "libuv"), node("cmake"), 1 { version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3") } 1, variant_value("cmake", "ownlibs", "False").
1 { version("libuv", "1.9.0"); version("libuv", "1.10.0") } 1 :- depends_on("cmake", "libuv"), node("cmake"), 1 { version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libuv", "build") :- node("cmake"), 1 { version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libuv", "link") :- node("cmake"), 1 { version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4") } 1, variant_value("cmake", "ownlibs", "False").
node("libuv") :- depends_on("cmake", "libuv"), node("cmake"), 1 { version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4") } 1, variant_value("cmake", "ownlibs", "False").
1 { version("libuv", "1.10.0") } 1 :- depends_on("cmake", "libuv"), node("cmake"), 1 { version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libuv", "build") :- node("cmake"), 1 { version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "libuv", "link") :- node("cmake"), 1 { version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
node("libuv") :- depends_on("cmake", "libuv"), node("cmake"), 1 { version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
1 { version("libuv", "1.10.0"); version("libuv", "1.25.0") } 1 :- depends_on("cmake", "libuv"), node("cmake"), 1 { version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "ncurses", "build") :- node("cmake"), variant_value("cmake", "ncurses", "True").
declared_dependency("cmake", "ncurses", "link") :- node("cmake"), variant_value("cmake", "ncurses", "True").
node("ncurses") :- depends_on("cmake", "ncurses"), node("cmake"), variant_value("cmake", "ncurses", "True").

declared_dependency("cmake", "openssl", "build") :- node("cmake"), 1 { version("cmake", "2.8.10.2"); version("cmake", "3.0.2"); version("cmake", "3.1.0"); version("cmake", "3.3.1"); version("cmake", "3.4.0"); version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1") } 1, variant_value("cmake", "openssl", "True").
declared_dependency("cmake", "openssl", "link") :- node("cmake"), 1 { version("cmake", "2.8.10.2"); version("cmake", "3.0.2"); version("cmake", "3.1.0"); version("cmake", "3.3.1"); version("cmake", "3.4.0"); version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1") } 1, variant_value("cmake", "openssl", "True").
node("openssl") :- depends_on("cmake", "openssl"), node("cmake"), 1 { version("cmake", "2.8.10.2"); version("cmake", "3.0.2"); version("cmake", "3.1.0"); version("cmake", "3.3.1"); version("cmake", "3.4.0"); version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1") } 1, variant_value("cmake", "openssl", "True").
1 { version("openssl", "1.0.1e"); version("openssl", "1.0.1h"); version("openssl", "1.0.1r"); version("openssl", "1.0.1t"); version("openssl", "1.0.1u"); version("openssl", "1.0.2d"); version("openssl", "1.0.2e"); version("openssl", "1.0.2f"); version("openssl", "1.0.2g"); version("openssl", "1.0.2h"); version("openssl", "1.0.2i"); version("openssl", "1.0.2j"); version("openssl", "1.0.2k"); version("openssl", "1.0.2m"); version("openssl", "1.0.2n"); version("openssl", "1.0.2o"); version("openssl", "1.0.2p"); version("openssl", "1.0.2r"); version("openssl", "1.0.2s"); version("openssl", "1.0.2t") } 1 :- depends_on("cmake", "openssl"), node("cmake"), 1 { version("cmake", "2.8.10.2"); version("cmake", "3.0.2"); version("cmake", "3.1.0"); version("cmake", "3.3.1"); version("cmake", "3.4.0"); version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1") } 1, variant_value("cmake", "openssl", "True").
declared_dependency("cmake", "openssl", "build") :- node("cmake"), variant_value("cmake", "openssl", "True").
declared_dependency("cmake", "openssl", "link") :- node("cmake"), variant_value("cmake", "openssl", "True").
node("openssl") :- depends_on("cmake", "openssl"), node("cmake"), variant_value("cmake", "openssl", "True").

declared_dependency("cmake", "py-sphinx", "build") :- node("cmake"), variant_value("cmake", "doc", "True").
node("py-sphinx") :- depends_on("cmake", "py-sphinx"), node("cmake"), variant_value("cmake", "doc", "True").

declared_dependency("cmake", "python", "build") :- node("cmake"), variant_value("cmake", "doc", "True").
node("python") :- depends_on("cmake", "python"), node("cmake"), variant_value("cmake", "doc", "True").
1 { version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.1.5"); version("python", "3.2.6"); version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("cmake", "python"), node("cmake"), variant_value("cmake", "doc", "True").

declared_dependency("cmake", "qt", "build") :- node("cmake"), variant_value("cmake", "qt", "True").
declared_dependency("cmake", "qt", "link") :- node("cmake"), variant_value("cmake", "qt", "True").
node("qt") :- depends_on("cmake", "qt"), node("cmake"), variant_value("cmake", "qt", "True").

declared_dependency("cmake", "rhash", "build") :- node("cmake"), 1 { version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "rhash", "link") :- node("cmake"), 1 { version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").
node("rhash") :- depends_on("cmake", "rhash"), node("cmake"), 1 { version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1, variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "xz", "build") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "xz", "link") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
node("xz") :- depends_on("cmake", "xz"), node("cmake"), variant_value("cmake", "ownlibs", "False").

declared_dependency("cmake", "zlib", "build") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
declared_dependency("cmake", "zlib", "link") :- node("cmake"), variant_value("cmake", "ownlibs", "False").
node("zlib") :- depends_on("cmake", "zlib"), node("cmake"), variant_value("cmake", "ownlibs", "False").


%----------------------------------------------------------------------------
% Package: compositeproto
%----------------------------------------------------------------------------
version_declared("compositeproto", "0.4.2", 0).

declared_dependency("compositeproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("compositeproto", "pkgconfig"), node("compositeproto").

declared_dependency("compositeproto", "util-macros", "build").
node("util-macros") :- depends_on("compositeproto", "util-macros"), node("compositeproto").


%----------------------------------------------------------------------------
% Package: cpio
%----------------------------------------------------------------------------
version_declared("cpio", "2.13", 0).


%----------------------------------------------------------------------------
% Package: cray-libsci
%----------------------------------------------------------------------------
version_declared("cray-libsci", "18.11.1.2", 0).
version_declared("cray-libsci", "16.11.1", 1).
version_declared("cray-libsci", "16.09.1", 2).
version_declared("cray-libsci", "16.07.1", 3).
version_declared("cray-libsci", "16.06.1", 4).
version_declared("cray-libsci", "16.03.1", 5).


%----------------------------------------------------------------------------
% Package: cuda
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: cups
%----------------------------------------------------------------------------
version_declared("cups", "2.2.3", 0).

declared_dependency("cups", "gnutls", "build").
declared_dependency("cups", "gnutls", "link").
node("gnutls") :- depends_on("cups", "gnutls"), node("cups").


%----------------------------------------------------------------------------
% Package: curl
%----------------------------------------------------------------------------
version_declared("curl", "7.68.0", 0).
version_declared("curl", "7.63.0", 1).
version_declared("curl", "7.60.0", 2).
version_declared("curl", "7.59.0", 3).
version_declared("curl", "7.56.0", 4).
version_declared("curl", "7.54.0", 5).
version_declared("curl", "7.53.1", 6).
version_declared("curl", "7.52.1", 7).
version_declared("curl", "7.50.3", 8).
version_declared("curl", "7.50.2", 9).
version_declared("curl", "7.50.1", 10).
version_declared("curl", "7.49.1", 11).
version_declared("curl", "7.47.1", 12).
version_declared("curl", "7.46.0", 13).
version_declared("curl", "7.45.0", 14).
version_declared("curl", "7.44.0", 15).
version_declared("curl", "7.43.0", 16).
version_declared("curl", "7.42.1", 17).

variant("curl", "darwinssl").
variant_single_value("curl", "darwinssl").
variant_default_value("curl", "darwinssl", "True").
variant_possible_value("curl", "darwinssl", "False").
variant_possible_value("curl", "darwinssl", "True").

variant("curl", "gssapi").
variant_single_value("curl", "gssapi").
variant_default_value("curl", "gssapi", "False").
variant_possible_value("curl", "gssapi", "False").
variant_possible_value("curl", "gssapi", "True").

variant("curl", "libssh").
variant_single_value("curl", "libssh").
variant_default_value("curl", "libssh", "False").
variant_possible_value("curl", "libssh", "False").
variant_possible_value("curl", "libssh", "True").

variant("curl", "libssh2").
variant_single_value("curl", "libssh2").
variant_default_value("curl", "libssh2", "False").
variant_possible_value("curl", "libssh2", "False").
variant_possible_value("curl", "libssh2", "True").

variant("curl", "nghttp2").
variant_single_value("curl", "nghttp2").
variant_default_value("curl", "nghttp2", "False").
variant_possible_value("curl", "nghttp2", "False").
variant_possible_value("curl", "nghttp2", "True").

declared_dependency("curl", "krb5", "build") :- node("curl"), variant_value("curl", "gssapi", "True").
declared_dependency("curl", "krb5", "link") :- node("curl"), variant_value("curl", "gssapi", "True").
node("krb5") :- depends_on("curl", "krb5"), node("curl"), variant_value("curl", "gssapi", "True").

declared_dependency("curl", "libssh", "build") :- node("curl"), variant_value("curl", "libssh", "True").
declared_dependency("curl", "libssh", "link") :- node("curl"), variant_value("curl", "libssh", "True").
node("libssh") :- depends_on("curl", "libssh"), node("curl"), variant_value("curl", "libssh", "True").

declared_dependency("curl", "libssh2", "build") :- node("curl"), variant_value("curl", "libssh2", "True").
declared_dependency("curl", "libssh2", "link") :- node("curl"), variant_value("curl", "libssh2", "True").
node("libssh2") :- depends_on("curl", "libssh2"), node("curl"), variant_value("curl", "libssh2", "True").

declared_dependency("curl", "nghttp2", "build") :- node("curl"), variant_value("curl", "nghttp2", "True").
declared_dependency("curl", "nghttp2", "link") :- node("curl"), variant_value("curl", "nghttp2", "True").
node("nghttp2") :- depends_on("curl", "nghttp2"), node("curl"), variant_value("curl", "nghttp2", "True").

declared_dependency("curl", "openssl", "build") :- node("curl"), variant_value("curl", "darwinssl", "False").
declared_dependency("curl", "openssl", "link") :- node("curl"), variant_value("curl", "darwinssl", "False").
node("openssl") :- depends_on("curl", "openssl"), node("curl"), variant_value("curl", "darwinssl", "False").

declared_dependency("curl", "zlib", "build").
declared_dependency("curl", "zlib", "link").
node("zlib") :- depends_on("curl", "zlib"), node("curl").


%----------------------------------------------------------------------------
% Package: dbus
%----------------------------------------------------------------------------
version_declared("dbus", "1.12.8", 0).
version_declared("dbus", "1.11.2", 1).
version_declared("dbus", "1.9.0", 2).
version_declared("dbus", "1.8.8", 3).
version_declared("dbus", "1.8.6", 4).
version_declared("dbus", "1.8.4", 5).
version_declared("dbus", "1.8.2", 6).

declared_dependency("dbus", "expat", "build").
declared_dependency("dbus", "expat", "link").
node("expat") :- depends_on("dbus", "expat"), node("dbus").

declared_dependency("dbus", "glib", "build").
declared_dependency("dbus", "glib", "link").
node("glib") :- depends_on("dbus", "glib"), node("dbus").

declared_dependency("dbus", "pkgconfig", "build").
node("pkgconfig") :- depends_on("dbus", "pkgconfig"), node("dbus").


%----------------------------------------------------------------------------
% Package: diffutils
%----------------------------------------------------------------------------
version_declared("diffutils", "3.7", 0).
version_declared("diffutils", "3.6", 1).

declared_dependency("diffutils", "libiconv", "build").
declared_dependency("diffutils", "libiconv", "link").
node("libiconv") :- depends_on("diffutils", "libiconv"), node("diffutils").


%----------------------------------------------------------------------------
% Package: docbook-xml
%----------------------------------------------------------------------------
version_declared("docbook-xml", "4.5", 0).


%----------------------------------------------------------------------------
% Package: docbook-xsl
%----------------------------------------------------------------------------
version_declared("docbook-xsl", "1.79.2", 0).

declared_dependency("docbook-xsl", "docbook-xml", "build").
declared_dependency("docbook-xsl", "docbook-xml", "link").
node("docbook-xml") :- depends_on("docbook-xsl", "docbook-xml"), node("docbook-xsl").


%----------------------------------------------------------------------------
% Package: double-conversion
%----------------------------------------------------------------------------
version_declared("double-conversion", "2.0.1", 0).
version_declared("double-conversion", "2.0.0", 1).
version_declared("double-conversion", "1.1.5", 2).
version_declared("double-conversion", "1.1.4", 3).
version_declared("double-conversion", "1.1.3", 4).

variant("double-conversion", "build_type").
variant_single_value("double-conversion", "build_type").
variant_default_value("double-conversion", "build_type", "RelWithDebInfo").
variant_possible_value("double-conversion", "build_type", "Debug").
variant_possible_value("double-conversion", "build_type", "MinSizeRel").
variant_possible_value("double-conversion", "build_type", "RelWithDebInfo").
variant_possible_value("double-conversion", "build_type", "Release").

declared_dependency("double-conversion", "cmake", "build").
node("cmake") :- depends_on("double-conversion", "cmake"), node("double-conversion").


%----------------------------------------------------------------------------
% Package: essl
%----------------------------------------------------------------------------

variant("essl", "cuda").
variant_single_value("essl", "cuda").
variant_default_value("essl", "cuda", "False").
variant_possible_value("essl", "cuda", "False").
variant_possible_value("essl", "cuda", "True").

variant("essl", "ilp64").
variant_single_value("essl", "ilp64").
variant_default_value("essl", "ilp64", "False").
variant_possible_value("essl", "ilp64", "False").
variant_possible_value("essl", "ilp64", "True").

variant("essl", "threads").
variant_single_value("essl", "threads").
variant_default_value("essl", "threads", "openmp").
variant_possible_value("essl", "threads", "none").
variant_possible_value("essl", "threads", "openmp").


%----------------------------------------------------------------------------
% Package: expat
%----------------------------------------------------------------------------
version_declared("expat", "2.2.9", 0).
version_declared("expat", "2.2.5", 1).
version_declared("expat", "2.2.2", 2).
version_declared("expat", "2.2.0", 3).

variant("expat", "libbsd").
variant_single_value("expat", "libbsd").
variant_default_value("expat", "libbsd", "False").
variant_possible_value("expat", "libbsd", "False").
variant_possible_value("expat", "libbsd", "True").

declared_dependency("expat", "libbsd", "build") :- node("expat"), 1 { version("expat", "2.2.2"); version("expat", "2.2.5"); version("expat", "2.2.9") } 1, variant_value("expat", "libbsd", "True").
declared_dependency("expat", "libbsd", "link") :- node("expat"), 1 { version("expat", "2.2.2"); version("expat", "2.2.5"); version("expat", "2.2.9") } 1, variant_value("expat", "libbsd", "True").
node("libbsd") :- depends_on("expat", "libbsd"), node("expat"), 1 { version("expat", "2.2.2"); version("expat", "2.2.5"); version("expat", "2.2.9") } 1, variant_value("expat", "libbsd", "True").


%----------------------------------------------------------------------------
% Package: findutils
%----------------------------------------------------------------------------
version_declared("findutils", "4.6.0", 0).
version_declared("findutils", "4.4.2", 1).
version_declared("findutils", "4.4.1", 2).
version_declared("findutils", "4.4.0", 3).
version_declared("findutils", "4.2.33", 4).
version_declared("findutils", "4.2.32", 5).
version_declared("findutils", "4.2.31", 6).
version_declared("findutils", "4.2.30", 7).
version_declared("findutils", "4.2.29", 8).
version_declared("findutils", "4.2.28", 9).
version_declared("findutils", "4.2.27", 10).
version_declared("findutils", "4.2.26", 11).
version_declared("findutils", "4.2.25", 12).
version_declared("findutils", "4.2.23", 13).
version_declared("findutils", "4.2.20", 14).
version_declared("findutils", "4.2.18", 15).
version_declared("findutils", "4.2.15", 16).
version_declared("findutils", "4.1.20", 17).
version_declared("findutils", "4.1", 18).

declared_dependency("findutils", "autoconf", "build") :- node("findutils"), 1 { version("findutils", "4.6.0") } 1.
node("autoconf") :- depends_on("findutils", "autoconf"), node("findutils"), 1 { version("findutils", "4.6.0") } 1.

declared_dependency("findutils", "automake", "build") :- node("findutils"), 1 { version("findutils", "4.6.0") } 1.
node("automake") :- depends_on("findutils", "automake"), node("findutils"), 1 { version("findutils", "4.6.0") } 1.

declared_dependency("findutils", "libtool", "build") :- node("findutils"), 1 { version("findutils", "4.6.0") } 1.
node("libtool") :- depends_on("findutils", "libtool"), node("findutils"), 1 { version("findutils", "4.6.0") } 1.

declared_dependency("findutils", "m4", "build") :- node("findutils"), 1 { version("findutils", "4.6.0") } 1.
node("m4") :- depends_on("findutils", "m4"), node("findutils"), 1 { version("findutils", "4.6.0") } 1.

declared_dependency("findutils", "texinfo", "build") :- node("findutils"), 1 { version("findutils", "4.6.0") } 1.
node("texinfo") :- depends_on("findutils", "texinfo"), node("findutils"), 1 { version("findutils", "4.6.0") } 1.


%----------------------------------------------------------------------------
% Package: fixesproto
%----------------------------------------------------------------------------
version_declared("fixesproto", "5.0", 0).

declared_dependency("fixesproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("fixesproto", "pkgconfig"), node("fixesproto").

declared_dependency("fixesproto", "util-macros", "build").
node("util-macros") :- depends_on("fixesproto", "util-macros"), node("fixesproto").


%----------------------------------------------------------------------------
% Package: flex
%----------------------------------------------------------------------------
version_declared("flex", "2.6.4", 0).
version_declared("flex", "2.6.3", 1).
version_declared("flex", "2.6.1", 2).
version_declared("flex", "2.6.0", 3).
version_declared("flex", "2.5.39", 4).

variant("flex", "lex").
variant_single_value("flex", "lex").
variant_default_value("flex", "lex", "True").
variant_possible_value("flex", "lex", "False").
variant_possible_value("flex", "lex", "True").

declared_dependency("flex", "autoconf", "build") :- node("flex"), 1 { version("flex", "2.5.39"); version("flex", "2.6.0"); version("flex", "2.6.4") } 1.
node("autoconf") :- depends_on("flex", "autoconf"), node("flex"), 1 { version("flex", "2.5.39"); version("flex", "2.6.0"); version("flex", "2.6.4") } 1.

declared_dependency("flex", "automake", "build") :- node("flex"), 1 { version("flex", "2.5.39"); version("flex", "2.6.0"); version("flex", "2.6.4") } 1.
node("automake") :- depends_on("flex", "automake"), node("flex"), 1 { version("flex", "2.5.39"); version("flex", "2.6.0"); version("flex", "2.6.4") } 1.

declared_dependency("flex", "bison", "build").
node("bison") :- depends_on("flex", "bison"), node("flex").

declared_dependency("flex", "diffutils", "build").
node("diffutils") :- depends_on("flex", "diffutils"), node("flex").

declared_dependency("flex", "findutils", "build").
node("findutils") :- depends_on("flex", "findutils"), node("flex").

declared_dependency("flex", "gettext", "build").
node("gettext") :- depends_on("flex", "gettext"), node("flex").

declared_dependency("flex", "help2man", "build").
node("help2man") :- depends_on("flex", "help2man"), node("flex").

declared_dependency("flex", "libtool", "build") :- node("flex"), 1 { version("flex", "2.5.39"); version("flex", "2.6.0"); version("flex", "2.6.4") } 1.
node("libtool") :- depends_on("flex", "libtool"), node("flex"), 1 { version("flex", "2.5.39"); version("flex", "2.6.0"); version("flex", "2.6.4") } 1.

declared_dependency("flex", "m4", "build").
node("m4") :- depends_on("flex", "m4"), node("flex").


%----------------------------------------------------------------------------
% Package: font-util
%----------------------------------------------------------------------------
version_declared("font-util", "1.3.2", 0).
version_declared("font-util", "1.3.1", 1).

variant("font-util", "fonts").
not variant_single_value("font-util", "fonts").
variant_default_value("font-util", "fonts", "encodings").
variant_default_value("font-util", "fonts", "font-adobe-100dpi").
variant_default_value("font-util", "fonts", "font-adobe-75dpi").
variant_default_value("font-util", "fonts", "font-adobe-utopia-100dpi").
variant_default_value("font-util", "fonts", "font-adobe-utopia-75dpi").
variant_default_value("font-util", "fonts", "font-adobe-utopia-type1").
variant_default_value("font-util", "fonts", "font-alias").
variant_default_value("font-util", "fonts", "font-arabic-misc").
variant_default_value("font-util", "fonts", "font-bh-100dpi").
variant_default_value("font-util", "fonts", "font-bh-75dpi").
variant_default_value("font-util", "fonts", "font-bh-lucidatypewriter-100dpi").
variant_default_value("font-util", "fonts", "font-bh-lucidatypewriter-75dpi").
variant_default_value("font-util", "fonts", "font-bh-ttf").
variant_default_value("font-util", "fonts", "font-bh-type1").
variant_default_value("font-util", "fonts", "font-bitstream-100dpi").
variant_default_value("font-util", "fonts", "font-bitstream-75dpi").
variant_default_value("font-util", "fonts", "font-bitstream-speedo").
variant_default_value("font-util", "fonts", "font-bitstream-type1").
variant_default_value("font-util", "fonts", "font-cronyx-cyrillic").
variant_default_value("font-util", "fonts", "font-cursor-misc").
variant_default_value("font-util", "fonts", "font-daewoo-misc").
variant_default_value("font-util", "fonts", "font-dec-misc").
variant_default_value("font-util", "fonts", "font-ibm-type1").
variant_default_value("font-util", "fonts", "font-isas-misc").
variant_default_value("font-util", "fonts", "font-jis-misc").
variant_default_value("font-util", "fonts", "font-micro-misc").
variant_default_value("font-util", "fonts", "font-misc-cyrillic").
variant_default_value("font-util", "fonts", "font-misc-ethiopic").
variant_default_value("font-util", "fonts", "font-misc-meltho").
variant_default_value("font-util", "fonts", "font-misc-misc").
variant_default_value("font-util", "fonts", "font-mutt-misc").
variant_default_value("font-util", "fonts", "font-schumacher-misc").
variant_default_value("font-util", "fonts", "font-screen-cyrillic").
variant_default_value("font-util", "fonts", "font-sun-misc").
variant_default_value("font-util", "fonts", "font-winitzki-cyrillic").
variant_default_value("font-util", "fonts", "font-xfree86-type1").
variant_possible_value("font-util", "fonts", "encodings").
variant_possible_value("font-util", "fonts", "font-adobe-100dpi").
variant_possible_value("font-util", "fonts", "font-adobe-75dpi").
variant_possible_value("font-util", "fonts", "font-adobe-utopia-100dpi").
variant_possible_value("font-util", "fonts", "font-adobe-utopia-75dpi").
variant_possible_value("font-util", "fonts", "font-adobe-utopia-type1").
variant_possible_value("font-util", "fonts", "font-alias").
variant_possible_value("font-util", "fonts", "font-arabic-misc").
variant_possible_value("font-util", "fonts", "font-bh-100dpi").
variant_possible_value("font-util", "fonts", "font-bh-75dpi").
variant_possible_value("font-util", "fonts", "font-bh-lucidatypewriter-100dpi").
variant_possible_value("font-util", "fonts", "font-bh-lucidatypewriter-75dpi").
variant_possible_value("font-util", "fonts", "font-bh-ttf").
variant_possible_value("font-util", "fonts", "font-bh-type1").
variant_possible_value("font-util", "fonts", "font-bitstream-100dpi").
variant_possible_value("font-util", "fonts", "font-bitstream-75dpi").
variant_possible_value("font-util", "fonts", "font-bitstream-speedo").
variant_possible_value("font-util", "fonts", "font-bitstream-type1").
variant_possible_value("font-util", "fonts", "font-cronyx-cyrillic").
variant_possible_value("font-util", "fonts", "font-cursor-misc").
variant_possible_value("font-util", "fonts", "font-daewoo-misc").
variant_possible_value("font-util", "fonts", "font-dec-misc").
variant_possible_value("font-util", "fonts", "font-ibm-type1").
variant_possible_value("font-util", "fonts", "font-isas-misc").
variant_possible_value("font-util", "fonts", "font-jis-misc").
variant_possible_value("font-util", "fonts", "font-micro-misc").
variant_possible_value("font-util", "fonts", "font-misc-cyrillic").
variant_possible_value("font-util", "fonts", "font-misc-ethiopic").
variant_possible_value("font-util", "fonts", "font-misc-meltho").
variant_possible_value("font-util", "fonts", "font-misc-misc").
variant_possible_value("font-util", "fonts", "font-mutt-misc").
variant_possible_value("font-util", "fonts", "font-schumacher-misc").
variant_possible_value("font-util", "fonts", "font-screen-cyrillic").
variant_possible_value("font-util", "fonts", "font-sun-misc").
variant_possible_value("font-util", "fonts", "font-winitzki-cyrillic").
variant_possible_value("font-util", "fonts", "font-xfree86-type1").

declared_dependency("font-util", "autoconf", "build").
node("autoconf") :- depends_on("font-util", "autoconf"), node("font-util").

declared_dependency("font-util", "automake", "build").
node("automake") :- depends_on("font-util", "automake"), node("font-util").

declared_dependency("font-util", "bdftopcf", "build").
node("bdftopcf") :- depends_on("font-util", "bdftopcf"), node("font-util").

declared_dependency("font-util", "mkfontdir", "build").
node("mkfontdir") :- depends_on("font-util", "mkfontdir"), node("font-util").

declared_dependency("font-util", "mkfontscale", "build").
node("mkfontscale") :- depends_on("font-util", "mkfontscale"), node("font-util").

declared_dependency("font-util", "pkgconfig", "build").
node("pkgconfig") :- depends_on("font-util", "pkgconfig"), node("font-util").

declared_dependency("font-util", "util-macros", "build").
node("util-macros") :- depends_on("font-util", "util-macros"), node("font-util").


%----------------------------------------------------------------------------
% Package: fontconfig
%----------------------------------------------------------------------------
version_declared("fontconfig", "2.12.3", 0).
version_declared("fontconfig", "2.12.1", 1).
version_declared("fontconfig", "2.11.1", 2).

declared_dependency("fontconfig", "font-util", "build").
declared_dependency("fontconfig", "font-util", "link").
node("font-util") :- depends_on("fontconfig", "font-util"), node("fontconfig").

declared_dependency("fontconfig", "freetype", "build").
declared_dependency("fontconfig", "freetype", "link").
node("freetype") :- depends_on("fontconfig", "freetype"), node("fontconfig").

declared_dependency("fontconfig", "gperf", "build") :- node("fontconfig"), 1 { version("fontconfig", "2.12.3") } 1.
node("gperf") :- depends_on("fontconfig", "gperf"), node("fontconfig"), 1 { version("fontconfig", "2.12.3") } 1.

declared_dependency("fontconfig", "libxml2", "build").
declared_dependency("fontconfig", "libxml2", "link").
node("libxml2") :- depends_on("fontconfig", "libxml2"), node("fontconfig").

declared_dependency("fontconfig", "pkgconfig", "build").
node("pkgconfig") :- depends_on("fontconfig", "pkgconfig"), node("fontconfig").


%----------------------------------------------------------------------------
% Package: fontsproto
%----------------------------------------------------------------------------
version_declared("fontsproto", "2.1.3", 0).

declared_dependency("fontsproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("fontsproto", "pkgconfig"), node("fontsproto").

declared_dependency("fontsproto", "util-macros", "build").
node("util-macros") :- depends_on("fontsproto", "util-macros"), node("fontsproto").


%----------------------------------------------------------------------------
% Package: freetype
%----------------------------------------------------------------------------
version_declared("freetype", "2.10.1", 0).
version_declared("freetype", "2.9.1", 1).
version_declared("freetype", "2.7.1", 2).
version_declared("freetype", "2.7", 3).
version_declared("freetype", "2.5.3", 4).

declared_dependency("freetype", "bzip2", "build").
declared_dependency("freetype", "bzip2", "link").
node("bzip2") :- depends_on("freetype", "bzip2"), node("freetype").

declared_dependency("freetype", "libpng", "build").
declared_dependency("freetype", "libpng", "link").
node("libpng") :- depends_on("freetype", "libpng"), node("freetype").

declared_dependency("freetype", "pkgconfig", "build").
node("pkgconfig") :- depends_on("freetype", "pkgconfig"), node("freetype").


%----------------------------------------------------------------------------
% Package: fujitsu-mpi
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: gawk
%----------------------------------------------------------------------------
version_declared("gawk", "5.0.1", 0).
version_declared("gawk", "4.1.4", 1).

declared_dependency("gawk", "gettext", "build").
declared_dependency("gawk", "gettext", "link").
node("gettext") :- depends_on("gawk", "gettext"), node("gawk").

declared_dependency("gawk", "gmp", "build").
declared_dependency("gawk", "gmp", "link").
node("gmp") :- depends_on("gawk", "gmp"), node("gawk").

declared_dependency("gawk", "libsigsegv", "build").
declared_dependency("gawk", "libsigsegv", "link").
node("libsigsegv") :- depends_on("gawk", "libsigsegv"), node("gawk").

declared_dependency("gawk", "mpfr", "build").
declared_dependency("gawk", "mpfr", "link").
node("mpfr") :- depends_on("gawk", "mpfr"), node("gawk").

declared_dependency("gawk", "readline", "build").
declared_dependency("gawk", "readline", "link").
node("readline") :- depends_on("gawk", "readline"), node("gawk").


%----------------------------------------------------------------------------
% Package: gdbm
%----------------------------------------------------------------------------
version_declared("gdbm", "1.18.1", 0).
version_declared("gdbm", "1.14.1", 1).
version_declared("gdbm", "1.13", 2).
version_declared("gdbm", "1.12", 3).
version_declared("gdbm", "1.11", 4).
version_declared("gdbm", "1.10", 5).
version_declared("gdbm", "1.9.1", 6).
version_declared("gdbm", "1.9", 7).

declared_dependency("gdbm", "readline", "build").
declared_dependency("gdbm", "readline", "link").
node("readline") :- depends_on("gdbm", "readline"), node("gdbm").


%----------------------------------------------------------------------------
% Package: gdk-pixbuf
%----------------------------------------------------------------------------
version_declared("gdk-pixbuf", "2.38.0", 0).
version_declared("gdk-pixbuf", "2.31.2", 1).

declared_dependency("gdk-pixbuf", "docbook-xsl", "build").
node("docbook-xsl") :- depends_on("gdk-pixbuf", "docbook-xsl"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "gettext", "build").
declared_dependency("gdk-pixbuf", "gettext", "link").
node("gettext") :- depends_on("gdk-pixbuf", "gettext"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "glib", "build").
declared_dependency("gdk-pixbuf", "glib", "link").
node("glib") :- depends_on("gdk-pixbuf", "glib"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "gobject-introspection", "build").
declared_dependency("gdk-pixbuf", "gobject-introspection", "link").
node("gobject-introspection") :- depends_on("gdk-pixbuf", "gobject-introspection"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "jpeg", "build").
declared_dependency("gdk-pixbuf", "jpeg", "link").
node("jpeg") :- depends_on("gdk-pixbuf", "jpeg"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "libpng", "build").
declared_dependency("gdk-pixbuf", "libpng", "link").
node("libpng") :- depends_on("gdk-pixbuf", "libpng"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "libtiff", "build").
declared_dependency("gdk-pixbuf", "libtiff", "link").
node("libtiff") :- depends_on("gdk-pixbuf", "libtiff"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "libxslt", "build").
node("libxslt") :- depends_on("gdk-pixbuf", "libxslt"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "meson", "build") :- node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.
node("meson") :- depends_on("gdk-pixbuf", "meson"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.
1 { version("meson", "0.49.0"); version("meson", "0.49.1") } 1 :- depends_on("gdk-pixbuf", "meson"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.
declared_dependency("gdk-pixbuf", "meson", "build") :- node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.
node("meson") :- depends_on("gdk-pixbuf", "meson"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.
1 { version("meson", "0.49.0"); version("meson", "0.49.1") } 1 :- depends_on("gdk-pixbuf", "meson"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.

declared_dependency("gdk-pixbuf", "ninja", "build") :- node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.
node("ninja") :- depends_on("gdk-pixbuf", "ninja"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1.

declared_dependency("gdk-pixbuf", "pkgconfig", "build").
node("pkgconfig") :- depends_on("gdk-pixbuf", "pkgconfig"), node("gdk-pixbuf").

declared_dependency("gdk-pixbuf", "shared-mime-info", "build") :- node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1, node_platform("gdk-pixbuf", "cray").
node("shared-mime-info") :- depends_on("gdk-pixbuf", "shared-mime-info"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1, node_platform("gdk-pixbuf", "cray").
declared_dependency("gdk-pixbuf", "shared-mime-info", "build") :- node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1, node_platform("gdk-pixbuf", "linux").
node("shared-mime-info") :- depends_on("gdk-pixbuf", "shared-mime-info"), node("gdk-pixbuf"), 1 { version("gdk-pixbuf", "2.38.0") } 1, node_platform("gdk-pixbuf", "linux").

declared_dependency("gdk-pixbuf", "zlib", "build").
declared_dependency("gdk-pixbuf", "zlib", "link").
node("zlib") :- depends_on("gdk-pixbuf", "zlib"), node("gdk-pixbuf").


%----------------------------------------------------------------------------
% Package: gettext
%----------------------------------------------------------------------------
version_declared("gettext", "0.20.1", 0).
version_declared("gettext", "0.19.8.1", 1).
version_declared("gettext", "0.19.7", 2).

variant("gettext", "bzip2").
variant_single_value("gettext", "bzip2").
variant_default_value("gettext", "bzip2", "True").
variant_possible_value("gettext", "bzip2", "False").
variant_possible_value("gettext", "bzip2", "True").

variant("gettext", "curses").
variant_single_value("gettext", "curses").
variant_default_value("gettext", "curses", "True").
variant_possible_value("gettext", "curses", "False").
variant_possible_value("gettext", "curses", "True").

variant("gettext", "git").
variant_single_value("gettext", "git").
variant_default_value("gettext", "git", "True").
variant_possible_value("gettext", "git", "False").
variant_possible_value("gettext", "git", "True").

variant("gettext", "libunistring").
variant_single_value("gettext", "libunistring").
variant_default_value("gettext", "libunistring", "False").
variant_possible_value("gettext", "libunistring", "False").
variant_possible_value("gettext", "libunistring", "True").

variant("gettext", "libxml2").
variant_single_value("gettext", "libxml2").
variant_default_value("gettext", "libxml2", "True").
variant_possible_value("gettext", "libxml2", "False").
variant_possible_value("gettext", "libxml2", "True").

variant("gettext", "tar").
variant_single_value("gettext", "tar").
variant_default_value("gettext", "tar", "True").
variant_possible_value("gettext", "tar", "False").
variant_possible_value("gettext", "tar", "True").

variant("gettext", "xz").
variant_single_value("gettext", "xz").
variant_default_value("gettext", "xz", "True").
variant_possible_value("gettext", "xz", "False").
variant_possible_value("gettext", "xz", "True").

declared_dependency("gettext", "bzip2", "build") :- node("gettext"), variant_value("gettext", "bzip2", "True").
declared_dependency("gettext", "bzip2", "link") :- node("gettext"), variant_value("gettext", "bzip2", "True").
node("bzip2") :- depends_on("gettext", "bzip2"), node("gettext"), variant_value("gettext", "bzip2", "True").

declared_dependency("gettext", "libunistring", "build") :- node("gettext"), variant_value("gettext", "libunistring", "True").
declared_dependency("gettext", "libunistring", "link") :- node("gettext"), variant_value("gettext", "libunistring", "True").
node("libunistring") :- depends_on("gettext", "libunistring"), node("gettext"), variant_value("gettext", "libunistring", "True").

declared_dependency("gettext", "libxml2", "build") :- node("gettext"), variant_value("gettext", "libxml2", "True").
declared_dependency("gettext", "libxml2", "link") :- node("gettext"), variant_value("gettext", "libxml2", "True").
node("libxml2") :- depends_on("gettext", "libxml2"), node("gettext"), variant_value("gettext", "libxml2", "True").

declared_dependency("gettext", "ncurses", "build") :- node("gettext"), variant_value("gettext", "curses", "True").
declared_dependency("gettext", "ncurses", "link") :- node("gettext"), variant_value("gettext", "curses", "True").
node("ncurses") :- depends_on("gettext", "ncurses"), node("gettext"), variant_value("gettext", "curses", "True").

declared_dependency("gettext", "tar", "build") :- node("gettext"), variant_value("gettext", "tar", "True").
declared_dependency("gettext", "tar", "link") :- node("gettext"), variant_value("gettext", "tar", "True").
node("tar") :- depends_on("gettext", "tar"), node("gettext"), variant_value("gettext", "tar", "True").

declared_dependency("gettext", "xz", "build") :- node("gettext"), variant_value("gettext", "xz", "True").
declared_dependency("gettext", "xz", "link") :- node("gettext"), variant_value("gettext", "xz", "True").
declared_dependency("gettext", "xz", "run") :- node("gettext"), variant_value("gettext", "xz", "True").
node("xz") :- depends_on("gettext", "xz"), node("gettext"), variant_value("gettext", "xz", "True").


%----------------------------------------------------------------------------
% Package: giflib
%----------------------------------------------------------------------------
version_declared("giflib", "5.1.4", 0).


%----------------------------------------------------------------------------
% Package: git
%----------------------------------------------------------------------------
version_declared("git", "2.25.0", 0).
version_declared("git", "2.21.0", 1).
version_declared("git", "2.20.1", 2).
version_declared("git", "2.19.2", 3).
version_declared("git", "2.19.1", 4).
version_declared("git", "2.18.0", 5).
version_declared("git", "2.17.1", 6).
version_declared("git", "2.17.0", 7).
version_declared("git", "2.15.1", 8).
version_declared("git", "2.14.1", 9).
version_declared("git", "2.13.0", 10).
version_declared("git", "2.12.2", 11).
version_declared("git", "2.12.1", 12).
version_declared("git", "2.12.0", 13).
version_declared("git", "2.11.1", 14).
version_declared("git", "2.11.0", 15).
version_declared("git", "2.9.3", 16).
version_declared("git", "2.9.2", 17).
version_declared("git", "2.9.1", 18).
version_declared("git", "2.9.0", 19).
version_declared("git", "2.8.4", 20).
version_declared("git", "2.8.3", 21).
version_declared("git", "2.8.2", 22).
version_declared("git", "2.8.1", 23).
version_declared("git", "2.8.0", 24).
version_declared("git", "2.7.3", 25).
version_declared("git", "2.7.1", 26).

variant("git", "tcltk").
variant_single_value("git", "tcltk").
variant_default_value("git", "tcltk", "False").
variant_possible_value("git", "tcltk", "False").
variant_possible_value("git", "tcltk", "True").

declared_dependency("git", "autoconf", "build").
node("autoconf") :- depends_on("git", "autoconf"), node("git").

declared_dependency("git", "automake", "build").
node("automake") :- depends_on("git", "automake"), node("git").

declared_dependency("git", "curl", "build").
declared_dependency("git", "curl", "link").
node("curl") :- depends_on("git", "curl"), node("git").

declared_dependency("git", "expat", "build").
declared_dependency("git", "expat", "link").
node("expat") :- depends_on("git", "expat"), node("git").

declared_dependency("git", "gettext", "build").
declared_dependency("git", "gettext", "link").
node("gettext") :- depends_on("git", "gettext"), node("git").

declared_dependency("git", "libiconv", "build").
declared_dependency("git", "libiconv", "link").
node("libiconv") :- depends_on("git", "libiconv"), node("git").

declared_dependency("git", "libtool", "build").
node("libtool") :- depends_on("git", "libtool"), node("git").

declared_dependency("git", "m4", "build").
node("m4") :- depends_on("git", "m4"), node("git").

declared_dependency("git", "openssl", "build").
declared_dependency("git", "openssl", "link").
node("openssl") :- depends_on("git", "openssl"), node("git").

declared_dependency("git", "pcre", "build") :- node("git"), 1 { version("git", "2.7.1"); version("git", "2.7.3"); version("git", "2.8.0"); version("git", "2.8.1"); version("git", "2.8.2"); version("git", "2.8.3"); version("git", "2.8.4"); version("git", "2.9.0"); version("git", "2.9.1"); version("git", "2.9.2"); version("git", "2.9.3"); version("git", "2.11.0"); version("git", "2.11.1"); version("git", "2.12.0"); version("git", "2.12.1"); version("git", "2.12.2"); version("git", "2.13.0") } 1.
declared_dependency("git", "pcre", "link") :- node("git"), 1 { version("git", "2.7.1"); version("git", "2.7.3"); version("git", "2.8.0"); version("git", "2.8.1"); version("git", "2.8.2"); version("git", "2.8.3"); version("git", "2.8.4"); version("git", "2.9.0"); version("git", "2.9.1"); version("git", "2.9.2"); version("git", "2.9.3"); version("git", "2.11.0"); version("git", "2.11.1"); version("git", "2.12.0"); version("git", "2.12.1"); version("git", "2.12.2"); version("git", "2.13.0") } 1.
node("pcre") :- depends_on("git", "pcre"), node("git"), 1 { version("git", "2.7.1"); version("git", "2.7.3"); version("git", "2.8.0"); version("git", "2.8.1"); version("git", "2.8.2"); version("git", "2.8.3"); version("git", "2.8.4"); version("git", "2.9.0"); version("git", "2.9.1"); version("git", "2.9.2"); version("git", "2.9.3"); version("git", "2.11.0"); version("git", "2.11.1"); version("git", "2.12.0"); version("git", "2.12.1"); version("git", "2.12.2"); version("git", "2.13.0") } 1.

declared_dependency("git", "pcre2", "build") :- node("git"), 1 { version("git", "2.14.1"); version("git", "2.15.1"); version("git", "2.17.0"); version("git", "2.17.1"); version("git", "2.18.0"); version("git", "2.19.1"); version("git", "2.19.2"); version("git", "2.20.1"); version("git", "2.21.0"); version("git", "2.25.0") } 1.
declared_dependency("git", "pcre2", "link") :- node("git"), 1 { version("git", "2.14.1"); version("git", "2.15.1"); version("git", "2.17.0"); version("git", "2.17.1"); version("git", "2.18.0"); version("git", "2.19.1"); version("git", "2.19.2"); version("git", "2.20.1"); version("git", "2.21.0"); version("git", "2.25.0") } 1.
node("pcre2") :- depends_on("git", "pcre2"), node("git"), 1 { version("git", "2.14.1"); version("git", "2.15.1"); version("git", "2.17.0"); version("git", "2.17.1"); version("git", "2.18.0"); version("git", "2.19.1"); version("git", "2.19.2"); version("git", "2.20.1"); version("git", "2.21.0"); version("git", "2.25.0") } 1.

declared_dependency("git", "perl", "build").
declared_dependency("git", "perl", "link").
node("perl") :- depends_on("git", "perl"), node("git").

declared_dependency("git", "tk", "build") :- node("git"), variant_value("git", "tcltk", "True").
declared_dependency("git", "tk", "link") :- node("git"), variant_value("git", "tcltk", "True").
node("tk") :- depends_on("git", "tk"), node("git"), variant_value("git", "tcltk", "True").

declared_dependency("git", "zlib", "build").
declared_dependency("git", "zlib", "link").
node("zlib") :- depends_on("git", "zlib"), node("git").


%----------------------------------------------------------------------------
% Package: glib
%----------------------------------------------------------------------------
version_declared("glib", "2.56.3", 0).
version_declared("glib", "2.56.2", 1).
version_declared("glib", "2.56.1", 2).
version_declared("glib", "2.56.0", 3).
version_declared("glib", "2.55.1", 4).
version_declared("glib", "2.53.1", 5).
version_declared("glib", "2.49.7", 6).
version_declared("glib", "2.49.4", 7).
version_declared("glib", "2.48.1", 8).
version_declared("glib", "2.42.1", 9).

variant("glib", "libmount").
variant_single_value("glib", "libmount").
variant_default_value("glib", "libmount", "False").
variant_possible_value("glib", "libmount", "False").
variant_possible_value("glib", "libmount", "True").

variant("glib", "tracing").
not variant_single_value("glib", "tracing").
variant_default_value("glib", "tracing", "none").
variant_possible_value("glib", "tracing", "dtrace").
variant_possible_value("glib", "tracing", "none").
variant_possible_value("glib", "tracing", "systemtap").

declared_dependency("glib", "gettext", "build").
declared_dependency("glib", "gettext", "link").
node("gettext") :- depends_on("glib", "gettext"), node("glib").

declared_dependency("glib", "libffi", "build").
declared_dependency("glib", "libffi", "link").
node("libffi") :- depends_on("glib", "libffi"), node("glib").

declared_dependency("glib", "libiconv", "build").
declared_dependency("glib", "libiconv", "link").
node("libiconv") :- depends_on("glib", "libiconv"), node("glib").

declared_dependency("glib", "pcre", "build") :- node("glib"), 1 { version("glib", "2.48.1"); version("glib", "2.49.4"); version("glib", "2.49.7"); version("glib", "2.53.1"); version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.
declared_dependency("glib", "pcre", "link") :- node("glib"), 1 { version("glib", "2.48.1"); version("glib", "2.49.4"); version("glib", "2.49.7"); version("glib", "2.53.1"); version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.
node("pcre") :- depends_on("glib", "pcre"), node("glib"), 1 { version("glib", "2.48.1"); version("glib", "2.49.4"); version("glib", "2.49.7"); version("glib", "2.53.1"); version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.
variant_set("pcre", "utf", "True") :- depends_on("glib", "pcre"), node("glib"), 1 { version("glib", "2.48.1"); version("glib", "2.49.4"); version("glib", "2.49.7"); version("glib", "2.53.1"); version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.

declared_dependency("glib", "perl", "build").
declared_dependency("glib", "perl", "run").
node("perl") :- depends_on("glib", "perl"), node("glib").

declared_dependency("glib", "pkgconfig", "build").
node("pkgconfig") :- depends_on("glib", "pkgconfig"), node("glib").

declared_dependency("glib", "python", "build") :- node("glib"), 1 { version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.
declared_dependency("glib", "python", "run") :- node("glib"), 1 { version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.
node("python") :- depends_on("glib", "python"), node("glib"), 1 { version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1.

declared_dependency("glib", "util-linux", "build") :- node("glib"), variant_value("glib", "libmount", "True").
declared_dependency("glib", "util-linux", "link") :- node("glib"), variant_value("glib", "libmount", "True").
node("util-linux") :- depends_on("glib", "util-linux"), node("glib"), variant_value("glib", "libmount", "True").

declared_dependency("glib", "zlib", "build").
declared_dependency("glib", "zlib", "link").
node("zlib") :- depends_on("glib", "zlib"), node("glib").


%----------------------------------------------------------------------------
% Package: glproto
%----------------------------------------------------------------------------
version_declared("glproto", "1.4.17", 0).

declared_dependency("glproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("glproto", "pkgconfig"), node("glproto").

declared_dependency("glproto", "util-macros", "build").
node("util-macros") :- depends_on("glproto", "util-macros"), node("glproto").


%----------------------------------------------------------------------------
% Package: gmake
%----------------------------------------------------------------------------
version_declared("gmake", "4.2.1", 0).
version_declared("gmake", "4.0", 1).

variant("gmake", "guile").
variant_single_value("gmake", "guile").
variant_default_value("gmake", "guile", "False").
variant_possible_value("gmake", "guile", "False").
variant_possible_value("gmake", "guile", "True").

variant("gmake", "nls").
variant_single_value("gmake", "nls").
variant_default_value("gmake", "nls", "True").
variant_possible_value("gmake", "nls", "False").
variant_possible_value("gmake", "nls", "True").

declared_dependency("gmake", "gettext", "build") :- node("gmake"), variant_value("gmake", "nls", "True").
declared_dependency("gmake", "gettext", "link") :- node("gmake"), variant_value("gmake", "nls", "True").
node("gettext") :- depends_on("gmake", "gettext"), node("gmake"), variant_value("gmake", "nls", "True").

declared_dependency("gmake", "guile", "build") :- node("gmake"), variant_value("gmake", "guile", "True").
declared_dependency("gmake", "guile", "link") :- node("gmake"), variant_value("gmake", "guile", "True").
node("guile") :- depends_on("gmake", "guile"), node("gmake"), variant_value("gmake", "guile", "True").

declared_dependency("gmake", "texinfo", "build").
node("texinfo") :- depends_on("gmake", "texinfo"), node("gmake").


%----------------------------------------------------------------------------
% Package: gmp
%----------------------------------------------------------------------------
version_declared("gmp", "6.1.2", 0).
version_declared("gmp", "6.1.1", 1).
version_declared("gmp", "6.1.0", 2).
version_declared("gmp", "6.0.0a", 3).
version_declared("gmp", "5.1.3", 4).
version_declared("gmp", "4.3.2", 5).

declared_dependency("gmp", "autoconf", "build").
node("autoconf") :- depends_on("gmp", "autoconf"), node("gmp").

declared_dependency("gmp", "automake", "build").
node("automake") :- depends_on("gmp", "automake"), node("gmp").

declared_dependency("gmp", "libtool", "build").
node("libtool") :- depends_on("gmp", "libtool"), node("gmp").

declared_dependency("gmp", "m4", "build").
node("m4") :- depends_on("gmp", "m4"), node("gmp").


%----------------------------------------------------------------------------
% Package: gnutls
%----------------------------------------------------------------------------
version_declared("gnutls", "3.6.8", 0).
version_declared("gnutls", "3.6.7.1", 1).
version_declared("gnutls", "3.5.19", 2).
version_declared("gnutls", "3.5.13", 3).
version_declared("gnutls", "3.5.10", 4).
version_declared("gnutls", "3.5.9", 5).
version_declared("gnutls", "3.3.9", 6).

variant("gnutls", "guile").
variant_single_value("gnutls", "guile").
variant_default_value("gnutls", "guile", "False").
variant_possible_value("gnutls", "guile", "False").
variant_possible_value("gnutls", "guile", "True").

variant("gnutls", "zlib").
variant_single_value("gnutls", "zlib").
variant_default_value("gnutls", "zlib", "True").
variant_possible_value("gnutls", "zlib", "False").
variant_possible_value("gnutls", "zlib", "True").

declared_dependency("gnutls", "gettext", "build").
declared_dependency("gnutls", "gettext", "link").
node("gettext") :- depends_on("gnutls", "gettext"), node("gnutls").

declared_dependency("gnutls", "guile", "build") :- node("gnutls"), variant_value("gnutls", "guile", "True").
declared_dependency("gnutls", "guile", "link") :- node("gnutls"), variant_value("gnutls", "guile", "True").
node("guile") :- depends_on("gnutls", "guile"), node("gnutls"), variant_value("gnutls", "guile", "True").

declared_dependency("gnutls", "libidn2", "build") :- node("gnutls"), 1 { version("gnutls", "3.3.9"); version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19") } 1.
declared_dependency("gnutls", "libidn2", "link") :- node("gnutls"), 1 { version("gnutls", "3.3.9"); version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19") } 1.
node("libidn2") :- depends_on("gnutls", "libidn2"), node("gnutls"), 1 { version("gnutls", "3.3.9"); version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19") } 1.
1 { version("libidn2", "2.0.5") } 1 :- depends_on("gnutls", "libidn2"), node("gnutls"), 1 { version("gnutls", "3.3.9"); version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19") } 1.

declared_dependency("gnutls", "nettle", "build") :- node("gnutls"), 1 { version("gnutls", "3.3.9") } 1.
declared_dependency("gnutls", "nettle", "link") :- node("gnutls"), 1 { version("gnutls", "3.3.9") } 1.
node("nettle") :- depends_on("gnutls", "nettle"), node("gnutls"), 1 { version("gnutls", "3.3.9") } 1.
1 { version("nettle", "2.7"); version("nettle", "2.7.1") } 1 :- depends_on("gnutls", "nettle"), node("gnutls"), 1 { version("gnutls", "3.3.9") } 1.
declared_dependency("gnutls", "nettle", "build") :- node("gnutls"), 1 { version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19"); version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.
declared_dependency("gnutls", "nettle", "link") :- node("gnutls"), 1 { version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19"); version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.
node("nettle") :- depends_on("gnutls", "nettle"), node("gnutls"), 1 { version("gnutls", "3.5.9"); version("gnutls", "3.5.10"); version("gnutls", "3.5.13"); version("gnutls", "3.5.19"); version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.
declared_dependency("gnutls", "nettle", "build") :- node("gnutls"), 1 { version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.
declared_dependency("gnutls", "nettle", "link") :- node("gnutls"), 1 { version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.
node("nettle") :- depends_on("gnutls", "nettle"), node("gnutls"), 1 { version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.
1 { version("nettle", "3.4"); version("nettle", "3.4.1") } 1 :- depends_on("gnutls", "nettle"), node("gnutls"), 1 { version("gnutls", "3.6.7.1"); version("gnutls", "3.6.8") } 1.

declared_dependency("gnutls", "pkgconfig", "build").
node("pkgconfig") :- depends_on("gnutls", "pkgconfig"), node("gnutls").

declared_dependency("gnutls", "zlib", "build") :- node("gnutls"), variant_value("gnutls", "zlib", "True").
declared_dependency("gnutls", "zlib", "link") :- node("gnutls"), variant_value("gnutls", "zlib", "True").
node("zlib") :- depends_on("gnutls", "zlib"), node("gnutls"), variant_value("gnutls", "zlib", "True").


%----------------------------------------------------------------------------
% Package: gobject-introspection
%----------------------------------------------------------------------------
version_declared("gobject-introspection", "1.56.1", 0).
version_declared("gobject-introspection", "1.49.2", 1).
version_declared("gobject-introspection", "1.48.0", 2).

declared_dependency("gobject-introspection", "bison", "build").
node("bison") :- depends_on("gobject-introspection", "bison"), node("gobject-introspection").

declared_dependency("gobject-introspection", "cairo", "build").
declared_dependency("gobject-introspection", "cairo", "link").
node("cairo") :- depends_on("gobject-introspection", "cairo"), node("gobject-introspection").

declared_dependency("gobject-introspection", "flex", "build").
node("flex") :- depends_on("gobject-introspection", "flex"), node("gobject-introspection").

declared_dependency("gobject-introspection", "glib", "build") :- node("gobject-introspection"), 1 { version("gobject-introspection", "1.48.0") } 1.
declared_dependency("gobject-introspection", "glib", "link") :- node("gobject-introspection"), 1 { version("gobject-introspection", "1.48.0") } 1.
node("glib") :- depends_on("gobject-introspection", "glib"), node("gobject-introspection"), 1 { version("gobject-introspection", "1.48.0") } 1.
1 { version("glib", "2.48.1") } 1 :- depends_on("gobject-introspection", "glib"), node("gobject-introspection"), 1 { version("gobject-introspection", "1.48.0") } 1.
declared_dependency("gobject-introspection", "glib", "build") :- node("gobject-introspection"), 1 { version("gobject-introspection", "1.49.2"); version("gobject-introspection", "1.56.1") } 1.
declared_dependency("gobject-introspection", "glib", "link") :- node("gobject-introspection"), 1 { version("gobject-introspection", "1.49.2"); version("gobject-introspection", "1.56.1") } 1.
node("glib") :- depends_on("gobject-introspection", "glib"), node("gobject-introspection"), 1 { version("gobject-introspection", "1.49.2"); version("gobject-introspection", "1.56.1") } 1.
1 { version("glib", "2.49.4"); version("glib", "2.49.7"); version("glib", "2.53.1"); version("glib", "2.55.1"); version("glib", "2.56.0"); version("glib", "2.56.1"); version("glib", "2.56.2"); version("glib", "2.56.3") } 1 :- depends_on("gobject-introspection", "glib"), node("gobject-introspection"), 1 { version("gobject-introspection", "1.49.2"); version("gobject-introspection", "1.56.1") } 1.

declared_dependency("gobject-introspection", "pkgconfig", "build").
node("pkgconfig") :- depends_on("gobject-introspection", "pkgconfig"), node("gobject-introspection").

declared_dependency("gobject-introspection", "python", "build").
declared_dependency("gobject-introspection", "python", "link").
node("python") :- depends_on("gobject-introspection", "python"), node("gobject-introspection").

declared_dependency("gobject-introspection", "sed", "build") :- node("gobject-introspection"), node_platform("gobject-introspection", "darwin").
node("sed") :- depends_on("gobject-introspection", "sed"), node("gobject-introspection"), node_platform("gobject-introspection", "darwin").


%----------------------------------------------------------------------------
% Package: gperf
%----------------------------------------------------------------------------
version_declared("gperf", "3.0.4", 0).


%----------------------------------------------------------------------------
% Package: graphite2
%----------------------------------------------------------------------------
version_declared("graphite2", "1.3.13", 0).

variant("graphite2", "build_type").
variant_single_value("graphite2", "build_type").
variant_default_value("graphite2", "build_type", "RelWithDebInfo").
variant_possible_value("graphite2", "build_type", "Debug").
variant_possible_value("graphite2", "build_type", "MinSizeRel").
variant_possible_value("graphite2", "build_type", "RelWithDebInfo").
variant_possible_value("graphite2", "build_type", "Release").

declared_dependency("graphite2", "cmake", "build").
node("cmake") :- depends_on("graphite2", "cmake"), node("graphite2").


%----------------------------------------------------------------------------
% Package: gtkplus
%----------------------------------------------------------------------------
version_declared("gtkplus", "3.20.10", 0).
version_declared("gtkplus", "2.24.32", 1).
version_declared("gtkplus", "2.24.31", 2).
version_declared("gtkplus", "2.24.25", 3).

variant("gtkplus", "cups").
variant_single_value("gtkplus", "cups").
variant_default_value("gtkplus", "cups", "False").
variant_possible_value("gtkplus", "cups", "False").
variant_possible_value("gtkplus", "cups", "True").

declared_dependency("gtkplus", "at-spi2-atk", "build") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
declared_dependency("gtkplus", "at-spi2-atk", "link") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
node("at-spi2-atk") :- depends_on("gtkplus", "at-spi2-atk"), node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.

declared_dependency("gtkplus", "atk", "build").
declared_dependency("gtkplus", "atk", "link").
node("atk") :- depends_on("gtkplus", "atk"), node("gtkplus").

declared_dependency("gtkplus", "cairo", "build").
declared_dependency("gtkplus", "cairo", "link").
node("cairo") :- depends_on("gtkplus", "cairo"), node("gtkplus").
variant_set("cairo", "X", "True") :- depends_on("gtkplus", "cairo"), node("gtkplus").
variant_set("cairo", "gobject", "True") :- depends_on("gtkplus", "cairo"), node("gtkplus").
variant_set("cairo", "pdf", "True") :- depends_on("gtkplus", "cairo"), node("gtkplus").

declared_dependency("gtkplus", "cups", "build") :- node("gtkplus"), variant_value("gtkplus", "cups", "True").
declared_dependency("gtkplus", "cups", "link") :- node("gtkplus"), variant_value("gtkplus", "cups", "True").
node("cups") :- depends_on("gtkplus", "cups"), node("gtkplus"), variant_value("gtkplus", "cups", "True").

declared_dependency("gtkplus", "fixesproto", "build") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
declared_dependency("gtkplus", "fixesproto", "link") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
node("fixesproto") :- depends_on("gtkplus", "fixesproto"), node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.

declared_dependency("gtkplus", "gdk-pixbuf", "build").
declared_dependency("gtkplus", "gdk-pixbuf", "link").
node("gdk-pixbuf") :- depends_on("gtkplus", "gdk-pixbuf"), node("gtkplus").

declared_dependency("gtkplus", "gettext", "build") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
declared_dependency("gtkplus", "gettext", "link") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
node("gettext") :- depends_on("gtkplus", "gettext"), node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.

declared_dependency("gtkplus", "glib", "build").
declared_dependency("gtkplus", "glib", "link").
node("glib") :- depends_on("gtkplus", "glib"), node("gtkplus").

declared_dependency("gtkplus", "gobject-introspection", "build").
declared_dependency("gtkplus", "gobject-introspection", "link").
node("gobject-introspection") :- depends_on("gtkplus", "gobject-introspection"), node("gtkplus").

declared_dependency("gtkplus", "inputproto", "build") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
declared_dependency("gtkplus", "inputproto", "link") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
node("inputproto") :- depends_on("gtkplus", "inputproto"), node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.

declared_dependency("gtkplus", "libepoxy", "build") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
declared_dependency("gtkplus", "libepoxy", "link") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
node("libepoxy") :- depends_on("gtkplus", "libepoxy"), node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.

declared_dependency("gtkplus", "libxi", "build") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
declared_dependency("gtkplus", "libxi", "link") :- node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.
node("libxi") :- depends_on("gtkplus", "libxi"), node("gtkplus"), 1 { version("gtkplus", "3.20.10") } 1.

declared_dependency("gtkplus", "pango", "build").
declared_dependency("gtkplus", "pango", "link").
node("pango") :- depends_on("gtkplus", "pango"), node("gtkplus").
variant_set("pango", "X", "True") :- depends_on("gtkplus", "pango"), node("gtkplus").

declared_dependency("gtkplus", "pkgconfig", "build").
node("pkgconfig") :- depends_on("gtkplus", "pkgconfig"), node("gtkplus").

declared_dependency("gtkplus", "shared-mime-info", "build").
declared_dependency("gtkplus", "shared-mime-info", "link").
node("shared-mime-info") :- depends_on("gtkplus", "shared-mime-info"), node("gtkplus").


%----------------------------------------------------------------------------
% Package: guile
%----------------------------------------------------------------------------
version_declared("guile", "2.2.6", 0).
version_declared("guile", "2.2.5", 1).
version_declared("guile", "2.2.4", 2).
version_declared("guile", "2.2.3", 3).
version_declared("guile", "2.2.2", 4).
version_declared("guile", "2.2.1", 5).
version_declared("guile", "2.2.0", 6).
version_declared("guile", "2.0.14", 7).
version_declared("guile", "2.0.11", 8).

variant("guile", "readline").
variant_single_value("guile", "readline").
variant_default_value("guile", "readline", "True").
variant_possible_value("guile", "readline", "False").
variant_possible_value("guile", "readline", "True").

variant("guile", "threads").
variant_single_value("guile", "threads").
variant_default_value("guile", "threads", "none").
variant_possible_value("guile", "threads", "dgux386").
variant_possible_value("guile", "threads", "none").
variant_possible_value("guile", "threads", "posix").

declared_dependency("guile", "bdw-gc", "build") :- node("guile"), variant_value("guile", "threads", "dgux386").
declared_dependency("guile", "bdw-gc", "link") :- node("guile"), variant_value("guile", "threads", "dgux386").
node("bdw-gc") :- depends_on("guile", "bdw-gc"), node("guile"), variant_value("guile", "threads", "dgux386").
variant_set("bdw-gc", "threads", "dgux386") :- depends_on("guile", "bdw-gc"), node("guile"), variant_value("guile", "threads", "dgux386").
declared_dependency("guile", "bdw-gc", "build") :- node("guile"), variant_value("guile", "threads", "none").
declared_dependency("guile", "bdw-gc", "link") :- node("guile"), variant_value("guile", "threads", "none").
node("bdw-gc") :- depends_on("guile", "bdw-gc"), node("guile"), variant_value("guile", "threads", "none").
variant_set("bdw-gc", "threads", "none") :- depends_on("guile", "bdw-gc"), node("guile"), variant_value("guile", "threads", "none").
declared_dependency("guile", "bdw-gc", "build") :- node("guile"), variant_value("guile", "threads", "posix").
declared_dependency("guile", "bdw-gc", "link") :- node("guile"), variant_value("guile", "threads", "posix").
node("bdw-gc") :- depends_on("guile", "bdw-gc"), node("guile"), variant_value("guile", "threads", "posix").
variant_set("bdw-gc", "threads", "posix") :- depends_on("guile", "bdw-gc"), node("guile"), variant_value("guile", "threads", "posix").

declared_dependency("guile", "gettext", "build").
declared_dependency("guile", "gettext", "link").
node("gettext") :- depends_on("guile", "gettext"), node("guile").

declared_dependency("guile", "gmp", "build").
declared_dependency("guile", "gmp", "link").
node("gmp") :- depends_on("guile", "gmp"), node("guile").

declared_dependency("guile", "libffi", "build").
declared_dependency("guile", "libffi", "link").
node("libffi") :- depends_on("guile", "libffi"), node("guile").

declared_dependency("guile", "libtool", "build").
declared_dependency("guile", "libtool", "link").
node("libtool") :- depends_on("guile", "libtool"), node("guile").

declared_dependency("guile", "libunistring", "build").
declared_dependency("guile", "libunistring", "link").
node("libunistring") :- depends_on("guile", "libunistring"), node("guile").

declared_dependency("guile", "pkgconfig", "build").
node("pkgconfig") :- depends_on("guile", "pkgconfig"), node("guile").

declared_dependency("guile", "readline", "build") :- node("guile"), variant_value("guile", "readline", "True").
declared_dependency("guile", "readline", "link") :- node("guile"), variant_value("guile", "readline", "True").
node("readline") :- depends_on("guile", "readline"), node("guile"), variant_value("guile", "readline", "True").


%----------------------------------------------------------------------------
% Package: gzip
%----------------------------------------------------------------------------
version_declared("gzip", "1.10", 0).


%----------------------------------------------------------------------------
% Package: harfbuzz
%----------------------------------------------------------------------------
version_declared("harfbuzz", "2.3.1", 0).
version_declared("harfbuzz", "2.1.3", 1).
version_declared("harfbuzz", "1.9.0", 2).
version_declared("harfbuzz", "1.4.6", 3).
version_declared("harfbuzz", "0.9.37", 4).

variant("harfbuzz", "graphite2").
variant_single_value("harfbuzz", "graphite2").
variant_default_value("harfbuzz", "graphite2", "False").
variant_possible_value("harfbuzz", "graphite2", "False").
variant_possible_value("harfbuzz", "graphite2", "True").

declared_dependency("harfbuzz", "cairo", "build").
declared_dependency("harfbuzz", "cairo", "link").
node("cairo") :- depends_on("harfbuzz", "cairo"), node("harfbuzz").

declared_dependency("harfbuzz", "freetype", "build").
declared_dependency("harfbuzz", "freetype", "link").
node("freetype") :- depends_on("harfbuzz", "freetype"), node("harfbuzz").

declared_dependency("harfbuzz", "glib", "build").
declared_dependency("harfbuzz", "glib", "link").
node("glib") :- depends_on("harfbuzz", "glib"), node("harfbuzz").

declared_dependency("harfbuzz", "graphite2", "build") :- node("harfbuzz"), variant_value("harfbuzz", "graphite2", "True").
declared_dependency("harfbuzz", "graphite2", "link") :- node("harfbuzz"), variant_value("harfbuzz", "graphite2", "True").
node("graphite2") :- depends_on("harfbuzz", "graphite2"), node("harfbuzz"), variant_value("harfbuzz", "graphite2", "True").

declared_dependency("harfbuzz", "icu4c", "build").
declared_dependency("harfbuzz", "icu4c", "link").
node("icu4c") :- depends_on("harfbuzz", "icu4c"), node("harfbuzz").

declared_dependency("harfbuzz", "pkgconfig", "build").
node("pkgconfig") :- depends_on("harfbuzz", "pkgconfig"), node("harfbuzz").

declared_dependency("harfbuzz", "zlib", "build").
declared_dependency("harfbuzz", "zlib", "link").
node("zlib") :- depends_on("harfbuzz", "zlib"), node("harfbuzz").


%----------------------------------------------------------------------------
% Package: hdf5
%----------------------------------------------------------------------------
version_declared("hdf5", "1.10.6", 0).
version_declared("hdf5", "1.10.5", 1).
version_declared("hdf5", "1.10.4", 2).
version_declared("hdf5", "1.10.3", 3).
version_declared("hdf5", "1.10.2", 4).
version_declared("hdf5", "1.10.1", 5).
version_declared("hdf5", "1.10.0-patch1", 6).
version_declared("hdf5", "1.10.0", 7).
version_declared("hdf5", "1.8.21", 8).
version_declared("hdf5", "1.8.19", 9).
version_declared("hdf5", "1.8.18", 10).
version_declared("hdf5", "1.8.17", 11).
version_declared("hdf5", "1.8.16", 12).
version_declared("hdf5", "1.8.15", 13).
version_declared("hdf5", "1.8.14", 14).
version_declared("hdf5", "1.8.13", 15).
version_declared("hdf5", "1.8.12", 16).
version_declared("hdf5", "1.8.10", 17).
version_declared("hdf5", "develop", 18).

variant("hdf5", "cxx").
variant_single_value("hdf5", "cxx").
variant_default_value("hdf5", "cxx", "False").
variant_possible_value("hdf5", "cxx", "False").
variant_possible_value("hdf5", "cxx", "True").

variant("hdf5", "debug").
variant_single_value("hdf5", "debug").
variant_default_value("hdf5", "debug", "False").
variant_possible_value("hdf5", "debug", "False").
variant_possible_value("hdf5", "debug", "True").

variant("hdf5", "fortran").
variant_single_value("hdf5", "fortran").
variant_default_value("hdf5", "fortran", "False").
variant_possible_value("hdf5", "fortran", "False").
variant_possible_value("hdf5", "fortran", "True").

variant("hdf5", "hl").
variant_single_value("hdf5", "hl").
variant_default_value("hdf5", "hl", "False").
variant_possible_value("hdf5", "hl", "False").
variant_possible_value("hdf5", "hl", "True").

variant("hdf5", "mpi").
variant_single_value("hdf5", "mpi").
variant_default_value("hdf5", "mpi", "True").
variant_possible_value("hdf5", "mpi", "False").
variant_possible_value("hdf5", "mpi", "True").

variant("hdf5", "pic").
variant_single_value("hdf5", "pic").
variant_default_value("hdf5", "pic", "True").
variant_possible_value("hdf5", "pic", "False").
variant_possible_value("hdf5", "pic", "True").

variant("hdf5", "shared").
variant_single_value("hdf5", "shared").
variant_default_value("hdf5", "shared", "True").
variant_possible_value("hdf5", "shared", "False").
variant_possible_value("hdf5", "shared", "True").

variant("hdf5", "szip").
variant_single_value("hdf5", "szip").
variant_default_value("hdf5", "szip", "False").
variant_possible_value("hdf5", "szip", "False").
variant_possible_value("hdf5", "szip", "True").

variant("hdf5", "threadsafe").
variant_single_value("hdf5", "threadsafe").
variant_default_value("hdf5", "threadsafe", "False").
variant_possible_value("hdf5", "threadsafe", "False").
variant_possible_value("hdf5", "threadsafe", "True").

declared_dependency("hdf5", "autoconf", "build") :- node("hdf5"), 1 { version("hdf5", "develop") } 1.
node("autoconf") :- depends_on("hdf5", "autoconf"), node("hdf5"), 1 { version("hdf5", "develop") } 1.

declared_dependency("hdf5", "automake", "build") :- node("hdf5"), 1 { version("hdf5", "develop") } 1.
node("automake") :- depends_on("hdf5", "automake"), node("hdf5"), 1 { version("hdf5", "develop") } 1.

declared_dependency("hdf5", "libtool", "build") :- node("hdf5"), 1 { version("hdf5", "develop") } 1.
node("libtool") :- depends_on("hdf5", "libtool"), node("hdf5"), 1 { version("hdf5", "develop") } 1.

declared_dependency("hdf5", "m4", "build") :- node("hdf5"), 1 { version("hdf5", "develop") } 1.
node("m4") :- depends_on("hdf5", "m4"), node("hdf5"), 1 { version("hdf5", "develop") } 1.

declared_dependency("hdf5", "mpi", "build") :- node("hdf5"), variant_value("hdf5", "mpi", "True").
declared_dependency("hdf5", "mpi", "link") :- node("hdf5"), variant_value("hdf5", "mpi", "True").
node("mpi") :- depends_on("hdf5", "mpi"), node("hdf5"), variant_value("hdf5", "mpi", "True").

declared_dependency("hdf5", "szip", "build") :- node("hdf5"), variant_value("hdf5", "szip", "True").
declared_dependency("hdf5", "szip", "link") :- node("hdf5"), variant_value("hdf5", "szip", "True").
node("szip") :- depends_on("hdf5", "szip"), node("hdf5"), variant_value("hdf5", "szip", "True").

declared_dependency("hdf5", "zlib", "build").
declared_dependency("hdf5", "zlib", "link").
node("zlib") :- depends_on("hdf5", "zlib"), node("hdf5").


%----------------------------------------------------------------------------
% Package: help2man
%----------------------------------------------------------------------------
version_declared("help2man", "1.47.11", 0).
version_declared("help2man", "1.47.8", 1).
version_declared("help2man", "1.47.4", 2).

declared_dependency("help2man", "gettext", "build").
node("gettext") :- depends_on("help2man", "gettext"), node("help2man").

declared_dependency("help2man", "perl", "build").
declared_dependency("help2man", "perl", "run").
node("perl") :- depends_on("help2man", "perl"), node("help2man").


%----------------------------------------------------------------------------
% Package: hwloc
%----------------------------------------------------------------------------
version_declared("hwloc", "2.1.0", 0).
version_declared("hwloc", "2.0.2", 1).
version_declared("hwloc", "2.0.1", 2).
version_declared("hwloc", "2.0.0", 3).
version_declared("hwloc", "1.11.11", 4).
version_declared("hwloc", "1.11.10", 5).
version_declared("hwloc", "1.11.9", 6).
version_declared("hwloc", "1.11.8", 7).
version_declared("hwloc", "1.11.7", 8).
version_declared("hwloc", "1.11.6", 9).
version_declared("hwloc", "1.11.5", 10).
version_declared("hwloc", "1.11.4", 11).
version_declared("hwloc", "1.11.3", 12).
version_declared("hwloc", "1.11.2", 13).
version_declared("hwloc", "1.11.1", 14).
version_declared("hwloc", "1.9", 15).
version_declared("hwloc", "master", 16).

variant("hwloc", "cairo").
variant_single_value("hwloc", "cairo").
variant_default_value("hwloc", "cairo", "False").
variant_possible_value("hwloc", "cairo", "False").
variant_possible_value("hwloc", "cairo", "True").

variant("hwloc", "cuda").
variant_single_value("hwloc", "cuda").
variant_default_value("hwloc", "cuda", "False").
variant_possible_value("hwloc", "cuda", "False").
variant_possible_value("hwloc", "cuda", "True").

variant("hwloc", "gl").
variant_single_value("hwloc", "gl").
variant_default_value("hwloc", "gl", "False").
variant_possible_value("hwloc", "gl", "False").
variant_possible_value("hwloc", "gl", "True").

variant("hwloc", "libxml2").
variant_single_value("hwloc", "libxml2").
variant_default_value("hwloc", "libxml2", "True").
variant_possible_value("hwloc", "libxml2", "False").
variant_possible_value("hwloc", "libxml2", "True").

variant("hwloc", "nvml").
variant_single_value("hwloc", "nvml").
variant_default_value("hwloc", "nvml", "False").
variant_possible_value("hwloc", "nvml", "False").
variant_possible_value("hwloc", "nvml", "True").

variant("hwloc", "pci").
variant_single_value("hwloc", "pci").
variant_default_value("hwloc", "pci", "False").
variant_possible_value("hwloc", "pci", "False").
variant_possible_value("hwloc", "pci", "True").

variant("hwloc", "shared").
variant_single_value("hwloc", "shared").
variant_default_value("hwloc", "shared", "True").
variant_possible_value("hwloc", "shared", "False").
variant_possible_value("hwloc", "shared", "True").

declared_dependency("hwloc", "autoconf", "build") :- node("hwloc"), 1 { version("hwloc", "master") } 1.
node("autoconf") :- depends_on("hwloc", "autoconf"), node("hwloc"), 1 { version("hwloc", "master") } 1.

declared_dependency("hwloc", "automake", "build") :- node("hwloc"), 1 { version("hwloc", "master") } 1.
node("automake") :- depends_on("hwloc", "automake"), node("hwloc"), 1 { version("hwloc", "master") } 1.

declared_dependency("hwloc", "cairo", "build") :- node("hwloc"), variant_value("hwloc", "cairo", "True").
declared_dependency("hwloc", "cairo", "link") :- node("hwloc"), variant_value("hwloc", "cairo", "True").
node("cairo") :- depends_on("hwloc", "cairo"), node("hwloc"), variant_value("hwloc", "cairo", "True").

declared_dependency("hwloc", "cuda", "build") :- node("hwloc"), variant_value("hwloc", "cuda", "True").
declared_dependency("hwloc", "cuda", "link") :- node("hwloc"), variant_value("hwloc", "cuda", "True").
node("cuda") :- depends_on("hwloc", "cuda"), node("hwloc"), variant_value("hwloc", "cuda", "True").
declared_dependency("hwloc", "cuda", "build") :- node("hwloc"), variant_value("hwloc", "nvml", "True").
declared_dependency("hwloc", "cuda", "link") :- node("hwloc"), variant_value("hwloc", "nvml", "True").
node("cuda") :- depends_on("hwloc", "cuda"), node("hwloc"), variant_value("hwloc", "nvml", "True").

declared_dependency("hwloc", "gl", "build") :- node("hwloc"), variant_value("hwloc", "gl", "True").
declared_dependency("hwloc", "gl", "link") :- node("hwloc"), variant_value("hwloc", "gl", "True").
node("gl") :- depends_on("hwloc", "gl"), node("hwloc"), variant_value("hwloc", "gl", "True").

declared_dependency("hwloc", "libpciaccess", "build") :- node("hwloc"), variant_value("hwloc", "pci", "True").
declared_dependency("hwloc", "libpciaccess", "link") :- node("hwloc"), variant_value("hwloc", "pci", "True").
node("libpciaccess") :- depends_on("hwloc", "libpciaccess"), node("hwloc"), variant_value("hwloc", "pci", "True").

declared_dependency("hwloc", "libtool", "build") :- node("hwloc"), 1 { version("hwloc", "master") } 1.
node("libtool") :- depends_on("hwloc", "libtool"), node("hwloc"), 1 { version("hwloc", "master") } 1.

declared_dependency("hwloc", "libxml2", "build") :- node("hwloc"), variant_value("hwloc", "libxml2", "True").
declared_dependency("hwloc", "libxml2", "link") :- node("hwloc"), variant_value("hwloc", "libxml2", "True").
node("libxml2") :- depends_on("hwloc", "libxml2"), node("hwloc"), variant_value("hwloc", "libxml2", "True").

declared_dependency("hwloc", "m4", "build") :- node("hwloc"), 1 { version("hwloc", "master") } 1.
node("m4") :- depends_on("hwloc", "m4"), node("hwloc"), 1 { version("hwloc", "master") } 1.

declared_dependency("hwloc", "numactl", "build") :- node("hwloc"), 1 { version("hwloc", "1.9"); version("hwloc", "1.11.1"); version("hwloc", "1.11.2"); version("hwloc", "1.11.3"); version("hwloc", "1.11.4"); version("hwloc", "1.11.5"); version("hwloc", "1.11.6"); version("hwloc", "1.11.7"); version("hwloc", "1.11.8"); version("hwloc", "1.11.9"); version("hwloc", "1.11.10"); version("hwloc", "1.11.11") } 1, node_platform("hwloc", "linux").
declared_dependency("hwloc", "numactl", "link") :- node("hwloc"), 1 { version("hwloc", "1.9"); version("hwloc", "1.11.1"); version("hwloc", "1.11.2"); version("hwloc", "1.11.3"); version("hwloc", "1.11.4"); version("hwloc", "1.11.5"); version("hwloc", "1.11.6"); version("hwloc", "1.11.7"); version("hwloc", "1.11.8"); version("hwloc", "1.11.9"); version("hwloc", "1.11.10"); version("hwloc", "1.11.11") } 1, node_platform("hwloc", "linux").
node("numactl") :- depends_on("hwloc", "numactl"), node("hwloc"), 1 { version("hwloc", "1.9"); version("hwloc", "1.11.1"); version("hwloc", "1.11.2"); version("hwloc", "1.11.3"); version("hwloc", "1.11.4"); version("hwloc", "1.11.5"); version("hwloc", "1.11.6"); version("hwloc", "1.11.7"); version("hwloc", "1.11.8"); version("hwloc", "1.11.9"); version("hwloc", "1.11.10"); version("hwloc", "1.11.11") } 1, node_platform("hwloc", "linux").

declared_dependency("hwloc", "pkgconfig", "build").
node("pkgconfig") :- depends_on("hwloc", "pkgconfig"), node("hwloc").


%----------------------------------------------------------------------------
% Package: ibm-java
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: icedtea
%----------------------------------------------------------------------------
version_declared("icedtea", "3.9.0", 0).
version_declared("icedtea", "3.8.0", 1).
version_declared("icedtea", "3.7.0", 2).
version_declared("icedtea", "3.6.0", 3).
version_declared("icedtea", "3.5.1", 4).
version_declared("icedtea", "3.5.0", 5).
version_declared("icedtea", "3.4.0", 6).

variant("icedtea", "X").
variant_single_value("icedtea", "X").
variant_default_value("icedtea", "X", "False").
variant_possible_value("icedtea", "X", "False").
variant_possible_value("icedtea", "X", "True").

variant("icedtea", "shenandoah").
variant_single_value("icedtea", "shenandoah").
variant_default_value("icedtea", "shenandoah", "False").
variant_possible_value("icedtea", "shenandoah", "False").
variant_possible_value("icedtea", "shenandoah", "True").

declared_dependency("icedtea", "alsa-lib", "build").
declared_dependency("icedtea", "alsa-lib", "link").
node("alsa-lib") :- depends_on("icedtea", "alsa-lib"), node("icedtea").

declared_dependency("icedtea", "cups", "build").
declared_dependency("icedtea", "cups", "link").
node("cups") :- depends_on("icedtea", "cups"), node("icedtea").

declared_dependency("icedtea", "freetype", "build").
declared_dependency("icedtea", "freetype", "link").
node("freetype") :- depends_on("icedtea", "freetype"), node("icedtea").

declared_dependency("icedtea", "giflib", "build").
declared_dependency("icedtea", "giflib", "link").
node("giflib") :- depends_on("icedtea", "giflib"), node("icedtea").

declared_dependency("icedtea", "gmake", "build").
node("gmake") :- depends_on("icedtea", "gmake"), node("icedtea").

declared_dependency("icedtea", "gtkplus", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("gtkplus") :- depends_on("icedtea", "gtkplus"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "gtkplus", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "gtkplus", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("gtkplus") :- depends_on("icedtea", "gtkplus"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "jdk", "build").
node("jdk") :- depends_on("icedtea", "jdk"), node("icedtea").

declared_dependency("icedtea", "jpeg", "build").
declared_dependency("icedtea", "jpeg", "link").
node("jpeg") :- depends_on("icedtea", "jpeg"), node("icedtea").

declared_dependency("icedtea", "lcms", "build").
declared_dependency("icedtea", "lcms", "link").
node("lcms") :- depends_on("icedtea", "lcms"), node("icedtea").

declared_dependency("icedtea", "libpng", "build").
declared_dependency("icedtea", "libpng", "link").
node("libpng") :- depends_on("icedtea", "libpng"), node("icedtea").

declared_dependency("icedtea", "libx11", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libx11") :- depends_on("icedtea", "libx11"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libx11", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libx11", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libx11") :- depends_on("icedtea", "libx11"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxau", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxau") :- depends_on("icedtea", "libxau"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxau", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxau", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxau") :- depends_on("icedtea", "libxau"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxcomposite", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxcomposite") :- depends_on("icedtea", "libxcomposite"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxcomposite", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxcomposite", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxcomposite") :- depends_on("icedtea", "libxcomposite"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxdmcp", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxdmcp") :- depends_on("icedtea", "libxdmcp"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxdmcp", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxdmcp", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxdmcp") :- depends_on("icedtea", "libxdmcp"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxext", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxext") :- depends_on("icedtea", "libxext"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxext", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxext", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxext") :- depends_on("icedtea", "libxext"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxi", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxi") :- depends_on("icedtea", "libxi"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxi", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxi", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxi") :- depends_on("icedtea", "libxi"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxinerama", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxinerama") :- depends_on("icedtea", "libxinerama"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxinerama", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxinerama", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxinerama") :- depends_on("icedtea", "libxinerama"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxrender", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxrender") :- depends_on("icedtea", "libxrender"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxrender", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxrender", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxrender") :- depends_on("icedtea", "libxrender"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxt", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxt") :- depends_on("icedtea", "libxt"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxt", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxt", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxt") :- depends_on("icedtea", "libxt"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "libxtst", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("libxtst") :- depends_on("icedtea", "libxtst"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "libxtst", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "libxtst", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("libxtst") :- depends_on("icedtea", "libxtst"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "pkgconfig", "build").
node("pkgconfig") :- depends_on("icedtea", "pkgconfig"), node("icedtea").

declared_dependency("icedtea", "wget", "build").
node("wget") :- depends_on("icedtea", "wget"), node("icedtea").

declared_dependency("icedtea", "xproto", "build") :- node("icedtea"), variant_value("icedtea", "X", "False").
node("xproto") :- depends_on("icedtea", "xproto"), node("icedtea"), variant_value("icedtea", "X", "False").
declared_dependency("icedtea", "xproto", "build") :- node("icedtea"), variant_value("icedtea", "X", "True").
declared_dependency("icedtea", "xproto", "link") :- node("icedtea"), variant_value("icedtea", "X", "True").
node("xproto") :- depends_on("icedtea", "xproto"), node("icedtea"), variant_value("icedtea", "X", "True").

declared_dependency("icedtea", "zlib", "build").
declared_dependency("icedtea", "zlib", "link").
node("zlib") :- depends_on("icedtea", "zlib"), node("icedtea").


%----------------------------------------------------------------------------
% Package: icu4c
%----------------------------------------------------------------------------
version_declared("icu4c", "65.1", 0).
version_declared("icu4c", "64.1", 1).
version_declared("icu4c", "60.1", 2).
version_declared("icu4c", "58.2", 3).
version_declared("icu4c", "57.1", 4).

variant("icu4c", "cxxstd").
variant_single_value("icu4c", "cxxstd").
variant_default_value("icu4c", "cxxstd", "11").
variant_possible_value("icu4c", "cxxstd", "11").
variant_possible_value("icu4c", "cxxstd", "14").
variant_possible_value("icu4c", "cxxstd", "17").

declared_dependency("icu4c", "python", "build") :- node("icu4c"), 1 { version("icu4c", "64.1"); version("icu4c", "65.1") } 1.
node("python") :- depends_on("icu4c", "python"), node("icu4c"), 1 { version("icu4c", "64.1"); version("icu4c", "65.1") } 1.


%----------------------------------------------------------------------------
% Package: inputproto
%----------------------------------------------------------------------------
version_declared("inputproto", "2.3.2", 0).

declared_dependency("inputproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("inputproto", "pkgconfig"), node("inputproto").

declared_dependency("inputproto", "util-macros", "build").
node("util-macros") :- depends_on("inputproto", "util-macros"), node("inputproto").


%----------------------------------------------------------------------------
% Package: intel-mkl
%----------------------------------------------------------------------------
version_declared("intel-mkl", "2020.0.166", 0).
version_declared("intel-mkl", "2019.5.281", 1).
version_declared("intel-mkl", "2019.4.243", 2).
version_declared("intel-mkl", "2019.3.199", 3).
version_declared("intel-mkl", "2019.2.187", 4).
version_declared("intel-mkl", "2019.1.144", 5).
version_declared("intel-mkl", "2019.0.117", 6).
version_declared("intel-mkl", "2018.4.274", 7).
version_declared("intel-mkl", "2018.3.222", 8).
version_declared("intel-mkl", "2018.2.199", 9).
version_declared("intel-mkl", "2018.1.163", 10).
version_declared("intel-mkl", "2018.0.128", 11).
version_declared("intel-mkl", "2017.4.239", 12).
version_declared("intel-mkl", "2017.3.196", 13).
version_declared("intel-mkl", "2017.2.174", 14).
version_declared("intel-mkl", "2017.1.132", 15).
version_declared("intel-mkl", "2017.0.098", 16).
version_declared("intel-mkl", "11.3.3.210", 17).
version_declared("intel-mkl", "11.3.2.181", 18).

variant("intel-mkl", "ilp64").
variant_single_value("intel-mkl", "ilp64").
variant_default_value("intel-mkl", "ilp64", "False").
variant_possible_value("intel-mkl", "ilp64", "False").
variant_possible_value("intel-mkl", "ilp64", "True").

variant("intel-mkl", "shared").
variant_single_value("intel-mkl", "shared").
variant_default_value("intel-mkl", "shared", "True").
variant_possible_value("intel-mkl", "shared", "False").
variant_possible_value("intel-mkl", "shared", "True").

variant("intel-mkl", "threads").
variant_single_value("intel-mkl", "threads").
variant_default_value("intel-mkl", "threads", "none").
variant_possible_value("intel-mkl", "threads", "none").
variant_possible_value("intel-mkl", "threads", "openmp").
variant_possible_value("intel-mkl", "threads", "tbb").

declared_dependency("intel-mkl", "cpio", "build").
node("cpio") :- depends_on("intel-mkl", "cpio"), node("intel-mkl").


%----------------------------------------------------------------------------
% Package: intel-mpi
%----------------------------------------------------------------------------
version_declared("intel-mpi", "2019.6.166", 0).
version_declared("intel-mpi", "2019.5.281", 1).
version_declared("intel-mpi", "2019.4.243", 2).
version_declared("intel-mpi", "2019.3.199", 3).
version_declared("intel-mpi", "2019.2.187", 4).
version_declared("intel-mpi", "2019.1.144", 5).
version_declared("intel-mpi", "2019.0.117", 6).
version_declared("intel-mpi", "2018.4.274", 7).
version_declared("intel-mpi", "2018.3.222", 8).
version_declared("intel-mpi", "2018.2.199", 9).
version_declared("intel-mpi", "2018.1.163", 10).
version_declared("intel-mpi", "2018.0.128", 11).
version_declared("intel-mpi", "2017.4.239", 12).
version_declared("intel-mpi", "2017.3.196", 13).
version_declared("intel-mpi", "2017.2.174", 14).
version_declared("intel-mpi", "2017.1.132", 15).
version_declared("intel-mpi", "5.1.3.223", 16).


%----------------------------------------------------------------------------
% Package: intel-parallel-studio
%----------------------------------------------------------------------------
version_declared("intel-parallel-studio", "professional.2020.0", 0).
version_declared("intel-parallel-studio", "professional.2019.5", 1).
version_declared("intel-parallel-studio", "professional.2019.4", 2).
version_declared("intel-parallel-studio", "professional.2019.3", 3).
version_declared("intel-parallel-studio", "professional.2019.2", 4).
version_declared("intel-parallel-studio", "professional.2019.1", 5).
version_declared("intel-parallel-studio", "professional.2019.0", 6).
version_declared("intel-parallel-studio", "professional.2018.4", 7).
version_declared("intel-parallel-studio", "professional.2018.3", 8).
version_declared("intel-parallel-studio", "professional.2018.2", 9).
version_declared("intel-parallel-studio", "professional.2018.1", 10).
version_declared("intel-parallel-studio", "professional.2018.0", 11).
version_declared("intel-parallel-studio", "professional.2017.7", 12).
version_declared("intel-parallel-studio", "professional.2017.6", 13).
version_declared("intel-parallel-studio", "professional.2017.5", 14).
version_declared("intel-parallel-studio", "professional.2017.4", 15).
version_declared("intel-parallel-studio", "professional.2017.3", 16).
version_declared("intel-parallel-studio", "professional.2017.2", 17).
version_declared("intel-parallel-studio", "professional.2017.1", 18).
version_declared("intel-parallel-studio", "professional.2017.0", 19).
version_declared("intel-parallel-studio", "professional.2016.4", 20).
version_declared("intel-parallel-studio", "professional.2016.3", 21).
version_declared("intel-parallel-studio", "professional.2016.2", 22).
version_declared("intel-parallel-studio", "professional.2016.1", 23).
version_declared("intel-parallel-studio", "professional.2016.0", 24).
version_declared("intel-parallel-studio", "professional.2015.6", 25).
version_declared("intel-parallel-studio", "professional.2015.1", 26).
version_declared("intel-parallel-studio", "composer.2020.0", 27).
version_declared("intel-parallel-studio", "composer.2019.5", 28).
version_declared("intel-parallel-studio", "composer.2019.4", 29).
version_declared("intel-parallel-studio", "composer.2019.3", 30).
version_declared("intel-parallel-studio", "composer.2019.2", 31).
version_declared("intel-parallel-studio", "composer.2019.1", 32).
version_declared("intel-parallel-studio", "composer.2019.0", 33).
version_declared("intel-parallel-studio", "composer.2018.4", 34).
version_declared("intel-parallel-studio", "composer.2018.3", 35).
version_declared("intel-parallel-studio", "composer.2018.2", 36).
version_declared("intel-parallel-studio", "composer.2018.1", 37).
version_declared("intel-parallel-studio", "composer.2018.0", 38).
version_declared("intel-parallel-studio", "composer.2017.7", 39).
version_declared("intel-parallel-studio", "composer.2017.6", 40).
version_declared("intel-parallel-studio", "composer.2017.5", 41).
version_declared("intel-parallel-studio", "composer.2017.4", 42).
version_declared("intel-parallel-studio", "composer.2017.3", 43).
version_declared("intel-parallel-studio", "composer.2017.2", 44).
version_declared("intel-parallel-studio", "composer.2017.1", 45).
version_declared("intel-parallel-studio", "composer.2017.0", 46).
version_declared("intel-parallel-studio", "composer.2016.4", 47).
version_declared("intel-parallel-studio", "composer.2016.3", 48).
version_declared("intel-parallel-studio", "composer.2016.2", 49).
version_declared("intel-parallel-studio", "composer.2015.6", 50).
version_declared("intel-parallel-studio", "composer.2015.1", 51).
version_declared("intel-parallel-studio", "cluster.2020.0", 52).
version_declared("intel-parallel-studio", "cluster.2019.5", 53).
version_declared("intel-parallel-studio", "cluster.2019.4", 54).
version_declared("intel-parallel-studio", "cluster.2019.3", 55).
version_declared("intel-parallel-studio", "cluster.2019.2", 56).
version_declared("intel-parallel-studio", "cluster.2019.1", 57).
version_declared("intel-parallel-studio", "cluster.2019.0", 58).
version_declared("intel-parallel-studio", "cluster.2018.4", 59).
version_declared("intel-parallel-studio", "cluster.2018.3", 60).
version_declared("intel-parallel-studio", "cluster.2018.2", 61).
version_declared("intel-parallel-studio", "cluster.2018.1", 62).
version_declared("intel-parallel-studio", "cluster.2018.0", 63).
version_declared("intel-parallel-studio", "cluster.2017.7", 64).
version_declared("intel-parallel-studio", "cluster.2017.6", 65).
version_declared("intel-parallel-studio", "cluster.2017.5", 66).
version_declared("intel-parallel-studio", "cluster.2017.4", 67).
version_declared("intel-parallel-studio", "cluster.2017.3", 68).
version_declared("intel-parallel-studio", "cluster.2017.2", 69).
version_declared("intel-parallel-studio", "cluster.2017.1", 70).
version_declared("intel-parallel-studio", "cluster.2017.0", 71).
version_declared("intel-parallel-studio", "cluster.2016.4", 72).
version_declared("intel-parallel-studio", "cluster.2016.3", 73).
version_declared("intel-parallel-studio", "cluster.2016.2", 74).
version_declared("intel-parallel-studio", "cluster.2016.1", 75).
version_declared("intel-parallel-studio", "cluster.2016.0", 76).
version_declared("intel-parallel-studio", "cluster.2015.6", 77).
version_declared("intel-parallel-studio", "cluster.2015.1", 78).

variant("intel-parallel-studio", "advisor").
variant_single_value("intel-parallel-studio", "advisor").
variant_default_value("intel-parallel-studio", "advisor", "False").
variant_possible_value("intel-parallel-studio", "advisor", "False").
variant_possible_value("intel-parallel-studio", "advisor", "True").

variant("intel-parallel-studio", "auto_dispatch").
not variant_single_value("intel-parallel-studio", "auto_dispatch").
variant_default_value("intel-parallel-studio", "auto_dispatch", "none").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "AVX").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "COMMON-AVX512").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "CORE-AVX-I").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "CORE-AVX2").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "CORE-AVX512").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "MIC-AVX512").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "SSE2").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "SSE3").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "SSE4.1").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "SSE4.2").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "SSSE3").
variant_possible_value("intel-parallel-studio", "auto_dispatch", "none").

variant("intel-parallel-studio", "clck").
variant_single_value("intel-parallel-studio", "clck").
variant_default_value("intel-parallel-studio", "clck", "False").
variant_possible_value("intel-parallel-studio", "clck", "False").
variant_possible_value("intel-parallel-studio", "clck", "True").

variant("intel-parallel-studio", "daal").
variant_single_value("intel-parallel-studio", "daal").
variant_default_value("intel-parallel-studio", "daal", "True").
variant_possible_value("intel-parallel-studio", "daal", "False").
variant_possible_value("intel-parallel-studio", "daal", "True").

variant("intel-parallel-studio", "gdb").
variant_single_value("intel-parallel-studio", "gdb").
variant_default_value("intel-parallel-studio", "gdb", "False").
variant_possible_value("intel-parallel-studio", "gdb", "False").
variant_possible_value("intel-parallel-studio", "gdb", "True").

variant("intel-parallel-studio", "ilp64").
variant_single_value("intel-parallel-studio", "ilp64").
variant_default_value("intel-parallel-studio", "ilp64", "False").
variant_possible_value("intel-parallel-studio", "ilp64", "False").
variant_possible_value("intel-parallel-studio", "ilp64", "True").

variant("intel-parallel-studio", "inspector").
variant_single_value("intel-parallel-studio", "inspector").
variant_default_value("intel-parallel-studio", "inspector", "False").
variant_possible_value("intel-parallel-studio", "inspector", "False").
variant_possible_value("intel-parallel-studio", "inspector", "True").

variant("intel-parallel-studio", "ipp").
variant_single_value("intel-parallel-studio", "ipp").
variant_default_value("intel-parallel-studio", "ipp", "True").
variant_possible_value("intel-parallel-studio", "ipp", "False").
variant_possible_value("intel-parallel-studio", "ipp", "True").

variant("intel-parallel-studio", "itac").
variant_single_value("intel-parallel-studio", "itac").
variant_default_value("intel-parallel-studio", "itac", "False").
variant_possible_value("intel-parallel-studio", "itac", "False").
variant_possible_value("intel-parallel-studio", "itac", "True").

variant("intel-parallel-studio", "mkl").
variant_single_value("intel-parallel-studio", "mkl").
variant_default_value("intel-parallel-studio", "mkl", "True").
variant_possible_value("intel-parallel-studio", "mkl", "False").
variant_possible_value("intel-parallel-studio", "mkl", "True").

variant("intel-parallel-studio", "mpi").
variant_single_value("intel-parallel-studio", "mpi").
variant_default_value("intel-parallel-studio", "mpi", "True").
variant_possible_value("intel-parallel-studio", "mpi", "False").
variant_possible_value("intel-parallel-studio", "mpi", "True").

variant("intel-parallel-studio", "newdtags").
variant_single_value("intel-parallel-studio", "newdtags").
variant_default_value("intel-parallel-studio", "newdtags", "False").
variant_possible_value("intel-parallel-studio", "newdtags", "False").
variant_possible_value("intel-parallel-studio", "newdtags", "True").

variant("intel-parallel-studio", "rpath").
variant_single_value("intel-parallel-studio", "rpath").
variant_default_value("intel-parallel-studio", "rpath", "True").
variant_possible_value("intel-parallel-studio", "rpath", "False").
variant_possible_value("intel-parallel-studio", "rpath", "True").

variant("intel-parallel-studio", "shared").
variant_single_value("intel-parallel-studio", "shared").
variant_default_value("intel-parallel-studio", "shared", "True").
variant_possible_value("intel-parallel-studio", "shared", "False").
variant_possible_value("intel-parallel-studio", "shared", "True").

variant("intel-parallel-studio", "tbb").
variant_single_value("intel-parallel-studio", "tbb").
variant_default_value("intel-parallel-studio", "tbb", "True").
variant_possible_value("intel-parallel-studio", "tbb", "False").
variant_possible_value("intel-parallel-studio", "tbb", "True").

variant("intel-parallel-studio", "threads").
variant_single_value("intel-parallel-studio", "threads").
variant_default_value("intel-parallel-studio", "threads", "none").
variant_possible_value("intel-parallel-studio", "threads", "none").
variant_possible_value("intel-parallel-studio", "threads", "openmp").

variant("intel-parallel-studio", "vtune").
variant_single_value("intel-parallel-studio", "vtune").
variant_default_value("intel-parallel-studio", "vtune", "False").
variant_possible_value("intel-parallel-studio", "vtune", "False").
variant_possible_value("intel-parallel-studio", "vtune", "True").


%----------------------------------------------------------------------------
% Package: intltool
%----------------------------------------------------------------------------
version_declared("intltool", "0.51.0", 0).

declared_dependency("intltool", "perl", "build").
declared_dependency("intltool", "perl", "run").
node("perl") :- depends_on("intltool", "perl"), node("intltool").

declared_dependency("intltool", "perl-xml-parser", "build").
declared_dependency("intltool", "perl-xml-parser", "run").
node("perl-xml-parser") :- depends_on("intltool", "perl-xml-parser"), node("intltool").


%----------------------------------------------------------------------------
% Package: isl
%----------------------------------------------------------------------------
version_declared("isl", "0.21", 0).
version_declared("isl", "0.20", 1).
version_declared("isl", "0.19", 2).
version_declared("isl", "0.18", 3).
version_declared("isl", "0.15", 4).
version_declared("isl", "0.14", 5).

declared_dependency("isl", "gmp", "build").
declared_dependency("isl", "gmp", "link").
node("gmp") :- depends_on("isl", "gmp"), node("isl").


%----------------------------------------------------------------------------
% Package: jdk
%----------------------------------------------------------------------------
version_declared("jdk", "12.0.2_10", 0).
version_declared("jdk", "12.0.1_12", 1).
version_declared("jdk", "11.0.2_9", 2).
version_declared("jdk", "11.0.1_13", 3).
version_declared("jdk", "10.0.2_13", 4).
version_declared("jdk", "10.0.1_10", 5).
version_declared("jdk", "1.8.0_241-b07", 6).
version_declared("jdk", "1.8.0_231-b11", 7).
version_declared("jdk", "1.8.0_212-b10", 8).
version_declared("jdk", "1.8.0_202-b08", 9).
version_declared("jdk", "1.8.0_141-b15", 10).
version_declared("jdk", "1.8.0_131-b11", 11).


%----------------------------------------------------------------------------
% Package: jemalloc
%----------------------------------------------------------------------------
version_declared("jemalloc", "5.2.1", 0).
version_declared("jemalloc", "4.5.0", 1).
version_declared("jemalloc", "4.4.0", 2).
version_declared("jemalloc", "4.3.1", 3).
version_declared("jemalloc", "4.2.1", 4).
version_declared("jemalloc", "4.2.0", 5).
version_declared("jemalloc", "4.1.0", 6).
version_declared("jemalloc", "4.0.4", 7).

variant("jemalloc", "je").
variant_single_value("jemalloc", "je").
variant_default_value("jemalloc", "je", "False").
variant_possible_value("jemalloc", "je", "False").
variant_possible_value("jemalloc", "je", "True").

variant("jemalloc", "prof").
variant_single_value("jemalloc", "prof").
variant_default_value("jemalloc", "prof", "False").
variant_possible_value("jemalloc", "prof", "False").
variant_possible_value("jemalloc", "prof", "True").

variant("jemalloc", "stats").
variant_single_value("jemalloc", "stats").
variant_default_value("jemalloc", "stats", "False").
variant_possible_value("jemalloc", "stats", "False").
variant_possible_value("jemalloc", "stats", "True").


%----------------------------------------------------------------------------
% Package: json-c
%----------------------------------------------------------------------------
version_declared("json-c", "0.13.1", 0).
version_declared("json-c", "0.12.1", 1).
version_declared("json-c", "0.11", 2).

declared_dependency("json-c", "autoconf", "build").
node("autoconf") :- depends_on("json-c", "autoconf"), node("json-c").


%----------------------------------------------------------------------------
% Package: kbproto
%----------------------------------------------------------------------------
version_declared("kbproto", "1.0.7", 0).

declared_dependency("kbproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("kbproto", "pkgconfig"), node("kbproto").

declared_dependency("kbproto", "util-macros", "build").
node("util-macros") :- depends_on("kbproto", "util-macros"), node("kbproto").


%----------------------------------------------------------------------------
% Package: krb5
%----------------------------------------------------------------------------
version_declared("krb5", "1.16.1", 0).

declared_dependency("krb5", "bison", "build").
node("bison") :- depends_on("krb5", "bison"), node("krb5").

declared_dependency("krb5", "openssl", "build").
declared_dependency("krb5", "openssl", "link").
node("openssl") :- depends_on("krb5", "openssl"), node("krb5").


%----------------------------------------------------------------------------
% Package: lcms
%----------------------------------------------------------------------------
version_declared("lcms", "2.9", 0).
version_declared("lcms", "2.8", 1).
version_declared("lcms", "2.6", 2).

declared_dependency("lcms", "jpeg", "build").
declared_dependency("lcms", "jpeg", "link").
node("jpeg") :- depends_on("lcms", "jpeg"), node("lcms").

declared_dependency("lcms", "libtiff", "build").
declared_dependency("lcms", "libtiff", "link").
node("libtiff") :- depends_on("lcms", "libtiff"), node("lcms").

declared_dependency("lcms", "zlib", "build").
declared_dependency("lcms", "zlib", "link").
node("zlib") :- depends_on("lcms", "zlib"), node("lcms").


%----------------------------------------------------------------------------
% Package: libaec
%----------------------------------------------------------------------------
version_declared("libaec", "1.0.2", 0).
version_declared("libaec", "1.0.1", 1).
version_declared("libaec", "1.0.0", 2).

variant("libaec", "build_type").
variant_single_value("libaec", "build_type").
variant_default_value("libaec", "build_type", "RelWithDebInfo").
variant_possible_value("libaec", "build_type", "Debug").
variant_possible_value("libaec", "build_type", "MinSizeRel").
variant_possible_value("libaec", "build_type", "RelWithDebInfo").
variant_possible_value("libaec", "build_type", "Release").

declared_dependency("libaec", "cmake", "build").
node("cmake") :- depends_on("libaec", "cmake"), node("libaec").


%----------------------------------------------------------------------------
% Package: libaio
%----------------------------------------------------------------------------
version_declared("libaio", "0.3.110", 0).


%----------------------------------------------------------------------------
% Package: libarchive
%----------------------------------------------------------------------------
version_declared("libarchive", "3.4.1", 0).
version_declared("libarchive", "3.3.2", 1).
version_declared("libarchive", "3.2.1", 2).
version_declared("libarchive", "3.1.2", 3).
version_declared("libarchive", "3.1.1", 4).
version_declared("libarchive", "3.1.0", 5).

declared_dependency("libarchive", "bzip2", "build").
declared_dependency("libarchive", "bzip2", "link").
node("bzip2") :- depends_on("libarchive", "bzip2"), node("libarchive").

declared_dependency("libarchive", "expat", "build").
declared_dependency("libarchive", "expat", "link").
node("expat") :- depends_on("libarchive", "expat"), node("libarchive").

declared_dependency("libarchive", "libxml2", "build").
declared_dependency("libarchive", "libxml2", "link").
node("libxml2") :- depends_on("libarchive", "libxml2"), node("libarchive").

declared_dependency("libarchive", "lz4", "build").
declared_dependency("libarchive", "lz4", "link").
node("lz4") :- depends_on("libarchive", "lz4"), node("libarchive").

declared_dependency("libarchive", "lzo", "build").
declared_dependency("libarchive", "lzo", "link").
node("lzo") :- depends_on("libarchive", "lzo"), node("libarchive").

declared_dependency("libarchive", "nettle", "build").
declared_dependency("libarchive", "nettle", "link").
node("nettle") :- depends_on("libarchive", "nettle"), node("libarchive").

declared_dependency("libarchive", "openssl", "build").
declared_dependency("libarchive", "openssl", "link").
node("openssl") :- depends_on("libarchive", "openssl"), node("libarchive").

declared_dependency("libarchive", "xz", "build").
declared_dependency("libarchive", "xz", "link").
node("xz") :- depends_on("libarchive", "xz"), node("libarchive").

declared_dependency("libarchive", "zlib", "build").
declared_dependency("libarchive", "zlib", "link").
node("zlib") :- depends_on("libarchive", "zlib"), node("libarchive").


%----------------------------------------------------------------------------
% Package: libatomic-ops
%----------------------------------------------------------------------------
version_declared("libatomic-ops", "7.6.6", 0).
version_declared("libatomic-ops", "7.4.4", 1).


%----------------------------------------------------------------------------
% Package: libbsd
%----------------------------------------------------------------------------
version_declared("libbsd", "0.10.0", 0).
version_declared("libbsd", "0.9.1", 1).
version_declared("libbsd", "0.9.0", 2).
version_declared("libbsd", "0.8.7", 3).
version_declared("libbsd", "0.8.6", 4).


%----------------------------------------------------------------------------
% Package: libcroco
%----------------------------------------------------------------------------
version_declared("libcroco", "0.6.12", 0).

declared_dependency("libcroco", "glib", "build").
declared_dependency("libcroco", "glib", "link").
node("glib") :- depends_on("libcroco", "glib"), node("libcroco").

declared_dependency("libcroco", "libxml2", "build").
declared_dependency("libcroco", "libxml2", "link").
node("libxml2") :- depends_on("libcroco", "libxml2"), node("libcroco").


%----------------------------------------------------------------------------
% Package: libedit
%----------------------------------------------------------------------------
version_declared("libedit", "3.1-20191231", 0).
version_declared("libedit", "3.1-20170329", 1).
version_declared("libedit", "3.1-20160903", 2).
version_declared("libedit", "3.1-20150325", 3).

declared_dependency("libedit", "ncurses", "build").
declared_dependency("libedit", "ncurses", "link").
node("ncurses") :- depends_on("libedit", "ncurses"), node("libedit").


%----------------------------------------------------------------------------
% Package: libepoxy
%----------------------------------------------------------------------------
version_declared("libepoxy", "1.4.3", 0).

variant("libepoxy", "glx").
variant_single_value("libepoxy", "glx").
variant_default_value("libepoxy", "glx", "True").
variant_possible_value("libepoxy", "glx", "False").
variant_possible_value("libepoxy", "glx", "True").

declared_dependency("libepoxy", "gl", "build").
declared_dependency("libepoxy", "gl", "link").
node("gl") :- depends_on("libepoxy", "gl"), node("libepoxy").

declared_dependency("libepoxy", "libx11", "build") :- node("libepoxy"), variant_value("libepoxy", "glx", "True").
declared_dependency("libepoxy", "libx11", "link") :- node("libepoxy"), variant_value("libepoxy", "glx", "True").
node("libx11") :- depends_on("libepoxy", "libx11"), node("libepoxy"), variant_value("libepoxy", "glx", "True").

declared_dependency("libepoxy", "meson", "build").
declared_dependency("libepoxy", "meson", "link").
node("meson") :- depends_on("libepoxy", "meson"), node("libepoxy").

declared_dependency("libepoxy", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libepoxy", "pkgconfig"), node("libepoxy").


%----------------------------------------------------------------------------
% Package: libevent
%----------------------------------------------------------------------------
version_declared("libevent", "2.1.8", 0).
version_declared("libevent", "2.0.22", 1).
version_declared("libevent", "2.0.21", 2).
version_declared("libevent", "2.0.20", 3).
version_declared("libevent", "2.0.19", 4).
version_declared("libevent", "2.0.18", 5).
version_declared("libevent", "2.0.17", 6).
version_declared("libevent", "2.0.16", 7).
version_declared("libevent", "2.0.15", 8).
version_declared("libevent", "2.0.14", 9).
version_declared("libevent", "2.0.13", 10).
version_declared("libevent", "2.0.12", 11).

variant("libevent", "openssl").
variant_single_value("libevent", "openssl").
variant_default_value("libevent", "openssl", "True").
variant_possible_value("libevent", "openssl", "False").
variant_possible_value("libevent", "openssl", "True").

declared_dependency("libevent", "openssl", "build") :- node("libevent"), 1 { version("libevent", "2.0.12"); version("libevent", "2.0.13"); version("libevent", "2.0.14"); version("libevent", "2.0.15"); version("libevent", "2.0.16"); version("libevent", "2.0.17"); version("libevent", "2.0.18"); version("libevent", "2.0.19"); version("libevent", "2.0.20"); version("libevent", "2.0.21"); version("libevent", "2.0.22") } 1, variant_value("libevent", "openssl", "True").
declared_dependency("libevent", "openssl", "link") :- node("libevent"), 1 { version("libevent", "2.0.12"); version("libevent", "2.0.13"); version("libevent", "2.0.14"); version("libevent", "2.0.15"); version("libevent", "2.0.16"); version("libevent", "2.0.17"); version("libevent", "2.0.18"); version("libevent", "2.0.19"); version("libevent", "2.0.20"); version("libevent", "2.0.21"); version("libevent", "2.0.22") } 1, variant_value("libevent", "openssl", "True").
node("openssl") :- depends_on("libevent", "openssl"), node("libevent"), 1 { version("libevent", "2.0.12"); version("libevent", "2.0.13"); version("libevent", "2.0.14"); version("libevent", "2.0.15"); version("libevent", "2.0.16"); version("libevent", "2.0.17"); version("libevent", "2.0.18"); version("libevent", "2.0.19"); version("libevent", "2.0.20"); version("libevent", "2.0.21"); version("libevent", "2.0.22") } 1, variant_value("libevent", "openssl", "True").
1 { version("openssl", "1.0.1e"); version("openssl", "1.0.1h"); version("openssl", "1.0.1r"); version("openssl", "1.0.1t"); version("openssl", "1.0.1u"); version("openssl", "1.0.2d"); version("openssl", "1.0.2e"); version("openssl", "1.0.2f"); version("openssl", "1.0.2g"); version("openssl", "1.0.2h"); version("openssl", "1.0.2i"); version("openssl", "1.0.2j"); version("openssl", "1.0.2k"); version("openssl", "1.0.2m"); version("openssl", "1.0.2n"); version("openssl", "1.0.2o"); version("openssl", "1.0.2p"); version("openssl", "1.0.2r"); version("openssl", "1.0.2s"); version("openssl", "1.0.2t") } 1 :- depends_on("libevent", "openssl"), node("libevent"), 1 { version("libevent", "2.0.12"); version("libevent", "2.0.13"); version("libevent", "2.0.14"); version("libevent", "2.0.15"); version("libevent", "2.0.16"); version("libevent", "2.0.17"); version("libevent", "2.0.18"); version("libevent", "2.0.19"); version("libevent", "2.0.20"); version("libevent", "2.0.21"); version("libevent", "2.0.22") } 1, variant_value("libevent", "openssl", "True").
declared_dependency("libevent", "openssl", "build") :- node("libevent"), variant_value("libevent", "openssl", "True").
declared_dependency("libevent", "openssl", "link") :- node("libevent"), variant_value("libevent", "openssl", "True").
node("openssl") :- depends_on("libevent", "openssl"), node("libevent"), variant_value("libevent", "openssl", "True").


%----------------------------------------------------------------------------
% Package: libfabric
%----------------------------------------------------------------------------
version_declared("libfabric", "1.9.0", 0).
version_declared("libfabric", "1.8.1", 1).
version_declared("libfabric", "1.8.0", 2).
version_declared("libfabric", "1.7.1", 3).
version_declared("libfabric", "1.7.0", 4).
version_declared("libfabric", "1.6.2", 5).
version_declared("libfabric", "1.6.1", 6).
version_declared("libfabric", "1.6.0", 7).
version_declared("libfabric", "1.5.3", 8).
version_declared("libfabric", "1.5.0", 9).
version_declared("libfabric", "1.4.2", 10).
version_declared("libfabric", "develop", 11).

variant("libfabric", "fabrics").
not variant_single_value("libfabric", "fabrics").
variant_default_value("libfabric", "fabrics", "sockets").
variant_possible_value("libfabric", "fabrics", "efa").
variant_possible_value("libfabric", "fabrics", "gni").
variant_possible_value("libfabric", "fabrics", "mlx").
variant_possible_value("libfabric", "fabrics", "mrail").
variant_possible_value("libfabric", "fabrics", "psm").
variant_possible_value("libfabric", "fabrics", "psm2").
variant_possible_value("libfabric", "fabrics", "rxd").
variant_possible_value("libfabric", "fabrics", "rxm").
variant_possible_value("libfabric", "fabrics", "shm").
variant_possible_value("libfabric", "fabrics", "sockets").
variant_possible_value("libfabric", "fabrics", "tcp").
variant_possible_value("libfabric", "fabrics", "udp").
variant_possible_value("libfabric", "fabrics", "usnic").
variant_possible_value("libfabric", "fabrics", "verbs").
variant_possible_value("libfabric", "fabrics", "xpmem").

variant("libfabric", "kdreg").
variant_single_value("libfabric", "kdreg").
variant_default_value("libfabric", "kdreg", "False").
variant_possible_value("libfabric", "kdreg", "False").
variant_possible_value("libfabric", "kdreg", "True").

declared_dependency("libfabric", "autoconf", "build") :- node("libfabric"), 1 { version("libfabric", "develop") } 1.
node("autoconf") :- depends_on("libfabric", "autoconf"), node("libfabric"), 1 { version("libfabric", "develop") } 1.

declared_dependency("libfabric", "automake", "build") :- node("libfabric"), 1 { version("libfabric", "develop") } 1.
node("automake") :- depends_on("libfabric", "automake"), node("libfabric"), 1 { version("libfabric", "develop") } 1.

declared_dependency("libfabric", "libtool", "build") :- node("libfabric"), 1 { version("libfabric", "develop") } 1.
node("libtool") :- depends_on("libfabric", "libtool"), node("libfabric"), 1 { version("libfabric", "develop") } 1.

declared_dependency("libfabric", "m4", "build") :- node("libfabric"), 1 { version("libfabric", "develop") } 1.
node("m4") :- depends_on("libfabric", "m4"), node("libfabric"), 1 { version("libfabric", "develop") } 1.

declared_dependency("libfabric", "opa-psm2", "build") :- node("libfabric"), variant_value("libfabric", "fabrics", "psm2").
declared_dependency("libfabric", "opa-psm2", "link") :- node("libfabric"), variant_value("libfabric", "fabrics", "psm2").
node("opa-psm2") :- depends_on("libfabric", "opa-psm2"), node("libfabric"), variant_value("libfabric", "fabrics", "psm2").

declared_dependency("libfabric", "psm", "build") :- node("libfabric"), variant_value("libfabric", "fabrics", "psm").
declared_dependency("libfabric", "psm", "link") :- node("libfabric"), variant_value("libfabric", "fabrics", "psm").
node("psm") :- depends_on("libfabric", "psm"), node("libfabric"), variant_value("libfabric", "fabrics", "psm").

declared_dependency("libfabric", "rdma-core", "build") :- node("libfabric"), variant_value("libfabric", "fabrics", "verbs").
declared_dependency("libfabric", "rdma-core", "link") :- node("libfabric"), variant_value("libfabric", "fabrics", "verbs").
node("rdma-core") :- depends_on("libfabric", "rdma-core"), node("libfabric"), variant_value("libfabric", "fabrics", "verbs").

declared_dependency("libfabric", "ucx", "build") :- node("libfabric"), variant_value("libfabric", "fabrics", "mlx").
declared_dependency("libfabric", "ucx", "link") :- node("libfabric"), variant_value("libfabric", "fabrics", "mlx").
node("ucx") :- depends_on("libfabric", "ucx"), node("libfabric"), variant_value("libfabric", "fabrics", "mlx").


%----------------------------------------------------------------------------
% Package: libffi
%----------------------------------------------------------------------------
version_declared("libffi", "3.2.1", 0).


%----------------------------------------------------------------------------
% Package: libflame
%----------------------------------------------------------------------------
version_declared("libflame", "5.2.0", 0).
version_declared("libflame", "5.1.0", 1).
version_declared("libflame", "master", 2).

variant("libflame", "debug").
variant_single_value("libflame", "debug").
variant_default_value("libflame", "debug", "False").
variant_possible_value("libflame", "debug", "False").
variant_possible_value("libflame", "debug", "True").

variant("libflame", "lapack2flame").
variant_single_value("libflame", "lapack2flame").
variant_default_value("libflame", "lapack2flame", "True").
variant_possible_value("libflame", "lapack2flame", "False").
variant_possible_value("libflame", "lapack2flame", "True").

variant("libflame", "shared").
variant_single_value("libflame", "shared").
variant_default_value("libflame", "shared", "True").
variant_possible_value("libflame", "shared", "False").
variant_possible_value("libflame", "shared", "True").

variant("libflame", "static").
variant_single_value("libflame", "static").
variant_default_value("libflame", "static", "True").
variant_possible_value("libflame", "static", "False").
variant_possible_value("libflame", "static", "True").

variant("libflame", "threads").
variant_single_value("libflame", "threads").
variant_default_value("libflame", "threads", "no").
variant_possible_value("libflame", "threads", "no").
variant_possible_value("libflame", "threads", "openmp").
variant_possible_value("libflame", "threads", "pthreads").

declared_dependency("libflame", "blas", "build").
declared_dependency("libflame", "blas", "link").
node("blas") :- depends_on("libflame", "blas"), node("libflame").


%----------------------------------------------------------------------------
% Package: libfontenc
%----------------------------------------------------------------------------
version_declared("libfontenc", "1.1.3", 0).

declared_dependency("libfontenc", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libfontenc", "pkgconfig"), node("libfontenc").

declared_dependency("libfontenc", "util-macros", "build").
node("util-macros") :- depends_on("libfontenc", "util-macros"), node("libfontenc").

declared_dependency("libfontenc", "xproto", "build").
node("xproto") :- depends_on("libfontenc", "xproto"), node("libfontenc").

declared_dependency("libfontenc", "zlib", "build").
declared_dependency("libfontenc", "zlib", "link").
node("zlib") :- depends_on("libfontenc", "zlib"), node("libfontenc").


%----------------------------------------------------------------------------
% Package: libgcrypt
%----------------------------------------------------------------------------
version_declared("libgcrypt", "1.8.5", 0).
version_declared("libgcrypt", "1.8.4", 1).
version_declared("libgcrypt", "1.8.1", 2).
version_declared("libgcrypt", "1.7.6", 3).
version_declared("libgcrypt", "1.6.2", 4).

declared_dependency("libgcrypt", "libgpg-error", "build").
declared_dependency("libgcrypt", "libgpg-error", "link").
node("libgpg-error") :- depends_on("libgcrypt", "libgpg-error"), node("libgcrypt").
1 { version("libgpg-error", "1.27"); version("libgpg-error", "1.36") } 1 :- depends_on("libgcrypt", "libgpg-error"), node("libgcrypt").


%----------------------------------------------------------------------------
% Package: libgpg-error
%----------------------------------------------------------------------------
version_declared("libgpg-error", "1.36", 0).
version_declared("libgpg-error", "1.27", 1).
version_declared("libgpg-error", "1.21", 2).
version_declared("libgpg-error", "1.18", 3).

declared_dependency("libgpg-error", "awk", "build").
node("awk") :- depends_on("libgpg-error", "awk"), node("libgpg-error").


%----------------------------------------------------------------------------
% Package: libice
%----------------------------------------------------------------------------
version_declared("libice", "1.0.9", 0).

declared_dependency("libice", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libice", "pkgconfig"), node("libice").

declared_dependency("libice", "util-macros", "build").
node("util-macros") :- depends_on("libice", "util-macros"), node("libice").

declared_dependency("libice", "xproto", "build").
node("xproto") :- depends_on("libice", "xproto"), node("libice").

declared_dependency("libice", "xtrans", "build").
node("xtrans") :- depends_on("libice", "xtrans"), node("libice").


%----------------------------------------------------------------------------
% Package: libiconv
%----------------------------------------------------------------------------
version_declared("libiconv", "1.16", 0).
version_declared("libiconv", "1.15", 1).
version_declared("libiconv", "1.14", 2).


%----------------------------------------------------------------------------
% Package: libidn2
%----------------------------------------------------------------------------
version_declared("libidn2", "2.1.1a", 0).
version_declared("libidn2", "2.1.1", 1).
version_declared("libidn2", "2.1.0", 2).
version_declared("libidn2", "2.0.5", 3).

declared_dependency("libidn2", "libunistring", "build").
declared_dependency("libidn2", "libunistring", "link").
node("libunistring") :- depends_on("libidn2", "libunistring"), node("libidn2").


%----------------------------------------------------------------------------
% Package: libjpeg
%----------------------------------------------------------------------------
version_declared("libjpeg", "9c", 0).
version_declared("libjpeg", "9b", 1).
version_declared("libjpeg", "9a", 2).


%----------------------------------------------------------------------------
% Package: libjpeg-turbo
%----------------------------------------------------------------------------
version_declared("libjpeg-turbo", "2.0.3", 0).
version_declared("libjpeg-turbo", "2.0.2", 1).
version_declared("libjpeg-turbo", "1.5.90", 2).
version_declared("libjpeg-turbo", "1.5.3", 3).
version_declared("libjpeg-turbo", "1.5.0", 4).
version_declared("libjpeg-turbo", "1.3.1", 5).

declared_dependency("libjpeg-turbo", "autoconf", "build") :- node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.3.1"); version("libjpeg-turbo", "1.5.0"); version("libjpeg-turbo", "1.5.3") } 1.
node("autoconf") :- depends_on("libjpeg-turbo", "autoconf"), node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.3.1"); version("libjpeg-turbo", "1.5.0"); version("libjpeg-turbo", "1.5.3") } 1.

declared_dependency("libjpeg-turbo", "automake", "build") :- node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.3.1"); version("libjpeg-turbo", "1.5.0"); version("libjpeg-turbo", "1.5.3") } 1.
node("automake") :- depends_on("libjpeg-turbo", "automake"), node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.3.1"); version("libjpeg-turbo", "1.5.0"); version("libjpeg-turbo", "1.5.3") } 1.

declared_dependency("libjpeg-turbo", "cmake", "build") :- node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.5.90"); version("libjpeg-turbo", "2.0.2"); version("libjpeg-turbo", "2.0.3") } 1.
node("cmake") :- depends_on("libjpeg-turbo", "cmake"), node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.5.90"); version("libjpeg-turbo", "2.0.2"); version("libjpeg-turbo", "2.0.3") } 1.

declared_dependency("libjpeg-turbo", "libtool", "build") :- node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.3.1"); version("libjpeg-turbo", "1.5.0"); version("libjpeg-turbo", "1.5.3") } 1.
node("libtool") :- depends_on("libjpeg-turbo", "libtool"), node("libjpeg-turbo"), 1 { version("libjpeg-turbo", "1.3.1"); version("libjpeg-turbo", "1.5.0"); version("libjpeg-turbo", "1.5.3") } 1.

declared_dependency("libjpeg-turbo", "nasm", "build").
node("nasm") :- depends_on("libjpeg-turbo", "nasm"), node("libjpeg-turbo").


%----------------------------------------------------------------------------
% Package: libmng
%----------------------------------------------------------------------------
version_declared("libmng", "2.0.3", 0).
version_declared("libmng", "2.0.2", 1).

variant("libmng", "build_type").
variant_single_value("libmng", "build_type").
variant_default_value("libmng", "build_type", "RelWithDebInfo").
variant_possible_value("libmng", "build_type", "Debug").
variant_possible_value("libmng", "build_type", "MinSizeRel").
variant_possible_value("libmng", "build_type", "RelWithDebInfo").
variant_possible_value("libmng", "build_type", "Release").

declared_dependency("libmng", "cmake", "build").
node("cmake") :- depends_on("libmng", "cmake"), node("libmng").

declared_dependency("libmng", "gzip", "build").
declared_dependency("libmng", "gzip", "link").
node("gzip") :- depends_on("libmng", "gzip"), node("libmng").

declared_dependency("libmng", "jpeg", "build").
declared_dependency("libmng", "jpeg", "link").
node("jpeg") :- depends_on("libmng", "jpeg"), node("libmng").

declared_dependency("libmng", "lcms", "build").
declared_dependency("libmng", "lcms", "link").
node("lcms") :- depends_on("libmng", "lcms"), node("libmng").

declared_dependency("libmng", "zlib", "build").
declared_dependency("libmng", "zlib", "link").
node("zlib") :- depends_on("libmng", "zlib"), node("libmng").


%----------------------------------------------------------------------------
% Package: libnl
%----------------------------------------------------------------------------
version_declared("libnl", "3.3.0", 0).

declared_dependency("libnl", "bison", "build").
node("bison") :- depends_on("libnl", "bison"), node("libnl").

declared_dependency("libnl", "flex", "build").
node("flex") :- depends_on("libnl", "flex"), node("libnl").

declared_dependency("libnl", "m4", "build").
node("m4") :- depends_on("libnl", "m4"), node("libnl").


%----------------------------------------------------------------------------
% Package: libnsl
%----------------------------------------------------------------------------
version_declared("libnsl", "1.2.0", 0).

declared_dependency("libnsl", "autoconf", "build").
node("autoconf") :- depends_on("libnsl", "autoconf"), node("libnsl").

declared_dependency("libnsl", "automake", "build").
node("automake") :- depends_on("libnsl", "automake"), node("libnsl").

declared_dependency("libnsl", "gettext", "build").
declared_dependency("libnsl", "gettext", "link").
node("gettext") :- depends_on("libnsl", "gettext"), node("libnsl").

declared_dependency("libnsl", "libtirpc", "build").
declared_dependency("libnsl", "libtirpc", "link").
node("libtirpc") :- depends_on("libnsl", "libtirpc"), node("libnsl").

declared_dependency("libnsl", "libtool", "build").
node("libtool") :- depends_on("libnsl", "libtool"), node("libnsl").

declared_dependency("libnsl", "m4", "build").
node("m4") :- depends_on("libnsl", "m4"), node("libnsl").

declared_dependency("libnsl", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libnsl", "pkgconfig"), node("libnsl").

declared_dependency("libnsl", "rpcsvc-proto", "build").
declared_dependency("libnsl", "rpcsvc-proto", "link").
node("rpcsvc-proto") :- depends_on("libnsl", "rpcsvc-proto"), node("libnsl").


%----------------------------------------------------------------------------
% Package: libpciaccess
%----------------------------------------------------------------------------
version_declared("libpciaccess", "0.13.5", 0).
version_declared("libpciaccess", "0.13.4", 1).

declared_dependency("libpciaccess", "libtool", "build").
node("libtool") :- depends_on("libpciaccess", "libtool"), node("libpciaccess").

declared_dependency("libpciaccess", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libpciaccess", "pkgconfig"), node("libpciaccess").

declared_dependency("libpciaccess", "util-macros", "build").
node("util-macros") :- depends_on("libpciaccess", "util-macros"), node("libpciaccess").


%----------------------------------------------------------------------------
% Package: libpng
%----------------------------------------------------------------------------
version_declared("libpng", "1.6.37", 0).
version_declared("libpng", "1.2.57", 1).

declared_dependency("libpng", "zlib", "build").
declared_dependency("libpng", "zlib", "link").
node("zlib") :- depends_on("libpng", "zlib"), node("libpng").


%----------------------------------------------------------------------------
% Package: libpsl
%----------------------------------------------------------------------------
version_declared("libpsl", "0.17.0", 0).

declared_dependency("libpsl", "gettext", "build").
node("gettext") :- depends_on("libpsl", "gettext"), node("libpsl").

declared_dependency("libpsl", "icu4c", "build").
declared_dependency("libpsl", "icu4c", "link").
node("icu4c") :- depends_on("libpsl", "icu4c"), node("libpsl").

declared_dependency("libpsl", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libpsl", "pkgconfig"), node("libpsl").

declared_dependency("libpsl", "python", "build").
node("python") :- depends_on("libpsl", "python"), node("libpsl").

declared_dependency("libpsl", "valgrind", "test").
node("valgrind") :- depends_on("libpsl", "valgrind"), node("libpsl").
variant_set("valgrind", "boost", "False") :- depends_on("libpsl", "valgrind"), node("libpsl").
variant_set("valgrind", "mpi", "False") :- depends_on("libpsl", "valgrind"), node("libpsl").


%----------------------------------------------------------------------------
% Package: libpthread-stubs
%----------------------------------------------------------------------------
version_declared("libpthread-stubs", "0.4", 0).
version_declared("libpthread-stubs", "0.3", 1).


%----------------------------------------------------------------------------
% Package: librsvg
%----------------------------------------------------------------------------
version_declared("librsvg", "2.44.14", 0).

declared_dependency("librsvg", "cairo", "build").
declared_dependency("librsvg", "cairo", "link").
node("cairo") :- depends_on("librsvg", "cairo"), node("librsvg").

declared_dependency("librsvg", "gdk-pixbuf", "build").
declared_dependency("librsvg", "gdk-pixbuf", "link").
node("gdk-pixbuf") :- depends_on("librsvg", "gdk-pixbuf"), node("librsvg").

declared_dependency("librsvg", "glib", "build").
declared_dependency("librsvg", "glib", "link").
node("glib") :- depends_on("librsvg", "glib"), node("librsvg").

declared_dependency("librsvg", "gobject-introspection", "build").
node("gobject-introspection") :- depends_on("librsvg", "gobject-introspection"), node("librsvg").

declared_dependency("librsvg", "libcroco", "build").
declared_dependency("librsvg", "libcroco", "link").
node("libcroco") :- depends_on("librsvg", "libcroco"), node("librsvg").

declared_dependency("librsvg", "libffi", "build").
declared_dependency("librsvg", "libffi", "link").
node("libffi") :- depends_on("librsvg", "libffi"), node("librsvg").

declared_dependency("librsvg", "libxml2", "build").
declared_dependency("librsvg", "libxml2", "link").
node("libxml2") :- depends_on("librsvg", "libxml2"), node("librsvg").

declared_dependency("librsvg", "pango", "build").
declared_dependency("librsvg", "pango", "link").
node("pango") :- depends_on("librsvg", "pango"), node("librsvg").

declared_dependency("librsvg", "pkgconfig", "build").
node("pkgconfig") :- depends_on("librsvg", "pkgconfig"), node("librsvg").

declared_dependency("librsvg", "rust", "build").
node("rust") :- depends_on("librsvg", "rust"), node("librsvg").


%----------------------------------------------------------------------------
% Package: libsigsegv
%----------------------------------------------------------------------------
version_declared("libsigsegv", "2.12", 0).
version_declared("libsigsegv", "2.11", 1).
version_declared("libsigsegv", "2.10", 2).


%----------------------------------------------------------------------------
% Package: libsm
%----------------------------------------------------------------------------
version_declared("libsm", "1.2.2", 0).

declared_dependency("libsm", "libice", "build").
declared_dependency("libsm", "libice", "link").
node("libice") :- depends_on("libsm", "libice"), node("libsm").

declared_dependency("libsm", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libsm", "pkgconfig"), node("libsm").

declared_dependency("libsm", "util-macros", "build").
node("util-macros") :- depends_on("libsm", "util-macros"), node("libsm").

declared_dependency("libsm", "xproto", "build").
node("xproto") :- depends_on("libsm", "xproto"), node("libsm").

declared_dependency("libsm", "xtrans", "build").
node("xtrans") :- depends_on("libsm", "xtrans"), node("libsm").


%----------------------------------------------------------------------------
% Package: libsodium
%----------------------------------------------------------------------------
version_declared("libsodium", "1.0.17", 0).
version_declared("libsodium", "1.0.16", 1).
version_declared("libsodium", "1.0.15", 2).
version_declared("libsodium", "1.0.13", 3).
version_declared("libsodium", "1.0.3", 4).
version_declared("libsodium", "1.0.2", 5).
version_declared("libsodium", "1.0.1", 6).
version_declared("libsodium", "1.0.0", 7).
version_declared("libsodium", "0.7.1", 8).


%----------------------------------------------------------------------------
% Package: libssh
%----------------------------------------------------------------------------
version_declared("libssh", "0.8.5", 0).
version_declared("libssh", "0.7.5", 1).

variant("libssh", "build_type").
variant_single_value("libssh", "build_type").
variant_default_value("libssh", "build_type", "RelWithDebInfo").
variant_possible_value("libssh", "build_type", "Debug").
variant_possible_value("libssh", "build_type", "MinSizeRel").
variant_possible_value("libssh", "build_type", "RelWithDebInfo").
variant_possible_value("libssh", "build_type", "Release").

declared_dependency("libssh", "cmake", "build").
node("cmake") :- depends_on("libssh", "cmake"), node("libssh").

declared_dependency("libssh", "openssl", "build") :- node("libssh"), 1 { version("libssh", "0.7.5") } 1.
declared_dependency("libssh", "openssl", "link") :- node("libssh"), 1 { version("libssh", "0.7.5") } 1.
node("openssl") :- depends_on("libssh", "openssl"), node("libssh"), 1 { version("libssh", "0.7.5") } 1.
1 { version("openssl", "1.0.1e"); version("openssl", "1.0.1h"); version("openssl", "1.0.1r"); version("openssl", "1.0.1t"); version("openssl", "1.0.1u"); version("openssl", "1.0.2d"); version("openssl", "1.0.2e"); version("openssl", "1.0.2f"); version("openssl", "1.0.2g"); version("openssl", "1.0.2h"); version("openssl", "1.0.2i"); version("openssl", "1.0.2j"); version("openssl", "1.0.2k"); version("openssl", "1.0.2m"); version("openssl", "1.0.2n"); version("openssl", "1.0.2o"); version("openssl", "1.0.2p"); version("openssl", "1.0.2r"); version("openssl", "1.0.2s"); version("openssl", "1.0.2t") } 1 :- depends_on("libssh", "openssl"), node("libssh"), 1 { version("libssh", "0.7.5") } 1.
declared_dependency("libssh", "openssl", "build").
declared_dependency("libssh", "openssl", "link").
node("openssl") :- depends_on("libssh", "openssl"), node("libssh").

declared_dependency("libssh", "zlib", "build").
declared_dependency("libssh", "zlib", "link").
node("zlib") :- depends_on("libssh", "zlib"), node("libssh").


%----------------------------------------------------------------------------
% Package: libssh2
%----------------------------------------------------------------------------
version_declared("libssh2", "1.8.0", 0).
version_declared("libssh2", "1.7.0", 1).
version_declared("libssh2", "1.4.3", 2).

variant("libssh2", "build_type").
variant_single_value("libssh2", "build_type").
variant_default_value("libssh2", "build_type", "RelWithDebInfo").
variant_possible_value("libssh2", "build_type", "Debug").
variant_possible_value("libssh2", "build_type", "MinSizeRel").
variant_possible_value("libssh2", "build_type", "RelWithDebInfo").
variant_possible_value("libssh2", "build_type", "Release").

variant("libssh2", "shared").
variant_single_value("libssh2", "shared").
variant_default_value("libssh2", "shared", "True").
variant_possible_value("libssh2", "shared", "False").
variant_possible_value("libssh2", "shared", "True").

declared_dependency("libssh2", "cmake", "build").
node("cmake") :- depends_on("libssh2", "cmake"), node("libssh2").
1 { version("cmake", "3.0.2"); version("cmake", "3.1.0"); version("cmake", "3.3.1"); version("cmake", "3.4.0"); version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1"); version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1 :- depends_on("libssh2", "cmake"), node("libssh2").

declared_dependency("libssh2", "openssl", "build").
declared_dependency("libssh2", "openssl", "link").
node("openssl") :- depends_on("libssh2", "openssl"), node("libssh2").

declared_dependency("libssh2", "xz", "build").
declared_dependency("libssh2", "xz", "link").
node("xz") :- depends_on("libssh2", "xz"), node("libssh2").

declared_dependency("libssh2", "zlib", "build").
declared_dependency("libssh2", "zlib", "link").
node("zlib") :- depends_on("libssh2", "zlib"), node("libssh2").


%----------------------------------------------------------------------------
% Package: libszip
%----------------------------------------------------------------------------
version_declared("libszip", "2.1.1", 0).
version_declared("libszip", "2.1", 1).


%----------------------------------------------------------------------------
% Package: libtiff
%----------------------------------------------------------------------------
version_declared("libtiff", "4.0.10", 0).
version_declared("libtiff", "4.0.9", 1).
version_declared("libtiff", "4.0.8", 2).
version_declared("libtiff", "4.0.7", 3).
version_declared("libtiff", "4.0.6", 4).
version_declared("libtiff", "3.9.7", 5).

declared_dependency("libtiff", "jpeg", "build").
declared_dependency("libtiff", "jpeg", "link").
node("jpeg") :- depends_on("libtiff", "jpeg"), node("libtiff").

declared_dependency("libtiff", "xz", "build").
declared_dependency("libtiff", "xz", "link").
node("xz") :- depends_on("libtiff", "xz"), node("libtiff").

declared_dependency("libtiff", "zlib", "build").
declared_dependency("libtiff", "zlib", "link").
node("zlib") :- depends_on("libtiff", "zlib"), node("libtiff").


%----------------------------------------------------------------------------
% Package: libtirpc
%----------------------------------------------------------------------------
version_declared("libtirpc", "1.1.4", 0).


%----------------------------------------------------------------------------
% Package: libtool
%----------------------------------------------------------------------------
version_declared("libtool", "2.4.6", 0).
version_declared("libtool", "2.4.2", 1).
version_declared("libtool", "develop", 2).

declared_dependency("libtool", "autoconf", "build") :- node("libtool"), 1 { version("libtool", "2.4.2"); version("libtool", "develop") } 1.
node("autoconf") :- depends_on("libtool", "autoconf"), node("libtool"), 1 { version("libtool", "2.4.2"); version("libtool", "develop") } 1.

declared_dependency("libtool", "automake", "build") :- node("libtool"), 1 { version("libtool", "2.4.2"); version("libtool", "develop") } 1.
node("automake") :- depends_on("libtool", "automake"), node("libtool"), 1 { version("libtool", "2.4.2"); version("libtool", "develop") } 1.

declared_dependency("libtool", "help2man", "build") :- node("libtool"), 1 { version("libtool", "2.4.2"); version("libtool", "develop") } 1.
node("help2man") :- depends_on("libtool", "help2man"), node("libtool"), 1 { version("libtool", "2.4.2"); version("libtool", "develop") } 1.

declared_dependency("libtool", "m4", "build").
node("m4") :- depends_on("libtool", "m4"), node("libtool").

declared_dependency("libtool", "texinfo", "build") :- node("libtool"), 1 { version("libtool", "develop") } 1.
node("texinfo") :- depends_on("libtool", "texinfo"), node("libtool"), 1 { version("libtool", "develop") } 1.

declared_dependency("libtool", "xz", "build") :- node("libtool"), 1 { version("libtool", "develop") } 1.
node("xz") :- depends_on("libtool", "xz"), node("libtool"), 1 { version("libtool", "develop") } 1.


%----------------------------------------------------------------------------
% Package: libunistring
%----------------------------------------------------------------------------
version_declared("libunistring", "0.9.10", 0).
version_declared("libunistring", "0.9.9", 1).
version_declared("libunistring", "0.9.8", 2).
version_declared("libunistring", "0.9.7", 3).
version_declared("libunistring", "0.9.6", 4).

declared_dependency("libunistring", "libiconv", "build").
declared_dependency("libunistring", "libiconv", "link").
node("libiconv") :- depends_on("libunistring", "libiconv"), node("libunistring").


%----------------------------------------------------------------------------
% Package: libuuid
%----------------------------------------------------------------------------
version_declared("libuuid", "1.0.3", 0).


%----------------------------------------------------------------------------
% Package: libuv
%----------------------------------------------------------------------------
version_declared("libuv", "1.25.0", 0).
version_declared("libuv", "1.10.0", 1).
version_declared("libuv", "1.9.0", 2).

declared_dependency("libuv", "autoconf", "build").
node("autoconf") :- depends_on("libuv", "autoconf"), node("libuv").

declared_dependency("libuv", "automake", "build").
node("automake") :- depends_on("libuv", "automake"), node("libuv").

declared_dependency("libuv", "libtool", "build").
node("libtool") :- depends_on("libuv", "libtool"), node("libuv").


%----------------------------------------------------------------------------
% Package: libx11
%----------------------------------------------------------------------------
version_declared("libx11", "1.6.7", 0).
version_declared("libx11", "1.6.5", 1).
version_declared("libx11", "1.6.3", 2).

declared_dependency("libx11", "inputproto", "build").
node("inputproto") :- depends_on("libx11", "inputproto"), node("libx11").

declared_dependency("libx11", "kbproto", "build").
declared_dependency("libx11", "kbproto", "link").
node("kbproto") :- depends_on("libx11", "kbproto"), node("libx11").

declared_dependency("libx11", "libxcb", "build").
declared_dependency("libx11", "libxcb", "link").
node("libxcb") :- depends_on("libx11", "libxcb"), node("libx11").

declared_dependency("libx11", "perl", "build").
node("perl") :- depends_on("libx11", "perl"), node("libx11").

declared_dependency("libx11", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libx11", "pkgconfig"), node("libx11").

declared_dependency("libx11", "util-macros", "build").
node("util-macros") :- depends_on("libx11", "util-macros"), node("libx11").

declared_dependency("libx11", "xextproto", "build").
declared_dependency("libx11", "xextproto", "link").
node("xextproto") :- depends_on("libx11", "xextproto"), node("libx11").

declared_dependency("libx11", "xproto", "build").
node("xproto") :- depends_on("libx11", "xproto"), node("libx11").

declared_dependency("libx11", "xtrans", "build").
node("xtrans") :- depends_on("libx11", "xtrans"), node("libx11").


%----------------------------------------------------------------------------
% Package: libxau
%----------------------------------------------------------------------------
version_declared("libxau", "1.0.8", 0).

declared_dependency("libxau", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxau", "pkgconfig"), node("libxau").

declared_dependency("libxau", "util-macros", "build").
node("util-macros") :- depends_on("libxau", "util-macros"), node("libxau").

declared_dependency("libxau", "xproto", "build").
declared_dependency("libxau", "xproto", "link").
node("xproto") :- depends_on("libxau", "xproto"), node("libxau").


%----------------------------------------------------------------------------
% Package: libxcb
%----------------------------------------------------------------------------
version_declared("libxcb", "1.13", 0).
version_declared("libxcb", "1.12", 1).
version_declared("libxcb", "1.11.1", 2).
version_declared("libxcb", "1.11", 3).

declared_dependency("libxcb", "libpthread-stubs", "build").
declared_dependency("libxcb", "libpthread-stubs", "link").
node("libpthread-stubs") :- depends_on("libxcb", "libpthread-stubs"), node("libxcb").

declared_dependency("libxcb", "libxau", "build").
declared_dependency("libxcb", "libxau", "link").
node("libxau") :- depends_on("libxcb", "libxau"), node("libxcb").

declared_dependency("libxcb", "libxdmcp", "build").
declared_dependency("libxcb", "libxdmcp", "link").
node("libxdmcp") :- depends_on("libxcb", "libxdmcp"), node("libxcb").

declared_dependency("libxcb", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxcb", "pkgconfig"), node("libxcb").

declared_dependency("libxcb", "util-macros", "build").
node("util-macros") :- depends_on("libxcb", "util-macros"), node("libxcb").

declared_dependency("libxcb", "xcb-proto", "build").
node("xcb-proto") :- depends_on("libxcb", "xcb-proto"), node("libxcb").
declared_dependency("libxcb", "xcb-proto", "build") :- node("libxcb"), 1 { version("libxcb", "1.11"); version("libxcb", "1.11.1") } 1.
node("xcb-proto") :- depends_on("libxcb", "xcb-proto"), node("libxcb"), 1 { version("libxcb", "1.11"); version("libxcb", "1.11.1") } 1.
declared_dependency("libxcb", "xcb-proto", "build") :- node("libxcb"), 1 { version("libxcb", "1.12") } 1.
node("xcb-proto") :- depends_on("libxcb", "xcb-proto"), node("libxcb"), 1 { version("libxcb", "1.12") } 1.
1 { version("xcb-proto", "1.12"); version("xcb-proto", "1.13") } 1 :- depends_on("libxcb", "xcb-proto"), node("libxcb"), 1 { version("libxcb", "1.12") } 1.
declared_dependency("libxcb", "xcb-proto", "build") :- node("libxcb"), 1 { version("libxcb", "1.13") } 1.
node("xcb-proto") :- depends_on("libxcb", "xcb-proto"), node("libxcb"), 1 { version("libxcb", "1.13") } 1.
1 { version("xcb-proto", "1.13") } 1 :- depends_on("libxcb", "xcb-proto"), node("libxcb"), 1 { version("libxcb", "1.13") } 1.


%----------------------------------------------------------------------------
% Package: libxcomposite
%----------------------------------------------------------------------------
version_declared("libxcomposite", "0.4.4", 0).

declared_dependency("libxcomposite", "compositeproto", "build").
node("compositeproto") :- depends_on("libxcomposite", "compositeproto"), node("libxcomposite").

declared_dependency("libxcomposite", "fixesproto", "build").
node("fixesproto") :- depends_on("libxcomposite", "fixesproto"), node("libxcomposite").

declared_dependency("libxcomposite", "libx11", "build").
declared_dependency("libxcomposite", "libx11", "link").
node("libx11") :- depends_on("libxcomposite", "libx11"), node("libxcomposite").

declared_dependency("libxcomposite", "libxfixes", "build").
declared_dependency("libxcomposite", "libxfixes", "link").
node("libxfixes") :- depends_on("libxcomposite", "libxfixes"), node("libxcomposite").

declared_dependency("libxcomposite", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxcomposite", "pkgconfig"), node("libxcomposite").

declared_dependency("libxcomposite", "util-macros", "build").
node("util-macros") :- depends_on("libxcomposite", "util-macros"), node("libxcomposite").


%----------------------------------------------------------------------------
% Package: libxdmcp
%----------------------------------------------------------------------------
version_declared("libxdmcp", "1.1.2", 0).

declared_dependency("libxdmcp", "libbsd", "build") :- node("libxdmcp"), node_platform("libxdmcp", "cray").
declared_dependency("libxdmcp", "libbsd", "link") :- node("libxdmcp"), node_platform("libxdmcp", "cray").
node("libbsd") :- depends_on("libxdmcp", "libbsd"), node("libxdmcp"), node_platform("libxdmcp", "cray").
declared_dependency("libxdmcp", "libbsd", "build") :- node("libxdmcp"), node_platform("libxdmcp", "linux").
declared_dependency("libxdmcp", "libbsd", "link") :- node("libxdmcp"), node_platform("libxdmcp", "linux").
node("libbsd") :- depends_on("libxdmcp", "libbsd"), node("libxdmcp"), node_platform("libxdmcp", "linux").

declared_dependency("libxdmcp", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxdmcp", "pkgconfig"), node("libxdmcp").

declared_dependency("libxdmcp", "util-macros", "build").
node("util-macros") :- depends_on("libxdmcp", "util-macros"), node("libxdmcp").

declared_dependency("libxdmcp", "xproto", "build").
node("xproto") :- depends_on("libxdmcp", "xproto"), node("libxdmcp").


%----------------------------------------------------------------------------
% Package: libxext
%----------------------------------------------------------------------------
version_declared("libxext", "1.3.3", 0).

declared_dependency("libxext", "libx11", "build").
declared_dependency("libxext", "libx11", "link").
node("libx11") :- depends_on("libxext", "libx11"), node("libxext").

declared_dependency("libxext", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxext", "pkgconfig"), node("libxext").

declared_dependency("libxext", "util-macros", "build").
node("util-macros") :- depends_on("libxext", "util-macros"), node("libxext").

declared_dependency("libxext", "xextproto", "build").
node("xextproto") :- depends_on("libxext", "xextproto"), node("libxext").

declared_dependency("libxext", "xproto", "build").
node("xproto") :- depends_on("libxext", "xproto"), node("libxext").


%----------------------------------------------------------------------------
% Package: libxfixes
%----------------------------------------------------------------------------
version_declared("libxfixes", "5.0.2", 0).

declared_dependency("libxfixes", "fixesproto", "build").
node("fixesproto") :- depends_on("libxfixes", "fixesproto"), node("libxfixes").

declared_dependency("libxfixes", "libx11", "build").
declared_dependency("libxfixes", "libx11", "link").
node("libx11") :- depends_on("libxfixes", "libx11"), node("libxfixes").

declared_dependency("libxfixes", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxfixes", "pkgconfig"), node("libxfixes").

declared_dependency("libxfixes", "util-macros", "build").
node("util-macros") :- depends_on("libxfixes", "util-macros"), node("libxfixes").

declared_dependency("libxfixes", "xextproto", "build").
node("xextproto") :- depends_on("libxfixes", "xextproto"), node("libxfixes").

declared_dependency("libxfixes", "xproto", "build").
node("xproto") :- depends_on("libxfixes", "xproto"), node("libxfixes").


%----------------------------------------------------------------------------
% Package: libxfont
%----------------------------------------------------------------------------
version_declared("libxfont", "1.5.2", 0).

declared_dependency("libxfont", "fontsproto", "build").
node("fontsproto") :- depends_on("libxfont", "fontsproto"), node("libxfont").

declared_dependency("libxfont", "freetype", "build").
declared_dependency("libxfont", "freetype", "link").
node("freetype") :- depends_on("libxfont", "freetype"), node("libxfont").

declared_dependency("libxfont", "libfontenc", "build").
declared_dependency("libxfont", "libfontenc", "link").
node("libfontenc") :- depends_on("libxfont", "libfontenc"), node("libxfont").

declared_dependency("libxfont", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxfont", "pkgconfig"), node("libxfont").

declared_dependency("libxfont", "util-macros", "build").
node("util-macros") :- depends_on("libxfont", "util-macros"), node("libxfont").

declared_dependency("libxfont", "xproto", "build").
node("xproto") :- depends_on("libxfont", "xproto"), node("libxfont").

declared_dependency("libxfont", "xtrans", "build").
node("xtrans") :- depends_on("libxfont", "xtrans"), node("libxfont").


%----------------------------------------------------------------------------
% Package: libxft
%----------------------------------------------------------------------------
version_declared("libxft", "2.3.2", 0).

declared_dependency("libxft", "fontconfig", "build").
declared_dependency("libxft", "fontconfig", "link").
node("fontconfig") :- depends_on("libxft", "fontconfig"), node("libxft").

declared_dependency("libxft", "freetype", "build").
declared_dependency("libxft", "freetype", "link").
node("freetype") :- depends_on("libxft", "freetype"), node("libxft").

declared_dependency("libxft", "libx11", "build").
declared_dependency("libxft", "libx11", "link").
node("libx11") :- depends_on("libxft", "libx11"), node("libxft").

declared_dependency("libxft", "libxrender", "build").
declared_dependency("libxft", "libxrender", "link").
node("libxrender") :- depends_on("libxft", "libxrender"), node("libxft").

declared_dependency("libxft", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxft", "pkgconfig"), node("libxft").

declared_dependency("libxft", "util-macros", "build").
node("util-macros") :- depends_on("libxft", "util-macros"), node("libxft").


%----------------------------------------------------------------------------
% Package: libxi
%----------------------------------------------------------------------------
version_declared("libxi", "1.7.6", 0).

declared_dependency("libxi", "fixesproto", "build").
node("fixesproto") :- depends_on("libxi", "fixesproto"), node("libxi").

declared_dependency("libxi", "inputproto", "build").
node("inputproto") :- depends_on("libxi", "inputproto"), node("libxi").

declared_dependency("libxi", "libx11", "build").
declared_dependency("libxi", "libx11", "link").
node("libx11") :- depends_on("libxi", "libx11"), node("libxi").

declared_dependency("libxi", "libxext", "build").
declared_dependency("libxi", "libxext", "link").
node("libxext") :- depends_on("libxi", "libxext"), node("libxi").

declared_dependency("libxi", "libxfixes", "build").
declared_dependency("libxi", "libxfixes", "link").
node("libxfixes") :- depends_on("libxi", "libxfixes"), node("libxi").

declared_dependency("libxi", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxi", "pkgconfig"), node("libxi").

declared_dependency("libxi", "xextproto", "build").
node("xextproto") :- depends_on("libxi", "xextproto"), node("libxi").

declared_dependency("libxi", "xproto", "build").
node("xproto") :- depends_on("libxi", "xproto"), node("libxi").


%----------------------------------------------------------------------------
% Package: libxinerama
%----------------------------------------------------------------------------
version_declared("libxinerama", "1.1.3", 0).

declared_dependency("libxinerama", "libx11", "build").
declared_dependency("libxinerama", "libx11", "link").
node("libx11") :- depends_on("libxinerama", "libx11"), node("libxinerama").

declared_dependency("libxinerama", "libxext", "build").
declared_dependency("libxinerama", "libxext", "link").
node("libxext") :- depends_on("libxinerama", "libxext"), node("libxinerama").

declared_dependency("libxinerama", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxinerama", "pkgconfig"), node("libxinerama").

declared_dependency("libxinerama", "util-macros", "build").
node("util-macros") :- depends_on("libxinerama", "util-macros"), node("libxinerama").

declared_dependency("libxinerama", "xextproto", "build").
node("xextproto") :- depends_on("libxinerama", "xextproto"), node("libxinerama").

declared_dependency("libxinerama", "xineramaproto", "build").
node("xineramaproto") :- depends_on("libxinerama", "xineramaproto"), node("libxinerama").


%----------------------------------------------------------------------------
% Package: libxml2
%----------------------------------------------------------------------------
version_declared("libxml2", "2.9.9", 0).
version_declared("libxml2", "2.9.8", 1).
version_declared("libxml2", "2.9.4", 2).
version_declared("libxml2", "2.9.2", 3).
version_declared("libxml2", "2.7.8", 4).

variant("libxml2", "python").
variant_single_value("libxml2", "python").
variant_default_value("libxml2", "python", "False").
variant_possible_value("libxml2", "python", "False").
variant_possible_value("libxml2", "python", "True").

declared_dependency("libxml2", "libiconv", "build").
declared_dependency("libxml2", "libiconv", "link").
node("libiconv") :- depends_on("libxml2", "libiconv"), node("libxml2").

declared_dependency("libxml2", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxml2", "pkgconfig"), node("libxml2").

declared_dependency("libxml2", "python", "build") :- node("libxml2"), variant_value("libxml2", "python", "True").
declared_dependency("libxml2", "python", "link") :- node("libxml2"), variant_value("libxml2", "python", "True").
node("python") :- depends_on("libxml2", "python"), node("libxml2"), variant_value("libxml2", "python", "True").
variant_set("python", "libxml2", "False") :- depends_on("libxml2", "python"), node("libxml2"), variant_value("libxml2", "python", "True").
variant_set("python", "shared", "True") :- depends_on("libxml2", "python"), node("libxml2"), variant_value("libxml2", "python", "True").

declared_dependency("libxml2", "xz", "build").
declared_dependency("libxml2", "xz", "link").
node("xz") :- depends_on("libxml2", "xz"), node("libxml2").

declared_dependency("libxml2", "zlib", "build").
declared_dependency("libxml2", "zlib", "link").
node("zlib") :- depends_on("libxml2", "zlib"), node("libxml2").


%----------------------------------------------------------------------------
% Package: libxrender
%----------------------------------------------------------------------------
version_declared("libxrender", "0.9.10", 0).
version_declared("libxrender", "0.9.9", 1).

declared_dependency("libxrender", "libx11", "build").
declared_dependency("libxrender", "libx11", "link").
node("libx11") :- depends_on("libxrender", "libx11"), node("libxrender").

declared_dependency("libxrender", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxrender", "pkgconfig"), node("libxrender").

declared_dependency("libxrender", "renderproto", "build").
declared_dependency("libxrender", "renderproto", "link").
node("renderproto") :- depends_on("libxrender", "renderproto"), node("libxrender").

declared_dependency("libxrender", "util-macros", "build").
node("util-macros") :- depends_on("libxrender", "util-macros"), node("libxrender").


%----------------------------------------------------------------------------
% Package: libxscrnsaver
%----------------------------------------------------------------------------
version_declared("libxscrnsaver", "1.2.2", 0).

declared_dependency("libxscrnsaver", "libx11", "build").
declared_dependency("libxscrnsaver", "libx11", "link").
node("libx11") :- depends_on("libxscrnsaver", "libx11"), node("libxscrnsaver").

declared_dependency("libxscrnsaver", "libxext", "build").
declared_dependency("libxscrnsaver", "libxext", "link").
node("libxext") :- depends_on("libxscrnsaver", "libxext"), node("libxscrnsaver").

declared_dependency("libxscrnsaver", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxscrnsaver", "pkgconfig"), node("libxscrnsaver").

declared_dependency("libxscrnsaver", "scrnsaverproto", "build").
node("scrnsaverproto") :- depends_on("libxscrnsaver", "scrnsaverproto"), node("libxscrnsaver").

declared_dependency("libxscrnsaver", "util-macros", "build").
node("util-macros") :- depends_on("libxscrnsaver", "util-macros"), node("libxscrnsaver").

declared_dependency("libxscrnsaver", "xextproto", "build").
node("xextproto") :- depends_on("libxscrnsaver", "xextproto"), node("libxscrnsaver").


%----------------------------------------------------------------------------
% Package: libxslt
%----------------------------------------------------------------------------
version_declared("libxslt", "1.1.33", 0).
version_declared("libxslt", "1.1.32", 1).
version_declared("libxslt", "1.1.29", 2).
version_declared("libxslt", "1.1.28", 3).
version_declared("libxslt", "1.1.26", 4).

variant("libxslt", "crypto").
variant_single_value("libxslt", "crypto").
variant_default_value("libxslt", "crypto", "True").
variant_possible_value("libxslt", "crypto", "False").
variant_possible_value("libxslt", "crypto", "True").

variant("libxslt", "python").
variant_single_value("libxslt", "python").
variant_default_value("libxslt", "python", "False").
variant_possible_value("libxslt", "python", "False").
variant_possible_value("libxslt", "python", "True").

declared_dependency("libxslt", "libgcrypt", "build") :- node("libxslt"), variant_value("libxslt", "crypto", "True").
declared_dependency("libxslt", "libgcrypt", "link") :- node("libxslt"), variant_value("libxslt", "crypto", "True").
node("libgcrypt") :- depends_on("libxslt", "libgcrypt"), node("libxslt"), variant_value("libxslt", "crypto", "True").

declared_dependency("libxslt", "libiconv", "build").
declared_dependency("libxslt", "libiconv", "link").
node("libiconv") :- depends_on("libxslt", "libiconv"), node("libxslt").

declared_dependency("libxslt", "libxml2", "build").
declared_dependency("libxslt", "libxml2", "link").
node("libxml2") :- depends_on("libxslt", "libxml2"), node("libxslt").
declared_dependency("libxslt", "libxml2", "build") :- node("libxslt"), variant_value("libxslt", "python", "True").
declared_dependency("libxslt", "libxml2", "link") :- node("libxslt"), variant_value("libxslt", "python", "True").
node("libxml2") :- depends_on("libxslt", "libxml2"), node("libxslt"), variant_value("libxslt", "python", "True").
variant_set("libxml2", "python", "True") :- depends_on("libxslt", "libxml2"), node("libxslt"), variant_value("libxslt", "python", "True").

declared_dependency("libxslt", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxslt", "pkgconfig"), node("libxslt").

declared_dependency("libxslt", "python", "build") :- node("libxslt"), variant_value("libxslt", "python", "True").
declared_dependency("libxslt", "python", "link") :- node("libxslt"), variant_value("libxslt", "python", "True").
node("python") :- depends_on("libxslt", "python"), node("libxslt"), variant_value("libxslt", "python", "True").
variant_set("python", "shared", "True") :- depends_on("libxslt", "python"), node("libxslt"), variant_value("libxslt", "python", "True").

declared_dependency("libxslt", "xz", "build").
declared_dependency("libxslt", "xz", "link").
node("xz") :- depends_on("libxslt", "xz"), node("libxslt").

declared_dependency("libxslt", "zlib", "build").
declared_dependency("libxslt", "zlib", "link").
node("zlib") :- depends_on("libxslt", "zlib"), node("libxslt").


%----------------------------------------------------------------------------
% Package: libxt
%----------------------------------------------------------------------------
version_declared("libxt", "1.1.5", 0).

declared_dependency("libxt", "kbproto", "build").
node("kbproto") :- depends_on("libxt", "kbproto"), node("libxt").

declared_dependency("libxt", "libice", "build").
declared_dependency("libxt", "libice", "link").
node("libice") :- depends_on("libxt", "libice"), node("libxt").

declared_dependency("libxt", "libsm", "build").
declared_dependency("libxt", "libsm", "link").
node("libsm") :- depends_on("libxt", "libsm"), node("libxt").

declared_dependency("libxt", "libx11", "build").
declared_dependency("libxt", "libx11", "link").
node("libx11") :- depends_on("libxt", "libx11"), node("libxt").

declared_dependency("libxt", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxt", "pkgconfig"), node("libxt").

declared_dependency("libxt", "util-macros", "build").
node("util-macros") :- depends_on("libxt", "util-macros"), node("libxt").

declared_dependency("libxt", "xproto", "build").
node("xproto") :- depends_on("libxt", "xproto"), node("libxt").


%----------------------------------------------------------------------------
% Package: libxtst
%----------------------------------------------------------------------------
version_declared("libxtst", "1.2.2", 0).

declared_dependency("libxtst", "fixesproto", "build").
node("fixesproto") :- depends_on("libxtst", "fixesproto"), node("libxtst").

declared_dependency("libxtst", "inputproto", "build").
node("inputproto") :- depends_on("libxtst", "inputproto"), node("libxtst").

declared_dependency("libxtst", "libx11", "build").
declared_dependency("libxtst", "libx11", "link").
node("libx11") :- depends_on("libxtst", "libx11"), node("libxtst").

declared_dependency("libxtst", "libxext", "build").
declared_dependency("libxtst", "libxext", "link").
node("libxext") :- depends_on("libxtst", "libxext"), node("libxtst").

declared_dependency("libxtst", "libxi", "build").
declared_dependency("libxtst", "libxi", "link").
node("libxi") :- depends_on("libxtst", "libxi"), node("libxtst").

declared_dependency("libxtst", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libxtst", "pkgconfig"), node("libxtst").

declared_dependency("libxtst", "recordproto", "build").
node("recordproto") :- depends_on("libxtst", "recordproto"), node("libxtst").

declared_dependency("libxtst", "util-macros", "build").
node("util-macros") :- depends_on("libxtst", "util-macros"), node("libxtst").

declared_dependency("libxtst", "xextproto", "build").
node("xextproto") :- depends_on("libxtst", "xextproto"), node("libxtst").


%----------------------------------------------------------------------------
% Package: libzmq
%----------------------------------------------------------------------------
version_declared("libzmq", "4.3.2", 0).
version_declared("libzmq", "4.3.1", 1).
version_declared("libzmq", "4.3.0", 2).
version_declared("libzmq", "4.2.5", 3).
version_declared("libzmq", "4.2.2", 4).
version_declared("libzmq", "4.1.4", 5).
version_declared("libzmq", "4.1.2", 6).
version_declared("libzmq", "4.1.1", 7).
version_declared("libzmq", "4.0.7", 8).
version_declared("libzmq", "4.0.6", 9).
version_declared("libzmq", "4.0.5", 10).
version_declared("libzmq", "develop", 11).

variant("libzmq", "libsodium").
variant_single_value("libzmq", "libsodium").
variant_default_value("libzmq", "libsodium", "True").
variant_possible_value("libzmq", "libsodium", "False").
variant_possible_value("libzmq", "libsodium", "True").

declared_dependency("libzmq", "autoconf", "build") :- node("libzmq"), 1 { version("libzmq", "develop") } 1.
node("autoconf") :- depends_on("libzmq", "autoconf"), node("libzmq"), 1 { version("libzmq", "develop") } 1.

declared_dependency("libzmq", "automake", "build") :- node("libzmq"), 1 { version("libzmq", "develop") } 1.
node("automake") :- depends_on("libzmq", "automake"), node("libzmq"), 1 { version("libzmq", "develop") } 1.

declared_dependency("libzmq", "libsodium", "build") :- node("libzmq"), 1 { version("libzmq", "4.0.5"); version("libzmq", "4.0.6"); version("libzmq", "4.0.7"); version("libzmq", "4.1.1"); version("libzmq", "4.1.2") } 1, variant_value("libzmq", "libsodium", "True").
declared_dependency("libzmq", "libsodium", "link") :- node("libzmq"), 1 { version("libzmq", "4.0.5"); version("libzmq", "4.0.6"); version("libzmq", "4.0.7"); version("libzmq", "4.1.1"); version("libzmq", "4.1.2") } 1, variant_value("libzmq", "libsodium", "True").
node("libsodium") :- depends_on("libzmq", "libsodium"), node("libzmq"), 1 { version("libzmq", "4.0.5"); version("libzmq", "4.0.6"); version("libzmq", "4.0.7"); version("libzmq", "4.1.1"); version("libzmq", "4.1.2") } 1, variant_value("libzmq", "libsodium", "True").
1 { version("libsodium", "0.7.1"); version("libsodium", "1.0.0"); version("libsodium", "1.0.1"); version("libsodium", "1.0.2"); version("libsodium", "1.0.3") } 1 :- depends_on("libzmq", "libsodium"), node("libzmq"), 1 { version("libzmq", "4.0.5"); version("libzmq", "4.0.6"); version("libzmq", "4.0.7"); version("libzmq", "4.1.1"); version("libzmq", "4.1.2") } 1, variant_value("libzmq", "libsodium", "True").
declared_dependency("libzmq", "libsodium", "build") :- node("libzmq"), variant_value("libzmq", "libsodium", "True").
declared_dependency("libzmq", "libsodium", "link") :- node("libzmq"), variant_value("libzmq", "libsodium", "True").
node("libsodium") :- depends_on("libzmq", "libsodium"), node("libzmq"), variant_value("libzmq", "libsodium", "True").

declared_dependency("libzmq", "libtool", "build") :- node("libzmq"), 1 { version("libzmq", "develop") } 1.
node("libtool") :- depends_on("libzmq", "libtool"), node("libzmq"), 1 { version("libzmq", "develop") } 1.

declared_dependency("libzmq", "pkgconfig", "build").
node("pkgconfig") :- depends_on("libzmq", "pkgconfig"), node("libzmq").


%----------------------------------------------------------------------------
% Package: llvm
%----------------------------------------------------------------------------
version_declared("llvm", "9.0.1", 0).
version_declared("llvm", "9.0.0", 1).
version_declared("llvm", "8.0.0", 2).
version_declared("llvm", "7.1.0", 3).
version_declared("llvm", "7.0.1", 4).
version_declared("llvm", "6.0.1", 5).
version_declared("llvm", "6.0.0", 6).
version_declared("llvm", "5.0.2", 7).
version_declared("llvm", "5.0.1", 8).
version_declared("llvm", "5.0.0", 9).
version_declared("llvm", "4.0.1", 10).
version_declared("llvm", "4.0.0", 11).
version_declared("llvm", "3.9.1", 12).
version_declared("llvm", "3.9.0", 13).
version_declared("llvm", "3.8.1", 14).
version_declared("llvm", "3.8.0", 15).
version_declared("llvm", "3.7.1", 16).
version_declared("llvm", "3.7.0", 17).
version_declared("llvm", "3.6.2", 18).
version_declared("llvm", "3.5.1", 19).
version_declared("llvm", "master", 20).

variant("llvm", "all_targets").
variant_single_value("llvm", "all_targets").
variant_default_value("llvm", "all_targets", "False").
variant_possible_value("llvm", "all_targets", "False").
variant_possible_value("llvm", "all_targets", "True").

variant("llvm", "build_type").
variant_single_value("llvm", "build_type").
variant_default_value("llvm", "build_type", "Release").
variant_possible_value("llvm", "build_type", "Debug").
variant_possible_value("llvm", "build_type", "MinSizeRel").
variant_possible_value("llvm", "build_type", "RelWithDebInfo").
variant_possible_value("llvm", "build_type", "Release").

variant("llvm", "clang").
variant_single_value("llvm", "clang").
variant_default_value("llvm", "clang", "True").
variant_possible_value("llvm", "clang", "False").
variant_possible_value("llvm", "clang", "True").

variant("llvm", "compiler-rt").
variant_single_value("llvm", "compiler-rt").
variant_default_value("llvm", "compiler-rt", "True").
variant_possible_value("llvm", "compiler-rt", "False").
variant_possible_value("llvm", "compiler-rt", "True").

variant("llvm", "gold").
variant_single_value("llvm", "gold").
variant_default_value("llvm", "gold", "True").
variant_possible_value("llvm", "gold", "False").
variant_possible_value("llvm", "gold", "True").

variant("llvm", "internal_unwind").
variant_single_value("llvm", "internal_unwind").
variant_default_value("llvm", "internal_unwind", "True").
variant_possible_value("llvm", "internal_unwind", "False").
variant_possible_value("llvm", "internal_unwind", "True").

variant("llvm", "libcxx").
variant_single_value("llvm", "libcxx").
variant_default_value("llvm", "libcxx", "True").
variant_possible_value("llvm", "libcxx", "False").
variant_possible_value("llvm", "libcxx", "True").

variant("llvm", "link_dylib").
variant_single_value("llvm", "link_dylib").
variant_default_value("llvm", "link_dylib", "False").
variant_possible_value("llvm", "link_dylib", "False").
variant_possible_value("llvm", "link_dylib", "True").

variant("llvm", "lld").
variant_single_value("llvm", "lld").
variant_default_value("llvm", "lld", "True").
variant_possible_value("llvm", "lld", "False").
variant_possible_value("llvm", "lld", "True").

variant("llvm", "lldb").
variant_single_value("llvm", "lldb").
variant_default_value("llvm", "lldb", "True").
variant_possible_value("llvm", "lldb", "False").
variant_possible_value("llvm", "lldb", "True").

variant("llvm", "omp_tsan").
variant_single_value("llvm", "omp_tsan").
variant_default_value("llvm", "omp_tsan", "False").
variant_possible_value("llvm", "omp_tsan", "False").
variant_possible_value("llvm", "omp_tsan", "True").

variant("llvm", "polly").
variant_single_value("llvm", "polly").
variant_default_value("llvm", "polly", "True").
variant_possible_value("llvm", "polly", "False").
variant_possible_value("llvm", "polly", "True").

variant("llvm", "python").
variant_single_value("llvm", "python").
variant_default_value("llvm", "python", "False").
variant_possible_value("llvm", "python", "False").
variant_possible_value("llvm", "python", "True").

variant("llvm", "shared_libs").
variant_single_value("llvm", "shared_libs").
variant_default_value("llvm", "shared_libs", "False").
variant_possible_value("llvm", "shared_libs", "False").
variant_possible_value("llvm", "shared_libs", "True").

declared_dependency("llvm", "binutils", "build") :- node("llvm"), variant_value("llvm", "gold", "True").
declared_dependency("llvm", "binutils", "link") :- node("llvm"), variant_value("llvm", "gold", "True").
node("binutils") :- depends_on("llvm", "binutils"), node("llvm"), variant_value("llvm", "gold", "True").
variant_set("binutils", "gold", "True") :- depends_on("llvm", "binutils"), node("llvm"), variant_value("llvm", "gold", "True").

declared_dependency("llvm", "cmake", "build").
node("cmake") :- depends_on("llvm", "cmake"), node("llvm").
1 { version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1"); version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1 :- depends_on("llvm", "cmake"), node("llvm").

declared_dependency("llvm", "gmp", "build") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2") } 1, variant_value("llvm", "polly", "True").
declared_dependency("llvm", "gmp", "link") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2") } 1, variant_value("llvm", "polly", "True").
node("gmp") :- depends_on("llvm", "gmp"), node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2") } 1, variant_value("llvm", "polly", "True").

declared_dependency("llvm", "isl", "build") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2") } 1, variant_value("llvm", "polly", "True").
declared_dependency("llvm", "isl", "link") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2") } 1, variant_value("llvm", "polly", "True").
node("isl") :- depends_on("llvm", "isl"), node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2") } 1, variant_value("llvm", "polly", "True").

declared_dependency("llvm", "libedit", "build") :- node("llvm"), variant_value("llvm", "lldb", "True").
declared_dependency("llvm", "libedit", "link") :- node("llvm"), variant_value("llvm", "lldb", "True").
node("libedit") :- depends_on("llvm", "libedit"), node("llvm"), variant_value("llvm", "lldb", "True").

declared_dependency("llvm", "ncurses", "build").
declared_dependency("llvm", "ncurses", "link").
node("ncurses") :- depends_on("llvm", "ncurses"), node("llvm").
variant_set("ncurses", "termlib", "True") :- depends_on("llvm", "ncurses"), node("llvm").

declared_dependency("llvm", "perl-data-dumper", "build").
node("perl-data-dumper") :- depends_on("llvm", "perl-data-dumper"), node("llvm").

declared_dependency("llvm", "py-six", "build") :- node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "lldb", "True"), variant_value("llvm", "python", "True").
declared_dependency("llvm", "py-six", "link") :- node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "lldb", "True"), variant_value("llvm", "python", "True").
node("py-six") :- depends_on("llvm", "py-six"), node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "lldb", "True"), variant_value("llvm", "python", "True").

declared_dependency("llvm", "python", "build") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "False").
node("python") :- depends_on("llvm", "python"), node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "False").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16") } 1 :- depends_on("llvm", "python"), node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "False").
declared_dependency("llvm", "python", "build") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "True").
declared_dependency("llvm", "python", "link") :- node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "True").
node("python") :- depends_on("llvm", "python"), node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "True").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16") } 1 :- depends_on("llvm", "python"), node("llvm"), 1 { version("llvm", "3.5.1"); version("llvm", "3.6.2"); version("llvm", "3.7.0"); version("llvm", "3.7.1"); version("llvm", "3.8.0"); version("llvm", "3.8.1"); version("llvm", "3.9.0"); version("llvm", "3.9.1"); version("llvm", "4.0.0"); version("llvm", "4.0.1") } 1, variant_value("llvm", "python", "True").
declared_dependency("llvm", "python", "build") :- node("llvm"), variant_value("llvm", "python", "True").
declared_dependency("llvm", "python", "link") :- node("llvm"), variant_value("llvm", "python", "True").
node("python") :- depends_on("llvm", "python"), node("llvm"), variant_value("llvm", "python", "True").
declared_dependency("llvm", "python", "build") :- node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "python", "False").
node("python") :- depends_on("llvm", "python"), node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "python", "False").
declared_dependency("llvm", "python", "build") :- node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "python", "True").
declared_dependency("llvm", "python", "link") :- node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "python", "True").
node("python") :- depends_on("llvm", "python"), node("llvm"), 1 { version("llvm", "5.0.0"); version("llvm", "5.0.1"); version("llvm", "5.0.2"); version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1, variant_value("llvm", "python", "True").

declared_dependency("llvm", "swig", "build") :- node("llvm"), variant_value("llvm", "lldb", "True").
declared_dependency("llvm", "swig", "link") :- node("llvm"), variant_value("llvm", "lldb", "True").
node("swig") :- depends_on("llvm", "swig"), node("llvm"), variant_value("llvm", "lldb", "True").


%----------------------------------------------------------------------------
% Package: lm-sensors
%----------------------------------------------------------------------------
version_declared("lm-sensors", "3-6-0", 0).
version_declared("lm-sensors", "3-5-0", 1).
version_declared("lm-sensors", "3-4-0", 2).
version_declared("lm-sensors", "3-3-5", 3).
version_declared("lm-sensors", "3-3-4", 4).
version_declared("lm-sensors", "3-3-3", 5).
version_declared("lm-sensors", "3-3-2", 6).
version_declared("lm-sensors", "3-3-1", 7).
version_declared("lm-sensors", "3-3-0", 8).
version_declared("lm-sensors", "3-2-0", 9).
version_declared("lm-sensors", "3-1-2", 10).
version_declared("lm-sensors", "3-1-1", 11).

declared_dependency("lm-sensors", "bison", "build").
node("bison") :- depends_on("lm-sensors", "bison"), node("lm-sensors").

declared_dependency("lm-sensors", "flex", "build").
node("flex") :- depends_on("lm-sensors", "flex"), node("lm-sensors").

declared_dependency("lm-sensors", "perl", "run").
node("perl") :- depends_on("lm-sensors", "perl"), node("lm-sensors").


%----------------------------------------------------------------------------
% Package: lsf
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: lz4
%----------------------------------------------------------------------------
version_declared("lz4", "1.9.2", 0).
version_declared("lz4", "1.9.0", 1).
version_declared("lz4", "1.8.3", 2).
version_declared("lz4", "1.8.1.2", 3).
version_declared("lz4", "1.7.5", 4).
version_declared("lz4", "1.3.1", 5).

declared_dependency("lz4", "valgrind", "test").
node("valgrind") :- depends_on("lz4", "valgrind"), node("lz4").


%----------------------------------------------------------------------------
% Package: lzo
%----------------------------------------------------------------------------
version_declared("lzo", "2.10", 0).
version_declared("lzo", "2.09", 1).
version_declared("lzo", "2.08", 2).
version_declared("lzo", "2.07", 3).
version_declared("lzo", "2.06", 4).
version_declared("lzo", "2.05", 5).


%----------------------------------------------------------------------------
% Package: m4
%----------------------------------------------------------------------------
version_declared("m4", "1.4.18", 0).
version_declared("m4", "1.4.17", 1).

variant("m4", "sigsegv").
variant_single_value("m4", "sigsegv").
variant_default_value("m4", "sigsegv", "True").
variant_possible_value("m4", "sigsegv", "False").
variant_possible_value("m4", "sigsegv", "True").

declared_dependency("m4", "libsigsegv", "build") :- node("m4"), variant_value("m4", "sigsegv", "True").
declared_dependency("m4", "libsigsegv", "link") :- node("m4"), variant_value("m4", "sigsegv", "True").
node("libsigsegv") :- depends_on("m4", "libsigsegv"), node("m4"), variant_value("m4", "sigsegv", "True").


%----------------------------------------------------------------------------
% Package: mariadb
%----------------------------------------------------------------------------
version_declared("mariadb", "10.4.8", 0).
version_declared("mariadb", "10.4.7", 1).
version_declared("mariadb", "10.2.8", 2).
version_declared("mariadb", "10.1.23", 3).
version_declared("mariadb", "10.1.14", 4).
version_declared("mariadb", "5.5.56", 5).
version_declared("mariadb", "5.5.49", 6).

variant("mariadb", "build_type").
variant_single_value("mariadb", "build_type").
variant_default_value("mariadb", "build_type", "RelWithDebInfo").
variant_possible_value("mariadb", "build_type", "Debug").
variant_possible_value("mariadb", "build_type", "MinSizeRel").
variant_possible_value("mariadb", "build_type", "RelWithDebInfo").
variant_possible_value("mariadb", "build_type", "Release").

variant("mariadb", "nonblocking").
variant_single_value("mariadb", "nonblocking").
variant_default_value("mariadb", "nonblocking", "True").
variant_possible_value("mariadb", "nonblocking", "False").
variant_possible_value("mariadb", "nonblocking", "True").

declared_dependency("mariadb", "bison", "build").
node("bison") :- depends_on("mariadb", "bison"), node("mariadb").

declared_dependency("mariadb", "boost", "build").
declared_dependency("mariadb", "boost", "link").
node("boost") :- depends_on("mariadb", "boost"), node("mariadb").

declared_dependency("mariadb", "cmake", "build").
node("cmake") :- depends_on("mariadb", "cmake"), node("mariadb").

declared_dependency("mariadb", "curl", "build").
declared_dependency("mariadb", "curl", "link").
node("curl") :- depends_on("mariadb", "curl"), node("mariadb").

declared_dependency("mariadb", "jemalloc", "build").
declared_dependency("mariadb", "jemalloc", "link").
node("jemalloc") :- depends_on("mariadb", "jemalloc"), node("mariadb").

declared_dependency("mariadb", "libaio", "build") :- node("mariadb"), node_platform("mariadb", "linux").
declared_dependency("mariadb", "libaio", "link") :- node("mariadb"), node_platform("mariadb", "linux").
node("libaio") :- depends_on("mariadb", "libaio"), node("mariadb"), node_platform("mariadb", "linux").

declared_dependency("mariadb", "libedit", "build").
declared_dependency("mariadb", "libedit", "link").
node("libedit") :- depends_on("mariadb", "libedit"), node("mariadb").

declared_dependency("mariadb", "libevent", "build") :- node("mariadb"), variant_value("mariadb", "nonblocking", "True").
declared_dependency("mariadb", "libevent", "link") :- node("mariadb"), variant_value("mariadb", "nonblocking", "True").
node("libevent") :- depends_on("mariadb", "libevent"), node("mariadb"), variant_value("mariadb", "nonblocking", "True").

declared_dependency("mariadb", "libxml2", "build").
declared_dependency("mariadb", "libxml2", "link").
node("libxml2") :- depends_on("mariadb", "libxml2"), node("mariadb").

declared_dependency("mariadb", "libzmq", "build").
declared_dependency("mariadb", "libzmq", "link").
node("libzmq") :- depends_on("mariadb", "libzmq"), node("mariadb").

declared_dependency("mariadb", "lz4", "build").
declared_dependency("mariadb", "lz4", "link").
node("lz4") :- depends_on("mariadb", "lz4"), node("mariadb").

declared_dependency("mariadb", "msgpack-c", "build").
declared_dependency("mariadb", "msgpack-c", "link").
node("msgpack-c") :- depends_on("mariadb", "msgpack-c"), node("mariadb").

declared_dependency("mariadb", "ncurses", "build").
declared_dependency("mariadb", "ncurses", "link").
node("ncurses") :- depends_on("mariadb", "ncurses"), node("mariadb").

declared_dependency("mariadb", "openssl", "build") :- node("mariadb"), 1 { version("mariadb", "5.5.49"); version("mariadb", "5.5.56"); version("mariadb", "10.1.14"); version("mariadb", "10.1.23") } 1.
declared_dependency("mariadb", "openssl", "link") :- node("mariadb"), 1 { version("mariadb", "5.5.49"); version("mariadb", "5.5.56"); version("mariadb", "10.1.14"); version("mariadb", "10.1.23") } 1.
node("openssl") :- depends_on("mariadb", "openssl"), node("mariadb"), 1 { version("mariadb", "5.5.49"); version("mariadb", "5.5.56"); version("mariadb", "10.1.14"); version("mariadb", "10.1.23") } 1.
1 { version("openssl", "1.0.1e"); version("openssl", "1.0.1h"); version("openssl", "1.0.1r"); version("openssl", "1.0.1t"); version("openssl", "1.0.1u"); version("openssl", "1.0.2d"); version("openssl", "1.0.2e"); version("openssl", "1.0.2f"); version("openssl", "1.0.2g"); version("openssl", "1.0.2h"); version("openssl", "1.0.2i"); version("openssl", "1.0.2j"); version("openssl", "1.0.2k"); version("openssl", "1.0.2m"); version("openssl", "1.0.2n"); version("openssl", "1.0.2o"); version("openssl", "1.0.2p"); version("openssl", "1.0.2r"); version("openssl", "1.0.2s"); version("openssl", "1.0.2t") } 1 :- depends_on("mariadb", "openssl"), node("mariadb"), 1 { version("mariadb", "5.5.49"); version("mariadb", "5.5.56"); version("mariadb", "10.1.14"); version("mariadb", "10.1.23") } 1.
declared_dependency("mariadb", "openssl", "build").
declared_dependency("mariadb", "openssl", "link").
node("openssl") :- depends_on("mariadb", "openssl"), node("mariadb").

declared_dependency("mariadb", "pkgconfig", "build").
node("pkgconfig") :- depends_on("mariadb", "pkgconfig"), node("mariadb").

declared_dependency("mariadb", "zlib", "build").
declared_dependency("mariadb", "zlib", "link").
node("zlib") :- depends_on("mariadb", "zlib"), node("mariadb").


%----------------------------------------------------------------------------
% Package: mawk
%----------------------------------------------------------------------------
version_declared("mawk", "1.3.4-20171017", 0).
version_declared("mawk", "1.3.4", 1).


%----------------------------------------------------------------------------
% Package: mesa
%----------------------------------------------------------------------------
version_declared("mesa", "18.3.6", 0).

variant("mesa", "glx").
variant_single_value("mesa", "glx").
variant_default_value("mesa", "glx", "False").
variant_possible_value("mesa", "glx", "False").
variant_possible_value("mesa", "glx", "True").

variant("mesa", "llvm").
variant_single_value("mesa", "llvm").
variant_default_value("mesa", "llvm", "True").
variant_possible_value("mesa", "llvm", "False").
variant_possible_value("mesa", "llvm", "True").

variant("mesa", "opengl").
variant_single_value("mesa", "opengl").
variant_default_value("mesa", "opengl", "True").
variant_possible_value("mesa", "opengl", "False").
variant_possible_value("mesa", "opengl", "True").

variant("mesa", "opengles").
variant_single_value("mesa", "opengles").
variant_default_value("mesa", "opengles", "False").
variant_possible_value("mesa", "opengles", "False").
variant_possible_value("mesa", "opengles", "True").

variant("mesa", "osmesa").
variant_single_value("mesa", "osmesa").
variant_default_value("mesa", "osmesa", "True").
variant_possible_value("mesa", "osmesa", "False").
variant_possible_value("mesa", "osmesa", "True").

variant("mesa", "swr").
not variant_single_value("mesa", "swr").
variant_default_value("mesa", "swr", "none").
variant_possible_value("mesa", "swr", "avx").
variant_possible_value("mesa", "swr", "avx2").
variant_possible_value("mesa", "swr", "knl").
variant_possible_value("mesa", "swr", "none").
variant_possible_value("mesa", "swr", "skx").

declared_dependency("mesa", "autoconf", "build").
node("autoconf") :- depends_on("mesa", "autoconf"), node("mesa").

declared_dependency("mesa", "automake", "build").
node("automake") :- depends_on("mesa", "automake"), node("mesa").

declared_dependency("mesa", "bison", "build").
node("bison") :- depends_on("mesa", "bison"), node("mesa").

declared_dependency("mesa", "expat", "build").
declared_dependency("mesa", "expat", "link").
node("expat") :- depends_on("mesa", "expat"), node("mesa").

declared_dependency("mesa", "flex", "build").
node("flex") :- depends_on("mesa", "flex"), node("mesa").

declared_dependency("mesa", "gettext", "build").
node("gettext") :- depends_on("mesa", "gettext"), node("mesa").

declared_dependency("mesa", "glproto", "build") :- node("mesa"), variant_value("mesa", "glx", "True").
node("glproto") :- depends_on("mesa", "glproto"), node("mesa"), variant_value("mesa", "glx", "True").

declared_dependency("mesa", "libtool", "build").
node("libtool") :- depends_on("mesa", "libtool"), node("mesa").

declared_dependency("mesa", "libx11", "build") :- node("mesa"), variant_value("mesa", "glx", "True").
declared_dependency("mesa", "libx11", "link") :- node("mesa"), variant_value("mesa", "glx", "True").
node("libx11") :- depends_on("mesa", "libx11"), node("mesa"), variant_value("mesa", "glx", "True").

declared_dependency("mesa", "libxcb", "build") :- node("mesa"), variant_value("mesa", "glx", "True").
declared_dependency("mesa", "libxcb", "link") :- node("mesa"), variant_value("mesa", "glx", "True").
node("libxcb") :- depends_on("mesa", "libxcb"), node("mesa"), variant_value("mesa", "glx", "True").

declared_dependency("mesa", "libxext", "build") :- node("mesa"), variant_value("mesa", "glx", "True").
declared_dependency("mesa", "libxext", "link") :- node("mesa"), variant_value("mesa", "glx", "True").
node("libxext") :- depends_on("mesa", "libxext"), node("mesa"), variant_value("mesa", "glx", "True").

declared_dependency("mesa", "libxml2", "build").
declared_dependency("mesa", "libxml2", "link").
node("libxml2") :- depends_on("mesa", "libxml2"), node("mesa").

declared_dependency("mesa", "llvm", "build") :- node("mesa"), variant_value("mesa", "llvm", "True").
declared_dependency("mesa", "llvm", "link") :- node("mesa"), variant_value("mesa", "llvm", "True").
node("llvm") :- depends_on("mesa", "llvm"), node("mesa"), variant_value("mesa", "llvm", "True").
1 { version("llvm", "6.0.0"); version("llvm", "6.0.1"); version("llvm", "7.0.1"); version("llvm", "7.1.0"); version("llvm", "8.0.0"); version("llvm", "9.0.0"); version("llvm", "9.0.1"); version("llvm", "master") } 1 :- depends_on("mesa", "llvm"), node("mesa"), variant_value("mesa", "llvm", "True").

declared_dependency("mesa", "m4", "build").
node("m4") :- depends_on("mesa", "m4"), node("mesa").

declared_dependency("mesa", "pkgconfig", "build").
node("pkgconfig") :- depends_on("mesa", "pkgconfig"), node("mesa").

declared_dependency("mesa", "py-mako", "build").
node("py-mako") :- depends_on("mesa", "py-mako"), node("mesa").

declared_dependency("mesa", "python", "build").
node("python") :- depends_on("mesa", "python"), node("mesa").

declared_dependency("mesa", "zlib", "build").
declared_dependency("mesa", "zlib", "link").
node("zlib") :- depends_on("mesa", "zlib"), node("mesa").


%----------------------------------------------------------------------------
% Package: meson
%----------------------------------------------------------------------------
version_declared("meson", "0.49.1", 0).
version_declared("meson", "0.49.0", 1).
version_declared("meson", "0.42.0", 2).
version_declared("meson", "0.41.2", 3).
version_declared("meson", "0.41.1", 4).

variant("meson", "ninjabuild").
variant_single_value("meson", "ninjabuild").
variant_default_value("meson", "ninjabuild", "True").
variant_possible_value("meson", "ninjabuild", "False").
variant_possible_value("meson", "ninjabuild", "True").

declared_dependency("meson", "ninja", "build") :- node("meson"), variant_value("meson", "ninjabuild", "True").
declared_dependency("meson", "ninja", "run") :- node("meson"), variant_value("meson", "ninjabuild", "True").
node("ninja") :- depends_on("meson", "ninja"), node("meson"), variant_value("meson", "ninjabuild", "True").

declared_dependency("meson", "py-setuptools", "build").
node("py-setuptools") :- depends_on("meson", "py-setuptools"), node("meson").

declared_dependency("meson", "python", "build").
declared_dependency("meson", "python", "link").
declared_dependency("meson", "python", "run").
node("python") :- depends_on("meson", "python"), node("meson").
1 { version("python", "3.1.5"); version("python", "3.2.6"); version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("meson", "python"), node("meson").


%----------------------------------------------------------------------------
% Package: mkfontdir
%----------------------------------------------------------------------------
version_declared("mkfontdir", "1.0.7", 0).

declared_dependency("mkfontdir", "mkfontscale", "run").
node("mkfontscale") :- depends_on("mkfontdir", "mkfontscale"), node("mkfontdir").

declared_dependency("mkfontdir", "pkgconfig", "build").
node("pkgconfig") :- depends_on("mkfontdir", "pkgconfig"), node("mkfontdir").

declared_dependency("mkfontdir", "util-macros", "build").
node("util-macros") :- depends_on("mkfontdir", "util-macros"), node("mkfontdir").


%----------------------------------------------------------------------------
% Package: mkfontscale
%----------------------------------------------------------------------------
version_declared("mkfontscale", "1.1.2", 0).

declared_dependency("mkfontscale", "freetype", "build").
declared_dependency("mkfontscale", "freetype", "link").
node("freetype") :- depends_on("mkfontscale", "freetype"), node("mkfontscale").

declared_dependency("mkfontscale", "libfontenc", "build").
declared_dependency("mkfontscale", "libfontenc", "link").
node("libfontenc") :- depends_on("mkfontscale", "libfontenc"), node("mkfontscale").

declared_dependency("mkfontscale", "pkgconfig", "build").
node("pkgconfig") :- depends_on("mkfontscale", "pkgconfig"), node("mkfontscale").

declared_dependency("mkfontscale", "util-macros", "build").
node("util-macros") :- depends_on("mkfontscale", "util-macros"), node("mkfontscale").

declared_dependency("mkfontscale", "xproto", "build").
node("xproto") :- depends_on("mkfontscale", "xproto"), node("mkfontscale").


%----------------------------------------------------------------------------
% Package: mpfr
%----------------------------------------------------------------------------
version_declared("mpfr", "4.0.2", 0).
version_declared("mpfr", "4.0.1", 1).
version_declared("mpfr", "4.0.0", 2).
version_declared("mpfr", "3.1.6", 3).
version_declared("mpfr", "3.1.5", 4).
version_declared("mpfr", "3.1.4", 5).
version_declared("mpfr", "3.1.3", 6).
version_declared("mpfr", "3.1.2", 7).

declared_dependency("mpfr", "gmp", "build").
declared_dependency("mpfr", "gmp", "link").
node("gmp") :- depends_on("mpfr", "gmp"), node("mpfr").
declared_dependency("mpfr", "gmp", "build") :- node("mpfr"), 1 { version("mpfr", "4.0.0"); version("mpfr", "4.0.1"); version("mpfr", "4.0.2") } 1.
declared_dependency("mpfr", "gmp", "link") :- node("mpfr"), 1 { version("mpfr", "4.0.0"); version("mpfr", "4.0.1"); version("mpfr", "4.0.2") } 1.
node("gmp") :- depends_on("mpfr", "gmp"), node("mpfr"), 1 { version("mpfr", "4.0.0"); version("mpfr", "4.0.1"); version("mpfr", "4.0.2") } 1.
1 { version("gmp", "5.1.3"); version("gmp", "6.0.0a"); version("gmp", "6.1.0"); version("gmp", "6.1.1"); version("gmp", "6.1.2") } 1 :- depends_on("mpfr", "gmp"), node("mpfr"), 1 { version("mpfr", "4.0.0"); version("mpfr", "4.0.1"); version("mpfr", "4.0.2") } 1.


%----------------------------------------------------------------------------
% Package: mpich
%----------------------------------------------------------------------------
version_declared("mpich", "3.3.2", 0).
version_declared("mpich", "3.3.1", 1).
version_declared("mpich", "3.3", 2).
version_declared("mpich", "3.2.1", 3).
version_declared("mpich", "3.2", 4).
version_declared("mpich", "3.1.4", 5).
version_declared("mpich", "3.1.3", 6).
version_declared("mpich", "3.1.2", 7).
version_declared("mpich", "3.1.1", 8).
version_declared("mpich", "3.1", 9).
version_declared("mpich", "3.0.4", 10).
version_declared("mpich", "develop", 11).

variant("mpich", "device").
variant_single_value("mpich", "device").
variant_default_value("mpich", "device", "ch3").
variant_possible_value("mpich", "device", "ch3").
variant_possible_value("mpich", "device", "ch4").

variant("mpich", "hydra").
variant_single_value("mpich", "hydra").
variant_default_value("mpich", "hydra", "True").
variant_possible_value("mpich", "hydra", "False").
variant_possible_value("mpich", "hydra", "True").

variant("mpich", "netmod").
variant_single_value("mpich", "netmod").
variant_default_value("mpich", "netmod", "tcp").
variant_possible_value("mpich", "netmod", "mxm").
variant_possible_value("mpich", "netmod", "ofi").
variant_possible_value("mpich", "netmod", "tcp").
variant_possible_value("mpich", "netmod", "ucx").

variant("mpich", "pci").
variant_single_value("mpich", "pci").
variant_default_value("mpich", "pci", "False").
variant_possible_value("mpich", "pci", "False").
variant_possible_value("mpich", "pci", "True").

variant("mpich", "pmi").
variant_single_value("mpich", "pmi").
variant_default_value("mpich", "pmi", "pmi").
variant_possible_value("mpich", "pmi", "off").
variant_possible_value("mpich", "pmi", "pmi").
variant_possible_value("mpich", "pmi", "pmi2").
variant_possible_value("mpich", "pmi", "pmix").

variant("mpich", "romio").
variant_single_value("mpich", "romio").
variant_default_value("mpich", "romio", "True").
variant_possible_value("mpich", "romio", "False").
variant_possible_value("mpich", "romio", "True").

variant("mpich", "slurm").
variant_single_value("mpich", "slurm").
variant_default_value("mpich", "slurm", "False").
variant_possible_value("mpich", "slurm", "False").
variant_possible_value("mpich", "slurm", "True").

variant("mpich", "verbs").
variant_single_value("mpich", "verbs").
variant_default_value("mpich", "verbs", "False").
variant_possible_value("mpich", "verbs", "False").
variant_possible_value("mpich", "verbs", "True").

variant("mpich", "wrapperrpath").
variant_single_value("mpich", "wrapperrpath").
variant_default_value("mpich", "wrapperrpath", "True").
variant_possible_value("mpich", "wrapperrpath", "False").
variant_possible_value("mpich", "wrapperrpath", "True").

declared_dependency("mpich", "autoconf", "build") :- node("mpich"), 1 { version("mpich", "develop") } 1.
node("autoconf") :- depends_on("mpich", "autoconf"), node("mpich"), 1 { version("mpich", "develop") } 1.
1 { version("autoconf", "2.69") } 1 :- depends_on("mpich", "autoconf"), node("mpich"), 1 { version("mpich", "develop") } 1.

declared_dependency("mpich", "automake", "build") :- node("mpich"), 1 { version("mpich", "develop") } 1.
node("automake") :- depends_on("mpich", "automake"), node("mpich"), 1 { version("mpich", "develop") } 1.
1 { version("automake", "1.15"); version("automake", "1.15.1"); version("automake", "1.16.1") } 1 :- depends_on("mpich", "automake"), node("mpich"), 1 { version("mpich", "develop") } 1.

declared_dependency("mpich", "findutils", "build").
node("findutils") :- depends_on("mpich", "findutils"), node("mpich").

declared_dependency("mpich", "libfabric", "build") :- node("mpich"), variant_value("mpich", "device", "ch3"), variant_value("mpich", "netmod", "ofi").
declared_dependency("mpich", "libfabric", "link") :- node("mpich"), variant_value("mpich", "device", "ch3"), variant_value("mpich", "netmod", "ofi").
node("libfabric") :- depends_on("mpich", "libfabric"), node("mpich"), variant_value("mpich", "device", "ch3"), variant_value("mpich", "netmod", "ofi").
1 { version("libfabric", "1.4.2"); version("libfabric", "1.5.0"); version("libfabric", "1.5.3"); version("libfabric", "1.6.0"); version("libfabric", "1.6.1"); version("libfabric", "1.6.2") } 1 :- depends_on("mpich", "libfabric"), node("mpich"), variant_value("mpich", "device", "ch3"), variant_value("mpich", "netmod", "ofi").
declared_dependency("mpich", "libfabric", "build") :- node("mpich"), variant_value("mpich", "netmod", "ofi").
declared_dependency("mpich", "libfabric", "link") :- node("mpich"), variant_value("mpich", "netmod", "ofi").
node("libfabric") :- depends_on("mpich", "libfabric"), node("mpich"), variant_value("mpich", "netmod", "ofi").

declared_dependency("mpich", "libpciaccess", "build") :- node("mpich"), variant_value("mpich", "pci", "True").
declared_dependency("mpich", "libpciaccess", "link") :- node("mpich"), variant_value("mpich", "pci", "True").
node("libpciaccess") :- depends_on("mpich", "libpciaccess"), node("mpich"), variant_value("mpich", "pci", "True").

declared_dependency("mpich", "libtool", "build") :- node("mpich"), 1 { version("mpich", "develop") } 1.
node("libtool") :- depends_on("mpich", "libtool"), node("mpich"), 1 { version("mpich", "develop") } 1.
1 { version("libtool", "2.4.6"); version("libtool", "develop") } 1 :- depends_on("mpich", "libtool"), node("mpich"), 1 { version("mpich", "develop") } 1.

declared_dependency("mpich", "libxml2", "build").
declared_dependency("mpich", "libxml2", "link").
node("libxml2") :- depends_on("mpich", "libxml2"), node("mpich").

declared_dependency("mpich", "m4", "build") :- node("mpich"), 1 { version("mpich", "develop") } 1.
node("m4") :- depends_on("mpich", "m4"), node("mpich"), 1 { version("mpich", "develop") } 1.

declared_dependency("mpich", "pkgconfig", "build").
node("pkgconfig") :- depends_on("mpich", "pkgconfig"), node("mpich").

declared_dependency("mpich", "pmix", "build") :- node("mpich"), variant_value("mpich", "pmi", "pmix").
declared_dependency("mpich", "pmix", "link") :- node("mpich"), variant_value("mpich", "pmi", "pmix").
node("pmix") :- depends_on("mpich", "pmix"), node("mpich"), variant_value("mpich", "pmi", "pmix").

declared_dependency("mpich", "slurm", "build") :- node("mpich"), variant_value("mpich", "slurm", "True").
declared_dependency("mpich", "slurm", "link") :- node("mpich"), variant_value("mpich", "slurm", "True").
node("slurm") :- depends_on("mpich", "slurm"), node("mpich"), variant_value("mpich", "slurm", "True").

declared_dependency("mpich", "ucx", "build") :- node("mpich"), variant_value("mpich", "netmod", "ucx").
declared_dependency("mpich", "ucx", "link") :- node("mpich"), variant_value("mpich", "netmod", "ucx").
node("ucx") :- depends_on("mpich", "ucx"), node("mpich"), variant_value("mpich", "netmod", "ucx").


%----------------------------------------------------------------------------
% Package: mpilander
%----------------------------------------------------------------------------
version_declared("mpilander", "develop", 0).

variant("mpilander", "build_type").
variant_single_value("mpilander", "build_type").
variant_default_value("mpilander", "build_type", "RelWithDebInfo").
variant_possible_value("mpilander", "build_type", "Debug").
variant_possible_value("mpilander", "build_type", "MinSizeRel").
variant_possible_value("mpilander", "build_type", "RelWithDebInfo").
variant_possible_value("mpilander", "build_type", "Release").

declared_dependency("mpilander", "cmake", "build").
node("cmake") :- depends_on("mpilander", "cmake"), node("mpilander").
1 { version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1 :- depends_on("mpilander", "cmake"), node("mpilander").


%----------------------------------------------------------------------------
% Package: mpt
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: msgpack-c
%----------------------------------------------------------------------------
version_declared("msgpack-c", "3.0.1", 0).
version_declared("msgpack-c", "1.4.1", 1).

variant("msgpack-c", "build_type").
variant_single_value("msgpack-c", "build_type").
variant_default_value("msgpack-c", "build_type", "RelWithDebInfo").
variant_possible_value("msgpack-c", "build_type", "Debug").
variant_possible_value("msgpack-c", "build_type", "MinSizeRel").
variant_possible_value("msgpack-c", "build_type", "RelWithDebInfo").
variant_possible_value("msgpack-c", "build_type", "Release").

declared_dependency("msgpack-c", "cmake", "build").
node("cmake") :- depends_on("msgpack-c", "cmake"), node("msgpack-c").
1 { version("cmake", "3.0.2"); version("cmake", "3.1.0"); version("cmake", "3.3.1"); version("cmake", "3.4.0"); version("cmake", "3.4.3"); version("cmake", "3.5.0"); version("cmake", "3.5.1"); version("cmake", "3.5.2"); version("cmake", "3.6.0"); version("cmake", "3.6.1"); version("cmake", "3.7.1"); version("cmake", "3.7.2"); version("cmake", "3.8.0"); version("cmake", "3.8.1"); version("cmake", "3.8.2"); version("cmake", "3.9.0"); version("cmake", "3.9.4"); version("cmake", "3.9.6"); version("cmake", "3.10.0"); version("cmake", "3.10.1"); version("cmake", "3.10.2"); version("cmake", "3.10.3"); version("cmake", "3.11.0"); version("cmake", "3.11.1"); version("cmake", "3.11.2"); version("cmake", "3.11.3"); version("cmake", "3.11.4"); version("cmake", "3.12.0"); version("cmake", "3.12.1"); version("cmake", "3.12.2"); version("cmake", "3.12.3"); version("cmake", "3.12.4"); version("cmake", "3.13.0"); version("cmake", "3.13.1"); version("cmake", "3.13.2"); version("cmake", "3.13.3"); version("cmake", "3.13.4"); version("cmake", "3.14.0"); version("cmake", "3.14.1"); version("cmake", "3.14.2"); version("cmake", "3.14.3"); version("cmake", "3.14.4"); version("cmake", "3.14.5"); version("cmake", "3.15.0"); version("cmake", "3.15.1"); version("cmake", "3.15.2"); version("cmake", "3.15.3"); version("cmake", "3.15.4"); version("cmake", "3.15.5"); version("cmake", "3.16.0"); version("cmake", "3.16.1"); version("cmake", "3.16.2") } 1 :- depends_on("msgpack-c", "cmake"), node("msgpack-c").

declared_dependency("msgpack-c", "googletest", "test").
node("googletest") :- depends_on("msgpack-c", "googletest"), node("msgpack-c").


%----------------------------------------------------------------------------
% Package: munge
%----------------------------------------------------------------------------
version_declared("munge", "0.5.13", 0).
version_declared("munge", "0.5.12", 1).
version_declared("munge", "0.5.11", 2).

declared_dependency("munge", "libgcrypt", "build").
declared_dependency("munge", "libgcrypt", "link").
node("libgcrypt") :- depends_on("munge", "libgcrypt"), node("munge").

declared_dependency("munge", "openssl", "build").
declared_dependency("munge", "openssl", "link").
node("openssl") :- depends_on("munge", "openssl"), node("munge").


%----------------------------------------------------------------------------
% Package: mvapich2
%----------------------------------------------------------------------------
version_declared("mvapich2", "2.3.2", 0).
version_declared("mvapich2", "2.3.1", 1).
version_declared("mvapich2", "2.3rc2", 2).
version_declared("mvapich2", "2.3rc1", 3).
version_declared("mvapich2", "2.3a", 4).
version_declared("mvapich2", "2.3", 5).
version_declared("mvapich2", "2.2", 6).
version_declared("mvapich2", "2.1", 7).

variant("mvapich2", "alloca").
variant_single_value("mvapich2", "alloca").
variant_default_value("mvapich2", "alloca", "False").
variant_possible_value("mvapich2", "alloca", "False").
variant_possible_value("mvapich2", "alloca", "True").

variant("mvapich2", "ch3_rank_bits").
variant_single_value("mvapich2", "ch3_rank_bits").
variant_default_value("mvapich2", "ch3_rank_bits", "32").
variant_possible_value("mvapich2", "ch3_rank_bits", "16").
variant_possible_value("mvapich2", "ch3_rank_bits", "32").

variant("mvapich2", "cuda").
variant_single_value("mvapich2", "cuda").
variant_default_value("mvapich2", "cuda", "False").
variant_possible_value("mvapich2", "cuda", "False").
variant_possible_value("mvapich2", "cuda", "True").

variant("mvapich2", "debug").
variant_single_value("mvapich2", "debug").
variant_default_value("mvapich2", "debug", "False").
variant_possible_value("mvapich2", "debug", "False").
variant_possible_value("mvapich2", "debug", "True").

variant("mvapich2", "fabrics").
variant_single_value("mvapich2", "fabrics").
variant_default_value("mvapich2", "fabrics", "mrail").
variant_possible_value("mvapich2", "fabrics", "mrail").
variant_possible_value("mvapich2", "fabrics", "nemesis").
variant_possible_value("mvapich2", "fabrics", "nemesisib").
variant_possible_value("mvapich2", "fabrics", "nemesisibtcp").
variant_possible_value("mvapich2", "fabrics", "nemesisofi").
variant_possible_value("mvapich2", "fabrics", "nemesistcpib").
variant_possible_value("mvapich2", "fabrics", "psm").
variant_possible_value("mvapich2", "fabrics", "psm2").
variant_possible_value("mvapich2", "fabrics", "sock").

variant("mvapich2", "file_systems").
not variant_single_value("mvapich2", "file_systems").
variant_default_value("mvapich2", "file_systems", "auto").
variant_possible_value("mvapich2", "file_systems", "auto").
variant_possible_value("mvapich2", "file_systems", "gpfs").
variant_possible_value("mvapich2", "file_systems", "lustre").
variant_possible_value("mvapich2", "file_systems", "nfs").
variant_possible_value("mvapich2", "file_systems", "ufs").

variant("mvapich2", "process_managers").
not variant_single_value("mvapich2", "process_managers").
variant_default_value("mvapich2", "process_managers", "auto").
variant_possible_value("mvapich2", "process_managers", "auto").
variant_possible_value("mvapich2", "process_managers", "gforker").
variant_possible_value("mvapich2", "process_managers", "hydra").
variant_possible_value("mvapich2", "process_managers", "remshell").
variant_possible_value("mvapich2", "process_managers", "slurm").

variant("mvapich2", "regcache").
variant_single_value("mvapich2", "regcache").
variant_default_value("mvapich2", "regcache", "True").
variant_possible_value("mvapich2", "regcache", "False").
variant_possible_value("mvapich2", "regcache", "True").

variant("mvapich2", "threads").
variant_single_value("mvapich2", "threads").
variant_default_value("mvapich2", "threads", "multiple").
variant_possible_value("mvapich2", "threads", "funneled").
variant_possible_value("mvapich2", "threads", "multiple").
variant_possible_value("mvapich2", "threads", "serialized").
variant_possible_value("mvapich2", "threads", "single").

variant("mvapich2", "wrapperrpath").
variant_single_value("mvapich2", "wrapperrpath").
variant_default_value("mvapich2", "wrapperrpath", "True").
variant_possible_value("mvapich2", "wrapperrpath", "False").
variant_possible_value("mvapich2", "wrapperrpath", "True").

declared_dependency("mvapich2", "bison", "build").
node("bison") :- depends_on("mvapich2", "bison"), node("mvapich2").

declared_dependency("mvapich2", "cuda", "build") :- node("mvapich2"), variant_value("mvapich2", "cuda", "True").
declared_dependency("mvapich2", "cuda", "link") :- node("mvapich2"), variant_value("mvapich2", "cuda", "True").
node("cuda") :- depends_on("mvapich2", "cuda"), node("mvapich2"), variant_value("mvapich2", "cuda", "True").

declared_dependency("mvapich2", "findutils", "build").
node("findutils") :- depends_on("mvapich2", "findutils"), node("mvapich2").

declared_dependency("mvapich2", "libfabric", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisofi").
declared_dependency("mvapich2", "libfabric", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisofi").
node("libfabric") :- depends_on("mvapich2", "libfabric"), node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisofi").

declared_dependency("mvapich2", "libxml2", "build").
declared_dependency("mvapich2", "libxml2", "link").
node("libxml2") :- depends_on("mvapich2", "libxml2"), node("mvapich2").

declared_dependency("mvapich2", "opa-psm2", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "psm2").
declared_dependency("mvapich2", "opa-psm2", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "psm2").
node("opa-psm2") :- depends_on("mvapich2", "opa-psm2"), node("mvapich2"), variant_value("mvapich2", "fabrics", "psm2").

declared_dependency("mvapich2", "pkgconfig", "build").
node("pkgconfig") :- depends_on("mvapich2", "pkgconfig"), node("mvapich2").

declared_dependency("mvapich2", "psm", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "psm").
declared_dependency("mvapich2", "psm", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "psm").
node("psm") :- depends_on("mvapich2", "psm"), node("mvapich2"), variant_value("mvapich2", "fabrics", "psm").

declared_dependency("mvapich2", "rdma-core", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "mrail").
declared_dependency("mvapich2", "rdma-core", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "mrail").
node("rdma-core") :- depends_on("mvapich2", "rdma-core"), node("mvapich2"), variant_value("mvapich2", "fabrics", "mrail").
declared_dependency("mvapich2", "rdma-core", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisib").
declared_dependency("mvapich2", "rdma-core", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisib").
node("rdma-core") :- depends_on("mvapich2", "rdma-core"), node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisib").
declared_dependency("mvapich2", "rdma-core", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisibtcp").
declared_dependency("mvapich2", "rdma-core", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisibtcp").
node("rdma-core") :- depends_on("mvapich2", "rdma-core"), node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesisibtcp").
declared_dependency("mvapich2", "rdma-core", "build") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesistcpib").
declared_dependency("mvapich2", "rdma-core", "link") :- node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesistcpib").
node("rdma-core") :- depends_on("mvapich2", "rdma-core"), node("mvapich2"), variant_value("mvapich2", "fabrics", "nemesistcpib").

declared_dependency("mvapich2", "slurm", "build") :- node("mvapich2"), variant_value("mvapich2", "process_managers", "slurm").
declared_dependency("mvapich2", "slurm", "link") :- node("mvapich2"), variant_value("mvapich2", "process_managers", "slurm").
node("slurm") :- depends_on("mvapich2", "slurm"), node("mvapich2"), variant_value("mvapich2", "process_managers", "slurm").

declared_dependency("mvapich2", "zlib", "build").
declared_dependency("mvapich2", "zlib", "link").
node("zlib") :- depends_on("mvapich2", "zlib"), node("mvapich2").


%----------------------------------------------------------------------------
% Package: nasm
%----------------------------------------------------------------------------
version_declared("nasm", "2.14.02", 0).
version_declared("nasm", "2.13.03", 1).
version_declared("nasm", "2.11.06", 2).


%----------------------------------------------------------------------------
% Package: ncurses
%----------------------------------------------------------------------------
version_declared("ncurses", "6.1", 0).
version_declared("ncurses", "6.0", 1).
version_declared("ncurses", "5.9", 2).

variant("ncurses", "symlinks").
variant_single_value("ncurses", "symlinks").
variant_default_value("ncurses", "symlinks", "False").
variant_possible_value("ncurses", "symlinks", "False").
variant_possible_value("ncurses", "symlinks", "True").

variant("ncurses", "termlib").
variant_single_value("ncurses", "termlib").
variant_default_value("ncurses", "termlib", "False").
variant_possible_value("ncurses", "termlib", "False").
variant_possible_value("ncurses", "termlib", "True").

declared_dependency("ncurses", "pkgconfig", "build").
node("pkgconfig") :- depends_on("ncurses", "pkgconfig"), node("ncurses").


%----------------------------------------------------------------------------
% Package: netlib-lapack
%----------------------------------------------------------------------------
version_declared("netlib-lapack", "3.8.0", 0).
version_declared("netlib-lapack", "3.7.1", 1).
version_declared("netlib-lapack", "3.7.0", 2).
version_declared("netlib-lapack", "3.6.1", 3).
version_declared("netlib-lapack", "3.6.0", 4).
version_declared("netlib-lapack", "3.5.0", 5).
version_declared("netlib-lapack", "3.4.2", 6).
version_declared("netlib-lapack", "3.4.1", 7).
version_declared("netlib-lapack", "3.4.0", 8).
version_declared("netlib-lapack", "3.3.1", 9).

variant("netlib-lapack", "build_type").
variant_single_value("netlib-lapack", "build_type").
variant_default_value("netlib-lapack", "build_type", "RelWithDebInfo").
variant_possible_value("netlib-lapack", "build_type", "Debug").
variant_possible_value("netlib-lapack", "build_type", "MinSizeRel").
variant_possible_value("netlib-lapack", "build_type", "RelWithDebInfo").
variant_possible_value("netlib-lapack", "build_type", "Release").

variant("netlib-lapack", "external-blas").
variant_single_value("netlib-lapack", "external-blas").
variant_default_value("netlib-lapack", "external-blas", "False").
variant_possible_value("netlib-lapack", "external-blas", "False").
variant_possible_value("netlib-lapack", "external-blas", "True").

variant("netlib-lapack", "lapacke").
variant_single_value("netlib-lapack", "lapacke").
variant_default_value("netlib-lapack", "lapacke", "True").
variant_possible_value("netlib-lapack", "lapacke", "False").
variant_possible_value("netlib-lapack", "lapacke", "True").

variant("netlib-lapack", "shared").
variant_single_value("netlib-lapack", "shared").
variant_default_value("netlib-lapack", "shared", "True").
variant_possible_value("netlib-lapack", "shared", "False").
variant_possible_value("netlib-lapack", "shared", "True").

variant("netlib-lapack", "xblas").
variant_single_value("netlib-lapack", "xblas").
variant_default_value("netlib-lapack", "xblas", "False").
variant_possible_value("netlib-lapack", "xblas", "False").
variant_possible_value("netlib-lapack", "xblas", "True").

declared_dependency("netlib-lapack", "blas", "build") :- node("netlib-lapack"), variant_value("netlib-lapack", "external-blas", "True").
declared_dependency("netlib-lapack", "blas", "link") :- node("netlib-lapack"), variant_value("netlib-lapack", "external-blas", "True").
node("blas") :- depends_on("netlib-lapack", "blas"), node("netlib-lapack"), variant_value("netlib-lapack", "external-blas", "True").

declared_dependency("netlib-lapack", "cmake", "build").
node("cmake") :- depends_on("netlib-lapack", "cmake"), node("netlib-lapack").

declared_dependency("netlib-lapack", "netlib-xblas", "build") :- node("netlib-lapack"), variant_value("netlib-lapack", "xblas", "True").
declared_dependency("netlib-lapack", "netlib-xblas", "link") :- node("netlib-lapack"), variant_value("netlib-lapack", "xblas", "True").
node("netlib-xblas") :- depends_on("netlib-lapack", "netlib-xblas"), node("netlib-lapack"), variant_value("netlib-lapack", "xblas", "True").
variant_set("netlib-xblas", "fortran", "True") :- depends_on("netlib-lapack", "netlib-xblas"), node("netlib-lapack"), variant_value("netlib-lapack", "xblas", "True").
variant_set("netlib-xblas", "plain_blas", "True") :- depends_on("netlib-lapack", "netlib-xblas"), node("netlib-lapack"), variant_value("netlib-lapack", "xblas", "True").

declared_dependency("netlib-lapack", "python", "test").
node("python") :- depends_on("netlib-lapack", "python"), node("netlib-lapack").


%----------------------------------------------------------------------------
% Package: netlib-xblas
%----------------------------------------------------------------------------
version_declared("netlib-xblas", "1.0.248", 0).

variant("netlib-xblas", "fortran").
variant_single_value("netlib-xblas", "fortran").
variant_default_value("netlib-xblas", "fortran", "True").
variant_possible_value("netlib-xblas", "fortran", "False").
variant_possible_value("netlib-xblas", "fortran", "True").

variant("netlib-xblas", "plain_blas").
variant_single_value("netlib-xblas", "plain_blas").
variant_default_value("netlib-xblas", "plain_blas", "True").
variant_possible_value("netlib-xblas", "plain_blas", "False").
variant_possible_value("netlib-xblas", "plain_blas", "True").


%----------------------------------------------------------------------------
% Package: nettle
%----------------------------------------------------------------------------
version_declared("nettle", "3.4.1", 0).
version_declared("nettle", "3.4", 1).
version_declared("nettle", "3.3", 2).
version_declared("nettle", "3.2", 3).
version_declared("nettle", "2.7.1", 4).
version_declared("nettle", "2.7", 5).

declared_dependency("nettle", "gmp", "build").
declared_dependency("nettle", "gmp", "link").
node("gmp") :- depends_on("nettle", "gmp"), node("nettle").

declared_dependency("nettle", "m4", "build").
node("m4") :- depends_on("nettle", "m4"), node("nettle").


%----------------------------------------------------------------------------
% Package: nghttp2
%----------------------------------------------------------------------------
version_declared("nghttp2", "1.26.0", 0).

declared_dependency("nghttp2", "py-cython", "build").
declared_dependency("nghttp2", "py-cython", "run").
node("py-cython") :- depends_on("nghttp2", "py-cython"), node("nghttp2").

declared_dependency("nghttp2", "py-setuptools", "build").
node("py-setuptools") :- depends_on("nghttp2", "py-setuptools"), node("nghttp2").

declared_dependency("nghttp2", "python", "build").
declared_dependency("nghttp2", "python", "run").
node("python") :- depends_on("nghttp2", "python"), node("nghttp2").


%----------------------------------------------------------------------------
% Package: ninja
%----------------------------------------------------------------------------
version_declared("ninja", "1.10.0", 0).
version_declared("ninja", "1.9.0", 1).
version_declared("ninja", "1.8.2", 2).
version_declared("ninja", "1.7.2", 3).
version_declared("ninja", "1.6.0", 4).
version_declared("ninja", "kitware", 5).

declared_dependency("ninja", "python", "build").
node("python") :- depends_on("ninja", "python"), node("ninja").


%----------------------------------------------------------------------------
% Package: numactl
%----------------------------------------------------------------------------
version_declared("numactl", "2.0.12", 0).
version_declared("numactl", "2.0.11", 1).

declared_dependency("numactl", "autoconf", "build").
node("autoconf") :- depends_on("numactl", "autoconf"), node("numactl").

declared_dependency("numactl", "automake", "build").
node("automake") :- depends_on("numactl", "automake"), node("numactl").

declared_dependency("numactl", "libtool", "build").
node("libtool") :- depends_on("numactl", "libtool"), node("numactl").

declared_dependency("numactl", "m4", "build").
node("m4") :- depends_on("numactl", "m4"), node("numactl").


%----------------------------------------------------------------------------
% Package: opa-psm2
%----------------------------------------------------------------------------
version_declared("opa-psm2", "11.2.77", 0).
version_declared("opa-psm2", "11.2.68", 1).
version_declared("opa-psm2", "10.3-37", 2).
version_declared("opa-psm2", "10.3-17", 3).
version_declared("opa-psm2", "10.3-10", 4).
version_declared("opa-psm2", "10.3-8", 5).
version_declared("opa-psm2", "10.2-260", 6).
version_declared("opa-psm2", "10.2-235", 7).
version_declared("opa-psm2", "10.2-175", 8).

variant("opa-psm2", "avx2").
variant_single_value("opa-psm2", "avx2").
variant_default_value("opa-psm2", "avx2", "True").
variant_possible_value("opa-psm2", "avx2", "False").
variant_possible_value("opa-psm2", "avx2", "True").

declared_dependency("opa-psm2", "numactl", "build").
declared_dependency("opa-psm2", "numactl", "link").
node("numactl") :- depends_on("opa-psm2", "numactl"), node("opa-psm2").


%----------------------------------------------------------------------------
% Package: openblas
%----------------------------------------------------------------------------
version_declared("openblas", "0.3.8", 0).
version_declared("openblas", "0.3.7", 1).
version_declared("openblas", "0.3.6", 2).
version_declared("openblas", "0.3.5", 3).
version_declared("openblas", "0.3.4", 4).
version_declared("openblas", "0.3.3", 5).
version_declared("openblas", "0.3.2", 6).
version_declared("openblas", "0.3.1", 7).
version_declared("openblas", "0.3.0", 8).
version_declared("openblas", "0.2.20", 9).
version_declared("openblas", "0.2.19", 10).
version_declared("openblas", "0.2.18", 11).
version_declared("openblas", "0.2.17", 12).
version_declared("openblas", "0.2.16", 13).
version_declared("openblas", "0.2.15", 14).
version_declared("openblas", "develop", 15).

variant("openblas", "ilp64").
variant_single_value("openblas", "ilp64").
variant_default_value("openblas", "ilp64", "False").
variant_possible_value("openblas", "ilp64", "False").
variant_possible_value("openblas", "ilp64", "True").

variant("openblas", "pic").
variant_single_value("openblas", "pic").
variant_default_value("openblas", "pic", "True").
variant_possible_value("openblas", "pic", "False").
variant_possible_value("openblas", "pic", "True").

variant("openblas", "shared").
variant_single_value("openblas", "shared").
variant_default_value("openblas", "shared", "True").
variant_possible_value("openblas", "shared", "False").
variant_possible_value("openblas", "shared", "True").

variant("openblas", "threads").
variant_single_value("openblas", "threads").
variant_default_value("openblas", "threads", "none").
variant_possible_value("openblas", "threads", "none").
variant_possible_value("openblas", "threads", "openmp").
variant_possible_value("openblas", "threads", "pthreads").


%----------------------------------------------------------------------------
% Package: opengl
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: openjdk
%----------------------------------------------------------------------------
version_declared("openjdk", "11.0.2", 0).
version_declared("openjdk", "11.0.1", 1).
version_declared("openjdk", "1.8.0_202-b08", 2).
version_declared("openjdk", "1.8.0_40-b25", 3).


%----------------------------------------------------------------------------
% Package: openmpi
%----------------------------------------------------------------------------
version_declared("openmpi", "3.1.5", 0).
version_declared("openmpi", "4.0.2", 1).
version_declared("openmpi", "4.0.1", 2).
version_declared("openmpi", "4.0.0", 3).
version_declared("openmpi", "3.1.4", 4).
version_declared("openmpi", "3.1.3", 5).
version_declared("openmpi", "3.1.2", 6).
version_declared("openmpi", "3.1.1", 7).
version_declared("openmpi", "3.1.0", 8).
version_declared("openmpi", "3.0.5", 9).
version_declared("openmpi", "3.0.4", 10).
version_declared("openmpi", "3.0.3", 11).
version_declared("openmpi", "3.0.2", 12).
version_declared("openmpi", "3.0.1", 13).
version_declared("openmpi", "3.0.0", 14).
version_declared("openmpi", "2.1.6", 15).
version_declared("openmpi", "2.1.5", 16).
version_declared("openmpi", "2.1.4", 17).
version_declared("openmpi", "2.1.3", 18).
version_declared("openmpi", "2.1.2", 19).
version_declared("openmpi", "2.1.1", 20).
version_declared("openmpi", "2.1.0", 21).
version_declared("openmpi", "2.0.4", 22).
version_declared("openmpi", "2.0.3", 23).
version_declared("openmpi", "2.0.2", 24).
version_declared("openmpi", "2.0.1", 25).
version_declared("openmpi", "2.0.0", 26).
version_declared("openmpi", "1.10.7", 27).
version_declared("openmpi", "1.10.6", 28).
version_declared("openmpi", "1.10.5", 29).
version_declared("openmpi", "1.10.4", 30).
version_declared("openmpi", "1.10.3", 31).
version_declared("openmpi", "1.10.2", 32).
version_declared("openmpi", "1.10.1", 33).
version_declared("openmpi", "1.10.0", 34).
version_declared("openmpi", "1.8.8", 35).
version_declared("openmpi", "1.8.7", 36).
version_declared("openmpi", "1.8.6", 37).
version_declared("openmpi", "1.8.5", 38).
version_declared("openmpi", "1.8.4", 39).
version_declared("openmpi", "1.8.3", 40).
version_declared("openmpi", "1.8.2", 41).
version_declared("openmpi", "1.8.1", 42).
version_declared("openmpi", "1.8", 43).
version_declared("openmpi", "1.7.5", 44).
version_declared("openmpi", "1.7.4", 45).
version_declared("openmpi", "1.7.3", 46).
version_declared("openmpi", "1.7.2", 47).
version_declared("openmpi", "1.7.1", 48).
version_declared("openmpi", "1.7", 49).
version_declared("openmpi", "1.6.5", 50).
version_declared("openmpi", "1.6.4", 51).
version_declared("openmpi", "1.6.3", 52).
version_declared("openmpi", "1.6.2", 53).
version_declared("openmpi", "1.6.1", 54).
version_declared("openmpi", "1.6", 55).
version_declared("openmpi", "1.5.5", 56).
version_declared("openmpi", "1.5.4", 57).
version_declared("openmpi", "1.5.3", 58).
version_declared("openmpi", "1.5.2", 59).
version_declared("openmpi", "1.5.1", 60).
version_declared("openmpi", "1.5", 61).
version_declared("openmpi", "1.4.5", 62).
version_declared("openmpi", "1.4.4", 63).
version_declared("openmpi", "1.4.3", 64).
version_declared("openmpi", "1.4.2", 65).
version_declared("openmpi", "1.4.1", 66).
version_declared("openmpi", "1.4", 67).
version_declared("openmpi", "1.3.4", 68).
version_declared("openmpi", "1.3.3", 69).
version_declared("openmpi", "1.3.2", 70).
version_declared("openmpi", "1.3.1", 71).
version_declared("openmpi", "1.3", 72).
version_declared("openmpi", "1.2.9", 73).
version_declared("openmpi", "1.2.8", 74).
version_declared("openmpi", "1.2.7", 75).
version_declared("openmpi", "1.2.6", 76).
version_declared("openmpi", "1.2.5", 77).
version_declared("openmpi", "1.2.4", 78).
version_declared("openmpi", "1.2.3", 79).
version_declared("openmpi", "1.2.2", 80).
version_declared("openmpi", "1.2.1", 81).
version_declared("openmpi", "1.2", 82).
version_declared("openmpi", "1.1.5", 83).
version_declared("openmpi", "1.1.4", 84).
version_declared("openmpi", "1.1.3", 85).
version_declared("openmpi", "1.1.2", 86).
version_declared("openmpi", "1.1.1", 87).
version_declared("openmpi", "1.1", 88).
version_declared("openmpi", "1.0.2", 89).
version_declared("openmpi", "1.0.1", 90).
version_declared("openmpi", "1.0", 91).
version_declared("openmpi", "develop", 92).

variant("openmpi", "cuda").
variant_single_value("openmpi", "cuda").
variant_default_value("openmpi", "cuda", "False").
variant_possible_value("openmpi", "cuda", "False").
variant_possible_value("openmpi", "cuda", "True").

variant("openmpi", "cxx_exceptions").
variant_single_value("openmpi", "cxx_exceptions").
variant_default_value("openmpi", "cxx_exceptions", "True").
variant_possible_value("openmpi", "cxx_exceptions", "False").
variant_possible_value("openmpi", "cxx_exceptions", "True").

variant("openmpi", "fabrics").
not variant_single_value("openmpi", "fabrics").
variant_default_value("openmpi", "fabrics", "none").
variant_possible_value("openmpi", "fabrics", "auto").
variant_possible_value("openmpi", "fabrics", "libfabric").
variant_possible_value("openmpi", "fabrics", "mxm").
variant_possible_value("openmpi", "fabrics", "none").
variant_possible_value("openmpi", "fabrics", "psm").
variant_possible_value("openmpi", "fabrics", "psm2").
variant_possible_value("openmpi", "fabrics", "ucx").
variant_possible_value("openmpi", "fabrics", "verbs").

variant("openmpi", "java").
variant_single_value("openmpi", "java").
variant_default_value("openmpi", "java", "False").
variant_possible_value("openmpi", "java", "False").
variant_possible_value("openmpi", "java", "True").

variant("openmpi", "legacylaunchers").
variant_single_value("openmpi", "legacylaunchers").
variant_default_value("openmpi", "legacylaunchers", "False").
variant_possible_value("openmpi", "legacylaunchers", "False").
variant_possible_value("openmpi", "legacylaunchers", "True").

variant("openmpi", "memchecker").
variant_single_value("openmpi", "memchecker").
variant_default_value("openmpi", "memchecker", "False").
variant_possible_value("openmpi", "memchecker", "False").
variant_possible_value("openmpi", "memchecker", "True").

variant("openmpi", "pmi").
variant_single_value("openmpi", "pmi").
variant_default_value("openmpi", "pmi", "False").
variant_possible_value("openmpi", "pmi", "False").
variant_possible_value("openmpi", "pmi", "True").

variant("openmpi", "schedulers").
not variant_single_value("openmpi", "schedulers").
variant_default_value("openmpi", "schedulers", "none").
variant_possible_value("openmpi", "schedulers", "alps").
variant_possible_value("openmpi", "schedulers", "auto").
variant_possible_value("openmpi", "schedulers", "loadleveler").
variant_possible_value("openmpi", "schedulers", "lsf").
variant_possible_value("openmpi", "schedulers", "none").
variant_possible_value("openmpi", "schedulers", "sge").
variant_possible_value("openmpi", "schedulers", "slurm").
variant_possible_value("openmpi", "schedulers", "tm").

variant("openmpi", "sqlite3").
variant_single_value("openmpi", "sqlite3").
variant_default_value("openmpi", "sqlite3", "False").
variant_possible_value("openmpi", "sqlite3", "False").
variant_possible_value("openmpi", "sqlite3", "True").

variant("openmpi", "thread_multiple").
variant_single_value("openmpi", "thread_multiple").
variant_default_value("openmpi", "thread_multiple", "False").
variant_possible_value("openmpi", "thread_multiple", "False").
variant_possible_value("openmpi", "thread_multiple", "True").

variant("openmpi", "vt").
variant_single_value("openmpi", "vt").
variant_default_value("openmpi", "vt", "True").
variant_possible_value("openmpi", "vt", "False").
variant_possible_value("openmpi", "vt", "True").

declared_dependency("openmpi", "autoconf", "build") :- node("openmpi"), 1 { version("openmpi", "develop") } 1.
node("autoconf") :- depends_on("openmpi", "autoconf"), node("openmpi"), 1 { version("openmpi", "develop") } 1.

declared_dependency("openmpi", "automake", "build") :- node("openmpi"), 1 { version("openmpi", "develop") } 1.
node("automake") :- depends_on("openmpi", "automake"), node("openmpi"), 1 { version("openmpi", "develop") } 1.

declared_dependency("openmpi", "binutils", "build") :- node("openmpi"), variant_value("openmpi", "fabrics", "mxm").
declared_dependency("openmpi", "binutils", "link") :- node("openmpi"), variant_value("openmpi", "fabrics", "mxm").
node("binutils") :- depends_on("openmpi", "binutils"), node("openmpi"), variant_value("openmpi", "fabrics", "mxm").
variant_set("binutils", "libiberty", "True") :- depends_on("openmpi", "binutils"), node("openmpi"), variant_value("openmpi", "fabrics", "mxm").

declared_dependency("openmpi", "hwloc", "build").
declared_dependency("openmpi", "hwloc", "link").
node("hwloc") :- depends_on("openmpi", "hwloc"), node("openmpi").
1 { version("hwloc", "1.9"); version("hwloc", "1.11.1"); version("hwloc", "1.11.2"); version("hwloc", "1.11.3"); version("hwloc", "1.11.4"); version("hwloc", "1.11.5"); version("hwloc", "1.11.6"); version("hwloc", "1.11.7"); version("hwloc", "1.11.8"); version("hwloc", "1.11.9"); version("hwloc", "1.11.10"); version("hwloc", "1.11.11") } 1 :- depends_on("openmpi", "hwloc"), node("openmpi").
declared_dependency("openmpi", "hwloc", "build") :- node("openmpi"), variant_value("openmpi", "cuda", "True").
declared_dependency("openmpi", "hwloc", "link") :- node("openmpi"), variant_value("openmpi", "cuda", "True").
node("hwloc") :- depends_on("openmpi", "hwloc"), node("openmpi"), variant_value("openmpi", "cuda", "True").
variant_set("hwloc", "cuda", "True") :- depends_on("openmpi", "hwloc"), node("openmpi"), variant_value("openmpi", "cuda", "True").

declared_dependency("openmpi", "java", "build") :- node("openmpi"), variant_value("openmpi", "java", "True").
declared_dependency("openmpi", "java", "link") :- node("openmpi"), variant_value("openmpi", "java", "True").
node("java") :- depends_on("openmpi", "java"), node("openmpi"), variant_value("openmpi", "java", "True").

declared_dependency("openmpi", "libfabric", "build") :- node("openmpi"), variant_value("openmpi", "fabrics", "libfabric").
declared_dependency("openmpi", "libfabric", "link") :- node("openmpi"), variant_value("openmpi", "fabrics", "libfabric").
node("libfabric") :- depends_on("openmpi", "libfabric"), node("openmpi"), variant_value("openmpi", "fabrics", "libfabric").

declared_dependency("openmpi", "libtool", "build") :- node("openmpi"), 1 { version("openmpi", "develop") } 1.
node("libtool") :- depends_on("openmpi", "libtool"), node("openmpi"), 1 { version("openmpi", "develop") } 1.

declared_dependency("openmpi", "lsf", "build") :- node("openmpi"), variant_value("openmpi", "schedulers", "lsf").
declared_dependency("openmpi", "lsf", "link") :- node("openmpi"), variant_value("openmpi", "schedulers", "lsf").
node("lsf") :- depends_on("openmpi", "lsf"), node("openmpi"), variant_value("openmpi", "schedulers", "lsf").

declared_dependency("openmpi", "m4", "build") :- node("openmpi"), 1 { version("openmpi", "develop") } 1.
node("m4") :- depends_on("openmpi", "m4"), node("openmpi"), 1 { version("openmpi", "develop") } 1.

declared_dependency("openmpi", "perl", "build") :- node("openmpi"), 1 { version("openmpi", "develop") } 1.
node("perl") :- depends_on("openmpi", "perl"), node("openmpi"), 1 { version("openmpi", "develop") } 1.

declared_dependency("openmpi", "slurm", "build") :- node("openmpi"), variant_value("openmpi", "schedulers", "slurm").
declared_dependency("openmpi", "slurm", "link") :- node("openmpi"), variant_value("openmpi", "schedulers", "slurm").
node("slurm") :- depends_on("openmpi", "slurm"), node("openmpi"), variant_value("openmpi", "schedulers", "slurm").

declared_dependency("openmpi", "sqlite", "build") :- node("openmpi"), 1 { version("openmpi", "1.0"); version("openmpi", "1.0.1"); version("openmpi", "1.0.2"); version("openmpi", "1.1"); version("openmpi", "1.1.1"); version("openmpi", "1.1.2"); version("openmpi", "1.1.3"); version("openmpi", "1.1.4"); version("openmpi", "1.1.5"); version("openmpi", "1.2"); version("openmpi", "1.2.1"); version("openmpi", "1.2.2"); version("openmpi", "1.2.3"); version("openmpi", "1.2.4"); version("openmpi", "1.2.5"); version("openmpi", "1.2.6"); version("openmpi", "1.2.7"); version("openmpi", "1.2.8"); version("openmpi", "1.2.9"); version("openmpi", "1.3"); version("openmpi", "1.3.1"); version("openmpi", "1.3.2"); version("openmpi", "1.3.3"); version("openmpi", "1.3.4"); version("openmpi", "1.4"); version("openmpi", "1.4.1"); version("openmpi", "1.4.2"); version("openmpi", "1.4.3"); version("openmpi", "1.4.4"); version("openmpi", "1.4.5"); version("openmpi", "1.5"); version("openmpi", "1.5.1"); version("openmpi", "1.5.2"); version("openmpi", "1.5.3"); version("openmpi", "1.5.4"); version("openmpi", "1.5.5"); version("openmpi", "1.6"); version("openmpi", "1.6.1"); version("openmpi", "1.6.2"); version("openmpi", "1.6.3"); version("openmpi", "1.6.4"); version("openmpi", "1.6.5"); version("openmpi", "1.7"); version("openmpi", "1.7.1"); version("openmpi", "1.7.2"); version("openmpi", "1.7.3"); version("openmpi", "1.7.4"); version("openmpi", "1.7.5"); version("openmpi", "1.8"); version("openmpi", "1.8.1"); version("openmpi", "1.8.2"); version("openmpi", "1.8.3"); version("openmpi", "1.8.4"); version("openmpi", "1.8.5"); version("openmpi", "1.8.6"); version("openmpi", "1.8.7"); version("openmpi", "1.8.8"); version("openmpi", "1.10.0"); version("openmpi", "1.10.1"); version("openmpi", "1.10.2"); version("openmpi", "1.10.3"); version("openmpi", "1.10.4"); version("openmpi", "1.10.5"); version("openmpi", "1.10.6"); version("openmpi", "1.10.7") } 1, variant_value("openmpi", "sqlite3", "True").
declared_dependency("openmpi", "sqlite", "link") :- node("openmpi"), 1 { version("openmpi", "1.0"); version("openmpi", "1.0.1"); version("openmpi", "1.0.2"); version("openmpi", "1.1"); version("openmpi", "1.1.1"); version("openmpi", "1.1.2"); version("openmpi", "1.1.3"); version("openmpi", "1.1.4"); version("openmpi", "1.1.5"); version("openmpi", "1.2"); version("openmpi", "1.2.1"); version("openmpi", "1.2.2"); version("openmpi", "1.2.3"); version("openmpi", "1.2.4"); version("openmpi", "1.2.5"); version("openmpi", "1.2.6"); version("openmpi", "1.2.7"); version("openmpi", "1.2.8"); version("openmpi", "1.2.9"); version("openmpi", "1.3"); version("openmpi", "1.3.1"); version("openmpi", "1.3.2"); version("openmpi", "1.3.3"); version("openmpi", "1.3.4"); version("openmpi", "1.4"); version("openmpi", "1.4.1"); version("openmpi", "1.4.2"); version("openmpi", "1.4.3"); version("openmpi", "1.4.4"); version("openmpi", "1.4.5"); version("openmpi", "1.5"); version("openmpi", "1.5.1"); version("openmpi", "1.5.2"); version("openmpi", "1.5.3"); version("openmpi", "1.5.4"); version("openmpi", "1.5.5"); version("openmpi", "1.6"); version("openmpi", "1.6.1"); version("openmpi", "1.6.2"); version("openmpi", "1.6.3"); version("openmpi", "1.6.4"); version("openmpi", "1.6.5"); version("openmpi", "1.7"); version("openmpi", "1.7.1"); version("openmpi", "1.7.2"); version("openmpi", "1.7.3"); version("openmpi", "1.7.4"); version("openmpi", "1.7.5"); version("openmpi", "1.8"); version("openmpi", "1.8.1"); version("openmpi", "1.8.2"); version("openmpi", "1.8.3"); version("openmpi", "1.8.4"); version("openmpi", "1.8.5"); version("openmpi", "1.8.6"); version("openmpi", "1.8.7"); version("openmpi", "1.8.8"); version("openmpi", "1.10.0"); version("openmpi", "1.10.1"); version("openmpi", "1.10.2"); version("openmpi", "1.10.3"); version("openmpi", "1.10.4"); version("openmpi", "1.10.5"); version("openmpi", "1.10.6"); version("openmpi", "1.10.7") } 1, variant_value("openmpi", "sqlite3", "True").
node("sqlite") :- depends_on("openmpi", "sqlite"), node("openmpi"), 1 { version("openmpi", "1.0"); version("openmpi", "1.0.1"); version("openmpi", "1.0.2"); version("openmpi", "1.1"); version("openmpi", "1.1.1"); version("openmpi", "1.1.2"); version("openmpi", "1.1.3"); version("openmpi", "1.1.4"); version("openmpi", "1.1.5"); version("openmpi", "1.2"); version("openmpi", "1.2.1"); version("openmpi", "1.2.2"); version("openmpi", "1.2.3"); version("openmpi", "1.2.4"); version("openmpi", "1.2.5"); version("openmpi", "1.2.6"); version("openmpi", "1.2.7"); version("openmpi", "1.2.8"); version("openmpi", "1.2.9"); version("openmpi", "1.3"); version("openmpi", "1.3.1"); version("openmpi", "1.3.2"); version("openmpi", "1.3.3"); version("openmpi", "1.3.4"); version("openmpi", "1.4"); version("openmpi", "1.4.1"); version("openmpi", "1.4.2"); version("openmpi", "1.4.3"); version("openmpi", "1.4.4"); version("openmpi", "1.4.5"); version("openmpi", "1.5"); version("openmpi", "1.5.1"); version("openmpi", "1.5.2"); version("openmpi", "1.5.3"); version("openmpi", "1.5.4"); version("openmpi", "1.5.5"); version("openmpi", "1.6"); version("openmpi", "1.6.1"); version("openmpi", "1.6.2"); version("openmpi", "1.6.3"); version("openmpi", "1.6.4"); version("openmpi", "1.6.5"); version("openmpi", "1.7"); version("openmpi", "1.7.1"); version("openmpi", "1.7.2"); version("openmpi", "1.7.3"); version("openmpi", "1.7.4"); version("openmpi", "1.7.5"); version("openmpi", "1.8"); version("openmpi", "1.8.1"); version("openmpi", "1.8.2"); version("openmpi", "1.8.3"); version("openmpi", "1.8.4"); version("openmpi", "1.8.5"); version("openmpi", "1.8.6"); version("openmpi", "1.8.7"); version("openmpi", "1.8.8"); version("openmpi", "1.10.0"); version("openmpi", "1.10.1"); version("openmpi", "1.10.2"); version("openmpi", "1.10.3"); version("openmpi", "1.10.4"); version("openmpi", "1.10.5"); version("openmpi", "1.10.6"); version("openmpi", "1.10.7") } 1, variant_value("openmpi", "sqlite3", "True").

declared_dependency("openmpi", "ucx", "build") :- node("openmpi"), variant_value("openmpi", "fabrics", "ucx").
declared_dependency("openmpi", "ucx", "link") :- node("openmpi"), variant_value("openmpi", "fabrics", "ucx").
node("ucx") :- depends_on("openmpi", "ucx"), node("openmpi"), variant_value("openmpi", "fabrics", "ucx").
declared_dependency("openmpi", "ucx", "build") :- node("openmpi"), variant_value("openmpi", "fabrics", "ucx"), variant_value("openmpi", "thread_multiple", "True").
declared_dependency("openmpi", "ucx", "link") :- node("openmpi"), variant_value("openmpi", "fabrics", "ucx"), variant_value("openmpi", "thread_multiple", "True").
node("ucx") :- depends_on("openmpi", "ucx"), node("openmpi"), variant_value("openmpi", "fabrics", "ucx"), variant_value("openmpi", "thread_multiple", "True").
variant_set("ucx", "thread_multiple", "True") :- depends_on("openmpi", "ucx"), node("openmpi"), variant_value("openmpi", "fabrics", "ucx"), variant_value("openmpi", "thread_multiple", "True").
declared_dependency("openmpi", "ucx", "build") :- node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1, variant_value("openmpi", "fabrics", "ucx").
declared_dependency("openmpi", "ucx", "link") :- node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1, variant_value("openmpi", "fabrics", "ucx").
node("ucx") :- depends_on("openmpi", "ucx"), node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1, variant_value("openmpi", "fabrics", "ucx").
variant_set("ucx", "thread_multiple", "True") :- depends_on("openmpi", "ucx"), node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1, variant_value("openmpi", "fabrics", "ucx").

declared_dependency("openmpi", "valgrind", "build") :- node("openmpi"), variant_value("openmpi", "memchecker", "True").
declared_dependency("openmpi", "valgrind", "link") :- node("openmpi"), variant_value("openmpi", "memchecker", "True").
node("valgrind") :- depends_on("openmpi", "valgrind"), node("openmpi"), variant_value("openmpi", "memchecker", "True").
variant_set("valgrind", "mpi", "False") :- depends_on("openmpi", "valgrind"), node("openmpi"), variant_value("openmpi", "memchecker", "True").

declared_dependency("openmpi", "zlib", "build") :- node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1.
declared_dependency("openmpi", "zlib", "link") :- node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1.
node("zlib") :- depends_on("openmpi", "zlib"), node("openmpi"), 1 { version("openmpi", "3.0.0"); version("openmpi", "3.0.1"); version("openmpi", "3.0.2"); version("openmpi", "3.0.3"); version("openmpi", "3.0.4"); version("openmpi", "3.0.5"); version("openmpi", "3.1.0"); version("openmpi", "3.1.1"); version("openmpi", "3.1.2"); version("openmpi", "3.1.3"); version("openmpi", "3.1.4"); version("openmpi", "3.1.5"); version("openmpi", "4.0.0"); version("openmpi", "4.0.1"); version("openmpi", "4.0.2"); version("openmpi", "develop") } 1.


%----------------------------------------------------------------------------
% Package: openssl
%----------------------------------------------------------------------------
version_declared("openssl", "1.1.1d", 0).
version_declared("openssl", "1.1.1c", 1).
version_declared("openssl", "1.1.1b", 2).
version_declared("openssl", "1.1.1a", 3).
version_declared("openssl", "1.1.1", 4).
version_declared("openssl", "1.1.0l", 5).
version_declared("openssl", "1.1.0k", 6).
version_declared("openssl", "1.1.0j", 7).
version_declared("openssl", "1.1.0i", 8).
version_declared("openssl", "1.1.0g", 9).
version_declared("openssl", "1.1.0e", 10).
version_declared("openssl", "1.1.0d", 11).
version_declared("openssl", "1.1.0c", 12).
version_declared("openssl", "1.0.2t", 13).
version_declared("openssl", "1.0.2s", 14).
version_declared("openssl", "1.0.2r", 15).
version_declared("openssl", "1.0.2p", 16).
version_declared("openssl", "1.0.2o", 17).
version_declared("openssl", "1.0.2n", 18).
version_declared("openssl", "1.0.2m", 19).
version_declared("openssl", "1.0.2k", 20).
version_declared("openssl", "1.0.2j", 21).
version_declared("openssl", "1.0.2i", 22).
version_declared("openssl", "1.0.2h", 23).
version_declared("openssl", "1.0.2g", 24).
version_declared("openssl", "1.0.2f", 25).
version_declared("openssl", "1.0.2e", 26).
version_declared("openssl", "1.0.2d", 27).
version_declared("openssl", "1.0.1u", 28).
version_declared("openssl", "1.0.1t", 29).
version_declared("openssl", "1.0.1r", 30).
version_declared("openssl", "1.0.1h", 31).
version_declared("openssl", "1.0.1e", 32).

variant("openssl", "systemcerts").
variant_single_value("openssl", "systemcerts").
variant_default_value("openssl", "systemcerts", "True").
variant_possible_value("openssl", "systemcerts", "False").
variant_possible_value("openssl", "systemcerts", "True").

declared_dependency("openssl", "perl", "build").
declared_dependency("openssl", "perl", "test").
node("perl") :- depends_on("openssl", "perl"), node("openssl").

declared_dependency("openssl", "zlib", "build").
declared_dependency("openssl", "zlib", "link").
node("zlib") :- depends_on("openssl", "zlib"), node("openssl").


%----------------------------------------------------------------------------
% Package: pango
%----------------------------------------------------------------------------
version_declared("pango", "1.41.0", 0).
version_declared("pango", "1.40.3", 1).
version_declared("pango", "1.40.1", 2).
version_declared("pango", "1.36.8", 3).

variant("pango", "X").
variant_single_value("pango", "X").
variant_default_value("pango", "X", "False").
variant_possible_value("pango", "X", "False").
variant_possible_value("pango", "X", "True").

declared_dependency("pango", "cairo", "build").
declared_dependency("pango", "cairo", "link").
node("cairo") :- depends_on("pango", "cairo"), node("pango").
variant_set("cairo", "fc", "True") :- depends_on("pango", "cairo"), node("pango").
variant_set("cairo", "ft", "True") :- depends_on("pango", "cairo"), node("pango").
declared_dependency("pango", "cairo", "build") :- node("pango"), variant_value("pango", "X", "False").
declared_dependency("pango", "cairo", "link") :- node("pango"), variant_value("pango", "X", "False").
node("cairo") :- depends_on("pango", "cairo"), node("pango"), variant_value("pango", "X", "False").
variant_set("cairo", "X", "False") :- depends_on("pango", "cairo"), node("pango"), variant_value("pango", "X", "False").
declared_dependency("pango", "cairo", "build") :- node("pango"), variant_value("pango", "X", "True").
declared_dependency("pango", "cairo", "link") :- node("pango"), variant_value("pango", "X", "True").
node("cairo") :- depends_on("pango", "cairo"), node("pango"), variant_value("pango", "X", "True").
variant_set("cairo", "X", "True") :- depends_on("pango", "cairo"), node("pango"), variant_value("pango", "X", "True").

declared_dependency("pango", "glib", "build").
declared_dependency("pango", "glib", "link").
node("glib") :- depends_on("pango", "glib"), node("pango").

declared_dependency("pango", "gobject-introspection", "build").
declared_dependency("pango", "gobject-introspection", "link").
node("gobject-introspection") :- depends_on("pango", "gobject-introspection"), node("pango").

declared_dependency("pango", "harfbuzz", "build").
declared_dependency("pango", "harfbuzz", "link").
node("harfbuzz") :- depends_on("pango", "harfbuzz"), node("pango").

declared_dependency("pango", "libxft", "build") :- node("pango"), variant_value("pango", "X", "True").
declared_dependency("pango", "libxft", "link") :- node("pango"), variant_value("pango", "X", "True").
node("libxft") :- depends_on("pango", "libxft"), node("pango"), variant_value("pango", "X", "True").

declared_dependency("pango", "pkgconfig", "build").
node("pkgconfig") :- depends_on("pango", "pkgconfig"), node("pango").


%----------------------------------------------------------------------------
% Package: papi
%----------------------------------------------------------------------------
version_declared("papi", "5.7.0", 0).
version_declared("papi", "5.6.0", 1).
version_declared("papi", "5.5.1", 2).
version_declared("papi", "5.5.0", 3).
version_declared("papi", "5.4.3", 4).
version_declared("papi", "5.4.1", 5).
version_declared("papi", "5.3.0", 6).

variant("papi", "example").
variant_single_value("papi", "example").
variant_default_value("papi", "example", "True").
variant_possible_value("papi", "example", "False").
variant_possible_value("papi", "example", "True").

variant("papi", "infiniband").
variant_single_value("papi", "infiniband").
variant_default_value("papi", "infiniband", "False").
variant_possible_value("papi", "infiniband", "False").
variant_possible_value("papi", "infiniband", "True").

variant("papi", "lmsensors").
variant_single_value("papi", "lmsensors").
variant_default_value("papi", "lmsensors", "False").
variant_possible_value("papi", "lmsensors", "False").
variant_possible_value("papi", "lmsensors", "True").

variant("papi", "powercap").
variant_single_value("papi", "powercap").
variant_default_value("papi", "powercap", "False").
variant_possible_value("papi", "powercap", "False").
variant_possible_value("papi", "powercap", "True").

variant("papi", "rapl").
variant_single_value("papi", "rapl").
variant_default_value("papi", "rapl", "False").
variant_possible_value("papi", "rapl", "False").
variant_possible_value("papi", "rapl", "True").

declared_dependency("papi", "lm-sensors", "build") :- node("papi"), variant_value("papi", "lmsensors", "True").
declared_dependency("papi", "lm-sensors", "link") :- node("papi"), variant_value("papi", "lmsensors", "True").
node("lm-sensors") :- depends_on("papi", "lm-sensors"), node("papi"), variant_value("papi", "lmsensors", "True").


%----------------------------------------------------------------------------
% Package: pcre
%----------------------------------------------------------------------------
version_declared("pcre", "8.42", 0).
version_declared("pcre", "8.41", 1).
version_declared("pcre", "8.40", 2).
version_declared("pcre", "8.39", 3).
version_declared("pcre", "8.38", 4).

variant("pcre", "jit").
variant_single_value("pcre", "jit").
variant_default_value("pcre", "jit", "False").
variant_possible_value("pcre", "jit", "False").
variant_possible_value("pcre", "jit", "True").

variant("pcre", "multibyte").
variant_single_value("pcre", "multibyte").
variant_default_value("pcre", "multibyte", "True").
variant_possible_value("pcre", "multibyte", "False").
variant_possible_value("pcre", "multibyte", "True").

variant("pcre", "utf").
variant_single_value("pcre", "utf").
variant_default_value("pcre", "utf", "True").
variant_possible_value("pcre", "utf", "False").
variant_possible_value("pcre", "utf", "True").


%----------------------------------------------------------------------------
% Package: pcre2
%----------------------------------------------------------------------------
version_declared("pcre2", "10.31", 0).
version_declared("pcre2", "10.20", 1).

variant("pcre2", "multibyte").
variant_single_value("pcre2", "multibyte").
variant_default_value("pcre2", "multibyte", "True").
variant_possible_value("pcre2", "multibyte", "False").
variant_possible_value("pcre2", "multibyte", "True").


%----------------------------------------------------------------------------
% Package: perl
%----------------------------------------------------------------------------
version_declared("perl", "5.30.1", 0).
version_declared("perl", "5.31.7", 1).
version_declared("perl", "5.31.4", 2).
version_declared("perl", "5.30.0", 3).
version_declared("perl", "5.28.0", 4).
version_declared("perl", "5.26.2", 5).
version_declared("perl", "5.24.1", 6).
version_declared("perl", "5.22.4", 7).
version_declared("perl", "5.22.3", 8).
version_declared("perl", "5.22.2", 9).
version_declared("perl", "5.22.1", 10).
version_declared("perl", "5.22.0", 11).
version_declared("perl", "5.20.3", 12).
version_declared("perl", "5.18.4", 13).
version_declared("perl", "5.16.3", 14).

variant("perl", "cpanm").
variant_single_value("perl", "cpanm").
variant_default_value("perl", "cpanm", "True").
variant_possible_value("perl", "cpanm", "False").
variant_possible_value("perl", "cpanm", "True").

variant("perl", "shared").
variant_single_value("perl", "shared").
variant_default_value("perl", "shared", "True").
variant_possible_value("perl", "shared", "False").
variant_possible_value("perl", "shared", "True").

variant("perl", "threads").
variant_single_value("perl", "threads").
variant_default_value("perl", "threads", "True").
variant_possible_value("perl", "threads", "False").
variant_possible_value("perl", "threads", "True").

declared_dependency("perl", "gdbm", "build").
declared_dependency("perl", "gdbm", "link").
node("gdbm") :- depends_on("perl", "gdbm"), node("perl").


%----------------------------------------------------------------------------
% Package: perl-data-dumper
%----------------------------------------------------------------------------
version_declared("perl-data-dumper", "2.173", 0).

declared_dependency("perl-data-dumper", "perl", "build").
declared_dependency("perl-data-dumper", "perl", "link").
declared_dependency("perl-data-dumper", "perl", "run").
node("perl") :- depends_on("perl-data-dumper", "perl"), node("perl-data-dumper").


%----------------------------------------------------------------------------
% Package: perl-encode-locale
%----------------------------------------------------------------------------
version_declared("perl-encode-locale", "1.05", 0).

declared_dependency("perl-encode-locale", "perl", "build").
declared_dependency("perl-encode-locale", "perl", "link").
declared_dependency("perl-encode-locale", "perl", "run").
node("perl") :- depends_on("perl-encode-locale", "perl"), node("perl-encode-locale").


%----------------------------------------------------------------------------
% Package: perl-extutils-config
%----------------------------------------------------------------------------
version_declared("perl-extutils-config", "0.008", 0).

declared_dependency("perl-extutils-config", "perl", "build").
declared_dependency("perl-extutils-config", "perl", "link").
declared_dependency("perl-extutils-config", "perl", "run").
node("perl") :- depends_on("perl-extutils-config", "perl"), node("perl-extutils-config").


%----------------------------------------------------------------------------
% Package: perl-extutils-helpers
%----------------------------------------------------------------------------
version_declared("perl-extutils-helpers", "0.026", 0).

declared_dependency("perl-extutils-helpers", "perl", "build").
declared_dependency("perl-extutils-helpers", "perl", "link").
declared_dependency("perl-extutils-helpers", "perl", "run").
node("perl") :- depends_on("perl-extutils-helpers", "perl"), node("perl-extutils-helpers").


%----------------------------------------------------------------------------
% Package: perl-extutils-installpaths
%----------------------------------------------------------------------------
version_declared("perl-extutils-installpaths", "0.012", 0).

declared_dependency("perl-extutils-installpaths", "perl", "build").
declared_dependency("perl-extutils-installpaths", "perl", "link").
declared_dependency("perl-extutils-installpaths", "perl", "run").
node("perl") :- depends_on("perl-extutils-installpaths", "perl"), node("perl-extutils-installpaths").


%----------------------------------------------------------------------------
% Package: perl-file-listing
%----------------------------------------------------------------------------
version_declared("perl-file-listing", "6.04", 0).

declared_dependency("perl-file-listing", "perl", "build").
declared_dependency("perl-file-listing", "perl", "link").
declared_dependency("perl-file-listing", "perl", "run").
node("perl") :- depends_on("perl-file-listing", "perl"), node("perl-file-listing").

declared_dependency("perl-file-listing", "perl-http-date", "build").
declared_dependency("perl-file-listing", "perl-http-date", "run").
node("perl-http-date") :- depends_on("perl-file-listing", "perl-http-date"), node("perl-file-listing").


%----------------------------------------------------------------------------
% Package: perl-html-parser
%----------------------------------------------------------------------------
version_declared("perl-html-parser", "3.72", 0).

declared_dependency("perl-html-parser", "perl", "build").
declared_dependency("perl-html-parser", "perl", "link").
declared_dependency("perl-html-parser", "perl", "run").
node("perl") :- depends_on("perl-html-parser", "perl"), node("perl-html-parser").

declared_dependency("perl-html-parser", "perl-html-tagset", "build").
declared_dependency("perl-html-parser", "perl-html-tagset", "run").
node("perl-html-tagset") :- depends_on("perl-html-parser", "perl-html-tagset"), node("perl-html-parser").


%----------------------------------------------------------------------------
% Package: perl-html-tagset
%----------------------------------------------------------------------------
version_declared("perl-html-tagset", "3.20", 0).

declared_dependency("perl-html-tagset", "perl", "build").
declared_dependency("perl-html-tagset", "perl", "link").
declared_dependency("perl-html-tagset", "perl", "run").
node("perl") :- depends_on("perl-html-tagset", "perl"), node("perl-html-tagset").


%----------------------------------------------------------------------------
% Package: perl-http-cookies
%----------------------------------------------------------------------------
version_declared("perl-http-cookies", "6.04", 0).

declared_dependency("perl-http-cookies", "perl", "build").
declared_dependency("perl-http-cookies", "perl", "link").
declared_dependency("perl-http-cookies", "perl", "run").
node("perl") :- depends_on("perl-http-cookies", "perl"), node("perl-http-cookies").

declared_dependency("perl-http-cookies", "perl-http-message", "build").
declared_dependency("perl-http-cookies", "perl-http-message", "run").
node("perl-http-message") :- depends_on("perl-http-cookies", "perl-http-message"), node("perl-http-cookies").

declared_dependency("perl-http-cookies", "perl-uri", "build").
declared_dependency("perl-http-cookies", "perl-uri", "run").
node("perl-uri") :- depends_on("perl-http-cookies", "perl-uri"), node("perl-http-cookies").


%----------------------------------------------------------------------------
% Package: perl-http-daemon
%----------------------------------------------------------------------------
version_declared("perl-http-daemon", "6.01", 0).

declared_dependency("perl-http-daemon", "perl", "build").
declared_dependency("perl-http-daemon", "perl", "link").
declared_dependency("perl-http-daemon", "perl", "run").
node("perl") :- depends_on("perl-http-daemon", "perl"), node("perl-http-daemon").

declared_dependency("perl-http-daemon", "perl-http-date", "build").
declared_dependency("perl-http-daemon", "perl-http-date", "run").
node("perl-http-date") :- depends_on("perl-http-daemon", "perl-http-date"), node("perl-http-daemon").

declared_dependency("perl-http-daemon", "perl-http-message", "build").
declared_dependency("perl-http-daemon", "perl-http-message", "run").
node("perl-http-message") :- depends_on("perl-http-daemon", "perl-http-message"), node("perl-http-daemon").

declared_dependency("perl-http-daemon", "perl-lwp-mediatypes", "build").
declared_dependency("perl-http-daemon", "perl-lwp-mediatypes", "run").
node("perl-lwp-mediatypes") :- depends_on("perl-http-daemon", "perl-lwp-mediatypes"), node("perl-http-daemon").

declared_dependency("perl-http-daemon", "perl-module-build-tiny", "build").
node("perl-module-build-tiny") :- depends_on("perl-http-daemon", "perl-module-build-tiny"), node("perl-http-daemon").


%----------------------------------------------------------------------------
% Package: perl-http-date
%----------------------------------------------------------------------------
version_declared("perl-http-date", "6.02", 0).

declared_dependency("perl-http-date", "perl", "build").
declared_dependency("perl-http-date", "perl", "link").
declared_dependency("perl-http-date", "perl", "run").
node("perl") :- depends_on("perl-http-date", "perl"), node("perl-http-date").


%----------------------------------------------------------------------------
% Package: perl-http-message
%----------------------------------------------------------------------------
version_declared("perl-http-message", "6.13", 0).

declared_dependency("perl-http-message", "perl", "build").
declared_dependency("perl-http-message", "perl", "link").
declared_dependency("perl-http-message", "perl", "run").
node("perl") :- depends_on("perl-http-message", "perl"), node("perl-http-message").

declared_dependency("perl-http-message", "perl-encode-locale", "build").
declared_dependency("perl-http-message", "perl-encode-locale", "run").
node("perl-encode-locale") :- depends_on("perl-http-message", "perl-encode-locale"), node("perl-http-message").

declared_dependency("perl-http-message", "perl-http-date", "build").
declared_dependency("perl-http-message", "perl-http-date", "run").
node("perl-http-date") :- depends_on("perl-http-message", "perl-http-date"), node("perl-http-message").

declared_dependency("perl-http-message", "perl-io-html", "build").
declared_dependency("perl-http-message", "perl-io-html", "run").
node("perl-io-html") :- depends_on("perl-http-message", "perl-io-html"), node("perl-http-message").

declared_dependency("perl-http-message", "perl-lwp-mediatypes", "build").
declared_dependency("perl-http-message", "perl-lwp-mediatypes", "run").
node("perl-lwp-mediatypes") :- depends_on("perl-http-message", "perl-lwp-mediatypes"), node("perl-http-message").

declared_dependency("perl-http-message", "perl-try-tiny", "build").
declared_dependency("perl-http-message", "perl-try-tiny", "run").
node("perl-try-tiny") :- depends_on("perl-http-message", "perl-try-tiny"), node("perl-http-message").

declared_dependency("perl-http-message", "perl-uri", "build").
declared_dependency("perl-http-message", "perl-uri", "run").
node("perl-uri") :- depends_on("perl-http-message", "perl-uri"), node("perl-http-message").


%----------------------------------------------------------------------------
% Package: perl-http-negotiate
%----------------------------------------------------------------------------
version_declared("perl-http-negotiate", "6.01", 0).

declared_dependency("perl-http-negotiate", "perl", "build").
declared_dependency("perl-http-negotiate", "perl", "link").
declared_dependency("perl-http-negotiate", "perl", "run").
node("perl") :- depends_on("perl-http-negotiate", "perl"), node("perl-http-negotiate").

declared_dependency("perl-http-negotiate", "perl-http-message", "build").
declared_dependency("perl-http-negotiate", "perl-http-message", "run").
node("perl-http-message") :- depends_on("perl-http-negotiate", "perl-http-message"), node("perl-http-negotiate").


%----------------------------------------------------------------------------
% Package: perl-io-html
%----------------------------------------------------------------------------
version_declared("perl-io-html", "1.001", 0).

declared_dependency("perl-io-html", "perl", "build").
declared_dependency("perl-io-html", "perl", "link").
declared_dependency("perl-io-html", "perl", "run").
node("perl") :- depends_on("perl-io-html", "perl"), node("perl-io-html").


%----------------------------------------------------------------------------
% Package: perl-libwww-perl
%----------------------------------------------------------------------------
version_declared("perl-libwww-perl", "6.33", 0).
version_declared("perl-libwww-perl", "6.29", 1).

declared_dependency("perl-libwww-perl", "perl", "build").
declared_dependency("perl-libwww-perl", "perl", "link").
declared_dependency("perl-libwww-perl", "perl", "run").
node("perl") :- depends_on("perl-libwww-perl", "perl"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-encode-locale", "build").
declared_dependency("perl-libwww-perl", "perl-encode-locale", "run").
node("perl-encode-locale") :- depends_on("perl-libwww-perl", "perl-encode-locale"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-file-listing", "build").
declared_dependency("perl-libwww-perl", "perl-file-listing", "run").
node("perl-file-listing") :- depends_on("perl-libwww-perl", "perl-file-listing"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-html-parser", "build").
declared_dependency("perl-libwww-perl", "perl-html-parser", "run").
node("perl-html-parser") :- depends_on("perl-libwww-perl", "perl-html-parser"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-http-cookies", "build").
declared_dependency("perl-libwww-perl", "perl-http-cookies", "run").
node("perl-http-cookies") :- depends_on("perl-libwww-perl", "perl-http-cookies"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-http-daemon", "build").
declared_dependency("perl-libwww-perl", "perl-http-daemon", "run").
node("perl-http-daemon") :- depends_on("perl-libwww-perl", "perl-http-daemon"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-http-date", "build").
declared_dependency("perl-libwww-perl", "perl-http-date", "run").
node("perl-http-date") :- depends_on("perl-libwww-perl", "perl-http-date"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-http-message", "build").
declared_dependency("perl-libwww-perl", "perl-http-message", "run").
node("perl-http-message") :- depends_on("perl-libwww-perl", "perl-http-message"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-http-negotiate", "build").
declared_dependency("perl-libwww-perl", "perl-http-negotiate", "run").
node("perl-http-negotiate") :- depends_on("perl-libwww-perl", "perl-http-negotiate"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-lwp-mediatypes", "build").
declared_dependency("perl-libwww-perl", "perl-lwp-mediatypes", "run").
node("perl-lwp-mediatypes") :- depends_on("perl-libwww-perl", "perl-lwp-mediatypes"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-net-http", "build").
declared_dependency("perl-libwww-perl", "perl-net-http", "run").
node("perl-net-http") :- depends_on("perl-libwww-perl", "perl-net-http"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-try-tiny", "build").
declared_dependency("perl-libwww-perl", "perl-try-tiny", "run").
node("perl-try-tiny") :- depends_on("perl-libwww-perl", "perl-try-tiny"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-uri", "build").
declared_dependency("perl-libwww-perl", "perl-uri", "run").
node("perl-uri") :- depends_on("perl-libwww-perl", "perl-uri"), node("perl-libwww-perl").

declared_dependency("perl-libwww-perl", "perl-www-robotrules", "build").
declared_dependency("perl-libwww-perl", "perl-www-robotrules", "run").
node("perl-www-robotrules") :- depends_on("perl-libwww-perl", "perl-www-robotrules"), node("perl-libwww-perl").


%----------------------------------------------------------------------------
% Package: perl-lwp-mediatypes
%----------------------------------------------------------------------------
version_declared("perl-lwp-mediatypes", "6.02", 0).

declared_dependency("perl-lwp-mediatypes", "perl", "build").
declared_dependency("perl-lwp-mediatypes", "perl", "link").
declared_dependency("perl-lwp-mediatypes", "perl", "run").
node("perl") :- depends_on("perl-lwp-mediatypes", "perl"), node("perl-lwp-mediatypes").


%----------------------------------------------------------------------------
% Package: perl-module-build
%----------------------------------------------------------------------------
version_declared("perl-module-build", "0.4224", 0).
version_declared("perl-module-build", "0.4220", 1).

declared_dependency("perl-module-build", "perl", "build").
declared_dependency("perl-module-build", "perl", "link").
declared_dependency("perl-module-build", "perl", "run").
node("perl") :- depends_on("perl-module-build", "perl"), node("perl-module-build").


%----------------------------------------------------------------------------
% Package: perl-module-build-tiny
%----------------------------------------------------------------------------
version_declared("perl-module-build-tiny", "0.039", 0).

declared_dependency("perl-module-build-tiny", "perl", "build").
declared_dependency("perl-module-build-tiny", "perl", "link").
declared_dependency("perl-module-build-tiny", "perl", "run").
node("perl") :- depends_on("perl-module-build-tiny", "perl"), node("perl-module-build-tiny").

declared_dependency("perl-module-build-tiny", "perl-extutils-config", "build").
declared_dependency("perl-module-build-tiny", "perl-extutils-config", "run").
node("perl-extutils-config") :- depends_on("perl-module-build-tiny", "perl-extutils-config"), node("perl-module-build-tiny").

declared_dependency("perl-module-build-tiny", "perl-extutils-helpers", "build").
declared_dependency("perl-module-build-tiny", "perl-extutils-helpers", "run").
node("perl-extutils-helpers") :- depends_on("perl-module-build-tiny", "perl-extutils-helpers"), node("perl-module-build-tiny").

declared_dependency("perl-module-build-tiny", "perl-extutils-installpaths", "build").
declared_dependency("perl-module-build-tiny", "perl-extutils-installpaths", "run").
node("perl-extutils-installpaths") :- depends_on("perl-module-build-tiny", "perl-extutils-installpaths"), node("perl-module-build-tiny").

declared_dependency("perl-module-build-tiny", "perl-module-build", "build").
node("perl-module-build") :- depends_on("perl-module-build-tiny", "perl-module-build"), node("perl-module-build-tiny").


%----------------------------------------------------------------------------
% Package: perl-net-http
%----------------------------------------------------------------------------
version_declared("perl-net-http", "6.17", 0).

declared_dependency("perl-net-http", "perl", "build").
declared_dependency("perl-net-http", "perl", "link").
declared_dependency("perl-net-http", "perl", "run").
node("perl") :- depends_on("perl-net-http", "perl"), node("perl-net-http").

declared_dependency("perl-net-http", "perl-uri", "build").
declared_dependency("perl-net-http", "perl-uri", "run").
node("perl-uri") :- depends_on("perl-net-http", "perl-uri"), node("perl-net-http").


%----------------------------------------------------------------------------
% Package: perl-test-needs
%----------------------------------------------------------------------------
version_declared("perl-test-needs", "0.002005", 0).

declared_dependency("perl-test-needs", "perl", "build").
declared_dependency("perl-test-needs", "perl", "link").
declared_dependency("perl-test-needs", "perl", "run").
node("perl") :- depends_on("perl-test-needs", "perl"), node("perl-test-needs").


%----------------------------------------------------------------------------
% Package: perl-try-tiny
%----------------------------------------------------------------------------
version_declared("perl-try-tiny", "0.28", 0).

declared_dependency("perl-try-tiny", "perl", "build").
declared_dependency("perl-try-tiny", "perl", "link").
declared_dependency("perl-try-tiny", "perl", "run").
node("perl") :- depends_on("perl-try-tiny", "perl"), node("perl-try-tiny").


%----------------------------------------------------------------------------
% Package: perl-uri
%----------------------------------------------------------------------------
version_declared("perl-uri", "1.72", 0).
version_declared("perl-uri", "1.71", 1).

declared_dependency("perl-uri", "perl", "build").
declared_dependency("perl-uri", "perl", "link").
declared_dependency("perl-uri", "perl", "run").
node("perl") :- depends_on("perl-uri", "perl"), node("perl-uri").

declared_dependency("perl-uri", "perl-test-needs", "build").
declared_dependency("perl-uri", "perl-test-needs", "test").
node("perl-test-needs") :- depends_on("perl-uri", "perl-test-needs"), node("perl-uri").


%----------------------------------------------------------------------------
% Package: perl-www-robotrules
%----------------------------------------------------------------------------
version_declared("perl-www-robotrules", "6.02", 0).

declared_dependency("perl-www-robotrules", "perl", "build").
declared_dependency("perl-www-robotrules", "perl", "link").
declared_dependency("perl-www-robotrules", "perl", "run").
node("perl") :- depends_on("perl-www-robotrules", "perl"), node("perl-www-robotrules").

declared_dependency("perl-www-robotrules", "perl-uri", "build").
declared_dependency("perl-www-robotrules", "perl-uri", "run").
node("perl-uri") :- depends_on("perl-www-robotrules", "perl-uri"), node("perl-www-robotrules").


%----------------------------------------------------------------------------
% Package: perl-xml-parser
%----------------------------------------------------------------------------
version_declared("perl-xml-parser", "2.44", 0).

declared_dependency("perl-xml-parser", "expat", "build").
declared_dependency("perl-xml-parser", "expat", "link").
node("expat") :- depends_on("perl-xml-parser", "expat"), node("perl-xml-parser").

declared_dependency("perl-xml-parser", "perl", "build").
declared_dependency("perl-xml-parser", "perl", "link").
declared_dependency("perl-xml-parser", "perl", "run").
node("perl") :- depends_on("perl-xml-parser", "perl"), node("perl-xml-parser").

declared_dependency("perl-xml-parser", "perl-libwww-perl", "build").
declared_dependency("perl-xml-parser", "perl-libwww-perl", "run").
node("perl-libwww-perl") :- depends_on("perl-xml-parser", "perl-libwww-perl"), node("perl-xml-parser").


%----------------------------------------------------------------------------
% Package: pixman
%----------------------------------------------------------------------------
version_declared("pixman", "0.38.0", 0).
version_declared("pixman", "0.34.0", 1).
version_declared("pixman", "0.32.6", 2).

declared_dependency("pixman", "libpng", "build").
declared_dependency("pixman", "libpng", "link").
node("libpng") :- depends_on("pixman", "libpng"), node("pixman").

declared_dependency("pixman", "pkgconfig", "build").
node("pkgconfig") :- depends_on("pixman", "pkgconfig"), node("pixman").


%----------------------------------------------------------------------------
% Package: pkg-config
%----------------------------------------------------------------------------
version_declared("pkg-config", "0.29.2", 0).
version_declared("pkg-config", "0.29.1", 1).
version_declared("pkg-config", "0.28", 2).

variant("pkg-config", "internal_glib").
variant_single_value("pkg-config", "internal_glib").
variant_default_value("pkg-config", "internal_glib", "True").
variant_possible_value("pkg-config", "internal_glib", "False").
variant_possible_value("pkg-config", "internal_glib", "True").


%----------------------------------------------------------------------------
% Package: pkgconf
%----------------------------------------------------------------------------
version_declared("pkgconf", "1.6.3", 0).
version_declared("pkgconf", "1.6.1", 1).
version_declared("pkgconf", "1.6.0", 2).
version_declared("pkgconf", "1.5.4", 3).
version_declared("pkgconf", "1.4.2", 4).
version_declared("pkgconf", "1.4.0", 5).
version_declared("pkgconf", "1.3.10", 6).
version_declared("pkgconf", "1.3.8", 7).


%----------------------------------------------------------------------------
% Package: pmix
%----------------------------------------------------------------------------
version_declared("pmix", "3.1.3", 0).
version_declared("pmix", "3.1.2", 1).
version_declared("pmix", "3.0.2", 2).
version_declared("pmix", "3.0.1", 3).
version_declared("pmix", "3.0.0", 4).
version_declared("pmix", "2.2.2", 5).
version_declared("pmix", "2.1.4", 6).
version_declared("pmix", "2.1.3", 7).
version_declared("pmix", "2.1.2", 8).
version_declared("pmix", "2.0.1", 9).
version_declared("pmix", "1.2.5", 10).

declared_dependency("pmix", "hwloc", "build") :- node("pmix"), 1 { version("pmix", "3.0.0"); version("pmix", "3.0.1"); version("pmix", "3.0.2"); version("pmix", "3.1.2"); version("pmix", "3.1.3") } 1.
declared_dependency("pmix", "hwloc", "link") :- node("pmix"), 1 { version("pmix", "3.0.0"); version("pmix", "3.0.1"); version("pmix", "3.0.2"); version("pmix", "3.1.2"); version("pmix", "3.1.3") } 1.
node("hwloc") :- depends_on("pmix", "hwloc"), node("pmix"), 1 { version("pmix", "3.0.0"); version("pmix", "3.0.1"); version("pmix", "3.0.2"); version("pmix", "3.1.2"); version("pmix", "3.1.3") } 1.
1 { version("hwloc", "1.11.1"); version("hwloc", "1.11.2"); version("hwloc", "1.11.3"); version("hwloc", "1.11.4"); version("hwloc", "1.11.5"); version("hwloc", "1.11.6"); version("hwloc", "1.11.7"); version("hwloc", "1.11.8"); version("hwloc", "1.11.9"); version("hwloc", "1.11.10"); version("hwloc", "1.11.11"); version("hwloc", "2.0.1"); version("hwloc", "2.0.2"); version("hwloc", "2.1.0"); version("hwloc", "master") } 1 :- depends_on("pmix", "hwloc"), node("pmix"), 1 { version("pmix", "3.0.0"); version("pmix", "3.0.1"); version("pmix", "3.0.2"); version("pmix", "3.1.2"); version("pmix", "3.1.3") } 1.

declared_dependency("pmix", "libevent", "build").
declared_dependency("pmix", "libevent", "link").
node("libevent") :- depends_on("pmix", "libevent"), node("pmix").
1 { version("libevent", "2.0.20"); version("libevent", "2.0.21"); version("libevent", "2.0.22"); version("libevent", "2.1.8") } 1 :- depends_on("pmix", "libevent"), node("pmix").


%----------------------------------------------------------------------------
% Package: psm
%----------------------------------------------------------------------------
version_declared("psm", "3.3", 0).
version_declared("psm", "2017-04-28", 1).

declared_dependency("psm", "libuuid", "build").
declared_dependency("psm", "libuuid", "link").
node("libuuid") :- depends_on("psm", "libuuid"), node("psm").


%----------------------------------------------------------------------------
% Package: py-alabaster
%----------------------------------------------------------------------------
version_declared("py-alabaster", "0.7.12", 0).
version_declared("py-alabaster", "0.7.10", 1).
version_declared("py-alabaster", "0.7.9", 2).

declared_dependency("py-alabaster", "py-pygments", "test").
node("py-pygments") :- depends_on("py-alabaster", "py-pygments"), node("py-alabaster").

declared_dependency("py-alabaster", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-alabaster", "py-setuptools"), node("py-alabaster").

declared_dependency("py-alabaster", "python", "build").
declared_dependency("py-alabaster", "python", "link").
declared_dependency("py-alabaster", "python", "run").
node("python") :- depends_on("py-alabaster", "python"), node("py-alabaster").


%----------------------------------------------------------------------------
% Package: py-appdirs
%----------------------------------------------------------------------------
version_declared("py-appdirs", "1.4.3", 0).
version_declared("py-appdirs", "1.4.0", 1).

declared_dependency("py-appdirs", "python", "build").
declared_dependency("py-appdirs", "python", "link").
declared_dependency("py-appdirs", "python", "run").
node("python") :- depends_on("py-appdirs", "python"), node("py-appdirs").


%----------------------------------------------------------------------------
% Package: py-attrs
%----------------------------------------------------------------------------
version_declared("py-attrs", "19.2.0", 0).
version_declared("py-attrs", "18.1.0", 1).
version_declared("py-attrs", "16.3.0", 2).

declared_dependency("py-attrs", "py-coverage", "test").
node("py-coverage") :- depends_on("py-attrs", "py-coverage"), node("py-attrs").

declared_dependency("py-attrs", "py-hypothesis", "test").
node("py-hypothesis") :- depends_on("py-attrs", "py-hypothesis"), node("py-attrs").

declared_dependency("py-attrs", "py-pympler", "test").
node("py-pympler") :- depends_on("py-attrs", "py-pympler"), node("py-attrs").

declared_dependency("py-attrs", "py-pytest", "test").
node("py-pytest") :- depends_on("py-attrs", "py-pytest"), node("py-attrs").

declared_dependency("py-attrs", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-attrs", "py-setuptools"), node("py-attrs").

declared_dependency("py-attrs", "py-six", "test").
node("py-six") :- depends_on("py-attrs", "py-six"), node("py-attrs").

declared_dependency("py-attrs", "py-zope-interface", "test").
node("py-zope-interface") :- depends_on("py-attrs", "py-zope-interface"), node("py-attrs").

declared_dependency("py-attrs", "python", "build").
declared_dependency("py-attrs", "python", "link").
declared_dependency("py-attrs", "python", "run").
node("python") :- depends_on("py-attrs", "python"), node("py-attrs").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-attrs", "python"), node("py-attrs").


%----------------------------------------------------------------------------
% Package: py-babel
%----------------------------------------------------------------------------
version_declared("py-babel", "2.7.0", 0).
version_declared("py-babel", "2.6.0", 1).
version_declared("py-babel", "2.4.0", 2).
version_declared("py-babel", "2.3.4", 3).

declared_dependency("py-babel", "py-freezegun", "test").
node("py-freezegun") :- depends_on("py-babel", "py-freezegun"), node("py-babel").

declared_dependency("py-babel", "py-pytest", "test").
node("py-pytest") :- depends_on("py-babel", "py-pytest"), node("py-babel").

declared_dependency("py-babel", "py-pytz", "build").
declared_dependency("py-babel", "py-pytz", "run").
node("py-pytz") :- depends_on("py-babel", "py-pytz"), node("py-babel").
1 { version("py-pytz", "2016.3"); version("py-pytz", "2016.6.1"); version("py-pytz", "2016.10"); version("py-pytz", "2018.4"); version("py-pytz", "2019.3") } 1 :- depends_on("py-babel", "py-pytz"), node("py-babel").

declared_dependency("py-babel", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-babel", "py-setuptools"), node("py-babel").

declared_dependency("py-babel", "python", "build").
declared_dependency("py-babel", "python", "link").
declared_dependency("py-babel", "python", "run").
node("python") :- depends_on("py-babel", "python"), node("py-babel").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-babel", "python"), node("py-babel").


%----------------------------------------------------------------------------
% Package: py-certifi
%----------------------------------------------------------------------------
version_declared("py-certifi", "2019.9.11", 0).
version_declared("py-certifi", "2019.6.16", 1).
version_declared("py-certifi", "2017.4.17", 2).
version_declared("py-certifi", "2017.1.23", 3).

declared_dependency("py-certifi", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-certifi", "py-setuptools"), node("py-certifi").

declared_dependency("py-certifi", "python", "build").
declared_dependency("py-certifi", "python", "link").
declared_dependency("py-certifi", "python", "run").
node("python") :- depends_on("py-certifi", "python"), node("py-certifi").


%----------------------------------------------------------------------------
% Package: py-chardet
%----------------------------------------------------------------------------
version_declared("py-chardet", "3.0.4", 0).
version_declared("py-chardet", "3.0.2", 1).
version_declared("py-chardet", "2.3.0", 2).

declared_dependency("py-chardet", "py-hypothesis", "test").
node("py-hypothesis") :- depends_on("py-chardet", "py-hypothesis"), node("py-chardet").

declared_dependency("py-chardet", "py-pytest", "test").
node("py-pytest") :- depends_on("py-chardet", "py-pytest"), node("py-chardet").

declared_dependency("py-chardet", "py-pytest-runner", "build").
node("py-pytest-runner") :- depends_on("py-chardet", "py-pytest-runner"), node("py-chardet").

declared_dependency("py-chardet", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-chardet", "py-setuptools"), node("py-chardet").

declared_dependency("py-chardet", "python", "build").
declared_dependency("py-chardet", "python", "link").
declared_dependency("py-chardet", "python", "run").
node("python") :- depends_on("py-chardet", "python"), node("py-chardet").


%----------------------------------------------------------------------------
% Package: py-cython
%----------------------------------------------------------------------------
version_declared("py-cython", "0.29.14", 0).
version_declared("py-cython", "0.29.13", 1).
version_declared("py-cython", "0.29.7", 2).
version_declared("py-cython", "0.29.5", 3).
version_declared("py-cython", "0.29", 4).
version_declared("py-cython", "0.28.6", 5).
version_declared("py-cython", "0.28.3", 6).
version_declared("py-cython", "0.28.1", 7).
version_declared("py-cython", "0.25.2", 8).
version_declared("py-cython", "0.23.5", 9).
version_declared("py-cython", "0.23.4", 10).
version_declared("py-cython", "0.21.2", 11).

declared_dependency("py-cython", "gdb", "test").
node("gdb") :- depends_on("py-cython", "gdb"), node("py-cython").

declared_dependency("py-cython", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-cython", "py-setuptools"), node("py-cython").

declared_dependency("py-cython", "python", "build") :- node("py-cython"), 1 { version("py-cython", "0.21.2") } 1.
declared_dependency("py-cython", "python", "run") :- node("py-cython"), 1 { version("py-cython", "0.21.2") } 1.
node("python") :- depends_on("py-cython", "python"), node("py-cython"), 1 { version("py-cython", "0.21.2") } 1.
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16") } 1 :- depends_on("py-cython", "python"), node("py-cython"), 1 { version("py-cython", "0.21.2") } 1.
declared_dependency("py-cython", "python", "build").
declared_dependency("py-cython", "python", "link").
declared_dependency("py-cython", "python", "run").
node("python") :- depends_on("py-cython", "python"), node("py-cython").
declared_dependency("py-cython", "python", "build") :- node("py-cython"), 1 { version("py-cython", "0.23.4"); version("py-cython", "0.23.5"); version("py-cython", "0.25.2"); version("py-cython", "0.28.1"); version("py-cython", "0.28.3"); version("py-cython", "0.28.6"); version("py-cython", "0.29"); version("py-cython", "0.29.5"); version("py-cython", "0.29.7"); version("py-cython", "0.29.13"); version("py-cython", "0.29.14") } 1.
declared_dependency("py-cython", "python", "run") :- node("py-cython"), 1 { version("py-cython", "0.23.4"); version("py-cython", "0.23.5"); version("py-cython", "0.25.2"); version("py-cython", "0.28.1"); version("py-cython", "0.28.3"); version("py-cython", "0.28.6"); version("py-cython", "0.29"); version("py-cython", "0.29.5"); version("py-cython", "0.29.7"); version("py-cython", "0.29.13"); version("py-cython", "0.29.14") } 1.
node("python") :- depends_on("py-cython", "python"), node("py-cython"), 1 { version("py-cython", "0.23.4"); version("py-cython", "0.23.5"); version("py-cython", "0.25.2"); version("py-cython", "0.28.1"); version("py-cython", "0.28.3"); version("py-cython", "0.28.6"); version("py-cython", "0.29"); version("py-cython", "0.29.5"); version("py-cython", "0.29.7"); version("py-cython", "0.29.13"); version("py-cython", "0.29.14") } 1.
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-cython", "python"), node("py-cython"), 1 { version("py-cython", "0.23.4"); version("py-cython", "0.23.5"); version("py-cython", "0.25.2"); version("py-cython", "0.28.1"); version("py-cython", "0.28.3"); version("py-cython", "0.28.6"); version("py-cython", "0.29"); version("py-cython", "0.29.5"); version("py-cython", "0.29.7"); version("py-cython", "0.29.13"); version("py-cython", "0.29.14") } 1.


%----------------------------------------------------------------------------
% Package: py-docutils
%----------------------------------------------------------------------------
version_declared("py-docutils", "0.15.2", 0).
version_declared("py-docutils", "0.14", 1).
version_declared("py-docutils", "0.13.1", 2).
version_declared("py-docutils", "0.12", 3).

declared_dependency("py-docutils", "py-setuptools", "build") :- node("py-docutils"), 1 { version("py-docutils", "0.15.2") } 1.
node("py-setuptools") :- depends_on("py-docutils", "py-setuptools"), node("py-docutils"), 1 { version("py-docutils", "0.15.2") } 1.

declared_dependency("py-docutils", "python", "build") :- node("py-docutils").
declared_dependency("py-docutils", "python", "run") :- node("py-docutils").
node("python") :- depends_on("py-docutils", "python"), node("py-docutils").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16") } 1 :- depends_on("py-docutils", "python"), node("py-docutils").
declared_dependency("py-docutils", "python", "build").
declared_dependency("py-docutils", "python", "link").
declared_dependency("py-docutils", "python", "run").
node("python") :- depends_on("py-docutils", "python"), node("py-docutils").
declared_dependency("py-docutils", "python", "build") :- node("py-docutils").
declared_dependency("py-docutils", "python", "run") :- node("py-docutils").
node("python") :- depends_on("py-docutils", "python"), node("py-docutils").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16") } 1 :- depends_on("py-docutils", "python"), node("py-docutils").
declared_dependency("py-docutils", "python", "build") :- node("py-docutils").
declared_dependency("py-docutils", "python", "run") :- node("py-docutils").
node("python") :- depends_on("py-docutils", "python"), node("py-docutils").
declared_dependency("py-docutils", "python", "build") :- node("py-docutils"), 1 { version("py-docutils", "0.12"); version("py-docutils", "0.13.1") } 1.
declared_dependency("py-docutils", "python", "run") :- node("py-docutils"), 1 { version("py-docutils", "0.12"); version("py-docutils", "0.13.1") } 1.
node("python") :- depends_on("py-docutils", "python"), node("py-docutils"), 1 { version("py-docutils", "0.12"); version("py-docutils", "0.13.1") } 1.
declared_dependency("py-docutils", "python", "build") :- node("py-docutils"), 1 { version("py-docutils", "0.14"); version("py-docutils", "0.15.2") } 1.
declared_dependency("py-docutils", "python", "run") :- node("py-docutils"), 1 { version("py-docutils", "0.14"); version("py-docutils", "0.15.2") } 1.
node("python") :- depends_on("py-docutils", "python"), node("py-docutils"), 1 { version("py-docutils", "0.14"); version("py-docutils", "0.15.2") } 1.
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-docutils", "python"), node("py-docutils"), 1 { version("py-docutils", "0.14"); version("py-docutils", "0.15.2") } 1.
declared_dependency("py-docutils", "python", "build") :- node("py-docutils").
declared_dependency("py-docutils", "python", "run") :- node("py-docutils").
node("python") :- depends_on("py-docutils", "python"), node("py-docutils").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-docutils", "python"), node("py-docutils").


%----------------------------------------------------------------------------
% Package: py-idna
%----------------------------------------------------------------------------
version_declared("py-idna", "2.8", 0).
version_declared("py-idna", "2.5", 1).

declared_dependency("py-idna", "py-setuptools", "build").
declared_dependency("py-idna", "py-setuptools", "link").
node("py-setuptools") :- depends_on("py-idna", "py-setuptools"), node("py-idna").

declared_dependency("py-idna", "python", "build").
declared_dependency("py-idna", "python", "link").
declared_dependency("py-idna", "python", "run").
node("python") :- depends_on("py-idna", "python"), node("py-idna").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-idna", "python"), node("py-idna").


%----------------------------------------------------------------------------
% Package: py-imagesize
%----------------------------------------------------------------------------
version_declared("py-imagesize", "1.1.0", 0).
version_declared("py-imagesize", "0.7.1", 1).

declared_dependency("py-imagesize", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-imagesize", "py-setuptools"), node("py-imagesize").

declared_dependency("py-imagesize", "python", "build").
declared_dependency("py-imagesize", "python", "link").
declared_dependency("py-imagesize", "python", "run").
node("python") :- depends_on("py-imagesize", "python"), node("py-imagesize").


%----------------------------------------------------------------------------
% Package: py-jinja2
%----------------------------------------------------------------------------
version_declared("py-jinja2", "2.10.3", 0).
version_declared("py-jinja2", "2.10", 1).
version_declared("py-jinja2", "2.9.6", 2).
version_declared("py-jinja2", "2.8", 3).
version_declared("py-jinja2", "2.7.3", 4).
version_declared("py-jinja2", "2.7.2", 5).
version_declared("py-jinja2", "2.7.1", 6).
version_declared("py-jinja2", "2.7", 7).

declared_dependency("py-jinja2", "py-babel", "build").
declared_dependency("py-jinja2", "py-babel", "run").
node("py-babel") :- depends_on("py-jinja2", "py-babel"), node("py-jinja2").

declared_dependency("py-jinja2", "py-markupsafe", "build").
declared_dependency("py-jinja2", "py-markupsafe", "run").
node("py-markupsafe") :- depends_on("py-jinja2", "py-markupsafe"), node("py-jinja2").
1 { version("py-markupsafe", "0.23"); version("py-markupsafe", "1.0"); version("py-markupsafe", "1.1.1") } 1 :- depends_on("py-jinja2", "py-markupsafe"), node("py-jinja2").

declared_dependency("py-jinja2", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-jinja2", "py-setuptools"), node("py-jinja2").

declared_dependency("py-jinja2", "python", "build").
declared_dependency("py-jinja2", "python", "link").
declared_dependency("py-jinja2", "python", "run").
node("python") :- depends_on("py-jinja2", "python"), node("py-jinja2").


%----------------------------------------------------------------------------
% Package: py-mako
%----------------------------------------------------------------------------
version_declared("py-mako", "1.0.4", 0).
version_declared("py-mako", "1.0.1", 1).

declared_dependency("py-mako", "py-markupsafe", "build").
declared_dependency("py-mako", "py-markupsafe", "run").
node("py-markupsafe") :- depends_on("py-mako", "py-markupsafe"), node("py-mako").

declared_dependency("py-mako", "py-mock", "test").
node("py-mock") :- depends_on("py-mako", "py-mock"), node("py-mako").

declared_dependency("py-mako", "py-pytest", "test").
node("py-pytest") :- depends_on("py-mako", "py-pytest"), node("py-mako").

declared_dependency("py-mako", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-mako", "py-setuptools"), node("py-mako").

declared_dependency("py-mako", "python", "build").
declared_dependency("py-mako", "python", "link").
declared_dependency("py-mako", "python", "run").
node("python") :- depends_on("py-mako", "python"), node("py-mako").


%----------------------------------------------------------------------------
% Package: py-markupsafe
%----------------------------------------------------------------------------
version_declared("py-markupsafe", "1.1.1", 0).
version_declared("py-markupsafe", "1.0", 1).
version_declared("py-markupsafe", "0.23", 2).
version_declared("py-markupsafe", "0.22", 3).
version_declared("py-markupsafe", "0.21", 4).
version_declared("py-markupsafe", "0.20", 5).
version_declared("py-markupsafe", "0.19", 6).

declared_dependency("py-markupsafe", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-markupsafe", "py-setuptools"), node("py-markupsafe").

declared_dependency("py-markupsafe", "python", "build").
declared_dependency("py-markupsafe", "python", "link").
declared_dependency("py-markupsafe", "python", "run").
node("python") :- depends_on("py-markupsafe", "python"), node("py-markupsafe").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-markupsafe", "python"), node("py-markupsafe").


%----------------------------------------------------------------------------
% Package: py-numpy
%----------------------------------------------------------------------------
version_declared("py-numpy", "1.18.1", 0).
version_declared("py-numpy", "1.18.0", 1).
version_declared("py-numpy", "1.17.5", 2).
version_declared("py-numpy", "1.17.4", 3).
version_declared("py-numpy", "1.17.3", 4).
version_declared("py-numpy", "1.17.2", 5).
version_declared("py-numpy", "1.17.1", 6).
version_declared("py-numpy", "1.17.0", 7).
version_declared("py-numpy", "1.16.6", 8).
version_declared("py-numpy", "1.16.5", 9).
version_declared("py-numpy", "1.16.4", 10).
version_declared("py-numpy", "1.16.3", 11).
version_declared("py-numpy", "1.16.2", 12).
version_declared("py-numpy", "1.16.1", 13).
version_declared("py-numpy", "1.16.0", 14).
version_declared("py-numpy", "1.15.4", 15).
version_declared("py-numpy", "1.15.3", 16).
version_declared("py-numpy", "1.15.2", 17).
version_declared("py-numpy", "1.15.1", 18).
version_declared("py-numpy", "1.15.0", 19).
version_declared("py-numpy", "1.14.6", 20).
version_declared("py-numpy", "1.14.5", 21).
version_declared("py-numpy", "1.14.4", 22).
version_declared("py-numpy", "1.14.3", 23).
version_declared("py-numpy", "1.14.2", 24).
version_declared("py-numpy", "1.14.1", 25).
version_declared("py-numpy", "1.14.0", 26).
version_declared("py-numpy", "1.13.3", 27).
version_declared("py-numpy", "1.13.1", 28).
version_declared("py-numpy", "1.13.0", 29).
version_declared("py-numpy", "1.12.1", 30).
version_declared("py-numpy", "1.12.0", 31).
version_declared("py-numpy", "1.11.3", 32).
version_declared("py-numpy", "1.11.2", 33).
version_declared("py-numpy", "1.11.1", 34).
version_declared("py-numpy", "1.11.0", 35).
version_declared("py-numpy", "1.10.4", 36).
version_declared("py-numpy", "1.9.3", 37).
version_declared("py-numpy", "1.9.2", 38).
version_declared("py-numpy", "1.9.1", 39).
version_declared("py-numpy", "master", 40).

variant("py-numpy", "blas").
variant_single_value("py-numpy", "blas").
variant_default_value("py-numpy", "blas", "True").
variant_possible_value("py-numpy", "blas", "False").
variant_possible_value("py-numpy", "blas", "True").

variant("py-numpy", "lapack").
variant_single_value("py-numpy", "lapack").
variant_default_value("py-numpy", "lapack", "True").
variant_possible_value("py-numpy", "lapack", "False").
variant_possible_value("py-numpy", "lapack", "True").

declared_dependency("py-numpy", "blas", "build") :- node("py-numpy"), variant_value("py-numpy", "blas", "True").
declared_dependency("py-numpy", "blas", "link") :- node("py-numpy"), variant_value("py-numpy", "blas", "True").
node("blas") :- depends_on("py-numpy", "blas"), node("py-numpy"), variant_value("py-numpy", "blas", "True").

declared_dependency("py-numpy", "lapack", "build") :- node("py-numpy"), variant_value("py-numpy", "lapack", "True").
declared_dependency("py-numpy", "lapack", "link") :- node("py-numpy"), variant_value("py-numpy", "lapack", "True").
node("lapack") :- depends_on("py-numpy", "lapack"), node("py-numpy"), variant_value("py-numpy", "lapack", "True").

declared_dependency("py-numpy", "py-cython", "build") :- node("py-numpy"), 1 { version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
node("py-cython") :- depends_on("py-numpy", "py-cython"), node("py-numpy"), 1 { version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
1 { version("py-cython", "0.29"); version("py-cython", "0.29.13"); version("py-cython", "0.29.14") } 1 :- depends_on("py-numpy", "py-cython"), node("py-numpy"), 1 { version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
declared_dependency("py-numpy", "py-cython", "build") :- node("py-numpy"), 1 { version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
node("py-cython") :- depends_on("py-numpy", "py-cython"), node("py-numpy"), 1 { version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
1 { version("py-cython", "0.29"); version("py-cython", "0.29.14") } 1 :- depends_on("py-numpy", "py-cython"), node("py-numpy"), 1 { version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.

declared_dependency("py-numpy", "py-nose", "test") :- node("py-numpy"), 1 { version("py-numpy", "1.9.1"); version("py-numpy", "1.9.2"); version("py-numpy", "1.9.3"); version("py-numpy", "1.10.4"); version("py-numpy", "1.11.0"); version("py-numpy", "1.11.1"); version("py-numpy", "1.11.2"); version("py-numpy", "1.11.3"); version("py-numpy", "1.12.0"); version("py-numpy", "1.12.1"); version("py-numpy", "1.13.0"); version("py-numpy", "1.13.1"); version("py-numpy", "1.13.3"); version("py-numpy", "1.14.0"); version("py-numpy", "1.14.1"); version("py-numpy", "1.14.2"); version("py-numpy", "1.14.3"); version("py-numpy", "1.14.4"); version("py-numpy", "1.14.5"); version("py-numpy", "1.14.6") } 1.
node("py-nose") :- depends_on("py-numpy", "py-nose"), node("py-numpy"), 1 { version("py-numpy", "1.9.1"); version("py-numpy", "1.9.2"); version("py-numpy", "1.9.3"); version("py-numpy", "1.10.4"); version("py-numpy", "1.11.0"); version("py-numpy", "1.11.1"); version("py-numpy", "1.11.2"); version("py-numpy", "1.11.3"); version("py-numpy", "1.12.0"); version("py-numpy", "1.12.1"); version("py-numpy", "1.13.0"); version("py-numpy", "1.13.1"); version("py-numpy", "1.13.3"); version("py-numpy", "1.14.0"); version("py-numpy", "1.14.1"); version("py-numpy", "1.14.2"); version("py-numpy", "1.14.3"); version("py-numpy", "1.14.4"); version("py-numpy", "1.14.5"); version("py-numpy", "1.14.6") } 1.

declared_dependency("py-numpy", "py-pytest", "test") :- node("py-numpy"), 1 { version("py-numpy", "1.15.0"); version("py-numpy", "1.15.1"); version("py-numpy", "1.15.2"); version("py-numpy", "1.15.3"); version("py-numpy", "1.15.4"); version("py-numpy", "1.16.0"); version("py-numpy", "1.16.1"); version("py-numpy", "1.16.2"); version("py-numpy", "1.16.3"); version("py-numpy", "1.16.4"); version("py-numpy", "1.16.5"); version("py-numpy", "1.16.6"); version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
node("py-pytest") :- depends_on("py-numpy", "py-pytest"), node("py-numpy"), 1 { version("py-numpy", "1.15.0"); version("py-numpy", "1.15.1"); version("py-numpy", "1.15.2"); version("py-numpy", "1.15.3"); version("py-numpy", "1.15.4"); version("py-numpy", "1.16.0"); version("py-numpy", "1.16.1"); version("py-numpy", "1.16.2"); version("py-numpy", "1.16.3"); version("py-numpy", "1.16.4"); version("py-numpy", "1.16.5"); version("py-numpy", "1.16.6"); version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.

declared_dependency("py-numpy", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-numpy", "py-setuptools"), node("py-numpy").

declared_dependency("py-numpy", "python", "build").
declared_dependency("py-numpy", "python", "link").
declared_dependency("py-numpy", "python", "run").
node("python") :- depends_on("py-numpy", "python"), node("py-numpy").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-numpy", "python"), node("py-numpy").
declared_dependency("py-numpy", "python", "build") :- node("py-numpy"), 1 { version("py-numpy", "1.16.0"); version("py-numpy", "1.16.1"); version("py-numpy", "1.16.2"); version("py-numpy", "1.16.3"); version("py-numpy", "1.16.4"); version("py-numpy", "1.16.5"); version("py-numpy", "1.16.6"); version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
declared_dependency("py-numpy", "python", "run") :- node("py-numpy"), 1 { version("py-numpy", "1.16.0"); version("py-numpy", "1.16.1"); version("py-numpy", "1.16.2"); version("py-numpy", "1.16.3"); version("py-numpy", "1.16.4"); version("py-numpy", "1.16.5"); version("py-numpy", "1.16.6"); version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
node("python") :- depends_on("py-numpy", "python"), node("py-numpy"), 1 { version("py-numpy", "1.16.0"); version("py-numpy", "1.16.1"); version("py-numpy", "1.16.2"); version("py-numpy", "1.16.3"); version("py-numpy", "1.16.4"); version("py-numpy", "1.16.5"); version("py-numpy", "1.16.6"); version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-numpy", "python"), node("py-numpy"), 1 { version("py-numpy", "1.16.0"); version("py-numpy", "1.16.1"); version("py-numpy", "1.16.2"); version("py-numpy", "1.16.3"); version("py-numpy", "1.16.4"); version("py-numpy", "1.16.5"); version("py-numpy", "1.16.6"); version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
declared_dependency("py-numpy", "python", "build") :- node("py-numpy"), 1 { version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
declared_dependency("py-numpy", "python", "run") :- node("py-numpy"), 1 { version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
node("python") :- depends_on("py-numpy", "python"), node("py-numpy"), 1 { version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-numpy", "python"), node("py-numpy"), 1 { version("py-numpy", "1.17.0"); version("py-numpy", "1.17.1"); version("py-numpy", "1.17.2"); version("py-numpy", "1.17.3"); version("py-numpy", "1.17.4"); version("py-numpy", "1.17.5"); version("py-numpy", "1.18.0"); version("py-numpy", "1.18.1"); version("py-numpy", "master") } 1.


%----------------------------------------------------------------------------
% Package: py-packaging
%----------------------------------------------------------------------------
version_declared("py-packaging", "19.2", 0).
version_declared("py-packaging", "19.1", 1).
version_declared("py-packaging", "17.1", 2).
version_declared("py-packaging", "16.8", 3).

declared_dependency("py-packaging", "py-attrs", "build") :- node("py-packaging"), 1 { version("py-packaging", "16.8"); version("py-packaging", "17.1"); version("py-packaging", "19.1") } 1.
declared_dependency("py-packaging", "py-attrs", "run") :- node("py-packaging"), 1 { version("py-packaging", "16.8"); version("py-packaging", "17.1"); version("py-packaging", "19.1") } 1.
node("py-attrs") :- depends_on("py-packaging", "py-attrs"), node("py-packaging"), 1 { version("py-packaging", "16.8"); version("py-packaging", "17.1"); version("py-packaging", "19.1") } 1.

declared_dependency("py-packaging", "py-pyparsing", "build").
declared_dependency("py-packaging", "py-pyparsing", "run").
node("py-pyparsing") :- depends_on("py-packaging", "py-pyparsing"), node("py-packaging").

declared_dependency("py-packaging", "py-six", "build").
declared_dependency("py-packaging", "py-six", "run").
node("py-six") :- depends_on("py-packaging", "py-six"), node("py-packaging").

declared_dependency("py-packaging", "python", "build").
declared_dependency("py-packaging", "python", "link").
declared_dependency("py-packaging", "python", "run").
node("python") :- depends_on("py-packaging", "python"), node("py-packaging").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-packaging", "python"), node("py-packaging").


%----------------------------------------------------------------------------
% Package: py-pygments
%----------------------------------------------------------------------------
version_declared("py-pygments", "2.4.2", 0).
version_declared("py-pygments", "2.3.1", 1).
version_declared("py-pygments", "2.2.0", 2).
version_declared("py-pygments", "2.1.3", 3).
version_declared("py-pygments", "2.0.2", 4).
version_declared("py-pygments", "2.0.1", 5).

declared_dependency("py-pygments", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-pygments", "py-setuptools"), node("py-pygments").

declared_dependency("py-pygments", "python", "build").
declared_dependency("py-pygments", "python", "link").
declared_dependency("py-pygments", "python", "run").
node("python") :- depends_on("py-pygments", "python"), node("py-pygments").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-pygments", "python"), node("py-pygments").


%----------------------------------------------------------------------------
% Package: py-pyparsing
%----------------------------------------------------------------------------
version_declared("py-pyparsing", "2.4.2", 0).
version_declared("py-pyparsing", "2.3.1", 1).
version_declared("py-pyparsing", "2.2.0", 2).
version_declared("py-pyparsing", "2.1.10", 3).
version_declared("py-pyparsing", "2.0.3", 4).

declared_dependency("py-pyparsing", "py-setuptools", "build") :- node("py-pyparsing"), 1 { version("py-pyparsing", "2.3.1"); version("py-pyparsing", "2.4.2") } 1.
node("py-setuptools") :- depends_on("py-pyparsing", "py-setuptools"), node("py-pyparsing"), 1 { version("py-pyparsing", "2.3.1"); version("py-pyparsing", "2.4.2") } 1.

declared_dependency("py-pyparsing", "python", "build").
declared_dependency("py-pyparsing", "python", "link").
declared_dependency("py-pyparsing", "python", "run").
node("python") :- depends_on("py-pyparsing", "python"), node("py-pyparsing").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-pyparsing", "python"), node("py-pyparsing").


%----------------------------------------------------------------------------
% Package: py-pytest-runner
%----------------------------------------------------------------------------
version_declared("py-pytest-runner", "5.1", 0).
version_declared("py-pytest-runner", "2.11.1", 1).

declared_dependency("py-pytest-runner", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-pytest-runner", "py-setuptools"), node("py-pytest-runner").

declared_dependency("py-pytest-runner", "py-setuptools-scm", "build").
node("py-setuptools-scm") :- depends_on("py-pytest-runner", "py-setuptools-scm"), node("py-pytest-runner").

declared_dependency("py-pytest-runner", "python", "build").
declared_dependency("py-pytest-runner", "python", "link").
declared_dependency("py-pytest-runner", "python", "run").
node("python") :- depends_on("py-pytest-runner", "python"), node("py-pytest-runner").


%----------------------------------------------------------------------------
% Package: py-pytz
%----------------------------------------------------------------------------
version_declared("py-pytz", "2019.3", 0).
version_declared("py-pytz", "2018.4", 1).
version_declared("py-pytz", "2016.10", 2).
version_declared("py-pytz", "2016.6.1", 3).
version_declared("py-pytz", "2016.3", 4).
version_declared("py-pytz", "2015.4", 5).
version_declared("py-pytz", "2014.10", 6).
version_declared("py-pytz", "2014.9", 7).

declared_dependency("py-pytz", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-pytz", "py-setuptools"), node("py-pytz").

declared_dependency("py-pytz", "python", "build").
declared_dependency("py-pytz", "python", "link").
declared_dependency("py-pytz", "python", "run").
node("python") :- depends_on("py-pytz", "python"), node("py-pytz").


%----------------------------------------------------------------------------
% Package: py-requests
%----------------------------------------------------------------------------
version_declared("py-requests", "2.22.0", 0).
version_declared("py-requests", "2.21.0", 1).
version_declared("py-requests", "2.14.2", 2).
version_declared("py-requests", "2.13.0", 3).
version_declared("py-requests", "2.11.1", 4).
version_declared("py-requests", "2.3.0", 5).

declared_dependency("py-requests", "py-certifi", "build") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
declared_dependency("py-requests", "py-certifi", "run") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
node("py-certifi") :- depends_on("py-requests", "py-certifi"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
1 { version("py-certifi", "2017.4.17"); version("py-certifi", "2019.6.16"); version("py-certifi", "2019.9.11") } 1 :- depends_on("py-requests", "py-certifi"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.

declared_dependency("py-requests", "py-chardet", "build") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
declared_dependency("py-requests", "py-chardet", "run") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
node("py-chardet") :- depends_on("py-requests", "py-chardet"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
1 { version("py-chardet", "3.0.2"); version("py-chardet", "3.0.4") } 1 :- depends_on("py-requests", "py-chardet"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.

declared_dependency("py-requests", "py-idna", "build") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
declared_dependency("py-requests", "py-idna", "run") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
node("py-idna") :- depends_on("py-requests", "py-idna"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.

declared_dependency("py-requests", "py-pysocks", "test").
node("py-pysocks") :- depends_on("py-requests", "py-pysocks"), node("py-requests").

declared_dependency("py-requests", "py-pytest", "test").
node("py-pytest") :- depends_on("py-requests", "py-pytest"), node("py-requests").

declared_dependency("py-requests", "py-pytest-cov", "test").
node("py-pytest-cov") :- depends_on("py-requests", "py-pytest-cov"), node("py-requests").

declared_dependency("py-requests", "py-pytest-httpbin", "test").
node("py-pytest-httpbin") :- depends_on("py-requests", "py-pytest-httpbin"), node("py-requests").

declared_dependency("py-requests", "py-pytest-mock", "test").
node("py-pytest-mock") :- depends_on("py-requests", "py-pytest-mock"), node("py-requests").

declared_dependency("py-requests", "py-pytest-xdist", "test").
node("py-pytest-xdist") :- depends_on("py-requests", "py-pytest-xdist"), node("py-requests").

declared_dependency("py-requests", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-requests", "py-setuptools"), node("py-requests").

declared_dependency("py-requests", "py-urllib3", "build") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
declared_dependency("py-requests", "py-urllib3", "run") :- node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
node("py-urllib3") :- depends_on("py-requests", "py-urllib3"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.
1 { version("py-urllib3", "1.21.1"); version("py-urllib3", "1.25.6") } 1 :- depends_on("py-requests", "py-urllib3"), node("py-requests"), 1 { version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1.

declared_dependency("py-requests", "python", "build").
declared_dependency("py-requests", "python", "link").
declared_dependency("py-requests", "python", "run").
node("python") :- depends_on("py-requests", "python"), node("py-requests").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-requests", "python"), node("py-requests").


%----------------------------------------------------------------------------
% Package: py-setuptools
%----------------------------------------------------------------------------
version_declared("py-setuptools", "41.4.0", 0).
version_declared("py-setuptools", "41.0.1", 1).
version_declared("py-setuptools", "40.8.0", 2).
version_declared("py-setuptools", "40.4.3", 3).
version_declared("py-setuptools", "40.2.0", 4).
version_declared("py-setuptools", "39.2.0", 5).
version_declared("py-setuptools", "39.0.1", 6).
version_declared("py-setuptools", "35.0.2", 7).
version_declared("py-setuptools", "34.4.1", 8).
version_declared("py-setuptools", "34.2.0", 9).
version_declared("py-setuptools", "25.2.0", 10).
version_declared("py-setuptools", "20.7.0", 11).
version_declared("py-setuptools", "20.6.7", 12).
version_declared("py-setuptools", "19.2", 13).
version_declared("py-setuptools", "18.1", 14).
version_declared("py-setuptools", "16.0", 15).
version_declared("py-setuptools", "11.3.1", 16).

declared_dependency("py-setuptools", "py-appdirs", "build") :- node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.
declared_dependency("py-setuptools", "py-appdirs", "run") :- node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.
node("py-appdirs") :- depends_on("py-setuptools", "py-appdirs"), node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.

declared_dependency("py-setuptools", "py-packaging", "build") :- node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.
declared_dependency("py-setuptools", "py-packaging", "run") :- node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.
node("py-packaging") :- depends_on("py-setuptools", "py-packaging"), node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.

declared_dependency("py-setuptools", "py-six", "build") :- node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.
declared_dependency("py-setuptools", "py-six", "run") :- node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.
node("py-six") :- depends_on("py-setuptools", "py-six"), node("py-setuptools"), 1 { version("py-setuptools", "34.2.0"); version("py-setuptools", "34.4.1"); version("py-setuptools", "35.0.2") } 1.

declared_dependency("py-setuptools", "python", "build").
declared_dependency("py-setuptools", "python", "link").
declared_dependency("py-setuptools", "python", "run").
node("python") :- depends_on("py-setuptools", "python"), node("py-setuptools").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-setuptools", "python"), node("py-setuptools").


%----------------------------------------------------------------------------
% Package: py-setuptools-scm
%----------------------------------------------------------------------------
version_declared("py-setuptools-scm", "3.3.3", 0).
version_declared("py-setuptools-scm", "3.1.0", 1).
version_declared("py-setuptools-scm", "1.15.6", 2).

declared_dependency("py-setuptools-scm", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-setuptools-scm", "py-setuptools"), node("py-setuptools-scm").

declared_dependency("py-setuptools-scm", "python", "build").
declared_dependency("py-setuptools-scm", "python", "link").
declared_dependency("py-setuptools-scm", "python", "run").
node("python") :- depends_on("py-setuptools-scm", "python"), node("py-setuptools-scm").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-setuptools-scm", "python"), node("py-setuptools-scm").


%----------------------------------------------------------------------------
% Package: py-six
%----------------------------------------------------------------------------
version_declared("py-six", "1.12.0", 0).
version_declared("py-six", "1.11.0", 1).
version_declared("py-six", "1.10.0", 2).
version_declared("py-six", "1.9.0", 3).
version_declared("py-six", "1.8.0", 4).

declared_dependency("py-six", "python", "build").
declared_dependency("py-six", "python", "link").
declared_dependency("py-six", "python", "run").
node("python") :- depends_on("py-six", "python"), node("py-six").


%----------------------------------------------------------------------------
% Package: py-snowballstemmer
%----------------------------------------------------------------------------
version_declared("py-snowballstemmer", "2.0.0", 0).
version_declared("py-snowballstemmer", "1.2.1", 1).

declared_dependency("py-snowballstemmer", "py-setuptools", "build") :- node("py-snowballstemmer"), 1 { version("py-snowballstemmer", "2.0.0") } 1.
node("py-setuptools") :- depends_on("py-snowballstemmer", "py-setuptools"), node("py-snowballstemmer"), 1 { version("py-snowballstemmer", "2.0.0") } 1.

declared_dependency("py-snowballstemmer", "python", "build").
declared_dependency("py-snowballstemmer", "python", "link").
declared_dependency("py-snowballstemmer", "python", "run").
node("python") :- depends_on("py-snowballstemmer", "python"), node("py-snowballstemmer").


%----------------------------------------------------------------------------
% Package: py-sphinx
%----------------------------------------------------------------------------
version_declared("py-sphinx", "2.2.0", 0).
version_declared("py-sphinx", "1.8.4", 1).
version_declared("py-sphinx", "1.8.2", 2).
version_declared("py-sphinx", "1.7.4", 3).
version_declared("py-sphinx", "1.6.3", 4).
version_declared("py-sphinx", "1.6.1", 5).
version_declared("py-sphinx", "1.5.5", 6).
version_declared("py-sphinx", "1.4.5", 7).
version_declared("py-sphinx", "1.3.1", 8).

declared_dependency("py-sphinx", "py-alabaster", "build").
declared_dependency("py-sphinx", "py-alabaster", "run").
node("py-alabaster") :- depends_on("py-sphinx", "py-alabaster"), node("py-sphinx").

declared_dependency("py-sphinx", "py-babel", "build").
declared_dependency("py-sphinx", "py-babel", "run").
node("py-babel") :- depends_on("py-sphinx", "py-babel"), node("py-sphinx").

declared_dependency("py-sphinx", "py-docutils", "build").
declared_dependency("py-sphinx", "py-docutils", "run").
node("py-docutils") :- depends_on("py-sphinx", "py-docutils"), node("py-sphinx").

declared_dependency("py-sphinx", "py-docutils-stubs", "test").
node("py-docutils-stubs") :- depends_on("py-sphinx", "py-docutils-stubs"), node("py-sphinx").

declared_dependency("py-sphinx", "py-flake8", "test").
node("py-flake8") :- depends_on("py-sphinx", "py-flake8"), node("py-sphinx").

declared_dependency("py-sphinx", "py-flake8-import-order", "test").
node("py-flake8-import-order") :- depends_on("py-sphinx", "py-flake8-import-order"), node("py-sphinx").

declared_dependency("py-sphinx", "py-html5lib", "test").
node("py-html5lib") :- depends_on("py-sphinx", "py-html5lib"), node("py-sphinx").

declared_dependency("py-sphinx", "py-imagesize", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-imagesize", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.
node("py-imagesize") :- depends_on("py-sphinx", "py-imagesize"), node("py-sphinx"), 1 { version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-jinja2", "build").
declared_dependency("py-sphinx", "py-jinja2", "run").
node("py-jinja2") :- depends_on("py-sphinx", "py-jinja2"), node("py-sphinx").

declared_dependency("py-sphinx", "py-mypy", "test").
node("py-mypy") :- depends_on("py-sphinx", "py-mypy"), node("py-sphinx").

declared_dependency("py-sphinx", "py-packaging", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-packaging", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.
node("py-packaging") :- depends_on("py-sphinx", "py-packaging"), node("py-sphinx"), 1 { version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-pygments", "build").
declared_dependency("py-sphinx", "py-pygments", "run").
node("py-pygments") :- depends_on("py-sphinx", "py-pygments"), node("py-sphinx").

declared_dependency("py-sphinx", "py-pytest", "test").
node("py-pytest") :- depends_on("py-sphinx", "py-pytest"), node("py-sphinx").

declared_dependency("py-sphinx", "py-pytest-cov", "test").
node("py-pytest-cov") :- depends_on("py-sphinx", "py-pytest-cov"), node("py-sphinx").

declared_dependency("py-sphinx", "py-requests", "build").
declared_dependency("py-sphinx", "py-requests", "run").
node("py-requests") :- depends_on("py-sphinx", "py-requests"), node("py-sphinx").
1 { version("py-requests", "2.11.1"); version("py-requests", "2.13.0"); version("py-requests", "2.14.2"); version("py-requests", "2.21.0"); version("py-requests", "2.22.0") } 1 :- depends_on("py-sphinx", "py-requests"), node("py-sphinx").

declared_dependency("py-sphinx", "py-setuptools", "build").
declared_dependency("py-sphinx", "py-setuptools", "run").
node("py-setuptools") :- depends_on("py-sphinx", "py-setuptools"), node("py-sphinx").

declared_dependency("py-sphinx", "py-six", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
declared_dependency("py-sphinx", "py-six", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
node("py-six") :- depends_on("py-sphinx", "py-six"), node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.

declared_dependency("py-sphinx", "py-snowballstemmer", "build").
declared_dependency("py-sphinx", "py-snowballstemmer", "run").
node("py-snowballstemmer") :- depends_on("py-sphinx", "py-snowballstemmer"), node("py-sphinx").

declared_dependency("py-sphinx", "py-sphinx-rtd-theme", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.3.1") } 1.
declared_dependency("py-sphinx", "py-sphinx-rtd-theme", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.3.1") } 1.
node("py-sphinx-rtd-theme") :- depends_on("py-sphinx", "py-sphinx-rtd-theme"), node("py-sphinx"), 1 { version("py-sphinx", "1.3.1") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-applehelp", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-applehelp", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("py-sphinxcontrib-applehelp") :- depends_on("py-sphinx", "py-sphinxcontrib-applehelp"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-devhelp", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-devhelp", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("py-sphinxcontrib-devhelp") :- depends_on("py-sphinx", "py-sphinxcontrib-devhelp"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-htmlhelp", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-htmlhelp", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("py-sphinxcontrib-htmlhelp") :- depends_on("py-sphinx", "py-sphinxcontrib-htmlhelp"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-jsmath", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-jsmath", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("py-sphinxcontrib-jsmath") :- depends_on("py-sphinx", "py-sphinxcontrib-jsmath"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-qthelp", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-qthelp", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("py-sphinxcontrib-qthelp") :- depends_on("py-sphinx", "py-sphinxcontrib-qthelp"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-serializinghtml", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-serializinghtml", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("py-sphinxcontrib-serializinghtml") :- depends_on("py-sphinx", "py-sphinxcontrib-serializinghtml"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "py-sphinxcontrib-websupport", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
declared_dependency("py-sphinx", "py-sphinxcontrib-websupport", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
node("py-sphinxcontrib-websupport") :- depends_on("py-sphinx", "py-sphinxcontrib-websupport"), node("py-sphinx"), 1 { version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.

declared_dependency("py-sphinx", "py-typing", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.6.1") } 1.
declared_dependency("py-sphinx", "py-typing", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.6.1") } 1.
node("py-typing") :- depends_on("py-sphinx", "py-typing"), node("py-sphinx"), 1 { version("py-sphinx", "1.6.1") } 1.
declared_dependency("py-sphinx", "py-typing", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "py-typing", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.
node("py-typing") :- depends_on("py-sphinx", "py-typing"), node("py-sphinx"), 1 { version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4"); version("py-sphinx", "2.2.0") } 1.

declared_dependency("py-sphinx", "python", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
declared_dependency("py-sphinx", "python", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
node("python") :- depends_on("py-sphinx", "python"), node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinx", "python"), node("py-sphinx"), 1 { version("py-sphinx", "1.3.1"); version("py-sphinx", "1.4.5"); version("py-sphinx", "1.5.5"); version("py-sphinx", "1.6.1"); version("py-sphinx", "1.6.3"); version("py-sphinx", "1.7.4"); version("py-sphinx", "1.8.2"); version("py-sphinx", "1.8.4") } 1.
declared_dependency("py-sphinx", "python", "build").
declared_dependency("py-sphinx", "python", "link").
declared_dependency("py-sphinx", "python", "run").
node("python") :- depends_on("py-sphinx", "python"), node("py-sphinx").
declared_dependency("py-sphinx", "python", "build") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
declared_dependency("py-sphinx", "python", "run") :- node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
node("python") :- depends_on("py-sphinx", "python"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinx", "python"), node("py-sphinx"), 1 { version("py-sphinx", "2.2.0") } 1.


%----------------------------------------------------------------------------
% Package: py-sphinx-rtd-theme
%----------------------------------------------------------------------------
version_declared("py-sphinx-rtd-theme", "0.4.3", 0).
version_declared("py-sphinx-rtd-theme", "0.2.5b1", 1).
version_declared("py-sphinx-rtd-theme", "0.1.10a0", 2).

declared_dependency("py-sphinx-rtd-theme", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinx-rtd-theme", "py-setuptools"), node("py-sphinx-rtd-theme").

declared_dependency("py-sphinx-rtd-theme", "python", "build").
declared_dependency("py-sphinx-rtd-theme", "python", "link").
declared_dependency("py-sphinx-rtd-theme", "python", "run").
node("python") :- depends_on("py-sphinx-rtd-theme", "python"), node("py-sphinx-rtd-theme").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-applehelp
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-applehelp", "1.0.1", 0).

declared_dependency("py-sphinxcontrib-applehelp", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-applehelp", "py-setuptools"), node("py-sphinxcontrib-applehelp").

declared_dependency("py-sphinxcontrib-applehelp", "python", "build").
declared_dependency("py-sphinxcontrib-applehelp", "python", "link").
declared_dependency("py-sphinxcontrib-applehelp", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-applehelp", "python"), node("py-sphinxcontrib-applehelp").
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-applehelp", "python"), node("py-sphinxcontrib-applehelp").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-devhelp
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-devhelp", "1.0.1", 0).

declared_dependency("py-sphinxcontrib-devhelp", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-devhelp", "py-setuptools"), node("py-sphinxcontrib-devhelp").

declared_dependency("py-sphinxcontrib-devhelp", "python", "build").
declared_dependency("py-sphinxcontrib-devhelp", "python", "link").
declared_dependency("py-sphinxcontrib-devhelp", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-devhelp", "python"), node("py-sphinxcontrib-devhelp").
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-devhelp", "python"), node("py-sphinxcontrib-devhelp").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-htmlhelp
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-htmlhelp", "1.0.2", 0).

declared_dependency("py-sphinxcontrib-htmlhelp", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-htmlhelp", "py-setuptools"), node("py-sphinxcontrib-htmlhelp").

declared_dependency("py-sphinxcontrib-htmlhelp", "python", "build").
declared_dependency("py-sphinxcontrib-htmlhelp", "python", "link").
declared_dependency("py-sphinxcontrib-htmlhelp", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-htmlhelp", "python"), node("py-sphinxcontrib-htmlhelp").
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-htmlhelp", "python"), node("py-sphinxcontrib-htmlhelp").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-jsmath
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-jsmath", "1.0.1", 0).

declared_dependency("py-sphinxcontrib-jsmath", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-jsmath", "py-setuptools"), node("py-sphinxcontrib-jsmath").

declared_dependency("py-sphinxcontrib-jsmath", "python", "build").
declared_dependency("py-sphinxcontrib-jsmath", "python", "link").
declared_dependency("py-sphinxcontrib-jsmath", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-jsmath", "python"), node("py-sphinxcontrib-jsmath").
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-jsmath", "python"), node("py-sphinxcontrib-jsmath").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-qthelp
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-qthelp", "1.0.2", 0).

declared_dependency("py-sphinxcontrib-qthelp", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-qthelp", "py-setuptools"), node("py-sphinxcontrib-qthelp").

declared_dependency("py-sphinxcontrib-qthelp", "python", "build").
declared_dependency("py-sphinxcontrib-qthelp", "python", "link").
declared_dependency("py-sphinxcontrib-qthelp", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-qthelp", "python"), node("py-sphinxcontrib-qthelp").
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-qthelp", "python"), node("py-sphinxcontrib-qthelp").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-serializinghtml
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-serializinghtml", "1.1.3", 0).

declared_dependency("py-sphinxcontrib-serializinghtml", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-serializinghtml", "py-setuptools"), node("py-sphinxcontrib-serializinghtml").

declared_dependency("py-sphinxcontrib-serializinghtml", "python", "build").
declared_dependency("py-sphinxcontrib-serializinghtml", "python", "link").
declared_dependency("py-sphinxcontrib-serializinghtml", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-serializinghtml", "python"), node("py-sphinxcontrib-serializinghtml").
1 { version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-serializinghtml", "python"), node("py-sphinxcontrib-serializinghtml").


%----------------------------------------------------------------------------
% Package: py-sphinxcontrib-websupport
%----------------------------------------------------------------------------
version_declared("py-sphinxcontrib-websupport", "1.1.2", 0).
version_declared("py-sphinxcontrib-websupport", "1.1.0", 1).
version_declared("py-sphinxcontrib-websupport", "1.0.1", 2).

declared_dependency("py-sphinxcontrib-websupport", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-sphinxcontrib-websupport", "py-setuptools"), node("py-sphinxcontrib-websupport").

declared_dependency("py-sphinxcontrib-websupport", "python", "build").
declared_dependency("py-sphinxcontrib-websupport", "python", "link").
declared_dependency("py-sphinxcontrib-websupport", "python", "run").
node("python") :- depends_on("py-sphinxcontrib-websupport", "python"), node("py-sphinxcontrib-websupport").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-sphinxcontrib-websupport", "python"), node("py-sphinxcontrib-websupport").


%----------------------------------------------------------------------------
% Package: py-typing
%----------------------------------------------------------------------------
version_declared("py-typing", "3.7.4.1", 0).
version_declared("py-typing", "3.6.4", 1).
version_declared("py-typing", "3.6.1", 2).

declared_dependency("py-typing", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-typing", "py-setuptools"), node("py-typing").

declared_dependency("py-typing", "python", "build").
declared_dependency("py-typing", "python", "link").
declared_dependency("py-typing", "python", "run").
node("python") :- depends_on("py-typing", "python"), node("py-typing").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-typing", "python"), node("py-typing").


%----------------------------------------------------------------------------
% Package: py-urllib3
%----------------------------------------------------------------------------
version_declared("py-urllib3", "1.25.6", 0).
version_declared("py-urllib3", "1.21.1", 1).
version_declared("py-urllib3", "1.20", 2).
version_declared("py-urllib3", "1.14", 3).

declared_dependency("py-urllib3", "py-mock", "test").
node("py-mock") :- depends_on("py-urllib3", "py-mock"), node("py-urllib3").

declared_dependency("py-urllib3", "py-pytest", "test").
node("py-pytest") :- depends_on("py-urllib3", "py-pytest"), node("py-urllib3").

declared_dependency("py-urllib3", "py-setuptools", "build").
node("py-setuptools") :- depends_on("py-urllib3", "py-setuptools"), node("py-urllib3").

declared_dependency("py-urllib3", "py-tornado", "test").
node("py-tornado") :- depends_on("py-urllib3", "py-tornado"), node("py-urllib3").

declared_dependency("py-urllib3", "python", "build").
declared_dependency("py-urllib3", "python", "link").
declared_dependency("py-urllib3", "python", "run").
node("python") :- depends_on("py-urllib3", "python"), node("py-urllib3").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("py-urllib3", "python"), node("py-urllib3").


%----------------------------------------------------------------------------
% Package: python
%----------------------------------------------------------------------------
version_declared("python", "3.7.6", 0).
version_declared("python", "3.8.1", 1).
version_declared("python", "3.8.0", 2).
version_declared("python", "3.7.5", 3).
version_declared("python", "3.7.4", 4).
version_declared("python", "3.7.3", 5).
version_declared("python", "3.7.2", 6).
version_declared("python", "3.7.1", 7).
version_declared("python", "3.7.0", 8).
version_declared("python", "3.6.8", 9).
version_declared("python", "3.6.7", 10).
version_declared("python", "3.6.6", 11).
version_declared("python", "3.6.5", 12).
version_declared("python", "3.6.4", 13).
version_declared("python", "3.6.3", 14).
version_declared("python", "3.6.2", 15).
version_declared("python", "3.6.1", 16).
version_declared("python", "3.6.0", 17).
version_declared("python", "3.5.7", 18).
version_declared("python", "3.5.2", 19).
version_declared("python", "3.5.1", 20).
version_declared("python", "3.5.0", 21).
version_declared("python", "3.4.10", 22).
version_declared("python", "3.4.3", 23).
version_declared("python", "3.3.6", 24).
version_declared("python", "3.2.6", 25).
version_declared("python", "3.1.5", 26).
version_declared("python", "2.7.16", 27).
version_declared("python", "2.7.15", 28).
version_declared("python", "2.7.14", 29).
version_declared("python", "2.7.13", 30).
version_declared("python", "2.7.12", 31).
version_declared("python", "2.7.11", 32).
version_declared("python", "2.7.10", 33).
version_declared("python", "2.7.9", 34).
version_declared("python", "2.7.8", 35).

variant("python", "bz2").
variant_single_value("python", "bz2").
variant_default_value("python", "bz2", "True").
variant_possible_value("python", "bz2", "False").
variant_possible_value("python", "bz2", "True").

variant("python", "ctypes").
variant_single_value("python", "ctypes").
variant_default_value("python", "ctypes", "True").
variant_possible_value("python", "ctypes", "False").
variant_possible_value("python", "ctypes", "True").

variant("python", "dbm").
variant_single_value("python", "dbm").
variant_default_value("python", "dbm", "True").
variant_possible_value("python", "dbm", "False").
variant_possible_value("python", "dbm", "True").

variant("python", "debug").
variant_single_value("python", "debug").
variant_default_value("python", "debug", "False").
variant_possible_value("python", "debug", "False").
variant_possible_value("python", "debug", "True").

variant("python", "libxml2").
variant_single_value("python", "libxml2").
variant_default_value("python", "libxml2", "True").
variant_possible_value("python", "libxml2", "False").
variant_possible_value("python", "libxml2", "True").

variant("python", "lzma").
variant_single_value("python", "lzma").
variant_default_value("python", "lzma", "True").
variant_possible_value("python", "lzma", "False").
variant_possible_value("python", "lzma", "True").

variant("python", "nis").
variant_single_value("python", "nis").
variant_default_value("python", "nis", "False").
variant_possible_value("python", "nis", "False").
variant_possible_value("python", "nis", "True").

variant("python", "optimizations").
variant_single_value("python", "optimizations").
variant_default_value("python", "optimizations", "False").
variant_possible_value("python", "optimizations", "False").
variant_possible_value("python", "optimizations", "True").

variant("python", "pic").
variant_single_value("python", "pic").
variant_default_value("python", "pic", "True").
variant_possible_value("python", "pic", "False").
variant_possible_value("python", "pic", "True").

variant("python", "pyexpat").
variant_single_value("python", "pyexpat").
variant_default_value("python", "pyexpat", "True").
variant_possible_value("python", "pyexpat", "False").
variant_possible_value("python", "pyexpat", "True").

variant("python", "pythoncmd").
variant_single_value("python", "pythoncmd").
variant_default_value("python", "pythoncmd", "True").
variant_possible_value("python", "pythoncmd", "False").
variant_possible_value("python", "pythoncmd", "True").

variant("python", "readline").
variant_single_value("python", "readline").
variant_default_value("python", "readline", "True").
variant_possible_value("python", "readline", "False").
variant_possible_value("python", "readline", "True").

variant("python", "shared").
variant_single_value("python", "shared").
variant_default_value("python", "shared", "False").
variant_possible_value("python", "shared", "False").
variant_possible_value("python", "shared", "True").

variant("python", "sqlite3").
variant_single_value("python", "sqlite3").
variant_default_value("python", "sqlite3", "True").
variant_possible_value("python", "sqlite3", "False").
variant_possible_value("python", "sqlite3", "True").

variant("python", "ssl").
variant_single_value("python", "ssl").
variant_default_value("python", "ssl", "True").
variant_possible_value("python", "ssl", "False").
variant_possible_value("python", "ssl", "True").

variant("python", "tix").
variant_single_value("python", "tix").
variant_default_value("python", "tix", "False").
variant_possible_value("python", "tix", "False").
variant_possible_value("python", "tix", "True").

variant("python", "tkinter").
variant_single_value("python", "tkinter").
variant_default_value("python", "tkinter", "False").
variant_possible_value("python", "tkinter", "False").
variant_possible_value("python", "tkinter", "True").

variant("python", "ucs4").
variant_single_value("python", "ucs4").
variant_default_value("python", "ucs4", "False").
variant_possible_value("python", "ucs4", "False").
variant_possible_value("python", "ucs4", "True").

variant("python", "uuid").
variant_single_value("python", "uuid").
variant_default_value("python", "uuid", "False").
variant_possible_value("python", "uuid", "False").
variant_possible_value("python", "uuid", "True").

variant("python", "zlib").
variant_single_value("python", "zlib").
variant_default_value("python", "zlib", "True").
variant_possible_value("python", "zlib", "False").
variant_possible_value("python", "zlib", "True").

declared_dependency("python", "bzip2", "build") :- node("python"), variant_value("python", "bz2", "True").
declared_dependency("python", "bzip2", "link") :- node("python"), variant_value("python", "bz2", "True").
node("bzip2") :- depends_on("python", "bzip2"), node("python"), variant_value("python", "bz2", "True").

declared_dependency("python", "expat", "build") :- node("python"), variant_value("python", "pyexpat", "True").
declared_dependency("python", "expat", "link") :- node("python"), variant_value("python", "pyexpat", "True").
node("expat") :- depends_on("python", "expat"), node("python"), variant_value("python", "pyexpat", "True").

declared_dependency("python", "gdbm", "build") :- node("python"), variant_value("python", "dbm", "True").
declared_dependency("python", "gdbm", "link") :- node("python"), variant_value("python", "dbm", "True").
node("gdbm") :- depends_on("python", "gdbm"), node("python"), variant_value("python", "dbm", "True").

declared_dependency("python", "gettext", "build") :- node("python"), variant_value("python", "libxml2", "False").
declared_dependency("python", "gettext", "link") :- node("python"), variant_value("python", "libxml2", "False").
node("gettext") :- depends_on("python", "gettext"), node("python"), variant_value("python", "libxml2", "False").
variant_set("gettext", "libxml2", "False") :- depends_on("python", "gettext"), node("python"), variant_value("python", "libxml2", "False").
declared_dependency("python", "gettext", "build") :- node("python"), variant_value("python", "libxml2", "True").
declared_dependency("python", "gettext", "link") :- node("python"), variant_value("python", "libxml2", "True").
node("gettext") :- depends_on("python", "gettext"), node("python"), variant_value("python", "libxml2", "True").
variant_set("gettext", "libxml2", "True") :- depends_on("python", "gettext"), node("python"), variant_value("python", "libxml2", "True").

declared_dependency("python", "libffi", "build") :- node("python"), variant_value("python", "ctypes", "True").
declared_dependency("python", "libffi", "link") :- node("python"), variant_value("python", "ctypes", "True").
node("libffi") :- depends_on("python", "libffi"), node("python"), variant_value("python", "ctypes", "True").

declared_dependency("python", "libnsl", "build") :- node("python"), variant_value("python", "nis", "True").
declared_dependency("python", "libnsl", "link") :- node("python"), variant_value("python", "nis", "True").
node("libnsl") :- depends_on("python", "libnsl"), node("python"), variant_value("python", "nis", "True").

declared_dependency("python", "ncurses", "build") :- node("python"), variant_value("python", "readline", "True").
declared_dependency("python", "ncurses", "link") :- node("python"), variant_value("python", "readline", "True").
node("ncurses") :- depends_on("python", "ncurses"), node("python"), variant_value("python", "readline", "True").

declared_dependency("python", "openssl", "build") :- node("python"), variant_value("python", "ssl", "True").
declared_dependency("python", "openssl", "link") :- node("python"), variant_value("python", "ssl", "True").
node("openssl") :- depends_on("python", "openssl"), node("python"), variant_value("python", "ssl", "True").
declared_dependency("python", "openssl", "build") :- node("python"), 1 { version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "ssl", "True").
declared_dependency("python", "openssl", "link") :- node("python"), 1 { version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "ssl", "True").
node("openssl") :- depends_on("python", "openssl"), node("python"), 1 { version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "ssl", "True").
1 { version("openssl", "1.0.2d"); version("openssl", "1.0.2e"); version("openssl", "1.0.2f"); version("openssl", "1.0.2g"); version("openssl", "1.0.2h"); version("openssl", "1.0.2i"); version("openssl", "1.0.2j"); version("openssl", "1.0.2k"); version("openssl", "1.0.2m"); version("openssl", "1.0.2n"); version("openssl", "1.0.2o"); version("openssl", "1.0.2p"); version("openssl", "1.0.2r"); version("openssl", "1.0.2s"); version("openssl", "1.0.2t"); version("openssl", "1.1.0c"); version("openssl", "1.1.0d"); version("openssl", "1.1.0e"); version("openssl", "1.1.0g"); version("openssl", "1.1.0i"); version("openssl", "1.1.0j"); version("openssl", "1.1.0k"); version("openssl", "1.1.0l"); version("openssl", "1.1.1"); version("openssl", "1.1.1a"); version("openssl", "1.1.1b"); version("openssl", "1.1.1c"); version("openssl", "1.1.1d") } 1 :- depends_on("python", "openssl"), node("python"), 1 { version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "ssl", "True").

declared_dependency("python", "pkgconfig", "build").
node("pkgconfig") :- depends_on("python", "pkgconfig"), node("python").

declared_dependency("python", "readline", "build") :- node("python"), variant_value("python", "readline", "True").
declared_dependency("python", "readline", "link") :- node("python"), variant_value("python", "readline", "True").
node("readline") :- depends_on("python", "readline"), node("python"), variant_value("python", "readline", "True").

declared_dependency("python", "sqlite", "build") :- node("python"), variant_value("python", "sqlite3", "True").
declared_dependency("python", "sqlite", "link") :- node("python"), variant_value("python", "sqlite3", "True").
node("sqlite") :- depends_on("python", "sqlite"), node("python"), variant_value("python", "sqlite3", "True").

declared_dependency("python", "tcl", "build") :- node("python"), variant_value("python", "tkinter", "True").
declared_dependency("python", "tcl", "link") :- node("python"), variant_value("python", "tkinter", "True").
node("tcl") :- depends_on("python", "tcl"), node("python"), variant_value("python", "tkinter", "True").

declared_dependency("python", "tix", "build") :- node("python"), variant_value("python", "tix", "True").
declared_dependency("python", "tix", "link") :- node("python"), variant_value("python", "tix", "True").
node("tix") :- depends_on("python", "tix"), node("python"), variant_value("python", "tix", "True").

declared_dependency("python", "tk", "build") :- node("python"), variant_value("python", "tkinter", "True").
declared_dependency("python", "tk", "link") :- node("python"), variant_value("python", "tkinter", "True").
node("tk") :- depends_on("python", "tk"), node("python"), variant_value("python", "tkinter", "True").

declared_dependency("python", "xz", "build") :- node("python"), 1 { version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "lzma", "True").
declared_dependency("python", "xz", "link") :- node("python"), 1 { version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "lzma", "True").
node("xz") :- depends_on("python", "xz"), node("python"), 1 { version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1, variant_value("python", "lzma", "True").

declared_dependency("python", "zlib", "build") :- node("python"), variant_value("python", "zlib", "True").
declared_dependency("python", "zlib", "link") :- node("python"), variant_value("python", "zlib", "True").
node("zlib") :- depends_on("python", "zlib"), node("python"), variant_value("python", "zlib", "True").


%----------------------------------------------------------------------------
% Package: qt
%----------------------------------------------------------------------------
version_declared("qt", "5.14.1", 0).
version_declared("qt", "5.14.0", 1).
version_declared("qt", "5.13.1", 2).
version_declared("qt", "5.12.5", 3).
version_declared("qt", "5.12.2", 4).
version_declared("qt", "5.11.3", 5).
version_declared("qt", "5.11.2", 6).
version_declared("qt", "5.10.0", 7).
version_declared("qt", "5.9.1", 8).
version_declared("qt", "5.9.0", 9).
version_declared("qt", "5.8.0", 10).
version_declared("qt", "5.7.1", 11).
version_declared("qt", "5.7.0", 12).
version_declared("qt", "5.5.1", 13).
version_declared("qt", "5.4.2", 14).
version_declared("qt", "5.4.0", 15).
version_declared("qt", "5.3.2", 16).
version_declared("qt", "5.2.1", 17).
version_declared("qt", "4.8.7", 18).
version_declared("qt", "4.8.6", 19).
version_declared("qt", "4.8.5", 20).
version_declared("qt", "3.3.8b", 21).

variant("qt", "dbus").
variant_single_value("qt", "dbus").
variant_default_value("qt", "dbus", "False").
variant_possible_value("qt", "dbus", "False").
variant_possible_value("qt", "dbus", "True").

variant("qt", "examples").
variant_single_value("qt", "examples").
variant_default_value("qt", "examples", "False").
variant_possible_value("qt", "examples", "False").
variant_possible_value("qt", "examples", "True").

variant("qt", "framework").
variant_single_value("qt", "framework").
variant_default_value("qt", "framework", "True").
variant_possible_value("qt", "framework", "False").
variant_possible_value("qt", "framework", "True").

variant("qt", "freetype").
variant_single_value("qt", "freetype").
variant_default_value("qt", "freetype", "spack").
variant_possible_value("qt", "freetype", "none").
variant_possible_value("qt", "freetype", "qt").
variant_possible_value("qt", "freetype", "spack").

variant("qt", "gtk").
variant_single_value("qt", "gtk").
variant_default_value("qt", "gtk", "False").
variant_possible_value("qt", "gtk", "False").
variant_possible_value("qt", "gtk", "True").

variant("qt", "krellpatch").
variant_single_value("qt", "krellpatch").
variant_default_value("qt", "krellpatch", "False").
variant_possible_value("qt", "krellpatch", "False").
variant_possible_value("qt", "krellpatch", "True").

variant("qt", "opengl").
variant_single_value("qt", "opengl").
variant_default_value("qt", "opengl", "False").
variant_possible_value("qt", "opengl", "False").
variant_possible_value("qt", "opengl", "True").

variant("qt", "phonon").
variant_single_value("qt", "phonon").
variant_default_value("qt", "phonon", "False").
variant_possible_value("qt", "phonon", "False").
variant_possible_value("qt", "phonon", "True").

variant("qt", "shared").
variant_single_value("qt", "shared").
variant_default_value("qt", "shared", "True").
variant_possible_value("qt", "shared", "False").
variant_possible_value("qt", "shared", "True").

variant("qt", "sql").
variant_single_value("qt", "sql").
variant_default_value("qt", "sql", "True").
variant_possible_value("qt", "sql", "False").
variant_possible_value("qt", "sql", "True").

variant("qt", "ssl").
variant_single_value("qt", "ssl").
variant_default_value("qt", "ssl", "True").
variant_possible_value("qt", "ssl", "False").
variant_possible_value("qt", "ssl", "True").

variant("qt", "tools").
variant_single_value("qt", "tools").
variant_default_value("qt", "tools", "True").
variant_possible_value("qt", "tools", "False").
variant_possible_value("qt", "tools", "True").

variant("qt", "webkit").
variant_single_value("qt", "webkit").
variant_default_value("qt", "webkit", "False").
variant_possible_value("qt", "webkit", "False").
variant_possible_value("qt", "webkit", "True").

declared_dependency("qt", "bison", "build") :- node("qt"), variant_value("qt", "webkit", "True").
node("bison") :- depends_on("qt", "bison"), node("qt"), variant_value("qt", "webkit", "True").

declared_dependency("qt", "dbus", "build") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1, variant_value("qt", "dbus", "True").
declared_dependency("qt", "dbus", "link") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1, variant_value("qt", "dbus", "True").
node("dbus") :- depends_on("qt", "dbus"), node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1, variant_value("qt", "dbus", "True").

declared_dependency("qt", "double-conversion", "build") :- node("qt"), 1 { version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
declared_dependency("qt", "double-conversion", "link") :- node("qt"), 1 { version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
node("double-conversion") :- depends_on("qt", "double-conversion"), node("qt"), 1 { version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.

declared_dependency("qt", "flex", "build") :- node("qt"), variant_value("qt", "webkit", "True").
node("flex") :- depends_on("qt", "flex"), node("qt"), variant_value("qt", "webkit", "True").

declared_dependency("qt", "freetype", "build") :- node("qt"), variant_value("qt", "freetype", "spack").
declared_dependency("qt", "freetype", "link") :- node("qt"), variant_value("qt", "freetype", "spack").
node("freetype") :- depends_on("qt", "freetype"), node("qt"), variant_value("qt", "freetype", "spack").

declared_dependency("qt", "gl", "build") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1, variant_value("qt", "opengl", "True").
declared_dependency("qt", "gl", "link") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1, variant_value("qt", "opengl", "True").
node("gl") :- depends_on("qt", "gl"), node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1, variant_value("qt", "opengl", "True").

declared_dependency("qt", "glib", "build") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
declared_dependency("qt", "glib", "link") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
node("glib") :- depends_on("qt", "glib"), node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.

declared_dependency("qt", "gperf", "build") :- node("qt"), variant_value("qt", "webkit", "True").
declared_dependency("qt", "gperf", "link") :- node("qt"), variant_value("qt", "webkit", "True").
node("gperf") :- depends_on("qt", "gperf"), node("qt"), variant_value("qt", "webkit", "True").

declared_dependency("qt", "gtkplus", "build") :- node("qt"), variant_value("qt", "gtk", "True").
declared_dependency("qt", "gtkplus", "link") :- node("qt"), variant_value("qt", "gtk", "True").
node("gtkplus") :- depends_on("qt", "gtkplus"), node("qt"), variant_value("qt", "gtk", "True").

declared_dependency("qt", "harfbuzz", "build") :- node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
declared_dependency("qt", "harfbuzz", "link") :- node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
node("harfbuzz") :- depends_on("qt", "harfbuzz"), node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.

declared_dependency("qt", "icu4c", "build").
declared_dependency("qt", "icu4c", "link").
node("icu4c") :- depends_on("qt", "icu4c"), node("qt").

declared_dependency("qt", "inputproto", "build") :- node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.
declared_dependency("qt", "inputproto", "link") :- node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.
node("inputproto") :- depends_on("qt", "inputproto"), node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.

declared_dependency("qt", "jpeg", "build").
declared_dependency("qt", "jpeg", "link").
node("jpeg") :- depends_on("qt", "jpeg"), node("qt").

declared_dependency("qt", "libmng", "build").
declared_dependency("qt", "libmng", "link").
node("libmng") :- depends_on("qt", "libmng"), node("qt").

declared_dependency("qt", "libpng", "build") :- node("qt"), 1 { version("qt", "3.3.8b") } 1.
declared_dependency("qt", "libpng", "link") :- node("qt"), 1 { version("qt", "3.3.8b") } 1.
node("libpng") :- depends_on("qt", "libpng"), node("qt"), 1 { version("qt", "3.3.8b") } 1.
1 { version("libpng", "1.2.57") } 1 :- depends_on("qt", "libpng"), node("qt"), 1 { version("qt", "3.3.8b") } 1.
declared_dependency("qt", "libpng", "build") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
declared_dependency("qt", "libpng", "link") :- node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
node("libpng") :- depends_on("qt", "libpng"), node("qt"), 1 { version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.

declared_dependency("qt", "libtiff", "build").
declared_dependency("qt", "libtiff", "link").
node("libtiff") :- depends_on("qt", "libtiff"), node("qt").

declared_dependency("qt", "libxml2", "build").
declared_dependency("qt", "libxml2", "link").
node("libxml2") :- depends_on("qt", "libxml2"), node("qt").

declared_dependency("qt", "openssl", "build") :- node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1") } 1, variant_value("qt", "krellpatch", "False"), variant_value("qt", "ssl", "True").
declared_dependency("qt", "openssl", "link") :- node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1") } 1, variant_value("qt", "krellpatch", "False"), variant_value("qt", "ssl", "True").
node("openssl") :- depends_on("qt", "openssl"), node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1") } 1, variant_value("qt", "krellpatch", "False"), variant_value("qt", "ssl", "True").
1 { version("openssl", "1.0.1e"); version("openssl", "1.0.1h"); version("openssl", "1.0.1r"); version("openssl", "1.0.1t"); version("openssl", "1.0.1u"); version("openssl", "1.0.2d"); version("openssl", "1.0.2e"); version("openssl", "1.0.2f"); version("openssl", "1.0.2g"); version("openssl", "1.0.2h"); version("openssl", "1.0.2i"); version("openssl", "1.0.2j"); version("openssl", "1.0.2k"); version("openssl", "1.0.2m"); version("openssl", "1.0.2n"); version("openssl", "1.0.2o"); version("openssl", "1.0.2p"); version("openssl", "1.0.2r"); version("openssl", "1.0.2s"); version("openssl", "1.0.2t") } 1 :- depends_on("qt", "openssl"), node("qt"), 1 { version("qt", "3.3.8b"); version("qt", "4.8.5"); version("qt", "4.8.6"); version("qt", "4.8.7"); version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1") } 1, variant_value("qt", "krellpatch", "False"), variant_value("qt", "ssl", "True").
declared_dependency("qt", "openssl", "build") :- node("qt"), variant_value("qt", "ssl", "True").
declared_dependency("qt", "openssl", "link") :- node("qt"), variant_value("qt", "ssl", "True").
node("openssl") :- depends_on("qt", "openssl"), node("qt"), variant_value("qt", "ssl", "True").

declared_dependency("qt", "pcre", "build") :- node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.
declared_dependency("qt", "pcre", "link") :- node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.
node("pcre") :- depends_on("qt", "pcre"), node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.
variant_set("pcre", "multibyte", "True") :- depends_on("qt", "pcre"), node("qt"), 1 { version("qt", "5.2.1"); version("qt", "5.3.2"); version("qt", "5.4.0"); version("qt", "5.4.2"); version("qt", "5.5.1"); version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0") } 1.

declared_dependency("qt", "pcre2", "build") :- node("qt"), 1 { version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
declared_dependency("qt", "pcre2", "link") :- node("qt"), 1 { version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
node("pcre2") :- depends_on("qt", "pcre2"), node("qt"), 1 { version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
variant_set("pcre2", "multibyte", "True") :- depends_on("qt", "pcre2"), node("qt"), 1 { version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.

declared_dependency("qt", "pkgconfig", "build").
node("pkgconfig") :- depends_on("qt", "pkgconfig"), node("qt").

declared_dependency("qt", "python", "build") :- node("qt"), 1 { version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.
node("python") :- depends_on("qt", "python"), node("qt"), 1 { version("qt", "5.7.0"); version("qt", "5.7.1"); version("qt", "5.8.0"); version("qt", "5.9.0"); version("qt", "5.9.1"); version("qt", "5.10.0"); version("qt", "5.11.2"); version("qt", "5.11.3"); version("qt", "5.12.2"); version("qt", "5.12.5"); version("qt", "5.13.1"); version("qt", "5.14.0"); version("qt", "5.14.1") } 1.

declared_dependency("qt", "sqlite", "build") :- node("qt"), variant_value("qt", "sql", "True").
declared_dependency("qt", "sqlite", "run") :- node("qt"), variant_value("qt", "sql", "True").
node("sqlite") :- depends_on("qt", "sqlite"), node("qt"), variant_value("qt", "sql", "True").
declared_dependency("qt", "sqlite", "build") :- node("qt"), variant_value("qt", "sql", "True"), node_compiler("qt", "intel"), node_compiler_hard("qt", "intel"), 1 {  } 1.
declared_dependency("qt", "sqlite", "run") :- node("qt"), variant_value("qt", "sql", "True"), node_compiler("qt", "intel"), node_compiler_hard("qt", "intel"), 1 {  } 1.
node("sqlite") :- depends_on("qt", "sqlite"), node("qt"), variant_value("qt", "sql", "True"), node_compiler("qt", "intel"), node_compiler_hard("qt", "intel"), 1 {  } 1.
variant_set("sqlite", "column_metadata", "True") :- depends_on("qt", "sqlite"), node("qt"), variant_value("qt", "sql", "True"), node_compiler("qt", "intel"), node_compiler_hard("qt", "intel"), 1 {  } 1.

declared_dependency("qt", "zlib", "build").
declared_dependency("qt", "zlib", "link").
node("zlib") :- depends_on("qt", "zlib"), node("qt").


%----------------------------------------------------------------------------
% Package: rdma-core
%----------------------------------------------------------------------------
version_declared("rdma-core", "20", 0).
version_declared("rdma-core", "17.1", 1).
version_declared("rdma-core", "13", 2).

variant("rdma-core", "build_type").
variant_single_value("rdma-core", "build_type").
variant_default_value("rdma-core", "build_type", "RelWithDebInfo").
variant_possible_value("rdma-core", "build_type", "Debug").
variant_possible_value("rdma-core", "build_type", "MinSizeRel").
variant_possible_value("rdma-core", "build_type", "RelWithDebInfo").
variant_possible_value("rdma-core", "build_type", "Release").

declared_dependency("rdma-core", "cmake", "build").
node("cmake") :- depends_on("rdma-core", "cmake"), node("rdma-core").

declared_dependency("rdma-core", "libnl", "build").
declared_dependency("rdma-core", "libnl", "link").
node("libnl") :- depends_on("rdma-core", "libnl"), node("rdma-core").

declared_dependency("rdma-core", "pkgconfig", "build").
node("pkgconfig") :- depends_on("rdma-core", "pkgconfig"), node("rdma-core").


%----------------------------------------------------------------------------
% Package: readline
%----------------------------------------------------------------------------
version_declared("readline", "8.0", 0).
version_declared("readline", "7.0", 1).
version_declared("readline", "6.3", 2).

declared_dependency("readline", "ncurses", "build").
declared_dependency("readline", "ncurses", "link").
node("ncurses") :- depends_on("readline", "ncurses"), node("readline").


%----------------------------------------------------------------------------
% Package: recordproto
%----------------------------------------------------------------------------
version_declared("recordproto", "1.14.2", 0).

declared_dependency("recordproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("recordproto", "pkgconfig"), node("recordproto").

declared_dependency("recordproto", "util-macros", "build").
node("util-macros") :- depends_on("recordproto", "util-macros"), node("recordproto").


%----------------------------------------------------------------------------
% Package: renderproto
%----------------------------------------------------------------------------
version_declared("renderproto", "0.11.1", 0).

declared_dependency("renderproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("renderproto", "pkgconfig"), node("renderproto").

declared_dependency("renderproto", "util-macros", "build").
node("util-macros") :- depends_on("renderproto", "util-macros"), node("renderproto").


%----------------------------------------------------------------------------
% Package: rhash
%----------------------------------------------------------------------------
version_declared("rhash", "1.3.5", 0).


%----------------------------------------------------------------------------
% Package: rpcsvc-proto
%----------------------------------------------------------------------------
version_declared("rpcsvc-proto", "1.4", 0).

declared_dependency("rpcsvc-proto", "gettext", "build").
declared_dependency("rpcsvc-proto", "gettext", "link").
node("gettext") :- depends_on("rpcsvc-proto", "gettext"), node("rpcsvc-proto").


%----------------------------------------------------------------------------
% Package: rust
%----------------------------------------------------------------------------
version_declared("rust", "1.41.0", 0).
version_declared("rust", "1.34.0", 1).
version_declared("rust", "1.32.0", 2).
version_declared("rust", "1.31.1", 3).
version_declared("rust", "1.31.0", 4).
version_declared("rust", "1.30.1", 5).
version_declared("rust", "develop", 6).

declared_dependency("rust", "binutils", "build").
declared_dependency("rust", "binutils", "link").
node("binutils") :- depends_on("rust", "binutils"), node("rust").

declared_dependency("rust", "cmake", "build").
declared_dependency("rust", "cmake", "link").
node("cmake") :- depends_on("rust", "cmake"), node("rust").

declared_dependency("rust", "curl", "build").
declared_dependency("rust", "curl", "link").
node("curl") :- depends_on("rust", "curl"), node("rust").

declared_dependency("rust", "git", "build").
declared_dependency("rust", "git", "link").
node("git") :- depends_on("rust", "git"), node("rust").

declared_dependency("rust", "llvm", "build").
declared_dependency("rust", "llvm", "link").
node("llvm") :- depends_on("rust", "llvm"), node("rust").

declared_dependency("rust", "openssl", "build").
declared_dependency("rust", "openssl", "link").
node("openssl") :- depends_on("rust", "openssl"), node("rust").

declared_dependency("rust", "python", "build").
declared_dependency("rust", "python", "link").
node("python") :- depends_on("rust", "python"), node("rust").
1 { version("python", "2.7.8"); version("python", "2.7.9"); version("python", "2.7.10"); version("python", "2.7.11"); version("python", "2.7.12"); version("python", "2.7.13"); version("python", "2.7.14"); version("python", "2.7.15"); version("python", "2.7.16") } 1 :- depends_on("rust", "python"), node("rust").


%----------------------------------------------------------------------------
% Package: scrnsaverproto
%----------------------------------------------------------------------------
version_declared("scrnsaverproto", "1.2.2", 0).

declared_dependency("scrnsaverproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("scrnsaverproto", "pkgconfig"), node("scrnsaverproto").

declared_dependency("scrnsaverproto", "util-macros", "build").
node("util-macros") :- depends_on("scrnsaverproto", "util-macros"), node("scrnsaverproto").


%----------------------------------------------------------------------------
% Package: sed
%----------------------------------------------------------------------------
version_declared("sed", "4.2.2", 0).


%----------------------------------------------------------------------------
% Package: shared-mime-info
%----------------------------------------------------------------------------
version_declared("shared-mime-info", "1.9", 0).
version_declared("shared-mime-info", "1.8", 1).

declared_dependency("shared-mime-info", "gettext", "build").
node("gettext") :- depends_on("shared-mime-info", "gettext"), node("shared-mime-info").

declared_dependency("shared-mime-info", "glib", "build").
declared_dependency("shared-mime-info", "glib", "link").
node("glib") :- depends_on("shared-mime-info", "glib"), node("shared-mime-info").

declared_dependency("shared-mime-info", "intltool", "build").
node("intltool") :- depends_on("shared-mime-info", "intltool"), node("shared-mime-info").

declared_dependency("shared-mime-info", "libxml2", "build").
declared_dependency("shared-mime-info", "libxml2", "link").
node("libxml2") :- depends_on("shared-mime-info", "libxml2"), node("shared-mime-info").

declared_dependency("shared-mime-info", "pkgconfig", "build").
node("pkgconfig") :- depends_on("shared-mime-info", "pkgconfig"), node("shared-mime-info").


%----------------------------------------------------------------------------
% Package: slurm
%----------------------------------------------------------------------------
version_declared("slurm", "18-08-0-1", 0).
version_declared("slurm", "17-11-9-2", 1).
version_declared("slurm", "17-02-6-1", 2).

variant("slurm", "gtk").
variant_single_value("slurm", "gtk").
variant_default_value("slurm", "gtk", "False").
variant_possible_value("slurm", "gtk", "False").
variant_possible_value("slurm", "gtk", "True").

variant("slurm", "hdf5").
variant_single_value("slurm", "hdf5").
variant_default_value("slurm", "hdf5", "False").
variant_possible_value("slurm", "hdf5", "False").
variant_possible_value("slurm", "hdf5", "True").

variant("slurm", "hwloc").
variant_single_value("slurm", "hwloc").
variant_default_value("slurm", "hwloc", "False").
variant_possible_value("slurm", "hwloc", "False").
variant_possible_value("slurm", "hwloc", "True").

variant("slurm", "mariadb").
variant_single_value("slurm", "mariadb").
variant_default_value("slurm", "mariadb", "False").
variant_possible_value("slurm", "mariadb", "False").
variant_possible_value("slurm", "mariadb", "True").

variant("slurm", "pmix").
variant_single_value("slurm", "pmix").
variant_default_value("slurm", "pmix", "False").
variant_possible_value("slurm", "pmix", "False").
variant_possible_value("slurm", "pmix", "True").

variant("slurm", "readline").
variant_single_value("slurm", "readline").
variant_default_value("slurm", "readline", "True").
variant_possible_value("slurm", "readline", "False").
variant_possible_value("slurm", "readline", "True").

declared_dependency("slurm", "curl", "build").
declared_dependency("slurm", "curl", "link").
node("curl") :- depends_on("slurm", "curl"), node("slurm").

declared_dependency("slurm", "glib", "build").
declared_dependency("slurm", "glib", "link").
node("glib") :- depends_on("slurm", "glib"), node("slurm").

declared_dependency("slurm", "gtkplus", "build") :- node("slurm"), variant_value("slurm", "gtk", "True").
declared_dependency("slurm", "gtkplus", "link") :- node("slurm"), variant_value("slurm", "gtk", "True").
node("gtkplus") :- depends_on("slurm", "gtkplus"), node("slurm"), variant_value("slurm", "gtk", "True").

declared_dependency("slurm", "hdf5", "build") :- node("slurm"), variant_value("slurm", "hdf5", "True").
declared_dependency("slurm", "hdf5", "link") :- node("slurm"), variant_value("slurm", "hdf5", "True").
node("hdf5") :- depends_on("slurm", "hdf5"), node("slurm"), variant_value("slurm", "hdf5", "True").

declared_dependency("slurm", "hwloc", "build") :- node("slurm"), variant_value("slurm", "hwloc", "True").
declared_dependency("slurm", "hwloc", "link") :- node("slurm"), variant_value("slurm", "hwloc", "True").
node("hwloc") :- depends_on("slurm", "hwloc"), node("slurm"), variant_value("slurm", "hwloc", "True").

declared_dependency("slurm", "json-c", "build").
declared_dependency("slurm", "json-c", "link").
node("json-c") :- depends_on("slurm", "json-c"), node("slurm").

declared_dependency("slurm", "lz4", "build").
declared_dependency("slurm", "lz4", "link").
node("lz4") :- depends_on("slurm", "lz4"), node("slurm").

declared_dependency("slurm", "mariadb", "build") :- node("slurm"), variant_value("slurm", "mariadb", "True").
declared_dependency("slurm", "mariadb", "link") :- node("slurm"), variant_value("slurm", "mariadb", "True").
node("mariadb") :- depends_on("slurm", "mariadb"), node("slurm"), variant_value("slurm", "mariadb", "True").

declared_dependency("slurm", "munge", "build").
declared_dependency("slurm", "munge", "link").
node("munge") :- depends_on("slurm", "munge"), node("slurm").

declared_dependency("slurm", "openssl", "build").
declared_dependency("slurm", "openssl", "link").
node("openssl") :- depends_on("slurm", "openssl"), node("slurm").

declared_dependency("slurm", "pkgconfig", "build").
node("pkgconfig") :- depends_on("slurm", "pkgconfig"), node("slurm").

declared_dependency("slurm", "pmix", "build") :- node("slurm"), variant_value("slurm", "pmix", "True").
declared_dependency("slurm", "pmix", "link") :- node("slurm"), variant_value("slurm", "pmix", "True").
node("pmix") :- depends_on("slurm", "pmix"), node("slurm"), variant_value("slurm", "pmix", "True").

declared_dependency("slurm", "readline", "build") :- node("slurm"), variant_value("slurm", "readline", "True").
declared_dependency("slurm", "readline", "link") :- node("slurm"), variant_value("slurm", "readline", "True").
node("readline") :- depends_on("slurm", "readline"), node("slurm"), variant_value("slurm", "readline", "True").

declared_dependency("slurm", "zlib", "build").
declared_dependency("slurm", "zlib", "link").
node("zlib") :- depends_on("slurm", "zlib"), node("slurm").


%----------------------------------------------------------------------------
% Package: spectrum-mpi
%----------------------------------------------------------------------------


%----------------------------------------------------------------------------
% Package: sqlite
%----------------------------------------------------------------------------
version_declared("sqlite", "3.30.1", 0).
version_declared("sqlite", "3.30.0", 1).
version_declared("sqlite", "3.29.0", 2).
version_declared("sqlite", "3.28.0", 3).
version_declared("sqlite", "3.27.2", 4).
version_declared("sqlite", "3.27.1", 5).
version_declared("sqlite", "3.27.0", 6).
version_declared("sqlite", "3.26.0", 7).

variant("sqlite", "column_metadata").
variant_single_value("sqlite", "column_metadata").
variant_default_value("sqlite", "column_metadata", "False").
variant_possible_value("sqlite", "column_metadata", "False").
variant_possible_value("sqlite", "column_metadata", "True").

variant("sqlite", "fts").
variant_single_value("sqlite", "fts").
variant_default_value("sqlite", "fts", "True").
variant_possible_value("sqlite", "fts", "False").
variant_possible_value("sqlite", "fts", "True").

variant("sqlite", "functions").
variant_single_value("sqlite", "functions").
variant_default_value("sqlite", "functions", "False").
variant_possible_value("sqlite", "functions", "False").
variant_possible_value("sqlite", "functions", "True").

variant("sqlite", "rtree").
variant_single_value("sqlite", "rtree").
variant_default_value("sqlite", "rtree", "False").
variant_possible_value("sqlite", "rtree", "False").
variant_possible_value("sqlite", "rtree", "True").

declared_dependency("sqlite", "readline", "build").
declared_dependency("sqlite", "readline", "link").
node("readline") :- depends_on("sqlite", "readline"), node("sqlite").

declared_dependency("sqlite", "zlib", "build").
declared_dependency("sqlite", "zlib", "link").
node("zlib") :- depends_on("sqlite", "zlib"), node("sqlite").


%----------------------------------------------------------------------------
% Package: swig
%----------------------------------------------------------------------------
version_declared("swig", "4.0.0", 0).
version_declared("swig", "3.0.12", 1).
version_declared("swig", "3.0.11", 2).
version_declared("swig", "3.0.10", 3).
version_declared("swig", "3.0.8", 4).
version_declared("swig", "3.0.2", 5).
version_declared("swig", "2.0.12", 6).
version_declared("swig", "2.0.2", 7).
version_declared("swig", "1.3.40", 8).
version_declared("swig", "fortran", 9).
version_declared("swig", "master", 10).

declared_dependency("swig", "autoconf", "build") :- node("swig"), 1 { version("swig", "fortran") } 1.
node("autoconf") :- depends_on("swig", "autoconf"), node("swig"), 1 { version("swig", "fortran") } 1.
declared_dependency("swig", "autoconf", "build") :- node("swig"), 1 { version("swig", "master") } 1.
node("autoconf") :- depends_on("swig", "autoconf"), node("swig"), 1 { version("swig", "master") } 1.

declared_dependency("swig", "automake", "build") :- node("swig"), 1 { version("swig", "fortran") } 1.
node("automake") :- depends_on("swig", "automake"), node("swig"), 1 { version("swig", "fortran") } 1.
declared_dependency("swig", "automake", "build") :- node("swig"), 1 { version("swig", "master") } 1.
node("automake") :- depends_on("swig", "automake"), node("swig"), 1 { version("swig", "master") } 1.

declared_dependency("swig", "libtool", "build") :- node("swig"), 1 { version("swig", "fortran") } 1.
node("libtool") :- depends_on("swig", "libtool"), node("swig"), 1 { version("swig", "fortran") } 1.
declared_dependency("swig", "libtool", "build") :- node("swig"), 1 { version("swig", "master") } 1.
node("libtool") :- depends_on("swig", "libtool"), node("swig"), 1 { version("swig", "master") } 1.

declared_dependency("swig", "pcre", "build").
declared_dependency("swig", "pcre", "link").
node("pcre") :- depends_on("swig", "pcre"), node("swig").

declared_dependency("swig", "pkgconfig", "build").
node("pkgconfig") :- depends_on("swig", "pkgconfig"), node("swig").


%----------------------------------------------------------------------------
% Package: tar
%----------------------------------------------------------------------------
version_declared("tar", "1.32", 0).
version_declared("tar", "1.31", 1).
version_declared("tar", "1.30", 2).
version_declared("tar", "1.29", 3).
version_declared("tar", "1.28", 4).

declared_dependency("tar", "libiconv", "build").
declared_dependency("tar", "libiconv", "link").
node("libiconv") :- depends_on("tar", "libiconv"), node("tar").


%----------------------------------------------------------------------------
% Package: tcl
%----------------------------------------------------------------------------
version_declared("tcl", "8.6.8", 0).
version_declared("tcl", "8.6.6", 1).
version_declared("tcl", "8.6.5", 2).
version_declared("tcl", "8.6.4", 3).
version_declared("tcl", "8.6.3", 4).
version_declared("tcl", "8.5.19", 5).

declared_dependency("tcl", "zlib", "build").
declared_dependency("tcl", "zlib", "link").
node("zlib") :- depends_on("tcl", "zlib"), node("tcl").


%----------------------------------------------------------------------------
% Package: texinfo
%----------------------------------------------------------------------------
version_declared("texinfo", "6.5", 0).
version_declared("texinfo", "6.3", 1).
version_declared("texinfo", "6.0", 2).
version_declared("texinfo", "5.2", 3).
version_declared("texinfo", "5.1", 4).
version_declared("texinfo", "5.0", 5).

declared_dependency("texinfo", "perl", "build").
declared_dependency("texinfo", "perl", "link").
node("perl") :- depends_on("texinfo", "perl"), node("texinfo").


%----------------------------------------------------------------------------
% Package: tix
%----------------------------------------------------------------------------
version_declared("tix", "8.4.3", 0).

declared_dependency("tix", "tcl", "build").
declared_dependency("tix", "tcl", "link").
node("tcl") :- depends_on("tix", "tcl"), node("tix").
1 { version("tcl", "8.5.19") } 1 :- depends_on("tix", "tcl"), node("tix").

declared_dependency("tix", "tk", "build").
declared_dependency("tix", "tk", "link").
node("tk") :- depends_on("tix", "tk"), node("tix").
1 { version("tk", "8.5.19") } 1 :- depends_on("tix", "tk"), node("tix").


%----------------------------------------------------------------------------
% Package: tk
%----------------------------------------------------------------------------
version_declared("tk", "8.6.8", 0).
version_declared("tk", "8.6.6", 1).
version_declared("tk", "8.6.5", 2).
version_declared("tk", "8.6.3", 3).
version_declared("tk", "8.5.19", 4).

variant("tk", "xft").
variant_single_value("tk", "xft").
variant_default_value("tk", "xft", "True").
variant_possible_value("tk", "xft", "False").
variant_possible_value("tk", "xft", "True").

variant("tk", "xss").
variant_single_value("tk", "xss").
variant_default_value("tk", "xss", "True").
variant_possible_value("tk", "xss", "False").
variant_possible_value("tk", "xss", "True").

declared_dependency("tk", "libx11", "build").
declared_dependency("tk", "libx11", "link").
node("libx11") :- depends_on("tk", "libx11"), node("tk").

declared_dependency("tk", "libxft", "build") :- node("tk"), variant_value("tk", "xft", "True").
declared_dependency("tk", "libxft", "link") :- node("tk"), variant_value("tk", "xft", "True").
node("libxft") :- depends_on("tk", "libxft"), node("tk"), variant_value("tk", "xft", "True").

declared_dependency("tk", "libxscrnsaver", "build") :- node("tk"), variant_value("tk", "xss", "True").
declared_dependency("tk", "libxscrnsaver", "link") :- node("tk"), variant_value("tk", "xss", "True").
node("libxscrnsaver") :- depends_on("tk", "libxscrnsaver"), node("tk"), variant_value("tk", "xss", "True").

declared_dependency("tk", "tcl", "build").
declared_dependency("tk", "tcl", "link").
node("tcl") :- depends_on("tk", "tcl"), node("tk").
declared_dependency("tk", "tcl", "build") :- node("tk"), 1 { version("tk", "8.6.3"); version("tk", "8.6.5"); version("tk", "8.6.6"); version("tk", "8.6.8") } 1.
declared_dependency("tk", "tcl", "link") :- node("tk"), 1 { version("tk", "8.6.3"); version("tk", "8.6.5"); version("tk", "8.6.6"); version("tk", "8.6.8") } 1.
node("tcl") :- depends_on("tk", "tcl"), node("tk"), 1 { version("tk", "8.6.3"); version("tk", "8.6.5"); version("tk", "8.6.6"); version("tk", "8.6.8") } 1.
1 { version("tcl", "8.6.3"); version("tcl", "8.6.4"); version("tcl", "8.6.5"); version("tcl", "8.6.6"); version("tcl", "8.6.8") } 1 :- depends_on("tk", "tcl"), node("tk"), 1 { version("tk", "8.6.3"); version("tk", "8.6.5"); version("tk", "8.6.6"); version("tk", "8.6.8") } 1.


%----------------------------------------------------------------------------
% Package: ucx
%----------------------------------------------------------------------------
version_declared("ucx", "1.6.1", 0).
version_declared("ucx", "1.6.0", 1).
version_declared("ucx", "1.5.2", 2).
version_declared("ucx", "1.5.1", 3).
version_declared("ucx", "1.5.0", 4).
version_declared("ucx", "1.4.0", 5).
version_declared("ucx", "1.3.1", 6).
version_declared("ucx", "1.3.0", 7).
version_declared("ucx", "1.2.2", 8).
version_declared("ucx", "1.2.1", 9).
version_declared("ucx", "1.2.0", 10).

variant("ucx", "thread_multiple").
variant_single_value("ucx", "thread_multiple").
variant_default_value("ucx", "thread_multiple", "False").
variant_possible_value("ucx", "thread_multiple", "False").
variant_possible_value("ucx", "thread_multiple", "True").

declared_dependency("ucx", "numactl", "build").
declared_dependency("ucx", "numactl", "link").
node("numactl") :- depends_on("ucx", "numactl"), node("ucx").

declared_dependency("ucx", "rdma-core", "build").
declared_dependency("ucx", "rdma-core", "link").
node("rdma-core") :- depends_on("ucx", "rdma-core"), node("ucx").


%----------------------------------------------------------------------------
% Package: util-linux
%----------------------------------------------------------------------------
version_declared("util-linux", "2.29.2", 0).
version_declared("util-linux", "2.29.1", 1).
version_declared("util-linux", "2.25", 2).

variant("util-linux", "libuuid").
variant_single_value("util-linux", "libuuid").
variant_default_value("util-linux", "libuuid", "True").
variant_possible_value("util-linux", "libuuid", "False").
variant_possible_value("util-linux", "libuuid", "True").

declared_dependency("util-linux", "pkgconfig", "build").
declared_dependency("util-linux", "pkgconfig", "link").
node("pkgconfig") :- depends_on("util-linux", "pkgconfig"), node("util-linux").

declared_dependency("util-linux", "python", "build").
declared_dependency("util-linux", "python", "link").
node("python") :- depends_on("util-linux", "python"), node("util-linux").


%----------------------------------------------------------------------------
% Package: util-macros
%----------------------------------------------------------------------------
version_declared("util-macros", "1.19.1", 0).
version_declared("util-macros", "1.19.0", 1).


%----------------------------------------------------------------------------
% Package: valgrind
%----------------------------------------------------------------------------
version_declared("valgrind", "3.15.0", 0).
version_declared("valgrind", "3.14.0", 1).
version_declared("valgrind", "3.13.0", 2).
version_declared("valgrind", "3.12.0", 3).
version_declared("valgrind", "3.11.0", 4).
version_declared("valgrind", "3.10.1", 5).
version_declared("valgrind", "3.10.0", 6).
version_declared("valgrind", "develop", 7).

variant("valgrind", "boost").
variant_single_value("valgrind", "boost").
variant_default_value("valgrind", "boost", "True").
variant_possible_value("valgrind", "boost", "False").
variant_possible_value("valgrind", "boost", "True").

variant("valgrind", "mpi").
variant_single_value("valgrind", "mpi").
variant_default_value("valgrind", "mpi", "True").
variant_possible_value("valgrind", "mpi", "False").
variant_possible_value("valgrind", "mpi", "True").

variant("valgrind", "only64bit").
variant_single_value("valgrind", "only64bit").
variant_default_value("valgrind", "only64bit", "True").
variant_possible_value("valgrind", "only64bit", "False").
variant_possible_value("valgrind", "only64bit", "True").

variant("valgrind", "ubsan").
variant_single_value("valgrind", "ubsan").
variant_default_value("valgrind", "ubsan", "False").
variant_possible_value("valgrind", "ubsan", "False").
variant_possible_value("valgrind", "ubsan", "True").

declared_dependency("valgrind", "autoconf", "build") :- node("valgrind"), 1 { version("valgrind", "develop") } 1.
node("autoconf") :- depends_on("valgrind", "autoconf"), node("valgrind"), 1 { version("valgrind", "develop") } 1.

declared_dependency("valgrind", "automake", "build") :- node("valgrind"), 1 { version("valgrind", "develop") } 1.
node("automake") :- depends_on("valgrind", "automake"), node("valgrind"), 1 { version("valgrind", "develop") } 1.

declared_dependency("valgrind", "boost", "build") :- node("valgrind"), variant_value("valgrind", "boost", "True").
declared_dependency("valgrind", "boost", "link") :- node("valgrind"), variant_value("valgrind", "boost", "True").
node("boost") :- depends_on("valgrind", "boost"), node("valgrind"), variant_value("valgrind", "boost", "True").

declared_dependency("valgrind", "libtool", "build") :- node("valgrind"), 1 { version("valgrind", "develop") } 1.
node("libtool") :- depends_on("valgrind", "libtool"), node("valgrind"), 1 { version("valgrind", "develop") } 1.

declared_dependency("valgrind", "mpi", "build") :- node("valgrind"), variant_value("valgrind", "mpi", "True").
declared_dependency("valgrind", "mpi", "link") :- node("valgrind"), variant_value("valgrind", "mpi", "True").
node("mpi") :- depends_on("valgrind", "mpi"), node("valgrind"), variant_value("valgrind", "mpi", "True").


%----------------------------------------------------------------------------
% Package: veclibfort
%----------------------------------------------------------------------------
version_declared("veclibfort", "0.4.2", 0).
version_declared("veclibfort", "develop", 1).

variant("veclibfort", "shared").
variant_single_value("veclibfort", "shared").
variant_default_value("veclibfort", "shared", "True").
variant_possible_value("veclibfort", "shared", "False").
variant_possible_value("veclibfort", "shared", "True").


%----------------------------------------------------------------------------
% Package: wget
%----------------------------------------------------------------------------
version_declared("wget", "1.20.3", 0).
version_declared("wget", "1.19.1", 1).
version_declared("wget", "1.17", 2).
version_declared("wget", "1.16", 3).

variant("wget", "libpsl").
variant_single_value("wget", "libpsl").
variant_default_value("wget", "libpsl", "False").
variant_possible_value("wget", "libpsl", "False").
variant_possible_value("wget", "libpsl", "True").

variant("wget", "pcre").
variant_single_value("wget", "pcre").
variant_default_value("wget", "pcre", "False").
variant_possible_value("wget", "pcre", "False").
variant_possible_value("wget", "pcre", "True").

variant("wget", "python").
variant_single_value("wget", "python").
variant_default_value("wget", "python", "False").
variant_possible_value("wget", "python", "False").
variant_possible_value("wget", "python", "True").

variant("wget", "ssl").
variant_single_value("wget", "ssl").
variant_default_value("wget", "ssl", "openssl").
variant_possible_value("wget", "ssl", "gnutls").
variant_possible_value("wget", "ssl", "openssl").

variant("wget", "zlib").
variant_single_value("wget", "zlib").
variant_default_value("wget", "zlib", "True").
variant_possible_value("wget", "zlib", "False").
variant_possible_value("wget", "zlib", "True").

declared_dependency("wget", "gettext", "build").
node("gettext") :- depends_on("wget", "gettext"), node("wget").

declared_dependency("wget", "gnutls", "build") :- node("wget"), variant_value("wget", "ssl", "gnutls").
declared_dependency("wget", "gnutls", "link") :- node("wget"), variant_value("wget", "ssl", "gnutls").
node("gnutls") :- depends_on("wget", "gnutls"), node("wget"), variant_value("wget", "ssl", "gnutls").

declared_dependency("wget", "libiconv", "build").
declared_dependency("wget", "libiconv", "link").
node("libiconv") :- depends_on("wget", "libiconv"), node("wget").

declared_dependency("wget", "libpsl", "build") :- node("wget"), variant_value("wget", "libpsl", "True").
declared_dependency("wget", "libpsl", "link") :- node("wget"), variant_value("wget", "libpsl", "True").
node("libpsl") :- depends_on("wget", "libpsl"), node("wget"), variant_value("wget", "libpsl", "True").

declared_dependency("wget", "openssl", "build") :- node("wget"), variant_value("wget", "ssl", "openssl").
declared_dependency("wget", "openssl", "link") :- node("wget"), variant_value("wget", "ssl", "openssl").
node("openssl") :- depends_on("wget", "openssl"), node("wget"), variant_value("wget", "ssl", "openssl").

declared_dependency("wget", "pcre", "build") :- node("wget"), variant_value("wget", "pcre", "True").
declared_dependency("wget", "pcre", "link") :- node("wget"), variant_value("wget", "pcre", "True").
node("pcre") :- depends_on("wget", "pcre"), node("wget"), variant_value("wget", "pcre", "True").

declared_dependency("wget", "perl", "build").
node("perl") :- depends_on("wget", "perl"), node("wget").

declared_dependency("wget", "pkgconfig", "build").
node("pkgconfig") :- depends_on("wget", "pkgconfig"), node("wget").

declared_dependency("wget", "python", "build") :- node("wget"), variant_value("wget", "python", "True").
node("python") :- depends_on("wget", "python"), node("wget"), variant_value("wget", "python", "True").
1 { version("python", "3.1.5"); version("python", "3.2.6"); version("python", "3.3.6"); version("python", "3.4.3"); version("python", "3.4.10"); version("python", "3.5.0"); version("python", "3.5.1"); version("python", "3.5.2"); version("python", "3.5.7"); version("python", "3.6.0"); version("python", "3.6.1"); version("python", "3.6.2"); version("python", "3.6.3"); version("python", "3.6.4"); version("python", "3.6.5"); version("python", "3.6.6"); version("python", "3.6.7"); version("python", "3.6.8"); version("python", "3.7.0"); version("python", "3.7.1"); version("python", "3.7.2"); version("python", "3.7.3"); version("python", "3.7.4"); version("python", "3.7.5"); version("python", "3.7.6"); version("python", "3.8.0"); version("python", "3.8.1") } 1 :- depends_on("wget", "python"), node("wget"), variant_value("wget", "python", "True").

declared_dependency("wget", "valgrind", "test").
node("valgrind") :- depends_on("wget", "valgrind"), node("wget").

declared_dependency("wget", "zlib", "build") :- node("wget"), variant_value("wget", "zlib", "True").
declared_dependency("wget", "zlib", "link") :- node("wget"), variant_value("wget", "zlib", "True").
node("zlib") :- depends_on("wget", "zlib"), node("wget"), variant_value("wget", "zlib", "True").


%----------------------------------------------------------------------------
% Package: xcb-proto
%----------------------------------------------------------------------------
version_declared("xcb-proto", "1.13", 0).
version_declared("xcb-proto", "1.12", 1).
version_declared("xcb-proto", "1.11", 2).


%----------------------------------------------------------------------------
% Package: xextproto
%----------------------------------------------------------------------------
version_declared("xextproto", "7.3.0", 0).

declared_dependency("xextproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("xextproto", "pkgconfig"), node("xextproto").

declared_dependency("xextproto", "util-macros", "build").
node("util-macros") :- depends_on("xextproto", "util-macros"), node("xextproto").


%----------------------------------------------------------------------------
% Package: xineramaproto
%----------------------------------------------------------------------------
version_declared("xineramaproto", "1.2.1", 0).

declared_dependency("xineramaproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("xineramaproto", "pkgconfig"), node("xineramaproto").

declared_dependency("xineramaproto", "util-macros", "build").
node("util-macros") :- depends_on("xineramaproto", "util-macros"), node("xineramaproto").


%----------------------------------------------------------------------------
% Package: xproto
%----------------------------------------------------------------------------
version_declared("xproto", "7.0.31", 0).
version_declared("xproto", "7.0.29", 1).

declared_dependency("xproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("xproto", "pkgconfig"), node("xproto").

declared_dependency("xproto", "util-macros", "build").
node("util-macros") :- depends_on("xproto", "util-macros"), node("xproto").


%----------------------------------------------------------------------------
% Package: xtrans
%----------------------------------------------------------------------------
version_declared("xtrans", "1.3.5", 0).

declared_dependency("xtrans", "pkgconfig", "build").
node("pkgconfig") :- depends_on("xtrans", "pkgconfig"), node("xtrans").

declared_dependency("xtrans", "util-macros", "build").
node("util-macros") :- depends_on("xtrans", "util-macros"), node("xtrans").


%----------------------------------------------------------------------------
% Package: xz
%----------------------------------------------------------------------------
version_declared("xz", "5.2.4", 0).
version_declared("xz", "5.2.3", 1).
version_declared("xz", "5.2.2", 2).
version_declared("xz", "5.2.0", 3).


%----------------------------------------------------------------------------
% Package: zlib
%----------------------------------------------------------------------------
version_declared("zlib", "1.2.11", 0).
version_declared("zlib", "1.2.8", 1).
version_declared("zlib", "1.2.3", 2).

variant("zlib", "optimize").
variant_single_value("zlib", "optimize").
variant_default_value("zlib", "optimize", "True").
variant_possible_value("zlib", "optimize", "False").
variant_possible_value("zlib", "optimize", "True").

variant("zlib", "pic").
variant_single_value("zlib", "pic").
variant_default_value("zlib", "pic", "True").
variant_possible_value("zlib", "pic", "False").
variant_possible_value("zlib", "pic", "True").

variant("zlib", "shared").
variant_single_value("zlib", "shared").
variant_default_value("zlib", "shared", "True").
variant_possible_value("zlib", "shared", "False").
variant_possible_value("zlib", "shared", "True").


%============================================================================
% Spec Constraints
%============================================================================
root("hdf5").

%----------------------------------------------------------------------------
% Spec: hdf5
%----------------------------------------------------------------------------
node("hdf5").

%=============================================================================-
% Display Results
%
% This section determines what parts of the model are printed at the end
%==============================================================================
#show node/1.
#show depends_on/3.
#show version/2.
#show variant_value/3.
#show node_platform/2.
#show node_os/2.
#show node_target/2.
#show node_compiler/2.
#show node_compiler_version/3.
#show node_flag/3.
#show node_flag_compiler_default/1.
#show node_flag_source/2.
#show no_flags/2.
