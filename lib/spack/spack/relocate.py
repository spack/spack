#  "Benedikt Hegner (CERN)"
#  "Patrick Gartung (FNAL)"

import os
import stat
import platform
import re
from commands import getstatusoutput
from spack.util.executable import which

import llnl.util.tty as tty


def get_existing_elf_rpaths(path_name, patchelf_executable):
    """
    Return the RPATHS in given elf file as a list of strings.
    """
    if platform.system() == 'Linux':
        command = '%s --print-rpath %s ' % (patchelf_executable, path_name)
        status, output = getstatusoutput(command)
        if status != 0:
            tty.warn('failed reading rpath for %s.' % path_name)
            return False
        return output.split(':')
    else:
        tty.die('relocation not supported for this platform')
    return retval

def modify_macho_object(path_name, old_dir, new_dir):
    """
    Modify MachO binaries by changing rpaths,and id and dependency lib paths.

    Examines the output of otool -l for these three patterns

          cmd LC_ID_DYLIB
      cmdsize 160
         name /Users/gartung/spack-macdev/opt/spack/darwin-x86_64/clang-7.0.2-apple/tcl-8.6.5-xfeydlhaojmei6iws2rnxndvriym242k/lib/libtcl8.6.dylib (offset 24)

          cmd LC_LOAD_DYLIB
      cmdsize 160
         name /Users/gartung/spack-macdev/opt/spack/darwin-x86_64/clang-7.0.2-apple/zlib-1.2.8-cyvcqvrzlgurne424y55hxvfucvz2354/lib/libz.1.dylib (offset 24)

          cmd LC_RPATH
      cmdsize 128
         path /Users/gartung/spack-macdev/opt/spack/darwin-x86_64/clang-7.0.2-apple/xz-5.2.2-d4ecxpuzf2g3ycz3cnj3xmdj7zdnuqwb/lib (offset 12)
  
    the old install dir in LC_LOAD_DYLIB is replace with the new install dir  using 
        install_name_tool -id newid binary

    the old install dir in LC_LOAD_DYLIB is replaced with the new install dir  using 
        install_name_tool -change old new binary

    the old install dir in LC_RPATH is replaced with the new install dir using
        install_name_tool  -rpath old new binary
   
    """
    command = which('otool')
    output  = command("-l", path_name, output=str, err=str)
    if command.returncode != 0:
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
                idpath=rhs
            if lhs == 'name' and last_cmd == 'LC_LOAD_DYLIB':
                deps.append(rhs)
    id = idpath.replace(old_dir,new_dir)
    nrpaths = []
    for rpath in rpaths:
        nrpath = rpath.replace(old_dir,new_dir)
        nrpaths.append(nrpath)
    ndeps = []
    for dep in deps:
        ndep = dep.replace(old_dir,new_dir)
        ndeps.append(ndep)

    st = os.stat(path_name)
    wmode = os.access(path_name, os.W_OK)
    if not wmode:
        os.chmod(path_name, st.st_mode | stat.S_IWUSR)

    if id :
        command = ("install_name_tool -id  %s  %s" % (id,path_name) )
        status, output = getstatusoutput(command)
        if status != 0:
            tty.warn('failed writing id for %s.' % path_name)
            tty.warn(output)

    for orig, new in zip(deps, ndeps):
        command = ("install_name_tool -change  %s %s %s" % 
                         (orig, new, path_name))
        status, output = getstatusoutput(command)
        if status != 0:
            tty.warn('failed writing dep for %s.' % path_name)
            tty.warn(output)

    for orig, new in zip(rpaths, nrpaths):
        command= ("install_name_tool -rpath %s %s %s" % 
                         (orig,new,path_name) )
        status, output = getstatusoutput(command)
        if status != 0:
            tty.warn('failed writing id for %s.' % path_name)
            tty.warn(output)

    os.chmod(path_name, st.st_mode)
    return



def get_filetype(path_name):
    """
    Check the output of the file command for given string.
    """
    file_command = "LC_ALL=C file -b -h \"%s\"" % path_name
    status, output = getstatusoutput(file_command)
    if status != 0:
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
        command = "%s --force-rpath --set-rpath '%s' '%s'" % \
            (patchelf_executable, new_joined, path_name)
        status, output = getstatusoutput(command)
        if status != 0:
            tty.warn('failed writing rpath for %s.' % path_name)
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
        modify_macho_object(path_name, old_dir, new_dir)
    elif platform.system() == 'Linux':
        orig_rpaths = get_existing_elf_rpaths(path_name, patchelf_executable)
        new_rpaths  = substitute_rpath(orig_rpath, old_dir, new_dir)
        modify_elf_object(path_name, orig_rpaths, new_rpaths, patchelf_executable)
    else:
        tty.die("Relocation not implemented for %s" % platform.system())


def relocate_text(path_name, old_dir, new_dir):
    """
    Replace old path with new path in text files
    """
    os.system("LC_ALL=C sed -i -e \"s#%s#%s#g\" \"%s\""
              % (old_dir, new_dir, path_name))


def substitute_rpath(orig_rpath, topdir, new_root_path):
    """
    Replace
    """
    new_rpaths = []
    for path in orig_rpath:
        new_rpath = path.replace(topdir, new_root_path)
        new_rpaths.append(new_rpath)
    return new_rpaths
