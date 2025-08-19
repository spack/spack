.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A guide for developers and administrators on how to package software for Spack, covering the structure of a package, creating and editing packages, and defining dependencies and variants.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 0
   :width: 100%

   * - **1. Creation**
     - :doc:`2. Build <packaging_guide_build>`
     - :doc:`3. Testing <packaging_guide_testing>`
     - :doc:`4. Advanced <packaging_guide_advanced>`

Packaging Guide: defining a package
===================================

This packaging guide is intended for developers or administrators who want to package software so that Spack can install it.
It assumes that you have at least some familiarity with Python, and that you've read the :ref:`basic usage guide <basic-usage>`, especially the part about :ref:`specs <sec-specs>`.

There are two key parts of Spack:

#. **Specs**: expressions for describing builds of software, and
#. **Packages**: Python modules that describe how to build and test software according to a spec.

Specs allow a user to describe a *particular* build in a way that a package author can understand.
Packages allow the packager to encapsulate the build logic for different versions, compilers, options, platforms, and dependency combinations in one place.
Essentially, a package translates a spec into build logic.
It also allows the packager to write spec-specific tests of the installed software.

Packages in Spack are written in pure Python, so you can do anything in Spack that you can do in Python.
Python was chosen as the implementation language for two reasons.
First, Python is ubiquitous in the scientific software community.
Second, it has many powerful features to help make package writing easy.

.. _setting-up-for-package-development:


Setting up for package development
----------------------------------

For developing new packages or working with existing ones, it's helpful to have the ``spack/spack-packages`` repository in a convenient location like your home directory, rather than the default ``~/.spack/package_repos/<hash>/``.

If you plan to contribute changes back to Spack, we recommend creating a fork of the `packages repository <https://github.com/spack/spack-packages>`_.
See `GitHub's fork documentation <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`_ for details.
Once you have a fork, clone it:

.. code-block:: console

   $ git clone --depth=100 git@github.com:YOUR-USERNAME/spack-packages.git ~/spack-packages
   $ cd ~/spack-packages
   $ git remote add --track develop upstream git@github.com:spack/spack-packages.git

Then configure Spack to use your local repository:

.. code-block:: console

   $ spack repo set --destination ~/spack-packages builtin

Before starting work, it's useful to create a new branch in your local repository.

.. code-block:: console

   $ git checkout -b add-my-package

Lastly, verify that Spack is picking up the right repository by checking the location of a known package, like ``zlib``:

.. code-block:: console

   $ spack location --package-dir zlib
   /home/your-username/spack-packages/repos/spack_repo/builtin/packages/zlib

With this setup, you can conveniently access the package files, and contribute changes back to Spack.

Structure of a package
----------------------

A Spack package is a Python module ``package.py`` stored in a package repository.
It contains a package class and sometimes a builder class that define its metadata and build behavior.

The typical structure of a package is as follows:

.. code-block:: python

   # spack_repo/builtin/packages/example/package.py

   # import of package / builder classes
   from spack_repo.builtin.build_systems.cmake import CMakePackage

   # import Package API
   from spack.package import *

   class Example(CMakePackage):
       """Example package"""  # package description

       # Metadata and Directives
       homepage = "https://example.com"
       url = "https://example.com/example/v2.4.0.tar.gz"

       maintainers("github_user1", "github_user2")

       license("UNKNOWN", checked_by="github_user1")

       # version directives listed in order with the latest first
       version("2.4.0", sha256="845ccd79ed915fa2dedf3b2abde3fffe7f9f5673cc51be88e47e6432bd1408be")
       version("2.3.0", sha256="cd3274e0abcbc2dfb678d87595e9d3ab1c6954d7921d57a88a23cf4981af46c9")

       # variant directives expose build options
       variant("feature", default=False, description="Enable a specific feature")
       variant("codec", default=False, description="Build the CODEC executables")

       # dependency directives declare required software
       depends_on("cxx", type="build")
       depends_on("libfoo", when="+feature")

       # Build Instructions
       def cmake_args(self):
           return [
               self.define_from_variant("BUILD_CODEC", "codec"),
               self.define("EXAMPLE_OPTIMIZED", False),
               self.define("BUILD_THIRDPARTY", False),
           ]

The package class is named after the package, and can roughly be divided into two parts:

* **metadata and directives**: attributes and directives that describe the package, such as its homepage, maintainers, license, variants, and dependencies.
  This is the declarative part of the package.
* **build instructions**: methods that define how to build and install the package, such as `cmake_args()`.
  This is the imperative part of the package.

In this part of the packaging guide we will cover the **metadata and directives** in detail.
In the :doc:`second part <packaging_guide_build>`, we will cover the **build instructions**, including how to write custom build logic for different build systems.

Package Names and the Package Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages are referred to by their **package names**, whether it's on the command line or in a package recipe.
Package names can contain lowercase letters, numbers, and dashes.
Every package lives as a ``package.py`` file in a **package directory** inside a :ref:`package repository <repositories>`.
Usually the package name coincides with the directory name on the filesystem: the ``libelf`` package corresponds to the ``libelf/package.py`` file.

.. note::

   **Package name to directory mapping**.
   There is a one to one mapping between package names and package directories.
   Usually the mapping is trivial: the package name is the same as the directory name.
   However, there are a few exceptions to this rule:

   1. Hyphens in package names are replaced by underscores in directory names.
      For example, the package name ``py-numpy`` maps to ``py_numpy/package.py``.
   2. Names starting with numbers get an underscore prefix.
      For example, the package name ``7zip`` maps to ``_7zip/package.py``.
   3. Package names that are reserved keywords in Python are also prefixed with an underscore.
      For example, the package name ``pass`` maps to ``_pass/package.py``.

   This ensures that every package directory is a valid Python module name.


Package class names
^^^^^^^^^^^^^^^^^^^

Spack loads ``package.py`` files dynamically, and it needs to find a special class name in the file for the load to succeed.
The **package class** is formed by converting words separated by ``-`` in the package name to CamelCase.
If the package name starts with a number, we prefix the class name with ``_``.
Here are some examples:

=================  =================
 Package Name         Class Name
=================  =================
 ``foo-bar``         ``FooBar``
 ``3proxy``          ``_3proxy``
=================  =================

In general, you won't have to remember this naming convention because :ref:`cmd-spack-create` and :ref:`cmd-spack-edit` handle the details for you.

.. _creating-and-editing-packages:

Creating and editing packages
-----------------------------

Spack has various commands that help you create and edit packages.
Spack can create the boilerplate for new packages and open them in your editor for you to fill in.
It can also help you edit existing packages, so you don't have to navigate to the package directory manually.


.. _controlling-the-editor:

Controlling the editor
^^^^^^^^^^^^^^^^^^^^^^

When Spack needs to open an editor for you (e.g., for commands like :ref:`cmd-spack-create` or :ref:`cmd-spack-edit`), it looks at several environment variables to figure out what to use.
The order of precedence is:

* ``SPACK_EDITOR``: highest precedence, in case you want something specific for Spack;
* ``VISUAL``: standard environment variable for full-screen editors like ``vim`` or ``emacs``;
* ``EDITOR``: older environment variable for your editor.

You can set any of these to the command you want to run, e.g., in ``bash`` you might run one of these:

.. code-block:: console

   $ export VISUAL=vim
   $ export EDITOR="emacs -nw"
   $ export SPACK_EDITOR=nano

If Spack finds none of these variables set, it will look for ``vim``, ``vi``, ``emacs``, ``nano``, and ``notepad``, in that order.

.. _cmd-spack-create:

Creating new packages
^^^^^^^^^^^^^^^^^^^^^

To create a new package, Spack provides a command that generates a ``package.py`` file in an existing repository, with a boilerplate package template.
Here's an example:

.. code-block:: console

   $ spack create https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2

Spack examines the tarball URL and tries to figure out the name of the package to be created.
If the name contains uppercase letters, these are automatically converted to lowercase.
If the name contains underscores or periods, these are automatically converted to dashes.

Spack also searches for *additional* versions located in the same directory on the website.
Spack prompts you to tell you how many versions it found and asks you how many you would like to download and checksum:

.. code-block:: console

   $ spack create https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
   ==> This looks like a URL for gmp
   ==> Found 16 versions of gmp:

     6.1.2   https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
     6.1.1   https://gmplib.org/download/gmp/gmp-6.1.1.tar.bz2
     6.1.0   https://gmplib.org/download/gmp/gmp-6.1.0.tar.bz2
     ...
     5.0.0   https://gmplib.org/download/gmp/gmp-5.0.0.tar.bz2

   How many would you like to checksum? (default is 1, q to abort)

Spack will automatically download the number of tarballs you specify (starting with the most recent) and checksum each of them.

You do not *have* to download all of the versions up front.
You can always choose to download just one tarball initially, and run :ref:`cmd-spack-checksum` later if you need more versions.

Spack automatically creates a directory in the appropriate repository, generates a boilerplate template for your package, and opens up the new ``package.py`` in your favorite ``$EDITOR`` (see :ref:`controlling-the-editor` for details):

.. code-block:: python
   :linenos:

   # Copyright Spack Project Developers. See COPYRIGHT file for details.
   #
   # SPDX-License-Identifier: (Apache-2.0 OR MIT)

   # ----------------------------------------------------------------------------
   # If you submit this package back to Spack as a pull request,
   # please first remove this boilerplate and all FIXME comments.
   #
   # This is a template package file for Spack.  We've put "FIXME"
   # next to all the things you'll want to change. Once you've handled
   # them, you can save this file and test your package like this:
   #
   #     spack install gmp
   #
   # You can edit this file again by typing:
   #
   #     spack edit gmp
   #
   # See the Spack documentation for more information on packaging.
   # ----------------------------------------------------------------------------
   import spack_repo.builtin.build_systems.autotools
   from spack.package import *


   class Gmp(AutotoolsPackage):
       """FIXME: Put a proper description of your package here."""

       # FIXME: Add a proper url for your package's homepage here.
       homepage = "https://www.example.com"
       url = "https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2"

       # FIXME: Add a list of GitHub accounts to
       # notify when the package is updated.
       # maintainers("github_user1", "github_user2")

       # FIXME: Add the SPDX identifier of the project's license below.
       # See https://spdx.org/licenses/ for a list. Upon manually verifying
       # the license, set checked_by to your Github username.
       license("UNKNOWN", checked_by="github_user1")

       version("6.2.1", sha256="eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c")

       # FIXME: Add dependencies if required.
       # depends_on("foo")

       def configure_args(self):
           # FIXME: Add arguments other than --prefix
           # FIXME: If not needed delete the function
           args = []
           return args

The tedious stuff (creating the class, checksumming archives) has been done for you.
Spack correctly detected that ``gmp`` uses the ``autotools`` build system, so it created a new ``Gmp`` package that subclasses the ``AutotoolsPackage`` base class.

The default installation procedure for a package subclassing the ``AutotoolsPackage`` is to go through the typical process of:

.. code-block:: bash

   ./configure --prefix=/path/to/installation/directory
   make
   make check
   make install

For most Autotools packages, this is sufficient.
If you need to add additional arguments to the ``./configure`` call, add them via the ``configure_args`` function.

In the generated package, the download ``url`` attribute is already set.
All the things you still need to change are marked with ``FIXME`` labels.
You can delete the commented instructions between the Spack license and the first import statement after reading them.
The rest of the tasks you need to complete are as follows:

