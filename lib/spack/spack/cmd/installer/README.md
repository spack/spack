This README will guide you through the steps needed to install Spack and 
start running it on a fresh Windows machine.

# Step 1: Install prerequisites

Before downloading and configuring spack, we have to prepare our box for the 
installation. The following packages are required to successfully build and 
run the installer, in addition to running spack in general:

* Visual Studio: Explanation, include CMake tools, etc.
* Python
* Git
* CMake
* Wix

## Visual Studio

Microsoft Visual Studio provides the Windows C/C++ compiler that is currently supported by Spack.

We require several specific components to be included in the Visual Studio installation.  One is the C/C++ toolset, which can be selected as "Desktop development with C++" or "C++ build tools," depending on installation type (Professional, Build Tools, etc.)  The other required component is "C++ CMake tools for Windows," which can be selected from among the optional packages.  This provides CMake and Ninja for use during Spack configuration.

If you already have Visual Studio installed, you can make sure these components are installed by
rerunning the installer.  Next to your installation, select "Modify" and look at the "Installation details" pane on the right.

## Python

Python 3 can be downloaded from the Windows Store and will appear in your
path if installed from there.

## Git

Git is a version control system similar to Subversion and will be needed to
download Spack and the appropriate installation files. A bash console and GUI
can be downloaded from https://git-scm.com/downloads. If you are unfamiliar
with Git, there are a myriad of resources online to help guide you through
checking out repositories and switching development branches.

## CMake

CMake is a buildfile generator that will be used to help create the Windows
installer and, later on, install packages with Spack. While your Visual
Studio installation will have a CMake installation as well (see above), we
recommend you still download CMake from https://cmake.org/download/ as
there may be a newer version available.

## Wix Toolset

Wix is a utility used for .msi creation and can be downloaded and
installed at https://wixtoolset.org/releases/. The Visual Studio
extensions are not necessary.

# Step 2: Get Spack

We are now ready to get the Spack environment set up on our machine. We
begin by creating a top-level directory to do our work in: we will call
it ``spack_install`` in this tutorial. Inside this directory, use Git to
clone the Spack repo, hosted at https://github.com/spack/spack.git.

The files and scripts used for Windows installation are on the
features/windows-support branch; ``cd`` into the repo and use 
``git checkout`` to switch to it. Then navigate to 
``lib\spack\spack\cmd\installer`` and copy the ``scripts`` directory and
``spack_cmd.bat`` up to the top-level ``spack_install`` directory.

Your file structure should look like this after following the above
steps:

```
spack_install
    |--------spack
    |--------scripts
    |--------spack_cmd.bat
```

# Step 3: Make the installer

To actually make the installer, start by running ``spack_cmd.bat`` from
Windows Explorer (this may require you to Run as Administrator). If a
warning appears that Python is not in your path, which can happen if you
installed Python from the website instead of Windows Store, add it in now.

``spack_cmd.bat`` will produce a DOS console window. Navigate to your
``spack_install`` directory (i.e. where you placed ``spack_cmd.bat``), and
create a new directory to store the installation (say, ``tmp``). This ``tmp``
directory must exist for the following commands to not fail.

There are two ways to create the installer. If you would like to create it
from a release version of Spack, say, 0.16.0, and store it in ``tmp``, you
can use the following command:

``spack make-installer -v 0.16.0 tmp``

The path to ``tmp`` can be either relative or absolute, but again, the
directory itself must already exist.

Alternatively, if you would like to build the installer using a local
checkout of Spack source (release or development), you can use the
-s flag. For example, if you already have a checkout of the version
0.16.0 source, you can use:

``spack make-installer -s spack-0.16.0 tmp``

Either way, a file called ``Spack.msi`` will be created inside the ``tmp``
directory, which can then be run from Windows Explorer like any other
installer. 

# Step 4: Run the installer

...

# Step 5: Configure Spack and test

The last thing to do after running the installer is to finish Spack configuration. This
is covered in the online documentation for Spack, but there are a few Windows-specific
nuances that are worth mentioning here.

First, inside the ``spack_cmd`` console, run the following command:

``spack compiler find``

This creates a .spack directory in our home directory, along with a windows subdirectory
containing a compilers.yaml file. On a fresh Windows install, the only compiler that
should be found is your installation of Microsoft Visual Studio.

We need to provide the config.yaml and packages.yaml configurations by ourselves. Open 
your text editor of choice and enter the following lines for config.yaml:

```
config:
  locks: false
  install_tree:
    root: $spack\opt\spack
    projections:
      all: '${ARCHITECTURE}\${COMPILERNAME}-${COMPILERVER}\${PACKAGE}-${VERSION}-${HASH}'
```

(These settings are identical to those in the default config.yaml
provided with your Spack checkout, except with forward slashes replaced by backslashes for
Windows compatibility.) It is important that all indentions in .yaml files are done with spaces and not tabs, so take care
when editing one by hand.

For the packages.yaml file, we need to direct spack towards both our CMake
installation and towards Ninja. Therefore, your packages.yaml file will look something
like this, with possibly slight variants in the paths to CMake and Ninja:

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
version. If you don't have a path to Ninja analogous to the above, then you can
obtain it by running the Visual Studio Insaller and following the instructions
in Step 1 of this walkthrough.

Once all three of these files are present in your ``.spack/windows`` directory,
it is time to give the installation a test. Install a basic package with 
``spack_cmd`` via:

``spack install cpuinfo``

If you are a developer and want to use your source version of Spack instead of
a release version, simply replace Spack in the above call with:

``python path\to\your\checkout\bin\spack``
