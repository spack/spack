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
# Set up args -- we want a subcommand and a spec.
set _sp_subcommand="";
set _sp_spec="";
[ $#_sp_args -gt 0 ] && set _sp_subcommand = ($_sp_args[1]);
[ $#_sp_args -gt 1 ] && set _sp_spec = ($_sp_args[2-]);

# Figure out what type of module we're running here.
set _sp_modtype = "";
switch ($_sp_subcommand)
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
    # Translate the parameter into pieces of a command.
    # _sp_modtype is an arg to spack module find, and
    # _sp_sh_cmd is the equivalent shell command.
    switch ($_sp_subcommand)
        case use:
        case unuse:
            set _sp_modtype = dotkit
            set _sp_sh_cmd = $_sp_subcommand
            breaksw
        case load:
        case unload:
            set _sp_modtype = tcl
            set _sp_sh_cmd = ( module $_sp_subcommand )
            breaksw
    endsw

    # Here the user has run use or unuse with a spec.  Find a matching
    # spec using 'spack module find', then use the appropriate module
    # tool's commands to add/remove the result from the environment.
    # If spack module command comes back with an error, do nothing.
    if { set _sp_full_spec = `command spack module find $_sp_modtype $_sp_spec` } then
        echo $_sp_sh_cmd $_sp_module_args $_sp_full_spec
    endif
default:
    command spack $_sp_args
endsw

unset _sp_args _sp_full_spec _sp_modtype _sp_module_args _sp_sh_cmd _sp_spec _sp_subcommand
