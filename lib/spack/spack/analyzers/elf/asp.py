# This is based on asp.py from spack/spack, copyright LLNL and spack developers
# It will eventually be added back to that scope - this script is developing
# new functionality to work with ABI.

import os


try:
    import elftools
except ImportError:
    elftools = None

from .corpus import Corpus
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

        # A lookup of DIE children ids
        self.child_lookup = {}
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

    def generate_elf_symbols(self, corpora):
        """For each corpus, write out elf symbols as facts.
        """
        for corpus in corpora:
            self.gen.h2("Corpus symbols: %s" % corpus.basename)

            for symbol, meta in corpus.elfsymbols.items():

                # It begins with a NULL symbol, not sure it's useful
                if not symbol or symbol not in self.needed_symbols:
                    continue

                # Prepare variables
                vinfo = meta['version_info']
                defined = meta['defined']

                # If the symbol has @@ in the name, it includes the version.
                if "@@" in symbol and not vinfo:
                    symbol, _ = symbol.split('@', 1)

                self.gen.fact(fn.symbol(symbol))
                self.gen.fact(fn.symbol_definition(corpus.basename, symbol, defined))
                self.gen.fact(fn.has_symbol(corpus.basename, symbol))

    def bytes2str(self, item):
        return elftools.common.py3compat.bytes2str(item)

    def set_needed_symbols(self, corpora, main):
        """
        Set needed symbols that we should filter to.
        """
        for corpus in corpora:
            if corpus.name == main:
                for symbol, meta in corpus.elfsymbols.items():
                    self.needed_symbols.add(symbol)

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
            if hasattr(corpus, "name") and hasattr(corpus, "uid"):
                self.gen.fact(fn.corpus(corpus.name, corpus.uid, corpus.basename))

            # Compilers won't have a name and uid
            else:
                self.gen.fact(fn.corpus(corpus.basename))

            # if we have seen the spec or dep name already, continue
            if corpus.name in seen:
                continue
            seen.add(corpus.name)

            # Is it a main corpus?
            if corpus.name == main:
                self.gen.fact(fn.is_main_corpus(corpus.name, corpus.uid))

            # If the corpus has a soname:
            if corpus.soname:
                self.gen.fact(fn.corpus_soname(corpus.name, corpus.uid, corpus.soname))

            # e_machine is the required architecture for the file
            self.gen.fact(fn.corpus_machine(corpus.name, corpus.uid, hdr["e_machine"]))
            self.generate_needed(corpus)

    def skip_symbols(self, corpora):
        """
        Generate a list of skip symbols, typically from a compiler.
        """
        pass

    def generate_needed(self, corpus):
        """
        Generate symbols from needed libraries.
        """
        ldd = which('ldd')
        output = ldd(corpus.path, output=str)

        syscorpora = []
        for line in output.split('\n'):
            if "=>" in line:
                lib, path = line.split('=>')
                lib = lib.strip()
                path = path.strip().split(' ')[0]
                if os.path.exists(path) and lib in corpus.needed:
                    syscorpora.append(Corpus(path))

        self.generate_elf_symbols(syscorpora)

    def generate(self, corpora, main):
        """
        Generate all facts for a set of corpora.

        Arguments:
            corpora: one or more corpora
        """
        # preliminary checks
        for corpus in corpora:
            assert corpus.exists()

        self.gen.h1("Corpus Facts")

        # Figure out needed symbols
        self.set_needed_symbols(corpora, main)

        # Generate high level corpus metadata facts (e.g., header)
        self.generate_corpus_metadata(corpora, main)

        # Generate all elf symbols (might be able to make this smaller set)
        self.generate_elf_symbols(corpora)


# Functions intended to be called by external clients


def generate_facts(spec, outfile):
    """
    A single function to generate facts for a spec.

    Arguments:
      spec (spack.spec.Spec) : the spec to generate facts for.
      outfile (str) : the output file to write to as we go
    """
    # The manifest includes the spec binar(y|(ies)
    # We extract facts for all binaries, even if they get used separately
    # We also keep track of these "main" binaries that are being assessed
    manifest = spack.binary_distribution.get_buildfile_manifest(spec)

    # Keep track of compilers
    compilers = {which(spec.compiler.name).path}

    # Generate corpora for each
    corpora = []
    for main in manifest['binary_to_relocate_fullpath']:

        # This version of the corpus is designed for spack
        corpora.append(Corpus(main, name=spec.name, uid=spec.build_hash()))

    # Find all needed libraries and compilers, used for all mains
    for dep in spec.dependencies():
        manifest = spack.binary_distribution.get_buildfile_manifest(dep)
        compilers.add(which(dep.compiler.name).path)

        for lib in manifest['binary_to_relocate_fullpath']:
            corpora.append(Corpus(lib, name=dep.name, uid=dep.build_hash()))

    # Add compilers
    for compiler in compilers:
        corpora.append(Corpus(compiler))

    # We use the PyClingoDriver only to write (not to solve)
    driver = spack.solver.asp.PyclingoDriver()
    out = open(outfile, 'w')
    driver.out = out

    # The generator translates corpora to atoms
    gen = ABIFactGenerator(driver)
    driver.init_control()

    with driver.control.backend() as backend:
        driver.backend = backend
        gen.generate(corpora, spec.name)

    out.close()
