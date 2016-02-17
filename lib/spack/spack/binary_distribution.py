__author__ = "Benedikt Hegner (CERN)"

import platform

def tarball_name(spec):
    """
    Return the name of the tarfile according to the convention
    <architecture>-<os>-<name>-<dag_hash>.tar.gz
    """
    return "%s-%s-%s-%s.tar.gz" %(architecture(),os(),spec.name,spec.dag_hash())

def os():
    """
    Return the Operating System and its major version like
    "macos109", "ubuntu14", ...
    """
    system = platform.system()
    if system == "Linux":
        pf = platform.linux_distribution(full_distribution_name=0)[0]
        version = platform.linux_distribution(full_distribution_name=0)[1].split(".")[0]
        # SLC6 misidentifies itself has RedHat
        if pf == "redhat":
            if "CERN" in platform.linux_distribution()[0]:
                pf = "slc"
    elif system == "Darwin":
        pf = "macos10"
        version = platform.mac_ver()[0].split(".")[1]
    elif system == "Windows":
        pass
    else:
        raise "System %s not supported" %system

    return (pf+version).lower()

def architecture():
    """
    return architecture as defined by platform.machine()
    """
    return platform.machine()
