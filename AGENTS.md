# Spack - Package Manager

Spack is a command-line tool for installing packages and managing dependencies.
All commands are subcommands of "spack", like `spack install...`

## Initializing Spack

**IMPORTANT:** Before running any `spack` commands, you must source the setup script:
- **Bash/sh:** `. share/spack/setup-env.sh`
- **tcsh/csh:** `source share/spack/setup-env.csh`

This adds the `spack` command to your PATH. Run this from the Spack root directory, or use the full path.

**Finding package definitions:**
- `spack location -p <package>`: Get the directory containing a package's package.py
- `spack repo list`: Show all package repositories (look for "builtin" for the main repo)

## Quick Reference (Common Tasks)

**Environments:**
- Create: `spack env create <name>`
- Activate: `spack env activate <name>`
- Add package: `spack add <spec>`
- Edit config: `spack config edit` (opens spack.yaml)

**Installing:**
- Install package: `spack install <spec>`
- Concretize (solve deps): `spack concretize`
- View installed: `spack find`

**External packages (use system packages instead of building):**
- Auto-detect: `spack external find <package>`
- Manual config: edit spack.yaml or ~/.spack/packages.yaml
- Add externals section under packages:<package>:externals:
- Use `buildable: false` to prevent Spack from building its own

**Spec syntax:**
- Version: `package@version`
- Variants: `package+feature` or `package~feature`
- Dependencies: `package ^dependency@version`

## Common Issues & Debugging

**Configuration & Debugging:**
- `spack config blame <section>`: Show which config file/scope set each value
- `spack debug report`: Get system info including Spack version, commit
- `spack spec <package>`: See how a package would be configured before installing
- Config scope precedence: `spack` > `user` > `site` > `system` > `defaults`
- Environments have their own config scope that overrides others when active

**Environment Gotchas:**
- Environments use `spack.lock` to pin exact versions after concretization
- Concrete specs in lockfiles continue to work even if package definitions change/disappear
- Re-concretize with `spack concretize -f` to get updates
- `spack find` behaves differently inside vs. outside environments
- Use `spack find -x` to exclude already-installed dependencies from output
- Can reuse/share specs between environments with `concretizer:reuse` config

**Compilers:**
- Compilers are defined as external packages in packages.yaml (not a separate compilers.yaml)
- Can add custom flags in the external definition under `extra_attributes:flags:`
- Use `spack compiler find` or `spack external find <compiler-package>` to auto-detect
- Target requirements (`packages:all:require: [target=x86_64_v3]`) interact with compiler definitions

**Example compiler with custom flags in packages.yaml:**
```yaml
packages:
  gcc:
    externals:
    - spec: gcc@11.2.0
      prefix: /usr
      extra_attributes:
        compilers:
          c: /usr/bin/gcc
          cxx: /usr/bin/g++
        flags:
          cflags: -Wall
```

**External Packages:**
- External packages with modules are loaded in topological order (leaf to root)
- Only transitive link/run dependencies have their modules loaded during builds

**Parallel Operations:**
- Multiple `spack install` commands can run simultaneously
- Spack will detect when another process is installing and wait appropriately
- Lock files prevent conflicts during concurrent installations

**Views:**
- Python extensions in views get special handling for shebang rewriting
- Views don't copy binaries unnecessarily, only scripts with shebangs need patching

## Where to Find More

- Documentation: lib/spack/docs/
- Unit tests: lib/spack/spack/tests/
- Package repositories: find with `spack repo list` (look for "builtin")
- Test package repos: var/spack/test_repos/spack_repo/builtin_mock/