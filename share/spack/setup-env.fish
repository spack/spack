# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


#################################################################################
# This file is part of Spack's fish (friendly interactive shell) support
# Ported from bash (setup-env.sh) by Johannes Blaschke,
#                                    johannes@blaschke.science
#################################################################################



#################################################################################
#
# This file is part of Spack and sets up the spack environment for the friendly
# interactive shell (fish). This includes dotkit support, module support, and it
# also puts spack in your path. The script also checks that at least module
# support exists, and provides suggestions if it doesn't. Source it like this:
#
#    . /path/to/spack/share/spack/setup-env.fish
#
#################################################################################
# This is a wrapper around the spack command that forwards calls to 'spack use'
# and 'spack unuse' to shell functions. This in turn allows them to be used to
# invoke dotkit functions.
#
# 'spack use' is smarter than just 'use' because it converts its arguments into
# a unique spack spec that is then passed to dotkit commands. This allows the
# user to use packages without knowing all their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack use libelf
#
# This will first find the available libelf dotkits and use a matching one. If
# there are two versions of libelf, the user would need to be more specific,
# e.g.:
#
#     spack use libelf@0.8.13
#
# This is very similar to how regular spack commands work and it avoids the need
# to come up with a user-friendly naming scheme for spack dotfiles.
#################################################################################





#
# ALLOCATE_SP_SHARED, and DELETE_SP_SHARED allocate (and delete) temporary
# global variables
#


function allocate_sp_shared -d "allocate shared (global variables)"
    set -gx __sp_remaining_args
    set -gx __sp_subcommand_args
    set -gx __sp_module_args
end



function delete_sp_shared -d "deallocate shared (global variables)"
    set -e __sp_remaining_args
    set -e __sp_subcommand_args
    set -e __sp_module_args
end




#
# STREAM_ARGS and SHIFT_ARGS: helper functions manipulating the `argv` array:
#   -> STREAM_ARGS: echos the `argv` array element-by-element
#   -> SHIFT_ARGS:  echos the `argv` array element-by-element starting with the
#                   second element. If `argv` has only one element, echo the
#                   empty string `""`.
# NOTE: while `stream_args` is not strictly necessary, it adds a nice symmetry
#       to `shift_args`
#


function stream_args -d "echos args as a stream"
    # return the elements of `$argv` as an array
    #  -> since we want to be able to call it as part of `set x (shift_args
    #     $x)`, we return these one-at-a-time using echo... this means that the
    #     sub-command stream will correctly concatenate the output into an array
    for elt in $argv
        echo $elt
    end
end



function shift_args -d "simulates bash shift"
    #
    # Returns argv[2..-1] (as an array)
    #  -> if argv has only 1 element, then returns the empty string. This
    #     simulates the behavior of bash `shift`
    #

    if test -z "$argv[2]"
        # there are no more element, returning the empty string
        echo ""
    else
        # return the next elements `$argv[2..-1]` as an array
        #  -> since we want to be able to call it as part of `set x (shift_args
        #     $x)`, we return these one-at-a-time using echo... this means that
        #     the sub-command stream will correctly concatenate the output into
        #     an array
        for elt in $argv[2..-1]
            echo $elt
        end
    end

end




#
# GET_SP_FLAGS, GET_MOD_ARGS, and CHECK_SP_FLAGS: support functions for
# extracting and checking arguments and flags. Note bash's `shift` operation is
# simulated by tracking the `__sp_remaining_args` array.
#


function get_sp_flags -d "return leading flags"
    #
    # Accumulate initial flags for main spack command. NOTE: Sets the external
    # array: `__sp_remaining_args` containing all unprocessed arguments.
    #

    # initialize argument counter
    set -l i 1

    # iterate over elements (`elt`) in `argv` array
    for elt in $argv

        # match element `elt` of `argv` array to check if it has a leading dash
        if echo $elt | string match -r -q "^-"
            # by echoing the current `elt`, the calling stream accumulates list
            # of valid flags. NOTE that this can also be done by adding to an
            # array, but fish functions can only return integers, so this is the
            # most elegant solution.
            echo $elt
        else
            # bash compatibility: stop when the match first fails. Upon failure,
            # we pack the remainder of `argv` into a global `__sp_remaining_args`
            # array (`i` tracks the index of the next element).
            set __sp_remaining_args (stream_args $argv[$i..-1])
            return
        end

        # increment argument counter: used in place of bash's `shift` command
        set -l i (math $i+1)

    end

    # if all elements in `argv` are matched, make sure that
    # `__sp_remaining_args` is initialized to an empty array (this might be
    # overkill...).
    set __sp_remaining_args
end



