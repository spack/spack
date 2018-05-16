.. _intelpackage:

------------
IntelPackage
------------

Intel provides many licensed software packages, which all share the
same basic steps for configuring and installing, as well as license
management.

This build system is a work-in-progress. See
https://github.com/spack/spack/pull/4300 and
https://github.com/spack/spack/pull/7469 for more information.

************
Introduction
************

Spack interacts with Intel packages in three ways:

(1) Integrating as *external* tools,
(2) Installing as tools *internal* to Spack, and
(3) *Using* the tools to compile what we'll call *client packages* within Spack.

Conceivably, there is an auxiliary way that follows naturally from item 2., like
any other regular Spack package, namely:

(4) Making the Spack-installed Intel tools available *external to Spack* for ad-hoc use.
This is done typically through Spack-managed modulefiles.

This document aims to clarify the different ways and to document how to go about
using the tools in each way, focusing on items 1. through 3.


***********
Licenses
***********

Some of Intel's software products require a license, in particular
the core development packages of compilers, analyzers, and optimizers.
Currently in Spack, these core components are available under two names:

* ``intel-parallel-studio`` - the entire suite,
* ``intel`` - a compilers-only subset.

For these core tools, a valid license is always needed to *install* them and to
*compile* client packages, but never to *run* client packages.

If you wish to integrate these tools into Spack as external packages (item 1.
above) we assume that their license configuration is in place and is working.
In this case, skip the rest of this section.

If you plan to have Spack install those tools for you (item 2. above), the
Intel installer that Spack will run for you must be able to find your license,
using one of the means explained in this section.

From 2017 onwards, Intel made many of its performance libraries, notably MPI
and MKL (which provides BLAS, Lapack, ScaLapack, and FFT), available for use
without purchasing a license. Earlier versions of these library products, do
require, like compilers, a license for *installation* of the products
themselves, and during *compilation* of client packages, but never at runtime
of client packages.

For more, see Intel's license documentation at:

* https://software.intel.com/en-us/faq/licensing
* https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses



To install a licensed Intel package within Spack, provide the license by one of
the following means *before* executing ``spack install intelfoo``:


Using a License Server
~~~~~~~~~~~~~~~~~~~~~~~

Setting up a license server as such is outside the scope of Spack. We assume
your system administrator has a license server running and has installed
network licenses for Intel packages.

To use an Intel license server client-side, e.g., by an Intel installer to
install licensed library packages or compilers, each such client application
needs to know the host name(s) and port number(s) of the license server.
This can be done by three methods, all described at
https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license .

Ideally, your license administrator will *already have installed* the necessary
files to tell clients where to reach the server.
Notably, any files under ``/opt/intel/licenses/foo.lic`` that have the form::

  SERVER  hostname  hostid_or_ANY  portnum
  USE_SERVER

will be found automatically by client applications like installers and
eventually compilers and require no further action to reach the license server.
While not particularly recommended, even the actual network license files
containing full PACKAGE and INCREMENT data could be placed this way, as long as
the ``SERVER`` and ``USE_SERVER`` tokens are present or have been added in the
header.

According to Intel's documentation, there is a way to install a licensed
product even when a FlexLM server process is *not running*, namely, when the
license server is specified via the ``INTEL_LICENSE_FILE`` environment variable
and has the form ``port@serverhost``. All other means of configuring a network
license for a client require the license server to be up.


Using a Standalone License File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you purchased a single-user license, be sure to obtain your license file as
instructed by Intel. If needed, request that the file be re-sent to you
`following Intel's instructions
<https://software.intel.com/en-us/articles/resend-license-file>`_.

License files are plain text files containing license tokens in FlexLM format
and whose name ends in ``.lic``.  Intel installers and compilers look for
license files in several different locations when they run, first in an
Intel-defined default directory, then the contents of the environment variable
``INTEL_LICENSE_FILE`` [1]_, and finally their own directory.

.. [1]  Despite the name, ``INTEL_LICENSE_FILE`` is actually a "PATH"-style
   variable that can hold a list of directories (presumed to contain ``*.lic``
   files), file names, or network locations in the form ``port@host`` (on Linux
   and Mac), with all items separated by ":" (on Linux and Mac).

Place your license by one of the following means, in order of decreasing
preference:

* Default directory

  Install your license file in the directory ``/opt/intel/licenses/`` if you
  have write permission to it. This directory is inspected by all Intel tools
  and is therefore preferred, as no further configuration steps are needed.

  Create the directory if it does not yet exist.  For the file name, either
  keep the downloaded name or use another suitably plain yet descriptive
  name that ends in ``.lic``. Set permissions such that the license file is
  accessible to the licensed users only.


