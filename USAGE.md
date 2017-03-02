Bootstrap
=======

For Pi users:

	$ ./bootstrap user --install

For rpm builders:

	$ ./bootstrap rpm --install

For compiler builders:

	$ ./bootstrap system --install

Spack shell support
======

And Spack shell support in `.bashrc` or `.zshrc`:

	export SPACK_ROOT=PATH_TO_SPACK
	source $SPACK_ROOT/share/spack/setup-env.sh

Spack basics
=======

Listing versions
------

SYNOSYS

	spack versions PKGNAME

Example:

	$ spack version gcc

Search packages in spack repo
------

Search by name:

	$ spack list sql

Search by description:

	$ spack list --search-description documentation

List package opitions
------

SYNOSYS

	spack info PKGNAME	

Examples:

	$ spack info python
	$ spack info python@2.7.13 


Installing packages
------

SYNOSYS

	spack install PKGSPEC

Examples:

Build Python 2.7.13 with GCC 5.4.6.
	
	$ spack install python@2.7.13 %gcc@5.4.0

Seeing installed packages
------

SYNOSYS
	
	spack find [--deps] [--paths] [--long] PKGNAME 

Examples:

	spack find gcc	

Locate installed packages
------

	$ spack locate -i gcc
	
Create filesystem views of installed packages
------

SYNOSYS
	
	spack view [symlink|hardlink|view] PKGNAME 
