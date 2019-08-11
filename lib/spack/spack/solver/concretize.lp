%=============================================================================
% Generate
%=============================================================================
% One version, arch, etc. per package
{ version(P, V) : version(P, V)} = 1              :- node(P).
{ arch_platform(P, A) : arch_platform(P, A) } = 1 :- node(P).
{ arch_os(P, A) : arch_os(P, A) } = 1             :- node(P).
{ arch_target(P, T) : arch_target(P, T) } = 1     :- node(P).

% one variant value for single-valued variants.
{ variant_value(P, V, X) : variant_value(P, V, X) } = 1
    :- node(P), variant(P, V), not variant_single_value(P, V).

%=============================================================================
% Define
%=============================================================================
% dependencies imply new nodes.
node(D) :- node(P), depends_on(P, D).

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------

% if a variant is set to anything, it is considered 'set'.
variant_set(P, V) :- variant_set(P, V, _).

% suppress wranings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant_set/3.

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(P, V, X) :- node(P), variant(P, V), variant_set(P, V, X).
variant_value(P, V, X) :- node(P), variant(P, V), not variant_set(P, V),
                 variant_default_value(P, V, X).

%-----------------------------------------------------------------------------
% Architecture semantics
%-----------------------------------------------------------------------------

% propagate platform, os, target downwards
arch_platform(D, A) :- node(D), depends_on(P, D), arch_platform(P, A).
arch_os(D, A) :- node(D), depends_on(P, D), arch_os(P, A).
arch_target(D, A) :- node(D), depends_on(P, D), arch_target(P, A).