* Environment variable

  If you cannot use the default directory, but your system already has set
  the environment variable ``INTEL_LICENSE_FILE`` outside of Spack, then, if
  you have the necessary write permission, place your license file in one of
  the directories mentioned in this environment variable. Make the license
  file accessible to the licensed users only.

  If your system has not yet set and used the environment variable
  ``INTEL_LICENSE_FILE``, you could use it for the ``spack install`` stage and
  you would be responsible to set always set it consistently, and persistently
  across updates and re-installations.  As this may be difficult in the long
  run, we recommend that you do *not* attempt to start using the variable
  solely for Spack.  Instead, try the next option.

* Spack-managed file

  If you cannot install your license file in Intel's default directory or a
  location within a location of a pre-existing ``INTEL_LICENSE_FILE`` setting,
  use the concept of a *Spack-global Intel license file*.

  To initialize this file, *copy* your downloaded license file to
  ``$SPACK_ROOT/etc/spack/licenses/intel/license.lic``; create the ``intel``
  directory if it does not yet exist.  This is a one-time action.  Once
  Spack's global Intel license file has been populated, no further action
  from you should be needed.

  Spack will use this file for Intel tools installed within Spack only (i.e.,
  under route 2. above), as follows: at the end of ``spack install
  intelfoo``, symbolic links to the global Intel license file will be placed
  in each directory where licensed Intel binaries were installed.

When you run ``spack install intelfoo``, Spack inspects the license locations
given above. If Spack cannot find a license, it will bring up an editor to
populate the global Intel license file.  At this point, you can copy&paste the
contents of *your* license file into this file.  This is an alternative way to
initialize the Spack-global Intel license file and, like initialization by
copy, should be needed only once.


**TODO:**

* Code this specific behavior (2018-05-16)
* Note `PR #6534 "Intel v18 License File Format Issue" <https://github.com/spack/spack/issues/6534>`_.


**************************************************
Integration of Intel tools *external* to Spack
**************************************************

This section discusses item 1. from the `Introduction`_.

A site that already uses Intel tools, especially licensed ones, will likely
have some versions already installed on the system, especially at a time when
Spack is just being introduced. It will be useful to make such previously
installed tools available for use by Spack as they are. Integration varies
depending on the nature of the tools:

Compilers
~~~~~~~~~~~

Configure external Intel *compilers*, like all compilers that Spack is to use,
in ``compilers.yaml`` files located in
``$SPACK_ROOT/etc/spack/`` or your own ``~/.spack/`` directory.
See `Vendor-Specific Compiler Configuration
<http://spack.readthedocs.io/en/latest/getting_started.html#vendor-specific-compiler-configuration>`_
in the Spack documentation and follow the specifics for Intel Compilers.

Briefly, the ``compilers.yaml`` files combine C and Fortran compilers of a
specific vendor release and define each such set as a Spack spec that in this
case has the form ``intel@version``.  The entry then determines how this spec
is resolved, via either a ``paths`` or ``modules`` tokens, to the specific
pre-installed compiler version on the system.

The following example illustrates how to integrate the 2017 Intel compiler
suite, which outside of Spack is activated by users of the example system as
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


Libraries
~~~~~~~~~~~

Configure external *library-type* packages (as opposed to compilers)
in the files ``$SPACK_ROOT/etc/spack/packages.yaml`` or
``~/.spack/packages.yaml``, as documented in the `Build settings Spack
documentation
<http://spack.readthedocs.io/en/latest/build_settings.html#external-packages>`_.

Similar to ``compilers.yaml``, the ``packages.yaml`` files define a package
external to Spack in terms of a Spack spec and resolve each such spec via
either the ``paths`` or ``modules`` tokens to a specific pre-installed package
version on the system.  Since Intel tools generally need environment variables
to interoperate, which cannot be conveyed in a mere ``paths`` specification,
the ``modules`` token will be more sensible to use. It resolves the Spack-side
spec to a modulefile that is generated and managed outside of Spack's purview,
and which will be loaded when the corresponding spec is called upon within
Spack to compile client packages.

The following example integrates two packages embodied by hypothetical
external modulefiles ``intel-mkl/18/18.0.1`` and ``intel-mkl/18/18.0.2``, as
Spack packages ``intel-mkl@2018.1.163`` and ``intel-mkl@2018.2.199``,
respectively:

.. code-block:: yaml

   packages:
     intel-mkl:
       modules:
         intel-mkl@2018.1.163  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.1
         intel-mkl@2018.2.199  arch=linux-centos6-x86_64:  intel-mkl/18/18.0.2

Note that the Spack spec does intentionally not contain a compiler
specification. This is intentional, as the Intel library packages can be used
unmodified with different compilers.

