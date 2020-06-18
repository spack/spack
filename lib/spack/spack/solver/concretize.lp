%=============================================================================
% Generate
%=============================================================================

%-----------------------------------------------------------------------------
% Version semantics
%-----------------------------------------------------------------------------

% versions are declared w/priority -- declared with priority implies declared
version_declared(Package, Version) :- version_declared(Package, Version, _).

% If something is a package, it has only one version and that must be a
% declared version.
1 { version(Package, Version) : version_declared(Package, Version) } 1
 :- node(Package).

version_weight(Package, Weight)
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

% a node that provides a virtual is a provider
provider(Package, Virtual)
  :- node(Package), provides_virtual(Package, Virtual).

% for any virtual, there can be at most one provider in the DAG
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
node(Package) :- root(Package).
needed(Package) :- root(Package).
needed(Dependency) :- needed(Package), depends_on(Package, Dependency).
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
% Platform semantics
%-----------------------------------------------------------------------------
% one platform per node
1 { node_platform(Package, Platform) : node_platform(Packagee, Platform) } 1
  :- node(Package).

% if no platform is set, fall back to the default
node_platform(Package, Platform)
 :- node(Package),
    not node_platform_set(Package),
    node_platform_default(Platform).

% setting platform on a node is a hard constraint
node_platform(Package, Platform)
 :- node(Package), node_platform_set(Package, Platform).

% platform is set if set to anything
node_platform_set(Package) :- node_platform_set(Package, _).

#defined node_platform_set/2.  % avoid warnings

%-----------------------------------------------------------------------------
% OS semantics
%-----------------------------------------------------------------------------
% one os per node
1 { node_os(Package, OS) : os(OS) } 1 :- node(Package).

% node_os_set implies that the node must have that os
node_os(Package, OS) :- node(Package), node_os_set(Package, OS).
node_os_set(Package) :- node_os_set(Package, _).

% inherit OS along dependencies
node_os_inherit(Package, OS) :- node_os_set(Package, OS).
node_os_inherit(Dependency, OS)
  :- node_os_inherit(Package, OS), depends_on(Package, Dependency),
     not node_os_set(Dependency).
node_os_inherit(Package) :- node_os_inherit(Package, _).

% fall back to default if not set or inherited
node_os(Package, OS)
  :- node(Package),
     not node_os_set(Package), not node_os_inherit(Package),
     node_os_default(OS).

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

% compatibility rules for targets among nodes
node_target_match_pref(Package, Target) :- node_target_set(Package, Target).
node_target_match_pref(Dependency, Target)
  :- depends_on(Package, Dependency), node_target_match_pref(Package, Target),
     not node_target_set(Dependency, _).
node_target_match(Package, 1)
  :- node_target(Package, Target), node_target_match_pref(Package, Target).

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
 :- node_compiler_hard(Package, Compiler),
    node_compiler_version(Package, Compiler, V).
node_compiler_version_match_pref(Dependency, Compiler, V)
 :- depends_on(Package, Dependency),
    node_compiler_version_match_pref(Package, Compiler, V),
    not node_compiler_hard(Dependency, Compiler).
compiler_version_match(Package, 1)
 :- node_compiler_version(Package, Compiler, V),
    node_compiler_version_match_pref(Package, Compiler, V).

#defined node_compiler_hard/2.

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
    Weight@8,Package : version_weight(Package, Weight)
}.

% compiler preferences
#maximize{ Weight@7,Package : compiler_match(Package, Weight) }.
#minimize{ Weight@6,Package : compiler_weight(Package, Weight) }.

% fastest target for node

% TODO: if these are slightly different by compiler (e.g., skylake is
% best, gcc supports skylake and broadweell, clang's best is haswell)
% things seem to get really slow.
#maximize{ Weight@5,Package : node_target_match(Package, Weight) }.
#minimize{ Weight@4,Package : node_target_weight(Package, Weight) }.
