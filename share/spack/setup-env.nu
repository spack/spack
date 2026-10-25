use std/util "path add"

const SPACK_ROOT = path self ../..

def split-to-next-subcommand [args] {
  {
    flags: ($args | take while { |flag| str starts-with "-" }),
     rest: ($args | skip while { |flag| str starts-with "-" })
  }
}

# Taken from: https://www.nushell.sh/cookbook/foreign_shell_scripts.html
def capture-foreign-env [
    --shell (-s): string = /bin/sh
    --arguments (-a): list<string> = []
] {
    let script_contents = $in;
    let env_out = with-env { SCRIPT_TO_SOURCE: $script_contents } {
        ^$shell ...$arguments -c `
        env
        echo '<ENV_CAPTURE_EVAL_FENCE>'
        eval "$SCRIPT_TO_SOURCE"
        echo '<ENV_CAPTURE_EVAL_FENCE>'
        env -0 -u _ -u _AST_FEATURES -u SHLVL`
    }
    | split row '<ENV_CAPTURE_EVAL_FENCE>'
    | {
        before: ($in | first | str trim | lines)
        after: ($in | last | str trim | split row (char --integer 0))
    }

    # Unfortunate Assumption:
    # No changed env var contains newlines (not cleanly parseable)
    $env_out.after
    | where { |line| $line not-in $env_out.before }
    | parse "{key}={value}"
    | transpose --header-row --as-record
    | if $in == [] { {} } else { $in }
}

def contains-any-of [candidates] {
  any { |it| $it in $candidates }
}

export def --env --wrapped spack [...args] {
  load-env (["DYLD_LIBRARY_PATH" "DYLD_FALLBACK_LIBRARY_PATH"] | each {|var|
    if $env has $var {
      { $"SPACK_($var)": ($env | get $var) }
    }
  } | into record)

  let base_split = split-to-next-subcommand $args

  # If no arguments were passed or the base arguments to spack contain `-h` or
  # `-V`, run the commandas-is.
  if ($args | is-empty) or (
       $base_split.flags | contains-any-of ["-h", "--help", "-V", "--version"]
     ) {
    ^spack ...$args
    return
  }

  let subcommand = $base_split.rest | first
  let subcommand_args = $base_split.rest | skip 1
  let subcommand_split = split-to-next-subcommand $subcommand_args

  # Each of these subcommands makes changes to the environment of the
  # current shell, so they need special treatment.
  match $subcommand {
    "cd" => {
      if ($subcommand_split.flags | contains-any-of ["-h", "--help"]) {
        ^spack cd -h
        return
      }

      let location = (spack location ...$subcommand_args)
      if ($location | path type) == "dir" {
        cd $location
      } else {
        return
      }
    }
    "env" => {
      # The user invoked `spack env` with no subcommand or flags.
      if ($subcommand_split.rest | is-empty) {
        ^spack ...$base_split.flags env ...$subcommand_split.rest
      }

      # Assumes there are no direct flags to `spack env`.
      let env_subcommand = $subcommand_split.rest | first

      match $env_subcommand {
        "activate" => {
          if ($base_split.flags | contains-any-of ["-h", "--help", "--sh", "--csh"]) {
            ^spack ...$base_split.flags
                   env
                   ...$subcommand_split.flags
                   activate
                   ...$subcommand_split.rest
            return
          }
          load-env (
            ^spack ...$base_split.flags
                   env
                   ...$subcommand_split.flags
                   activate --sh
                   ...($subcommand_split.rest | skip 1) | capture-foreign-env
          )
          return
        }
        "deactivate" => {
          if ($base_split.flags | contains-any-of ["-h", "--help", "--sh", "--csh"]) {
            ^spack ...$base_split.flags
                   env
                   ...$subcommand_split.flags
                   activate
                   ...$subcommand_split.rest
            return
          }
          load-env (
            ^spack ...$base_split.flags
                   env
                   ...$subcommand_split.flags
                   deactivate --sh
                   ...($subcommand_split.rest | skip 1) | capture-foreign-env
          )

          # capture-foreign-env doesn't cover unset.
          hide-env SPACK_ENV SPACK_ENV_VIEW
          return
        }
        _ => {}
      }
    }

    # Other sub-commands are run as-is.
    _ => {
      ^spack ...$args
    }
  }
}

export-env {
  $env.SPACK_ROOT = $SPACK_ROOT
  $env.SPACK_PYTHON = (which python3 python python2 | first | get path)
  path add ($env.SPACK_ROOT | path join "bin")
}
