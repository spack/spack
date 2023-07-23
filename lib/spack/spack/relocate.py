# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import itertools
import os
import re
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional

import macholib.mach_o
import macholib.MachO

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.lang import memoized
from llnl.util.symlink import symlink

import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.util.elf as elf
import spack.util.executable as executable

from .relocate_text import BinaryFilePrefixReplacer, TextFilePrefixReplacer

is_macos = str(spack.platforms.real_host()) == "darwin"


class InstallRootStringError(spack.error.SpackError):
    def __init__(self, file_path, root_path):
        """Signal that the relocated binary still has the original
        Spack's store root string

        Args:
            file_path (str): path of the binary
            root_path (str): original Spack's store root string
        """
        super().__init__(
            "\n %s \ncontains string\n %s \n"
            "after replacing it in rpaths.\n"
            "Package should not be relocated.\n Use -a to override." % (file_path, root_path)
        )


@memoized
def _patchelf():
    """Return the full path to the patchelf binary, if available, else None."""
    import spack.bootstrap

    if is_macos:
        return None

    with spack.bootstrap.ensure_bootstrap_configuration():
        patchelf = spack.bootstrap.ensure_patchelf_in_path_or_raise()

    return patchelf.path


def _decode_macho_data(bytestring):
    return bytestring.rstrip(b"\x00").decode("ascii")


def modify_macho_object(filepath: str, path_to_path_fn: Callable[[str], Optional[str]]):
    """
    This function is used to make machO buildcaches on macOS by
    replacing old paths with new paths using install_name_tool
    Inputs:
    mach-o binary to be modified
    function mapping old to new paths, returning None if no change is needed
    """
    # avoid error message for libgcc_s
    if "libgcc_" in filepath:
        return

    rpaths, deps, idpath = macholib_get_paths(filepath)

    args: List[Any] = []

    if idpath:
        new_idpath = path_to_path_fn(idpath)
        if new_idpath and not idpath == new_idpath:
            args += [("-id", new_idpath)]

    for dep in deps:
        new_dep = path_to_path_fn(dep)
        if new_dep and dep != new_dep:
            args += [("-change", dep, new_dep)]

    new_rpaths = []
    for orig_rpath in rpaths:
        new_rpath = path_to_path_fn(orig_rpath)
        if new_rpath and not orig_rpath == new_rpath:
            args_to_add = ("-rpath", orig_rpath, new_rpath)
            if args_to_add not in args and new_rpath not in new_rpaths:
                args += [args_to_add]
                new_rpaths.append(new_rpath)

    # Deduplicate and flatten
    args = list(itertools.chain.from_iterable(llnl.util.lang.dedupe(args)))
    if args:
        args.append(filepath)
        install_name_tool = executable.Executable("install_name_tool")
        install_name_tool(*args)

    return


def modify_object_macholib(cur_path, path_to_path_fn):
    """
    This function is used when install machO buildcaches on linux by
    rewriting mach-o loader commands for dependency library paths of
    mach-o binaries and the id path for mach-o libraries.
    Rewritting of rpaths is handled by replace_prefix_bin.
    Inputs
    mach-o binary to be modified
    dictionary mapping paths in old install layout to new install layout
    """

    dll = macholib.MachO.MachO(cur_path)
    dll.rewriteLoadCommands(path_to_path_fn)

    try:
        f = open(dll.filename, "rb+")
        for header in dll.headers:
            f.seek(0)
            dll.write(f)
        f.seek(0, 2)
        f.flush()
        f.close()
    except Exception:
        pass

    return


def macholib_get_paths(cur_path):
    """Get rpaths, dependent libraries, and library id of mach-o objects."""
    headers = macholib.MachO.MachO(cur_path).headers
    if not headers:
        tty.warn("Failed to read Mach-O headers: {0}".format(cur_path))
        commands = []
    else:
        if len(headers) > 1:
            # Reproduce original behavior of only returning the last mach-O
            # header section
            tty.warn("Encountered fat binary: {0}".format(cur_path))
        if headers[-1].filetype == "dylib_stub":
            tty.warn("File is a stub, not a full library: {0}".format(cur_path))
        commands = headers[-1].commands

    LC_ID_DYLIB = macholib.mach_o.LC_ID_DYLIB
    LC_LOAD_DYLIB = macholib.mach_o.LC_LOAD_DYLIB
    LC_RPATH = macholib.mach_o.LC_RPATH

    ident = None
    rpaths = []
    deps = []
    for load_command, dylib_command, data in commands:
        cmd = load_command.cmd
        if cmd == LC_RPATH:
            rpaths.append(_decode_macho_data(data))
        elif cmd == LC_LOAD_DYLIB:
            deps.append(_decode_macho_data(data))
        elif cmd == LC_ID_DYLIB:
            ident = _decode_macho_data(data)

    return (rpaths, deps, ident)


