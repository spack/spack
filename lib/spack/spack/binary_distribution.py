__author__ = "Benedikt Hegner (CERN)"

import platform
from architecture import get_full_system_from_platform

def tarball_name(spec):
    """
    Return the name of the tarfile according to the convention
    <architecture>-<os>-<name>-<dag_hash>.tar.gz
    """
    return "%s-%s-%s.tar.gz" %(get_full_system_from_platform(),spec.name,spec.dag_hash())
