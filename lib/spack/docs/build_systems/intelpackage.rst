.. _intelpackage:

.. contents::

------------
IntelPackage
------------

Intel provides many licensed software packages, which all share the
same basic steps for configuring and installing, as well as license
management.

This build system is a work-in-progress. See
https://github.com/spack/spack/pull/4300 and
https://github.com/spack/spack/pull/7469 for more information.


**TODO:** replace http links to other files to rst syntax.

^^^^^^^^^^^^
Introduction
^^^^^^^^^^^^

Spack interacts with Intel packages using three routes:

.. _`route 1`:

1. Integrating as *external* tools,

.. _`route 2`:

2. Installing as tools *internal* to Spack, and

.. _`route 3`:

3. *Using* the tools to compile what we'll call *client packages* within Spack.

Conceivably, there is an auxiliary route that follows naturally from `route 2`_, like
any regular Spack package, namely:

.. _`route 4`:

4. Making Spack-installed Intel tools available outside of Spack for ad-hoc use.
   This would be done typically through Spack-managed modulefiles.

This document covers routes 1 through 3 and explains how to go about
integrating and using these tools with Spack.


^^^^^^^^^^
Licenses
^^^^^^^^^^

""""""""""""""""""""""""""
When are licenses needed?
""""""""""""""""""""""""""

Some of Intel's software products require a license, notably
the core development packages that contain compilers, analyzers, and optimizers.
Currently in Spack, these core components can be provided by two packages:

* ``intel-parallel-studio`` – the entire suite,
* ``intel`` – a compilers-only subset.

For the core tools, a valid license is always needed at product installation
time and to compile client packages, but never to run the resulting client
packages.

From 2017 onwards, Intel made many of its standalone performance library
products, notably MPI and MKL (which provides BLAS, Lapack, ScaLapack, and
FFT), available for use `under a no-cost license
<https://software.intel.com/en-us/license/intel-simplified-software-license>`_.
These performance libraries are available as the following standalone Spack
packages (at the time of writing):

* ``intel-mkl`` – Math Kernel Library,
* ``intel-mpi`` – Intel's MPI implementation (which is based on MPICH),
* ``intel-ipp`` – Building blocks for image processing, signal processing, and data processing,
* ``intel-daal`` – Machine learning and data analytics library.

Pre-2017 versions [fn1]_ of the performance library products do require, like
compilers, the license at installation time of the products and during
compilation of client packages.

The performance libraries are also provided by the omnibus
``intel-parallel-studio`` package in Spack, which always requires a license.
To complicate matters a bit, that package comes in 3 editions,
of which only the uppermost ``cluster`` edition contains the MPI components,
and hence only that edition will provide the ``mpi`` virtual package.

""""""""""""""""""""""""""""""""""""""""""""""""""
What must you do in Spack to use Intel licenses?
""""""""""""""""""""""""""""""""""""""""""""""""""

* If you wish to integrate licensed Intel tools into Spack as external packages
  (`route 1`_ above) we assume that their license configuration is in place and
  is working [fn2]_. In this case, skip the rest of this section and proceed to
  `Integration of Intel tools external to Spack`_.

* If you plan to use Spack to install licensed tools for you (`route 2`_
  above), the Intel product installer that Spack will run underneath must be
  able to find your license by one of the means explained in this section.

For authoritative information, see Intel's license documentation at:

* https://software.intel.com/en-us/faq/licensing
* https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses


To install a licensed Intel package within Spack, provide the license by one of
the following means *before* executing ``spack install intelfoo``:


Pointing to a license server
""""""""""""""""""""""""""""""

Setting up a license server as such is outside the scope of Spack. We assume
your system administrator has a license server running and has installed
network licenses for Intel packages.

To obtain a license from an Intel license server for temporary use by a client
application, a process known as "checking out a license", the client
application needs to be told the host name and port number of one or more
license server. This can be done by three methods, all described at
https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license .

Ideally, your license administrator will already have installed the necessary
files to tell clients where to reach the license server.
Look for files under ``/opt/intel/licenses/foo.lic`` that have the form::

  SERVER  hostname  hostid_or_ANY  portnum
  USE_SERVER

The key tokens are the ``SERVER`` lines to indicate the network address and the
``USE_SERVER`` line, placed there specifically for clients.

According to Intel's documentation, there is a way to install a licensed
product even when a FlexLM server process is *not running*, namely, when the
license server is specified via the ``INTEL_LICENSE_FILE`` environment variable
and has the form ``port@serverhost``. All other means of specifying a network
license require that license server be up.


