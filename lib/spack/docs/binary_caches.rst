.. _binary_caches:

Build caches
============================

.. warning:: The feature of build caches is still evolving over time.

Some sites may encourage users to set up their own test environments
before carrying out central installations, or some users prefer to set
up these environments on their own motivation. To reduce the load of
recompiling otherwise identical package specs in different installations,
created build artifacts can be put into binary tarballs, uploaded onto 
your spack mirror and then downloaded and installed by others.


Creating build cache tarballs
-----------------------------

Tarballs of sofware built can be created via 
``spack buildcache create ``.
It allows either to tar up a a package including all
its dependencies. The location for the tarballs
can be given via the ``--directory`` option:

.. code-block:: sh

   $ spack buildcache create -d ~/caches bison
   ==> recursing dependencies
   ==> adding dependency bison@3.0.4%gcc@5.3.1=linux-x86_64^libsigsegv@2.10%gcc@5.3.1=linux-x86_64^m4@1.4.17%gcc@5.3.1+sigsegv=linux-x86_64
   ==> adding dependency m4@1.4.17%gcc@5.3.1+sigsegv=linux-x86_64^libsigsegv@2.10%gcc@5.3.1=linux-x86_64
   ==> adding dependency libsigsegv@2.10%gcc@5.3.1=linux-x86_64
   ==> creating tarball for package bison@3.0.4%gcc@5.3.1=linux-x86_64^libsigsegv@2.10%gcc@5.3.1=linux-x86_64^m4@1.4.17%gcc@5.3.1+sigsegv=linux-x86_64 
   ==> /home/hegner/caches/ubuntu16_04-x86_64/gcc-5.3.1/bison/ubuntu16_04-x86_64-bison-3.0.4-n6naf2v2wt2p5tg3jdveuqufhjwlba7o.tar.gz
   ==> creating tarball for package libsigsegv@2.10%gcc@5.3.1=linux-x86_64 
   ==> /home/hegner/caches/ubuntu16_04-x86_64/gcc-5.3.1/libsigsegv/ubuntu16_04-x86_64-libsigsegv-2.10-klc6t4jq2w6ochuz6xosu6vaujbwszds.tar.gz
   ==> creating tarball for package m4@1.4.17%gcc@5.3.1+sigsegv=linux-x86_64^libsigsegv@2.10%gcc@5.3.1=linux-x86_64 
   ==> /home/hegner/caches/ubuntu16_04-x86_64/gcc-5.3.1/m4/ubuntu16_04-x86_64-m4-1.4.17-6hpdn55vhztd25vxwuamxqo7edmootwv.tar.gz


The created tarballs are put into the directory structure expected for the
spack mirror.


Installing build cache tarballs
--------------------------------

To install binary tarballs, one has to add the corresponding spack mirror
with ``spack mirror add <name> <url>``. Afterwards binaries can be installed
via:

.. code-block:: sh

   $ spack buildcache install bison
   
The package bison and all its dependencies will be downloaded from the 
specified mirror(s). It fails if a package cannot be downloaded.


Relocation
-------------------------------

Initial build and later installation do not necessarily happen at the same
location. Spack provides a very basic relocation capability and corrects for
RPATHs and non-relocatable scripts. However, many packages compile paths into
binary artificats directly. In such cases, the build instructions of this
package would need to be adjusted for better re-locatability.