def _set_elf_rpaths(target, rpaths):
    """Replace the original RPATH of the target with the paths passed
    as arguments.

    Args:
        target: target executable. Must be an ELF object.
        rpaths: paths to be set in the RPATH

    Returns:
        A string concatenating the stdout and stderr of the call
        to ``patchelf`` if it was invoked
    """
    # Join the paths using ':' as a separator
    rpaths_str = ":".join(rpaths)

    patchelf, output = executable.Executable(_patchelf()), None
    try:
        # TODO: revisit the use of --force-rpath as it might be conditional
        # TODO: if we want to support setting RUNPATH from binary packages
        patchelf_args = ["--force-rpath", "--set-rpath", rpaths_str, target]
        output = patchelf(*patchelf_args, output=str, error=str)
    except executable.ProcessError as e:
        msg = "patchelf --force-rpath --set-rpath {0} failed with error {1}"
        tty.warn(msg.format(target, e))
    return output


def needs_binary_relocation(m_type, m_subtype):
    """Returns True if the file with MIME type/subtype passed as arguments
    needs binary relocation, False otherwise.

    Args:
        m_type (str): MIME type of the file
        m_subtype (str): MIME subtype of the file
    """
    subtypes = ("x-executable", "x-sharedlib", "x-mach-binary", "x-pie-executable")
    if m_type == "application":
        if m_subtype in subtypes:
            return True
    return False


def needs_text_relocation(m_type, m_subtype):
    """Returns True if the file with MIME type/subtype passed as arguments
    needs text relocation, False otherwise.

    Args:
        m_type (str): MIME type of the file
        m_subtype (str): MIME subtype of the file
    """
    return m_type == "text"


def maybe_replace(regex, prefix_to_prefix: Dict[str, str], path: str) -> Optional[str]:
    match = regex.match(path)
    return prefix_to_prefix[match.group()] + path[match.end() :] if match else None


def relocate_macho_binaries(binaries: List[str], prefix_to_prefix: Dict[str, str]):
    regex = re.compile("|".join(re.escape(p) for p in prefix_to_prefix.keys()))
    path_to_path_fn = lambda p: maybe_replace(regex, prefix_to_prefix, p)

    for path in binaries:
        # Corner case where macho object file ended up in the path name list
        if path.endswith(".o"):
            continue

        if is_macos:
            modify_macho_object(path, path_to_path_fn)
        else:
            modify_object_macholib(path, path_to_path_fn)


def relocate_elf_binaries(binaries, prefix_to_prefix):
    """Take a list of binaries, and an ordered dictionary of
    prefix to prefix mapping, and update the rpaths accordingly."""

    # Transform to binary string
    prefix_to_prefix = OrderedDict(
        (k.encode("utf-8"), v.encode("utf-8")) for (k, v) in prefix_to_prefix.items()
    )

    for path in binaries:
        try:
            elf.replace_rpath_in_place_or_raise(path, prefix_to_prefix)
        except elf.ElfDynamicSectionUpdateFailed as e:
            # Fall back to the old `patchelf --set-rpath` method.
            _set_elf_rpaths(path, e.new.decode("utf-8").split(":"))


def make_link_relative(new_links, orig_links):
    """Compute the relative target from the original link and
    make the new link relative.

    Args:
        new_links (list): new links to be made relative
        orig_links (list): original links
    """
    for new_link, orig_link in zip(new_links, orig_links):
        target = os.readlink(orig_link)
        relative_target = os.path.relpath(target, os.path.dirname(orig_link))
        os.unlink(new_link)
        symlink(relative_target, new_link)


def warn_if_link_cant_be_relocated(link, target):
    if not os.path.isabs(target):
        return
    tty.warn(f'Symbolic link at "{link}" to "{target}" cannot be relocated')


def relocate_links(links, prefix_to_prefix):
    """Relocate links to a new install prefix."""
    regex = re.compile("|".join(re.escape(p) for p in prefix_to_prefix.keys()))
    for link in links:
        old_target = os.readlink(link)
        match = regex.match(old_target)

        # No match.
        if match is None:
            warn_if_link_cant_be_relocated(link, old_target)
            continue

        new_target = prefix_to_prefix[match.group()] + old_target[match.end() :]
        os.unlink(link)
        symlink(new_target, link)


def relocate_text(files, prefixes):
    """Relocate text file from the original installation prefix to the
    new prefix.

    Relocation also affects the the path in Spack's sbang script.

    Args:
        files (list): Text files to be relocated
        prefixes (OrderedDict): String prefixes which need to be changed
    """
    TextFilePrefixReplacer.from_strings_or_bytes(prefixes).apply(files)


def relocate_text_bin(binaries, prefixes):
    """Replace null terminated path strings hard-coded into binaries.

    The new install prefix must be shorter than the original one.

    Args:
        binaries (list): binaries to be relocated
        prefixes (OrderedDict): String prefixes which need to be changed.

    Raises:
      spack.relocate_text.BinaryTextReplaceError: when the new path is longer than the old path
    """
    return BinaryFilePrefixReplacer.from_strings_or_bytes(prefixes).apply(binaries)


