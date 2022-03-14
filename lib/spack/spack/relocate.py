# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import multiprocessing.pool
import os
import re
import shutil

import macholib.mach_o
import macholib.MachO

import llnl.util.lang
import llnl.util.tty as tty

import spack.bootstrap
import spack.platforms
import spack.repo
import spack.spec
import spack.util.executable as executable

is_macos = (str(spack.platforms.real_host()) == 'darwin')


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
    """Return the full path to the patchelf binary, if available, else None."""
    if is_macos:
        return None

    patchelf = executable.which('patchelf')
    if patchelf is None:
        with spack.bootstrap.ensure_bootstrap_configuration():
            patchelf = spack.bootstrap.ensure_patchelf_in_path_or_raise()

    return patchelf.path


def _elf_rpaths_for(path):
    """Return the RPATHs for an executable or a library.

    The RPATHs are obtained by ``patchelf --print-rpath PATH``.

    Args:
        path (str): full path to the executable or library

    Return:
        RPATHs as a list of strings.
    """
    # If we're relocating patchelf itself, use it
    patchelf_path = path if path.endswith("/bin/patchelf") else _patchelf()
    patchelf = executable.Executable(patchelf_path)

    output = ''
    try:
        output = patchelf('--print-rpath', path, output=str, error=str)
        output = output.strip('\n')
    except executable.ProcessError as e:
        msg = 'patchelf --print-rpath {0} produced an error [{1}]'
        tty.warn(msg.format(path, str(e)))

    return output.split(':') if output else []


def _make_relative(reference_file, path_root, paths):
    """Return a list where any path in ``paths`` that starts with
    ``path_root`` is made relative to the directory in which the
    reference file is stored.

    After a path is made relative it is prefixed with the ``$ORIGIN``
    string.

    Args:
        reference_file (str): file from which the reference directory
            is computed
        path_root (str): root of the relative paths
        paths: (list) paths to be examined

    Returns:
        List of relative paths
    """
    start_directory = os.path.dirname(reference_file)
    pattern = re.compile(path_root)
    relative_paths = []

    for path in paths:
        if pattern.match(path):
            rel = os.path.relpath(path, start=start_directory)
            path = os.path.join('$ORIGIN', rel)

        relative_paths.append(path)

    return relative_paths


def _normalize_relative_paths(start_path, relative_paths):
    """Normalize the relative paths with respect to the original path name
    of the file (``start_path``).

    The paths that are passed to this function existed or were relevant
    on another filesystem, so os.path.abspath cannot be used.

    A relative path may contain the signifier $ORIGIN. Assuming that
    ``start_path`` is absolute, this implies that the relative path
    (relative to start_path) should be replaced with an absolute path.

    Args:
        start_path (str): path from which the starting directory
            is extracted
        relative_paths (str): list of relative paths as obtained by a
            call to :ref:`_make_relative`

    Returns:
        List of normalized paths
    """
    normalized_paths = []
    pattern = re.compile(re.escape('$ORIGIN'))
    start_directory = os.path.dirname(start_path)

    for path in relative_paths:
        if path.startswith('$ORIGIN'):
            sub = pattern.sub(start_directory, path)
            path = os.path.normpath(sub)
        normalized_paths.append(path)

    return normalized_paths


def _placeholder(dirname):
    """String of  of @'s with same length of the argument"""
    return '@' * len(dirname)


