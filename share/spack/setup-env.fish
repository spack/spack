#################################################################################
# This file is part of Spack.
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








function get_sp_flags -d "return leading flags"
    #
    # accumulate initial flags for main spack command
    #

    # initialize argument counter
    set i 0

    # iterate over elements (`elt`) in `argv` array
    for elt in $argv

        # increment argument counter: used in place of bash's `shift` command
        set i (math $i+1)

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
            set -x remaining_args $argv[$i..-1]
            return
        end
    end

    # if all elements in `argv` are matched, make sure that `remaining_args` is
    # initialized to an empty array (this might be overkill...).
    set -x remaining_args ""
end

function check_sp_flags -d "check spack flags for h/V flags"

    # check if inputs contain h or V flags.

    # skip if called with blank input
    #  -> bit of a hack: test -n and test -z are not working atm (=> future fish)
    if count $argv > /dev/null
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
# save raw arguments into an array before butchering them
#

set args $argv



#
# accumulate initial flags for main spack command
#

set remaining_args "" # remaining (unparsed) arguments
set sp_flags (get_sp_flags $argv)



#
# h and V flags don't require further output parsing.
#

if check_sp_flags $sp_flags
    command spack $sp_flags $remaining_args
end



#
# isolate subcommand and subcommand specs
#  -> bit of a hack: test -n and test -z are not working atm (=> future fish)
#

set sp_subcommand ""
set sp_spec $remaining_args
if count $remaining_args[1] > /dev/null
    set sp_subcommand $remaining_args[1]
    set sp_spec $remaining_args[2..-1]
end



# temporary debugging statements

echo "sp_flags = $sp_flags"
echo "remaining_args = $remaining_args"
echo "sp_subcommand = $sp_subcommand"
echo "sp_spec = $sp_spec"
