import argparse
import spack
from spack.config import config

parser = argparse.ArgumentParser(
    description="Add C/C++ compiler flags to Spack configuration."
)
parser.add_argument(
    "--scope", default="user", help="Configuration scope to read/write."
)
parser.add_argument("--compiler-spec", type=str, help="Compiler spec to modify.")
parser.add_argument(
    "--fields",
    type=str,
    nargs="+",
    help="Which type of flags to write.",
    default=["cflags", "cxxflags"],
    choices=["cflags", "cxxflags", "cppflags", "fflags", "ldflags", "ldlibs"],
)
parser.add_argument(
    "flags", type=str, nargs="+", help="Compiler flags to set in the configuration."
)
args = parser.parse_args()
flags_str = " ".join(args.flags)
compiler_configs = config.get("compilers", scope=args.scope)
for compiler_config in compiler_configs:
    compiler_spec = spack.spec.Spec(compiler_config["compiler"]["spec"])
    if compiler_spec.satisfies(args.compiler_spec):
        compiler_flags = compiler_config["compiler"].get("flags", {})
        for field in args.fields:
            compiler_flags[field] = flags_str
        compiler_config["compiler"]["flags"] = compiler_flags
config.update_config("compilers", compiler_configs, scope=args.scope)
