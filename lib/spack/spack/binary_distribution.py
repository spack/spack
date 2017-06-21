# "Benedikt Hegner (CERN)"

import os
import platform
import tarfile
import yaml
import shutil

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, join_path

import spack.cmd
import spack
from spack.stage import Stage
import spack.fetch_strategy as fs
import spack.relocate
from contextlib import closing
import platform
import re


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
            elif spack.relocate.needs_text_relocation(path_name, spec.prefix,
                                                      filetype):
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
    return "%s/%s/%s" % (spack.architecture.sys_type(),
                         str(spec.compiler).replace("@", "-"),
                         spec.name)


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    return "%s-%s-%s-%s%s" % (spack.architecture.sys_type(),
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
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_dir = join_path(outdir, tarball_directory_name(spec))
    tarfile_path = join_path(tarfile_dir, tarfile_name)
    mkdirp(tarfile_dir)
    spackfile_path = os.path.join(outdir, tarball_path_name(spec, '.spack'))
    if os.path.exists(spackfile_path):
        if force:
            os.remove(spackfile_path)
        else:
            tty.warn("file exists, use -f to force overwrite: %s" %
                     spackfile_path)
            return

    # need to copy the spec file so the build cache can be downloaded
    # without concretizing with the current spack packages
    # and preferences
    spec_file = join_path(spec.prefix, ".spack", "spec.yaml")
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = join_path(tarfile_dir, specfile_name)
    if os.path.exists(specfile_path):
        if force:
            os.remove(specfile_path)
        else:
            tty.warn("file exists, use -f to force overwrite: %s" %
                     specfile_path)
            return
    shutil.copyfile(spec_file,specfile_path)

    # create info for later relocation and create tar
    write_buildinfo_file(spec)
    with closing(tarfile.open(tarfile_path, 'w:gz')) as tar:
        tar.add(name='%s' % spec.prefix, arcname='%s' %
                os.path.basename(spec.prefix))

    # Sign the packages.
    # spack gpg sign [--key key] tarfile_path
    # spack gpg sign [--key key] tarfile_path + '/spec.yaml'

    # temporary to test adding and extracting .asc files
    path1 = '%s.asc' % tarfile_path
    with open(path1, 'a'):
        os.utime(path1, None)
    path2 = '%s.asc' % specfile_path
    with open(path2, 'a'):
        os.utime(path2, None)
    # temporary to test adding and extracting .asc files

    with closing(tarfile.open(spackfile_path, 'w')) as tar:
        tar.add(name='%s' % tarfile_path, arcname='%s' % tarfile_name)
        tar.add(name='%s' % specfile_path, arcname='%s' % specfile_name)
        tar.add(name='%s.asc' % tarfile_path, arcname='%s.asc' % tarfile_name)
        tar.add(name='%s.asc' % specfile_path, arcname='%s.asc' % specfile_name)
        os.remove(tarfile_path)

    os.remove(path1)
    os.remove(path2)


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
    tarball = tarball_name(package.spec, '.spack')
    local_tarball = package.stage.path + "/" + tarball
    mkdirp(package.prefix)
    tarfile_name = tarball_name(package.spec, '.tar.gz')
    tarfile_path = os.path.join(package.stage.path, tarfile_name)
    specfile_name = tarball_name(package.spec, '.tar.gz')
    specfile_path = os.path.join(package.stage.path, tarfile_name)
    with closing(tarfile.open(local_tarball, 'r')) as tar:
        tar.extract(specfile_name, package.stage.path)
        tar.extract(specfile_name + '.asc', package.stage.path)

        # spack gpg verify os.path.join(package.prefix, 'spec.yaml')

        tar.extract(tarfile_name, package.stage.path)
        tar.extract(tarfile_name + '.asc', package.stage.path)

        # spack gpg verify tarfile_path

    with closing(tarfile.open(tarfile_path, 'r')) as tar:
        tar.extractall(path=os.path.dirname(package.prefix))

    os.remove(tarfile_path)
    os.remove(tarfile_path + '.asc')
    os.remove(specfile_path)
    os.remove(specfile_path + '.asc')


def relocate_package(package):
    """
    Relocate the given package
    """
    buildinfo = read_buildinfo_file(package)
    new_path = spack.store.layout.root
    old_path = buildinfo['buildpath']
    if old_path == new_path:
        return True  # No need to relocate

    tty.msg("Relocating package from",
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
        gcc_prefix=re.sub('/bin/.*$','',package.compiler.cc)
        spack.relocate.relocate_binary(path_name,
                                       old_path,
                                       new_path,
                                       patchelf_executable,
                                       gcc_prefix)

    for filename in buildinfo['relocate_textfiles']:
        path_name = os.path.join(package.prefix, filename)
        spack.relocate.relocate_text(path_name, old_path, new_path)
