%==============================================================================
% The symbol compatitiblity model looks at elf symbols
%==============================================================================

%=============================================================================
% Matching function and variable symbols
% symbols are missing if they are needed (present in the working library),
% not undefined in the working library (indicating they come from elsewhere)
% and undefined in both the potential library and binary.
%=============================================================================

% These are symbols to skip checking (profiling and other)
skip_symbol("_ITM_deregisterTMCloneTable").
skip_symbol("__gmon_start__").
skip_symbol("_ITM_registerTMCloneTable").

% ask gil about datalog
% don't do hashes right now, associate symbols with version of package
% tree versions of zlib, associate symbols with versions instead of hash


%----------------------------------------------------------------------------
% Corpus symbols: libtcl8.6.so
%----------------------------------------------------------------------------

% model 1: base (spack solver)
% model 2: symbols
% model 3: libabigail
% model 4: type/location model "code centric model"
% model 5: inlined code "data centric model" 

% something is a symbol if any binary has it
symbol :- has_symbol(_, Symbol).

% a package corpus needs a symbol if:
needs_symbol(Package, Version, Symbol, Corpus)

    % it's not one flagged to skip
    :- not skip_symbol(Symbol),

    % the corpus has it
    corpus(Package, Version, Corpus),

    % the corpus has the symbol
    has_symbol(Corpus, Symbol).


% A symbol is undefined for a package and corpus
% (a corpus is a binary/library provided by the package) if:
undefined_symbol(Package, Version, Symbol, Corpus)

    % the package needs the symbol
    :- needs_symbol(Package, Version, Symbol, Corpus),

    % and it's definition is UND
    symbol_definition(Corpus, Symbol, "UND").

% a symbol is undefined for a package version if
undefined_symbol(Package, Version, Symbol) 

    % it's undefined in any corpora
    :- undefined_symbol(Package, Version, Symbol, _).


% A symbol is defined for a package version if:
defined_symbol(Package, Version, Symbol, Corpus, Definition)

    % the package needs the symbol
    :- needs_symbol(Package, Version, Symbol, Corpus),

    % the corpus has a symbol definition
    symbol_definition(Corpus, Symbol, Definition),

    % and definition != UND
    Definition != "UND".

% A symbol is defined for a package verison across all corpora if
defined_symbol(Package, Version, Symbol)

    % it's defined for any corpora
    :- defined_symbol(Package, Version, Symbol, _, _).

% A package is abi compatible with a dependency if
%abi_compatible(Package, Dependency) :-
%    not mismatch(Package, Dependency).

% This is the main "entry" function from concretize.lp
% the dependency checks hold
dependency_checks_hold(Package, Dependency, Type)

    :- node(Package),
    version(Package, Version),
    version(Dependency, DependencyVersion),    
    mismatch(Package, PackageVersion, Dependency, DependencyVersion, Type).


% There is a mismatch for a package and dependency if:
mismatch(Package, Version, Dependency, DependencyVersion, Type)

    % they are linkable
    :- linkable(Package, Dependency),

    % The package and dependency each have their own version
    version(Package, Version),
    version(Dependency, DependencyVersion),

    % The package has an undefined symbol
    undefined_symbol(Package, Version, Symbol),

    % the package depends on the dependency
    depends_on(Package, Dependency, Type),

    % and the symbol is not defined for the dependency
    not defined_symbol(Dependency, DependencyVersion, Symbol).


% a package and dependency are linkable if
linkable(Package, Dependency)

    % The package and dependency are nodes in the graph
    :- node(Package),
    node(Dependency),

    % And the dependency holds
    dependency_holds(Package, Dependency, _).

% transitive
% I don't know how we can have two versions here?
defined_symbol(Package, Version, Symbol)
    :- depends_on(Package, Dependency, Type), defined_symbol(Dependency, Version, Symbol).

:- depends_on(Package, Dependency, _),
   not dependency_checks_hold(Package, Dependency, _).
