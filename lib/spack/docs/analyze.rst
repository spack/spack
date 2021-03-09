.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _analyze:

=======
Analyze
=======

The analyze commands allows you to take an existing package install, and run
an analyzer to extract one or more metrics. The metrics can range from reading
metadata about install files and output to extracting Application Binary
Interface (ABI) information from binaries. 

-----------------
Analyzer Metadata
-----------------

For all analyzers, we write to an ``analyze`` folder in the package install
directory metadata folder. For example, here we see an analyze folder that is
alongside a wget install:

.. code-block:: console

    $ ls .spack/
    analyze                   archived-files                     repos                              spack-build-03-build-out.txt
    spack-build-out.txt       install_environment.json           spack-build-01-autoreconf-out.txt  spack-build-04-install-out.txt
    spack-configure-args.txt  install_manifest.json              spack-build-02-configure-out.txt   spack-build-env.txt
    spec.yaml

This means that you can always find analyzer output in this folder. Sometimes the output
is a bit redundant - parsed files from the folder above, but it's been added to
be namespaced as an analyzer output.

-----------------
Listing Analyzers
-----------------

If you aren't familiar with Spack's analyzers, you can quickly list those that 
are available:

.. code-block:: console

    $ spack analyze --list-analyzers
    ==> install_files                      : install file listing read from install_manifest.json
    ==> environment_variables              : environment variables parsed from spack-build-env.txt
    ==> config_args                        : config args loaded from spack-configure-args.txt
    ==> abigail                            : Application Binary Interface (ABI) features for objects


In the above, the first three are fairly simple - parsing metadata files from
a package install directory to save

-------------------
Analyzing a Package
-------------------

The analyze command, akin to install, will accept a package spec to perform
an analysis for. The package must be installed. Let's walk through an example
with zlib. We first ask to analyze it. However, since we have more than one
install, we are asked to disambiguate:

.. code-block:: console

    $ spack analyze zlib
    ==> Error: zlib matches multiple packages.
      Matching packages:
        fz2bs56 zlib@1.2.11%gcc@7.5.0 arch=linux-ubuntu18.04-skylake
        sl7m27m zlib@1.2.11%gcc@9.3.0 arch=linux-ubuntu20.04-skylake
      Use a more specific spec.


We can then specify the spec version that we want to analyze:

.. code-block:: console

    $ spack analyze zlib@1.2.11%gcc@7.5.0 arch=linux-ubuntu18.04-skylake

If you don't provide any specific analyzer names, by default all analyzers 
(shown in the ``--list-analyzers`` list) will be run. If an analyzer does not
have any result, it will be skipped. For example, here is a result running for
wget, which didn't have config args, and also did not have the libabigail
analyzer implemented yet:

.. code-block:: console

    $ ls opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/wget-1.20.3-bum6zeaezbuqjhudzphcsyb4avkiizhj/.spack/analyze/
    spack-analyzer-environment-variables.json  spack-analyzer-install-files.json

If you want to run a specific analyzer, ask for it with `--analyzer`. Here we run
spack analyze on libabigail (already installed) _using_ libabigail1

.. code-block:: console

    $ spack analyze --analyzer abigail libabigail

You can now see the abigail results in the analyze folder!

    $ ls opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/wget-1.20.3-bum6zeaezbuqjhudzphcsyb4avkiizhj/.spack/analyze/
    spack-analyzer-environment-variables.json  spack-analyzer-install-files.json  spack-analyzer-libabigail-wget.xml

It is currently flat (not compressed) xml, and will eventually be gzipped when libabigail supports it.


----------------------
Monitoring An Analysis
----------------------

For any kind of analysis, you can
use a `spack monitor <https://github.com/spack/spack-monitor>`_ "Spackmon"
as a server to upload the same run metadata to. You can
follow the instructions in the `spack monitor documentation <https://spack-monitor.readthedocs.org>`_
to first create a server along with a username and token for yourself.
You can then use this guide to interact with the server.

You should first export our spack monitor token and username to the environment:

.. code-block:: console
 
    $ export SPACKMON_TOKEN=50445263afd8f67e59bd79bff597836ee6c05438
    $ export SPACKMON_USER=spacky


By default, the host for your server is expected to be at ``http://127.0.0.1``
with a prefix of ``ms1``, and if this is the case, you can simply add the
``--monitor`` flag to the install command:

.. code-block:: console

    $ spack analyze --monitor wget

If you need to customize the host or the prefix, you can do that as well:

.. code-block:: console

    $ spack analyze --monitor --monitor-prefix monitor --monitor-host https://monitor-service.io wget

If your server doesn't have authentication, you can skip it:

.. code-block:: console

    $ spack analyze --monitor --monitor-disable-auth wget
    
Regardless of your choice, when you run analyze on an installed package (whether
it was installed with ``--monitor`` or not, you'll see the results generating as they did
before, and a message that the monitor server was pinged:

.. code-block:: console

    $ spack analyze --monitor wget
    ==> Writing result to /home/vanessa/Desktop/Code/spack/opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/wget-1.20.3-bum6zeaezbuqjhudzphcsyb4avkiizhj/.spack/analyze/spack-analyzer-install-files.json
    ==> Writing result to /home/vanessa/Desktop/Code/spack/opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/wget-1.20.3-bum6zeaezbuqjhudzphcsyb4avkiizhj/.spack/analyze/spack-analyzer-environment-variables.json
    ==> Writing result to /home/vanessa/Desktop/Code/spack/opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/wget-1.20.3-bum6zeaezbuqjhudzphcsyb4avkiizhj/.spack/analyze/spack-analyzer-install-files.json
    ==> Sending result for wget bin/wget to monitor.
