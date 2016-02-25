#!/usr/bin/env bash


function _bash_completion_spack {
    # Bash programmable completion for Spack
    #
    # The following variables are useful for Bash completion:
    #     COMP_CWORD: An index into ${COMP_WORDS} of the word containing the current cursor position
    #     COMP_KEY:   The key (or final key of a key sequence) used to invoke the current completion function
    #     COMP_LINE:  The current command line
    #     COMP_POINT: The index of the current cursor position relative to the beginning of the current command
    #     COMP_TYPE:  Set to an integer value corresponding to the type of completion attempted
    #     COMP_WORDS: an array containing individual command arguments typed so far
    #     COMPREPLY:  an array containing possible completions as a result of your function

    # In all following examples, let the cursor be denoted by brackets, i.e. []

    # For our purposes, flags should not affect tab completion. For instance,
    # `spack install []` and `spack -d install []` should both give the same
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
    subfunction=$(IFS=_; echo "_${COMP_WORDS_NO_FLAGS[@]}")

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



    # TODO:
    # In general, when envoking tab completion, the user is not expecting to
    # see optional flags mixed in with subcommands or package names. Tab
    # completion is used by the lazy and by those who are bad at spelling.
    # If someone doesn't remember what flag to use, seeing single letter flags
    # in their results won't help them, and they should consult the
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

    COMPREPLY=($($subcommand))
}

function _spack {
    if $list_options
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
        compgen -W "$(_available_packages)" -- "$cur"
    fi
}

function _spack_checksum {
    if $list_options
    then
        compgen -W "-h --help --keep-stage" -- "$cur"
    else
        compgen -W "$(_available_packages)" -- "$cur"
    fi
}

function _spack_clean {
    if $list_options
    then
        compgen -W "-h --help"
    else
        compgen -W "$(_available_packages)" -- "$cur"
    fi
}

function _spack_compiler {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add remove list info"
    fi
}

function _spack_compiler_add {
    compgen -o dirnames -- "$cur"
}

function _spack_compiler_remove {
    compgen -W "$(_installed_compilers)" -- "$cur"
}

function _spack_compiler_list {
    # `spack compiler list` has no valid options
}

function _spack_compiler_info {
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
        compgen -W "edit get"
    fi
}

function _spack_config_edit {
    compgen -W "compilers mirrors" # TODO: more?
}

function _spack_config_get {
    compgen -W "compilers mirrors" # TODO: more?
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
        compgen -W "-h --help"
    else
        compgen -W "$(_available_packages)" -- "$cur"
    fi
}

function _spack_diy {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies --keep-prefix
                    --skip-patch" -- "$cur"
    else
        compgen -W "$(_available_packages)" -- "$cur"
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
        compgen -W "$(_available_packages)" -- "$cur"
    fi
}

function _spack_env {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_available_packages)" -- "$cur"
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
        compgen -W "$(_available_packages)" -- "$cur"
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
        compgen -W "$(_available_packages)" -- "$cur"
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
        compgen -W "$(_available_packages)" -- "$cur"
    fi
}

function _spack_install {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies -j --jobs --keep-prefix
                    --keep-stage -n --no-checksum -v --verbose --fake" -- "$cur"
    else
        compgen -W "$(_spack_available_packages)" -- "$cur"
    fi
}

function _spack_list {
function _spack_load {
function _spack_location {
function _spack_md5 {
function _spack_mirror {
function _spack_module {
function _spack_package-list {
function _spack_patch {
function _spack_pkg {
function _spack_providers {
function _spack_purge {
function _spack_python {
function _spack_reindex {
function _spack_repo {
function _spack_restage {
function _spack_spec {
function _spack_stage {
function _spack_test {
function _spack_test-install {
function _spack_uninstall {
function _spack_unload {
function _spack_unuse {
function _spack_url-parse {
function _spack_urls {
function _spack_use {
function _spack_versions {



function _subcommands {
    spack help | grep "^    [a-z]" | awk '{print $1}'
}

function _available_packages {
    spack list
}

function _installed_packages {
    spack find | grep -v "^--"
}

function _installed_compilers {
    spack compilers | grep -v "^--"
}

function test_vars {
    echo "-----------------------------------------------------"            >> ~/temp
    echo "Full line:                '$COMP_LINE'"                           >> ~/temp
    echo                                                                    >> ~/temp
    echo "Word list w/ flags:       $(pretty_print COMP_WORDS[@])"          >> ~/temp
    echo "# words w/ flags:         '${#COMP_WORDS[@]}'"                    >> ~/temp
    echo "Cursor index w/ flags:    '$COMP_CWORD'"                          >> ~/temp
    echo                                                                    >> ~/temp
    echo "Word list w/out flags:    $(pretty_print COMP_WORDS_NO_FLAGS[@])" >> ~/temp
    echo "# words w/out flags:      '${#COMP_WORDS_NO_FLAGS[@]}'"           >> ~/temp
    echo "Cursor index w/out flags: '$COMP_CWORD_NO_FLAGS'"                 >> ~/temp
    echo                                                                    >> ~/temp
    if $list_options
    then
        echo "List options:             'True'"  >> ~/temp
    else
        echo "List options:             'False'" >> ~/temp
    fi
    echo "Current word:             '$cur'"  >> ~/temp
    echo "Previous word:            '$prev'" >> ~/temp
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


