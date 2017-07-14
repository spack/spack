#  "Benedikt Hegner (CERN)"
#  "Patrick Gartung (FNAL)"

import os
import stat
import platform
import re
from spack.util.executable import which
from llnl.util.filesystem import filter_file
import llnl.util.tty as tty


def get_existing_elf_rpaths(path_name, patchelf_executable):
    """
    Return the RPATHS in given elf file as a list of strings.
    """
    if platform.system() == 'Linux':
        command = which(patchelf_executable)
        output = command('--print-rpath', '%s' %
                         path_name, output=str, err=str)
        if command.returncode != 0:
            tty.warn('failed reading rpath for %s.' % path_name)
            return False
        return output.rstrip('\n').split(':')
    else:
        tty.die('relocation not supported for this platform')
    return retval


def get_relative_rpaths(path_name, orig_dir, orig_rpaths):
    rel_rpaths = set()
    for rpath in orig_rpaths:
        if re.match(orig_dir, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            rel_rpaths.add('$ORIGIN/%s' % rel)
        else:
            rel_rpaths.add(rpath)
    return rel_rpaths


def modify_macho_object(path_name, old_dir, new_dir, relative):
    """
    Modify MachO binaries by changing rpaths,and id and dependency lib paths.
    Examines the output of otool -l for these three patterns
    cmd LC_ID_DYLIB
    cmdsize 160
    name /Users/gartung/spack-macdev/opt/spack/darwin-x86_64/clang-7.0.2
    -apple/tcl-8.6.5-xfeydlhaojmei6iws2rnxndvriym242k/lib/libtcl8.6.dylib
    (offset 24)
    cmd LC_LOAD_DYLIB
    cmdsize 160
    name /Users/gartung/spack-macdev/opt/spack/darwin-x86_64/clang-7.0.2
    -apple/zlib-1.2.8-cyvcqvrzlgurne424y55hxvfucvz2354/lib/libz.1.dylib
    (offset 24)
    cmd LC_RPATH
    cmdsize 128
    path /Users/gartung/spack-macdev/opt/spack/darwin-x86_64/clang-7.0.2
    -apple/xz-5.2.2-d4ecxpuzf2g3ycz3cnj3xmdj7zdnuqwb/lib
    (offset 12)
    the old install dir in LC_LOAD_DYLIB is replaced with the new install dir
    using install_name_tool -id newid binary
    the old install dir in LC_LOAD_DYLIB is replaced with the new install dir
    using install_name_tool -change old new binary
    the old install dir in LC_RPATH is replaced with the new install dir using
    install_name_tool  -rpath old new binary
    """
    if 'libgcc_' in path_name:
        return
    otool = which('otool')
    output = otool("-l", path_name, output=str, err=str)
    if otool.returncode != 0:
        tty.warn('failed reading rpath for %s.' % path_name)
        return False
    last_cmd = None
    idpath = ''
    rpaths = []
    deps = []
    for line in output.split('\n'):
        match = re.search('( *[a-zA-Z]+ )(.*)', line)
        if match:
            lhs = match.group(1).lstrip().rstrip()
            rhs = match.group(2)
            match2 = re.search('(.*) \(.*\)', rhs)
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
    id = None
    nrpaths = []
    ndeps = []
    if relative:
        id = '@rpath/%s' % os.path.basename(idpath)
        for rpath in rpaths:
            if re.match(old_dir, rpath):
                rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
                nrpaths.append('@loader_path/%s' % rel)
            else:
                nrpaths.append(rpath)
        for dep in deps:
            if re.match(old_dir, dep):
                rel = os.path.relpath(dep, start=os.path.dirname(path_name))
                ndeps.append('@loader_path/%s' % rel)
            else:
                ndeps.append(dep)
    else:
        id = idpath.replace(old_dir, new_dir)
        for rpath in rpaths:
            nrpath = rpath.replace(old_dir, new_dir)
            nrpaths.append(nrpath)
        for dep in deps:
            ndep = dep.replace(old_dir, new_dir)
            ndeps.append(ndep)

    st = os.stat(path_name)
    wmode = os.access(path_name, os.W_OK)
    if not wmode:
        os.chmod(path_name, st.st_mode | stat.S_IWUSR)

    install_name_tool = which('install_name_tool')
    if id:
        output = install_name_tool('-id', id, path_name, output=str, err=str)
        if install_name_tool.returncode != 0:
            tty.warn('failed writing id for %s.' % path_name)
            tty.warn(output)

    for orig, new in zip(deps, ndeps):
        output = install_name_tool('-change', orig, new, path_name)
        if install_name_tool.returncode != 0:
            tty.warn('failed writing dep for %s.' % path_name)
            tty.warn(output)

    for orig, new in zip(rpaths, nrpaths):
        output = install_name_tool('-rpath', orig, new, path_name)
        if install_name_tool.returncode != 0:
            tty.warn('failed writing id for %s.' % path_name)
            tty.warn(output)
    os.chmod(path_name, st.st_mode)
    return


def get_filetype(path_name):
    """
    Check the output of the file command for given string.
    """
    bash = which('bash')
    output = bash('-c', 'LC_ALL=C && file -b -h %s' % path_name,
                  output=str, err=str)
    if bash.returncode != 0:
        tty.warn('getting filetype of "%s" failed' % path_name)
        return None
    return output.strip()


def modify_elf_object(path_name, orig_rpath, new_rpath, patchelf_executable):
    """
    Replace RPATH's in given elf object
    """
    st = os.stat(path_name)
    wmode = os.access(path_name, os.W_OK)
    if not wmode:
        os.chmod(path_name, st.st_mode | stat.S_IWUSR)
    if platform.system() == 'Linux':
        new_joined = ':'.join(new_rpath)
        command = which(patchelf_executable)
        output = command('--force-rpath', '--set-rpath', '%s' % new_joined,
                         '%s' % path_name, output=str, cmd=str)
        if command.returncode != 0:
            tty.warn('failed writing rpath for %s.' % path_name)
            tty.warn(output)
    else:
        tty.die('relocation not supported for this platform')
    os.chmod(path_name, st.st_mode)


def needs_binary_relocation(filetype):
    """
    Check whether the given filetype is a binary that may need relocation.
    """
    retval = False
    if "relocatable" in filetype:
        return False
    if platform.system() == 'Darwin':
        return ('Mach-O' in filetype)
    elif platform.system() == 'Linux':
        return ('ELF' in filetype)
    else:
        tty.die("Relocation not implemented for %s" % platform.system())
    return retval


def needs_text_relocation(filetype):
    """
    Check whether the given filetype needs relocation.
    """
    return ("text" in filetype)


def relocate_binary(path_name, old_dir, new_dir, patchelf_executable):
    """
    Change RPATHs in given elf or mach-o file
    """
    if platform.system() == 'Darwin':
        modify_macho_object(path_name, old_dir, new_dir, relative=False)
    elif platform.system() == 'Linux':
        orig_rpaths = get_existing_elf_rpaths(path_name, patchelf_executable)
        new_rpaths = substitute_rpath(orig_rpaths, old_dir, new_dir)
        modify_elf_object(path_name, orig_rpaths, new_rpaths,
                          patchelf_executable)
    else:
        tty.die("Relocation not implemented for %s" % platform.system())


def prelocate_binary(path_name, old_dir, patchelf_executable):
    """
    Change RPATHs in given elf or mach-o file to relative
    """
    if platform.system() == 'Darwin':
        new_dir = ''
        modify_macho_object(path_name, old_dir, new_dir, relative=True)
    elif platform.system() == 'Linux':
        orig_rpaths = get_existing_elf_rpaths(path_name, patchelf_executable)
        new_rpaths = get_relative_rpaths(path_name, old_dir, orig_rpaths)
        modify_elf_object(path_name, orig_rpaths, new_rpaths,
                          patchelf_executable)
    else:
        tty.die("Prelocation not implemented for %s" % platform.system())


def relocate_text(path_name, old_dir, new_dir):
    """
    Replace old path with new path in text files
    """
#    filter_file("r'%s'" % old_dir, "r'%s'" % new_dir, path_name)
    perl = which('perl')
    perl('-p', '-i', '-e', 's|%s|%s|g' % (old_dir, new_dir), path_name)


def substitute_rpath(orig_rpath, topdir, new_root_path):
    """
    Replace
    """
    new_rpaths = []
    for path in orig_rpath:
        new_rpath = path.replace(topdir, new_root_path)
        new_rpaths.append(new_rpath)
    return new_rpaths
