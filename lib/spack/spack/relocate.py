#  "Benedikt Hegner (CERN)"

import os
import stat
import platform
import re
from commands import getstatusoutput
from spack.util.executable import which

import llnl.util.tty as tty


def get_existing_rpath(path_name, patchelf_executable):
    """
    Return the RPATHS in given file as a list of strings.
    """
    if platform.system() == 'Darwin':
        command = which('otool')
        output  = command("-l", path_name, output=str, err=str)
        if command.returncode != 0:
            tty.warn('failed reading rpath for %s.' % path_name)
            return False
        last_cmd = None
        path = set()
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
                    path.add(rhs)
        return path
    elif platform.system() == 'Linux':
        command = '%s --print-rpath %s ' % (patchelf_executable, path_name)
        status, output = getstatusoutput(command)
        if status != 0:
            tty.warn('failed reading rpath for %s.' % path_name)
            return False
        return output.split(':')
    else:
        tty.die('relocation not supported for this platform')
    return retval

def change_dylib(path_name, rpaths):
    """
    Return the RPATHS in given file as a list of strings.
    """
    command = which('otool')
    output  = command("-l", path_name, output=str, err=str)
    if command.returncode != 0:
        tty.warn('failed reading rpath for %s.' % path_name)
        return False
    last_cmd = None
    path = ''
    deps = set()
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
            if lhs == 'path' and last_cmd == 'LC_ID_DYLIB':
                path=rhs
            if lhs == 'path' and last_cmd == 'LC_LOAD_DYLIB':
                deps.append(rhs)
    id = None
    ndeps = set()
    for rpath in rpaths:
        if re.match(rpath,path):
            id = '@rpath/' + re.split(rpath,path)[1]
        for dep in deps:
            if re.match(rpath,dep):
                ndep = '@rpath/' + re.split(rpath,dep)[1]
                ndeps.append(ndep)

    icommand = which("install_name_tool")

    if id :
        output = icommand("-id ", "%s" % id,
                     "%s" % path_name,
                     output=str,
                     err=str)
        if icommand.returncode != 0:
            tty.warn('failed writing id for %s.' % path_name)

    for orig, new in zip(deps, ndeps):
        output = icommand("-change ", "%s" % orig,
                         "%s" % new,
                         "%s" % path_name,
                         output=str,
                         err=str)
        if icommand.returncode != 0:
            tty.warn('failed writing dep for %s.' % path_name)
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


def modify_rpath(path_name, orig_rpath, new_rpath, patchelf_executable):
    """
    Replace RPATH in given binary
    """
    st = os.stat(path_name)
    wmode = os.access(path_name, os.W_OK)
    if not wmode:
        os.chmod(path_name, st.st_mode | stat.S_IWUSR)
    if platform.system() == 'Darwin':
        for orig, new in zip(orig_rpath, new_rpath):
            command = which("install_name_tool")
            output = command("-rpath", "%s" % orig,
                             "%s" % new,
                             "%s" % path_name,
                             output=str,
                             err=str)
            if command.returncode != 0:
                tty.warn('failed writing rpath for %s.' % path_name)
        change_dylib(path_name,orig_rpath)
    elif platform.system() == 'Linux':
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
    Change RPATHs in given file
    """
    orig_rpath = get_existing_rpath(path_name, patchelf_executable)
    new_rpath  = substitute_rpath(orig_rpath, old_dir, new_dir)
    modify_rpath(path_name, orig_rpath, new_rpath, patchelf_executable)


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