def _decode_macho_data(bytestring):
    return bytestring.rstrip(b'\x00').decode('ascii')


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
    args = []

    if idpath:
        new_idpath = paths_to_paths.get(idpath, None)
        if new_idpath and not idpath == new_idpath:
            args += ['-id', new_idpath]
    for dep in deps:
        new_dep = paths_to_paths.get(dep)
        if new_dep and dep != new_dep:
            args += ['-change', dep, new_dep]

    for orig_rpath in rpaths:
        new_rpath = paths_to_paths.get(orig_rpath)
        if new_rpath and not orig_rpath == new_rpath:
            args += ['-rpath', orig_rpath, new_rpath]

    if args:
        args.append(str(cur_path))
        install_name_tool = executable.Executable('install_name_tool')
        install_name_tool(*args)

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
    dll.rewriteLoadCommands(paths_to_paths.get)

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
    """Get rpaths, dependent libraries, and library id of mach-o objects.
    """
    headers = macholib.MachO.MachO(cur_path).headers
    if not headers:
        tty.warn("Failed to read Mach-O headers: {0}".format(cur_path))
        commands = []
    else:
        if len(headers) > 1:
            # Reproduce original behavior of only returning the last mach-O
            # header section
            tty.warn("Encountered fat binary: {0}".format(cur_path))
        if headers[-1].filetype == 'dylib_stub':
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

    This function uses ``patchelf`` to set RPATHs.

    Args:
        target: target executable. Must be an ELF object.
        rpaths: paths to be set in the RPATH

    Returns:
        A string concatenating the stdout and stderr of the call
        to ``patchelf``
    """
    # Join the paths using ':' as a separator
    rpaths_str = ':'.join(rpaths)

    # If we're relocating patchelf itself, make a copy and use it
    bak_path = None
    if target.endswith("/bin/patchelf"):
        bak_path = target + ".bak"
        shutil.copy(target, bak_path)

    patchelf, output = executable.Executable(bak_path or _patchelf()), None
    try:
        # TODO: revisit the use of --force-rpath as it might be conditional
        # TODO: if we want to support setting RUNPATH from binary packages
        patchelf_args = ['--force-rpath', '--set-rpath', rpaths_str, target]
        output = patchelf(*patchelf_args, output=str, error=str)
    except executable.ProcessError as e:
        msg = 'patchelf --force-rpath --set-rpath {0} failed with error {1}'
        tty.warn(msg.format(target, e))
    finally:
        if bak_path and os.path.exists(bak_path):
            os.remove(bak_path)
    return output


def needs_binary_relocation(m_type, m_subtype):
    """Returns True if the file with MIME type/subtype passed as arguments
    needs binary relocation, False otherwise.

    Args:
        m_type (str): MIME type of the file
        m_subtype (str): MIME subtype of the file
    """
    if m_type == 'application':
        if m_subtype in ('x-executable', 'x-sharedlib', 'x-mach-binary'):
            return True
    return False


def needs_text_relocation(m_type, m_subtype):
    """Returns True if the file with MIME type/subtype passed as arguments
    needs text relocation, False otherwise.

    Args:
        m_type (str): MIME type of the file
        m_subtype (str): MIME subtype of the file
    """
    return m_type == 'text'


def _replace_prefix_text(filename, compiled_prefixes):
    """Replace all the occurrences of the old install prefix with a
    new install prefix in text files that are utf-8 encoded.

    Args:
        filename (str): target text file (utf-8 encoded)
        compiled_prefixes (OrderedDict): OrderedDictionary where the keys are
        precompiled regex of the old prefixes and the values are the new
        prefixes (uft-8 encoded)
    """
    with open(filename, 'rb+') as f:
        data = f.read()
        f.seek(0)
        for orig_prefix_rexp, new_bytes in compiled_prefixes.items():
            data = orig_prefix_rexp.sub(new_bytes, data)
        f.write(data)
        f.truncate()


def _replace_prefix_bin(filename, byte_prefixes):
    """Replace all the occurrences of the old install prefix with a
    new install prefix in binary files.

    The new install prefix is prefixed with ``os.sep`` until the
    lengths of the prefixes are the same.

    Args:
        filename (str): target binary file
        byte_prefixes (OrderedDict): OrderedDictionary where the keys are
        precompiled regex of the old prefixes and the values are the new
        prefixes (uft-8 encoded)
    """

    with open(filename, 'rb+') as f:
        data = f.read()
        f.seek(0)
        for orig_bytes, new_bytes in byte_prefixes.items():
            original_data_len = len(data)
            # Skip this hassle if not found
            if orig_bytes not in data:
                continue
            # We only care about this problem if we are about to replace
            length_compatible = len(new_bytes) <= len(orig_bytes)
            if not length_compatible:
                tty.debug('Binary failing to relocate is %s' % filename)
                raise BinaryTextReplaceError(orig_bytes, new_bytes)
            pad_length = len(orig_bytes) - len(new_bytes)
            padding = os.sep * pad_length
            padding = padding.encode('utf-8')
            data = data.replace(orig_bytes, new_bytes + padding)
            # Really needs to be the same length
            if not len(data) == original_data_len:
                print('Length of pad:', pad_length, 'should be', len(padding))
                print(new_bytes, 'was to replace', orig_bytes)
                raise BinaryStringReplacementError(
                    filename, original_data_len, len(data))
        f.write(data)
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
            if is_macos:
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
            if is_macos:
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
            if is_macos:
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
            if is_macos:
                modify_macho_object(path_name, rpaths, deps,
                                    idpath, paths_to_paths)
            else:
                modify_object_macholib(path_name,
                                       paths_to_paths)


def _transform_rpaths(orig_rpaths, orig_root, new_prefixes):
    """Return an updated list of RPATHs where each entry in the original list
    starting with the old root is relocated to another place according to the
    mapping passed as argument.

    Args:
        orig_rpaths (list): list of the original RPATHs
        orig_root (str): original root to be substituted
        new_prefixes (dict): dictionary that maps the original prefixes to
            where they should be relocated

    Returns:
        List of paths
    """
    new_rpaths = []
    for orig_rpath in orig_rpaths:
        # If the original RPATH doesn't start with the target root
        # append it verbatim and proceed
        if not orig_rpath.startswith(orig_root):
            new_rpaths.append(orig_rpath)
            continue

        # Otherwise inspect the mapping and transform + append any prefix
        # that starts with a registered key
        # avoiding duplicates
        for old_prefix, new_prefix in new_prefixes.items():
            if orig_rpath.startswith(old_prefix):
                new_rpath = re.sub(re.escape(old_prefix), new_prefix,
                                   orig_rpath)
                if new_rpath not in new_rpaths:
                    new_rpaths.append(new_rpath)
    return new_rpaths


def relocate_elf_binaries(binaries, orig_root, new_root,
                          new_prefixes, rel, orig_prefix, new_prefix):
    """Relocate the binaries passed as arguments by changing their RPATHs.

    Use patchelf to get the original RPATHs and then replace them with
    rpaths in the new directory layout.

    New RPATHs are determined from a dictionary mapping the prefixes in the
    old directory layout to the prefixes in the new directory layout if the
    rpath was in the old layout root, i.e. system paths are not replaced.

    Args:
        binaries (list): list of binaries that might need relocation, located
            in the new prefix
        orig_root (str): original root to be substituted
        new_root (str): new root to be used, only relevant for relative RPATHs
        new_prefixes (dict): dictionary that maps the original prefixes to
            where they should be relocated
        rel (bool): True if the RPATHs are relative, False if they are absolute
        orig_prefix (str): prefix where the executable was originally located
        new_prefix (str): prefix where we want to relocate the executable
    """
    for new_binary in binaries:
        orig_rpaths = _elf_rpaths_for(new_binary)
        # TODO: Can we deduce `rel` from the original RPATHs?
        if rel:
            # Get the file path in the original prefix
            orig_binary = re.sub(
                re.escape(new_prefix), orig_prefix, new_binary
            )

            # Get the normalized RPATHs in the old prefix using the file path
            # in the orig prefix
            orig_norm_rpaths = _normalize_relative_paths(
                orig_binary, orig_rpaths
            )
            # Get the normalize RPATHs in the new prefix
            new_norm_rpaths = _transform_rpaths(
                orig_norm_rpaths, orig_root, new_prefixes
            )
            # Get the relative RPATHs in the new prefix
            new_rpaths = _make_relative(
                new_binary, new_root, new_norm_rpaths
            )
            # check to see if relative rpaths are changed before rewriting
            if sorted(new_rpaths) != sorted(orig_rpaths):
                _set_elf_rpaths(new_binary, new_rpaths)
        else:
            new_rpaths = _transform_rpaths(
                orig_rpaths, orig_root, new_prefixes
            )
            _set_elf_rpaths(new_binary, new_rpaths)


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
        os.symlink(relative_target, new_link)


def make_macho_binaries_relative(cur_path_names, orig_path_names,
                                 old_layout_root):
    """
    Replace old RPATHs with paths relative to old_dir in binary files
    """
    if not is_macos:
        return

    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        (rpaths, deps, idpath) = macholib_get_paths(cur_path)
        paths_to_paths = macho_make_paths_relative(
            orig_path, old_layout_root, rpaths, deps, idpath
        )
        modify_macho_object(cur_path, rpaths, deps, idpath, paths_to_paths)


def make_elf_binaries_relative(new_binaries, orig_binaries, orig_layout_root):
    """Replace the original RPATHs in the new binaries making them
    relative to the original layout root.

    Args:
        new_binaries (list): new binaries whose RPATHs is to be made relative
        orig_binaries (list): original binaries
        orig_layout_root (str): path to be used as a base for making
            RPATHs relative
    """
    for new_binary, orig_binary in zip(new_binaries, orig_binaries):
        orig_rpaths = _elf_rpaths_for(new_binary)
        if orig_rpaths:
            new_rpaths = _make_relative(
                orig_binary, orig_layout_root, orig_rpaths
            )
            _set_elf_rpaths(new_binary, new_rpaths)


def raise_if_not_relocatable(binaries, allow_root):
    """Raise an error if any binary in the list is not relocatable.

    Args:
        binaries (list): list of binaries to check
        allow_root (bool): whether root dir is allowed or not in a binary

    Raises:
        InstallRootStringError: if the file is not relocatable
    """
    for binary in binaries:
        if not (allow_root or file_is_relocatable(binary)):
            raise InstallRootStringError(binary, spack.store.layout.root)


def relocate_links(links, orig_layout_root,
                   orig_install_prefix, new_install_prefix):
    """Relocate links to a new install prefix.

    The symbolic links are relative to the original installation prefix.
    The old link target is read and the placeholder is replaced by the old
    layout root. If the old link target is in the old install prefix, the new
    link target is create by replacing the old install prefix with the new
    install prefix.

    Args:
        links (list): list of links to be relocated
        orig_layout_root (str): original layout root
        orig_install_prefix (str): install prefix of the original installation
        new_install_prefix (str): install prefix where we want to relocate
    """
    placeholder = _placeholder(orig_layout_root)
    abs_links = [os.path.join(new_install_prefix, link) for link in links]
    for abs_link in abs_links:
        link_target = os.readlink(abs_link)
        link_target = re.sub(placeholder, orig_layout_root, link_target)
        # If the link points to a file in the original install prefix,
        # compute the corresponding target in the new prefix and relink
        if link_target.startswith(orig_install_prefix):
            link_target = re.sub(
                orig_install_prefix, new_install_prefix, link_target
            )
            os.unlink(abs_link)
            os.symlink(link_target, abs_link)

        # If the link is absolute and has not been relocated then
        # warn the user about that
        if (os.path.isabs(link_target) and
            not link_target.startswith(new_install_prefix)):
            msg = ('Link target "{0}" for symbolic link "{1}" is outside'
                   ' of the new install prefix {2}')
            tty.warn(msg.format(link_target, abs_link, new_install_prefix))


def relocate_text(files, prefixes, concurrency=32):
    """Relocate text file from the original installation prefix to the
     new prefix.

     Relocation also affects the the path in Spack's sbang script.

     Args:
         files (list): Text files to be relocated
         prefixes (OrderedDict): String prefixes which need to be changed
         concurrency (int): Preferred degree of parallelism
    """

    # This now needs to be handled by the caller in all cases
    # orig_sbang = '#!/bin/bash {0}/bin/sbang'.format(orig_spack)
    # new_sbang = '#!/bin/bash {0}/bin/sbang'.format(new_spack)

    compiled_prefixes = collections.OrderedDict({})

    for orig_prefix, new_prefix in prefixes.items():
        if orig_prefix != new_prefix:
            orig_bytes = orig_prefix.encode('utf-8')
            orig_prefix_rexp = re.compile(
                b'(?<![\\w\\-_/])([\\w\\-_]*?)%s([\\w\\-_/]*)' % orig_bytes)
            new_bytes = b'\\1%s\\2' % new_prefix.encode('utf-8')
            compiled_prefixes[orig_prefix_rexp] = new_bytes

    # Do relocations on text that refers to the install tree
    # multiprocesing.ThreadPool.map requires single argument

    args = []
    for filename in files:
        args.append((filename, compiled_prefixes))

    tp = multiprocessing.pool.ThreadPool(processes=concurrency)
    try:
        tp.map(llnl.util.lang.star(_replace_prefix_text), args)
    finally:
        tp.terminate()
        tp.join()


def relocate_text_bin(binaries, prefixes, concurrency=32):
    """Replace null terminated path strings hard coded into binaries.

    The new install prefix must be shorter than the original one.

    Args:
        binaries (list): binaries to be relocated
        prefixes (OrderedDict): String prefixes which need to be changed.
        concurrency (int): Desired degree of parallelism.

    Raises:
      BinaryTextReplaceError: when the new path is longer than the old path
    """
    byte_prefixes = collections.OrderedDict({})

    for orig_prefix, new_prefix in prefixes.items():
        if orig_prefix != new_prefix:
            if isinstance(orig_prefix, bytes):
                orig_bytes = orig_prefix
            else:
                orig_bytes = orig_prefix.encode('utf-8')
            if isinstance(new_prefix, bytes):
                new_bytes = new_prefix
            else:
                new_bytes = new_prefix.encode('utf-8')
            byte_prefixes[orig_bytes] = new_bytes

    # Do relocations on text in binaries that refers to the install tree
    # multiprocesing.ThreadPool.map requires single argument
    args = []

    for binary in binaries:
        args.append((binary, byte_prefixes))

    tp = multiprocessing.pool.ThreadPool(processes=concurrency)

    try:
        tp.map(llnl.util.lang.star(_replace_prefix_bin), args)
    finally:
        tp.terminate()
        tp.join()


def is_relocatable(spec):
    """Returns True if an installed spec is relocatable.

    Args:
        spec (spack.spec.Spec): spec to be analyzed

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


