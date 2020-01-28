# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

if [ "$CURRENTLY_BUILDING_DOCKER_IMAGE" '!=' '1' ] ; then

if [ x$SPACK_PROMPT '!=' x0 ] ; then

__tmp="`mktemp -d`"

__trylock() {
    local dir
    dir="$__tmp/$1.lock"
    mkdir "$dir" &>/dev/null
    return $?
}

__queue_init() {
    local r
    local w

    mkdir "$__tmp/$1.read.lock" ; r=$?
    mkdir "$__tmp/$1.write.lock" ; w=$?

    if [ "$r" '=' '0' -a "$w" '=' '0' ] ; then
        return 0
    else
        return 1
    fi
}

__queue_try_read() {
    __trylock "$1.read"
    return $?
}

__queue_try_write() {
    __trylock "$1.write"
    return $?
}

__queue_make_readable() {
    rm -r "$__tmp/$1.read.lock" &>/dev/null
    return $?
}

__queue_make_writable() {
    rm -r "$__tmp/$1.write.lock" &>/dev/null
    return $?
}

__read() {
    cat "$__tmp/$1" 2> /dev/null
    return $?
}

__write() {
    cat > "$__tmp/$1" 2> /dev/null
    return $?
}

__revparse_head() {
    head="`git -C "$SPACK_ROOT" rev-parse $@ HEAD 2>/dev/null`"
    result="$?"
    if [ "$result" '!=' '0' ] ; then
        head="`git --git-dir="$SPACK_ROOT"/.git \\
              --work-tree="$SPACK_ROOT" rev-parse $@ HEAD 2>/dev/null`"
        result="$?"
    fi

    echo "$head"
    return $result
}

__git_head() {
    head="`__revparse_head --abbrev-ref`"
    if [ "$?" '=' '0' ] ; then
        if [ "$head" '=' 'HEAD' ] ; then
            head="`__revparse_head | cut -c1-8`..."
        fi

        echo "$head"
    fi
}

__update_prompt() {
    local prompt
    prompt=''
    linux_distro="$DOCKERFILE_DISTRO"
    if [ -n "$linux_distro" ] ; then
        linux_distro='\[\e[1;34m\][\[\e[0;34m\]'"$linux_distro"'\[\e[1;34m\]]'
        if [ -n "$prompt" ] ; then
            prompt="$prompt "
        fi
        prompt="$prompt$linux_distro"
    fi

    git_head="`__git_head`"

    if [ -n "$git_head" ] ; then
        git_head='\[\e[1;32m\](\[\e[0;32m\]'"$git_head"'\[\e[1;32m\])'
        if [ -n "$prompt" ] ; then
            prompt="$prompt "
        fi
        prompt="$prompt$git_head"
    fi

    if [ -n "$prompt" ] ; then
        prompt="$prompt "
    fi
    prompt="$prompt"'\[\e[0;m\]\W: '
    echo "$prompt" | __write prompt
}

set -m
(
    __queue_init query
    __queue_init prompt

    __update_prompt
    __queue_make_readable prompt

    __queue_make_writable query

    while sleep 0.010 ; do
        last_q_time=''

        while sleep 0.010 ; do
            q_time="`date +%s%N`"
            if __queue_try_read query ; then
                last_q_time="$q_time"
                __queue_make_writable query
            fi

            if [ -n "$last_q_time" -a \
                "$(( (q_time - last_q_time)/10000000 > 100 ))" '=' '1' ] ; then
                break
            fi
        done

        __update_prompt
        __queue_make_readable prompt
    done
) &>/dev/null &
set +m

__update_prompt_main_first_call=1
__update_prompt_main() {
    if [ "$__update_prompt_main_first_call" '=' '1' ] ; then
        while sleep 0.001 ; do
            if __queue_try_read prompt ; then
                PS1="`__read prompt`"
                break
            fi
        done
        __update_prompt_main_first_call=0
    else
        if __queue_try_read prompt ; then
            PS1="`__read prompt`"
        fi
    fi

    if __queue_try_write query ; then
        __queue_make_readable query
    fi
}

PROMPT_COMMAND=__update_prompt_main

fi # [ x$SPACK_PROMPT '!=' x0 ]

fi # [ "$CURRENTLY_BUILDING_DOCKER_IMAGE" '!=' '1' ]