Installing a standalone license file
""""""""""""""""""""""""""""""""""""

If you purchased a single-user license, be sure to obtain your license file as
instructed by Intel. If needed, request that the file be re-sent to you
`following Intel's instructions
<https://software.intel.com/en-us/articles/resend-license-file>`_.

License files are plain text files containing license tokens in FlexLM format
and whose name ends in ``.lic``.  Intel installers and compilers look for
license files in several different locations when they run, first in an
Intel-defined default directory, then the contents of the environment variable
``INTEL_LICENSE_FILE`` [fn3]_, and finally their own directory.

Place your license by one of the following means, in order of decreasing
preference:

* Default directory

  Install your license file in the directory ``/opt/intel/licenses/`` if you
  have write permission to it. This directory is inspected by all Intel tools
  and is therefore preferred, as no further configuration steps will be needed.

  Create the directory if it does not yet exist.  For the file name, either
  keep the downloaded name or use another suitably plain yet descriptive
  name that ends in ``.lic``. Set permissions such that the license file is
  accessible to the licensed users only.


* Directory given in environment variable

  If you cannot use the default directory, but your system already has set
  the environment variable ``INTEL_LICENSE_FILE`` outside of Spack, then, if
  you have the necessary write permissions, place your license file in one of
  the directories mentioned in this environment variable. Make the license file
  accessible to the licensed users only.

  **Recommendation:**
  If your system has not yet set and used the environment variable
  ``INTEL_LICENSE_FILE``, you could start using it for the ``spack install``
  stage of licensed tools and subsequent client packages.  You would, however,
  be in a bind to always set that variable in the same manner, even after
  updates and re-installations, and perhaps accommodate additions to it. As
  this may be difficult in the long run, we recommend that you do *not* attempt
  to start using the variable solely for Spack.  Instead, try the next option.

* Spack-managed file

  If you cannot install your license file in Intel's default directory or a
  directory pointed to by a pre-existing ``INTEL_LICENSE_FILE`` setting, use
  the concept of a *Spack-global Intel license file*.

  To initialize this file, do the following:

  .. code-block:: sh

    dir="$SPACK_ROOT/etc/spack/licenses/intel"
    mkdir -p "$dir"
    cp -p your_downloaded_name.lic "$dir/license.lic"

  Obviously, adjust ``your_downloaded_name.lic`` to your license file name but
  keep the target name ``license.lic``. 

  The Spack-global Intel license file will be used for Intel tools installed
  within Spack (i.e., under `route 2`_ above) only, in the following manner:
  Spack will, during the final phases of ``spack install intelfoo``, place
  symbolic links to this file in each directory where licensed Intel binaries
  were installed.

When you run ``spack install intelfoo``, Spack inspects the license locations
given above. If Spack cannot find a license after all, it will bring up an
editor for the Spack-global Intel license file, with the expectation and
instructions for you to populate the file.  This should not happen, but if it
does, copy&paste the contents of your downloaded license file into the editor [fn4]_,
save the file, and quit the editor.  You will recognize these steps as an
alternative means to initialize the file. Either way, once populated, you
should not have to touch this file again until your license status changes.


**TODO:**

* Code this specific behavior (2018-05-16)  Use SGILF path explicitly in
  ``silent.cfg``, or convey it via a temporary INTEL_LICENSE_FILE setting!?

* Note `PR #6534 "Intel v18 License File Format Issue" <https://github.com/spack/spack/issues/6534>`_.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Integration of Intel tools *external* to Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section discusses `route 1`_ under `Introduction`_.

A site that already uses Intel tools, especially licensed ones, will likely
have some versions already installed on the system, especially at a time when
Spack is just being introduced. It will be useful to make such previously
installed tools available for use by Spack as they are. How to do this varies
depending on the type of the tools:

""""""""""
Compilers
""""""""""

Configure external Intel compilers, like all compilers that Spack is to use,
in ``compilers.yaml`` files located in
``$SPACK_ROOT/etc/spack/`` or your own ``~/.spack/`` directory.
See `Vendor-Specific Compiler Configuration
<http://spack.readthedocs.io/en/latest/getting_started.html#vendor-specific-compiler-configuration>`_
in the Spack documentation and follow the specifics for Intel Compilers.

Briefly, the ``compilers.yaml`` files combine C and Fortran compilers of a
specific vendor release and define each such set as a Spack spec that in this
case always has the form ``intel@compilerversion``.  The entry determines
how this spec is resolved, via ``paths`` and/or ``modules`` tokens, to the
specific pre-installed compiler version on the system.

