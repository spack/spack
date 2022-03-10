# Test data for unparser

These are test packages for testing Spack's unparser. They are used to ensure that the
canonical unparser used for Spack's package hash remains consistent across Python
versions.

All of these were copied from mainline Spack packages, and they have been renamed with
`.txt` suffixes so that they're not considered proper source files by the various
checkers used in Spack CI.

These packages were chosen for various reasons, but mainly because:

1. They're some of the more complex packages in Spack, and they exercise more unparser
   features than other packages.

2. Each of these packages has some interesting feature that was hard to unparse
   consistently across Python versions.  See docstrings in packages for details.
