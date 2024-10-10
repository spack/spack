# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# NOTE: spack-completion.fish is auto-generated by:
#
#   $ spack commands --aliases --format=fish
#       --header=fish/spack-completion.fish --update=spack-completion.fish
#
# Please do not manually modify this file.

# Check fish version before proceeding
set -l fish_version (string split '.' $FISH_VERSION)
if test $fish_version[1] -lt 3
    if test $fish_version[1] -eq 3
        and test $fish_version[2] -lt 2
        echo 'Fish version is older than 3.2.0. Some completion features may not work'
        set -g __fish_spack_force_files
    else
        echo 'This script requires fish version 3.0 or later'
        exit 1
    end
else
    set -g __fish_spack_force_files -F
end

# The following global variables are used as a cache of `__fish_spack_argparse`

# Cached command line
set -g __fish_spack_argparse_cache_line
# Parsed command
set -g __fish_spack_argparse_command
# Remaining arguments
set -g __fish_spack_argparse_argv
# Return value
set -g __fish_spack_argparse_return

# Spack command generates an optspec variable $__fish_spack_optspecs_<command>.
# We check if this command exists, and echo the optspec variable name.
function __fish_spack_get_optspecs -d 'Get optspecs of spack command'
    # Convert arguments to replace ' ' and '-' by '_'
    set -l cmd_var (string replace -ra -- '[ -]' '_' $argv | string join '_')
    # Set optspec variable name
    set -l optspecs_var __fish_spack_optspecs_$cmd_var
    # Query if variable $$optspecs_var exists
    set -q $optspecs_var; or return 1
    # If it exists, echo all optspecs line by line.
    # String join returns 1 if no join was performed, so we return 0 in such case.
    string join \n $$optspecs_var; or return 0
end

# Parse command-line arguments, save results to global variables,
# and add found flags to __fish_spack_flag_<flag>.
# Returns 1 if help flag is found.
function __fish_spack_argparse
    # Figure out if the current invocation already has a command.
    set -l args $argv
    set -l commands

    # Return cached result if arguments haven't changed
    if test "$__fish_spack_argparse_cache_line" = "$args"
        return $__fish_spack_argparse_return
    end

    # Clear all flags found in last run
    set -g | string replace -rf -- '^(__fish_spack_flag_\w+)(.*?)$' 'set -ge $1' | source

    # Set default return value to 0, indicating success
    set -g __fish_spack_argparse_return 0
    # Set command line to current arguments
    set -g __fish_spack_argparse_cache_line $argv

    # Recursively check arguments for commands
    while set -q args[1]
        # Get optspecs of current command
        set -l optspecs (__fish_spack_get_optspecs $commands $args[1])
        or break

        # If command exists, shift arguments
        set -a commands $args[1]
        set -e args[1]

        # If command has no arguments, continue
        set -q optspecs[1]; or continue

        # Parse arguments. Set variable _flag_<flag> if flag is found.
        # We find all these variables and set them to the global variable __fish_spack_flag_<flag>.
        argparse -i -s $optspecs -- $args 2>/dev/null; or break
        set -l | string replace -rf -- '^(_flag_.*)$' 'set -g __fish_spack$1' | source

        # Set args to not parsed arguments
        set args $argv

        # If command has help flag, we don't need to parse more so short circuit
        if set -q _flag_help
            set -g __fish_spack_argparse_return 1
            break
        end
    end

    # Set cached variables
    set -g __fish_spack_argparse_command $commands
    set -g __fish_spack_argparse_argv $args

    return $__fish_spack_argparse_return
end

# Check if current commandline's command is "spack $argv"
function __fish_spack_using_command
    set -l line (commandline -opc)
    __fish_spack_argparse $line; or return 1

    set -p argv spack
    test "$__fish_spack_argparse_command" = "$argv"
end

# Check if current commandline's command is "spack $argv[2..-1]",
# and cursor is at $argv[1]-th positional argument
function __fish_spack_using_command_pos
    __fish_spack_using_command $argv[2..-1]
    or return

    test (count $__fish_spack_argparse_argv) -eq $argv[1]
end

function __fish_spack_using_command_pos_remainder
    __fish_spack_using_command $argv[2..-1]
    or return

    test (count $__fish_spack_argparse_argv) -ge $argv[1]
end

# Helper functions for subcommands

function __fish_spack_bootstrap_names
    if set -q __fish_spack_flag_scope
        spack bootstrap list --scope $__fish_spack_flag_scope
    else
        spack bootstrap list
    end
end

# Reference: sudo's fish completion
function __fish_spack_build_env_spec
    set token (commandline -opt)

    set -l index (contains -- -- $__fish_spack_argparse_argv)
    if set -q index[1]
        __fish_complete_subcommand --commandline $__fish_spack_argparse_argv[(math $index + 1)..-1]
    else if set -q __fish_spack_argparse_argv[1]
        __fish_complete_subcommand --commandline "$__fish_spack_argparse_argv[2..-1] $token"
    else
        __fish_spack_specs
    end
