##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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
    _spack_pathadd DK_NODE    "$_sp_dotkit_root/$_sp_sys_type"
    _spack_pathadd MODULEPATH "$_sp_tcl_root/$_sp_sys_type"
else
    echo "ERROR: Sourcing spack setup-env.csh requires setting SPACK_ROOT to the root of your spack installation"
endif
