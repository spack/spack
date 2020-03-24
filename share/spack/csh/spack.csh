# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

########################################################################
# This is a wrapper around the spack command that forwards calls to
# 'spack load' and 'spack unload' to shell functions.  This in turn
# allows them to be used to invoke environment-modules functions.
#
# 'spack load' is smarter than just 'load' because it converts its
# arguments into a unique Spack spec that is then passed to environment-modules
# commands.  This allows the user to use packages without knowing all
# their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack load libelf
#
# This will first find the available libelf module file and use a
# matching one.  If there are two versions of libelf, the user would
# need to be more specific, e.g.:
#
#     spack load libelf@0.8.13
#
# This is very similar to how regular spack commands work and it
# avoids the need to come up with a user-friendly naming scheme for
# spack module files.
########################################################################
# Store LD_LIBRARY_PATH variables from spack shell function
# This is necessary because MacOS System Integrity Protection clears
# (DY?)LD_LIBRARY_PATH variables on process start.
if ( ${?LD_LIBRARY_PATH} ) then
    setenv SPACK_LD_LIBRARY_PATH $LD_LIBRARY_PATH
endif
if ( ${?DYLD_LIBRARY_PATH} ) then
    setenv SPACK_DYLD_LIBRARY_PATH $DYLD_LIBRARY_PATH
endif

# accumulate initial flags for main spack command
set _sp_flags = ""
while ( $#_sp_args > 0 )
    if ( "$_sp_args[1]" !~ "-*" ) break
    set _sp_flags = "$_sp_flags $_sp_args[1]"
    shift _sp_args
end

# h and V flags don't require further output parsing.
if ( "$_sp_flags" =~ *h* || "$_sp_flags" =~ *V* ) then
    \spack $_sp_flags $_sp_args
    goto _sp_end
endif

# Set up args -- we want a subcommand and a spec.
set _sp_subcommand=""
set _sp_spec=""
[ $#_sp_args -gt 0 ] && set _sp_subcommand = ($_sp_args[1])
[ $#_sp_args -gt 1 ] && set _sp_spec = ($_sp_args[2-])

# Run subcommand
switch ($_sp_subcommand)
case cd:
    shift _sp_args  # get rid of 'cd'

    set _sp_arg=""
    [ $#_sp_args -gt 0 ] && set _sp_arg = ($_sp_args[1])
    shift _sp_args

    if ( "$_sp_arg" == "-h" ) then
        \spack cd -h
    else
        cd `\spack location $_sp_arg $_sp_args`
    endif
    breaksw
case env:
    shift _sp_args  # get rid of 'env'

    set _sp_arg=""
    [ $#_sp_args -gt 0 ] && set _sp_arg = ($_sp_args[1])

    if ( "$_sp_arg" == "-h" ) then
        \spack env -h
    else
        switch ($_sp_arg)
            case activate:
                set _sp_env_arg=""
                [ $#_sp_args -gt 1 ] && set _sp_env_arg = ($_sp_args[2])

                if ( "$_sp_env_arg" == "" || "$_sp_args" =~ "*--sh*" || "$_sp_args" =~ "*--csh*" || "$_sp_args" =~ "*-h*" ) then
                    # no args or args contain -h/--help, --sh, or --csh: just execute
                    \spack $_sp_flags env $_sp_args
                else
                    shift _sp_args  # consume 'activate' or 'deactivate'
                    # actual call to activate: source the output
                    eval `\spack $_sp_flags env activate --csh $_sp_args`
                endif
                breaksw
            case deactivate:
                set _sp_env_arg=""
                [ $#_sp_args -gt 1 ] && set _sp_env_arg = ($_sp_args[2])

                if ( "$_sp_env_arg" != "" ) then
                    # with args: execute the command
                    \spack $_sp_flags env $_sp_args
                else
                    # no args: source the output
                    eval `\spack $_sp_flags env deactivate --csh`
                endif
                breaksw
            default:
                echo default
                \spack $_sp_flags env $_sp_args
                breaksw
        endsw
    endif
case load:
case unload:
    # Space in `-h` portion is important for differentiating -h option
    # from variants that begin with "h" or packages with "-h" in name
    if ( "$_sp_spec" =~ "*--sh*" || "$_sp_spec" =~ "*--csh*" || \
         " $_sp_spec" =~ "* -h*" || "$_sp_spec" =~ "*--help*") then
        # IF a shell is given, print shell output
        \spack $_sp_flags $_sp_subcommand $_sp_spec
    else
        # otherwise eval with csh
        eval `\spack $_sp_flags $_sp_subcommand --csh $_sp_spec || \
             echo "exit 1"`
    endif
    breaksw

default:
    \spack $_sp_flags $_sp_args
    breaksw
endsw

_sp_end:
unset _sp_args _sp_full_spec _sp_sh_cmd _sp_spec _sp_subcommand _sp_flags
unset _sp_arg _sp_env_arg
