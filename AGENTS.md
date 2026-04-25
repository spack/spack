# Spack - Package Manager

Spack is a command-line tool for installing packages and managing dependencies.
All commands are subcommands of "spack", like `spack install...`

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

## Where to Find More

- Documentation: lib/spack/docs/
- Unit tests: lib/spack/spack/tests/
- Package repositories: find with `spack repo list` (look for "builtin")
- Test package repos: var/spack/test_repos/spack_repo/builtin_mock/