end

function __fish_spack_commands
    spack commands
end

function __fish_spack_colon_path
    set token (string split -rm1 ':' (commandline -opt))

    if test (count $token) -lt 2
        __fish_complete_path $token[1]
    else
        __fish_complete_path $token[2] | string replace -r -- '^' "$token[1]:"
    end
end

function __fish_spack_config_sections
    if set -q __fish_spack_flag_scope
        spack config --scope $__fish_spack_flag_scope list | string split ' '
    else
        spack config list | string split ' '
    end
end

function __fish_spack_environments
    string trim (spack env list)
end

function __fish_spack_extensions
    # Skip optional flags, or it will be really slow
    string match -q -- '-*' (commandline -opt)
    and return

    comm -1 -2 (spack extensions | string trim | psub) (__fish_spack_installed_packages | sort | psub)
end

function __fish_spack_gpg_keys
    spack gpg list
end

function __fish_spack_installed_compilers
    spack compilers | grep -v '^[=-]\|^$'
end

function __fish_spack_installed_packages
    spack find --no-groups --format '{name}' | uniq
end

function __fish_spack_installed_specs
    # Try match local hash first
    __fish_spack_installed_specs_id
    and return

    spack find --no-groups --format '{name}@{version}'
end

function __fish_spack_installed_specs_id
    set -l token (commandline -opt)
    string match -q -- '/*' $token
    or return 1

    spack find --format '/{hash:7}'\t'{name}{@version}'
end

function __fish_spack_git_rev
    type -q __fish_git_ranges
    and __fish_git_ranges
end

function __fish_spack_mirrors
    spack mirror list | awk {'printf ("%s\t%s", $1, $2)'}
end

function __fish_spack_package_versions
    string trim (spack versions $argv)
end

function __fish_spack_packages
    spack list
end

function __fish_spack_pkg_packages
    spack pkg list
end

function __fish_spack_providers
    string trim (spack providers | grep -v '^$')
end

function __fish_spack_repos
    spack repo list | awk {'printf ("%s\t%s", $1, $2)'}
end

function __fish_spack_scopes
    # TODO: how to list all scopes?
    set -l scope system site user defaults
    set -l platform cray darwin linux test

    string join \n $scope
end

function __fish_spack_specs
    set -l token (commandline -opt)

    # Complete compilers
    if string match -rq -- '^(?<pre>.*%)[\w-]*(@[\w\.+~-]*)?$' $token
        __fish_spack_installed_compilers | string replace -r -- '^' "$pre"
        return
    end

    # Try to complete spec version
    # Currently we can only match '@' after a package name
    set -l package

    # Match ^ following package name
    if string match -rq -- '^(?<pre>.*?\^)[\w\.+~-]*$' $token
        # Package name is the nearest, assuming first character is always a letter or digit
        set packages (string match -ar -- '^[\w-]+' $__fish_spack_argparse_argv $token)
        set package $packages[-1]

        if test -n "$package"
            spack dependencies $package | string replace -r -- '^' "$pre"
            return
        end
    end

    # Match @ following package name
    if string match -rq -- '^(?<pre>.*?\^?(?<packages>[\w\.+~-]*)@)[\w\.]*$' $token
        set package $packages[-1]

        # Matched @ starting at next token
        if test -z "$package"
            string match -arq -- '(^|\^)(?<inners>[\w\.+~-]*)$' $__fish_spack_argparse_argv[-1]
            if test -n "$inners[1]"
                set package $inners[-1]
            end
        end
    end

    # Complete version if package found
    if test -n "$package"
        # Only list safe versions for speed
        string trim (spack versions --safe $package) | string replace -r -- '^' "$pre"
        return
    end

    # Else complete package name
    __fish_spack_installed_packages | string replace -r -- '$' \t"installed"
    spack list
end

function __fish_spack_specs_or_id
    # Try to match local hash first
    __fish_spack_installed_specs_id
    and return

    __fish_spack_specs
end

function __fish_spack_tags
    string trim (spack tags)
end

function __fish_spack_tests
    spack test list | grep -v '^[=-]'
end

function __fish_spack_unit_tests
    # Skip optional flags, or it will be really slow
    string match -q -- '-*' (commandline -opt)
    and return

    spack unit-test -l
end

function __fish_spack_yamls
    # Trim flag from current token
    string match -rq -- '(?<pre>-.)?(?<token>.*)' (commandline -opt)

    if test -n "$token"
        find $token* -type f '(' -iname '*.yaml' -or -iname '*.yml' ')'
    else
        find -maxdepth 2 -type f '(' -iname '*.yaml' -or -iname '*.yml' ')' | cut -c 3-
    end
end

# Reset existing completions
complete -c spack --erase

# Spack commands
#
# Everything below here is auto-generated.
