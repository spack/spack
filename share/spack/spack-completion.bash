#!/usr/bin/env bash

# The following global variables are used/set by Bash programmable completion
#     COMP_CWORD: An index into ${COMP_WORDS} of the word containing the
#                 current cursor position
#     COMP_LINE:  The current command line
#     COMP_WORDS: an array containing individual command arguments typed so far
#     COMPREPLY:  an array containing possible completions as a result of your
#                 function

# Bash programmable completion for Spack
function _bash_completion_spack {
    # In all following examples, let the cursor be denoted by brackets, i.e. []

    # For our purposes, flags should not affect tab completion. For instance,
    # `spack install []` and `spack -d install --jobs 8 []` should both give the same
    # possible completions. Therefore, we need to ignore any flags in COMP_WORDS.
    local COMP_WORDS_NO_FLAGS=()
    local index=0
    while [[ "$index" -lt "$COMP_CWORD" ]]
    do
        if [[ "${COMP_WORDS[$index]}" == [a-z]* ]]
        then
            COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$index]}")
        fi
        let index++
    done

    # Options will be listed by a subfunction named after non-flag arguments.
    # For example, `spack -d install []` will call _spack_install
    # and `spack compiler add []` will call _spack_compiler_add
    local subfunction=$(IFS='_'; echo "_${COMP_WORDS_NO_FLAGS[*]}")

    # However, the word containing the current cursor position needs to be
    # added regardless of whether or not it is a flag. This allows us to
    # complete something like `spack install --keep-st[]`
    COMP_WORDS_NO_FLAGS+=("${COMP_WORDS[$COMP_CWORD]}")

    # Since we have removed all words after COMP_CWORD, we can safely assume
    # that COMP_CWORD_NO_FLAGS is simply the index of the last element
    local COMP_CWORD_NO_FLAGS=$(( ${#COMP_WORDS_NO_FLAGS[@]} - 1 ))

    # There is no guarantee that the cursor is at the end of the command line
    # when tab completion is envoked. For example, in the following situation:
    #     `spack -d [] install`
    # if the user presses the TAB key, a list of valid flags should be listed.
    # Note that we cannot simply ignore everything after the cursor. In the
    # previous scenario, the user should expect to see a list of flags, but
    # not of other subcommands. Obviously, `spack -d list install` would be
    # invalid syntax. To accomplish this, we use the variable list_options
    # which is true if the current word starts with '-' or if the cursor is
    # not at the end of the line.
    local list_options=false
    if [[ "${COMP_WORDS[$COMP_CWORD]}" == -* || \
          "$COMP_CWORD" -ne "${#COMP_WORDS[@]}-1" ]]
    then
        list_options=true
    fi

    # In general, when envoking tab completion, the user is not expecting to
    # see optional flags mixed in with subcommands or package names. Tab
    # completion is used by those who are either lazy or just bad at spelling.
    # If someone doesn't remember what flag to use, seeing single letter flags
    # in their results won't help them, and they should instead consult the
    # documentation. However, if the user explicitly declares that they are
    # looking for a flag, we can certainly help them out.
    #     `spack install -[]`
    # and
    #     `spack install --[]`
    # should list all flags and long flags, respectively. Furthermore, if a
    # subcommand has no non-flag completions, such as `spack arch []`, it
    # should list flag completions.

    local cur=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS]}
    local prev=${COMP_WORDS_NO_FLAGS[$COMP_CWORD_NO_FLAGS-1]}

    #test_vars

    # Make sure function exists before calling it
    if [[ "$(type -t $subfunction)" == "function" ]]
    then
        COMPREPLY=($($subfunction))
    fi
}

function _spack {
    if $list_options
    then
        compgen -W "-h --help -d --debug -D --pdb -k --insecure -m --mock -p
                    --profile -v --verbose -V --version" -- "$cur"
    else
        compgen -W "$(_subcommands)" -- "$cur"
    fi
}

