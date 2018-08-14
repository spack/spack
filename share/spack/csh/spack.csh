########################################################################
# This is a wrapper around the spack command that forwards calls to
# 'spack use' and 'spack unuse' to shell functions.  This in turn
# allows them to be used to invoke dotkit functions.
#
# 'spack use' is smarter than just 'use' because it converts its
# arguments into a unique spack spec that is then passed to dotkit
# commands.  This allows the user to use packages without knowing all
# their installation details.
#
# e.g., rather than requring a full spec for libelf, the user can type:
#
#     spack use libelf
#
# This will first find the available libelf dotkits and use a
# matching one.  If there are two versions of libelf, the user would
# need to be more specific, e.g.:
#
#     spack use libelf@0.8.13
#
# This is very similar to how regular spack commands work and it
# avoids the need to come up with a user-friendly naming scheme for
# spack dotfiles.
########################################################################
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

# Figure out what type of module we're running here.
set _sp_modtype = ""
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
case use:
case unuse:
case load:
case unload:
    set _sp_module_args=""""
    if ( "$_sp_spec" =~ "-*" ) then
        set _sp_module_args = $_sp_spec[1]
        shift _sp_spec
        set _sp_spec = ($_sp_spec)
    endif

    # Here the user has run use or unuse with a spec.  Find a matching
    # spec using 'spack module find', then use the appropriate module
    # tool's commands to add/remove the result from the environment.
    switch ($_sp_subcommand)
        case "use":
            set _sp_full_spec = ( "`\spack $_sp_flags module dotkit find $_sp_spec`" )
            if ( $? == 0 ) then
                use $_sp_module_args $_sp_full_spec
            endif
            breaksw
        case "unuse":
            set _sp_full_spec = ( "`\spack $_sp_flags module dotkit find $_sp_spec`" )
            if ( $? == 0 ) then
                unuse $_sp_module_args $_sp_full_spec
            endif
            breaksw
        case "load":
            set _sp_full_spec = ( "`\spack $_sp_flags module tcl find $_sp_spec`" )
            if ( $? == 0 ) then
                module load $_sp_module_args $_sp_full_spec
            endif
            breaksw
        case "unload":
            set _sp_full_spec = ( "`\spack $_sp_flags module tcl find $_sp_spec`" )
            if ( $? == 0 ) then
                module unload $_sp_module_args $_sp_full_spec
            endif
            breaksw
    endsw
    breaksw

default:
    \spack $_sp_flags $_sp_args
    breaksw
endsw

_sp_end:
unset _sp_args _sp_full_spec _sp_modtype _sp_module_args
unset _sp_sh_cmd _sp_spec _sp_subcommand _sp_flags