**TODO:** Confirm how the compiler-less spec is handled.

If your system administrator did not provide modules for pre-installed Intel
tools, you could do well to ask for them, because installing multiple copies
of the Intel tools, as is wont to happen once Spack is in the picture, is
bound to stretch disk space and patience thin. If you *are* the system
administrator and are still new to modules, then perhaps it's best to follow
the next section and install the Intel tools solely within Spack.

A more advanced version follows, illustrating how to provide variants and
using the ``buildable:`` directive to prevent Spack from installing other
versions or variants of the named package through its normal internal
mechanism.

.. code-block:: yaml

   packages:
     intel-parallel-studio:
       modules:
         intel-parallel-studio@cluster.2018.1.163 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.1
         intel-parallel-studio@cluster.2018.2.199 +mkl+mpi+ipp+tbb+daal  arch=linux-centos6-x86_64:  intel/18/18.0.2
       buildable: False

**TODO:** Confirm variant handling.


*************************************
Installing Intel tools *within* Spack
*************************************

This section discusses item 2. from the `Introduction`_.

When a system does not yet have Intel tools installed already, or the
installed versions are too old, Spack can install Intel tools as normal Spack
packages for you and then use them, with the appropriate configuration, to
compile further client packages.

As stated in the previous section `Integration of Intel tools *external* to
Spack`_, Intel compilers and some early library-type Intel packages require a
license for *installing* and *running* them. Follow the section `Licenses`_ on
how to make your license accessible to Spack and to the Intel installer that
Spack will run for you.

Compiler components
~~~~~~~~~~~~~~~~~~~~~

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


*********************************************
Using Intel tools to compile client packages
*********************************************

Finally, this section pertains to item 3. from the `Introduction`_.

Once Intel packages are integrated into Spack as either external package or
installed within Spack, they can be used as intended for installing *client
packages* within Spack.  There are three different routes for doing so,
depending on the type of the Intel component needed:

Using Intel compilers
~~~~~~~~~~~~~~~~~~~~~~~~~

To select Intel compilers to compile client packages, use one of the following
means:

* Request the Intel compilers expliclity in the client spec, e.g.:

.. code-block:: sh

   spack install libxc@3.0.0%intel


* Alternatively, you can request Intel compilers by so-called concretization preference.
To do so, configure the order in the appropriate ``packages.yaml`` file, under
either an ``all:`` or client-package-specific entry, in a  ``compiler:`` list; see section
`Configuring Package Preferences <http://spack.readthedocs.io/en/latest/tutorial_configuration.html#configuring-package-preferences>`_.
of the Spack documentation.

See also: `Concretization Preferences <http://spack.readthedocs.io/en/latest/build_settings.html#concretization-preferences>`_.

Example: ``etc/spack/packages.yaml`` might contain:

.. code-block:: yaml

  packages:
    all:
      compiler: [ intel@18, intel@17, gcc@4.4.7, gcc@4.9.3, gcc@7.3.0, ]



Using Intel packages as virtual packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Intel packages, whether integrated into Spack as external packages or
installed within Spack, can be called upon to satisfy the requirement of a
client package for a library that is available from different providers.
The relevant virtual packages for Intel are ``blas``, ``lapack``,
``scalapack``, and ``mpi``.

In both kinds of installation, Intel packages have optional *variants*
which may alter the list of virtual packages provided, depending on the
variants that were active for each externally declared or internally
installed package.

To have Intel packages used by default for all client packages or a specific
client one, edit the ``packages.yaml`` file.
Customize, either under the ``all:`` entry or a client package entry, a new
``providers:`` dictionary entry whose keys are the virtual packages and whose
values are the Spack specs that satisfy the virtual package, in order of
decreasing preference.

For specifics on the ``providers:`` settings, see the Spack documentation at

* Tutorial for `Configuring Package Preferences <http://spack.readthedocs.io/en/latest/tutorial_configuration.html#configuring-package-preferences>`_.

* `Concretization Preferences <http://spack.readthedocs.io/en/latest/build_settings.html#concretization-preferences>`_.

Example: ``~/.spack/packages.yaml`` might contain:

.. code-block:: yaml

  packages:
    all:
      providers:
        mpi: [intel-mpi, intel-parallel-studio, openmpi, mpich, ]
        blas: [intel-mkl, ]
        lapack: [intel-mkl, ]
        scalapack: [intel-mkl, ]


**TODO:** confirm this is clean and sensible.


Explicit dependency
~~~~~~~~~~~~~~~~~~~~~~~~

With the proper installation as detailed above, no special steps should be
required when a client package specifically requests an Intel package as
dependency, this being one of the target use cases for Spack.

**TODO:** confirm for DAAL, IPP

