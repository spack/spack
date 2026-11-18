# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.dependency as dep
import spack.deptypes as dt
import spack.spec


def test_intern_dependency():
    """Test that identical unpatched dependencies are interned."""
    s1 = spack.spec.Spec("zlib@1.2.11")
    s2 = spack.spec.Spec("zlib@1.2.11")
    
    # Create two equivalent Dependency objects
    d1 = dep.Dependency(s1, dt.LINK | dt.BUILD)
    d2 = dep.Dependency(s2, dt.LINK | dt.BUILD)
    
    # Check that intern_dependency returns the same instance
    interned1 = dep.intern_dependency(d1)
    interned2 = dep.intern_dependency(d2)
    
    assert interned1 is interned2
    
    # Create a dependency with a different flag
    d3 = dep.Dependency(s1, dt.RUN)
    interned3 = dep.intern_dependency(d3)
    
    assert interned3 is not interned1


def test_dependency_repr():
    """Test the string representation of Dependency objects."""
    s = spack.spec.Spec("hdf5+mpi")
    d = dep.Dependency(s, dt.BUILD | dt.LINK)
    rep = repr(d)
    assert "Dependency: " in rep
    assert "hdf5+mpi" in rep
    assert "bl" in rep
    
    # Test representation with patches
    d_patch = dep.Dependency(s, dt.BUILD)
    d_patch.patches = {spack.spec.Spec(): ["mock_patch"]}
    rep_patch = repr(d_patch)
    assert "mock_patch" in rep_patch
    assert "b " in rep_patch

def test_dependency_name():
    """Test the name property of a Dependency object."""
    s = spack.spec.Spec("python@3.10")
    d = dep.Dependency(s)
    assert d.name == "python"

