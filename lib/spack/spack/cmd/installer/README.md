Use the contents of this directory and the spack 'make-installer' command to
create a Windows installer. Installers are not supported on other platforms.

The installer must be created on Windows and requires the following:
* Spack (https://github.com/spack/spack)
* Python (https://www.python.org/downloads/)
* CMake (https://cmake.org/download/)
* Wix (https://wixtoolset.org/releases/)

Note: Spack and Python may be installed using the Spack installer. This has the
advantage of setting up the PATH automatically.

To create the installer, first copy the spack_cmd executable and scripts directory
to your top-level directory. Then, after launching spack_cmd (this may require you
to Run as Administrator), run:

spack make-installer -v <spack_version> <output directory>

e.g. ``spack make-installer -v 0.16.0 tmp``

This will download spack from https://github.com/spack/spack/releases/download/v0.16.0
and create the installer in 'tmp'.

The output directory may be an absolute path or relative to the current
directory. It *must* already exist.

Alternatively, specify a local spack directory:

spack make-installer -s <spack directory> <output directory>

e.g. ``spack make-installer -s spack-0.16.0 tmp``

The spack directory may be an absolute path or relative to the current
directory. The entire contents of the specified directory will be included
in the installed (e.g. .git files or local changes). 

Regardless of the method you use, you can obtain the spack environment by entering
the output directory and running the Spack.msi installer package.

To get spack running on Windows, first run the following command:

``spack compiler find``

This creates a .spack directory in our home directory, along with a windows subdirectory
containing a compilers.yaml file. In all likelihood, there is only one compiler listed and
it is some version of Microsoft Visual Studio.

We need to provide the config.yaml and packages.yaml configurations by ourselves. The
config file is the simpler of the two to set up. We simply need the following lines:

```
config:
  locks: false
  install_tree:
    root: $spack\opt\spack
    projections:
      all: '${ARCHITECTURE}\${COMPILERNAME}-${COMPILERVER}\${PACKAGE}-${VERSION}-${HASH}'
```

Notice that the projections stanza is identical to the one in the default config.yaml
provided with the spack checkout (albeit with backslashes instead of forward ones).
Also importantly, it is important that all indents in .yaml files are done with
spaces and not indents (i.e. tabs), so take care when editing one by hand.

For the packages.yaml file, we need to direct spack towards both our CMake
installation and towards Ninja. We know we have CMake from our previous steps,
but the Ninja install we want will need to be installed alongside Microsoft VS.

To see if your installation of Visual Studio has Ninja, you can run the Visual Studio
Installer. Select "Modify" next to your Visual Studio version, and look at the
"Installation details" pane. If the install does not have the subheader
"Desktop development with C++", download that workload. In particular, make sure that
the download includes "C++ CMake tools for Windows", as that will have the Ninja
installation for packages.yaml.

Your packages.yaml file will look something like this, with possibly slight variants
in the paths to CMake and Ninja:

```
packages:
  cmake:
    externals:
    - spec: cmake@3.20.1
      prefix: 'c:\Program Files\CMake'
    buildable: False
  ninja:
    externals:
    - spec: ninja@1.8.2
      prefix: 'c:\Program Files (x86)\Microsoft Visual Studio
\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja'
    buildable: False
```	

It is also entirely possible to use the CMake that comes with the Visual Studio
install. We use the one installed externally as that is likely a more recent
version.

Finally, in spack_cmd, it is time to give the installation a test:

``spack install cpuinfo``

If you are a developer and want to use your source version of spack instead of
a release version, simply replace spack in the above call with:

``python path\to\your\checkout\bin\spack``
