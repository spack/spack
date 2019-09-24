# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re
import platform
import spack.repo
import spack.cmd
import llnl.util.lang
import llnl.util.filesystem as fs
from spack.util.executable import Executable, ProcessError
import llnl.util.tty as tty


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


class MissingMachotoolsException(spack.error.SpackError):
    """
    Raised when the size of the file changes after binary path substitution.
    """

    def __init__(self, error):
        super(MissingMachotoolsException, self).__init__(
            "%s\n"
            "Python package machotools needs to be avaiable to list\n"
            "and modify a mach-o binary's rpaths, deps and id.\n"
            "Use virtualenv with pip install machotools or\n"
            "use spack to install the py-machotools package\n"
            "spack install py-machotools\n"
            "spack activate py-machotools\n"
            "spack load python\n"
            % error)


def get_patchelf():
    """
    Builds and installs spack patchelf package on linux platforms
    using the first concretized spec.
    Returns the full patchelf binary path.
    """
    # as we may need patchelf, find out where it is
    patchelf = spack.util.executable.which('patchelf')
    if patchelf is not None:
        return patchelf.path
    else:
        if str(spack.architecture.platform()) == 'test':
            return None
        if str(spack.architecture.platform()) == 'darwin':
            return None
        patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
        patchelf = spack.repo.get(patchelf_spec)
        if not patchelf.installed:
            patchelf.do_install(use_cache=False)
        patchelf_executable = os.path.join(patchelf.prefix.bin, "patchelf")
        return patchelf_executable


def get_existing_elf_rpaths(path_name):
    """
    Return the RPATHS returned by patchelf --print-rpath path_name
    as a list of strings.
    """
    patchelf = Executable(get_patchelf())
    try:
        output = patchelf('--print-rpath', '%s' %
                          path_name, output=str, error=str)
        return output.rstrip('\n').split(':')
    except ProcessError as e:
        tty.debug('patchelf --print-rpath produced an error on %s' %
                  path_name, e)
        return []
    return


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
            rel_rpaths.append('$ORIGIN/%s' % rel)
        else:
            rel_rpaths.append(rpath)
    return rel_rpaths


def set_placeholder(dirname):
    """
    return string of @'s with same length
    """
    return '@' * len(dirname)


def get_placeholder_rpaths(path_name, orig_rpaths):
    """
    Replaces original layout root dir with a placeholder string in all rpaths.
    """
    rel_rpaths = []
    orig_dir = spack.store.layout.root
    for rpath in orig_rpaths:
        if re.match(orig_dir, rpath):
            placeholder = set_placeholder(orig_dir)
            rel = re.sub(orig_dir, placeholder, rpath)
            rel_rpaths.append('%s' % rel)
        else:
            rel_rpaths.append(rpath)
    return rel_rpaths


def macho_get_paths(path_name):
    """
    Examines the output of otool -l path_name for these three fields:
    LC_ID_DYLIB, LC_LOAD_DYLIB, LC_RPATH and parses out the rpaths,
    dependiencies and library id.
    Returns these values.
    """
    otool = Executable('otool')
    output = otool("-l", path_name, output=str, err=str)
    last_cmd = None
    idpath = None
    rpaths = []
    deps = []
    for line in output.split('\n'):
        match = re.search('( *[a-zA-Z]+ )(.*)', line)
        if match:
            lhs = match.group(1).lstrip().rstrip()
            rhs = match.group(2)
            match2 = re.search(r'(.*) \(.*\)', rhs)
            if match2:
                rhs = match2.group(1)
            if lhs == 'cmd':
                last_cmd = rhs
            if lhs == 'path' and last_cmd == 'LC_RPATH':
                rpaths.append(rhs)
            if lhs == 'name' and last_cmd == 'LC_ID_DYLIB':
                idpath = rhs
            if lhs == 'name' and last_cmd == 'LC_LOAD_DYLIB':
                deps.append(rhs)
    return rpaths, deps, idpath


