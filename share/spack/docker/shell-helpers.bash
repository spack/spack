# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

if [ -z "$__spack_shell_helpers_guard" ] ; then __spack_shell_helpers_guard=1

setup_ssh_server() {
    if ssh_server_is_setup ; then
        return 0
    fi

    uid="`id -u`"
    if [ "$uid" '=' '0' ] ; then
        key_types="dsa ecdsa rsa"
        if [ "$DOCKERFILE_DISTRO" '!=' 'centos' -o \
             "$DOCKERFILE_DISTRO_VERSION" '!=' '6' ] ; then
            key_types="${key_types} ed25519"
        fi

        for key_type in $key_types ; do
            private_key_file="/etc/ssh/ssh_host_${key_type}_key"
            public_key_file="$private_key_file.pub"

            if [ '!' -f "$private_key_file" ] ; then
                ssh-keygen \
                    -q -t "$key_type" -N "" -f "$private_key_file"
                chmod 600 "$private_key_file"
                chmod 644 "$public_key_file"
            fi
        done

        touch /etc/ssh/initialized
        return 0
    fi
    return 1
}

ssh_server_is_setup() {
    if [ -f "/etc/ssh/initialized" ] ; then
        return 0
    fi
    return 1
}

clear_ssh_server() {
    if ssh_server_is_setup ; then
        uid="`id -u`"
        if [ "$uid" '=' '0' ] ; then
            rm -f /etc/ssh/ssh_host_*_key* /etc/ssh/initialized
            return 0
        fi
        return 1
    fi
    return 0
}

start_ssh_server() {
    if ssh_server_is_started ; then
        return 0
    fi

    uid="`id -u`"
    if [ "$uid" '=' '0' ] ; then
        setup_ssh_server
        mkdir -p /var/run/sshd
        nohup /usr/sbin/sshd -f /etc/ssh/sshd_config < /dev/null &> /dev/null
        return 0
    fi
    return 1
}

ssh_server_is_started() {
    if pgrep -u 0 -U 0 sshd &> /dev/null ; then
        return 0
    fi
    return 1
}

stop_ssh_server() {
    if ssh_server_is_started ; then
        uid="`id -u`"
        if [ "$uid" '=' '0' ] ; then
            pkill sshd
            return 0
        fi
        return 1
    fi
    return 0
}

setup_ssh_user() {
    if ssh_user_is_setup ; then
        return 0
    fi

    if [ '!' -f "$HOME/.ssh/id_rsa" ] ; then
        ssh-keygen \
            -t rsa -C "spack.user@docker.host" -N "" -f "$HOME/.ssh/id_rsa"
        cat "$HOME/.ssh/id_rsa.pub" >> "$HOME/.ssh/authorized_keys"
        chmod 600 "$HOME/.ssh/authorized_keys"

        start_ssh=1
        if ssh_server_is_started ; then
            start_ssh=0
        fi

        if [ "$start_ssh" '=' '0' ] || start_ssh_server ; then
            docker_ip="`ip address show dev eth0 |
                        grep inet |
                        cut -d' ' -f 6 |
                        cut -d/ -f 1`"

            ssh-keyscan -t rsa 127.0.0.1 localhost "$docker_ip" "`hostname`" \
                > "$HOME/.ssh/known_hosts" 2> /dev/null
        fi

        if [ "$start_ssh" '=' '1' ] ; then
            stop_ssh_server
        fi

        touch "$HOME/.ssh/initialized"
    fi
}

ssh_user_is_setup() {
    if [ -f "$HOME/.ssh/initialized" ] ; then
        return 0
    fi
    return 1
}

clear_ssh_user() {
    if ssh_user_is_setup ; then
        rm -f "$HOME/.ssh/*"
    fi
    return 0
}

ssh_init() {
    start_ssh_server
    setup_ssh_server
    setup_ssh_user
}

ssh_clear() {
    clear_ssh_user
    clear_ssh_server
    stop_ssh_server
}

setup_spack() {
    source /usr/share/lmod/lmod/init/bash
    source "$SPACK_ROOT/share/spack/setup-env.sh"

    if [ "$1" '=' '--with-completion' ] ; then
        source "$SPACK_ROOT/share/spack/spack-completion.bash"
    fi
}

fi # !__spack_shell_helpers_guard