function _spack_activate {
    if $list_options
    then
        compgen -W "-h --help -f --force" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_arch {
    # `spack arch` has no non-flag options
    # Always list options
    compgen -W "-h --help" -- "$cur"
}

function _spack_bootstrap {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_cd {
    if $list_options
    then
        compgen -W "-h --help -m --module-dir -r --spack-root -i --install-dir
                    -p --package-dir -P --packages -s --stage-dir -S --stages
                    -b --build-dir" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_checksum {
    if $list_options
    then
        compgen -W "-h --help --keep-stage" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_clean {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_compiler {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add info list remove" -- "$cur"
    fi
}

function _spack_compiler_add {
    compgen -o dirnames -- "$cur"
}

function _spack_compiler_info {
    compgen -W "$(_installed_compilers)" -- "$cur"
}

function _spack_compiler_list {
    # `spack compiler list` has no valid options
    :
}

function _spack_compiler_remove {
    compgen -W "$(_installed_compilers)" -- "$cur"
}

function _spack_compilers {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_config {
    if $list_options
    then
        compgen -W "-h --help --user --site" -- "$cur"
    else
        compgen -W "edit get" -- "$cur"
    fi
}

function _spack_config_edit {
    compgen -W "compilers mirrors" -- "$cur" # TODO: more?
}

function _spack_config_get {
    compgen -W "compilers mirrors" -- "$cur" # TODO: more?
}

function _spack_create {
    # You can't complet a URL. Just list options
    compgen -W "-h --help --keep-stage -n --name -r --repo -N --namespace
                -f --force" -- "$cur"
}

function _spack_deactivate {
    if $list_options
    then
        compgen -W "-h --help -f --force -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_dependents {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_diy {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies --keep-prefix
                    --skip-patch" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_doc {
    # TODO: What does this function even do?
    compgen -W "-h --help" -- "$cur"
}

function _spack_edit {
    if $list_options
    then
        compgen -W "-h --help -f --force -c --command -t --test -m --module
                    -r --repo -N --namespace" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_env {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_extensions {
    if $list_options
    then
        compgen -W "-h --help -l --long -p --paths -d --deps" -- "$cur"
    else
        # TODO: Is Python currently the only package that can be extended?
        compgen -W "python" -- "$cur"
    fi
}

function _spack_fetch {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum -m --missing
                    -D --dependencies" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_find {
    if $list_options
    then
        compgen -W "-h --help -s --short -p --paths -d --deps -l --long
                    -L --very-long -u --unknown -m --missing -M --only-missing
                    -N --namespace" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_graph {
    if $list_options
    then
        compgen -W "-h --help --ascii --dot --concretize" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_help {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_subcommands)" -- "$cur"
    fi
}

function _spack_info {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_install {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies -j --jobs --keep-prefix
                    --keep-stage -n --no-checksum -v --verbose --fake" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_list {
    if $list_options
    then
        compgen -W "-h --help -i --insensitive" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_load {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_location {
    if $list_options
    then
        compgen -W "-h --help -m --module-dir -r --spack-root -i --install-dir
                    -p --package-dir -P --packages -s --stage-dir -S --stages
                    -b --build-dir" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_md5 {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o filenames -- "$cur"
    fi
}

function _spack_mirror {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "add create list remove" -- "$cur"
    fi
}

function _spack_mirror_add {
    compgen -o dirnames -- "$cur"
}

function _spack_mirror_create {
    compgen -W "$(_all_packages)" -- "$cur"
}

function _spack_mirror_list {
    # `spack mirror list` has no valid options
    :
}

function _spack_mirror_remove {
    compgen -W "$(_mirrors)" -- "$cur"
}

function _spack_module {
    if $list_compilers
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "find refresh" -- "$cur"
    fi
}

function _spack_module_find {
    # `spack module find` has no valid options
    :
}

function _spack_module_refresh {
    # `spack module refresh` has no valid arguments
    :
}

function _spack_package-list {
    compgen -W "-h --help" -- "$cur"
}

function _spack_patch {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_pkg {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add added diff list removed" -- "$cur"
    fi
}

function _spack_pkg_add {
    # `spack pkg add` has no valid options
    :
}

function _spack_pkg_added {
    # `spack pkg added` has no valid options
    :
}

function _spack_pkg_diff {
    # `spack pkg diff` has no valid options
    :
}

function _spack_pkg_list {
    # `spack pkg list` has no valid options
    :
}

function _spack_pkg_removed {
    # `spack pkg removed` has no valid options
    :
}

function _spack_providers {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "blas elf lapack mpe mpi scalapack" -- "$cur"
    fi
}

function _spack_purge {
    compgen -W "-h --help" -- "$cur"
}

function _spack_python {
    if $list_options
    then
        compgen -W "-h --help -c" -- "$cur"
    else
        compgen -o filenames -- "$cur"
    fi
}

function _spack_reindex {
    compgen -W "-h --help" -- "$cur"
}

function _spack_repo {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add create list remove" -- "$cur"
    fi
}

function _spack_repo_add {
    # `spack repo add` has no valid options
    :
}

function _spack_repo_create {
    # `spack repo create` has no valid options
    :
}

function _spack_repo_list {
    # `spack repo list` has no valid options
    :
}

function _spack_repo_remove {
    compgen -W "$(_repos)" -- "$cur"
}

function _spack_restage {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_spec {
    if $list_options
    then
        compgen -W "-h --help -i --ids" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_stage {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_test {
    # TODO: What does this subcommand even do?
    compgen -W "-h --help -l --list --createXmlOutput --xmlOutputDir
                -v --verbose" -- "$cur"
}

function _spack_test-install {
    if $list_options
    then
        compgen -W "-h --help -j --jobs -n --no-checksum -o --output" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_uninstall {
    if $list_options
    then
        compgen -W "-h --help -f --force -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_unload {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)"
    fi
}

function _spack_unuse {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)"
    fi
}

function _spack_url-parse {
    compgen -W "-h --help -s --spider" -- "$cur"
}

function _spack_urls {
    compgen -W "-h --help -c --color -e --extrapolation" -- "$cur"
}

function _spack_use {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_versions {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _subcommands {
    spack help | grep "^    [a-z]" | awk '{print $1}'
}

function _all_packages {
    spack list
}

function _installed_packages {
    # Perl one-liner used to strip out color codes
    spack find | grep -v "^--" | perl -pe 's/\e\[?.*?[\@-~]//g'
}

function _installed_compilers {
    spack compilers | egrep -v "^(-|=)"
}

function _mirrors {
    spack mirror list | awk '{print $1}'
}

function _repos {
    spack repo list | awk '{print $1}'
}

function test_vars {
    echo "-----------------------------------------------------"            >> temp
    echo "Full line:                '$COMP_LINE'"                           >> temp
    echo                                                                    >> temp
    echo "Word list w/ flags:       $(pretty_print COMP_WORDS[@])"          >> temp
    echo "# words w/ flags:         '${#COMP_WORDS[@]}'"                    >> temp
    echo "Cursor index w/ flags:    '$COMP_CWORD'"                          >> temp
    echo                                                                    >> temp
    echo "Word list w/out flags:    $(pretty_print COMP_WORDS_NO_FLAGS[@])" >> temp
    echo "# words w/out flags:      '${#COMP_WORDS_NO_FLAGS[@]}'"           >> temp
    echo "Cursor index w/out flags: '$COMP_CWORD_NO_FLAGS'"                 >> temp
    echo                                                                    >> temp
    echo "Subfunction:              '$subfunction'"                         >> temp
    if $list_options
    then
        echo "List options:             'True'"  >> temp
    else
        echo "List options:             'False'" >> temp
    fi
    echo "Current word:             '$cur'"  >> temp
    echo "Previous word:            '$prev'" >> temp
}

# Pretty-prints one or more arrays
# Syntax: pretty_print array1[@] ...
function pretty_print {
    for arg in $@
    do
        local array=("${!arg}")
        echo -n "$arg: ["
        printf   "'%s'" "${array[0]}"
        printf ", '%s'" "${array[@]:1}"
        echo "]"
    done
}

complete -F _bash_completion_spack spack

