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


%----------------------------------------------------------------------------
% Corpus symbols: libtcl8.6.so
%----------------------------------------------------------------------------


% A symbol is undefined for a given binary if:
symbol_is_undefined(Package, Hash, Symbol, Binary)

    % it's a symbol
    :- symbol(Symbol),

    % it's not one flagged to skip
    not skip_symbol(Symbol),

    % the package with matching hash is a corpus
    corpus(Package, Hash, Binary),

    % it's a main corpus
    is_main_corpus(Package, Hash),

    % the corpus has the symbol (possibly reundant)
    has_symbol(Binary, Symbol),

    % and it's definition is UND
    symbol_definition(Binary, Symbol, "UND").


% A symbol is defined in a library for a dependency if:
symbol_is_defined(Package, Symbol, Dependency, DepHash, Library, Definition)

    % it's a symbol
    :- symbol(Symbol),

    % The package has the dependency
    depends_on(Package, Dependency),

    % The library belongs to the Dependency
    corpus(Dependency, DepHash, Library),

    % the library has a symbol definition
    symbol_definition(Library, Symbol, Definition),

    % and definition != UND
    Definition != "UND".


% A symbol is defined for a package across all binaries if
symbol_is_defined(Package, Hash, Symbol) 

    % any dependency has it
    :- symbol_is_defined(Package, Hash, Symbol, _, _, _).


% A symbol is missing for a binary if
symbol_is_missing(Package, Hash, Symbol, Binary)

    % it's undefined for the binary
    :- symbol_is_undefined(Package, Hash, Symbol, Binary),

    % and it's not defined for the package anywhere
    not symbol_is_defined(Package, Hash, Symbol).


% TODO add compiler to skip symbols

% A dependency is not ABI compatible for a package if
:- abi_compatible(Package), 

    % The symbol is missing
    symbol_is_missing(Package, _, _, _).
