#! /usr/bin/env bash
#
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

set -e

TMP_REPO_DIR='/tmp-repo'

shout() {
    echo -ne '\x1b[0m'
    echo -ne '\x1b[1;37m'
    echo "$@"
    echo -ne '\x1b[0m'
}

mkpkg() {
    if [ '!' -d "$TMP_REPO_DIR" ] ; then
        mkdir -p "$TMP_REPO_DIR/packages/spack-bootstrap"
        (
            echo '---'
            echo 'repo:'
            echo '  namespace: bootstrap'
        ) > "$TMP_REPO_DIR/repo.yaml"

        /spack/bin/spack repo add --scope user "$TMP_REPO_DIR"
    fi

    cp "$1" "$TMP_REPO_DIR/packages/spack-bootstrap/package.py"
}

cleanup() {
    if [ -d "$TMP_REPO_DIR" ] ; then
        /spack/bin/spack repo rm --scope user bootstrap
        rm -r "$TMP_REPO_DIR"
    fi
}

trap 'cleanup' EXIT INT TERM QUIT

mkdir -p /etc/spack \
         /spack-bootstrap/sw \
         /spack-bootstrap/modules \
         /spack-prebootstrap/sw \
         /spack-prebootstrap/modules \
         /root/.spack \
         /work

rm -rf /spack/.git

cd /work

eval "$( /spack/bin/spack --print-shell-vars sh )"
compatible_sys_type="$( echo $_sp_compatible_sys_types | sed 's/.*://g' )"

phase="$1" ; shift
counting=0
if [ -z "$phase" ] ; then
    phase=0
    counting=1
fi

cd /spack/share/spack/docker/conf

while ls -d "$phase"* &> /dev/null ; do
    for entry in $( ls -1d "$phase"* | sort ) ; do
        (
            . /spack/share/spack/setup-env.sh
            set -e

            if [ "$( basename "$entry" .yaml )" '!=' "$entry" ] ; then
                scope="$( echo "$entry" | cut -d - -f 2 )"

                case $scope in
                    system)
                        dir="/etc/spack"
                        ;;
                    user)
                        dir="$HOME/.spack"
                        ;;
                    *)
                        echo "Error: unrecognized config scope: ${scope}" >&2
                        exit 1
                        ;;
                esac

                shout "[[Updating '${scope}' scope (${entry/\/*})]]"
                (
                    config=''
                    IFS=$'\n'
                    grep -v '^\(#\|$\)' "$entry" | while read line ; do
                        if echo "$line" | grep -q '^\S\+:$' ; then
                            config="${line::-1}"
                            n="${#config}"
                            n="$(( n - 1 ))"
                            quotes="${config::1}${config:$n}"

                            if [ "$n" -gt 0 -a \
                                 '(' "$quotes" '=' '""' -o \
                                     "$quotes" '=' "''" ')' ] ; then
                                config="${config:1:-1}"
                            fi

                            shout "  $config"
                            echo '---' > "$dir/$config.yaml"
                        fi

                        echo "$line" >> "$dir/$config.yaml"
                    done
                )

            elif [ "$( basename "$entry" .py )" '!=' "$entry" ] ; then
                shout "[[Installing bundle: $( basename "$entry" .py )]]"
                mkpkg "$entry"
                false
                spack install --only dependencies \
                    "spack-bootstrap arch=$compatible_sys_type"
                spack module tcl refresh --yes-to-all

            elif [ "$( basename $entry .preload )" '!=' "$entry" ] ; then

                for pkg in $( grep -v '^\(#\|$\)' "$entry" ) ; do
                    shout "[[Preloading: $pkg]]"
                    spack load --dependencies "$pkg"
                done

            elif [ "$( basename $entry .symlink )" '!=' "$entry" ] ; then

                for pkg in $( grep -v '^\(#\|$\)' "$entry" ) ; do
                    shout "[[Symlinking: $pkg]]"
                    spack view --dependencies no symlink /usr/local "$pkg"
                    spack compiler find &> /dev/null
                done

            elif [ "$( basename $entry .bs )" '!=' "$entry" ] ; then
                shout "[[Running spack bootstrap]]"
                spack bootstrap
                spack module tcl refresh --yes-to-all

            else
                echo "Error: unrecognized config entry: $entry" >&2
                exit 1
            fi
        ) || exit 1
    done

    if [ "$counting" '=' '0' ] ; then
        break
    fi

    phase="$(( phase + 1 ))"
done
