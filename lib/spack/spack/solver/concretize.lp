% -----------------------------------------
% Generate
% -----------------------------------------
% One version, arch, etc. per package
{ version(P, V) : version(P, V)} = 1              :- node(P).
{ arch_platform(P, A) : arch_platform(P, A) } = 1 :- node(P).
{ arch_os(P, A) : arch_os(P, A) } = 1             :- node(P).
{ arch_target(P, T) : arch_target(P, T) } = 1     :- node(P).

% one variant value for single-valued variants.
{ variant_value(P, V, X) : variant_value(P, V, X) } = 1
    :- node(P), variant(P, V), not variant_single_value(P, V).

% -----------------------------------------
% Define
% -----------------------------------------
% dependencies imply new nodes.
node(D) :- node(P), depends_on(P, D).

% propagate platform, os, target downwards
arch_platform(D, A) :- node(D), depends_on(P, D), arch_platform(P, A).
arch_os(D, A) :- node(D), depends_on(P, D), arch_os(P, A).
arch_target(D, A) :- node(D), depends_on(P, D), arch_target(P, A).

% if a variant is set to anything, it is considered 'set'.
variant_set(P, V) :- variant_set(P, V, _).

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(P, V, X) :- node(P), variant(P, V), variant_set(P, V, X).
