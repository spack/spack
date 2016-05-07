__author__ = "Benedikt Hegner (CERN)"

import llnl.util.tty as tty

import os
import platform
import urllib2
from architecture import get_full_system_from_platform
from spack.util.executable import which
import spack.cmd
import spack
from spack.stage import Stage
import spack.fetch_strategy as fs

def prepare():
    """
    Install patchelf as pre-requisite to the required relocation of binary packages
    """
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    patchelf = spack.repo.get(patchelf_spec)
    patchelf.do_install()

def build_info_file(spec):
    """
    Filename of the binary package meta-data file
    """
    return os.path.join(spec.prefix,".spack","binary_distribution")

def tarball_name(spec):
    """
    Return the name of the tarfile according to the convention
    <architecture>-<os>-<name>-<dag_hash>.tar.gz
    """
    return "%s-%s-%s-%s.tar.gz" %(get_full_system_from_platform(),spec.name,spec.version,spec.dag_hash())

def build_tarball(spec, outdir, force=False):
    """
    Build a tarball from given spec
    """
    tarfile = os.path.join(outdir, tarball_name(spec))
    if os.path.exists(tarfile):
        if force:
            os.remove(tarfile)
        else:
            tty.die("file exists, use -f to force overwrite: %s"%tarfile)

    tar = which('tar', required=True)
    dirname = os.path.dirname(spec.prefix)
    basename = os.path.basename(spec.prefix)
    
    # handle meta-data
    cp = which("cp", required = True)
    spec_file = os.path.join(spec.prefix,".spack","spec.yaml")
    target_spec_file = tarfile+".yaml"
    cp(spec_file,target_spec_file)  
    
    with open(build_info_file(spec),"w") as package_file:
        package_file.write(spack.install_path)
    
    tar("--directory=%s" %dirname, "-cf", tarfile, basename)
    tty.msg(tarfile)


def download_tarball(package):
    """
    Download binary tarball for given package into stage area
    Return True if successful 
    """
    if len(spack.config.get_config('mirrors')) == 0:
        tty.die("Please add a spack mirror to allow download of pre-compiled packages.")

    # stage the tarball into standard place
    tarball = tarball_name(package.spec)
    stage = Stage(tarball,name=package.stage.path,mirror_path=tarball)
    try: 
      stage.fetch(mirror_only = True)
      return True
    except fs.FetchError:
      return False

def extract_tarball(package):
    """
    extract binary tarball for given package into install area
    """
    tarball = tarball_name(package.spec)
    tar = which("tar")
    local_tarball = package.stage.path+"/"+tarball
    tar("--strip-components=1","-C%s"%package.prefix,"-xf",local_tarball)

def relocate(package):
    # get location of previously installed patchelf
    with open(build_info_file(package.spec),"r") as package_file:
        build_path = package_file.read()
    if build_path != spack.install_path:
        tty.warn("Using incomplete feature for relocating binary package from %s to %s." %(build_path, spack.install_path))
        patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
        patchelf = spack.repo.get(patchelf_spec)
        patchelf_executable=os.path.join(patchelf.prefix,"bin","patchelf")
        rpath = ":".join(package.rpath)
        os.chdir(package.prefix)
        for root, dirs, files in os.walk(package.prefix):
            for file in files:
                if file.endswith("so"):
                    fullname = os.path.join(root, file)
                    os.system("%s --set-rpath %s %s"%(patchelf_executable,rpath,fullname) )
