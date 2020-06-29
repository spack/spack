# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


#
# This file is part of Spack and sets up the spack environment for
# csh and tcsh.  This includes environment modules and lmod support, and
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
    alias spacktivate    'spack env activate'
    alias _spack_pathadd 'set _pa_args = (\!*) && source $_spack_share_dir/csh/pathadd.csh'

    # Set variables needed by this script
    _spack_pathadd PATH "$SPACK_ROOT/bin"
    eval `spack --print-shell-vars csh`

    # Set up module search paths in the user environment
    set tcl_roots = `echo $_sp_tcl_roots:q | sed 's/:/ /g'`
    set compatible_sys_types = `echo $_sp_compatible_sys_types:q | sed 's/:/ /g'`
    foreach tcl_root ($tcl_roots:q)
        foreach systype ($compatible_sys_types:q)
            _spack_pathadd MODULEPATH "$tcl_root/$systype"
        end
    end

else
    echo "ERROR: Sourcing spack setup-env.csh requires setting SPACK_ROOT to "
    echo "       the root of your spack installation."
endif
