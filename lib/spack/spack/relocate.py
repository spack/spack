# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re
import shutil
import platform
import spack.repo
import spack.cmd
import llnl.util.lang
from spack.util.executable import Executable, ProcessError
import llnl.util.tty as tty
from macholib.MachO import MachO
from spack.spec import Spec
import macholib.mach_o


class InstallRootStringException(spack.error.SpackError):
    """
    Raised when the relocated binary still has the install root string.
    """

    def __init__(self, file_path, root_path):
        super(InstallRootStringException, self).__init__(
            "\n %s \ncontains string\n %s \n"
            "after replacing it in rpaths.\n"
            "Package should not be relocated.\n Use -a to override." %
            (file_path, root_path))


class BinaryStringReplacementException(spack.error.SpackError):
    """
    Raised when the size of the file changes after binary path substitution.
    """

    def __init__(self, file_path, old_len, new_len):
        super(BinaryStringReplacementException, self).__init__(
            "Doing a binary string replacement in %s failed.\n"
            "The size of the file changed from %s to %s\n"
            "when it should have remanined the same." %
            (file_path, old_len, new_len))


class BinaryTextReplaceException(spack.error.SpackError):
    """
    Raised when the new install path is shorter than the old install path
    so binary text replacement cannot occur.
    """

    def __init__(self, old_path, new_path):
        msg = "New path longer than old path: binary text"
        msg += " replacement not possible."
        err_msg = "The new path %s" % new_path
        err_msg += " is longer than the old path %s.\n" % old_path
        err_msg += "Text replacement in binaries will not work.\n"
        err_msg += "Create buildcache from an install path "
        err_msg += "longer than new path."
        super(BinaryTextReplaceException, self).__init__(msg, err_msg)


class PatchelfError(spack.error.SpackError):
    """
    Raised when patchelf command returns a ProcessError.
    """

    def __init__(self, error):
        super(PatchelfError, self).__init__(error)


def get_patchelf():
    """
    Returns the full patchelf binary path if available in $PATH.
    Builds and installs spack patchelf package on linux platforms
    using the first concretized spec if it is not installed and
    returns the full patchelf binary path.
    """
    # as we may need patchelf, find out where it is
    patchelf = spack.util.executable.which('patchelf')
    if patchelf is not None:
        return patchelf.path
    patchelf_spec = Spec('patchelf').concretized()
    patchelf = patchelf_spec.package
    if patchelf.installed:
        patchelf_executable = os.path.join(patchelf.prefix.bin, "patchelf")
        return patchelf_executable
    else:
        if (str(spack.architecture.platform()) == 'test' or
            str(spack.architecture.platform()) == 'darwin'):
            return None
        else:
            patchelf.do_install()
            patchelf_executable = os.path.join(patchelf.prefix.bin, "patchelf")
            return patchelf_executable


def get_existing_elf_rpaths(path_name):
    """
    Return the RPATHS returned by patchelf --print-rpath path_name
    as lists of strings.
    """

    # if we're relocating patchelf itself, use it

    if path_name[-13:] == "/bin/patchelf":
        patchelf = Executable(path_name)
    else:
        patchelf = Executable(get_patchelf())

    rpaths = list()
    try:
        output = patchelf('--print-rpath', '%s' %
                          path_name, output=str, error=str)
        rpaths = output.rstrip('\n').split(':')
    except ProcessError as e:
        msg = 'patchelf --print-rpath %s produced an error %s' % (path_name, e)
        raise PatchelfError(msg)
    return rpaths


