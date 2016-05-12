# "Benedikt Hegner (CERN)"

import os
import re
import stat
import platform
from commands import getstatusoutput

import llnl.util.tty as tty
from architecture import get_full_system_from_platform
from spack.util.executable import which
import spack.cmd
import spack
from spack.stage import Stage
import spack.fetch_strategy as fs


def prepare():
    """
    Install patchelf as pre-requisite to the
    required relocation of binary packages
    """
    if platform.system() == 'Darwin':
        return
    dir = os.getcwd()
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    if not spack.install_layout.check_installed(patchelf_spec):
        patchelf = spack.repo.get(patchelf_spec)
        patchelf.do_install()
    os.chdir(dir)


def build_info_file(spec):
    """
    Filename of the binary package meta-data file
    """
    return os.path.join(spec.prefix, ".spack", "binary_distribution")


def tarball_name(spec):
    """
    Return the name of the tarfile according to the convention
    <architecture>-<os>-<name>-<dag_hash>.tar.gz
    """
    return "%s-%s-%s-%s.tar.gz" % (get_full_system_from_platform(),
                                   spec.name,
                                   spec.version,
                                   spec.dag_hash())


def build_tarball(spec, outdir, force=False):
    """
    Build a tarball from given spec
    """
    tarfile = os.path.join(outdir, tarball_name(spec))
    if os.path.exists(tarfile):
        if force:
            os.remove(tarfile)
        else:
            tty.die("file exists, use -f to force overwrite: %s" % tarfile)

    tar = which('tar', required=True)
    dirname = os.path.dirname(spec.prefix)
    basename = os.path.basename(spec.prefix)

    # handle meta-data
    cp = which("cp", required=True)
    spec_file = os.path.join(spec.prefix, ".spack", "spec.yaml")
    target_spec_file = tarfile + ".yaml"
    cp(spec_file, target_spec_file)

    with open(build_info_file(spec), "w") as package_file:
        package_file.write(spack.install_path)

    tar("--directory=%s" % dirname, "-czf", tarfile, basename)
    tty.msg(tarfile)


def download_tarball(package):
    """
    Download binary tarball for given package into stage area
    Return True if successful
    """
    if len(spack.config.get_config('mirrors')) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of pre-compiled packages.")

    # stage the tarball into standard place
    tarball = tarball_name(package.spec)
    stage = Stage(tarball, name=package.stage.path, mirror_path=tarball)
    try:
        stage.fetch(mirror_only=True)
        return True
    except fs.FetchError:
        return False


def extract_tarball(package):
    """
    extract binary tarball for given package into install area
    """
    tarball = tarball_name(package.spec)
    tar = which("tar")
    local_tarball = package.stage.path + "/" + tarball
    tar("--strip-components=1",
        "-C%s" % package.prefix,
        "-xf",
        local_tarball)


def get_filetype(path_name):
    """
    check the output of the file command for given string
    """
    file_command = "LC_ALL=C file -b -h \"%s\"" % path_name
    status, output = getstatusoutput(file_command)

    if status != 0:
        tty.warn('getting filetype of "%s" failed' % path_name)
        return None
    return output.strip()


def needs_binary_relocation(filetype):
    """
    check whether the given filetype is a binary that may need relocation
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
    check whether the given filetype needs relocation.
    """
    return ("text" in filetype)


def relocate_binary(path_name, topdir, new_root_dir, patchelf_executable):
    """
    Change RPATHs in given file
    """
    orig_rpath = get_existing_rpath(path_name, patchelf_executable)
    new_rpath  = substitute_rpath(orig_rpath, topdir, new_root_dir)
    modify_rpath(path_name, orig_rpath, new_rpath, patchelf_executable)


def get_existing_rpath(path_name, patchelf_executable):
    if platform.system() == 'Darwin':
        command = which('otool')
        output  = command("-l", path_name, output=str, err=str)
        if command.returncode != 0:
            tty.warn('failed reading rpath for %s.' % path_name)
            return False
        last_cmd = None
        path = ()
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


def substitute_rpath(orig_rpath, topdir, new_root_path):
    head0, comp = os.path.split(new_root_path)
    head, arch = os.path.split(head0)
    arch_comp = os.path.join(arch, comp)
    new_rpath = []
    for path in orig_rpath:
        new_path = re.sub('.*/' + arch_comp, new_root_path, path)
        new_rpath.append(new_path)
    return new_rpath


def modify_rpath(path_name, orig_rpath, new_rpath, patchelf_executable):
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


def relocate_text(path_name, original_path, new_path):
    """
    Replace old path with new path in text files
    """
    os.system("LC_ALL=C sed -i -e \"s#%s#%s#g\" \"%s\""
              % (original_path, new_path, path_name))


def relocate(package):
    """
    Relocate a package by fixing RPATHS, #! and other files that have
    the path hardcoded.
    """
    with open(build_info_file(package.spec), "r") as package_file:
        original_path = package_file.read()
    if original_path == spack.install_path:
        return True  # nothing to do
    new_path = spack.install_path
    tty.warn("Using experimental feature for relocating package from %s to %s."
             % (original_path, new_path))

    # as we need patchelf, find out where it is
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    patchelf = spack.repo.get(patchelf_spec)
    patchelf_executable = os.path.join(patchelf.prefix, "bin", "patchelf")

    # now do the actual relocation
    os.chdir(package.prefix)

    blacklist = (".spack", "man")
    for root, dirs, files in os.walk(package.prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for filename in files:
            path_name = os.path.join(root, filename)
            filetype = get_filetype(path_name)
            if needs_binary_relocation(filetype):
                relocate_binary(path_name,
                                original_path,
                                new_path,
                                patchelf_executable)
            elif needs_text_relocation(filetype):
                relocate_text(path_name, original_path, new_path)
