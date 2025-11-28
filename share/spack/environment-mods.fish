# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

function _spack_env_set -a name value
    set -gx $name $value
end

function _spack_env_unset -a name
    set -e $name
end

function _spack_env_append -a name value sep
    if test -n $name
        set -gx $name $$name$sep$value
    else
        set -gx $name $value
    end
end

function _spack_env_prepend -a name value sep
    if test -n $name
        set -gx $name $value$sep$$name
    else
        set -gx $name $value
    end
end

function _spack_env_remove_value -a name value sep
    set as_list (string split $sep -- $$name)
    while true
        if set index (contains --index $value $as_list)
            set -e as_list[$index]
        else
            break
        end
    end
    set -gx $name (string join -- $sep $as_list)
end

function _spack_env_remove_first -a name value sep
    set as_list (string split $sep -- $$name)
    if set index (contains --index $value $as_list)
        set -e as_list[$index]
    end
    set -gx $name (string join -- $sep $as_list)
end

function _spack_env_remove_last -a name value sep
    set as_list (string split $sep -- $$name)

    # reverse list order
    set reversed_list
    for element in $as_list
        set -p reversed_list $element
    end

    # remove first matching element
    if set index (contains --index $value $reversed_list)
        set -e reversed_list[$index]
    end

    # reverse list order
    set as_list
    for element in $reversed_list
        set -p as_list $element
    end

    set -gx $name (string join -- $sep $as_list)
end

function _spack_env_prune_duplicates -a name sep
    set as_list (string split $sep -- $$name)
    set new_list

    for element in $as_list
        if not contains -- $element $new_list
            set -a new_list $element
        end
    end

    set -gx $name (string join -- $sep $new_list)
end
