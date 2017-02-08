##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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

    #_test_vars

    # Make sure function exists before calling it
    if [[ "$(type -t $subfunction)" == "function" ]]
    then
        COMPREPLY=($($subfunction))
    fi
}

# Spack commands

function _spack {
    if $list_options
    then
        compgen -W "-h --help -d --debug -D --pdb -k --insecure -m --mock -p
                    --profile -v --verbose -s --stacktrace -V --version" -- "$cur"
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
    compgen -W "-h --help -p --platform" -- "$cur"
}

function _spack_bootstrap {
    # FIXME: What does this command even do?
    if $list_options
    then
        compgen -W "-h --help -r --remote" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_build {
    if $list_options
    then
        compgen -W "-h --help -v --verbose" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
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
        compgen -W "find add remove rm list info" -- "$cur"
    fi
}

function _spack_compiler_add {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_compiler_find {
    # Alias to `spack compiler add`
    _spack_compiler_add
}

function _spack_compiler_info {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_installed_compilers)" -- "$cur"
    fi
}

function _spack_compiler_list {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_compiler_remove {
    if $list_options
    then
        compgen -W "-h --help -a --all --scope" -- "$cur"
    else
        compgen -W "$(_installed_compilers)" -- "$cur"
    fi
}

function _spack_compiler_rm {
    # Alias to `spack compiler remove`
    _spack_compiler_remove
}

function _spack_compilers {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_config {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "edit get" -- "$cur"
    fi
}

function _spack_config_edit {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "mirrors repos modules packages config compilers" -- "$cur"
    fi
}

function _spack_config_get {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "mirrors repos modules packages config compilers" -- "$cur"
    fi
}

function _spack_configure {
    if $list_options
    then
        compgen -W "-h --help -v --verbose" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_create {
    compgen -W "-h --help --keep-stage -n --name -t --template -r --repo
                -N --namespace -f --force" -- "$cur"
}

function _spack_deactivate {
    if $list_options
    then
        compgen -W "-h --help -f --force -a --all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_debug {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "create-db-tarball" -- "$cur"
    fi
}

function _spack_create-db-tarball {
    compgen -W "-h --help" -- "$cur"
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
                    --skip-patch -q --quiet --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_doc {
    # FIXME: What does this command even do?
    compgen -W "-h --help" -- "$cur"
}

function _spack_edit {
    if $list_options
    then
        compgen -W "-h --help -b --build-system -c --command -t --test -m --module
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
        compgen -W "go-bootstrap go lua octave python r ruby rust" -- "$cur"
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
                    -L --very-long -f --show-flags -e --explicit
                    -E --implicit -u --unknown -m --missing -v --variants
                    -M --only-missing -N --namespace" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_flake8 {
    if $list_options
    then
        compgen -W "-h --help -k --keep-temp -o --output
                    -r --root-relative -U --no-untracked" -- "$cur"
    else
        compgen -o filenames -- "$cur"
    fi
}

function _spack_graph {
    if $list_options
    then
        compgen -W "-h --help -a --ascii -d --dot -n --normalize -s --static
                    -i --installed -t --deptype" -- "$cur"
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
        compgen -W "-h --help --only -j --jobs --keep-prefix --keep-stage
                    -n --no-checksum -v --verbose --fake --clean --dirty
                    --run-tests --log-format --log-file" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_list {
    if $list_options
    then
        compgen -W "-h --help -d --search-description --format" -- "$cur"
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
        compgen -W "add create list remove rm" -- "$cur"
    fi
}

function _spack_mirror_add {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_mirror_create {
    if $list_options
    then
        compgen -W "-h --help -d --directory -f --file
                    -D --dependencies -o --one-version-per-spec" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_mirror_list {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_mirror_remove {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_mirrors)" -- "$cur"
    fi
}

function _spack_module {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "find loads refresh rm" -- "$cur"
    fi
}

function _spack_module_find {
    if $list_options
    then
        compgen -W "-h --help -m --module-type" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_loads {
    if $list_options
    then
        compgen -W "-h --help --input-only -p --prefix -x --exclude
                    -m --module-type -r --dependencies" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi

}

function _spack_module_refresh {
    if $list_options
    then
        compgen -W "-h --help --delete-tree -m --module-type
                    -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
}

function _spack_module_rm {
    if $list_options
    then
        compgen -W "-h --help -m --module-type -y --yes-to-all" -- "$cur"
    else
        compgen -W "$(_installed_packages)" -- "$cur"
    fi
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
    # FIXME: What does this subcommand even do?
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "add added diff list removed" -- "$cur"
    fi
}

function _spack_pkg_add {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_pkg_added {
    # FIXME: How to list git revisions?
    compgen -W "-h --help" -- "$cur"
}

function _spack_pkg_diff {
    # FIXME: How to list git revisions?
    compgen -W "-h --help" -- "$cur"
}

function _spack_pkg_list {
    # FIXME: How to list git revisions?
    compgen -W "-h --help" -- "$cur"
}

function _spack_pkg_removed {
    # FIXME: How to list git revisions?
    compgen -W "-h --help" -- "$cur"
}

function _spack_providers {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "blas daal elf golang ipp lapack mkl
                    mpe mpi pil scalapack" -- "$cur"
    fi
}

function _spack_purge {
    compgen -W "-h --help -s --stage -d --downloads
                -m --misc-cache -a --all" -- "$cur"
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
        compgen -W "add create list remove rm" -- "$cur"
    fi
}

function _spack_repo_add {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_repo_create {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_repo_list {
    compgen -W "-h --help --scope" -- "$cur"
}

function _spack_repo_remove {
    if $list_options
    then
        compgen -W "-h --help --scope" -- "$cur"
    else
        compgen -W "$(_repos)" -- "$cur"
    fi
}

function _spack_repo_rm {
    # Alias to `spack repo remove`
    _spack_repo_remove
}

function _spack_restage {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_setup {
    if $list_options
    then
        compgen -W "-h --help -i --ignore-dependencies -v --verbose
                    --clean --dirty" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_spec {
    if $list_options
    then
        compgen -W "-h --help -l --long -L --very-long -y --yaml -c --cover
                    -N --namespaces -I --install-status -t --types" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_stage {
    if $list_options
    then
        compgen -W "-h --help -n --no-checksum -p --path" -- "$cur"
    else
        compgen -W "$(_all_packages)" -- "$cur"
    fi
}

function _spack_test {
    if $list_options
    then
        compgen -W "-h --help -H --pytest-help -l --list
                    -L --long-list" -- "$cur"
    else
        compgen -W "$(_tests)" -- "$cur"
    fi
}

function _spack_uninstall {
    if $list_options
    then
        compgen -W "-h --help -f --force -a --all -d --dependents
                    -y --yes-to-all" -- "$cur"
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

function _spack_url {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -W "list parse test" -- "$cur"
    fi
}

function _spack_url_list {
    compgen -W "-h --help -c --color -e --extrapolation -n --incorrect-name
                -v --incorrect-version" -- "$cur"
}

function _spack_url_parse {
    compgen -W "-h --help -s --spider" -- "$cur"
}

function _spack_url_test {
    compgen -W "-h --help" -- "$cur"
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

function _spack_view {
    if $list_options
    then
        compgen -W "-h --help -v --verbose -e --exclude
                    -d --dependencies" -- "$cur"
    else
        compgen -W "add check hard hardlink remove rm soft
                    statlink status symlink" -- "$cur"
    fi
}

function _spack_view_add {
    # Alias for `spack view symlink`
    _spack_view_symlink
}

function _spack_view_check {
    # Alias for `spack view statlink`
    _spack_view_statlink
}

function _spack_view_hard {
    # Alias for `spack view hardlink`
    _spack_view_hardlink
}

function _spack_view_hardlink {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_view_remove {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_view_rm {
    # Alias for `spack view remove`
    _spack_view_remove
}

function _spack_view_soft {
    # Alias for `spack view symlink`
    _spack_view_symlink
}

function _spack_view_statlink {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

function _spack_view_status {
    # Alias for `spack view statlink`
    _spack_view_statlink
}

function _spack_view_symlink {
    if $list_options
    then
        compgen -W "-h --help" -- "$cur"
    else
        compgen -o dirnames -- "$cur"
    fi
}

# Helper functions for subcommands

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

function _tests {
    spack test -l
}

# Testing functions

function _test_vars {
    echo "-----------------------------------------------------"            >> temp
    echo "Full line:                '$COMP_LINE'"                           >> temp
    echo                                                                    >> temp
    echo "Word list w/ flags:       $(_pretty_print COMP_WORDS[@])"          >> temp
    echo "# words w/ flags:         '${#COMP_WORDS[@]}'"                    >> temp
    echo "Cursor index w/ flags:    '$COMP_CWORD'"                          >> temp
    echo                                                                    >> temp
    echo "Word list w/out flags:    $(_pretty_print COMP_WORDS_NO_FLAGS[@])" >> temp
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
# Syntax: _pretty_print array1[@] ...
function _pretty_print {
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