def file_is_relocatable(filename, paths_to_relocate=None):
    """Returns True if the filename passed as argument is relocatable.

    Args:
        filename: absolute path of the file to be analyzed

    Returns:
        True or false

    Raises:

        ValueError: if the filename does not exist or the path is not absolute
    """
    default_paths_to_relocate = [spack.store.layout.root, spack.paths.prefix]
    paths_to_relocate = paths_to_relocate or default_paths_to_relocate

    if not os.path.exists(filename):
        raise ValueError('{0} does not exist'.format(filename))

    if not os.path.isabs(filename):
        raise ValueError('{0} is not an absolute path'.format(filename))

    strings = executable.Executable('strings')

    # Remove the RPATHS from the strings in the executable
    set_of_strings = set(strings(filename, output=str).split())

    m_type, m_subtype = mime_type(filename)
    if m_type == 'application':
        tty.debug('{0},{1}'.format(m_type, m_subtype))

    if not is_macos:
        if m_subtype == 'x-executable' or m_subtype == 'x-sharedlib':
            rpaths = ':'.join(_elf_rpaths_for(filename))
            set_of_strings.discard(rpaths)
    else:
        if m_subtype == 'x-mach-binary':
            rpaths, deps, idpath = macholib_get_paths(filename)
            set_of_strings.discard(set(rpaths))
            set_of_strings.discard(set(deps))
            if idpath is not None:
                set_of_strings.discard(idpath)

    for path_to_relocate in paths_to_relocate:
        if any(path_to_relocate in x for x in set_of_strings):
            # One binary has the root folder not in the RPATH,
            # meaning that this spec is not relocatable
            msg = 'Found "{0}" in {1} strings'
            tty.debug(msg.format(path_to_relocate, filename))
            return False

    return True


