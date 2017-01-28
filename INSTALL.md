Installing Spack
=======

	$ git clone https://github.com/llnl/spack.git

And Spack's shell support in `.bashrc` or `.zshrc`

	export SPACK_ROOT=/path/to/spack
	source $SPACK_ROOT/share/spack/setup-env.sh

Spack customization
=======

Compiler
------

Check available compilers.

	$ spack compilers

Find pre-installed compilers by searching a given path. Or run `spack compiler find` without arguments for auto detection.

	$ module purge; module load icc/14.0
	$ spack compiler find
	$ module purge; module load icc/15.0
	$ spack compiler find
	$ module purge; module load icc/16.0
	$ spack compiler find

Customize compiler names and dependent modules in `~/.spack/linux/compilers.yaml`. Then check newly-added compilers. A pre-configured compiler file is shipped with this project which can be invoked by:
	
	$ ln -sf ./compilers.yaml ~/.spack/linux/

List available compilers:

	$ spack compilers 

List compiler location:
	
	$ spack location --install-dir gcc@5.4.0 

Library preference
------

Default compilers and MPI proivders can be specified in `~/.spack/package.yaml`. A preconfigured one is shipped with this project which can be invoked by: 

	$ ln -sf ./package.yaml ~/.spack

Installation Prefix
------

Installation prefix can be configured in `~/.spack/config.yaml`. A pre-configured one can be invoked via:

	$ ln -sf ./config.yaml ~/.spack/

Spack basics
=======

Find available packages
------

SYNOSYS
	
	spack find PKGNAME 

Examples:

	spack find gcc	

List versions
------

SYNOSYS

	spack versions PKGNAME

Example:

	$ spack version gcc

List package opitions
------

SYNOSYS

	spack info PKGNAME	

Examples:

	$ spack info python
	$ spack info python@2.7.13 

Install packages
------

SYNOSYS

	spack install PKGSPEC

Examples:

Build Python 2.7.13 with GCC 5.4.6.
	
	$ spack install python@2.7.13 %gcc@5.4.0
