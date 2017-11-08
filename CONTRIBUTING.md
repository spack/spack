Package Contribution Guidelines
===============================

If you are submitting a new Spack package, please observe the
following standards:

1. Code must be [PEP-8 compliant](http://spack.readthedocs.io/en/latest/contribution_guide.html?highlight=pep-8#flake8-tests)

2. At least one numeric (checksummable) version must be supplied.  If
   this package does not yet have any official releases, create an
   unofficial checksummable Spack-only release using something like:
   ```
   version('1.9.5.1.1',
        git='https://github.com/jswhit/pyproj.git',
        commit='0be612cc9f972e38b50a90c946a9b353e2ab140f')
   ```

2. All explicit versions in `depends_on()` statements must be for
   checksummable versions.  If you need to depend on unreleased
   versions of other packages, add unofficial releases to them too.

3. If the package builds binaries... once you've built the package on
   your machine, please check the binaries it produces with
   [ldd](http://man7.org/linux/man-pages/man1/ldd.1.html) to find any
   hidden dependencies not explicitly listed with `depends_on()` in
   your `package.py`.  If you find any hidden dependencies, please
   make them explicit.

4. Does your package build static libraries?  If so, make sure there
   is [+pic](https://github.com/LLNL/spack/pull/2375) variant, turned
   on by default when building static libraries.

5. Does your package optionally build shared or static libraries?  If
   so, implemented `+shared` and `+static` variants [as
   appropriate](https://github.com/LLNL/spack/issues/2380).

6. Does the build download stuff during the `install()` phase?  If so,
   please re-work things so it does not, because Spack needs to work
   on clusters disconnected from the Internet.  Usually this happens
   because the upstream authors wanted to auto-install dependencies.
   Usually you can disable it by supplying command line options to the
   build that tell it where those dependencies have already been
   built.  You might also find [Spack
   Resources](http://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=resources)
   to be useful here.

7. Have you applied appropriate dependency types to your
   `depends_on()` declarations?
   a) Common `build` dependencies are `cmake`, `autotools`, `doxygen`.
   b) Python package dependencies are usually of type `nolink`.

8. Is your package built with CMake?  If so, subclass from
   [CMakePackage](http://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=cmakepackage#cmakepackage).

9. Is there a copyright notice at the top?  Copyright must be assigned
   to the Spack project.  You may copy the copyright notice from
   another Spack package.


