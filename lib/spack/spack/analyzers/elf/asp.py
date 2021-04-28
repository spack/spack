# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


try:
    import elftools
except ImportError:
    elftools = None

import re
import hashlib
from .corpus import Corpus, et
from spack.solver.asp import AspFunctionBuilder
from spack.util.executable import which
import spack.binary_distribution
import spack.solver.asp
import spack.main

fn = AspFunctionBuilder()


class ABIFactGenerator(object):
    """Class to set up and generate corpus ABI facts."""

    def __init__(self, gen):
        self.gen = gen

        # Filter down originally to needed symbols for smaller output
        self.needed_symbols = set()

        # Or any symbols to advise further parsing
        self.symbols = {}

        # A lookup of DIE children ids
        self.child_lookup = {}
        self.die_lookup = {}
        self.language = None

        global elftools

        if not elftools:
            with spack.bootstrap.ensure_bootstrap_configuration():
                spec = spack.spec.Spec("py-pyelftools")
                spec.concretize()
                spack.bootstrap.make_module_available(
                    'elftools', spec=spec, install=True
                )
                import elftools

    def generate_elf_symbols(self, corpora, detail=False):
        """For each corpus, write out elf symbols as facts.
        """
        for corpus in corpora:
            self.gen.h2("Corpus symbols: %s" % corpus.basename)

            for symbol, meta in corpus.elfsymbols.items():

                # It begins with a NULL symbol, not sure it's useful
                if not symbol or symbol not in self.needed_symbols:
                    continue

                self._generate_elf_symbol(corpus, symbol, meta, detail=detail)

    def _generate_elf_symbol(self, corpus, symbol, meta, detail=False):
        """Shared helped function to generate metadata for a symbol
        """
        # Prepare variables
        vinfo = meta['version_info']
        defined = meta['defined']

        # If the symbol has @@ in the name, it includes the version.
        if "@@" in symbol and not vinfo:
            symbol, _ = symbol.split('@', 1)

        self.gen.fact(fn.symbol_definition(corpus.basename, symbol, defined))
        self.gen.fact(fn.has_symbol(corpus.basename, symbol))

        if detail:
            # vis = meta['visibility']
            bind = meta['binding']

            # Additional elf metadata / details to generate
            self.gen.fact(fn.symbol_type(corpus.basename, symbol, meta['type']))
            # self.gen.fact(fn.symbol_version(corpus.basename, symbol, vinfo))
            self.gen.fact(fn.symbol_binding(corpus.basename, symbol, bind))
            # self.gen.fact(fn.symbol_visibility(corpus.basename, symbol, vis))

    def generate_elf_symbol(self, corpus, symbol, detail=True):
        """Given a specific elf symbol, generate it's defails if it's:

        1. a needed symbol, meaning exported by a main
        2. defined for the corpus in question
        """
        if symbol not in self.needed_symbols or corpus.basename not in self.symbols:
            return

        # Generate the symbol if its defined for the corpus
        if symbol in self.symbols[corpus.basename]:
            meta = corpus.elfsymbols[symbol]
            self._generate_elf_symbol(corpus, symbol, meta, detail=detail)

    def bytes2str(self, item):
        return elftools.common.py3compat.bytes2str(item)

    def set_needed_symbols(self, corpora, main):
        """
        Set needed symbols that we should filter to.
        """
        for corpus in corpora:
            if corpus.name == main:
                for symbol, _ in corpus.elfsymbols.items():
                    self.needed_symbols.add(symbol)

    def create_symbol_lookup(self, corpora):
        """
        Create a lookup (by corpus name) of symbols.

        We want to be able to parse DIEs and add names that match any symbol
        that is exported in the elf symbols, so we create these lookups.
        """
        for corpus in corpora:
            self.symbols[corpus.basename] = set()
            for symbol, _ in corpus.elfsymbols.items():
                self.symbols[corpus.basename].add(symbol)

    def _die_hash(self, die, corpus, parent):
        """
        We need a unique id for a die entry based on it's corpus, cu, content
        """
        hasher = hashlib.md5()
        hasher.update(str(die).encode("utf-8"))
        hasher.update(corpus.path.encode("utf-8"))
        hasher.update(str(die.cu.cu_offset).encode('utf-8'))
        if parent:
            hasher.update(parent.encode("utf-8"))
        return hasher.hexdigest()

    def generate_dwarf_information_entries(self, corpora):
        """
        Given a list of corpora, add needed libraries from dynamic tags.

        Given that we know overlapping interfaces (we do not), for each we will
        need to identify a set of variables/type for each. Functions: means
        parameters and returns. Global variables: just the variable.
        Exceptions: the exception object. Constants: name and type.
        """
        # We will keep a lookup of die
        for corpus in corpora:

            # Add to child and die lookup, for redundancy check
            if corpus.path not in self.die_lookup:
                self.die_lookup[corpus.path] = {}
            if corpus.path not in self.child_lookup:
                self.child_lookup[corpus.path] = {}

            for die in corpus.iter_dwarf_information_entries():

                # Skip entries without tags
                if not die.tag:
                    continue

                # Parse the die entry!
                self._parse_die_children(corpus, die)

    def _get_tag(self, die):
        """Get a clingo appropriate tag name.

        The die tag needs to be parsed to be all lowercase, and for some
        die tags, we want to remove the "Dwarf specific words." (e.g.,
        a subprogram --> a function, along with "DW_TAG".
        """
        tag = die.tag.lower()

        # A subprogram is a function
        if "subprogram" in tag:
            tag = re.sub('subprogram', 'function', tag)

        return tag.replace('dw_tag_', '', 1)

    def _parse_die_children(self, corpus, die, parent=None):
        """
        Parse die children, writing facts for attributions and relationships.

        Parse die children will loop recursively through dwarf information
        entries, and based on the type, generate facts for it, ensuring that
        we only parse interfaces that are represented as symbols.
        """
        # Get the tag for the die
        tag = self._get_tag(die)

        # Keep track of unique id (hash of attributes, parent, and corpus)
        die.unique_id = self._die_hash(die, corpus, parent)

        # If it's already been parsed, skip
        if die.abbrev_code in self.die_lookup[corpus.path]:
            return

        # Add to the lookup
        self.die_lookup[corpus.path][die.abbrev_code] = die

        # Parse common attributes of symbols
        self._parse_common_attributes(corpus, die, tag)

        # We keep a handle on the root to return
        if not parent:
            parent = die.unique_id

        if die.has_children:
            for child in die.iter_children():
                self._parse_die_children(corpus, child, parent)

    def get_location(self, die):
        """Given a DW_AT_location parameter, parse it to get a location.
        """
        location_lists = die.dwarfinfo.location_lists()
        loc_parser = et.locationlists.LocationParser(location_lists)

        # https://github.com/eliben/pyelftools/blob/master/examples/dwarf_location_info.py
        for attr in et.py3compat.itervalues(die.attributes):
            if loc_parser.attribute_has_location(attr, die.cu['version']):
                loc = loc_parser.parse_from_attribute(attr, die.cu['version'])

                # Attribute itself contains location information
                if isinstance(loc, et.locationlists.LocationExpr):
                    return et.dwarf.describe_DWARF_expr(loc.loc_expr,
                                                        die.dwarfinfo.structs,
                                                        die.cu.cu_offset)

                # Attribute is reference to .debug_loc section
                elif isinstance(loc, list):
                    print('LIST')
                    import IPython
                    IPython.embed()
                    print(show_loclist(loc, die.dwarfinfo, '      ', die.cu.cu_offset))
                    import sys
                    sys.exit(0)

    def _parse_common_attributes(self, corpus, die, tag):
        """
        Many share these attributes, so we have a common function to parse.
        """
        # We want to represent things as names, locations, and types
        name = None
        loc = None
        die_type = None

        # We only care if it has a name, and the name is an elf symbol
        if "DW_AT_linkage_name" in die.attributes:
            name = self.bytes2str(die.attributes["DW_AT_linkage_name"].value)

        elif "DW_AT_name" in die.attributes:
            name = self.bytes2str(die.attributes["DW_AT_name"].value)

        # If it doesn't have a name, or its not a known symbol, continue
        if not name or name not in self.symbols[corpus.basename]:
            return

        # We found metadata for a symbol! :D
        self.generate_elf_symbol(corpus, name, detail=True)

        # Determine if we have a location and die_type
        if "DW_AT_type" in die.attributes:
            die_type = self._get_die_type(die)

        if "DW_AT_location" in die.attributes:
            loc = self.get_location(die)

        # If we have a parent, we can add it
        parent = die.get_parent()
        pname = None
        if "DW_AT_name" in parent.attributes:
            pname = os.path.basename(
                self.bytes2str(parent.attributes['DW_AT_name'].value))

        # Case 1: we have a parent, loc, name, and die_type
        # (e.g., a formal_parameter)
        if die_type and pname and loc:
            fact = fn.abi_typelocation(corpus.basename, pname, name, die_type, loc)

        # Case 2: just die_type and loc (e.g., a variable)
        elif die_type and loc:
            fact = fn.abi_typelocation(corpus.basename, name, die_type, loc)

        # If we have a die_type and the tag is function, it'a s return type
        # abi_typelocation('exe', 'main', 'int', 'return')
        # return values are imports
        elif tag == "function" and pname and die_type:
            cname = corpus.basename
            fact = fn.abi_typelocation(cname, pname, name, die_type, "return")

        # function without a return type
        elif not die_type:
            fact = fn.interface(corpus.basename, name)

        # abi_typelocation('exe', 'main', 'char**', 'fb-32')
        # here we get dies with possibly an incorrect type, these should
        # be spot checked (I'm not sure what they are)
        # maybe we need to derived from DW_AT_declaration or DW_AT_sibling?
        else:
            cname = corpus.basename
            fact = fn.abi_typelocation_unsure(cname, pname, name, die_type)
        self.gen.fact(fact)

    def _get_die_type(self, die, lookup_die=None):
        """
        Parse the die type.

        We typically get the size in bytes or look it up. If lookup die
        is provided, it means we are digging into layers and are looking
        for a type for "die."

        Might be useful:
        https://www.gitmemory.com/issue/eliben/pyelftools/353/784166976

        """
        type_die = None

        # The die we query for the type is either the die itself, or one we've
        # already found
        query_die = lookup_die or die

        # CU relative offset
        if query_die.attributes["DW_AT_type"].form.startswith("DW_FORM_ref"):
            try:
                type_die = query_die.cu.get_DIE_from_refaddr(
                    query_die.attributes["DW_AT_type"].value
                )

            # DWARFError: refaddr 48991 not in DIE range of CU 66699
            # https://github.com/eliben/pyelftools/blob/master/elftools/dwarf/compileunit.py#L113
            # When using a reference class attribute with a form that is
            # relative to the compile unit, add unit add the compile unit's
            # .cu_addr before calling this function.
            except et.exceptions.DWARFError:
                type_die = query_die.cu.get_DIE_from_refaddr(
                    query_die.attributes["DW_AT_type"].value + query_die.cu.cu_offset
                )

        # Absolute offset
        elif query_die.attributes["DW_AT_type"].startswith("DW_FORM_ref_addr"):
            print("ABSOLUTE OFFSET")
            import IPython

            IPython.embed()

        # If we grabbed the type, just explicitly write the size/type
        # In the future we could reference another die, but don't
        # have it's parent here at the moment
        if type_die:

            # If we have another type def, call function again until we find it
            if "DW_AT_type" in type_die.attributes:
                return self._get_die_type(die, type_die)

            # Not sure how to parse this, call it const for now
            elif type_die.tag == 'DW_TAG_const_type':
                return "const"

            # Just call structures a type for now, and pointers
            elif type_die.tag == 'DW_TAG_structure_type':
                return "structure"

            elif type_die.tag == "DW_TAG_pointer_type":
                return "pointer"

            else:
                type_name = None
                if "DW_AT_linkage_name" in type_die.attributes:
                    type_name = self.bytes2str(
                        type_die.attributes["DW_AT_linkage_name"].value
                    )
                elif "DW_AT_name" in type_die.attributes:
                    type_name = self.bytes2str(type_die.attributes["DW_AT_name"].value)
                return type_name

    def generate_corpus_metadata(self, corpora, main):
        """
        Label a set of corpora as the main ones we are assessing for compatibility.
        """
        seen = set()

        # Use ldd to find a needed path. Assume we are on some system compiled on.
        for corpus in corpora:

            hdr = corpus.elfheader
            self.gen.h2("Corpus facts: %s" % corpus.basename)

            # packages have a name and uid
            self.gen.fact(fn.corpus(corpus.basename))

            # if we have seen the spec or dep name already, continue
            if corpus.name in seen:
                continue
            seen.add(corpus.name)

            # Is it a main corpus?
            if corpus.name == main or corpus.uid is not None:
                self.gen.fact(fn.is_main_corpus(corpus.name, corpus.uid))

            # If the corpus has a soname:
            if corpus.soname:
                self.gen.fact(fn.corpus_soname(corpus.name, corpus.soname))

            # e_machine is the required architecture for the file
            self.gen.fact(fn.corpus_machine(corpus.name, hdr["e_machine"]))

    def get_system_corpora(self, corpora):
        """Get a list of corpora for system corpora
        """
        ldd = which('ldd')

        seen = set()
        syscorpora = []
        for corpus in corpora:
            output = ldd(corpus.path, output=str)

            for line in output.split('\n'):
                if "=>" in line:
                    lib, path = line.split('=>')
                    lib = lib.strip()
                    path = path.strip().split(' ')[0]

                    # Don't add redundant entries
                    if path in seen:
                        continue
                    if os.path.exists(path) and lib in corpus.needed:
                        syscorpora.append(Corpus(path, name=lib))
                    seen.add(path)
        return syscorpora

    def generate_typelocations(self, corpora, main):
        """
        Generate type location facts for a set of corpora.

        Arguments:
            corpora: one or more corpora
            main: the name of the main corpus
        """
        # preliminary checks
        for corpus in corpora:
            assert corpus.exists()

        self.gen.h1("Corpus Facts")

        # Add system corpora to the list ?
        corpora += self.get_system_corpora(corpora)

        # We still want to filter down to needed symbols by main corpora
        self.set_needed_symbols(corpora, main)

        # We also want to create a symbol lookup to advise parsing the DIEs
        self.create_symbol_lookup(corpora)

        # Generate high level corpus metadata facts (e.g., header)
        self.generate_corpus_metadata(corpora, main)

        self.gen.h1("Corpus Symbols")

        # Generate dwarf information entries for symbols we see
        self.generate_dwarf_information_entries(corpora)

    def generate(self, corpora, main):
        """
        Generate all facts for a set of corpora.

        Arguments:
            corpora: one or more corpora
            main: the name of the main corpus
            details: generate additional DIE metadata and details.
        """
        # preliminary checks
        for corpus in corpora:
            assert corpus.exists()

        self.gen.h1("Corpus Facts")

        # Figure out needed symbols
        self.set_needed_symbols(corpora, main)

        # Generate high level corpus metadata facts (e.g., header)
        self.generate_corpus_metadata(corpora, main)

        # Add system corpora to elf symbols
        self.generate_elf_symbols(self.get_system_corpora(corpora))

        # Generate all elf symbols (might be able to make this smaller set)
        self.generate_elf_symbols(corpora, detail=False)