The following example illustrates how to integrate the 2017 Intel compiler
suite, which outside of Spack was activated by users of the example system as
``module load intel/17``. Since Spack must be rather more picky about versions,
we must specify full versions and complete modulefile names in the relevant
``compilers.yaml`` entry:

.. code-block:: yaml

    compilers:
    ...
    - compiler:
        target:     x86_64
        operating_system:   centos6
        modules:    [intel/17/17.0.6]
        spec:       intel@17.0.6
        paths:
          cc:       /opt/intel/compilers_and_libraries_2017.6.256/linux/bin/intel64/icc
          cxx:      /opt/intel/compilers_and_libraries_2017.6.256/linux/bin/intel64/icpc
          f77:      /opt/intel/compilers_and_libraries_2017.6.256/linux/bin/intel64/ifort
          fc:       /opt/intel/compilers_and_libraries_2017.6.256/linux/bin/intel64/ifort
    ...


""""""""""
Libraries
""""""""""

Configure external library-type packages (as opposed to compilers)
in the files ``$SPACK_ROOT/etc/spack/packages.yaml`` or
``~/.spack/packages.yaml``, fully documented in the `Build settings
<http://spack.readthedocs.io/en/latest/build_settings.html#external-packages>`_
Spack documentation.

Similar to ``compilers.yaml``, the ``packages.yaml`` files define a package
external to Spack in terms of a Spack spec and resolve each such spec via
either the ``paths`` or ``modules`` tokens to a specific pre-installed package
version on the system.  Since Intel tools generally need environment variables
to interoperate, which cannot be conveyed in a mere ``paths`` specification,
the ``modules`` token will be more sensible to use. It resolves the Spack-side
spec to a modulefile generated and managed outside of Spack's purview,
to be loaded within Spack when the corresponding spec is called upon to compile
client packages.

If your system administrator did not provide modules for pre-installed Intel
tools, you could do well to ask for them, because installing multiple copies
of the Intel tools, as is wont to happen once Spack is in the picture, is
bound to stretch disk space and patience thin. If you *are* the system
administrator and are still new to modules, then perhaps it's best to follow
the `next section <Installing Intel tools within Spack_>`_ to install the tools
solely within Spack.

The following example integrates two packages embodied by hypothetical
external modulefiles ``intel-mkl/18/18.0.1`` and ``intel-mkl/18/18.0.2``, as
Spack packages ``intel-mkl@2018.1.163`` and ``intel-mkl@2018.2.199``,
respectively.

.. code-block:: yaml

   packages:
     intel-mkl:
       modules:
         intel-mkl@2018.1.163  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.1
         intel-mkl@2018.2.199  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.2

Note that the version numbers in the ``intel-mkl`` spec correspond to the ones
used for the Intel products and adopted within Spack. You can inspect them by:

.. code-block:: sh

  spack info intel-mkl

Using the same version numbers is useful for clarity, but not strictly necessary.

**TODO:** Confirm.

Note that the Spack spec in the example does not contain a compiler
specification. This is intentional, as the Intel library packages can be used
unmodified with different compilers.

**TODO:** Confirm how the compiler-less spec is handled.

A slightly more advanced example follows, illustrating how to provide variants
and using the ``buildable: False`` directive to prevent Spack from installing
other versions or variants of the named package through its normal internal
mechanism.

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       modules:
         intel-parallel-studio@cluster.2018.1.163 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.1
         intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.2
       buildable: False

**TODO:** Confirm variant handling.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing Intel tools *within* Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section discusses `route 2`_ from the `Introduction`_.

When a system does not yet have Intel tools installed already, or the installed
versions are undesirable, Spack can install Intel tools like regular Spack
packages for you and subsequently use them, with appropriate configuration, to
compile client packages.

As stated in the previous section `Integration of Intel tools external to
Spack`_, Intel compilers and some early library-type Intel packages require a
license at installation and during runtime. Follow the section `Licenses`_ on
how to make your license accessible to Spack, for passing on to the Intel
installer that Spack will run for you.

""""""""""""""""""""
Compiler components
""""""""""""""""""""

Follow the same basic steps as shown under `Compilers`_ in the previous
section to configure entries in ``compilers.yaml``, with the following
considerations:

* Under ``paths:``, use the full paths to the actual compiler binaries (``icc``,
  ``ifort``, etc.) located within the Spack installation tree, in all their
  unpleasant length.

* Use the ``modules:`` or ``cflags:`` tokens to specify a suitable accompanying
  ``gcc`` version to help pacify picky C++ client packages which may require C++
  standards that are more recent than the ones that your system-provided ``gcc``
  and its ``libstdc++.so`` can support.