function get_mod_args -d "return submodule flags"
    #
    # Accumulate subcommand and submodule arguments. These are accumulated into
    # the external arrays `__sp_subcommand_args`, and `__sp_module_args`. NOTE:
    # Sets the external array: `__sp_remaining_args` containing all unprocessed
    # arguments.
    #

    set __sp_subcommand_args
    set __sp_module_args

    # initialize argument counter
    set -l i 1

    for elt in $argv

        if echo $elt | string match -r -q "^-"

            if test "x$elt" = "x-r"
                set __sp_subcommand_args $__sp_subcommand_args $elt
            else if test "x$elt" = "x--dependencies"
                set __sp_subcommand_args $__sp_subcommand_args $elt
            else
                set __sp_module_args $__sp_module_args $elt
            end

        else
            # bash compatibility: stop when the match first fails. Upon failure,
            # we pack the remainder of `argv` into a global `__sp_remaining_args`
            # array (`i` tracks the index of the next element).
            set __sp_remaining_args (stream_args $argv[$i..-1])
            return
        end

        # increment argument counter: used in place of bash's `shift` command
        set -l i (math $i+1)

    end

    # if all elements in `argv` are matched, make sure that
    # `__sp_remaining_args` is initialized to an empty array (this might be
    # overkill...).
    set __sp_remaining_args
end



function check_sp_flags -d "check spack flags for h/V flags"

    # check if inputs contain h or V flags.

    # skip if called with blank input
    #  -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
    #     undefined, or if it is an array, `test -n $argv` is unpredictable.
    #     Instead, encapsulate `argv` in a string, and test the string instead.
    if test -n "$argv"
        if echo $argv | string match -r -q ".*h.*"
            return 0
        end
        if echo $argv | string match -r -q ".*V.*"
            return 0
        end
    end

    return 1
end



#
# SPACK wrapper function, preprocessing arguments and flags.
#


function spack -d "wrapper for the `spack` command"

    #
    # Allocate temporary global variables used for return extra arguments from
    # functions. NOTE: remember to call delete_sp_shared whenever returning from
    # this function.
    #

    allocate_sp_shared



    #
    # Accumulate initial flags for main spack command
    #

    set __sp_remaining_args # remaining (unparsed) arguments
    set -l sp_flags (get_sp_flags $argv) # sets __sp_remaining_args



    #
    # h and V flags don't require further output parsing.
    #

    if check_sp_flags $sp_flags
        command spack $sp_flags $__sp_remaining_args
        delete_sp_shared
        return 0
    end



    #
    # Isolate subcommand and subcommand specs
    #  -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
    #     undefined, or if it is an array, `test -n $argv` is unpredictable.
    #     Instead, encapsulate `argv` in a string, and test the string.
    #

    set -l sp_subcommand ""

    if test -n "$__sp_remaining_args[1]"
        set sp_subcommand $__sp_remaining_args[1]
        set __sp_remaining_args (shift_args $__sp_remaining_args)  # simulates bash shift
    end

    set -l sp_spec $__sp_remaining_args


    #
    # Filter out cd, and use and unuse (or similarly module's load and unload).
    # For any other commands, just run the command.
    #

    switch $sp_subcommand

        # CASE: spack subcommand is `cd`: if the sub command arg is `-h`, nothing
        # further needs to be done. Otherwise, test the location referring the
        # subcommand and cd there (if it exists).

        case "cd"

            set -l sp_arg ""

            # Extract the first subcommand argument:
            # -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
            #    undefined, or if it is an array, `test -n $argv` is
            #    unpredictable. Instead, encapsulate `argv` in a string, and test
            #    the string.
            if test -n "$__sp_remaining_args[1]"
                set sp_arg $__sp_remaining_args[1]
                set __sp_remaining_args (shift_args $__sp_remaining_args) # simulates bash shift
            end

            if test "x$sp_arg" = "x-h" || test "x$sp_arg" = "x--help"
                # nothing more needs to be done for `-h` or `--help`
                command spack cd -h
            else
                # extract location using the subcommand (fish `(...)`)
                set -l LOC (command spack location $sp_arg $__sp_remaining_args)

                # test location and cd if exists:
                if test -d "$LOC"
                    cd $LOC
                else
                    delete_sp_shared
                    return 1
                end

            end

            delete_sp_shared
            return 0


        # CASE: spack subcommand is `env`:

        case "env"

            set -l sp_arg ""

            # Extract the first subcommand argument:
            # -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
            #    undefined, or if it is an array, `test -n $argv` is
            #    unpredictable. Instead, encapsulate `argv` in a string, and test
            #    the string.
            if test -n "$__sp_remaining_args[1]"
                set sp_arg $__sp_remaining_args[1]
                set __sp_remaining_args (shift_args $__sp_remaining_args) # simulates bash shift
            end

            if test "x$sp_arg" = "x-h" || test "x$sp_arg" = "x--help"
                # nothing more needs to be done for `-h` or `--help`
                command spack cd -h
            else
                switch $sp_arg
                    case "activate"
                        set -l _a (stream_args $__sp_remaining_args)
                    case "deactivate"
                end
            end
 



        # CASE: spack subcommand is either `use`, `unuse`, `load`, or `unload`.
        # These statements deal with the technical details of actually using
        # modules. Especially to deal with the substituting latest version
        # numbers to the module command.

        case "use" or "unuse" or "load" or "unload"

            # Shift any other args for use off before parsing spec.
            set __sp_subcommand_args          # sets: __sp_remaining_args
            set __sp_module_args              #       __sp_subcommand_args
            get_mod_args $__sp_remaining_args #       __sp_module_args

            set sp_spec $__sp_remaining_args


            # Here the user has run use or unuse with a spec. Find a matching spec
            # using 'spack module find', then use the appropriate module tool's
            # commands to add/remove the result from the environment. If spack
            # module command comes back with an error, do nothing.

            switch $sp_subcommand

                case "use"
                    set -l dotkit_args $__sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module dotkit find $dotkit_args)
                        use $__sp_module_args $sp_full_spec
                    else
                        delete_sp_shared
                        return 1
                    end

                case "unuse"
                    set -l dotkit_args $__sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module dotkit find $dotkit_args)
                        unuse $__sp_module_args $sp_full_spec
                    else
                        delete_sp_shared
                        return 1
                    end

                case "load"
                    set -l tcl_args $__sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module tcl find $tcl_args)
                        # This is a strange behavior of `modulecmd fish load
                        # $args`. In fish, `load` returns a list of `set`
                        # imperatives rather than applying them outright. So
                        # what we'll do is to dump them into a `load_cmd` array
                        # and then evaluate the contents.
                        set load_cmd (module load $__sp_module_args $sp_full_spec)
                        eval $load_cmd
                    else
                        delete_sp_shared
                        return 1
                    end

                case "unload"
                    set -l tcl_args $__sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module tcl find $tcl_args)
                        # This is a strange behavior of `modulecmd fish load
                        # $args`. In fish, `unload` returns a list of `set`
                        # imperatives rather than applying them outright. So
                        # what we'll do is to dump them into a `load_cmd` array
                        # and then evaluate the contents.
                        set unload_cmd (module unload $__sp_module_args $sp_full_spec)
                        eval $unload_cmd
                    else
                        delete_sp_shared
                        return 1
                    end
            end


        # CASE: Catch-all

        case "*"
            command spack $argv

    end

    delete_sp_shared
