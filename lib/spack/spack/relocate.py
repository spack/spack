# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import platform
import re
import shutil

import llnl.util.lang
import llnl.util.tty as tty
import macholib.MachO
import macholib.mach_o
import spack.cmd
import spack.repo
import spack.spec
import spack.util.executable as executable


class InstallRootStringError(spack.error.SpackError):
    def __init__(self, file_path, root_path):
        """Signal that the relocated binary still has the original
        Spack's store root string

        Args:
            file_path (str): path of the binary
            root_path (str): original Spack's store root string
        """
        super(InstallRootStringError, self).__init__(
            "\n %s \ncontains string\n %s \n"
            "after replacing it in rpaths.\n"
            "Package should not be relocated.\n Use -a to override." %
            (file_path, root_path))


class BinaryStringReplacementError(spack.error.SpackError):
    def __init__(self, file_path, old_len, new_len):
        """The size of the file changed after binary path substitution

        Args:
            file_path (str): file with changing size
            old_len (str): original length of the file
            new_len (str): length of the file after substitution
        """
        super(BinaryStringReplacementError, self).__init__(
            "Doing a binary string replacement in %s failed.\n"
            "The size of the file changed from %s to %s\n"
            "when it should have remanined the same." %
            (file_path, old_len, new_len))


class BinaryTextReplaceError(spack.error.SpackError):
    def __init__(self, old_path, new_path):
        """Raised when the new install path is longer than the
        old one, so binary text replacement cannot occur.

        Args:
            old_path (str): original path to be substituted
            new_path (str): candidate path for substitution
        """

        msg = "New path longer than old path: binary text"
        msg += " replacement not possible."
        err_msg = "The new path %s" % new_path
        err_msg += " is longer than the old path %s.\n" % old_path
        err_msg += "Text replacement in binaries will not work.\n"
        err_msg += "Create buildcache from an install path "
        err_msg += "longer than new path."
        super(BinaryTextReplaceError, self).__init__(msg, err_msg)


def _patchelf():
    """Return the full path to the patchelf binary, if available, else None.

    Search first the current PATH for patchelf. If not found, try to look
    if the default patchelf spec is installed and if not install it.

    Return None on Darwin or if patchelf cannot be found.
    """
    # Check if patchelf is already in the PATH
    patchelf = spack.util.executable.which('patchelf')
    if patchelf is not None:
        return patchelf.path

    # Check if patchelf spec is installed
    spec = spack.spec.Spec('patchelf').concretized()
    exe_path = os.path.join(spec.prefix.bin, "patchelf")
    if spec.package.installed and os.path.exists(exe_path):
        return exe_path

    # Skip darwin
    if str(spack.architecture.platform()) == 'darwin':
        return None

    # Install the spec and return its path
    spec.package.do_install()
    return exe_path if os.path.exists(exe_path) else None


def get_existing_elf_rpaths(path_name):
    """
    Return the RPATHS returned by patchelf --print-rpath path_name
    as a list of strings.
    """

    # if we're relocating patchelf itself, use it

    if path_name.endswith("/bin/patchelf"):
        patchelf = executable.Executable(path_name)
    else:
        patchelf = executable.Executable(_patchelf())

    rpaths = list()
    try:
        output = patchelf('--print-rpath', '%s' %
                          path_name, output=str, error=str)
        rpaths = output.rstrip('\n').split(':')
    except executable.ProcessError as e:
        msg = 'patchelf --print-rpath %s produced an error %s' % (path_name, e)
        tty.warn(msg)
    return rpaths


