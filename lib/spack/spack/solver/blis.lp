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
virtual("pkgconfig").
provides_virtual("pkg-config", "pkgconfig").
provides_virtual("pkgconf", "pkgconfig").

%----------------------------------------------------------------------------
% Default virtual providers
%----------------------------------------------------------------------------
default_provider_preference("pkgconfig", "pkgconf", 0).
default_provider_preference("pkgconfig", "pkg-config", 1).

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
% Package: diffutils
%----------------------------------------------------------------------------
version_declared("diffutils", "3.7", 0).
version_declared("diffutils", "3.6", 1).

declared_dependency("diffutils", "libiconv", "build").
declared_dependency("diffutils", "libiconv", "link").
node("libiconv") :- depends_on("diffutils", "libiconv"), node("diffutils").


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
% Package: gperf
%----------------------------------------------------------------------------
version_declared("gperf", "3.0.4", 0).


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
% Package: inputproto
%----------------------------------------------------------------------------
version_declared("inputproto", "2.3.2", 0).

declared_dependency("inputproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("inputproto", "pkgconfig"), node("inputproto").

declared_dependency("inputproto", "util-macros", "build").
node("util-macros") :- depends_on("inputproto", "util-macros"), node("inputproto").


%----------------------------------------------------------------------------
% Package: kbproto
%----------------------------------------------------------------------------
version_declared("kbproto", "1.0.7", 0).

declared_dependency("kbproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("kbproto", "pkgconfig"), node("kbproto").

declared_dependency("kbproto", "util-macros", "build").
node("util-macros") :- depends_on("kbproto", "util-macros"), node("kbproto").


%----------------------------------------------------------------------------
% Package: libbsd
%----------------------------------------------------------------------------
version_declared("libbsd", "0.10.0", 0).
version_declared("libbsd", "0.9.1", 1).
version_declared("libbsd", "0.9.0", 2).
version_declared("libbsd", "0.8.7", 3).
version_declared("libbsd", "0.8.6", 4).


%----------------------------------------------------------------------------
% Package: libffi
%----------------------------------------------------------------------------
version_declared("libffi", "3.2.1", 0).


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
% Package: libiconv
%----------------------------------------------------------------------------
version_declared("libiconv", "1.16", 0).
version_declared("libiconv", "1.15", 1).
version_declared("libiconv", "1.14", 2).


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
% Package: libpng
%----------------------------------------------------------------------------
version_declared("libpng", "1.6.37", 0).
version_declared("libpng", "1.2.57", 1).

declared_dependency("libpng", "zlib", "build").
declared_dependency("libpng", "zlib", "link").
node("zlib") :- depends_on("libpng", "zlib"), node("libpng").


%----------------------------------------------------------------------------
% Package: libpthread-stubs
%----------------------------------------------------------------------------
version_declared("libpthread-stubs", "0.4", 0).
version_declared("libpthread-stubs", "0.3", 1).


%----------------------------------------------------------------------------
% Package: libsigsegv
%----------------------------------------------------------------------------
version_declared("libsigsegv", "2.12", 0).
version_declared("libsigsegv", "2.11", 1).
version_declared("libsigsegv", "2.10", 2).


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
% Package: readline
%----------------------------------------------------------------------------
version_declared("readline", "8.0", 0).
version_declared("readline", "7.0", 1).
version_declared("readline", "6.3", 2).

declared_dependency("readline", "ncurses", "build").
declared_dependency("readline", "ncurses", "link").
node("ncurses") :- depends_on("readline", "ncurses"), node("readline").


%----------------------------------------------------------------------------
% Package: renderproto
%----------------------------------------------------------------------------
version_declared("renderproto", "0.11.1", 0).

declared_dependency("renderproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("renderproto", "pkgconfig"), node("renderproto").

declared_dependency("renderproto", "util-macros", "build").
node("util-macros") :- depends_on("renderproto", "util-macros"), node("renderproto").


%----------------------------------------------------------------------------
% Package: rpcsvc-proto
%----------------------------------------------------------------------------
version_declared("rpcsvc-proto", "1.4", 0).

declared_dependency("rpcsvc-proto", "gettext", "build").
declared_dependency("rpcsvc-proto", "gettext", "link").
node("gettext") :- depends_on("rpcsvc-proto", "gettext"), node("rpcsvc-proto").


%----------------------------------------------------------------------------
% Package: scrnsaverproto
%----------------------------------------------------------------------------
version_declared("scrnsaverproto", "1.2.2", 0).

declared_dependency("scrnsaverproto", "pkgconfig", "build").
node("pkgconfig") :- depends_on("scrnsaverproto", "pkgconfig"), node("scrnsaverproto").

declared_dependency("scrnsaverproto", "util-macros", "build").
node("util-macros") :- depends_on("scrnsaverproto", "util-macros"), node("scrnsaverproto").


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
% Package: util-macros
%----------------------------------------------------------------------------
version_declared("util-macros", "1.19.1", 0).
version_declared("util-macros", "1.19.0", 1).


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
root("blis").

%----------------------------------------------------------------------------
% Spec: blis
%----------------------------------------------------------------------------
node("blis").

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
