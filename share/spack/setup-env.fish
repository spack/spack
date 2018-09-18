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




function stream_args
    for elt in $argv
        echo $elt
    end
end



function shift_args -d "simulates bash shift"
    #
    # Returns argv[2..-1] (as an array)
    #  -> if argv has only 1 element, then returns the empty string
    # simulates the behavior of bash `shift`
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

        #for elt in $argv[2..-1]
        #    echo $elt
        #end
        echo (stream_args $argv[2..-1])

    end

end





function get_sp_flags -d "return leading flags"
    #
    # accumulate initial flags for main spack command
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
            # we pack the remainder of `argv` into a global `remaining_args`
            # array (`i` tracks the index of the next element).
            set remaining_args (stream_args $argv[$i..-1])
            return
        end

        # increment argument counter: used in place of bash's `shift` command
        set -l i (math $i+1)

    end

    # if all elements in `argv` are matched, make sure that `remaining_args` is
    # initialized to an empty array (this might be overkill...).
    set remaining_args ""
end



function get_mod_args -d "return submodule flags"

    set sp_subcommand_args ""
    set sp_module_args ""

    # initialize argument counter
    set -l i 0

    for elt in $argv

        if echo $elt | string match -r -q "^-"

            if test "x$elt" = "x-r"
                set sp_subcommand_args $sp_subcommand_args $elt
            else if test "x$elt" = "x--dependencies"
                set sp_subcommand_args $sp_subcommand_args $elt
            else
                set sp_module_args $sp_module_args $elt
            end

        else
            # bash compatibility: stop when the match first fails. Upon failure,
            # we pack the remainder of `argv` into a global `remaining_args`
            # array (`i` tracks the index of the next element).
            set remaining_args (shift_args $argv[$i..-1])
            return
        end

        # increment argument counter: used in place of bash's `shift` command
        set -l i (math $i+1)

    end

    # if all elements in `argv` are matched, make sure that `remaining_args` is
    # initialized to an empty array (this might be overkill...).
    set remaining_args ""
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




function spack -d "wrapper for the `spack` command"

    #
    # save raw arguments into an array before butchering them
    #

    set -l args $argv



    #
    # accumulate initial flags for main spack command
    #

    set -g remaining_args "" # remaining (unparsed) arguments
    set -l sp_flags (get_sp_flags $argv)



    #
    # h and V flags don't require further output parsing.
    #

    if check_sp_flags $sp_flags
        command spack $sp_flags $remaining_args
    end



    #
    # isolate subcommand and subcommand specs
    #  -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
    #     undefined, or if it is an array, `test -n $argv` is unpredictable.
    #     Instead, encapsulate `argv` in a string, and test the string instead.
    #

    set sp_subcommand ""

    if test -n "$remaining_args[1]"
        set sp_subcommand $remaining_args[1]
        set remaining_args (shift_args $remaining_args)     # simulates bash shift
    end

    set -l sp_spec $remaining_args
    echo "sp_subcommand = $sp_subcommand"
    echo "sp_spec = $sp_spec"


    #
    # Filter out use and unuse. For any other commands, just run the command.
    #

    switch $sp_subcommand

        # CASE: spack subcommand is `cd`: if the sub command arg is `-h`, nothing
        # further needs to be done. Otherwise, test the location referring the
        # subcommand and cd there (if it exists).

        case "cd"

            set -l sp_arg ""

            # Extract the first subcommand argument:
            # -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
            #    undefined, or if it is an array, `test -n $argv` is unpredictable.
            #    Instead, encapsulate `argv` in a string, and test the string
            #    instead.
            if test -n "$remaining_args[1]"
                set sp_arg $remaining_args[1]
                set remaining_args (shift_args $remaining_args)     # simulates bash shift
            end

            echo $sp_arg

            if test "x$sp_arg" = "x-h"
                # nothing more needs to be done for `-h`
                command spack cd -h
            else
                # extract location using the subcommand (fish `(...)`)
                set -l LOC (command spack location $sp_arg $remaining_args)
                echo $LOC

                # test location and cd if exists:
                if test -d "$LOC"
                    cd $LOC
                else
                    exit 1
                end

            end

            exit 0


            # CASE: spack subcommand is either `use`, `unuse`, `load`, or `unload`.
            # These statements deal with the technical details of actually using
            # modules.

        case "use" or "unuse" or "load" or "unload"

            # Shift any other args for use off before parsing spec.
            set sp_subcommand_args ""
            set sp_module_args ""

            get_mod_args $remaining_args

            set sp_spec $remaining_args


            # Here the user has run use or unuse with a spec. Find a matching spec
            # using 'spack module find', then use the appropriate module tool's
            # commands to add/remove the result from the environment. If spack
            # module command comes back with an error, do nothing.

            switch $sp_subcommand

                case "use"
                    set -l dotkit_args $sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module dotkit find $dotkit_args)
                        use $sp_module_args $sp_full_spec
                    else
                        exit 1
                    end

                case "unuse"
                    set -l dotkit_args $sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module dotkit find $dotkit_args)
                        unuse $sp_module_args $sp_full_spec
                    else
                        exit 1
                    end

                case "load"
                    set -l tcl_args $sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module tcl find $tcl_args)
                        module load $sp_module_args $sp_full_spec
                    else
                        exit 1
                    end

                case "unload"
                    set -l tcl_args $sp_subcommand_args $sp_spec
                    if set sp_full_spec (command spack $sp_flags module tcl find $tcl_args)
                        module unload $sp_module_args $sp_full_spec
                    else
                        exit 1
                    end
            end


            # CASE: Catch-all
        case "*"
            command spack $argv

    end
end



#################################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
#################################################################################
function spack_pathadd
    # If no variable name is supplied, just append to PATH otherwise append to
    # that variable.

    set -l pa_varname PATH
    set -l pa_new_path $argv[1]

    if test -n "$argv[2]"
        set pa_varname $argv[1]
        set pa_new_path $argv[2]
    end

    set -l pa_oldvalue $$pa_varname

    if test -d "$pa_new_path"
        if string match -q "$pa_new_path" $pa_oldvalue
        else
            if test -n "$pa_oldvalue"
                set -g $pa_varname $pa_new_path $pa_oldvalue
            else
                set -g $pa_varname $pa_new_path
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
set -g SPACK_ROOT $sp_prefix



#
# No need to determine which shell is being used (obviously it's fish)
#
set -g SPACK_SHELL "fish"



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
    set -g $expr_token[1] $expr_token[2]
end

if test "$need_module" = "yes"
    set -l sp_shell_vars (command spack --print-shell-vars sh,modules)

    for sp_var_expr in $sp_shell_vars
        sp_apply_shell_vars $sp_var_expr
    end

    # _sp_module_prefix is set by spack --print-sh-vars
    if test "$_sp_module_prefix" != "not_installed"
        set -g MODULE_PREFIX $_sp_module_prefix
        set -g fish_user_paths "$MODULE_PREFIX/bin" $fish_user_paths
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
spack_pathadd DK_NODE    "$_sp_dotkit_root/$_sp_sys_type"
spack_pathadd MODULEPATH "$_sp_tcl_root%/$_sp_sys_type"

