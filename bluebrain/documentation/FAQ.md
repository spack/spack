# FAQ for BlueBrain Spack Usage

## Building Software

#### Q: How do I build and *load* a piece of software?

<details>
  <summary>Expand answer</summary>

  We'll install `MG(1)`, a standard editor.

  Make sure you're setup as per
  [the instructions linked on the README](https://github.com/BlueBrain/spack),
  then install the editor via

      $ spack install mg

  One can then run `mg` with

      $ spack load mg
      $ mg foo.txt

</details>

#### Q: Why do I have to rebuild the entire world?

<details>
  <summary>Expand answer</summary>

  If you are on the BlueBrain5, you shouldn't need to.

  As [described here](setup_bb5.md),
  one can use the system packages available with appropriate configuration
  options.
  If those instructions don't help, please use the [#spack](https://bluebrainproject.slack.com/archives/C023KQ47GHL)
  channel on Slack.
</details>

#### Q: Why is it so slow to interact with the Spack repository on GPFS

<details>
  <summary>Expand answer</summary>

  Make sure the `spack` repo is checked out in a subdirectory of `$HOME`.
  The `spack` repository is quite large, and when it is checked out under a
  `/gpfs/bbp.cscs.ch/project/*` directory, performance can be 10x slower
  than on the SSD provided storage of `$HOME`.
</details>

#### Q: Is there a binary cache?

<details>
  <summary>Expand answer</summary>

  No.
  Possibilities are being explored to provide a binary cache configuration
  for our desktops.
</details>

## Modules

#### Q: Why are the module files not being rebuilt?

<details>
  <summary>Expand answer</summary>

  The `spack module tcl refresh` command respects a blacklist that can be
  found via:

      $ spack config blame modules

  This blacklist is overruled by a corresponding whitelist.
  If your software is not listed in the latter, no modules will be
  generated for it.

  Use

      $ spack config add modules:tcl:whitelist:my_package
      $ spack module tcl refresh my_package

  To produce an up-to-date module for `my_package` (adjust as needed).
</details>

## Concretization Issues

#### Q: Why does Spack fail with cryptic error messages

<details>
  <summary>Expand answer</summary>

  When determining what to build (to concretize a spec in "Spack lingo"),
  sometimes Spack will not be able to satisfy the requirements of all
  software needing to be built.
  It may then display a somewhat cryptic error message:

      ❯ spack spec -I py-morphology-repair-workflow\^py-pandas@1.3:
      Input spec
      --------------------------------
       -   py-morphology-repair-workflow
       -       ^py-pandas@1.3:

      Concretized
      --------------------------------
      ==> Error: py-morphology-repair-workflow ^py-pandas@1.3: is unsatisfiable, errors are:
        no version satisfies the given constraints

          To see full clingo unsat cores, re-run with `spack --show-cores=full`
          For full, subset-minimal unsat cores, re-run with `spack --show-cores=minimized
          Warning: This may take (up to) hours for some specs

  By running the recommendation, one may produce more cryptic output:

      ❯ spack --show-cores=full spec -I py-morphology-repair-workflow\^py-pandas@1.3:
      Input spec
      --------------------------------
       -   py-morphology-repair-workflow
       -       ^py-pandas@1.3:

      Concretized
      --------------------------------
      ==> Error: py-morphology-repair-workflow ^py-pandas@1.3: is unsatisfiable, conflicts are:
        condition(5258)
        condition(5275)
        condition(5281)
        dependency_condition(5258,"py-morph-validator","py-pandas")
        dependency_condition(5275,"py-morphology-repair-workflow","py-morph-validator")
        dependency_condition(5281,"py-morphology-repair-workflow","py-pandas")
        dependency_type(5258,"build")
        dependency_type(5275,"run")
        dependency_type(5281,"run")
        imposed_constraint(5258,"version_satisfies","py-pandas","0.25:1.2.99")
        no version satisfies the given constraints
        root("py-morphology-repair-workflow")
        version_satisfies("py-pandas","1.3:")

          For full, subset-minimal unsat cores, re-run with `spack --show-cores=minimized
          Warning: This may take (up to) hours for some specs

  By analyzing the output, it can be seen that
  `py-morphology-repair-workflow` depends on `py-morph-validator`,
  which in turn depends on `py-pandas` between versions `0.25` and
  `1.2.99` (using the numerical references together with the package names
  / versions).
  This in turn conflicts with the user requirement of a `py-pandas` newer
  than `1.3`.
  Removing said user requirement will make the software install.
  In other instances, loosening dependency requirements in packages may be
  the appropriate solution.
</details>