def get_relative_elf_rpaths(path_name, orig_layout_root, orig_rpaths):
    """
    Replaces orig rpath with relative path from dirname(path_name) if an rpath
    in orig_rpaths contains orig_layout_root. Prefixes $ORIGIN
    to relative paths and returns replacement rpaths.
    """
    rel_rpaths = []
    for rpath in orig_rpaths:
        if re.match(orig_layout_root, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            rel_rpaths.append(os.path.join('$ORIGIN', '%s' % rel))
        else:
            rel_rpaths.append(rpath)
    return rel_rpaths


def get_normalized_elf_rpaths(orig_path_name, rel_rpaths):
    """
    Normalize the relative rpaths with respect to the original path name
    of the file. If the rpath starts with $ORIGIN replace $ORIGIN with the
    dirname of the original path name and then normalize the rpath.
    A dictionary mapping relativized rpaths to normalized rpaths is returned.
    """
    norm_rpaths = list()
    for rpath in rel_rpaths:
        if rpath.startswith('$ORIGIN'):
            sub = re.sub(re.escape('$ORIGIN'),
                         os.path.dirname(orig_path_name),
                         rpath)
            norm = os.path.normpath(sub)
            norm_rpaths.append(norm)
        else:
            norm_rpaths.append(rpath)
    return norm_rpaths


def set_placeholder(dirname):
    """
    return string of @'s with same length
    """
    return '@' * len(dirname)


def macho_make_paths_relative(path_name, old_layout_root,
                              rpaths, deps, idpath):
    """
    Return a dictionary mapping the original rpaths to the relativized rpaths.
    This dictionary is used to replace paths in mach-o binaries.
    Replace old_dir with relative path from dirname of path name
    in rpaths and deps; idpath is replaced with @rpath/libname.
    """
    paths_to_paths = dict()
    if idpath:
        paths_to_paths[idpath] = os.path.join(
            '@rpath', '%s' % os.path.basename(idpath))
    for rpath in rpaths:
        if re.match(old_layout_root, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            paths_to_paths[rpath] = os.path.join('@loader_path', '%s' % rel)
        else:
            paths_to_paths[rpath] = rpath
    for dep in deps:
        if re.match(old_layout_root, dep):
            rel = os.path.relpath(dep, start=os.path.dirname(path_name))
            paths_to_paths[dep] = os.path.join('@loader_path', '%s' % rel)
        else:
            paths_to_paths[dep] = dep
    return paths_to_paths


def macho_make_paths_normal(orig_path_name, rpaths, deps, idpath):
    """
    Return a dictionary mapping the relativized rpaths to the original rpaths.
    This dictionary is used to replace paths in mach-o binaries.
    Replace '@loader_path' with the dirname of the origname path name
    in rpaths and deps; idpath is replaced with the original path name
    """
    rel_to_orig = dict()
    if idpath:
        rel_to_orig[idpath] = orig_path_name

    for rpath in rpaths:
        if re.match('@loader_path', rpath):
            norm = os.path.normpath(re.sub(re.escape('@loader_path'),
                                           os.path.dirname(orig_path_name),
                                           rpath))
            rel_to_orig[rpath] = norm
        else:
            rel_to_orig[rpath] = rpath
    for dep in deps:
        if re.match('@loader_path', dep):
            norm = os.path.normpath(re.sub(re.escape('@loader_path'),
                                           os.path.dirname(orig_path_name),
                                           dep))
            rel_to_orig[dep] = norm
        else:
            rel_to_orig[dep] = dep
    return rel_to_orig


def macho_find_paths(orig_rpaths, deps, idpath,
                     old_layout_root, prefix_to_prefix):
    """
    Inputs
    original rpaths from mach-o binaries
    dependency libraries for mach-o binaries
    id path of mach-o libraries
    old install directory layout root
    prefix_to_prefix dictionary which maps prefixes in the old directory layout
    to directories in the new directory layout
    Output
    paths_to_paths dictionary which maps all of the old paths to new paths
    """
    paths_to_paths = dict()
    for orig_rpath in orig_rpaths:
        if orig_rpath.startswith(old_layout_root):
            for old_prefix, new_prefix in prefix_to_prefix.items():
                if orig_rpath.startswith(old_prefix):
                    new_rpath = re.sub(re.escape(old_prefix),
                                       new_prefix, orig_rpath)
                    paths_to_paths[orig_rpath] = new_rpath
        else:
            paths_to_paths[orig_rpath] = orig_rpath

    if idpath:
        for old_prefix, new_prefix in prefix_to_prefix.items():
            if idpath.startswith(old_prefix):
                paths_to_paths[idpath] = re.sub(
                    re.escape(old_prefix), new_prefix, idpath)
    for dep in deps:
        for old_prefix, new_prefix in prefix_to_prefix.items():
            if dep.startswith(old_prefix):
                paths_to_paths[dep] = re.sub(
                    re.escape(old_prefix), new_prefix, dep)
        if dep.startswith('@'):
            paths_to_paths[dep] = dep

    return paths_to_paths


def modify_macho_object(cur_path, rpaths, deps, idpath,
                        paths_to_paths):
    """
    This function is used to make machO buildcaches on macOS by
    replacing old paths with new paths using install_name_tool
    Inputs:
    mach-o binary to be modified
    original rpaths
    original dependency paths
    original id path if a mach-o library
    dictionary mapping paths in old install layout to new install layout
    """
    # avoid error message for libgcc_s
    if 'libgcc_' in cur_path:
        return
    install_name_tool = executable.Executable('install_name_tool')

    if idpath:
        new_idpath = paths_to_paths.get(idpath, None)
        if new_idpath and not idpath == new_idpath:
            install_name_tool('-id', new_idpath, str(cur_path))
    for dep in deps:
        new_dep = paths_to_paths.get(dep)
        if new_dep and dep != new_dep:
            install_name_tool('-change', dep, new_dep, str(cur_path))

    for orig_rpath in rpaths:
        new_rpath = paths_to_paths.get(orig_rpath)
        if new_rpath and not orig_rpath == new_rpath:
            install_name_tool('-rpath', orig_rpath, new_rpath, str(cur_path))
    return


def modify_object_macholib(cur_path, paths_to_paths):
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

    changedict = paths_to_paths

    def changefunc(path):
        npath = changedict.get(path, None)
        return npath

    dll.rewriteLoadCommands(changefunc)

    try:
        f = open(dll.filename, 'rb+')
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
    """
    Get rpaths, dependencies and id of mach-o objects
    using python macholib package
    """
    dll = macholib.MachO.MachO(cur_path)

    ident = None
    rpaths = list()
    deps = list()
    for header in dll.headers:
        rpaths = [data.rstrip(b'\0').decode('utf-8')
                  for load_command, dylib_command, data in header.commands if
                  load_command.cmd == macholib.mach_o.LC_RPATH]
        deps = [data.rstrip(b'\0').decode('utf-8')
                for load_command, dylib_command, data in header.commands if
                load_command.cmd == macholib.mach_o.LC_LOAD_DYLIB]
        idents = [data.rstrip(b'\0').decode('utf-8')
                  for load_command, dylib_command, data in header.commands if
                  load_command.cmd == macholib.mach_o.LC_ID_DYLIB]
        if len(idents) == 1:
            ident = idents[0]
    tty.debug('ident: %s' % ident)
    tty.debug('deps: %s' % deps)
    tty.debug('rpaths: %s' % rpaths)
    return (rpaths, deps, ident)


def modify_elf_object(path_name, new_rpaths):
    """
    Replace orig_rpath with new_rpath in RPATH of elf object path_name
    """

    new_joined = ':'.join(new_rpaths)

    # if we're relocating patchelf itself, use it
    bak_path = path_name + ".bak"

    if path_name[-13:] == "/bin/patchelf":
        shutil.copy(path_name, bak_path)
        patchelf = executable.Executable(bak_path)
    else:
        patchelf = executable.Executable(_patchelf())

    try:
        patchelf('--force-rpath', '--set-rpath', '%s' % new_joined,
                 '%s' % path_name, output=str, error=str)
    except executable.ProcessError as e:
        msg = 'patchelf --force-rpath --set-rpath %s failed with error %s' % (
            path_name, e)
        tty.warn(msg)
    if os.path.exists(bak_path):
        os.remove(bak_path)


def needs_binary_relocation(m_type, m_subtype):
    """
    Check whether the given filetype is a binary that may need relocation.
    """
    if m_type == 'application':
        if (m_subtype == 'x-executable' or m_subtype == 'x-sharedlib' or
                m_subtype == 'x-mach-binary'):
            return True
    return False


def needs_text_relocation(m_type, m_subtype):
    """
    Check whether the given filetype is text that may need relocation.
    """
    return (m_type == "text")


def replace_prefix_text(path_name, old_dir, new_dir):
    """
    Replace old install prefix with new install prefix
    in text files using utf-8 encoded strings.
    """
    with open(path_name, 'rb+') as f:
        data = f.read()
        f.seek(0)
        # Replace old_dir with new_dir if it appears at the beginning of a path
        # Negative lookbehind for a character legal in a path
        # Then a match group for any characters legal in a compiler flag
        # Then old_dir
        # Then characters legal in a path
        # Ensures we only match the old_dir if it's precedeed by a flag or by
        # characters not legal in a path, but not if it's preceeded by other
        # components of a path.
        old_bytes = old_dir.encode('utf-8')
        pat = b'(?<![\\w\\-_/])([\\w\\-_]*?)%s([\\w\\-_/]*)' % old_bytes
        repl = b'\\1%s\\2' % new_dir.encode('utf-8')
        ndata = re.sub(pat, repl, data)
        f.write(ndata)
        f.truncate()


def replace_prefix_bin(path_name, old_dir, new_dir):
    """
    Attempt to replace old install prefix with new install prefix
    in binary files by prefixing new install prefix with os.sep
    until the lengths of the prefixes are the same.
    """

    def replace(match):
        occurances = match.group().count(old_dir.encode('utf-8'))
        olen = len(old_dir.encode('utf-8'))
        nlen = len(new_dir.encode('utf-8'))
        padding = (olen - nlen) * occurances
        if padding < 0:
            return data
        return match.group().replace(old_dir.encode('utf-8'),
                                     os.sep.encode('utf-8') * padding +
                                     new_dir.encode('utf-8'))

    with open(path_name, 'rb+') as f:
        data = f.read()
        f.seek(0)
        original_data_len = len(data)
        pat = re.compile(old_dir.encode('utf-8'))
        if not pat.search(data):
            return
        ndata = pat.sub(replace, data)
        if not len(ndata) == original_data_len:
            raise BinaryStringReplacementError(
                path_name, original_data_len, len(ndata))
        f.write(ndata)
        f.truncate()


def replace_prefix_nullterm(path_name, old_dir, new_dir):
    """
    Attempt to replace old install prefix with new install prefix
    in binary files by replacing with null terminated string
    that is the same length unless the old path is shorter
    Used on linux to replace mach-o rpaths
    """

    def replace(match):
        occurances = match.group().count(old_dir.encode('utf-8'))
        olen = len(old_dir.encode('utf-8'))
        nlen = len(new_dir.encode('utf-8'))
        padding = (olen - nlen) * occurances
        if padding < 0:
            return data
        return match.group().replace(old_dir.encode('utf-8'),
                                     new_dir.encode('utf-8')) + b'\0' * padding

    if len(new_dir) > len(old_dir):
        raise BinaryTextReplaceError(old_dir, new_dir)

    with open(path_name, 'rb+') as f:
        data = f.read()
        f.seek(0)
        original_data_len = len(data)
        pat = re.compile(re.escape(old_dir).encode('utf-8') + b'([^\0]*?)\0')
        if not pat.search(data):
            return
        ndata = pat.sub(replace, data)
        if not len(ndata) == original_data_len:
            raise BinaryStringReplacementError(
                path_name, original_data_len, len(ndata))
        f.write(ndata)
        f.truncate()


def relocate_macho_binaries(path_names, old_layout_root, new_layout_root,
                            prefix_to_prefix, rel, old_prefix, new_prefix):
    """
    Use macholib python package to get the rpaths, depedent libraries
    and library identity for libraries from the MachO object. Modify them
    with the replacement paths queried from the dictionary mapping old layout
    prefixes to hashes and the dictionary mapping hashes to the new layout
    prefixes.
    """

    for path_name in path_names:
        # Corner case where macho object file ended up in the path name list
        if path_name.endswith('.o'):
            continue
        if rel:
            # get the relativized paths
            rpaths, deps, idpath = macholib_get_paths(path_name)
            # get the file path name in the original prefix
            orig_path_name = re.sub(re.escape(new_prefix), old_prefix,
                                    path_name)
            # get the mapping of the relativized paths to the original
            # normalized paths
            rel_to_orig = macho_make_paths_normal(orig_path_name,
                                                  rpaths, deps,
                                                  idpath)
            # replace the relativized paths with normalized paths
            if platform.system().lower() == 'darwin':
                modify_macho_object(path_name, rpaths, deps,
                                    idpath, rel_to_orig)
            else:
                modify_object_macholib(path_name,
                                       rel_to_orig)
            # get the normalized paths in the mach-o binary
            rpaths, deps, idpath = macholib_get_paths(path_name)
            # get the mapping of paths in old prefix to path in new prefix
            paths_to_paths = macho_find_paths(rpaths, deps, idpath,
                                              old_layout_root,
                                              prefix_to_prefix)
            # replace the old paths with new paths
            if platform.system().lower() == 'darwin':
                modify_macho_object(path_name, rpaths, deps,
                                    idpath, paths_to_paths)
            else:
                modify_object_macholib(path_name,
                                       paths_to_paths)
            # get the new normalized path in the mach-o binary
            rpaths, deps, idpath = macholib_get_paths(path_name)
            # get the mapping of paths to relative paths in the new prefix
            paths_to_paths = macho_make_paths_relative(path_name,
                                                       new_layout_root,
                                                       rpaths, deps, idpath)
            # replace the new paths with relativized paths in the new prefix
            if platform.system().lower() == 'darwin':
                modify_macho_object(path_name, rpaths, deps,
                                    idpath, paths_to_paths)
            else:
                modify_object_macholib(path_name,
                                       paths_to_paths)
        else:
            # get the paths in the old prefix
            rpaths, deps, idpath = macholib_get_paths(path_name)
            # get the mapping of paths in the old prerix to the new prefix
            paths_to_paths = macho_find_paths(rpaths, deps, idpath,
                                              old_layout_root,
                                              prefix_to_prefix)
            # replace the old paths with new paths
            if platform.system().lower() == 'darwin':
                modify_macho_object(path_name, rpaths, deps,
                                    idpath, paths_to_paths)
            else:
                modify_object_macholib(path_name,
                                       paths_to_paths)


def elf_find_paths(orig_rpaths, old_layout_root, prefix_to_prefix):
    new_rpaths = list()
    for orig_rpath in orig_rpaths:
        if orig_rpath.startswith(old_layout_root):
            for old_prefix, new_prefix in prefix_to_prefix.items():
                if orig_rpath.startswith(old_prefix):
                    new_rpaths.append(re.sub(re.escape(old_prefix),
                                             new_prefix, orig_rpath))
        else:
            new_rpaths.append(orig_rpath)
    return new_rpaths


def relocate_elf_binaries(path_names, old_layout_root, new_layout_root,
                          prefix_to_prefix, rel, old_prefix, new_prefix):
    """
    Use patchelf to get the original rpaths and then replace them with
    rpaths in the new directory layout.
    New rpaths are determined from a dictionary mapping the prefixes in the
    old directory layout to the prefixes in the new directory layout if the
    rpath was in the old layout root, i.e. system paths are not replaced.
    """
    for path_name in path_names:
        orig_rpaths = get_existing_elf_rpaths(path_name)
        new_rpaths = list()
        if rel:
            # get the file path in the old_prefix
            orig_path_name = re.sub(re.escape(new_prefix), old_prefix,
                                    path_name)
            # get the normalized rpaths in the old prefix using the file path
            # in the orig prefix
            orig_norm_rpaths = get_normalized_elf_rpaths(orig_path_name,
                                                         orig_rpaths)
            # get the normalize rpaths in the new prefix
            norm_rpaths = elf_find_paths(orig_norm_rpaths, old_layout_root,
                                         prefix_to_prefix)
            # get the relativized rpaths in the new prefix
            new_rpaths = get_relative_elf_rpaths(path_name, new_layout_root,
                                                 norm_rpaths)
            modify_elf_object(path_name, new_rpaths)
        else:
            new_rpaths = elf_find_paths(orig_rpaths, old_layout_root,
                                        prefix_to_prefix)
            modify_elf_object(path_name, new_rpaths)


def make_link_relative(cur_path_names, orig_path_names):
    """
    Change absolute links to relative links.
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        target = os.readlink(orig_path)
        relative_target = os.path.relpath(target, os.path.dirname(orig_path))

        os.unlink(cur_path)
        os.symlink(relative_target, cur_path)


def make_macho_binaries_relative(cur_path_names, orig_path_names,
                                 old_layout_root):
    """
    Replace old RPATHs with paths relative to old_dir in binary files
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        rpaths = set()
        deps = set()
        idpath = None
        if platform.system().lower() == 'darwin':
            (rpaths, deps, idpath) = macholib_get_paths(cur_path)
            paths_to_paths = macho_make_paths_relative(orig_path,
                                                       old_layout_root,
                                                       rpaths, deps, idpath)
            modify_macho_object(cur_path,
                                rpaths, deps, idpath,
                                paths_to_paths)


def make_elf_binaries_relative(cur_path_names, orig_path_names,
                               old_layout_root):
    """
    Replace old RPATHs with paths relative to old_dir in binary files
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        orig_rpaths = get_existing_elf_rpaths(cur_path)
        if orig_rpaths:
            new_rpaths = get_relative_elf_rpaths(orig_path, old_layout_root,
                                                 orig_rpaths)
            modify_elf_object(cur_path, new_rpaths)


def check_files_relocatable(cur_path_names, allow_root):
    """
    Check binary files for the current install root
    """
    for cur_path in cur_path_names:
        if (not allow_root and
                not file_is_relocatable(cur_path)):
            raise InstallRootStringError(
                cur_path, spack.store.layout.root)


def relocate_links(linknames, old_layout_root, new_layout_root,
                   old_install_prefix, new_install_prefix, prefix_to_prefix):
    """
    The symbolic links in filenames are absolute links or placeholder links.
    The old link target is read and the placeholder is replaced by the old
    layout root. If the old link target is in the old install prefix, the new
    link target is create by replacing the old install prefix with the new
    install prefix.
    """
    placeholder = set_placeholder(old_layout_root)
    link_names = [os.path.join(new_install_prefix, linkname)
                  for linkname in linknames]
    for link_name in link_names:
        link_target = os.readlink(link_name)
        link_target = re.sub(placeholder, old_layout_root, link_target)
        if link_target.startswith(old_install_prefix):
            new_link_target = re.sub(
                old_install_prefix, new_install_prefix, link_target)
            os.unlink(link_name)
            os.symlink(new_link_target, link_name)
        if (os.path.isabs(link_target) and
            not link_target.startswith(new_install_prefix)):
            msg = 'Link target %s' % link_target
            msg += ' for symbolic link %s is outside' % link_name
            msg += ' of the newinstall prefix %s.\n' % new_install_prefix
            tty.warn(msg)


def relocate_text(path_names, old_layout_root, new_layout_root,
                  old_install_prefix, new_install_prefix,
                  old_spack_prefix, new_spack_prefix,
                  prefix_to_prefix):
    """
    Replace old paths with new paths in text files
    including the path the the spack sbang script
    """
    sbangre = '#!/bin/bash %s/bin/sbang' % old_spack_prefix
    sbangnew = '#!/bin/bash %s/bin/sbang' % new_spack_prefix

    for path_name in path_names:
        replace_prefix_text(path_name, old_install_prefix, new_install_prefix)
        for orig_dep_prefix, new_dep_prefix in prefix_to_prefix.items():
            replace_prefix_text(path_name, orig_dep_prefix, new_dep_prefix)
        replace_prefix_text(path_name, old_layout_root, new_layout_root)
        replace_prefix_text(path_name, sbangre, sbangnew)


def relocate_text_bin(path_names, old_layout_root, new_layout_root,
                      old_install_prefix, new_install_prefix,
                      old_spack_prefix, new_spack_prefix,
                      prefix_to_prefix):
    """
      Replace null terminated path strings hard coded into binaries.
      Raise an exception when the new path in longer than the old path
      because this breaks the binary.
      """
    if len(new_install_prefix) <= len(old_install_prefix):
        for path_name in path_names:
            for old_dep_prefix, new_dep_prefix in prefix_to_prefix.items():
                if len(new_dep_prefix) <= len(old_dep_prefix):
                    replace_prefix_bin(
                        path_name, old_dep_prefix, new_dep_prefix)
            replace_prefix_bin(path_name, old_spack_prefix, new_spack_prefix)
    else:
        if len(path_names) > 0:
            raise BinaryTextReplaceError(
                old_install_prefix, new_install_prefix)


def is_relocatable(spec):
    """Returns True if an installed spec is relocatable.

    Args:
        spec (Spec): spec to be analyzed

    Returns:
        True if the binaries of an installed spec
        are relocatable and False otherwise.

    Raises:
        ValueError: if the spec is not installed
    """
    if not spec.install_status():
        raise ValueError('spec is not installed [{0}]'.format(str(spec)))

    if spec.external or spec.virtual:
        tty.warn('external or virtual package %s is not relocatable' %
                 spec.name)
        return False

    # Explore the installation prefix of the spec
    for root, dirs, files in os.walk(spec.prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in ('.spack', 'man')]
        abs_files = [os.path.join(root, f) for f in files]
        if not all(file_is_relocatable(f) for f in abs_files if is_binary(f)):
            # If any of the file is not relocatable, the entire
            # package is not relocatable
            return False

    return True


def file_is_relocatable(file, paths_to_relocate=None):
    """Returns True if the file passed as argument is relocatable.

    Args:
        file: absolute path of the file to be analyzed

    Returns:
        True or false

    Raises:

        ValueError: if the file does not exist or the path is not absolute
    """
    default_paths_to_relocate = [spack.store.layout.root, spack.paths.prefix]
    paths_to_relocate = paths_to_relocate or default_paths_to_relocate

    if not (platform.system().lower() == 'darwin'
            or platform.system().lower() == 'linux'):
        msg = 'function currently implemented only for linux and macOS'
        raise NotImplementedError(msg)

    if not os.path.exists(file):
        raise ValueError('{0} does not exist'.format(file))

    if not os.path.isabs(file):
        raise ValueError('{0} is not an absolute path'.format(file))

    strings = executable.Executable('strings')

    # Remove the RPATHS from the strings in the executable
    set_of_strings = set(strings(file, output=str).split())

    m_type, m_subtype = mime_type(file)
    if m_type == 'application':
        tty.debug('{0},{1}'.format(m_type, m_subtype))

    if platform.system().lower() == 'linux':
        if m_subtype == 'x-executable' or m_subtype == 'x-sharedlib':
            rpaths = ':'.join(get_existing_elf_rpaths(file))
            set_of_strings.discard(rpaths)
    if platform.system().lower() == 'darwin':
        if m_subtype == 'x-mach-binary':
            rpaths, deps, idpath = macholib_get_paths(file)
            set_of_strings.discard(set(rpaths))
            set_of_strings.discard(set(deps))
            if idpath is not None:
                set_of_strings.discard(idpath)

    for path_to_relocate in paths_to_relocate:
        if any(path_to_relocate in x for x in set_of_strings):
            # One binary has the root folder not in the RPATH,
            # meaning that this spec is not relocatable
            msg = 'Found "{0}" in {1} strings'
            tty.debug(msg.format(path_to_relocate, file))
            return False

    return True


def is_binary(file):
    """Returns true if a file is binary, False otherwise

    Args:
        file: file to be tested

    Returns:
        True or False
    """
    m_type, _ = mime_type(file)

    msg = '[{0}] -> '.format(file)
    if m_type == 'application':
        tty.debug(msg + 'BINARY FILE')
        return True

    tty.debug(msg + 'TEXT FILE')
    return False


@llnl.util.lang.memoized
def mime_type(file):
    """Returns the mime type and subtype of a file.

    Args:
        file: file to be analyzed

    Returns:
        Tuple containing the MIME type and subtype
    """
    file_cmd = executable.Executable('file')
    output = file_cmd('-b', '-h', '--mime-type', file, output=str, error=str)
    tty.debug('[MIME_TYPE] {0} -> {1}'.format(file, output.strip()))
    # In corner cases the output does not contain a subtype prefixed with a /
    # In those cases add the / so the tuple can be formed.
    if '/' not in output:
        output += '/'
    split_by_slash = output.strip().split('/')
    return (split_by_slash[0], "/".join(split_by_slash[1:]))
