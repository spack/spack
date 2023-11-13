import json
import os.path
import sys
from typing import Any, Dict, Tuple, Union

from .environment import EnvironmentModifications, sanitize
from .executable import Executable, which

Path = str


def from_sourcing_file(filename: Path, *arguments: str, **kwargs: Any) -> EnvironmentModifications:
    """Returns the environment modifications that have the same effect as
    sourcing the input file.

    Args:
        filename: the file to be sourced
        *arguments: arguments to pass on the command line

    Keyword Args:
        shell (str): the shell to use (default: ``bash``)
        shell_options (str): options passed to the shell (default: ``-c``)
        source_command (str): the command to run (default: ``source``)
        suppress_output (str): redirect used to suppress output of command
            (default: ``&> /dev/null``)
        concatenate_on_success (str): operator used to execute a command
            only when the previous command succeeds (default: ``&&``)
        exclude ([str or re]): ignore any modifications of these
            variables (default: [])
        include ([str or re]): always respect modifications of these
            variables (default: []). Supersedes any excluded variables.
        clean (bool): in addition to removing empty entries,
            also remove duplicate entries (default: False).
    """
    # Check if the file actually exists
    if not os.path.isfile(filename):
        msg = f"Trying to source non-existing file: {filename}"
        raise RuntimeError(msg)

    # Prepare include and exclude lists of environment variable names
    exclude = kwargs.get("exclude", [])
    include = kwargs.get("include", [])
    clean = kwargs.get("clean", False)

    # Other variables unrelated to sourcing a file
    exclude.extend(
        [
            # Bash internals
            "SHLVL",
            "_",
            "PWD",
            "OLDPWD",
            "PS1",
            "PS2",
            "ENV",
            # Environment Modules or Lmod
            "LOADEDMODULES",
            "_LMFILES_",
            "MODULEPATH",
            "MODULERCFILE",
            "BASH_FUNC_ml()",
            "BASH_FUNC_module()",
            # Environment Modules-specific configuration
            "MODULESHOME",
            "BASH_FUNC__module_raw()",
            r"MODULES_(.*)",
            r"__MODULES_(.*)",
            r"(\w*)_mod(quar|share)",
            # Lmod-specific configuration
            r"LMOD_(.*)",
        ]
    )

    # Compute the environments before and after sourcing
    before = sanitize(
        environment_after_sourcing_files(os.devnull, **kwargs), exclude=exclude, include=include
    )
    file_and_args = (filename,) + arguments
    after = sanitize(
        environment_after_sourcing_files(file_and_args, **kwargs), exclude=exclude, include=include
    )

    # Delegate to the other factory
    return EnvironmentModifications.from_environment_diff(before, after, clean)


def environment_after_sourcing_files(
    *files: Union[Path, Tuple[str, ...]], **kwargs
) -> Dict[str, str]:
    """Returns a dictionary with the environment that one would have
    after sourcing the files passed as argument.

    Args:
        *files: each item can either be a string containing the path
            of the file to be sourced or a sequence, where the first element
            is the file to be sourced and the remaining are arguments to be
            passed to the command line

    Keyword Args:
        env (dict): the initial environment (default: current environment)
        shell (str): the shell to use (default: ``/bin/bash`` or ``cmd.exe`` (Windows))
        shell_options (str): options passed to the shell (default: ``-c`` or ``/C`` (Windows))
        source_command (str): the command to run (default: ``source``)
        suppress_output (str): redirect used to suppress output of command
            (default: ``&> /dev/null``)
        concatenate_on_success (str): operator used to execute a command
            only when the previous command succeeds (default: ``&&``)
    """
    # Set the shell executable that will be used to source files
    if sys.platform == "win32":
        shell_cmd = kwargs.get("shell", "cmd.exe")
        shell_options = kwargs.get("shell_options", "/C")
        suppress_output = kwargs.get("suppress_output", "")
        source_command = kwargs.get("source_command", "")
    else:
        shell_cmd = kwargs.get("shell", "/bin/bash")
        shell_options = kwargs.get("shell_options", "-c")
        suppress_output = kwargs.get("suppress_output", "&> /dev/null")
        source_command = kwargs.get("source_command", "source")
    concatenate_on_success = kwargs.get("concatenate_on_success", "&&")

    shell = Executable(shell_cmd)

    def _source_single_file(file_and_args, environment):
        shell_options_list = shell_options.split()

        source_file = [source_command]
        source_file.extend(x for x in file_and_args)
        source_file = " ".join(source_file)

        # If the environment contains 'python' use it, if not
        # go with sys.executable. Below we just need a working
        # Python interpreter, not necessarily sys.executable.
        python_cmd = which("python3", "python", "python2")
        python_cmd = python_cmd.path if python_cmd else sys.executable

        dump_cmd = "import os, json; print(json.dumps(dict(os.environ)))"
        dump_environment_cmd = python_cmd + f' -E -c "{dump_cmd}"'

        # Try to source the file
        source_file_arguments = " ".join(
            [source_file, suppress_output, concatenate_on_success, dump_environment_cmd]
        )
        output = shell(
            *shell_options_list,
            source_file_arguments,
            output=str,
            env=environment,
            ignore_quotes=True,
        )

        return json.loads(output)

    current_environment = kwargs.get("env", dict(os.environ))
    for file in files:
        # Normalize the input to the helper function
        if isinstance(file, str):
            file = (file,)

        current_environment = _source_single_file(file, environment=current_environment)

    return current_environment
