.. _binary_caches:

Build caches
============

Some sites may encourage users to set up their own test environments
before carrying out central installations, or some users prefer to set
up these environments on their own motivation. To reduce the load of
recompiling otherwise identical package specs in different installations,
installed packages can be put into build cache tarballs, uploaded to 
your spack mirror and then downloaded and installed by others.


Creating build cache files
--------------------------

A compressed tarball of an installed package is created. Tarballs are created
for all of its link and run dependency packages as well. Compressed tarballs are
signed with gpg and signature and tarball and put in a ".spack" file. Optionally
, the rpaths ( and ids and deps on macOS ) can be changed to paths relative to 
the spack install tree before the tarball is created.

Build caches are created via:

.. code-block:: sh

   $ spack buildcache create 


Finding or installing build cache files
---------------------------------------

To find build caches or install build caches, a spack mirror must be configured
with
 
``spack mirror add <name> <url>``. 

Build caches are found via: 

.. code-block:: sh

   $ spack buildcache list

Build caches are installed via:

.. code-block:: sh

   $ spack buildcache install 
   

Relocation
----------

Initial build and later installation do not necessarily happen at the same 
location. Spack provides a relocation capability and corrects for RPATHs and 
non-relocatable scripts. However, many packages compile paths into binary 
artificats directly. In such cases, the build instructions of this package would
need to be adjusted for better re-locatability.


Usage 
-----
spack buildcache create <>
^^^^^^^^^^^^^^^^^^^^^^^^^^
Create tarball of installed spack package and all dependencies. 
Tarballs is checksummed and signed if gpg2 is available.
Places them in a directory build_cache that can be copied to a mirror.
Commands like "spack buildcache install" will search it for pre-compiled packages.
 

options:

-d <path> : directory in which "build_cache" direcory is created, defaults to "."
-f : overwrite ".spack" file in "build_cache" directory if it exists
-k <key> : the key to sign package with. In the case where multiple keys exist, the package will be unsigned unless -k is used.
-r : make paths in binaries relative before creating tarball
-y : answer yes to all create unsigned "build_cache" questions
<> : list of package specs or package hashes with leading /

spack buildcache list <>
^^^^^^^^^^^^^^^^^^^^^^^^
Retrieves all specs for build caches available on a spack mirror.

options:

<> string to be matched to matched to begining of listed concretized short 
specs, eg. "spack buildcache list gcc" with print only commands to install gcc
package(s)

spack buildcache install <>
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Retrieves all specs for build caches available on a spack mirror and installs build caches 
with specs matching the specs or hashes input. 

options:

-f : remove install directory if it exists before unpacking tarball
-y : answer yes to all to don't verify package with gpg questions
<> : list of package specs or package hashes with leading /

spack buildcache keys
^^^^^^^^^^^^^^^^^^^^^
List public keys available on spack mirror.

options:

-i : trust the keys downloaded with prompt for each
-y : answer yes to all trust all keys downloaded
