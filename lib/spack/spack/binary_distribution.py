__author__ = "Benedikt Hegner (CERN)"

import os
import platform
import urllib2
from architecture import get_full_system_from_platform
from spack.util.executable import which
import spack.cmd
import spack

def prepare():
    """
    Install patchelf as pre-requisite to the required relocation of binary packages
    """
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    patchelf = spack.repo.get(patchelf_spec)
    patchelf.do_install()

def tarball_name(spec):
    """
    Return the name of the tarfile according to the convention
    <architecture>-<os>-<name>-<dag_hash>.tar.gz
    """
    return "%s-%s-%s-%s.tar.gz" %(get_full_system_from_platform(),spec.name,spec.version,spec.dag_hash())

def download_tarball(package):
    """
    Download binary tarball for given package into stage area
    """
    try:
        download_url = os.environ["SPACK_DOWNLOAD_URL"]
    except KeyError:
        print "Please set the SPACK_DOWNLOAD_URL environment variable for downloading pre-compiled packages!"
        raise KeyError()
    tarball = tarball_name(package.spec)
    remote_tarball = os.path.join(download_url, tarball)
    local_tarball = package.stage.path+"/"+tarball
    # TODO: handle failures
    f = urllib2.urlopen(remote_tarball)
    content = f.read()
    with open(local_tarball, "wb") as local:
        local.write(content)

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
