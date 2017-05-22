# "Benedikt Hegner (CERN)"

import os
import platform
import tarfile
import yaml

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

from spack.util.executable import which
import spack.cmd
import spack
from spack.stage import Stage
import spack.fetch_strategy as fs
import spack.relocate


def get_full_system_from_platform():
    import platform
    import re
    system = platform.system()
    if system == "Linux":
        pf = platform.linux_distribution(full_distribution_name=0)[0]
        version = platform.linux_distribution(full_distribution_name=0)[1]
        if pf != 'Ubuntu':
            # For non-Ubuntu major version number is enough
            # to understand compatibility
            version = version.split('.')[0]
    elif system == "Darwin":
        pf = "macos10"
        version = platform.mac_ver()[0].split(".")[1]
    else:
        raise "System %s not supported" % system
    sys_type = pf + version + '-' + platform.machine()
    sys_type = re.sub(r'[^\w-]', '_', sys_type)
    return sys_type.lower()


def prepare():
    """
    Install patchelf as pre-requisite to the
    required relocation of binary packages
    """
    if platform.system() == 'Darwin':
        return
    dir = os.getcwd()
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    if not spack.store.layout.check_installed(patchelf_spec):
        patchelf = spack.repo.get(patchelf_spec)
        patchelf.do_install()
    os.chdir(dir)


def buildinfo_file_name(spec):
    """
    Filename of the binary package meta-data file
    """
    return os.path.join(spec.prefix, ".spack", "binary_distribution")


def read_buildinfo_file(package):
    """
    Read buildinfo file
    """
    filename = buildinfo_file_name(package)
    with open(filename, 'r') as inputfile:
        content = inputfile.read()
        buildinfo = yaml.load(content)
    return buildinfo


def write_buildinfo_file(spec):
    """
    Create a cache file containing information
    required for the relocation
    """
    text_to_relocate = []
    binary_to_relocate = []
    blacklist = (".spack", "man")
    for root, dirs, files in os.walk(spec.prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for filename in files:
            path_name = os.path.join(root, filename)
            filetype = spack.relocate.get_filetype(path_name)
            if spack.relocate.needs_binary_relocation(filetype):
                rel_path_name = os.path.relpath(path_name, spec.prefix)
                binary_to_relocate.append(rel_path_name)
            elif spack.relocate.needs_text_relocation(filetype):
                rel_path_name = os.path.relpath(path_name, spec.prefix)
                text_to_relocate.append(rel_path_name)

    # Create buildinfo data and write it to disk
    buildinfo = {}
    buildinfo['buildpath'] = spack.store.layout.root
    buildinfo['relocate_textfiles'] = text_to_relocate
    buildinfo['relocate_binaries'] = binary_to_relocate
    filename = buildinfo_file_name(spec)
    with open(filename, 'w') as outfile:
        outfile.write(yaml.dump(buildinfo, default_flow_style=True))


def tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>/
    """
    return "%s/%s/%s" % (get_full_system_from_platform(),
                         str(spec.compiler).replace("@", "-"),
                         spec.name)


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash>.tar.gz
    """
    return "%s-%s-%s-%s%s" % (get_full_system_from_platform(),
                            spec.name,
                            spec.version,
                            spec.dag_hash(),
                            ext)


def tarball_path_name(spec, ext):
    """
    Return the full path+name for a given spec according to the convention
    <tarball_directory_name>/<tarball_name>
    """
    return os.path.join(tarball_directory_name(spec),
                        tarball_name(spec, ext))


def build_tarball(spec, outdir, force=False, key=None):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    tarfile_dir = os.path.join(outdir, tarball_directory_name(spec))
    tarfile_path = os.path.join(outdir, tarball_path_name(spec, '.tar.gz'))
    if force:
        os.remove(tarfile)
    else:
        tty.warn("file exists, use -f to force overwrite: %s" % tarfile)
        return
    if not os.path.exists(tarfile_dir):
        mkdirp(tarfile_dir)

    dirname = os.path.dirname(spec.prefix)
    basename = os.path.basename(spec.prefix)
    spec_file = os.path.join(spec.prefix, ".spack", "spec.yaml")

    # create info for later relocation and create tar
    with tarfile.open(tarfile_path, 'w:gz') as tar:
        write_buildinfo_file(spec)

        tar.add(basename)

        spec_info = tar.gettarinfo(spec_file, arcname='.spack/spec.yaml')
        tar.addfile(spec_info)

    # Sign the packages.
    #spack gpg sign [--key key] tarfile_path
    #spack gpg sign [--key key] spec_file

    spackfile_path = os.path.join(outdir, tarball_path_name(spec, '.spack'))
    with tarfile.open(spackfile_path, 'w') as tar:
        tar.add(tarfile_path)
        #tar.add(tarfile_path + '.asc')

        spec_info = tar.gettarinfo(spec_file, arcname='spec.yaml')
        tar.addfile(spec_info)

        #tar.add(spec_file + '.asc')

    tty.msg(tarfile_path)


def download_tarball(package):
    """
    Download binary tarball for given package into stage area
    Return True if successful
    """
    mirrors = spack.config.get_config('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of pre-compiled packages.")
    tarball = tarball_path_name(package.spec, '.spack')
    for key in mirrors:
        url = mirrors[key] + "/" + tarball
        # print url
        # stage the tarball into standard place
        stage = Stage(url, name=package.stage.path)
        try:
            stage.fetch()
            return True
        except fs.FetchError:
            next
    return False


def extract_tarball(package):
    """
    extract binary tarball for given package into install area
    """
    tarball = tarball_name(package.spec)
    local_tarball = package.stage.path + "/" + tarball
    mkdirp(package.prefix)
    tarfile_name = tarball_path_name(spec, '.tar.gz')
    tarfile_path = os.path.join(package.prefix, tarfile_name)
    with tarfile.open(local_tarball, 'r') as tar:
        tar.extract('spec.yaml', package.prefix)
        tar.extract('spec.yaml.asc', package.prefix)

        # spack gpg verify os.path.join(package.prefix, 'spec.yaml')

        tar.extract(tarfile_name, package.prefix)
        tar.extract(tarfile_name + '.asc', package.prefix)

        # spack gpg verify tarfile_path

    with tarfile.open(tarfile_path, 'r') as tar:
        tar.extractall(path=package.prefix)

    #os.remove(tarfile_path)
    #os.remove(tarfile_path + '.asc')


def relocate_package(package):
    """
    Relocate the given package
    """
    buildinfo = read_buildinfo_file(package)
    new_path = spack.store.layout.root
    old_path = buildinfo['buildpath']
    if old_path == new_path:
        return True  # No need to relocate

    tty.warn("Using experimental feature for relocating package from",
             "%s to %s." % (old_path, new_path))

    # as we may need patchelf, find out where it is
    patchelf_executable = ''
    if platform.system() != 'Darwin':
        patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
        patchelf = spack.repo.get(patchelf_spec)
        patchelf_executable = os.path.join(patchelf.prefix, "bin", "patchelf")

    # now do the actual relocation
    for filename in buildinfo['relocate_binaries']:
        path_name = os.path.join(package.prefix, filename)
        spack.relocate.relocate_binary(path_name,
                                       old_path,
                                       new_path,
                                       patchelf_executable)
    for filename in buildinfo['relocate_textfiles']:
        path_name = os.path.join(package.prefix, filename)
        spack.relocate.relocate_text(path_name, old_path, new_path)
