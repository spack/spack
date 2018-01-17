##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import os
import platform
import re
import spack
import spack.cmd
from spack.util.executable import Executable
from llnl.util.filesystem import filter_file
import llnl.util.tty as tty


def get_patchelf():
    """
    Builds and installs spack patchelf package on linux platforms
    using the first concretized spec.
    Returns the full patchelf binary path.
    """
    # as we may need patchelf, find out where it is
    if platform.system() == 'Darwin':
        return None
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    patchelf = spack.repo.get(patchelf_spec)
    if not patchelf.installed:
        patchelf.do_install()
    patchelf_executable = os.path.join(patchelf.prefix.bin, "patchelf")
    return patchelf_executable


def get_existing_elf_rpaths(path_name):
    """
    Return the RPATHS returned by patchelf --print-rpath path_name
    as a list of strings.
    """
    if platform.system() == 'Linux':
        command = Executable(get_patchelf())
        output = command('--print-rpath', '%s' %
                         path_name, output=str, err=str)
        return output.rstrip('\n').split(':')
    else:
        tty.die('relocation not supported for this platform')
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
    return rpaths, deps, idpath


def macho_make_paths_relative(path_name, old_dir, rpaths, deps, idpath):
    """
    Replace old_dir with relative path from dirname(path_name)
    in rpaths and deps; idpaths are replaced with @rpath/basebane(path_name);
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
    if new_idpath:
        install_name_tool('-id', new_idpath, str(cur_path),
                          output=str, err=str)

    for orig, new in zip(deps, new_deps):
        install_name_tool('-change', orig, new, str(cur_path))

    for orig, new in zip(rpaths, new_rpaths):
        install_name_tool('-rpath', orig, new, str(cur_path))
    return


def get_filetype(path_name):
    """
    Return the output of file path_name as a string to identify file type.
    """
    file = Executable('file')
    file.add_default_env('LC_ALL', 'C')
    output = file('-b', '-h', '%s' % path_name,
                  output=str, err=str)
    return output.strip()


def modify_elf_object(path_name, orig_rpath, new_rpath):
    """
    Replace orig_rpath with new_rpath in RPATH of elf object path_name
    """
    if platform.system() == 'Linux':
        new_joined = ':'.join(new_rpath)
        patchelf = Executable(get_patchelf())
        patchelf('--force-rpath', '--set-rpath', '%s' % new_joined,
                 '%s' % path_name, output=str, cmd=str)
    else:
        tty.die('relocation not supported for this platform')


def needs_binary_relocation(filetype, os_id=None):
    """
    Check whether the given filetype is a binary that may need relocation.
    """
    retval = False
    if "relocatable" in filetype:
        return False
    if "link to" in filetype:
        return False
    if os_id == 'Darwin':
        return ("Mach-O" in filetype)
    elif os_id == 'Linux':
        return ("ELF" in filetype)
    else:
        tty.die("Relocation not implemented for %s" % os_id)
    return retval


def needs_text_relocation(filetype):
    """
    Check whether the given filetype is text that may need relocation.
    """
    if "link to" in filetype:
        return False
    return ("text" in filetype)


def relocate_binary(path_names, old_dir, new_dir):
    """
    Change old_dir to new_dir in RPATHs of elf or mach-o files
    """
    if platform.system() == 'Darwin':
        for path_name in path_names:
            rpaths, deps, idpath = macho_get_paths(path_name)
            new_rpaths, new_deps, new_idpath = macho_replace_paths(old_dir,
                                                                   new_dir,
                                                                   rpaths,
                                                                   deps,
                                                                   idpath)
            modify_macho_object(path_name,
                                rpaths, deps, idpath,
                                new_rpaths, new_deps, new_idpath)
    elif platform.system() == 'Linux':
        for path_name in path_names:
            orig_rpaths = get_existing_elf_rpaths(path_name)
            new_rpaths = substitute_rpath(orig_rpaths, old_dir, new_dir)
            modify_elf_object(path_name, orig_rpaths, new_rpaths)
    else:
        tty.die("Relocation not implemented for %s" % platform.system())


def make_binary_relative(cur_path_names, orig_path_names, old_dir):
    """
    Make RPATHs relative to old_dir in given elf or mach-o files
    """
    if platform.system() == 'Darwin':
        for cur_path, orig_path in zip(cur_path_names, orig_path_names):
            rpaths, deps, idpath = macho_get_paths(cur_path)
            (new_rpaths,
             new_deps,
             new_idpath) = macho_make_paths_relative(orig_path, old_dir,
                                                     rpaths, deps, idpath)
            modify_macho_object(cur_path,
                                rpaths, deps, idpath,
                                new_rpaths, new_deps, new_idpath)
    elif platform.system() == 'Linux':
        for cur_path, orig_path in zip(cur_path_names, orig_path_names):
            orig_rpaths = get_existing_elf_rpaths(cur_path)
            new_rpaths = get_relative_rpaths(orig_path, old_dir,
                                             orig_rpaths)
            modify_elf_object(cur_path, orig_rpaths, new_rpaths)
    else:
        tty.die("Prelocation not implemented for %s" % platform.system())


def relocate_text(path_names, old_dir, new_dir):
    """
    Replace old path with new path in text file path_name
    """
    filter_file('%s' % old_dir, '%s' % new_dir,
                *path_names, backup=False)


def substitute_rpath(orig_rpath, topdir, new_root_path):
    """
    Replace topdir with new_root_path RPATH list orig_rpath
    """
    new_rpaths = []
    for path in orig_rpath:
        new_rpath = path.replace(topdir, new_root_path)
        new_rpaths.append(new_rpath)
    return new_rpaths
