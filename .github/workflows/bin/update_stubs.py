import argparse
import difflib
import subprocess
import sys
import tempfile
from pathlib import Path


def manage_stubs(module_name: str, stub_path: Path, fix: bool) -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            subprocess.run(
                [sys.executable, "-m", "mypy.stubgen", "-m", module_name, "-o", temp_dir],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running stubgen:\n{e.stderr}", file=sys.stderr)
            return 1

        generated_files = list(Path(temp_dir).rglob("*.pyi"))
        if not generated_files:
            print(
                f"Error: stubgen did not generate any .pyi files for {module_name}.",
                file=sys.stderr,
            )
            return 1

        generated_content = generated_files[0].read_text(encoding="utf-8")

    existing_content = ""
    if stub_path.exists():
        existing_content = stub_path.read_text(encoding="utf-8")

    if generated_content == existing_content:
        print(f"Stub for '{module_name}' is up to date.")
        return 0

    if fix:
        stub_path.parent.mkdir(parents=True, exist_ok=True)
        stub_path.write_text(generated_content, encoding="utf-8")
        print(f"Updated stub file in-place: {stub_path}")
        return 0
    else:
        print(
            f"CI Check Failed: The stub file at {stub_path} is out of sync with '{module_name}'.",
            file=sys.stderr,
        )
        print("Diff:", file=sys.stderr)

        diff = difflib.unified_diff(
            existing_content.splitlines(),
            generated_content.splitlines(),
            fromfile=str(stub_path),
            tofile="generated_stub",
            lineterm="",
        )
        for line in diff:
            print(line, file=sys.stderr)

        print("\nFix this by running the script locally with the --fix flag.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", default="spack.package")
    parser.add_argument("--stub-path", type=Path, required=True)
    parser.add_argument("--fix", action="store_true")

    args = parser.parse_args()
    sys.exit(manage_stubs(args.module, args.stub_path, args.fix))