That's all there's to say for the mere installation of the Intel tools by
Spack.  To use those tools for client packages, additional configuration steps
are neeeded, shown the the next section
`Using Intel tools to compile client packages`_.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using Intel tools to compile client packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally, this section pertains to `route 3`_ from the `Introduction`_.

Once Intel packages are integrated into Spack as either external package or
installed within Spack, they can be used as intended for installing *client
packages* within Spack.  There are three different routes for doing so,
depending on the type of the Intel component needed:

""""""""""""""""""""""""
Using Intel compilers
""""""""""""""""""""""""

To select Intel compilers to compile client packages, use one of the following
means:

* Request the Intel compilers expliclity in the client spec, e.g.:

  .. code-block:: sh

    spack install libxc@3.0.0%intel


* Alternatively, request Intel compilers implicitly by concretization preferences.
  To do so, configure the order of compilers in the appropriate
  ``packages.yaml`` file, under either an ``all:`` or client-package-specific
  entry, in a  ``compiler:`` list; see section
  `Configuring Package Preferences
  <http://spack.readthedocs.io/en/latest/tutorial_configuration.html#configuring-package-preferences>`_
  of the Spack documentation.

  See also: `Concretization Preferences
  <http://spack.readthedocs.io/en/latest/build_settings.html#concretization-preferences>`_.

Example: ``etc/spack/packages.yaml`` might contain:

.. code-block:: yaml

  packages:
    all:
      compiler: [ intel@18, intel@17, gcc@4.4.7, gcc@4.9.3, gcc@7.3.0, ]



""""""""""""""""""""""""""""""""""""""""""""""""
Using Intel packages to satisfy virtual packages
""""""""""""""""""""""""""""""""""""""""""""""""

Intel packages, whether integrated into Spack as external packages or
installed within Spack, can be called upon to satisfy the requirement of a
client package for a library that is available from different providers.
The relevant virtual packages for Intel are ``blas``, ``lapack``,
``scalapack``, and ``mpi``.

In both kinds of installation, Intel packages have optional `variants
<http://spack.readthedocs.io/en/latest/basic_usage.html#variants>`_ which alter
the list of virtual packages they can satisfy.  For Spack-external packages,
the active variants are a combination of the defaults declared in Spack's
package repository and the relevant declaration in ``packages.yaml``.
Likewise, for Spack-internal packages, the set of active variants is a
combination of the defaults from the package definition in the Spack repository
and the spec used with ``spack install intelfoo [variant ...]``. The variants
are permanently tied to the package so installed.

To have Intel packages used by default for all client packages or a specific
client one, edit the ``packages.yaml`` file.
Customize, either under the ``all:`` entry or a client package entry, a new
``providers:`` dictionary entry whose keys are the virtual packages and whose
values are the Spack specs that satisfy the virtual package, in order of
decreasing preference.

For specifics on the ``providers:`` settings, see the Spack documentation at

* Tutorial for `Configuring Package Preferences <http://spack.readthedocs.io/en/latest/tutorial_configuration.html#configuring-package-preferences>`_.

* `Concretization Preferences <http://spack.readthedocs.io/en/latest/build_settings.html#concretization-preferences>`_.

Example: The following fairly minimal example for ``packages.yaml`` shows how
to exclusively use the standalone ``intel-mkl`` for all the linear algebra
virtual packages in Spack, and ``intel-mpi`` as preferred MPI implementation,
but leaving the door open to use other implementations if desired.

.. code-block:: yaml

  packages:
    all:
      providers:
        mpi: [intel-mpi, openmpi, mpich, ]
        blas: [intel-mkl, ]
        lapack: [intel-mkl, ]
        scalapack: [intel-mkl, ]


""""""""""""""""""""""""
Explicit dependency
""""""""""""""""""""""""

With the proper installation as detailed above, no special steps should be
required when a client package specifically requests an Intel package as
dependency, this being one of the target use cases for Spack.

**TODO:** confirm for DAAL, IPP

.. [fn1] Strictly speaking, versions up to and including ``2017.1``.

.. [fn2] How would the external installation have succeeded otherwise?

.. [fn3]  Despite the name, ``INTEL_LICENSE_FILE`` can hold several and diverse entries.
   They  can be either directories (presumed to contain ``*.lic`` files), file
   names, or network locations in the form ``port@host`` (on Linux and Mac),
   with all items separated by ":" (on Linux and Mac).

.. [fn4] Should said editor turn out to be ``vi``, you better be in a postion
   to know how to use it.