end



#################################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
#################################################################################
function spack_pathadd
    # If no variable name is supplied, just append to PATH otherwise append to
    # that variable.

    if test -n "$argv[2]"
        set pa_varname $argv[1]
        set pa_new_path $argv[2]
    else
        true # this is a bit of a strange hack! when the test in the if
             # statement fails, the `status` flag is set to 1. `true` resets
             # this. since `set` passes `status` along, we thus avoid the
             # function returning 1 by mistake.
        set pa_varname PATH
        set pa_new_path $argv[1]
    end

    set pa_oldvalue $$pa_varname

    if test -d "$pa_new_path"
        if not string match -q "$pa_new_path" $pa_oldvalue
            if test -n "$pa_oldvalue"
                set $pa_varname $pa_new_path $pa_oldvalue
            else
                true # this is a bit of a strange hack! when the test in the if
                     # statement fails, the `status` flag is set to 1. `true`
                     # resets this. since `set` passes `status` along, we thus
                     # avoid the function returning 1 by mistake.
                set $pa_varname $pa_new_path
            end
        end
    end
end






#
# Figure out where this file is. Below code only needs to work in fish
#
set -l sp_source_file (status -f)  # name of current file



#
# Find root directory and add bin to path.
#
set -l sp_share_dir (realpath (dirname $sp_source_file))
set -l sp_prefix (realpath (dirname (dirname $sp_share_dir)))
spack_pathadd fish_user_paths "$sp_prefix/bin"
set -xg SPACK_ROOT $sp_prefix



#
# No need to determine which shell is being used (obviously it's fish)
#
set -xg SPACK_SHELL "fish"



#
# Check whether we need environment-variables (module) <= `use` is not available
#
set -l need_module "no"
if not functions -q use and not functions -q module
    set need_module "yes"
end



#
# Make environment-modules available to shell
#
function sp_apply_shell_vars -d "applies expressions of the type `a='b'` as `set a b`"
    set -l expr_token (string trim -c "'" (string split "=" $argv))
    set -xg $expr_token[1] $expr_token[2]
end

if test "$need_module" = "yes"
    set -l sp_shell_vars (command spack --print-shell-vars sh,modules)

    for sp_var_expr in $sp_shell_vars
        sp_apply_shell_vars $sp_var_expr
    end

    # _sp_module_prefix is set by spack --print-sh-vars
    if test "$_sp_module_prefix" != "not_installed"
        set -xg MODULE_PREFIX $_sp_module_prefix
        set -xg fish_user_paths "$MODULE_PREFIX/bin" $fish_user_paths
    end

else

    set -l sp_shell_vars (command spack --print-shell-vars sh)

    for sp_var_expr in $sp_shell_vars
        sp_apply_shell_vars $sp_var_expr
    end

end

function module -d "wrapper for the `module` command to point at Spack's modules instance"
    eval $MODULE_PREFIX/bin/modulecmd $SPACK_SHELL $argv
end



#
# set module system roots
#
set -xg DK_NODE
set -xg MODULEPATH
spack_pathadd DK_NODE "$_sp_dotkit_root/$_sp_sys_type"
spack_pathadd MODULEPATH "$_sp_tcl_root/$_sp_sys_type"