#. Add a description.

   Immediately inside the package class is a *docstring* in triple-quotes (``"""``).
   It is used to generate the description shown when users run ``spack info``.

#. Change the ``homepage`` to a useful URL.

   The ``homepage`` is displayed when users run ``spack info`` so that they can learn more about your package.

#. Add a comma-separated list of maintainers.

   Add a list of GitHub accounts of people who want to be notified any time the package is modified.
   See :ref:`package_maintainers`.

#. Change the ``license`` to the correct license.

   The ``license`` is displayed when users run ``spack info`` so that they can learn more about your package.
   See :ref:`package_license`.

#. Add ``depends_on()`` calls for the package's dependencies.

   ``depends_on`` tells Spack that other packages need to be built and installed before this one.
   See :ref:`dependencies`.

#. Get the installation working.

   Your new package may require specific flags during ``configure``.
   These can be added via ``configure_args``.
   If no arguments are needed at this time, change the implementation to ``return []``.
   Specifics will differ depending on the package and its build system.
   :ref:`installation_process` is covered in detail later.

Further package creation options
""""""""""""""""""""""""""""""""

If you do not have a URL to a tarball, you can still use ``spack create`` to generate the boilerplate for a package.

.. code-block:: console

   $ spack create --name intel

This will create a simple ``intel`` package with an ``install()`` method that you can craft to install your package.
Likewise, you can force the build system to be used with ``--template`` and, in case it's needed, you can overwrite a package already in the repository with ``--force``:

.. code-block:: console

   $ spack create --name gmp https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
   $ spack create --force --template autotools https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2

A complete list of available build system templates can be found by running ``spack create --help``.

.. _cmd-spack-edit:

Editing existing packages
^^^^^^^^^^^^^^^^^^^^^^^^^

One of the easiest ways to learn how to write packages is to look at existing ones.
You can open an existing package in your editor using the ``spack edit`` command:

.. code-block:: console

   $ spack edit gmp

If you used ``spack create`` to create a package, you can get back to it later with ``spack edit``.
The ``spack edit`` command saves you the trouble of figuring out the package location and navigating to it.
If needed, you can still find the package location using the ``spack location`` command:

.. code-block:: console

   $ spack location --package-dir gmp
   ~/spack-packages/repos/spack_repo/builtin/packages/gmp/

and with shell support enabled, you can also enter to the package directory:

.. code-block:: console

   $ spack cd --package-dir gmp

If you want to edit multiple packages at once, you can run

.. code-block:: console

   $ spack edit

without specifying a package name, which will open the directory containing all the packages in your editor.

Finally, the commands ``spack location --repo`` and ``spack cd --repo`` help you navigate to the root of the package repository.

Source code and versions
------------------------

Spack packages are designed to be built from source code.
Typically every package version has a corresponding source code archive, which Spack downloads and verifies before building the package.

.. _versions-and-fetching:

Versions and URLs
^^^^^^^^^^^^^^^^^

The most straightforward way to add new versions to your package is to add a line like this in the package class:

.. code-block:: python

   class Foo(Package):

       url = "http://example.com/foo-8.2.1.tar.gz"

       version("8.2.1", sha256="85f477fdd6f8194ab6a0e7afd1cb34eae46c775278d5db9d7ebc9ddaf50c23b1")
       version("8.2.0", sha256="427b2e244e73385515b8ad4f75358139d44a4c792d9b26ddffe2582835cedd8c")
       version("8.1.2", sha256="67630a20f92ace137e68b67f13010487a03e4f036cdd328e199db85d24a434a4")

.. note::

   By convention, we list versions in descending order, from newest to oldest.

.. note::

   :ref:`Bundle packages  <bundlepackage>` do not have source code so there is nothing to fetch.
   Consequently, their version directives consist solely of the version name (e.g., ``version("202309")``).


Notice how you only have to specify the URL once, in the ``url`` field.
Spack is smart enough to extrapolate the URL for each version based on the version number and download version ``8.2.0`` of the ``Foo`` package above from ``http://example.com/foo-8.2.0.tar.gz``.

If the URL is particularly complicated or changes based on the release, you can override the default URL generation algorithm by defining your own ``url_for_version()`` function.
For example, the download URL for OpenMPI contains the ``major.minor`` version in one spot and the ``major.minor.patch`` version in another:

.. code-block:: text

   https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2

In order to handle this, you can define a ``url_for_version()`` function like so:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/openmpi/package.py
   :pyobject: Openmpi.url_for_version

With the use of this ``url_for_version()``, Spack knows to download OpenMPI ``2.1.1`` from http://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2 but download OpenMPI ``1.10.7`` from http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.7.tar.bz2.

You'll notice that OpenMPI's ``url_for_version()`` function makes use of a special ``Version`` function called ``up_to()``.
When you call ``version.up_to(2)`` on a version like ``1.10.0``, it returns ``1.10``.
``version.up_to(1)`` would return ``1``.
This can be very useful for packages that place all ``X.Y.*`` versions in a single directory and then places all ``X.Y.Z`` versions in a sub-directory.

There are a few ``Version`` properties you should be aware of.
We generally prefer numeric versions to be separated by dots for uniformity, but not all tarballs are named that way.
For example, ``icu4c`` separates its major and minor versions with underscores, like ``icu4c-57_1-src.tgz``.
The value ``57_1`` can be obtained with the use of the ``version.underscored`` property.
There are other separator properties as well:

===================  ======
Property             Result
===================  ======
version.dotted       1.2.3
version.dashed       1-2-3
version.underscored  1_2_3
version.joined       123
===================  ======

.. note::

   Python properties don't need parentheses.
   ``version.dashed`` is correct.
   ``version.dashed()`` is incorrect.

In addition, these version properties can be combined with ``up_to()``.
For example:

.. code-block:: python

   >>> version = Version("1.2.3")
   >>> version.up_to(2).dashed
   Version("1-2")
   >>> version.underscored.up_to(2)
   Version("1_2")


As you can see, order is not important.
Just keep in mind that ``up_to()`` and the other version properties return ``Version`` objects, not strings.

If a URL cannot be derived systematically, or there is a special URL for one of its versions, you can add an explicit URL for a particular version:

.. code-block:: python

   version(
       "8.2.1",
       sha256="91ee5e9f42ba3d34e414443b36a27b797a56a47aad6bb1e4c1769e69c77ce0ca",
       url="http://example.com/foo-8.2.1-special-version.tar.gz",
   )


When you supply a custom URL for a version, Spack uses that URL *verbatim* and does not perform extrapolation.
The order of precedence of these methods is:

#. package-level ``url``
#. ``url_for_version()``
#. version-specific ``url``

so if your package contains a ``url_for_version()``, it can be overridden by a version-specific ``url``.

If your package does not contain a package-level ``url`` or ``url_for_version()``, Spack can determine which URL to download from even if only some of the versions specify their own ``url``.
Spack will use the nearest URL *before* the requested version.
This is useful for packages that have an easy to extrapolate URL, but keep changing their URL format every few releases.
With this method, you only need to specify the ``url`` when the URL changes.

.. _checksum-verification:

Checksum verification
^^^^^^^^^^^^^^^^^^^^^

In the above example we see that each version is associated with a ``sha256`` checksum.
Spack uses these checksums to verify that downloaded source code has not been modified, corrupted or compromised.
Therefore, Spack requires that all URL downloads have a checksum, and refuses to install packages when checksum verification fails.

.. note::

   While this requirement can be disabled for development with ``spack install --no-checksum``, it is **not recommended**.

.. warning::

   **Trusted Downloads.**
   It is critical from a security and reproducibility standpoint that Spack be able to verify the downloaded source.
   This is accomplished using a hash.

   For URL downloads, Spack supports multiple cryptographic hash algorithms, including ``sha256`` (recommended), ``sha384`` and ``sha512``.
   See :ref:`version urls <versions-and-fetching>` for more information.

   For repository downloads, which we will cover in more detail later, this is done by specifying a **full commit hash** (e.g., :ref:`git <git-commits>`, :ref:`hg <hg-revisions>`).


.. _cmd-spack-checksum:

Automatically adding new versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``spack checksum`` command can be used to automate the process of adding new versions to a package, assuming the package's download URLs follow a consistent pattern.

``spack checksum``
""""""""""""""""""

Using ``spack checksum`` is straightforward:

.. code-block:: console

   $ spack checksum libelf
   ==> Found 16 versions of libelf.
     0.8.13    http://www.mr511.de/software/libelf-0.8.13.tar.gz
     0.8.12    http://www.mr511.de/software/libelf-0.8.12.tar.gz
     0.8.11    http://www.mr511.de/software/libelf-0.8.11.tar.gz
     0.8.10    http://www.mr511.de/software/libelf-0.8.10.tar.gz
     0.8.9     http://www.mr511.de/software/libelf-0.8.9.tar.gz
     0.8.8     http://www.mr511.de/software/libelf-0.8.8.tar.gz
     0.8.7     http://www.mr511.de/software/libelf-0.8.7.tar.gz
     0.8.6     http://www.mr511.de/software/libelf-0.8.6.tar.gz
     0.8.5     http://www.mr511.de/software/libelf-0.8.5.tar.gz
     ...
     0.5.2     http://www.mr511.de/software/libelf-0.5.2.tar.gz

   How many would you like to checksum? (default is 1, q to abort)

This does the same thing that ``spack create`` does, but it allows you to go back and add new versions easily as you need them (e.g., as they're released).
It fetches the tarballs you ask for and prints out a list of ``version`` commands ready to copy/paste into your package file:

.. code-block:: console

   ==> Checksummed new versions of libelf:
       version("0.8.13", sha256="ec6ddbe4b1ac220244230b040fd6a5a102a96337603e703885848ff64cb582a5")
       version("0.8.12", sha256="46db404a287b3d17210b4183cbc7055d7b8bbcb15957daeb51f2dc06002ca8a3")
       version("0.8.11", sha256="e5be0f5d199ad11fbc74e59a8e120cc8b6fbcadaf1827c4e8e6a133ceaadbc4c")
       version("0.8.10", sha256="f1708dd17a476a7abaf6c395723e0745ba8f6b196115513b6d8922d4b5bfbab4")

.. note::

   ``spack checksum`` assumes that Spack can extrapolate new URLs from an existing URL in the package, and that Spack can find similar URLs on a webpage.
   If that's not possible, e.g., if the package's developers don't name their source archive consistently, you'll need to manually add ``version`` calls yourself.

By default, Spack will search for new versions by scraping the parent URL component of the source archive you gave it in the ``url`` attribute.
So, if the sources are at ``http://example.com/downloads/foo-1.0.tar.gz``, Spack computes a *list URL* from it ``http://example.com/downloads/``, and scans that for links to other versions of the package.
If you need to search another path for download links, you can supply some extra attributes that control how your package finds new versions.
See the documentation on :ref:`attribute_list_url` and :ref:`attribute_list_depth`.


.. _attribute_list_url:

``list_url``
""""""""""""

This optional attribute can be set to tell Spack where to scan for links to other versions of the package.
For example, the following package has a ``list_url`` attribute that points to a page listing all available versions of the package:

.. code-block:: python
   :linenos:

   class Example(Package):
       homepage = "http://www.example.com"
       url      = "http://www.example.com/libexample-1.2.3.tar.gz"
       list_url = "http://www.example.com/downloads/all-versions.html"

.. _attribute_list_depth:

``list_depth``
""""""""""""""

Many packages have a listing of available versions on a single webpage, but not all do.
For example, ``mpich`` has a tarball URL that looks like this:

.. code-block:: python

   url = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"

But its downloads are a few clicks away from ``http://www.mpich.org/static/downloads/``.
So, we need to add a ``list_url`` *and* a ``list_depth`` attribute:

.. code-block:: python
   :linenos:

   class Mpich(Package):
       homepage   = "http://www.mpich.org"
       url        = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
       list_url   = "http://www.mpich.org/static/downloads/"
       list_depth = 1

By default, Spack only looks at the top-level page available at ``list_url``.
``list_depth = 1`` tells it to follow up to 1 level of links from the top-level page.
Note that here, this implies 1 level of subdirectories, as the ``mpich`` website is structured much like a filesystem.
But ``list_depth`` really refers to link depth when spidering the page.

Mirrors of the main URL
^^^^^^^^^^^^^^^^^^^^^^^

Spack supports listing mirrors of the main URL in a package by defining the ``urls`` attribute:

.. code-block:: python

  class Foo(Package):

    urls = [
        "http://example.com/foo-1.0.tar.gz",
        "http://mirror.com/foo-1.0.tar.gz"
    ]

instead of just a single ``url``.
This attribute is a list of possible URLs that will be tried in order when fetching packages.
Notice that either one of ``url`` or ``urls`` can be present in a package, but not both at the same time.

A well-known case of packages that can be fetched from multiple mirrors is that of GNU.
For that, Spack goes a step further and defines a mixin class that takes care of all of the plumbing and requires packagers to just define a proper ``gnu_mirror_path`` attribute:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/autoconf/package.py
   :lines: 9-18


.. _preferred_versions:

Preferring versions over others
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When users install a package without constraining the versions, Spack will typically pick the latest version available.
Usually this is the desired behavior, but as a packager you may know that the latest version is not mature enough or has known issues that make it unsuitable for production use.
In this case, you can mark an older version as preferred using the ``preferred=True`` argument in the ``version`` directive, so that Spack will default to the latest *preferred* version.

.. code-block:: python

   class Foo(Package):
       version("2.0.0", sha256="...")
       version("1.2.3", sha256="...", preferred=True)

See the section on :ref:`version ordering <version-comparison>` for more details and exceptions on how the latest version is computed.


.. _deprecate:

Deprecating old versions
^^^^^^^^^^^^^^^^^^^^^^^^

There are many reasons to remove old versions of software:

#. Security vulnerabilities (most serious reason)
#. No longer available for download (right to be forgotten)
#. Maintainer/developer inability/unwillingness to support old versions
#. Changing build systems that increase package complexity
#. Changing dependencies/patches/resources/flags that increase package complexity
#. Package or version rename

At the same time, there are many reasons to keep old versions of software:

#. Reproducibility
#. Requirements for older packages (e.g., some packages still rely on Qt 3)

In general, you should not remove old versions from a ``package.py`` directly.
Instead, you should first deprecate them using the following syntax:

.. code-block:: python

   version("1.2.3", sha256="...", deprecated=True)


This has two effects.
First, ``spack info`` will no longer advertise that version.
Second, commands like ``spack install`` that fetch the package will require user approval:

.. code-block:: spec

   $ spack install openssl@1.0.1e
   ==> Warning: openssl@1.0.1e is deprecated and may be removed in a future Spack release.
   ==>   Fetch anyway? [y/N]


If you use ``spack install --deprecated``, this check can be skipped.

This also applies to package recipes that are renamed or removed.
You should first deprecate all versions before removing a package.
If you need to rename it, you can deprecate the old package and create a new package at the same time.

Version deprecations should always last at least one release cycle of the builtin package repository before the version is completely removed.
No version should be removed without such a deprecation process.
This gives users a chance to complain about the deprecation in case the old version is needed for some application.
If you require a deprecated version of a package, simply submit a PR to remove ``deprecated=True`` from the package.
However, you may be asked to help maintain this version of the package if the current maintainers are unwilling to support this older version.


.. _version-comparison:

Version ordering
^^^^^^^^^^^^^^^^

Without :ref:`version constraints <version_constraints>`, :ref:`preferences <preferred_versions>` and :ref:`deprecations <deprecate>`, Spack will always pick *the latest* version as defined in the package.
What latest means is determined by the version comparison rules defined in Spack, *not* the order in which versions are listed in the package file.

Spack imposes a generic total ordering on the set of versions, independently from the package they are associated with.

Most Spack versions are numeric, a tuple of integers; for example, ``0.1``, ``6.96``, or ``1.2.3.1``.
In this very basic case, version comparison is lexicographical on the numeric components: ``1.2 < 1.2.1 < 1.2.2 < 1.10``.

Other separators for components are also possible, for example ``2025-03-01 < 2025-06``.

Spack can also support string components such as ``1.1.1a`` and ``1.y.0``.
String components are considered less than numeric components, so ``1.y.0 < 1.0``.
This is for consistency with `RPM <https://bugzilla.redhat.com/show_bug.cgi?id=50977>`_.
String components do not have to be separated by dots or any other delimiter.
So, the contrived version ``1y0`` is identical to ``1.y.0``.

Pre-release suffixes also contain string parts, but they are handled in a special way.
For example ``1.2.3alpha1`` is parsed as a pre-release of the version ``1.2.3``.
This allows Spack to order it before the actual release: ``1.2.3alpha1 < 1.2.3``.
Spack supports alpha, beta and release candidate suffixes: ``1.2alpha1 < 1.2beta1 < 1.2rc1 < 1.2``.
Any suffix not recognized as a pre-release is treated as an ordinary string component, so ``1.2 < 1.2-mysuffix``.

Finally, there are a few special string components that are considered "infinity versions".
They include ``develop``, ``main``, ``master``, ``head``, ``trunk``, and ``stable``, in descending order.
For example: ``1.2 < develop``.
These are useful for specifying the most recent development version of a package (often a moving target like a git branch), without assigning a specific version number.
Infinity versions are not automatically used when determining the latest version of a package unless explicitly required by another package or user.

More formally, the order on versions is defined as follows.
A version string is split into a list of components based on delimiters such as ``.``, ``-``, ``_``, and string boundaries.
The components are split into the **release** and a possible **pre-release** (if the last component is numeric and the second to last is a string ``alpha``, ``beta`` or ``rc``).
The release components are ordered lexicographically, with comparison between different types of components as follows:

#. The following special strings are considered larger than any other numeric or non-numeric version component, and satisfy the following order between themselves: ``develop > main > master > head > trunk > stable``.

#. Numbers are ordered numerically, are less than special strings, and larger than other non-numeric components.

#. All other non-numeric components are less than numeric components, and are ordered alphabetically.

Finally, if the release components are equal, the pre-release components are used to break the tie.

The logic behind this sort order is two-fold:

#. Non-numeric versions are usually used for special cases while developing or debugging a piece of software.
   Keeping most of them less than numeric versions ensures that Spack chooses numeric versions by default whenever possible.

#. The most-recent development version of a package will usually be newer than any released numeric versions.
   This allows the ``@develop`` version to satisfy dependencies like ``depends_on(abc, when="@x.y.z:")``


.. _vcs-fetch:

Fetching from code repositories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For some packages, source code is provided in a Version Control System (VCS) repository rather than in a tarball.
Spack can fetch packages from VCS repositories.
Currently, Spack supports fetching with `Git <git-fetch_>`_, `Mercurial (hg) <hg-fetch_>`_, `Subversion (svn) <svn-fetch_>`_, and `CVS (cvs) <cvs-fetch_>`_.
In all cases, the destination is the standard stage source path.

To fetch a package from a source repository, Spack needs to know which VCS to use and where to download from.
Much like with ``url``, package authors can specify a class-level ``git``, ``hg``, ``svn``, or ``cvs`` attribute containing the correct download location.

Many packages developed with Git have both a Git repository as well as release tarballs available for download.
Packages can define both a class-level tarball URL and VCS.
For example:

.. code-block:: python

   class Trilinos(CMakePackage):

       homepage = "https://trilinos.org/"
       url      = "https://github.com/trilinos/Trilinos/archive/trilinos-release-12-12-1.tar.gz"
       git      = "https://github.com/trilinos/Trilinos.git"

       version("develop", branch="develop")
       version("master",  branch="master")
       version("12.12.1", sha256="87428fc522803d31065e7bce3cf03fe475096631e5e07bbd7a0fde60c4cf25c7")
       version("12.10.1", sha256="0263829989b6fd954f72baaf2fc64bc2e2f01d692d4de72986ea808f6e99813f")
       version("12.8.1",  sha256="a3a5e715f0cc574a73c3f9bebb6bc24f32ffd5b67b387244c2c909da779a1478")

If a package contains both a ``url`` and ``git`` class-level attribute, Spack decides which to use based on the arguments to the ``version()`` directive.
Versions containing a specific branch, tag, commit or revision are assumed to be for VCS download methods, while versions containing a checksum are assumed to be for URL download methods.

Like ``url``, if a specific version downloads from a different repository than the default repo, it can be overridden with a version-specific argument.

.. note::

   In order to reduce ambiguity, each package can only have a single VCS top-level attribute in addition to ``url``.
   In the rare case that a package uses multiple VCS, a fetch strategy can be specified for each version.
   For example, the ``rockstar`` package contains:

   .. code-block:: python

      class Rockstar(MakefilePackage):

          homepage = "https://bitbucket.org/gfcstanford/rockstar"

          version("develop", git="https://bitbucket.org/gfcstanford/rockstar.git")
          version("yt", hg="https://bitbucket.org/MatthewTurk/rockstar")


.. _git-fetch:

Git
"""""""

Git fetching supports the following parameters to the ``version`` directive:

* ``git``: URL of the git repository, if different than the class-level ``git``.
* ``branch``: Name of a :ref:`branch <git-branches>` to fetch.
* ``tag``: Name of a :ref:`tag <git-tags>` to fetch.
* ``commit``: SHA hash (or prefix) of a :ref:`commit <git-commits>` to fetch.
* ``submodules``: Also fetch :ref:`submodules <git-submodules>` recursively when checking out this repository.
* ``submodules_delete``: A list of submodules to forcibly delete from the repository after fetching.
  Useful if a version in the repository has submodules that have disappeared/are no longer accessible.
* ``get_full_repo``: Ensure the full git history is checked out with all remote branch information.
  Normally (``get_full_repo=False``, the default), the git option ``--depth 1`` will be used if the version of git and the specified transport protocol support it, and ``--single-branch`` will be used if the version of git supports it.
* ``git_sparse_paths``: Only clone the provided :ref:`relative paths <git-sparse-checkout>`.

The destination directory for the clone is the standard stage source path.

.. note::

   ``tag`` and ``branch`` should not be combined in the version parameters.

   We strongly recommend that all ``tag`` entries be paired with ``commit``.


.. warning::

   **Trusted Downloads.**
   It is critical from a security and reproducibility standpoint that Spack be able to verify the downloaded source.

   Providing the full ``commit`` SHA hash allows for Spack to preserve binary provenance for all binaries since git commits are guaranteed to be unique points in the git history.
   Whereas, the mutable nature of branches and tags cannot provide such a guarantee.

   A git download *is trusted* only if the full commit SHA is specified.
   Therefore, it is *the* recommended way to securely download from a Git repository.


.. _git-default-branch:

Default branch
  A version with only a name results in fetching a repository's default branch:

  .. code-block:: python

     class Example(Package):

         git = "https://github.com/example-project/example.git"

         version("develop")

  Aside from use of HTTPS, there is no way to verify that the repository has not been compromised.
  Furthermore, the commit you get when you install the package likely won't be the same commit that was used when the package was first written.
  There is also the risk that the default branch may change.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.

    It is better to specify a branch name (see :ref:`below <git-branches>`).


.. _git-branches:

Branches
  To fetch a particular branch, use the ``branch`` parameter, preferrably with the same name as the version.
  For example,

  .. code-block:: python

     version("main", branch="main")
     version("experimental", branch="experimental")

  Branches are moving targets, which means the commit you get when you install the package likely won't be the one used when the package was first written.

  .. note::

     Common branch names are special in terms of how Spack determines the latest version of a package.
     See "infinity versions" in :ref:`version ordering <version-comparison>` for more information.

  .. warning::

    This download method is **untrusted**, and is **not recommended** for production installations.


.. _git-tags:

Tags
  To fetch from a particular tag, use ``tag`` instead:

  .. code-block:: python

     version("1.0.1", tag="v1.0.1")

  While tags are generally more stable than branches, Git allows tags to be moved.
  Many developers use tags to denote rolling releases, and may move the tag when a bug is fixed.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.

    If you must use a ``tag``, it is recommended to combine it with the ``commit`` option (see :ref:`below <git-commits>`).


.. _git-commits:

Commits
  To fetch a particular commit, use the ``commit`` argument:

  .. code-block:: python

     version("2014-10-08", commit="1e6ef73d93a28240f954513bc4c2ed46178fa32b")
     version("1.0.4", tag="v1.0.4", commit="420136f6f1f26050d95138e27cf8bc905bc5e7f52")   

  It may be useful to provide a saner version for commits like this, e.g., you might use the date as the version, as done in the first example above.
  Or, if you know the commit at which a release was cut, you can use the release version.
  It is up to the package author to decide which of these options makes the most sense.

  .. warning::

    A git download is *trusted only if* the **full commit sha** is specified.


  .. hint::

     **Avoid using the commit hash as the version.**
     It is not recommended to use the commit hash as the version itself, since it won't sort properly for :ref:`version ordering <version-comparison>` purposes.


.. _git-submodules:

Submodules
  You can supply ``submodules=True`` to cause Spack to fetch submodules recursively along with the repository.

  .. code-block:: python

     version("1.1.0", commit="907d5f40d653a73955387067799913397807adf3", submodules=True)

  If a package needs more fine-grained control over submodules, define ``submodules`` to be a callable function that takes the package instance as its only argument.
  The function needs to return a list of submodules to be fetched.

  .. code-block:: python

     def submodules(package):
         submodules = []
         if "+variant-1" in package.spec:
             submodules.append("submodule_for_variant_1")
         if "+variant-2" in package.spec:
             submodules.append("submodule_for_variant_2")
         return submodules


      class MyPackage(Package):
          version("1.1.0", commit="907d5f40d653a73955387067799913397807adf3", submodules=submodules)

  For more information about git submodules see the man page of git: ``man git-submodule``.


.. _git-sparse-checkout:

Sparse-Checkout
  If you only want to clone a subset of the contents of a git repository, you can supply ``git_sparse_paths`` at the package or version level to utilize git's sparse-checkout feature.
  The paths can be specified through an attribute, property or callable function.
  This option is useful for large repositories containing separate features that can be built independently.

  .. note::

     This leverages a newer feature in git that requires version ``2.25.0`` or greater.

     If ``git_sparse_paths`` is supplied to a git version that is too old then a warning will be issued before standard cloning operations are performed.

  .. note::

     Paths to directories result in the cloning of *all* of their contents, including the contents of their subdirectories.

  The ``git_sparse_paths`` attribute needs to provide a list of relative paths within the repository.
  If using a property -- a function decorated with ``@property`` -- or an argument that is a callable function, the function needs to return a list of paths.

  For example, using the attribute approach:

  .. code-block:: python

    class MyPackage(package):
        # using an attribute
        git_sparse_paths = ["doe", "rae"]

        version("1.0.0")
        version("1.1.0")

  results in the files from the top level directory of the repository and the contents of the ``doe`` and ``rae`` relative paths within the repository to be cloned.

  Alternatively, you can provide the paths to the version directive argument using a callable function whose return value is a list for paths.
  For example:

  .. code-block:: python

    def sparse_path_function(package)
        paths = ["doe", "rae", "me/file.cpp"]
        if package.spec.version >  Version("1.2.0"):
            paths.extend(["fae"])
        return paths

    class MyPackage(package):
        version("1.1.5", git_sparse_paths=sparse_path_function)
        version("1.2.0", git_sparse_paths=sparse_path_function)
        version("1.2.5", git_sparse_paths=sparse_path_function)
        version("1.1.5", git_sparse_paths=sparse_path_function)

  results in the cloning of the files from the top level directory of the repository, the contents of the ``doe`` and ``rae`` relative paths, *and* the ``me/file.cpp`` file.
  If the package version is greater than ``1.2.0`` then the contents of the ``fae`` relative path will also be cloned.

  .. note::

     The version directives in the examples above are simplified to emphasize use of this feature.
     Trusted downloads require a hash, such as a :ref:`sha256 <github-fetch>` or :ref:`commit <git-commits>`.


.. _github-fetch:

GitHub
""""""

If a project is hosted on GitHub, *any* valid Git branch, tag, or hash may be downloaded as a tarball.
This is accomplished simply by constructing an appropriate URL.
Spack can checksum any package downloaded this way, thereby producing a trusted download.
For example, the following downloads a particular hash, and then applies a checksum.

.. code-block:: python

       version(
           "1.9.5.1.1",
           sha256="8d74beec1be996322ad76813bafb92d40839895d6dd7ee808b17ca201eac98be",
           url="https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f",
       )

Alternatively, you could provide the GitHub ``url`` for one version as a property and Spack will extrapolate the URL for other versions as described in :ref:`Versions and URLs <versions-and-fetching>`.


.. _hg-fetch:

Mercurial
"""""""""

Fetching with Mercurial works much like `Git <git-fetch>`_, but you use the ``hg`` parameter.
The destination directory is still the standard stage source path.

.. _hg-default-branch:

Default branch
  Add the ``hg`` attribute with no ``revision`` passed to ``version``:

  .. code-block:: python

     class Example(Package):

         hg = "https://bitbucket.org/example-project/example"

         version("develop")

  As with Git's default fetching strategy, there is no way to verify the integrity of the download.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.


.. _hg-revisions:

Revisions
  To fetch a particular revision, use the ``revision`` parameter:

  .. code-block:: python

     version("1.0", revision="v1.0")

  Unlike ``git``, which has special parameters for different types of revisions, you can use ``revision`` for branches, tags, and **commits** when you fetch with Mercurial.

  .. warning::

    Like Git, fetching specific branches or tags is an **untrusted** download method, and is **not recommended**.

    The recommended fetch strategy is to specify a particular commit hash as the revision.


.. _svn-fetch:

Subversion
""""""""""

To fetch with subversion, use the ``svn`` and ``revision`` parameters.
The destination directory will be the standard stage source path.

Fetching the head
  Simply add an ``svn`` parameter to the package:

  .. code-block:: python

     class Example(Package):

         svn = "https://outreach.scidac.gov/svn/example/trunk"

         version("develop")

  .. warning::

    This download method is **untrusted**, and is **not recommended** for the same reasons as mentioned above.


.. _svn-revisions:

Fetching a revision
  To fetch a particular revision, add a ``revision`` argument to the version directive:

  .. code-block:: python

     version("develop", revision=128)

  Unfortunately, Subversion has no commit hashing scheme like Git and Mercurial do, so there is no way to guarantee that the download you get is the same as the download used when the package was created.
  Use at your own risk.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.


Subversion branches are handled as part of the directory structure, so you can check out a branch or tag by changing the URL.
If you want to package multiple branches, simply add a ``svn`` argument to each version directive.


.. _cvs-fetch:

CVS
"""""""

CVS (Concurrent Versions System) is an old centralized version control system.
It is a predecessor of Subversion.

To fetch with CVS, use the ``cvs``, branch, and ``date`` parameters.
The destination directory will be the standard stage source path.

.. _cvs-head:

Fetching the head
  Simply add a ``cvs`` parameter to the package:

  .. code-block:: python

     class Example(Package):

         cvs = ":pserver:outreach.scidac.gov/cvsroot%module=modulename"

         version("1.1.2.4")

  CVS repository locations are described using an older syntax that is different from today's ubiquitous URL syntax.
  ``:pserver:`` denotes the transport method.
  CVS servers can host multiple repositories (called "modules") at the same location, and one needs to specify both the server location and the module name to access.
  Spack combines both into one string using the ``%module=modulename`` suffix shown above.

  .. warning::

    This download method is **untrusted**.


.. _cvs-date:

Fetching a date
  Versions in CVS are commonly specified by date.
  To fetch a particular branch or date, add a ``branch`` and/or ``date`` argument to the version directive:

  .. code-block:: python

     version("2021.4.22", branch="branchname", date="2021-04-22")

  Unfortunately, CVS does not identify repository-wide commits via a revision or hash like Subversion, Git, or Mercurial do.
  This makes it impossible to specify an exact commit to check out.

  .. warning::

    This download method is **untrusted**.


CVS has more features, but since CVS is rarely used these days, Spack does not support all of them.

Sources that are not archives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack normally expands archives (e.g., ``*.tar.gz`` and ``*.zip``) automatically into a standard stage source directory (``self.stage.source_path``) after downloading them.
If you want to skip this step (e.g., for self-extracting executables and other custom archive types), you can add ``expand=False`` to a ``version`` directive.

.. code-block:: python

   version(
       "8.2.1",
       sha256="a2bbdb2de53523b8099b37013f251546f3d65dbe7a0774fa41af0a4176992fd4",
       url="http://example.com/foo-8.2.1-special-version.sh",
       expand=False,
   )

When ``expand`` is set to ``False``, Spack sets the current working directory to the directory containing the downloaded archive before it calls your ``install`` method.
Within ``install``, the path to the downloaded archive is available as ``self.stage.archive_file``.

Here is an example snippet for packages distributed as self-extracting archives.
The example sets permissions on the downloaded file to make it executable, then runs it with some arguments.

.. code-block:: python

   def install(self, spec, prefix):
       set_executable(self.stage.archive_file)
       installer = Executable(self.stage.archive_file)
       installer("--prefix=%s" % prefix, "arg1", "arg2", "etc.")


Extra Resources
^^^^^^^^^^^^^^^

Some packages (most notably compilers) provide optional features if additional resources are expanded within their source tree before building.
In Spack it is possible to describe such a need with the ``resource`` directive:

.. code-block:: python

   resource(
      name="cargo",
      git="https://github.com/rust-lang/cargo.git",
      tag="0.10.0",
      destination="cargo",
   )

The arguments are similar to those of the ``versions`` directive.
The keyword ``destination`` is relative to the source root of the package and should point to where the resource is to be expanded.

Download caching
^^^^^^^^^^^^^^^^

Spack maintains a cache (described :ref:`here <caching>`) which saves files retrieved during package installations to avoid re-downloading in the case that a package is installed with a different specification (but the same version) or reinstalled on account of a change in the hashing scheme.
In rare cases, it may be necessary to avoid caching for a particular version by adding ``no_cache=True`` as an option to the ``version()`` directive.
Example situations would be a "snapshot"-like Version Control System (VCS) tag, a VCS branch such as ``v6-16-00-patches``, or a URL specifying a regularly updated snapshot tarball.


.. _version_constraints:

Specifying version constraints
------------------------------

Many Spack directives allow limiting versions to support features such as :ref:`backward and forward compatibility <version_compatibility>`.
These constraints on :ref:`package specs <sec-specs>` are defined using the ``@<specifier>`` syntax.
(See :ref:`version-specifier` for more information.)

For example, the following:

.. code-block:: python

   depends_on("foo")
   depends_on("python@3")

   conflicts("^foo@1.2.3:", when="@:4.5")

illustrates, in order, three of four forms of version range constraints: implicit, lower bound and upper bound.
The fourth form provides lower *and* upper bounds on the version.

In this example, the implicit range is used to indicate that the package :ref:`depends on <dependencies>` *any* ``python`` *with* ``3`` *as the major version number* (e.g., ``3.13.5``).
The other two range constraints are shown in the :ref:`conflict <packaging_conflicts>` with the dependency package ``foo``.
The conflict with ``foo`` *at version* ``1.2.3`` *or newer* is **triggered** for builds of the package at *any version up to and including* ``4.5``.
For an example of the fourth form, suppose the dependency in this example had been ``python@3.6:3``.
In this case, the package would depend on *any version of* ``python`` *from* ``3.6`` *on so long as the major version number is* ``3``.

While you can constrain the spec to a single version -- using the ``@=<version>`` form of ``specifier`` -- **ranges are preferred** even if they would only match a single version currently defined in the package.
Using ranges helps avoid overly constrained dependencies, patches, and conflicts.
They also come in handy when, for example, users define versions in :ref:`packages-config` that include custom suffixes.
For example, if the package defines the version ``1.2.3``, we know from :ref:`version-comparison`, that a user-defined version ``1.2.3-custom`` will satisfy the version constraint ``@1.2.3``.

.. warning::

   Specific ``@=`` versions should only be used in **exceptional cases**, such as when the package has a versioning scheme that omits the zero in the first patch release.
   For example, suppose a package defines versions: ``3.1``, ``3.1.1`` and ``3.1.2``.
   Then the specifier ``@=3.1`` is the correct way to select only ``3.1``, whereas ``@3.1`` would be satisfied by all three versions.


.. _variants:

Variants
--------

Many software packages can be configured to enable optional features, which often come at the expense of additional dependencies or longer build times.
To be flexible enough and support a wide variety of use cases, Spack allows you to expose to the end-user the ability to choose which features should be activated in a package at the time it is installed.
The mechanism to be employed is the :py:func:`~spack.package.variant` directive.

Boolean variants
^^^^^^^^^^^^^^^^

In their simplest form, variants are boolean options specified at the package level:

.. code-block:: python

  class Hdf5(AutotoolsPackage):
      ...
      variant("shared", default=True, description="Builds a shared version of the library")

with a default value and a description of their meaning in the package.

With this variant defined, users can now run ``spack install hdf5 +shared`` and ``spack install hdf5 ~shared`` to enable or disable the ``shared`` feature, respectively.
See also the :ref:`basic-variants` for the spec syntax of variants.

Of course, merely defining a variant in a package does not automatically enable or disable any features in the build system.
As a packager, you are responsible for translating variants to build system flags or environment variables, to influence the build process.
We will see this in action in the next part of the packaging guide, where we talk about :ref:`configuring the build with spec objects <spec-objects>`.

Other than influencing the build process, variants are often used to specify optional :ref:`dependencies of a package <dependencies>`.
For example, a package may depend on another package only if a certain variant is enabled:

..  code-block:: python

  class Hdf5(AutotoolsPackage):
      ...
      variant("szip", default=False, description="Enable szip support")
      depends_on("szip", when="+szip")

In this case, ``szip`` is modeled as an optional dependency of ``hdf5``, and users can run ``spack install hdf5 +szip`` to enable it.

Single-valued variants
^^^^^^^^^^^^^^^^^^^^^^

Other than boolean variants, Spack supports single- and multi-valued variants that can take one or more *string* values.

To define a *single-valued* variant, simply pass a tuple of possible values to the ``variant`` directive, together with ``multi=False``:

.. code-block:: python

  class Blis(Package):
      ...
      variant(
          "threads",
          default="none",
          values=("pthreads", "openmp", "none"),
          multi=False,
          description="Multithreading support",
      )

This allows users to ``spack install blis threads=openmp``.

In the example above the argument ``multi=False`` indicates that only a **single value** can be selected at a time.
This constraint is enforced by the solver, and an error is emitted if a user specifies two or more values at the same time:

.. code-block:: spec

  $ spack spec blis threads=openmp,pthreads
  Input spec
  --------------------------------
  blis threads=openmp,pthreads

  Concretized
  --------------------------------
  ==> Error: multiple values are not allowed for variant "threads"

.. hint::

   In the example above, the value ``threads=none`` is a variant value like any other, and means that *no value is selected*.
   In Spack, all variants have to have a value, so ``none`` was chosen as a *convention* to indicate that no value is selected.

Multi-valued variants
^^^^^^^^^^^^^^^^^^^^^

Like single-valued variants, multi-valued variants take one or more *string* values, but allow users to select multiple values at the same time.

To define a *multi-valued* variant, simply pass ``multi=True`` instead:

.. code-block:: python

  class Gcc(AutotoolsPackage):
      ...
      variant(
          "languages",
          default="c,c++,fortran",
          values=("ada", "brig", "c", "c++", "fortran", "objc"),
          multi=True,
          description="Compilers and runtime libraries to build",
      )

This allows users to run ``spack install languages=c,c++`` where the values are separated by commas.


Advanced validation of multi-valued variants
""""""""""""""""""""""""""""""""""""""""""""

As noted above, the value ``none`` is a value like any other, which raises the question: what if a variant allows multiple values to be selected, *or* none at all?
Naively, one might think that this can be achieved by simply creating a multi-valued variant that includes the value ``none``:

.. code-block:: python

   class Adios(AutotoolsPackage):
       ...
       variant(
           "staging",
           values=("dataspaces", "flexpath", "none"),
           multi=True,
           description="Enable dataspaces and/or flexpath staging transports",
       )

but this does not prevent users from selecting the non-sensical option ``staging=dataspaces,none``.

In these cases, more advanced validation logic is required to prevent ``none`` from being selected along with any other value.
Spack provides two validator functions to help with this, which can be passed to the ``values=`` argument of the ``variant`` directive.

The first validator function is :py:func:`~spack.package.any_combination_of`, which can be used as follows:

.. code-block:: python

   class Adios(AutotoolsPackage):
       ...
       variant(
           "staging",
           values=any_combination_of("flexpath", "dataspaces"),
           description="Enable dataspaces and/or flexpath staging transports",
       )

This solves the issue by allowing the user to select either any combination of the values ``flexpath`` and ``dataspaces``, or ``none``.
In other words, users can specify ``staging=none`` to select nothing, or any of ``staging=dataspaces``, ``staging=flexpath``, and ``staging=dataspaces,flexpath``.

The second validator function :py:func:`~spack.package.disjoint_sets` generalizes this idea further:

.. code-block:: python

   class Mvapich2(AutotoolsPackage):
       ...
       variant(
           "process_managers",
           description="List of the process managers to activate",
           values=disjoint_sets(("auto",), ("slurm",), ("hydra", "gforker", "remshell"))
           .prohibit_empty_set()
           .with_error("'slurm' or 'auto' cannot be activated along with other process managers")
           .with_default("auto")
           .with_non_feature_values("auto"),
       )

In this case, examples of valid options are ``process_managers=auto``, ``process_managers=slurm``, and ``process_managers=hydra,remshell``, whereas ``process_managers=slurm,hydra`` is invalid, as it picks values from two different sets.

Both validator functions return a :py:class:`~spack.variant.DisjointSetsOfValues` object, which defines chaining methods to further customize the behavior of the variant.

Conditional Possible Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are cases where a variant may take multiple values, and the list of allowed values expands over time.
Consider, for instance, the C++ standard with which we might compile Boost, which can take one of multiple possible values with the latest standards only available for more recent versions.

To model a similar situation we can use *conditional possible values* in the variant declaration:

.. code-block:: python

   variant(
       "cxxstd",
       default="98",
       values=(
           "98",
           "11",
           "14",
           # C++17 is not supported by Boost < 1.63.0.
           conditional("17", when="@1.63.0:"),
           # C++20/2a is not supported by Boost < 1.73.0
           conditional("2a", "2b", when="@1.73.0:"),
       ),
       multi=False,
       description="Use the specified C++ standard when building.",
   )


The snippet above allows ``98``, ``11`` and ``14`` as unconditional possible values for the ``cxxstd`` variant, while ``17`` requires a version greater or equal to ``1.63.0`` and both ``2a`` and ``2b`` require a version greater or equal to ``1.73.0``.


Conditional Variants
^^^^^^^^^^^^^^^^^^^^

As new versions of packages are released, optional features may be added and removed.
Sometimes, features are only available for a particular platform or architecture.

To reduce the visual clutter in specs, packages can define variants *conditionally* using a ``when`` clause.
The variant will only be present on specs that satisfy this condition.

For example, the following package defines a variant ``bar`` that exists only when it is at version 2.0 or higher, and a variant ``baz`` that exists only on the Darwin platform:

.. code-block:: python

   class Foo(Package):
       ...
       variant("bar", default=False, when="@2.0:", ...)
       variant("baz", default=True, when="platform=darwin", ...)

Do note that conditional variants can also be a source of confusion.
In Spack, the absence of a variant is different from it being disabled.
For example, a user might run ``spack install foo ~bar``, expecting it to allow version 1.0 (which does not have the ``bar`` feature) and version 2.0 (with the feature disabled).
However, the constraint ``~bar`` tells Spack that the ``bar`` variant *must exist* and be disabled.
This forces Spack to select version 2.0 or higher, where the variant is defined.

Sticky Variants
^^^^^^^^^^^^^^^

The variant directive can be marked as ``sticky`` by setting the corresponding argument to ``True``:

.. code-block:: python

   variant("bar", default=False, sticky=True)

A ``sticky`` variant differs from a regular one in that it is always set to either:

#. An explicit value appearing in a spec literal or
#. Its default value

The concretizer thus is not free to pick an alternate value to work around conflicts, but will error out instead.
Setting this property on a variant is useful in cases where the variant allows some dangerous or controversial options (e.g., using unsupported versions of a compiler for a library) and the packager wants to ensure that allowing these options is done on purpose by the user, rather than automatically by the solver.


Overriding Variants
^^^^^^^^^^^^^^^^^^^

Packages may override variants for several reasons, most often to change the default from a variant defined in a parent class or to change the conditions under which a variant is present on the spec.

When a variant is defined multiple times, whether in the same package file or in a subclass and a superclass, the last definition is used for all attributes **except** for the ``when`` clauses.
The ``when`` clauses are accumulated through all invocations, and the variant is present on the spec if any of the accumulated conditions are satisfied.

For example, consider the following package:

.. code-block:: python

   class Foo(Package):
       ...
       variant("bar", default=False, when="@1.0", description="help1")
       variant("bar", default=True, when="platform=darwin", description="help2")
       ...

This package ``foo`` has a variant ``bar`` when the spec satisfies either ``@1.0`` or ``platform=darwin``, but not for other platforms at other versions.
The default for this variant, when it is present, is always ``True``, regardless of which condition of the variant is satisfied.
This allows packages to override variants in packages or build system classes from which they inherit, by modifying the variant values without modifying the ``when`` clause.
It also allows a package to implement ``or`` semantics for a variant ``when`` clause by duplicating the variant definition.

.. _dependencies:

Dependencies
------------

We've covered how to build a simple package, but what if one package relies on another package to build?
How do you express that in a package file?
And how do you refer to the other package in the build script for your own package?

Spack makes this relatively easy.
Let's take a look at the ``libdwarf`` package to see how it's done:

.. code-block:: python
   :emphasize-lines: 9
   :linenos:

   class Libdwarf(Package):
       homepage = "http://www.prevanders.net/dwarf.html"
       url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
       list_url = homepage

       version("20130729", sha256="092fcfbbcfca3b5be7ae1b5e58538e92c35ab273ae13664fed0d67484c8e78a6")
       ...

       depends_on("libelf")

       def install(self, spec, prefix):
           ...

``depends_on()``
^^^^^^^^^^^^^^^^

The highlighted ``depends_on("libelf")`` call tells Spack that it needs to build and install the ``libelf`` package before it builds ``libdwarf``.
This means that in your ``install()`` method, you are guaranteed that ``libelf`` has been built and installed successfully, so you can rely on it for your libdwarf build.

.. _dependency_specs:

Dependency specs
^^^^^^^^^^^^^^^^

``depends_on`` doesn't just take the name of another package.
It can take a full spec as well.
This means that you can restrict the versions or other configuration options of ``libelf`` that ``libdwarf`` will build with.
For example, suppose that in the ``libdwarf`` package you write:

.. code-block:: python

   depends_on("libelf@0.8")

Now ``libdwarf`` will require ``libelf`` in the range ``0.8``, which includes patch versions ``0.8.1``, ``0.8.2``, etc.
Apart from version restrictions, you can also specify variants if this package requires optional features of the dependency.

.. code-block:: python

   depends_on("libelf@0.8 +parser +pic")

Both users *and* package authors use the same spec syntax to refer to different package configurations.
Users use the spec syntax on the command line to find installed packages or to install packages with particular constraints, and package authors can use specs to describe relationships between packages.

.. _version_compatibility:

Specifying backward and forward compatibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages are often compatible with a range of versions of their dependencies.
This is typically referred to as backward and forward compatibility.
Spack allows you to specify this in the ``depends_on`` directive using version ranges.

**Backward compatibility** means that the package requires at least a certain version of its dependency:

.. code-block:: python

   depends_on("python@3.10:")

In this case, the package requires Python 3.10 or newer.

Commonly, packages drop support for older versions of a dependency as they release new versions.
In Spack you can conveniently add every backward compatibility rule as a separate line:

.. code-block:: python

   # backward compatibility with Python
   depends_on("python@3.8:")
   depends_on("python@3.9:", when="@1.2:")
   depends_on("python@3.10:", when="@1.4:")

This means that in general we need Python 3.8 or newer; from version 1.2 onwards we need Python 3.9 or newer; from version 1.4 onwards we need Python 3.10 or newer.
Notice that it's fine to have overlapping ranges in the ``when`` clauses.

**Forward compatibility** means that the package requires at most a certain version of its dependency.
Forward compatibility rules are necessary when there are breaking changes in the dependency that the package cannot handle.
In Spack we often add forward compatibility bounds only at the time a new, breaking version of a dependency is released.
As with backward compatibility, it is typical to see a list of forward compatibility bounds in a package file as separate lines:

.. code-block:: python

   # forward compatibility with Python
   depends_on("python@:3.12", when="@:1.10")
   depends_on("python@:3.13", when="@:1.12")

Notice how the ``:`` now appears before the version number both in the dependency and in the ``when`` clause.
This tells Spack that in general we need Python 3.13 or older up to version ``1.12.x``, and up to version ``1.10.x`` we need Python 3.12 or older.
Said differently, forward compatibility with Python 3.13 was added in version 1.11, while version 1.13 added forward compatibility with Python 3.14.

Notice that a version range ``@:3.12`` includes *any* patch version number ``3.12.x``, which is often useful when specifying forward compatibility bounds.

So far we have seen open-ended version ranges, which is by far the most common use case.
It is also possible to specify both a lower and an upper bound on the version of a dependency, like this:

.. code-block:: python

   depends_on("python@3.10:3.12")

There is short syntax to specify that a package is compatible with say any ``3.x`` version:

.. code-block:: python

   depends_on("python@3")

The above is equivalent to ``depends_on("python@3:3")``, which means at least Python version 3 and at most any version ``3.x.y``.

In very rare cases, you may need to specify an exact version, for example if you need to distinguish between ``3.2`` and ``3.2.1``:

.. code-block:: python

   depends_on("pkg@=3.2")

But in general, you should try to use version ranges as much as possible, so that custom suffixes are included too.
The above example can be rewritten in terms of ranges as follows:

.. code-block:: python

   depends_on("pkg@3.2:3.2.0")

A spec can contain a version list of ranges and individual versions separated by commas.
For example, if you need Boost 1.59.0 or newer, but there are known issues with 1.64.0, 1.65.0, and 1.66.0, you can say:

.. code-block:: python

   depends_on("boost@1.59.0:1.63,1.65.1,1.67.0:")


.. _dependency-types:

Dependency types
^^^^^^^^^^^^^^^^

Not all dependencies are created equal, and Spack allows you to specify exactly what kind of a dependency you need.
For example:

.. code-block:: python

   depends_on("cmake", type="build")
   depends_on("py-numpy", type=("build", "run"))
   depends_on("libelf", type=("build", "link"))
   depends_on("py-pytest", type="test")

The following dependency types are available:

* **build**: the dependency will be added to the ``PATH`` and ``PYTHONPATH`` at build-time.
* **link**: the dependency will be added to Spack's compiler wrappers, automatically injecting the appropriate linker flags, including ``-I``, ``-L``, and RPATH/RUNPATH handling.
* **run**: the dependency will be added to the ``PATH`` and ``PYTHONPATH`` at run-time.
  This is true for both ``spack load`` and the module files Spack writes.
* **test**: the dependency will be added to the ``PATH`` and ``PYTHONPATH`` at build-time.
  The only difference between "build" and "test" is that test dependencies are only built if the user requests unit tests with ``spack install --test``.

One of the advantages of the ``build`` dependency type is that although the dependency needs to be installed in order for the package to be built, it can be uninstalled without concern afterwards.
``link`` and ``run`` disallow this because uninstalling the dependency would break the package.

``build``, ``link``, and ``run`` dependencies all affect the hash of Spack packages (along with ``sha256`` sums of patches and archives used to build the package, and a `canonical hash <https://github.com/spack/spack/pull/28156>`_ of the ``package.py`` recipes).
``test`` dependencies do not affect the package hash, as they are only used to construct a test environment *after* building and installing a given package installation.
Older versions of Spack did not include build dependencies in the hash, but this has been `fixed <https://github.com/spack/spack/pull/28504>`_ as of |Spack v0.18|_.

.. |Spack v0.18| replace:: Spack ``v0.18``
.. _Spack v0.18: https://github.com/spack/spack/releases/tag/v0.18.0

If the dependency type is not specified, Spack uses a default of ``("build", "link")``.
This is the common case for compiler languages.
Non-compiled packages like Python modules commonly use ``("build", "run")``.
This means that the compiler wrappers don't need to inject the dependency's ``prefix/lib`` directory, but the package needs to be in ``PATH`` and ``PYTHONPATH`` during the build process and later when a user wants to run the package.

Conditional dependencies
^^^^^^^^^^^^^^^^^^^^^^^^

You may have a package that only requires a dependency under certain conditions.
For example, you may have a package with optional MPI support.
You would then provide a variant to reflect that the feature is optional and specify the MPI dependency only applies when MPI support is enabled.
In that case, you could say something like:

.. code-block:: python

   variant("mpi", default=False, description="Enable MPI support")

   depends_on("mpi", when="+mpi")


Suppose that, starting from version 3, the above package also has optional `Trilinos` support.
Furthermore, you want to ensure that when `Trilinos` support is enabled, the package can be built both with and without MPI.
Further suppose you require a version of `Trilinos` no older than 12.6.
In that case, the `trilinos` variant and dependency directives would be:

.. code-block:: python

   variant("trilinos", default=False, description="Enable Trilinos support")

   depends_on("trilinos@12.6:", when="@3: +trilinos")
   depends_on("trilinos@12.6: +mpi", when="@3: +trilinos +mpi")


Alternatively, you could use the `when` context manager to equivalently specify the `trilinos` variant dependencies as follows:

.. code-block:: python

   with when("@3: +trilinos"):
       depends_on("trilinos@12.6:")
       depends_on("trilinos +mpi", when="+mpi")


The argument to ``when`` in either case can include any Spec constraints that are supported on the command line using the same :ref:`syntax <sec-specs>`.

.. note::

   If a dependency isn't typically used, you can save time by making it conditional since Spack will not build the dependency unless it is required for the Spec.


.. _dependency_dependency_patching:

Dependency patching
^^^^^^^^^^^^^^^^^^^

Some packages maintain special patches on their dependencies, either to add new features or to fix bugs.
This typically makes a package harder to maintain, and we encourage developers to upstream (contribute back) their changes rather than maintaining patches.
However, in some cases it's not possible to upstream.
Maybe the dependency's developers don't accept changes, or maybe they just haven't had time to integrate them.

For times like these, Spack's ``depends_on`` directive can optionally take a patch or list of patches:

.. code-block:: python

    class SpecialTool(Package):
        ...
        depends_on("binutils", patches="special-binutils-feature.patch")
        ...

Here, the ``special-tool`` package requires a special feature in ``binutils``, so it provides an extra ``patches=<filename>`` keyword argument.
This is similar to the `patch directive <patching_>`_, with one small difference.
Here, ``special-tool`` is responsible for the patch, so it should live in ``special-tool``'s directory in the package repository, not the ``binutils`` directory.

If you need something more sophisticated than this, you can simply nest a ``patch()`` directive inside of ``depends_on``:

.. code-block:: python

    class SpecialTool(Package):
        ...
        depends_on(
            "binutils",
            patches=patch("special-binutils-feature.patch",
                          level=3,
                          when="@:1.3"),   # condition on binutils
            when="@2.0:")                  # condition on special-tool
        ...

Note that there are two optional ``when`` conditions here -- one on the ``patch`` directive and the other on ``depends_on``.
The condition in the ``patch`` directive applies to ``binutils`` (the package being patched), while the condition in ``depends_on`` applies to ``special-tool``.
See `patch directive <patching_>`_ for details on all the arguments the ``patch`` directive can take.

Finally, if you need *multiple* patches on a dependency, you can provide a list for ``patches``, e.g.:

.. code-block:: python

    class SpecialTool(Package):
        ...
        depends_on(
            "binutils",
            patches=[
                "binutils-bugfix1.patch",
                "binutils-bugfix2.patch",
                patch("https://example.com/special-binutils-feature.patch",
                      sha256="252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866",
                      when="@:1.3")],
            when="@2.0:")
        ...

As with ``patch`` directives, patches are applied in the order they appear in the package file (or in this case, in the list).

.. note::

   You may wonder whether dependency patching will interfere with other packages that depend on ``binutils``.
   It won't.

   As described in :ref:`patching`, Patching a package adds the ``sha256`` of the patch to the package's spec, which means it will have a *different* unique hash than other versions without the patch.
   The patched version coexists with unpatched versions, and Spack's support for :ref:`handling_rpaths` guarantees that each installation finds the right version.
   If two packages depend on ``binutils`` patched *the same* way, they can both use a single installation of ``binutils``.

.. _virtual-dependencies:

Virtual dependencies
--------------------

In some cases, more than one package can satisfy another package's dependency.
One way this can happen is if a package depends on a particular *interface*, but there are multiple *implementations* of the interface, and the package could be built with any of them.
A *very* common interface in HPC is the `Message Passing Interface (MPI) <http://www.mcs.anl.gov/research/projects/mpi/>`_, which is used in many large-scale parallel applications.

MPI has several different implementations (e.g., `MPICH <http://www.mpich.org>`_, `OpenMPI <http://www.open-mpi.org>`_, and `MVAPICH <http://mvapich.cse.ohio-state.edu>`_) and scientific applications can be built with any one of them.
Many package managers handle interfaces like this by requiring many variations of the package recipe for each implementation of MPI, e.g., ``foo``, ``foo-mvapich``, ``foo-mpich``.
In Spack every package is defined in a single ``package.py`` file, and avoids the combinatorial explosion through *virtual dependencies*.

``provides``
^^^^^^^^^^^^

In Spack, ``mpi`` is handled as a *virtual package*.
A package like ``mpileaks`` can depend on the virtual ``mpi`` just like any other package, by supplying a ``depends_on`` call in the package definition.
For example:

.. code-block:: python
   :linenos:
   :emphasize-lines: 7

   class Mpileaks(Package):
       homepage = "https://github.com/hpc/mpileaks"
       url = "https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

       version("1.0", sha256="768c71d785bf6bbbf8c4d6af6582041f2659027140a962cd0c55b11eddfd5e3d")

       depends_on("mpi")
       depends_on("adept-utils")
       depends_on("callpath")

Here, ``callpath`` and ``adept-utils`` are concrete packages, but there is no actual package for ``mpi``, so we say it is a *virtual* package.
The syntax of ``depends_on`` is the same for both.
If we look inside the package file of an MPI implementation, say MPICH, we'll see something like this:

.. code-block:: python

   class Mpich(Package):
       provides("mpi")
       ...

The ``provides("mpi")`` call tells Spack that the ``mpich`` package can be used to satisfy the dependency of any package that ``depends_on("mpi")``.

Providing multiple virtuals simultaneously
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages can provide more than one virtual dependency.
Sometimes, due to implementation details, there are subsets of those virtuals that need to be provided together by the same package.

A well-known example is ``openblas``, which provides both the ``lapack`` and ``blas`` API in a single ``libopenblas`` library.
A package that needs ``lapack`` and ``blas`` must either use ``openblas`` to provide both, or not use ``openblas`` at all.
It cannot pick one or the other.

To express this constraint in a package, the two virtual dependencies must be listed in the same ``provides`` directive:

.. code-block:: python

   provides("blas", "lapack")

This makes it impossible to select ``openblas`` as a provider for one of the two virtual dependencies and not for the other.
If you try to, Spack will report an error:

.. code-block:: spec

   $ spack spec netlib-scalapack  ^[virtuals=lapack] openblas ^[virtuals=blas] atlas
   ==> Error: concretization failed for the following reasons:

      1. Package 'openblas' needs to provide both 'lapack' and 'blas' together, but provides only 'lapack'

Versioned Interfaces
^^^^^^^^^^^^^^^^^^^^

Just as you can pass a spec to ``depends_on``, so can you pass a spec to ``provides`` to add constraints.
This allows Spack to support the notion of *versioned interfaces*.
The MPI standard has gone through many revisions, each with new functions added, and each revision of the standard has a version number.
Some packages may require a recent implementation that supports MPI-3 functions, but some MPI versions may only provide up to MPI-2.
Others may need MPI 2.1 or higher.
You can indicate this by adding a version constraint to the spec passed to ``provides``:

.. code-block:: python

   provides("mpi@:2")

Suppose that the above ``provides`` call is in the ``mpich2`` package.
This says that ``mpich2`` provides MPI support *up to* version 2, but if a package ``depends_on("mpi@3")``, then Spack will *not* build that package with ``mpich2``.

Currently, names and versions are the only spec components supported for virtual packages.

``provides when``
^^^^^^^^^^^^^^^^^

The same package may provide different versions of an interface depending on *its* version.
Above, we simplified the ``provides`` call in ``mpich`` to make the explanation easier.
In reality, this is how ``mpich`` calls ``provides``:

.. code-block:: python

   provides("mpi@:3", when="@3:")
   provides("mpi@:1", when="@1:")

The ``when`` argument to ``provides`` allows you to specify optional constraints on the *providing* package, or the *provider*.
The provider only provides the declared virtual spec when *it* matches the constraints in the ``when`` clause.
Here, when ``mpich`` is at version 3 or higher, it provides MPI up to version 3.
When ``mpich`` is at version 1 or higher, it provides the MPI virtual package at version 1.

The ``when`` qualifier ensures that Spack selects a suitably high version of ``mpich`` to satisfy some other package that ``depends_on`` a particular version of MPI.
It will also prevent a user from building with too low a version of ``mpich``.
For example, suppose the package ``foo`` declares this:

.. code-block:: python

   class Foo(Package):
       ...
       depends_on("mpi@2")

Suppose a user invokes ``spack install`` like this:

.. code-block:: spec

   $ spack install foo ^mpich@1.0

Spack will fail with a constraint violation, because the version of MPICH requested is too low for the ``mpi`` requirement in ``foo``.

.. _language-dependencies:

Language and compiler dependencies
----------------------------------

Whenever you use ``spack create`` to create a new package, Spack scans the package's source code and heuristically adds *language dependencies*, which look like this:

.. code-block:: python

   depends_on("c", type="build")
   depends_on("cxx", type="build")
   depends_on("fortran", type="build")

The languages ``c``, ``cxx`` and ``fortran`` are **virtuals provided by compiler packages**, such as ``gcc``, ``llvm``, or ``intel-oneapi-compilers``.

When you concretize a package that depends on ``c``, Spack will select a compiler for it that provides the ``c`` virtual package.

Typically one compiler will be used to provide all languages, but Spack is allowed to create a mixed toolchain.
For example, the ``c`` compiler could be ``clang`` from the ``llvm`` package, whereas the ``fortran`` compiler could be ``gfortran`` from the ``gcc``.
This means that language dependencies translate to one or more compiler packages as build dependencies.


.. _packaging_conflicts:

Conflicts
---------

Sometimes packages have known bugs, or limitations, that would prevent them from concretizing or building usable software.
Spack makes it possible to express such constraints with the ``conflicts`` directive, which takes a spec that is known to cause a conflict and optional ``when`` and ``msg`` arguments.

The ``when`` argument is a spec that triggers the conflict.

The ``msg`` argument allows you to provide a custom error message that Spack prints when the spec to be installed satisfies the conflict spec and ``when`` trigger.

Adding the following to a package:

.. code-block:: python

    conflicts(
        "%intel-oneapi-compilers@:2024",
         when="@:1.2",
         msg="known bug when using Intel oneAPI compilers through v2024",
    )

expresses that the current package *cannot be built* with Intel oneAPI compilers *up through any version* ``2024`` *when trying to install the package with a version up to* ``1.2``.

If the ``when`` argument is omitted, then the conflict is *always triggered* for specs satisfying the conflict spec.
For example,

.. code-block:: python

   conflicts("+cuda+rocm", msg="Cannot build with both cuda and rocm enabled")

means the package cannot be installed with both variants enabled.

Similarly, a conflict can be based on where the build is being performed.
For example,

.. code-block:: python

   for os in ["ventura", "monterey", "bigsur"]:
       conflicts(f"platform=darwin os={os}", msg=f"{os} is not supported")

means the package cannot be built on a Mac running Ventura, Monterey, or Big Sur.

.. note::

   These examples illustrate a few of the types of constraints that can be specified.
   Conflict and ``when`` specs can constrain the compiler, :ref:`version <version_constraints>`, :ref:`variants <basic-variants>`, :ref:`architecture <architecture_specifiers>`, :ref:`dependencies <dependency_specs>`, and more.
   See :ref:`sec-specs` for more information.


.. _packaging_requires:

Requires
--------

Sometimes packages can be built only with specific options.
In those cases the ``requires`` directive can be used.
It allows for complex conditions involving more than a single spec through the ability to specify multiple required specs before keyword arguments.
The same optional ``when`` and ``msg`` arguments as ``conflicts`` are supported (see :ref:`packaging_conflicts`).
The directive also supports a ``policy`` argument for determining how the multiple required specs apply.
Values for ``policy`` may be either ``any_of`` or ``one_of`` (default) and have the same semantics described for their equivalents in :ref:`package-requirements`.

.. hint::

   We recommend that the ``policy`` argument be explicitly specified when multiple specs are used with the directive.

For example, suppose a package can only be built with Apple Clang on Darwin.
This requirement would be specified as:

.. code-block:: python

    requires(
        "%apple-clang",
        when="platform=darwin",
        msg="builds only with Apple Clang compiler on Darwin",
    )

Similarly, suppose a package only builds for the ``x86_64`` target:

.. code-block:: python

    requires("target=x86_64:", msg="package is only available on x86_64")

Or the package must be built with a GCC or Clang that supports C++ 20, which you could ensure by adding the following:

.. code-block:: python

    requires(
        "%gcc@10:", "%clang@16:",
        policy="one_of",
        msg="builds only with a GCC or Clang that support C++ 20",
    )

.. note::

   These examples show only a few of the constraints that can be specified.
   Required and ``when`` specs can constrain the compiler, :ref:`version <version_constraints>`, :ref:`variants <basic-variants>`, :ref:`architecture <architecture_specifiers>`, :ref:`dependencies <dependency_specs>`, and more.
   See :ref:`sec-specs` for more information.


.. _patching:

Patches
-------

Depending on the host architecture, package version, known bugs, or other issues, you may need to patch your software to get it to build correctly.
Like many other package systems, Spack allows you to store patches alongside your package files and apply them to source code after it's downloaded.

``patch``
^^^^^^^^^

You can specify patches in your package file with the ``patch()`` directive.
``patch`` looks like this:

.. code-block:: python

   class Mvapich2(Package):
       ...
       patch("ad_lustre_rwcontig_open_source.patch", when="@1.9:")

The first argument can be either a URL or a filename.
It specifies a patch file that should be applied to your source.
If the patch you supply is a filename, then the patch needs to live within the Spack source tree.
For example, the patch above lives in a directory structure like this:

.. code-block:: none

   spack_repo/builtin/packages/
       mvapich2/
           package.py
           ad_lustre_rwcontig_open_source.patch

If you supply a URL instead of a filename, you need to supply a ``sha256`` checksum, like this:

.. code-block:: python

   patch("http://www.nwchem-sw.org/images/Tddft_mxvec20.patch",
         sha256="252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866")

Spack includes the hashes of patches in its versioning information, so that the same package with different patches applied will have different hash identifiers.
To ensure that the hashing scheme is consistent, you must use a ``sha256`` checksum for the patch.
Patches will be fetched from their URLs, checked, and applied to your source code.
You can use the GNU utils ``sha256sum`` or the macOS ``shasum -a 256`` commands to generate a checksum for a patch file.

Spack can also handle compressed patches.
If you use these, Spack needs a little more help.
Specifically, it needs *two* checksums: the ``sha256`` of the patch and ``archive_sha256`` for the compressed archive.
``archive_sha256`` helps Spack ensure that the downloaded file is not corrupted or malicious, before running it through a tool like ``tar`` or ``zip``.
The ``sha256`` of the patch is still required so that it can be included in specs.
Providing it in the package file ensures that Spack won't have to download and decompress patches it won't end up using at install time.
Both the archive and patch checksum are checked when patch archives are downloaded.

.. code-block:: python

   patch("http://www.nwchem-sw.org/images/Tddft_mxvec20.patch.gz",
         sha256="252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866",
         archive_sha256="4e8092a161ec6c3a1b5253176fcf33ce7ba23ee2ff27c75dbced589dabacd06e")

``patch`` keyword arguments are described below.

``sha256``, ``archive_sha256``
""""""""""""""""""""""""""""""

Hashes of downloaded patch and compressed archive, respectively.
Only needed for patches fetched from URLs.

``when``
""""""""

If supplied, this is a spec that tells Spack when to apply the patch.
If the installed package spec matches this spec, the patch will be applied.
In our example above, the patch is applied when mvapich is at version ``1.9`` or higher.

``level``
"""""""""

This tells Spack how to run the ``patch`` command.
By default, the level is 1 and Spack runs ``patch -p 1``.
If level is 2, Spack will run ``patch -p 2``, and so on.

A lot of people are confused by the level, so here's a primer.
If you look in your patch file, you may see something like this:

.. code-block:: diff
   :linenos:

   --- a/src/mpi/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 12:05:44.806417000 -0800
   +++ b/src/mpi/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 11:53:03.295622000 -0800
   @@ -8,7 +8,7 @@
     *   Copyright (C) 2008 Sun Microsystems, Lustre group
     \*/

   -#define _XOPEN_SOURCE 600
   +//#define _XOPEN_SOURCE 600
    #include <stdlib.h>
    #include <malloc.h>
    #include "ad_lustre.h"

Lines 1-2 show paths with synthetic ``a/`` and ``b/`` prefixes.
These are placeholders for the two ``mvapich2`` source directories that ``diff`` compared when it created the patch file.
This is git's default behavior when creating patch files, but other programs may behave differently.

``-p1`` strips off the first level of the prefix in both paths, allowing the patch to be applied from the root of an expanded mvapich2 archive.
If you set level to ``2``, it would strip off ``src``, and so on.

It's generally easier to just structure your patch file so that it applies cleanly with ``-p1``, but if you're using a patch you didn't create yourself, ``level`` can be handy.

``working_dir``
"""""""""""""""

This tells Spack where to run the ``patch`` command.
By default, the working directory is the source path of the stage (``.``).
However, sometimes patches are made with respect to a subdirectory and this is where the working directory comes in handy.
Internally, the working directory is given to ``patch`` via the ``-d`` option.
Let's take the example patch from above and assume for some reason, it can only be downloaded in the following form:

.. code-block:: diff
   :linenos:

   --- a/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 12:05:44.806417000 -0800
   +++ b/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 11:53:03.295622000 -0800
   @@ -8,7 +8,7 @@
     *   Copyright (C) 2008 Sun Microsystems, Lustre group
     \*/

   -#define _XOPEN_SOURCE 600
   +//#define _XOPEN_SOURCE 600
    #include <stdlib.h>
    #include <malloc.h>
    #include "ad_lustre.h"

Hence, the patch needs to be applied in the ``src/mpi`` subdirectory, and the ``working_dir="src/mpi"`` option would exactly do that.

Patch functions
^^^^^^^^^^^^^^^^^^^^^

In addition to supplying patch files, you can write a custom function to patch a package's source.
For example, the ``py-pyside2`` package contains some custom code for tweaking the way the PySide build handles include files:

.. _pyside-patch:

.. literalinclude:: .spack/spack-packages/repos/spack_repo/builtin/packages/py_pyside2/package.py
   :pyobject: PyPyside2.patch
   :linenos:

A ``patch`` function, if present, will be run after patch files are applied and before ``install()`` is run.

You could put this logic in ``install()``, but putting it in a patch function gives you some benefits.
First, Spack ensures that the ``patch()`` function is run once per code checkout.
That means that if you run install, hit ctrl-C, and run install again, the code in the patch function is only run once.

.. _patch_dependency_patching:

Dependency patching
^^^^^^^^^^^^^^^^^^^

So far we've covered how the ``patch`` directive can be used by a package to patch *its own* source code.
Packages can *also* specify patches to be applied to their dependencies, if they require special modifications.
As with all packages in Spack, a patched dependency library can coexist with other versions of that library.
See the `section on depends_on <dependency_dependency_patching_>`_ for more details.

.. _patch_inspecting_patches:

Inspecting patches
^^^^^^^^^^^^^^^^^^^

If you want to better understand the patches that Spack applies to your packages, you can do that using ``spack spec``, ``spack find``, and other query commands.
Let's look at ``m4``.
If you run ``spack spec m4``, you can see the patches that would be applied to ``m4``:

.. code-block:: spec

   $ spack spec m4
   Input spec
   --------------------------------
   m4
 
   Concretized
   --------------------------------
   m4@1.4.18%apple-clang@9.0.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=darwin-highsierra-x86_64
       ^libsigsegv@2.11%apple-clang@9.0.0 arch=darwin-highsierra-x86_64

You can also see patches that have been applied to installed packages with ``spack find -v``:

.. code-block:: spec

   $ spack find -v m4
   ==> 1 installed package
   -- darwin-highsierra-x86_64 / apple-clang@9.0.0 -----------------
   m4@1.4.18 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv

.. _cmd-spack-resource:

In both cases above, you can see that the patches' sha256 hashes are stored on the spec as a variant.
As mentioned above, this means that you can have multiple, differently-patched versions of a package installed at once.

You can look up a patch by its sha256 hash (or a short version of it) using the ``spack resource show`` command

.. code-block:: console

   $ spack resource show 3877ab54
   3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00
       path:       .../spack_repo/builtin/packages/m4/gnulib-pgi.patch
       applies to: builtin.m4

``spack resource show`` looks up downloadable resources from package files by hash and prints out information about them.
Above, we see that the ``3877ab54`` patch applies to the ``m4`` package.
The output also tells us where to find the patch.

Things get more interesting if you want to know about dependency patches.
For example, when ``dealii`` is built with ``boost@1.68.0``, it has to patch boost to work correctly.
If you didn't know this, you might wonder where the extra boost patches are coming from:

.. code-block:: console

   $ spack spec dealii ^boost@1.68.0 ^hdf5+fortran | grep "\^boost"
       ^boost@1.68.0
           ^boost@1.68.0%apple-clang@9.0.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199,b37164268f34f7133cbc9a4066ae98fda08adf51e1172223f6a969909216870f ~pic+program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave arch=darwin-highsierra-x86_64
   $ spack resource show b37164268
   b37164268f34f7133cbc9a4066ae98fda08adf51e1172223f6a969909216870f
       path:       .../spack_repo/builtin/packages/dealii/boost_1.68.0.patch
       applies to: builtin.boost
       patched by: builtin.dealii

Here you can see that the patch is applied to ``boost`` by ``dealii``, and that it lives in ``dealii``'s directory in Spack's ``builtin`` package repository.

.. _packaging_extensions:

Extensions
----------

Spack's support for package extensions is documented extensively in :ref:`extensions`.
This section documents how to make your own extendable packages and extensions.

To support extensions, a package needs to set its ``extendable`` property to ``True``, e.g.:

.. code-block:: python

   class Python(Package):
       ...
       extendable = True
       ...

To make a package into an extension, simply add an ``extends`` call in the package definition, and pass it the name of an extendable package:

.. code-block:: python

   class PyNumpy(Package):
       ...
       extends("python")
       ...

This accomplishes a few things.
Firstly, the Python package can set special variables such as ``PYTHONPATH`` for all extensions when the run or build environment is set up.
Secondly, filesystem views can ensure that extensions are put in the same prefix as their extendee.
This ensures that Python in a view can always locate its Python packages, even without environment variables set.

A package can only extend one other package at a time.
To support packages that may extend one of a list of other packages, Spack supports multiple ``extends`` directives as long as at most one of them is selected as a dependency during concretization.
For example, a lua package could extend either lua or luajit, but not both:

.. code-block:: python

   class LuaLpeg(Package):
       ...
       variant("use_lua", default=True)
       extends("lua", when="+use_lua")
       extends("lua-luajit", when="~use_lua")
       ...

Now, a user can install, and activate, the ``lua-lpeg`` package for either lua or luajit.

Adding additional constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some packages produce a Python extension, but are only compatible with Python 3, or with Python 2.
In those cases, a ``depends_on()`` declaration should be made in addition to the ``extends()`` declaration:

.. code-block:: python

   class Icebin(Package):
       extends("python", when="+python")
       depends_on("python@3:", when="+python")

Many packages produce Python extensions for *some* variants, but not others: they should extend ``python`` only if the appropriate variant(s) are selected.
This may be accomplished with conditional ``extends()`` declarations:

.. code-block:: python

   class FooLib(Package):
       variant("python", default=True, description="Build the Python extension Module")
       extends("python", when="+python")
       ...

Mixins for common metadata
--------------------------

Spack's package repository contains a number of mixin classes that can be used to simplify package definitions and to share common metadata and behavior across multiple packages.

For instance, packages that depend on ``cuda`` typically need variants such as ``+cuda`` and ``cuda_arch``, and conflicts to specify compatibility between architectures, compilers and CUDA versions.
To avoid duplicating this metadata in every package that requires CUDA, Spack provides a mixin class called ``CudaPackage`` that can be used to inherit this common metadata and behavior.

Other mixin classes such as ``GNUMirrorPackage`` do not add variants or conflicts, but configure the usual GNU mirror URLs for downloading source code.

The following table lists the full list of mixin classes available in Spack's builtin package repository.

+----------------------------------------------------------------------------+----------------------------------+
|     **API docs**                                                           |           **Description**        |
+============================================================================+==================================+
| :class:`~spack_repo.builtin.build_systems.cuda.CudaPackage`                | A helper class for packages that |
|                                                                            | use CUDA                         |
+----------------------------------------------------------------------------+----------------------------------+
| :class:`~spack_repo.builtin.build_systems.rocm.ROCmPackage`                | A helper class for packages that |
|                                                                            | use ROCm                         |
+----------------------------------------------------------------------------+----------------------------------+
| :class:`~spack_repo.builtin.build_systems.gnu.GNUMirrorPackage`            | A helper class for GNU packages  |
|                                                                            |                                  |
+----------------------------------------------------------------------------+----------------------------------+
| :class:`~spack_repo.builtin.build_systems.python.PythonExtension`          | A helper class for Python        |
|                                                                            | extensions                       |
+----------------------------------------------------------------------------+----------------------------------+
| :class:`~spack_repo.builtin.build_systems.sourceforge.SourceforgePackage`  | A helper class for packages      |
|                                                                            | from sourceforge.org             |
+----------------------------------------------------------------------------+----------------------------------+
| :class:`~spack_repo.builtin.build_systems.sourceware.SourcewarePackage`    | A helper class for packages      |
|                                                                            | from sourceware.org              |
+----------------------------------------------------------------------------+----------------------------------+
| :class:`~spack_repo.builtin.build_systems.xorg.XorgPackage`                | A helper class for x.org         |
|                                                                            | packages                         |
+----------------------------------------------------------------------------+----------------------------------+

These mixins should be used as additional base classes for your package, in addition to the base class that you would normally use (e.g. ``MakefilePackage``, ``AutotoolsPackage``, etc.):

.. code-block:: python

   class Cp2k(MakefilePackage, CudaPackage):
       pass

In the example above ``Cp2k`` inherits the variants and conflicts defined by ``CudaPackage``.

.. _package_maintainers:

Maintainers
-----------

Each package in Spack may have one or more maintainers, i.e. one or more GitHub accounts of people who want to be notified any time the package is modified.

When a pull request is submitted that updates the package, these people will be requested to review the PR.
This is useful for developers who maintain a Spack package for their own software, as well as users who rely on a piece of software and want to ensure that the package doesn't break.
It also gives users a list of people to contact for help when someone reports a build error with the package.

To add maintainers to a package, simply declare them with the ``maintainers`` directive:

.. code-block:: python

   maintainers("user1", "user2")

The list of maintainers is additive, and includes all the accounts eventually declared in base classes.

.. _package_license:

License Information
-------------------

Most of the software in Spack is open source, and most open source software is released under one or more `common open source licenses <https://opensource.org/licenses/>`_.
Specifying the license that a package is released under in a project's ``package.py`` is good practice.
To specify a license, find the `SPDX identifier <https://spdx.org/licenses/>`_ for a project and then add it using the license directive:

.. code-block:: python

   license("<SPDX Identifier HERE>")

For example, the SPDX ID for the Apache Software License, version 2.0 is ``Apache-2.0``, so you'd write:

.. code-block:: python

   license("Apache-2.0")

Or, for a dual-licensed package like Spack, you would use an `SPDX Expression <https://spdx.github.io/spdx-spec/v2-draft/SPDX-license-expressions/>`_ with both of its licenses:

.. code-block:: python

   license("Apache-2.0 OR MIT")

Note that specifying a license without a ``when=`` clause makes it apply to all versions and variants of the package, which might not actually be the case.
For example, a project might have switched licenses at some point or have certain build configurations that include files that are licensed differently.
Spack itself used to be under the ``LGPL-2.1`` license, until it was relicensed in version ``0.12`` in 2018.

You can specify when a ``license()`` directive applies using a ``when=`` clause, just like other directives.
For example, to specify that a specific license identifier should only apply to versions up to ``0.11``, but another license should apply for later versions, you could write:

.. code-block:: python

   license("LGPL-2.1", when="@:0.11")
   license("Apache-2.0 OR MIT", when="@0.12:")

Note that unlike for most other directives, the ``when=`` constraints in the ``license()`` directive can't intersect.
Spack needs to be able to resolve exactly one license identifier expression for any given version.
To specify *multiple* licenses, use SPDX expressions and operators as above.
The operators you probably care most about are:

* ``OR``: user chooses one license to adhere to; and
* ``AND``: user has to adhere to all the licenses.

You may also care about `license exceptions <https://spdx.org/licenses/exceptions-index.html>`_ that use the ``WITH`` operator, e.g. ``Apache-2.0 WITH LLVM-exception``.

Many of the licenses that are currently in the spack repositories have been automatically determined.
While this is great for bulk adding license information and is most likely correct, there are sometimes edge cases that require manual intervention.
To determine which licenses are validated and which are not, there is the ``checked_by`` parameter in the license directive:

.. code-block:: python

   license("<license>", when="<when>", checked_by="<github username>")

When you have validated a package license, either when doing so explicitly or as part of packaging a new package, please set the ``checked_by`` parameter to your Github username to signal that the license has been manually verified.

.. _license:

Proprietary software
--------------------

In order to install proprietary software, Spack needs to know a few more details about a package.
The following class attributes should be defined.

``license_required``
^^^^^^^^^^^^^^^^^^^^

Boolean.
If set to ``True``, this software requires a license.
If set to ``False``, all of the following attributes will be ignored.
Defaults to ``False``.

``license_comment``
^^^^^^^^^^^^^^^^^^^

String.
Contains the symbol used by the license manager to denote a comment.
Defaults to ``#``.

``license_files``
^^^^^^^^^^^^^^^^^

List of strings.
These are files that the software searches for when looking for a license.
All file paths must be relative to the installation directory.
More complex packages like Intel may require multiple licenses for individual components.
Defaults to the empty list.

``license_vars``
^^^^^^^^^^^^^^^^

List of strings.
Environment variables that can be set to tell the software where to look for a license if it is not in the usual location.
Defaults to the empty list.

``license_url``
^^^^^^^^^^^^^^^

String.
A URL pointing to license setup instructions for the software.
Defaults to the empty string.

For example, let's take a look at the Arm Forge package.

.. code-block:: python

   # Licensing
   license_required = True
   license_comment = "#"
   license_files = ["licences/Licence"]
   license_vars = [
       "ALLINEA_LICENSE_DIR",
       "ALLINEA_LICENCE_DIR",
       "ALLINEA_LICENSE_FILE",
       "ALLINEA_LICENCE_FILE",
   ]
   license_url = "https://developer.arm.com/documentation/101169/latest/Use-Arm-Licence-Server"

Arm Forge requires a license.
Its license manager uses the ``#`` symbol to denote a comment.
It expects the license file to be named ``License`` and to be located in a ``licenses`` directory in the installation prefix.

If you would like the installation file to be located elsewhere, simply set ``ALLINEA_LICENSE_DIR`` or one of the other license variables after installation.
For further instructions on installation and licensing, see the URL provided.

If your package requires the license to install, you can reference the location of this global license using ``self.global_license_file``.
After installation, symlinks for all of the files given in ``license_files`` will be created, pointing to this global license.
If you install a different version or variant of the package, Spack will automatically detect and reuse the already existing global license.

If the software you are trying to package doesn't rely on license files, Spack will print a warning message, letting the user know that they need to set an environment variable or pointing them to installation documentation.


Grouping directives
-------------------

We have seen various directives such as ``depends_on``, ``conflicts``, and ``requires``.
Very often, these directives share a common argument, which you becomes repetitive and verbose to write.

.. _group_when_spec:

Grouping with ``when()``
^^^^^^^^^^^^^^^^^^^^^^^^

Spack provides a context manager called ``when()`` that allows you to group directives by a common constraint or condition.

.. code-block:: python

   class Gcc(AutotoolsPackage):

       with when("+nvptx"):
           depends_on("cuda")
           conflicts("@:6", msg="NVPTX only supported in gcc 7 and above")
           conflicts("languages=ada")
           conflicts("languages=brig")
           conflicts("languages=go")

The snippet above is equivalent to the more verbose:

.. code-block:: python

   class Gcc(AutotoolsPackage):

       depends_on("cuda", when="+nvptx")
       conflicts("@:6", when="+nvptx", msg="NVPTX only supported in gcc 7 and above")
       conflicts("languages=ada", when="+nvptx")
       conflicts("languages=brig", when="+nvptx")
       conflicts("languages=go", when="+nvptx")

Constraints from the ``when`` block are composable with ``when`` arguments in directives inside the block.
For instance,

.. code-block:: python

   with when("+elpa"):
       depends_on("elpa+openmp", when="+openmp")

is equivalent to:

.. code-block:: python

   depends_on("elpa+openmp", when="+openmp+elpa")

Constraints from nested context managers are also combined together, but they are rarely needed, and are not recommended.

.. _default_args:

Grouping with ``default_args()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More generally, if directives have a common set of default arguments, you can group them together in a ``with default_args()`` block:

.. code-block:: python

   class PyExample(PythonPackage):

       with default_args(type=("build", "run")):
           depends_on("py-foo")
           depends_on("py-foo@2:", when="@2:")
           depends_on("py-bar")
           depends_on("py-bz")

The above is short for:

.. code-block:: python

   class PyExample(PythonPackage):

       depends_on("py-foo", type=("build", "run"))
       depends_on("py-foo@2:", when="@2:", type=("build", "run"))
       depends_on("py-bar", type=("build", "run"))
       depends_on("py-bz", type=("build", "run"))

.. note::

   The ``with when()`` context manager is composable, while ``with default_args()`` merely overrides the default.
   For example:

   .. code-block:: python

      with default_args(when="+feature"):
          depends_on("foo")
          depends_on("bar")
          depends_on("baz", when="+baz")

   is equivalent to:

   .. code-block:: python

      depends_on("foo", when="+feature")
      depends_on("bar", when="+feature")
      depends_on("baz", when="+baz")  # Note: not when="+feature+baz"

.. _custom-attributes:

``home``, ``command``, ``headers``, and ``libs``
------------------------------------------------

Often a package will need to provide attributes for dependents to query various details about what it provides.
While any number of custom defined attributes can be implemented by a package, the four specific attributes described below are always available on every package with default implementations and the ability to customize with alternate implementations in the case of virtual packages provided:

=========== =========================================== =====================
Attribute   Purpose                                     Default
=========== =========================================== =====================
``home``    The installation path for the package       ``spec.prefix``
``command`` An executable command for the package       | ``spec.name`` found
                                                          in
                                                        | ``.home.bin``
``headers`` A list of headers provided by the package   | All headers
                                                          searched
                                                        | recursively in
                                                          ``.home.include``
``libs``    A list of libraries provided by the package | ``lib{spec.name}``
                                                          searched
                                                        | recursively in
                                                          ``.home`` starting
                                                        | with ``lib``,
                                                          ``lib64``, then the
                                                        | rest of ``.home``
=========== =========================================== =====================

Each of these can be customized by implementing the relevant attribute as a ``@property`` in the package's class:

.. code-block:: python
   :linenos:

   class Foo(Package):
       ...
       @property
       def libs(self):
           # The library provided by Foo is libMyFoo.so
           return find_libraries("libMyFoo", root=self.home, recursive=True)

A package may also provide a custom implementation of each attribute for the virtual packages it provides by implementing the ``<virtual>_<attribute>`` property in the package's class.
The implementation used is the first one found from:

#. Specialized virtual: ``Package.<virtual>_<attribute>``
#. Generic package: ``Package.<attribute>``
#. Default

The use of customized attributes is demonstrated in the next example.

Example: Customized attributes for virtual packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a package ``foo`` that can optionally provide two virtual packages ``bar`` and ``baz``.
When both are enabled, the installation tree appears as follows:

.. code-block:: console

   include/foo.h
   include/bar/bar.h
   lib64/libFoo.so
   lib64/libFooBar.so
   baz/include/baz/baz.h
   baz/lib/libFooBaz.so

The install tree shows that ``foo`` is providing the header ``include/foo.h`` and library ``lib64/libFoo.so`` in its install prefix.
The virtual package ``bar`` is providing ``include/bar/bar.h`` and library ``lib64/libFooBar.so``, also in ``foo``'s install prefix.
The ``baz`` package, however, is provided in the ``baz`` subdirectory of ``foo``'s prefix with the ``include/baz/baz.h`` header and ``lib/libFooBaz.so`` library.
Such a package could implement the optional attributes as follows:

.. code-block:: python
   :linenos:

   class Foo(Package):
       ...
       variant("bar", default=False, description="Enable the Foo implementation of bar")
       variant("baz", default=False, description="Enable the Foo implementation of baz")
       ...
       provides("bar", when="+bar")
       provides("baz", when="+baz")
       ....

       # Just the foo headers
       @property
       def headers(self):
           return find_headers("foo", root=self.home.include, recursive=False)

       # Just the foo libraries
       @property
       def libs(self):
           return find_libraries("libFoo", root=self.home, recursive=True)

       # The header provided by the bar virtual package
       @property
       def bar_headers(self):
           return find_headers("bar/bar.h", root=self.home.include, recursive=False)

       # The library provided by the bar virtual package
       @property
       def bar_libs(self):
           return find_libraries("libFooBar", root=self.home, recursive=True)

       # The baz virtual package home
       @property
       def baz_home(self):
           return self.prefix.baz

       # The header provided by the baz virtual package
       @property
       def baz_headers(self):
           return find_headers("baz/baz", root=self.baz_home.include, recursive=False)

       # The library provided by the baz virtual package
       @property
       def baz_libs(self):
           return find_libraries("libFooBaz", root=self.baz_home, recursive=True)

Now consider another package, ``foo-app``, depending on all three:

.. code-block:: python
   :linenos:

   class FooApp(CMakePackage):
       ...
       depends_on("foo")
       depends_on("bar")
       depends_on("baz")

The resulting spec objects for its dependencies shows the result of the above attribute implementations:

.. code-block:: python

   # The core headers and libraries of the foo package

   >>> spec["foo"]
   foo@1.0%gcc@11.3.1+bar+baz arch=linux-fedora35-haswell
   >>> spec["foo"].prefix
   "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6"

   # home defaults to the package install prefix without an explicit implementation
   >>> spec["foo"].home
   "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6"

   # foo headers from the foo prefix
   >>> spec["foo"].headers
   HeaderList([
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/include/foo.h",
   ])

   # foo include directories from the foo prefix
   >>> spec["foo"].headers.directories
   ["/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/include"]

   # foo libraries from the foo prefix
   >>> spec["foo"].libs
   LibraryList([
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/lib64/libFoo.so",
   ])

   # foo library directories from the foo prefix
   >>> spec["foo"].libs.directories
   ["/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/lib64"]

.. code-block:: python

   # The virtual bar package in the same prefix as foo

   # bar resolves to the foo package
   >>> spec["bar"]
   foo@1.0%gcc@11.3.1+bar+baz arch=linux-fedora35-haswell
   >>> spec["bar"].prefix
   "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6"

   # home defaults to the foo prefix without either a Foo.bar_home
   # or Foo.home implementation
   >>> spec["bar"].home
   "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6"

   # bar header in the foo prefix
   >>> spec["bar"].headers
   HeaderList([
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/include/bar/bar.h"
   ])

   # bar include dirs from the foo prefix
   >>> spec["bar"].headers.directories
   ["/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/include"]

   # bar library from the foo prefix
   >>> spec["bar"].libs
   LibraryList([
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/lib64/libFooBar.so"
   ])

   # bar library directories from the foo prefix
   >>> spec["bar"].libs.directories
   ["/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/lib64"]

.. code-block:: python

   # The virtual baz package in a subdirectory of foo's prefix

   # baz resolves to the foo package
   >>> spec["baz"]
   foo@1.0%gcc@11.3.1+bar+baz arch=linux-fedora35-haswell
   >>> spec["baz"].prefix
   "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6"

   # baz_home implementation provides the subdirectory inside the foo prefix
   >>> spec["baz"].home
   "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/baz"

   # baz headers in the baz subdirectory of the foo prefix
   >>> spec["baz"].headers
   HeaderList([
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/baz/include/baz/baz.h"
   ])

   # baz include directories in the baz subdirectory of the foo prefix
   >>> spec["baz"].headers.directories
   [
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/baz/include"
   ]

   # baz libraries in the baz subdirectory of the foo prefix
   >>> spec["baz"].libs
   LibraryList([
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/baz/lib/libFooBaz.so"
   ])

   # baz library directories in the baz subdirectory of the foo prefix
   >>> spec["baz"].libs.directories
   [
       "/opt/spack/linux-fedora35-haswell/gcc-11.3.1/foo-1.0-ca3rczp5omy7dfzoqw4p7oc2yh3u7lt6/baz/lib"
   ]

Style guidelines for packages
-----------------------------

The following guidelines are provided, in the interests of making Spack packages work in a consistent manner:

Variant Names
^^^^^^^^^^^^^

Spack packages with variants similar to already-existing Spack packages should use the same name for their variants.
Standard variant names are:

======= ======== ========================
Name    Default   Description
======= ======== ========================
shared   True     Build shared libraries
mpi      True     Use MPI
python   False    Build Python extension
======= ======== ========================

If specified in this table, the corresponding default is recommended.

The semantics of the `shared` variant are important.
When a package is built `~shared`, the package guarantees that no shared libraries are built.
When a package is built `+shared`, the package guarantees that shared libraries are built, but it makes no guarantee about whether static libraries are built.

Version definitions
^^^^^^^^^^^^^^^^^^^

Spack packages should list supported versions with the newest first.

Using ``home`` vs ``prefix``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``home`` and ``prefix`` are both attributes that can be queried on a package's dependencies, often when passing configure arguments pointing to the location of a dependency.
The difference is that while ``prefix`` is the location on disk where a concrete package resides, ``home`` is the `logical` location that a package resides, which may be different than ``prefix`` in the case of virtual packages or other special circumstances.
For most use cases inside a package, its dependency locations can be accessed via either ``self.spec["foo"].home`` or ``self.spec["foo"].prefix``.
Specific packages that should be consumed by dependents via ``.home`` instead of ``.prefix`` should be noted in their respective documentation.

See :ref:`custom-attributes` for more details and an example implementing a custom ``home`` attribute.