def macho_make_paths_relative(path_name, old_dir, rpaths, deps, idpath):
    """
    Replace old_dir with relative path from dirname(path_name)
    in rpaths and deps; idpaths are replaced with @rpath/libname as needed;
    replacement are returned.
    """
    new_idpath = None
    if idpath:
        new_idpath = '@rpath/%s' % os.path.basename(idpath)
    new_rpaths = list()
    new_deps = list()
    for rpath in rpaths:
        if re.match(old_dir, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            new_rpaths.append('@loader_path/%s' % rel)
        else:
            new_rpaths.append(rpath)
    for dep in deps:
        if re.match(old_dir, dep):
            rel = os.path.relpath(dep, start=os.path.dirname(path_name))
            new_deps.append('@loader_path/%s' % rel)
        else:
            new_deps.append(dep)
    return (new_rpaths, new_deps, new_idpath)


def macho_make_paths_placeholder(rpaths, deps, idpath):
    """
    Replace old_dir with a placeholder of the same length
    in rpaths and deps and idpaths is needed.
    replacement are returned.
    """
    new_idpath = None
    old_dir = spack.store.layout.root
    placeholder = set_placeholder(old_dir)
    if idpath:
        new_idpath = re.sub(old_dir, placeholder, idpath)
    new_rpaths = list()
    new_deps = list()
    for rpath in rpaths:
        if re.match(old_dir, rpath):
            ph = re.sub(old_dir, placeholder, rpath)
            new_rpaths.append('%s' % ph)
        else:
            new_rpaths.append(rpath)
    for dep in deps:
        if re.match(old_dir, dep):
            ph = re.sub(old_dir, placeholder, dep)
            new_deps.append('%s' % ph)
        else:
            new_deps.append(dep)
    return (new_rpaths, new_deps, new_idpath)


def macho_replace_paths(old_dir, new_dir, rpaths, deps, idpath):
    """
    Replace old_dir with new_dir in rpaths, deps and idpath
    and return replacements
    """
    new_idpath = None
    if idpath:
        new_idpath = idpath.replace(old_dir, new_dir)
    new_rpaths = list()
    new_deps = list()
    for rpath in rpaths:
        new_rpath = rpath.replace(old_dir, new_dir)
        new_rpaths.append(new_rpath)
    for dep in deps:
        new_dep = dep.replace(old_dir, new_dir)
        new_deps.append(new_dep)
    return new_rpaths, new_deps, new_idpath


def modify_macho_object(cur_path, rpaths, deps, idpath,
                        new_rpaths, new_deps, new_idpath):
    """
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
    if new_idpath and not idpath == new_idpath:
        install_name_tool('-id', new_idpath, str(cur_path))

    if len(deps) == len(new_deps):
        for orig, new in zip(deps, new_deps):
            if not orig == new:
                install_name_tool('-change', orig, new, str(cur_path))

    if len(rpaths) == len(new_rpaths):
        for orig, new in zip(rpaths, new_rpaths):
            if not orig == new:
                install_name_tool('-rpath', orig, new, str(cur_path))

    return


def modify_object_machotools(cur_path, rpaths, deps, idpath,
                             new_rpaths, new_deps, new_idpath):
    """
    Modify MachO binary path_name by replacing old_dir with new_dir
    or the relative path to spack install root.
    The old install dir in LC_ID_DYLIB is replaced with the new install dir
    using py-machotools
    The old install dir in LC_LOAD_DYLIB is replaced with the new install dir
    using py-machotools
    The old install dir in LC_RPATH is replaced with the new install dir using
    using py-machotools
    """
    if cur_path.endswith('.o'):
        return
    try:
        import machotools
    except ImportError as e:
        raise MissingMachotoolsException(e)
    rewriter = machotools.rewriter_factory(cur_path)
    if machotools.detect.is_dylib(cur_path):
        if not new_idpath == idpath:
            rewriter.install_name = new_idpath
    for orig, new in zip(deps, new_deps):
        if not orig == new:
            rewriter.change_dependency(orig, new)
    rewriter.commit()
    return


def machotools_get_paths(path_name):
    """
    Examines the output of otool -l path_name for these three fields:
    LC_ID_DYLIB, LC_LOAD_DYLIB, LC_RPATH and parses out the rpaths,
    dependiencies and library id.
    Returns these values.
    """
    try:
        import machotools
    except ImportError as e:
        raise MissingMachotoolsException(e)
    idpath = None
    rpaths = list()
    deps = list()
    rewriter = machotools.rewriter_factory(path_name)
    if machotools.detect.is_dylib(path_name):
        idpath = rewriter.install_name
    rpaths = rewriter.rpaths
    deps = rewriter.dependencies
    return rpaths, deps, idpath


def strings_contains_installroot(path_name, root_dir):
    """
    Check if the file contain the install root string.
    """
    strings = Executable('strings')
    output = strings('%s' % path_name,
                     output=str, err=str)
    return (root_dir in output or spack.paths.prefix in output)


def modify_elf_object(path_name, new_rpaths):
    """
    Replace orig_rpath with new_rpath in RPATH of elf object path_name
    """
    new_joined = ':'.join(new_rpaths)
    patchelf = Executable(get_patchelf())
    try:
        patchelf('--force-rpath', '--set-rpath', '%s' % new_joined,
                 '%s' % path_name, output=str, error=str)
    except ProcessError as e:
        tty.die('patchelf --set-rpath %s failed' %
                path_name, e)
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


def replace_prefix_bin(path_name, old_dir, new_dir):
    """
    Attempt to replace old install prefix with new install prefix
    in binary files by replacing with null terminated string
    that is the same length unless the old path is shorter
    """

    def replace(match):
        occurances = match.group().count(old_dir)
        padding = (len(old_dir) - len(new_dir)) * occurances
        if padding < 0:
            return data
        return match.group().replace(old_dir, new_dir) + b'\0' * padding

    with open(path_name, 'rb+') as f:
        data = f.read()
        f.seek(0)
        original_data_len = len(data)
        pat = re.compile(re.escape(old_dir) + b'([^\0]*?)\0')
        ndata = pat.sub(replace, data)
        new_data_len = len(ndata)
        if not new_data_len == original_data_len:
            raise BinaryStringReplacementException(
                path_name, original_data_len, new_data_len)
        f.write(data)
        f.truncate()


def relocate_macho_binaries(path_names, old_dir, new_dir, allow_root):
    """
    Change old_dir to new_dir in LC_RPATH of mach-o files (on macOS)
    Change old_dir to new_dir in LC_ID and LC_DEP of mach-o files
    Account for the case where old_dir is now a placeholder
    """
    placeholder = set_placeholder(old_dir)
    for path_name in path_names:
        deps = set()
        idpath = None
        if platform.system().lower() == 'darwin':
            if path_name.endswith('.o'):
                continue
            else:
                rpaths, deps, idpath = macho_get_paths(path_name)
        else:
            rpaths, deps, idpath = machotools_get_paths(path_name)
        # one pass to replace placeholder
        (n_rpaths,
         n_deps,
         n_idpath) = macho_replace_paths(placeholder,
                                         new_dir,
                                         rpaths,
                                         deps,
                                         idpath)
        # another pass to replace old_dir
        (new_rpaths,
         new_deps,
         new_idpath) = macho_replace_paths(old_dir,
                                           new_dir,
                                           n_rpaths,
                                           n_deps,
                                           n_idpath)
        if platform.system().lower() == 'darwin':
            modify_macho_object(path_name,
                                rpaths, deps, idpath,
                                new_rpaths, new_deps, new_idpath)
        else:
            modify_object_machotools(path_name,
                                     rpaths, deps, idpath,
                                     new_rpaths, new_deps, new_idpath)

        if not new_dir == old_dir:
            if len(new_dir) <= len(old_dir):
                replace_prefix_bin(path_name, old_dir, new_dir)
            else:
                tty.warn('Cannot do a binary string replacement'
                         ' with padding for %s'
                         ' because %s is longer than %s' %
                         (path_name, new_dir, old_dir))


def relocate_elf_binaries(path_names, old_dir, new_dir, allow_root):
    """
    Change old_dir to new_dir in RPATHs of elf binaries
    Account for the case where old_dir is now a placeholder
    """
    placeholder = set_placeholder(old_dir)
    for path_name in path_names:
        orig_rpaths = get_existing_elf_rpaths(path_name)
        if orig_rpaths:
            # one pass to replace placeholder
            n_rpaths = substitute_rpath(orig_rpaths,
                                        placeholder, new_dir)
            # one pass to replace old_dir
            new_rpaths = substitute_rpath(n_rpaths,
                                          old_dir, new_dir)
            modify_elf_object(path_name, new_rpaths)
            if not new_dir == old_dir:
                if len(new_dir) <= len(old_dir):
                    replace_prefix_bin(path_name, old_dir, new_dir)
                else:
                    tty.warn('Cannot do a binary string replacement'
                             ' with padding for %s'
                             ' because %s is longer than %s.' %
                             (path_name, new_dir, old_dir))


def make_link_relative(cur_path_names, orig_path_names):
    """
    Change absolute links to be relative.
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        old_src = os.readlink(orig_path)
        new_src = os.path.relpath(old_src, orig_path)

        os.unlink(cur_path)
        os.symlink(new_src, cur_path)


def make_macho_binaries_relative(cur_path_names, orig_path_names, old_dir,
                                 allow_root):
    """
    Replace old RPATHs with paths relative to old_dir in binary files
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        rpaths = set()
        deps = set()
        idpath = None
        if platform.system().lower() == 'darwin':
            (rpaths, deps, idpath) = macho_get_paths(cur_path)
        else:
            (rpaths, deps, idpath) = machotools_get_paths(cur_path)
        (new_rpaths,
         new_deps,
         new_idpath) = macho_make_paths_relative(orig_path, old_dir,
                                                 rpaths, deps, idpath)
        if platform.system().lower() == 'darwin':
            modify_macho_object(cur_path,
                                rpaths, deps, idpath,
                                new_rpaths, new_deps, new_idpath)
        else:
            modify_object_machotools(cur_path,
                                     rpaths, deps, idpath,
                                     new_rpaths, new_deps, new_idpath)

        if (not allow_root and
                not file_is_relocatable(cur_path)):
            raise InstallRootStringException(cur_path, old_dir)


def make_elf_binaries_relative(cur_path_names, orig_path_names, old_dir,
                               allow_root):
    """
    Replace old RPATHs with paths relative to old_dir in binary files
    """
    for cur_path, orig_path in zip(cur_path_names, orig_path_names):
        orig_rpaths = get_existing_elf_rpaths(cur_path)
        if orig_rpaths:
            new_rpaths = get_relative_rpaths(orig_path, old_dir,
                                             orig_rpaths)
            modify_elf_object(cur_path, new_rpaths)
        if (not allow_root and
                not file_is_relocatable(cur_path)):
            raise InstallRootStringException(cur_path, old_dir)


def check_files_relocatable(cur_path_names, allow_root):
    """
    Check binary files for the current install root
    """
    for cur_path in cur_path_names:
        if (not allow_root and
                not file_is_relocatable(cur_path)):
            raise InstallRootStringException(
                cur_path, spack.store.layout.root)


def make_link_placeholder(cur_path_names, cur_dir, old_dir):
    """
    Replace old install path with placeholder in absolute links.

    Links in ``cur_path_names`` must link to absolute paths.
    """
    for cur_path in cur_path_names:
        placeholder = set_placeholder(spack.store.layout.root)
        placeholder_prefix = old_dir.replace(spack.store.layout.root,
                                             placeholder)
        cur_src = os.readlink(cur_path)
        rel_src = os.path.relpath(cur_src, cur_dir)
        new_src = os.path.join(placeholder_prefix, rel_src)

        os.unlink(cur_path)
        os.symlink(new_src, cur_path)


def relocate_links(path_names, old_dir, new_dir):
    """
    Replace old path with new path in link sources.

    Links in ``path_names`` must link to absolute paths or placeholders.
    """
    placeholder = set_placeholder(old_dir)
    for path_name in path_names:
        old_src = os.readlink(path_name)
        # replace either placeholder or old_dir
        new_src = old_src.replace(placeholder, new_dir, 1)
        new_src = new_src.replace(old_dir, new_dir, 1)

        os.unlink(path_name)
        os.symlink(new_src, path_name)


def relocate_text(path_names, oldpath, newpath, oldprefix, newprefix):
    """
    Replace old path with new path in text file path_name
    """
    fs.filter_file('%s' % oldpath, '%s' % newpath, *path_names,
                   backup=False, string=True)
    sbangre = '#!/bin/bash %s/bin/sbang' % oldprefix
    sbangnew = '#!/bin/bash %s/bin/sbang' % newprefix
    fs.filter_file(sbangre, sbangnew, *path_names,
                   backup=False, string=True)
    fs.filter_file(oldprefix, newprefix, *path_names,
                   backup=False, string=True)


def substitute_rpath(orig_rpath, topdir, new_root_path):
    """
    Replace topdir with new_root_path RPATH list orig_rpath
    """
    new_rpaths = []
    for path in orig_rpath:
        new_rpath = path.replace(topdir, new_root_path)
        new_rpaths.append(new_rpath)
    return new_rpaths


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


def file_is_relocatable(file):
    """Returns True if the file passed as argument is relocatable.

    Args:
        file: absolute path of the file to be analyzed

    Returns:
        True or false

    Raises:

        ValueError: if the file does not exist or the path is not absolute
    """

    if not (platform.system().lower() == 'darwin'
            or platform.system().lower() == 'linux'):
        msg = 'function currently implemented only for linux and macOS'
        raise NotImplementedError(msg)

    if not os.path.exists(file):
        raise ValueError('{0} does not exist'.format(file))

    if not os.path.isabs(file):
        raise ValueError('{0} is not an absolute path'.format(file))

    strings = Executable('strings')
    patchelf = Executable(get_patchelf())

    # Remove the RPATHS from the strings in the executable
    set_of_strings = set(strings(file, output=str).split())

    m_type, m_subtype = mime_type(file)
    if m_type == 'application':
        tty.debug('{0},{1}'.format(m_type, m_subtype))

    if platform.system().lower() == 'linux':
        if m_subtype == 'x-executable' or m_subtype == 'x-sharedlib':
            rpaths = patchelf('--print-rpath', file, output=str).strip()
            set_of_strings.discard(rpaths.strip())
    if platform.system().lower() == 'darwin':
        if m_subtype == 'x-mach-binary':
            rpaths, deps, idpath = macho_get_paths(file)
            set_of_strings.discard(set(rpaths))
            set_of_strings.discard(set(deps))
            if idpath is not None:
                set_of_strings.discard(idpath)

    if any(spack.store.layout.root in x for x in set_of_strings):
        # One binary has the root folder not in the RPATH,
        # meaning that this spec is not relocatable
        msg = 'Found "{0}" in {1} strings'
        tty.debug(msg.format(spack.store.layout.root, file))
        return False

    if any(spack.paths.prefix in x for x in set_of_strings):
        # One binary has the root folder not in the RPATH,
        # meaning that this spec is not relocatable
        msg = 'Found "{0}" in {1} strings'
        tty.debug(msg.format(spack.paths.prefix, file))
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
    if '/' not in output:
        output += '/'
    return tuple(output.strip().split('/'))
