#! /usr/bin/env bash
#
# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

function prefix_tokens() {
    line="$1" ; shift
    nprefix="$1"

    line="${line::$nprefix} "
    echo "${line::$nprefix}"
}


# read file contents, or stdin
cat "$1" |

# remove blank lines
grep -v '^ *$' |

# remove leading whitespace
sed 's/^ *//g' |

# remove comments
grep -v '^#.*' |

# remove trailing whitespace
sed 's/ *$//g' |

# remove extraneous whitespace
sed 's/  */ /g' |

# mask out subsections
(
    stack_level=1
    mask_level=1

    while read LINE ; do
        try_print=1

        if [ "$( prefix_tokens "$LINE" 10 )" '=' 'MASK PUSH ' ] ; then
            tmp="$stack_level"
            stack_level="$(( stack_level + 1 ))"
            if [ "$mask_level" '=' "$tmp" ] ; then
                mask_level="$stack_level"
            fi
            try_print=0
        elif [ "$( prefix_tokens "$LINE" 9 )" '=' 'MASK POP ' ] ; then
            stack_level="$(( stack_level - 1 ))"
            if [ "$mask_level" -gt "$stack_level" ] ; then
                mask_level="$stack_level"
            fi
            try_print=0
        elif [ "$( prefix_tokens "$LINE" 5 )" '=' 'MASK ' ] ; then
            if [ "$(( mask_level + 1 ))" -ge "$stack_level" ] ; then
                mask_level="$stack_level"
                eval "${LINE:5}"
                if [ "$?" '!=' 0 ] ; then
                    mask_level="$(( mask_level - 1 ))"
                fi
            fi
            try_print=0
        fi

        if [ "$stack_level" -lt 1 ] ; then
            stack_level=1
            mask_level=0
        fi

        if [ "$try_print" '=' 1 -a "$mask_level" '=' "$stack_level" ] ; then
            echo "$LINE"
        fi
    done
)

