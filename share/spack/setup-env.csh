# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


#
# This file is part of Spack and sets up the spack environment for
# csh and tcsh.  This includes dotkit support, module support, and
# it also puts spack in your path.  Source it like this:
#
#    setenv SPACK_ROOT /path/to/spack
#    source $SPACK_ROOT/share/spack/setup-env.csh
#
if ($?SPACK_ROOT) then
    set _spack_source_file = $SPACK_ROOT/share/spack/setup-env.csh
    set _spack_share_dir   = $SPACK_ROOT/share/spack

    # Command aliases point at separate source files
    alias spack          'set _sp_args = (\!*); source $_spack_share_dir/csh/spack.csh'
    alias _spack_pathadd 'set _pa_args = (\!*) && source $_spack_share_dir/csh/pathadd.csh'

    # Set variables needed by this script
    _spack_pathadd PATH "$SPACK_ROOT/bin"
    eval `spack --print-shell-vars csh`

    # Set up modules and dotkit search paths in the user environment
    set tcl_roots = `echo $_sp_tcl_roots:q | sed 's/:/ /g'`
    foreach tcl_root ($tcl_roots:q)
        _spack_pathadd MODULEPATH "$tcl_root/$_sp_sys_type"
    end

    set dotkit_roots = `echo $_sp_dotkit_roots:q | sed 's/:/ /g'`
    foreach dotkit_root ($dotkit_roots)
        _spack_pathadd DK_NODE "$dotkit_root/$_sp_sys_type"
    end
else
    echo "ERROR: Sourcing spack setup-env.csh requires setting SPACK_ROOT to "
    echo "       the root of your spack installation."
endif
