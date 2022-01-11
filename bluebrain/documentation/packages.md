# Package structure

The official Spack packages can be found in the `builtin` repository:

    ${SPACK_ROOT}/var/spack/repos/builtin/packages/${PACKAGE}/package.py

These packages should only be modified if all other measures fail.
Excessive modifications to this repository will impede future Spack
updates.

Packages derived from builtin packages or new packages targeting code not
owned by BlueBrain are stored in the `patches` repository:

    ${SPACK_ROOT}/bluebrain/repo-patches/packages/${PACKAGE}/package.py

Finally, code specific to BlueBrain can be found in the `bluebrain`
repository:

    ${SPACK_ROOT}/bluebrain/repo-bluebrain/packages/${PACKAGE}/package.py

Packages for any of these repositories can be installed explicitly by
prepending the repository namespace to a package name, for example:

    $ spack install builtin.spark
    $ spack install patches.spark
    $ spack install bluebrain.touchdetector

If no namespace is used, the `bluebrain` repository will be used if it
contains the requested package, otherwise the `patches` repository, before
finally falling back to the `builtin` one.

## Creating new packages with non-BlueBrain code

To create new packages for non-BlueBrain software, please use the `patches`
repository.
For example, use the builtin `spack` commands to create a skeleton:

    $ spack create -t python -N patches py-my-dreams

## Adding new versions or modifying packages with non-BlueBrain code

For convenience, the `augment` command can be used to create a `patches`
package based on the `builtin` one.
To add a new version to `py-black`, first run the checksum on the latest
available:

    $ spack checksum --latest py-black
    ==> Found 1 version of py-black:

      21.12b0  https://files.pythonhosted.org/packages/f7/60/7a9775dc1b81a572eb26836c7e77c92bf454ada00693af4b2d2f2614971a/black-21.12b0.tar.gz#sha256=77b80f693a569e2e527958459634f18df9b0ba2625ba4e0c2d5da5be42e6f2b3

    ==> Fetching https://files.pythonhosted.org/packages/f7/60/7a9775dc1b81a572eb26836c7e77c92bf454ada00693af4b2d2f2614971a/black-21.12b0.tar.gz#sha256=77b80f693a569e2e527958459634f18df9b0ba2625ba4e0c2d5da5be42e6f2b3

        version('21.12b0', sha256='77b80f693a569e2e527958459634f18df9b0ba2625ba4e0c2d5da5be42e6f2b3')

Now `augment` the `builtin` package:

    $ spack augment py-black

The created package now looks like:

    from spack import *
    from spack.pkg.builtin.py_black import PyBlack as BuiltinPyBlack


    class PyBlack(BuiltinPyBlack):
        pass

Modify it to include the new version:

    from spack import *
    from spack.pkg.builtin.py_black import PyBlack as BuiltinPyBlack


    class PyBlack(BuiltinPyBlack):
        version('21.12b0', sha256='77b80f693a569e2e527958459634f18df9b0ba2625ba4e0c2d5da5be42e6f2b3')

Modifications done here can include `version`, `depends_on`, `patch`
directives, and may overwrite other package related functions.

For packages that utilize a lot of meta-programming, it may be easier to
"clone" the recipe and perform the modifications on the clone.
When using `neovim` (or `vim`) as `$EDITOR`

    $ spack augment -s py-black

will open a split window with both the original and augmented packages
displayed.
The original recipe can then be easily duplicated and modified.

## Creating new packages with BlueBrain code

To create new packages for BlueBrain software, please use the `bluebrain`
repository.
For example, use the builtin `spack` commands to create a skeleton with the
`bluebrain` repository as the default:

    $ spack create -t python py-my-dreams

## Adding new versions or modifying packages with BlueBrain code

The builtin commands should defer to the `bluebrain` repository by default,
and, i.e.

    $ spack edit py-my-dreams

should work out of the box.