def is_binary(filename):
    """Returns true if a file is binary, False otherwise

    Args:
        filename: file to be tested

    Returns:
        True or False
    """
    m_type, _ = fs.mime_type(filename)

    msg = "[{0}] -> ".format(filename)
    if m_type == "application":
        tty.debug(msg + "BINARY FILE")
        return True

    tty.debug(msg + "TEXT FILE")
    return False


# Memoize this due to repeated calls to libraries in the same directory.
@llnl.util.lang.memoized
def _exists_dir(dirname):
    return os.path.isdir(dirname)


def fixup_macos_rpath(root, filename):
    """Apply rpath fixups to the given file.

    Args:
        root: absolute path to the parent directory
        filename: relative path to the library or binary

    Returns:
        True if fixups were applied, else False
    """
    abspath = os.path.join(root, filename)
    if fs.mime_type(abspath) != ("application", "x-mach-binary"):
        return False

    # Get Mach-O header commands
    (rpath_list, deps, id_dylib) = macholib_get_paths(abspath)

    # Convert rpaths list to (name -> number of occurrences)
    add_rpaths = set()
    del_rpaths = set()
    rpaths = collections.defaultdict(int)
    for rpath in rpath_list:
        rpaths[rpath] += 1

    args = []

    # Check dependencies for non-rpath entries
    spack_root = spack.store.STORE.layout.root
    for name in deps:
        if name.startswith(spack_root):
            tty.debug("Spack-installed dependency for {0}: {1}".format(abspath, name))
            (dirname, basename) = os.path.split(name)
            if dirname != root or dirname in rpaths:
                # Only change the rpath if it's a dependency *or* if the root
                # rpath was already added to the library (this is to prevent
                # GCC or similar getting rpaths when they weren't at all
                # configured)
                args += ["-change", name, "@rpath/" + basename]
                add_rpaths.add(dirname.rstrip("/"))

    # Check for nonexistent rpaths (often added by spack linker overzealousness
    # with both lib/ and lib64/) and duplicate rpaths
    for rpath, count in rpaths.items():
        if rpath.startswith("@loader_path") or rpath.startswith("@executable_path"):
            # Allowable relative paths
            pass
        elif not _exists_dir(rpath):
            tty.debug("Nonexistent rpath in {0}: {1}".format(abspath, rpath))
            del_rpaths.add(rpath)
        elif count > 1:
            # Rpath should only be there once, but it can sometimes be
            # duplicated between Spack's compiler and libtool. If there are
            # more copies of the same one, something is very odd....
            tty_debug = tty.debug if count == 2 else tty.warn
            tty_debug("Rpath appears {0} times in {1}: {2}".format(count, abspath, rpath))
            del_rpaths.add(rpath)

    # Delete bad rpaths
    for rpath in del_rpaths:
        args += ["-delete_rpath", rpath]

    # Add missing rpaths that are not set for deletion
    for rpath in add_rpaths - del_rpaths - set(rpaths):
        args += ["-add_rpath", rpath]

    if not args:
        # No fixes needed
        return False

    args.append(abspath)
    executable.Executable("install_name_tool")(*args)
    return True


def fixup_macos_rpaths(spec):
    """Remove duplicate and nonexistent rpaths.

    Some autotools packages write their own ``-rpath`` entries in addition to
    those implicitly added by the Spack compiler wrappers. On Linux these
    duplicate rpaths are eliminated, but on macOS they result in multiple
    entries which makes it harder to adjust with ``install_name_tool
    -delete_rpath``.
    """
    if spec.external or spec.virtual:
        tty.warn("external or virtual package cannot be fixed up: {0!s}".format(spec))
        return False

    if "platform=darwin" not in spec:
        raise NotImplementedError("fixup_macos_rpaths requires macOS")

    applied = 0

    libs = frozenset(["lib", "lib64", "libexec", "plugins", "Library", "Frameworks"])
    prefix = spec.prefix

    if not os.path.exists(prefix):
        raise RuntimeError(
            "Could not fix up install prefix spec {0} because it does "
            "not exist: {1!s}".format(prefix, spec.name)
        )

    # Explore the installation prefix of the spec
    for root, dirs, files in os.walk(prefix, topdown=True):
        dirs[:] = set(dirs) & libs
        for name in files:
            try:
                needed_fix = fixup_macos_rpath(root, name)
            except Exception as e:
                tty.warn("Failed to apply library fixups to: {0}/{1}: {2!s}".format(root, name, e))
                needed_fix = False
            if needed_fix:
                applied += 1

    specname = spec.format("{name}{/hash:7}")
    if applied:
        tty.info(
            "Fixed rpaths for {0:d} {1} installed to {2}".format(
                applied, "binary" if applied == 1 else "binaries", specname
            )
        )
    else:
        tty.debug("No rpath fixup needed for " + specname)