def is_binary(filename):
    """Returns true if a file is binary, False otherwise

    Args:
        filename: file to be tested

    Returns:
        True or False
    """
    m_type, _ = mime_type(filename)

    msg = '[{0}] -> '.format(filename)
    if m_type == 'application':
        tty.debug(msg + 'BINARY FILE')
        return True

    tty.debug(msg + 'TEXT FILE')
    return False


@llnl.util.lang.memoized
def _get_mime_type():
    file_cmd = executable.which('file')
    for arg in ['-b', '-h', '--mime-type']:
        file_cmd.add_default_arg(arg)
    return file_cmd


@llnl.util.lang.memoized
def mime_type(filename):
    """Returns the mime type and subtype of a file.

    Args:
        filename: file to be analyzed

    Returns:
        Tuple containing the MIME type and subtype
    """
    output = _get_mime_type()(filename, output=str, error=str).strip()
    tty.debug('==> ' + output)
    type, _, subtype = output.partition('/')
    return type, subtype


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
    if mime_type(abspath) != ('application', 'x-mach-binary'):
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
    spack_root = spack.store.layout.root
    for name in deps:
        if name.startswith(spack_root):
            tty.debug("Spack-installed dependency for {0}: {1}"
                      .format(abspath, name))
            (dirname, basename) = os.path.split(name)
            if dirname != root or dirname in rpaths:
                # Only change the rpath if it's a dependency *or* if the root
                # rpath was already added to the library (this is to prevent
                # GCC or similar getting rpaths when they weren't at all
                # configured)
                args += ['-change', name, '@rpath/' + basename]
                add_rpaths.add(dirname.rstrip('/'))

    # Check for nonexistent rpaths (often added by spack linker overzealousness
    # with both lib/ and lib64/) and duplicate rpaths
    for (rpath, count) in rpaths.items():
        if (rpath.startswith('@loader_path')
                or rpath.startswith('@executable_path')):
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
            tty_debug("Rpath appears {0} times in {1}: {2}".format(
                count, abspath, rpath
            ))
            del_rpaths.add(rpath)

    # Delete bad rpaths
    for rpath in del_rpaths:
        args += ['-delete_rpath', rpath]

    # Add missing rpaths that are not set for deletion
    for rpath in add_rpaths - del_rpaths - set(rpaths):
        args += ['-add_rpath', rpath]

    if not args:
        # No fixes needed
        return False

    args.append(abspath)
    executable.Executable('install_name_tool')(*args)
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
        tty.warn('external or virtual package cannot be fixed up: {0!s}'
                 .format(spec))
        return False

    if 'platform=darwin' not in spec:
        raise NotImplementedError('fixup_macos_rpaths requires macOS')

    applied = 0

    libs = frozenset(['lib', 'lib64', 'libexec', 'plugins',
                      'Library', 'Frameworks'])
    prefix = spec.prefix

    if not os.path.exists(prefix):
        raise RuntimeError(
            'Could not fix up install prefix spec {0} because it does '
            'not exist: {1!s}'.format(prefix, spec.name)
        )

    # Explore the installation prefix of the spec
    for root, dirs, files in os.walk(prefix, topdown=True):
        dirs[:] = set(dirs) & libs
        for name in files:
            try:
                needed_fix = fixup_macos_rpath(root, name)
            except Exception as e:
                tty.warn("Failed to apply library fixups to: {0}/{1}: {2!s}"
                         .format(root, name, e))
                needed_fix = False
            if needed_fix:
                applied += 1

    specname = spec.format('{name}{/hash:7}')
    if applied:
        tty.info('Fixed rpaths for {0:d} {1} installed to {2}'.format(
            applied,
            "binary" if applied == 1 else "binaries",
            specname
        ))
    else:
        tty.debug('No rpath fixup needed for ' + specname)
