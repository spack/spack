# Using installed software in an IDE

Let's assume you want to work on a C++ code that uses CMake. Further, the
package has many non-trivial dependencies and it makes sense to use `spack` to
install all of them. Therefore, the first step is to clone the repository and
repeatedly invoke variants of `spack dev-build` until everything compiles and
links properly.

Once this succeeds, one could start development using an editor and running
`spack dev-build --overwrite`. However, you want to use an IDE. Let's look at
the files, that were generated as part of the `dev-build`:

  * `spack-build-env.txt` which could be `source`ed to obtain the environment
  `spack` uses.
  * `spack-configure-args.txt` a file with additional arguments passed to CMake.
  * a folder `spack-build-*` which is the output of running CMake.

Remark: It might be a good idea to use `spack` environments to reduce the
number of packages that get listed as dependencies.

## Quick method
Since CMake has been run during the `spack dev-build` and we know the name of
the folder, one may simply use that folder, i.e. tell your IDE to use this
folder instead of what it would use normally.

The IDE is unlikely to be able to recreate this folder, but you can simply
rerun `spack` when needed.

## Using `CMAKE_PREFIX_PATH`
Let's treat `spack` as a package installer; and CMake as the tool which tells
the IDE how to configure itself. For our purposed `spack` works as follows:

  * Every dependency is installed into a unique folder.
  * If multiple versions, also incompatible ones, are installed, `spack` knows
  which ones should be used together.

The trick is to convince CMake that it should find the correct version of each
dependency, this is done by setting through `CMAKE_PREFIX_PATH`.

By inspecting `spack-build-env.txt` we see that it sets the environment variable
`CMAKE_PREFIX_PATH`, containing the long list of paths where each dependency can
be found.

### Option 1
Somehow set the same environment variable in the IDE.

### Option 2
Convert the environment variable into a command line argument
`-DCMAKE_PREFIX_PATH=...`. Small caveat, the environment variable is separated
by colons and in the CLI argument paths must be separated by semi-colons.

There's a script for this:

    bluebrain/bin/spack2cmake.sh SOURCE_DIR

which outputs the required CMake command. Here `SOURCE_DIR` is the directory
containing the `spack-build-env.txt`.

Most IDEs should allow you to pass additional arguments to CMake on a per
project basis. Read the output of the previous command carefully and copy-paste
the required parts to your IDE.

## Using `compile_commands.json`
It's possible that your IDE isn't happy yet. Maybe it simply can't deal directly
with `CMakeLists.txt`. So here a second common trick. CMake can generate a file
called `compile_commands.json`. This is a file that various IDEs/editors can
parse to figure out things like include paths.

How can we generate this file? Use Option 2 in the previous method to generate
a CMake command. Then add the flag `-DCMAKE_EXPORT_COMPILE_COMMANDS=1`. The
complete command will look something like:

    cmake -DCMAKE_PREFIX_PATH=... \
          -DCMAKE_EXPORT_COMPILE_COMMANDS=1 \
          FURTHER_FLAGS \
          -B build

Now point your IDE/editor to the generated file, e.g.
`build/compile_commands.json`.

# Concrete examples
Let's take `touchdetector` as an example and assume you've set up an
environment for it:
```
spacktivate -p TouchDetector
```
Now, clone the repository
```
git clone --recursive git@bbpgitlab.epfl.ch:hpc/circuit-building/touchdetector.git
cd touchdetector
```
Now try building the project with `spack` as follows
```
spack add touchdetector@develop
spack develop --no-clone -p $PWD touchdetector@develop
spack install
```
Maybe you need to specify the compiler, etc. Repeat variants of this step
until it works.

## CLion
Follow the method "Using `CMAKE_PREFIX_PATH`: Option 2".

Start CLion, open the folder or `CMakeLists.txt`. You should be able to find
the settings under "File -> Settings". Then navigate to "Build, Execution,
...". Now you should find a category "CMake" which will have a field "CMake
options", this is where you paste the `-DCMAKE_PREFIX_PATH=...`.

Now CLion should simply configure itself.

## VSCode
Follow the method "Using `CMAKE_PREFIX_PATH`: Option 2" and also "Using
`compile_commands.json`".

Under the setting of the extension `CMake tools` you can set: a) the location
of the `compile_commands.json`. This can probably be a user-wide setting,
especially since you can instruct VSCode to move `compile_commands.json` after
each successful configure.

Now also look for "CMake: Configure Args" this is where you can add

    -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DCMAKE_PREFIX_PATH=...

You can make VSCode print the cmake command it's running.

## QtCreator
Follow the method "Using `CMAKE_PREFIX_PATH`: Option 2".

Open QtCreator, then open the `CMakeLists.txt` pick the Toolchain kits. Under
`Project` you get to set the additional CMake commands.

## Vim with Conquer of Completion
You can turn into an almost IDE using [Conquer of Completion]. In that case
you probably want to follow the path "Using `compile_commands.json`".

[Conquer of Completion]: https://github.com/neoclide/coc.nvim