def get_relative_rpaths(path_name, orig_dir, orig_rpaths):
    """
    Replaces orig_dir with relative path from dirname(path_name) if an rpath
    in orig_rpaths contains orig_path. Prefixes $ORIGIN
    to relative paths and returns replacement rpaths.
    """
    rel_rpaths = []
    for rpath in orig_rpaths:
        if re.match(orig_dir, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            rel_rpaths.append(os.path.join('$ORIGIN', '%s' % rel))
        else:
            rel_rpaths.append(rpath)
    return rel_rpaths


def set_placeholder(dirname):
    """
    return string of @'s with same length
    """
    return '@' * len(dirname)


def macho_make_paths_relative(path_name, old_layout_root,
                              rpaths, deps, idpath):
    """
    Replace old_dir with relative path from dirname(path_name)
    in rpaths and deps; idpaths are replaced with @rpath/libname as needed.
    Used to make machO buildcaches with relatived paths.
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


def macho_find_paths(orig_rpaths, deps, idpath,
                     old_layout_root, prefix_to_prefix):
    """
    Use the rpaths defined in the current build environment for the spec to
    define the new install prefixes to be be passed to the function which
    queries them for the location of dependency libraries and library ID for
    a dylib. This library list is used to define the new dependecy library
    path, new rpaths and the library ID for a dylib.
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
    This function is used to make machO buildcaches with relativized paths.
    Modify MachO binary path_name by replacing old_dir with new_dir
    or the relative path to spack install root.
    The old install dir in LC_ID_DYLIB is replaced with the new install dir
    using install_name_tool -id newid binary
    The old install dir in LC_LOAD_DYLIB is replaced with the new install dir
    using install_name_tool -change old new binary
    The old install dir in LC_RPATH is replaced with the new install dir using
    install_name_tool  -rpath old new binary
    """
    # avoid error message for libgcc_s
    if 'libgcc_' in cur_path:
        return
    install_name_tool = Executable('install_name_tool')

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


def modify_object_macholib(cur_path, rpaths, deps, idpath, old_prefix,
                           paths_to_paths):
    """
    Modify MachO binary path names using py-macholib.
    The old install path in LC_ID_DYLIB header is replaced with
    new absolute install path.
    The old install paths in LC_LOAD_DYLIB headers is replaced with
    new absolute install paths.
    The old install paths in LC_RPATH are not replaced because
    the replacement dependency library path is an absolute path.
    This is used when install machO buildcaches on linux or macOS.
    """

    dll = MachO(cur_path)

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
    dll = MachO(cur_path)

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

    if path_name[-13:] == "/bin/patchelf":
        bak_path = path_name + ".bak"
        shutil.copy(path_name, bak_path)
        patchelf = Executable(bak_path)
    else:
        patchelf = Executable(get_patchelf())

    try:
        patchelf('--force-rpath', '--set-rpath', '%s' % new_joined,
                 '%s' % path_name, output=str, error=str)
    except ProcessError as e:
        msg = 'patchelf --set-rpath %s failed with error %s' % (path_name, e)
        raise PatchelfError(msg)
        pass


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
    in binary files by replacing with null terminated string
    that is the same length. If the old path is shorter then the new_path
    raise an exception because this replacement would break the binary.
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
        raise BinaryTextReplaceException(old_dir, new_dir)

    with open(path_name, 'rb+') as f:
        data = f.read()
        f.seek(0)
        original_data_len = len(data)
        pat = re.compile(re.escape(old_dir).encode('utf-8') + b'([^\0]*?)\0')
        if not pat.search(data):
            return
        ndata = pat.sub(replace, data)
        if not len(ndata) == original_data_len:
            raise BinaryStringReplacementException(
                path_name, original_data_len, len(ndata))
        f.write(ndata)
        f.truncate()


def relocate_macho_binaries(path_names, old_layout_root, prefix_to_prefix):
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
        rpaths, deps, idpath = macholib_get_paths(path_name)
        paths_to_paths = macho_find_paths(rpaths, deps, idpath,
                                          old_layout_root,
                                          prefix_to_prefix)
        if platform.system().lower() == 'darwin':
            modify_macho_object(path_name, rpaths, deps,
                                idpath, paths_to_paths)
        else:
            modify_object_macholib(path_name, rpaths, deps,
                                   idpath, old_layout_root,
                                   paths_to_paths)


def relocate_elf_binaries(path_names, old_layout_root, prefix_to_prefix):
    """
    Use the current build environment defined for the buildcache spec
    to get the rpaths.
    Use patchelf to get the original rpaths and needed libraries
    from the ELF objects then modify them with the replacement rpaths
    queried from the new build environment.
    """
    for path_name in path_names:
        orig_rpaths = get_existing_elf_rpaths(path_name)
        new_rpaths = list()
        for orig_rpath in orig_rpaths:
            if orig_rpath.startswith(old_layout_root):
                for old_prefix, new_prefix in prefix_to_prefix.items():
                    if orig_rpath.startswith(old_prefix):
                        new_rpaths.append(re.sub(re.escape(old_prefix),
                                                 new_prefix, orig_rpath))
            else:
                new_rpaths.append(orig_rpath)
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


def make_elf_binaries_relative(cur_path_names, orig_path_names, old_dir):
    """
    Replace old RPATHs with paths relative to old_dir in binary files
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        orig_rpaths = get_existing_elf_rpaths(cur_path)
        if orig_rpaths:
            new_rpaths = get_relative_rpaths(orig_path, old_dir,
                                             orig_rpaths)
            modify_elf_object(cur_path, new_rpaths)


def check_files_relocatable(cur_path_names, allow_root):
    """
    Check binary files for the current install root
    """
    for cur_path in cur_path_names:
        if (not allow_root and
                not file_is_relocatable(cur_path)):
            raise InstallRootStringException(
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
        old_link_target = os.readlink(link_name)
        old_link_target = re.sub(placeholder, old_layout_root, old_link_target)
        if old_link_target.startswith(old_install_prefix):
            new_link_target = re.sub(
                old_install_prefix, new_install_prefix, old_link_target)
            os.unlink(link_name)
            os.symlink(new_link_target, link_name)
        else:
            msg = 'Old link target %s' % old_link_target
            msg += ' for symbolic link %s is outside' % link_name
            msg += ' of the old install prefix %s.\n' % old_install_prefix
            msg += 'This symbolic link will not be relocated'
            msg += ' and might break relocation.'
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
            raise BinaryTextReplaceException(
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

    strings = Executable('strings')

    # Remove the RPATHS from the strings in the executable
    set_of_strings = set(strings(file, output=str).split())

    m_type, m_subtype = mime_type(file)
    if m_type == 'application':
        tty.debug('{0},{1}'.format(m_type, m_subtype))

    if platform.system().lower() == 'linux':
        if m_subtype == 'x-executable' or m_subtype == 'x-sharedlib':
            rpaths = set(get_existing_elf_rpaths(file))
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
    file_cmd = Executable('file')
    output = file_cmd('-b', '-h', '--mime-type', file, output=str, error=str)
    tty.debug('[MIME_TYPE] {0} -> {1}'.format(file, output.strip()))
    # In corner cases the output does not contain a subtype prefixed with a /
    # In those cases add the / so the tuple can be formed.
    if '/' not in output:
        output += '/'
    return tuple(output.strip().split('/'))
