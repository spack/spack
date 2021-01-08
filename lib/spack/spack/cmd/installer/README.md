Use the contents of this directory and the spack 'make-installer' command to
create a Windows installer. Installers are not supported on other platforms.

The installer must be created on Windows and requires the following:
* Spack (https://github.com/spack/spack)
* Python (https://www.python.org/downloads/)
* CMake (https://cmake.org/download/)
* Wix (https://wixtoolset.org/releases/)

Note: Spack and Python may be installed using the Spack installer. This has the
advantage of setting up the PATH automatically.

To create the installer, run:

spack make-installer -v <spack_version> <output directory>

e.g. spack make-installer -v 0.16.0 tmp

This will download spack from https://github.com/spack/spack/releases/download/v0.16.0
and create the installer in 'tmp'.

The output directory may be an absolute path or relative to the current
directory. It *must* already exist.

Alternatively, specify a local spack directory:

spack make-installer -s <spack directory> <output directory>

e.g. spack make-installer -s spack-0.16.0 tmp

The spack directory may be an absolute path or relative to the current
directory. The entire contents of the specified directory will be included
in the installed (e.g. .git files or local changes).