def show_loclist(loclist, dwarfinfo, indent, cu_offset):
    """TODO have not encountered this case yet"""
    print('show loclist!')
    import IPython
    IPython.embed()
    d = []
    for loc_entity in loclist:
        if isinstance(loc_entity, et.locationlists.LocationEntry):
            d.append('%s <<%s>>' % (
                loc_entity,
                et.dwarf.describe_DWARF_expr(loc_entity.loc_expr,
                                             dwarfinfo.structs, cu_offset)))
        else:
            d.append(str(loc_entity))
    return '\n'.join(indent + s for s in d)


# Functions intended to be called by external clients
def generate_corpora(spec, include_compilers=False):
    """Generate one or more corpora for a spec.
    """
    # The manifest includes the spec binar(y|(ies)
    # We extract facts for all binaries, even if they get used separately
    # We also keep track of these "main" binaries that are being assessed
    manifest = spack.binary_distribution.get_buildfile_manifest(spec)

    # Keep track of compilers
    compilers = {spec.compiler}

    # Generate corpora for each
    corpora = []
    for main in manifest['binary_to_relocate_fullpath']:

        # This version of the corpus is designed for spack
        corpora.append(Corpus(main, name=spec.name, uid=spec.version))

    # Find all needed libraries and compilers, used for all mains
    for dep in spec.dependencies():
        manifest = spack.binary_distribution.get_buildfile_manifest(dep)
        compilers.add(dep.compiler)

        for lib in manifest['binary_to_relocate_fullpath']:
            corpora.append(Corpus(lib, name=dep.name, uid=dep.version))

    # Add compilers
    if include_compilers:
        for compiler in compilers:
            corpora.append(Corpus(which(compiler.name).path, name=compiler.name,
                                  uid=compiler.version))

    return corpora


def generate_facts(spec, outfile, include_compilers=True, details=False):
    """
    A single function to generate facts for a spec.

    Arguments:
      spec (spack.spec.Spec) : the spec to generate facts for.
      outfile (str) : the output file to write to as we go
    """
    # We don't currently have a way to identify sets of overlapping interfaces.
    # Symbol name matching could miss symbols that are missing
    corpora = generate_corpora(spec, include_compilers=True)

    # We use the PyClingoDriver only to write (not to solve)
    driver = spack.solver.asp.PyclingoDriver()
    out = open(outfile, 'w')
    driver.out = out

    # The generator translates corpora to atoms
    gen = ABIFactGenerator(driver)
    driver.init_control()

    with driver.control.backend() as backend:
        driver.backend = backend

        # Do we want typelocations?
        if details:
            gen.generate_typelocations(corpora, spec.name)
        else:
            gen.generate(corpora, spec.name)
    out.close()
