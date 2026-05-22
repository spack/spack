..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Glossary of terms used throughout the Spack documentation.

========
Glossary
========

This page collects definitions for the terms that appear throughout the Spack documentation.
For an alphabetic list of every documented keyword and environment variable, see the :ref:`general index <genindex>`.

.. glossary::
   :sorted:

   spec
      A description of a package configuration: name, version, variants, compiler, flags, architecture, and dependencies.
      Specs are Spack's central data structure and the syntax users type on the command line.
      See :doc:`spec_syntax` and :ref:`sec-specs`.

   abstract spec
      A spec that is only partially specified.
      Missing fields (version, variants, compiler, dependencies) are filled in during :term:`concretization`.
      Anything a user types on the command line is an abstract spec until it is concretized.

   concrete spec
      A fully specified spec in which every field is fixed: an exact version, all variant values, a compiler, an architecture, and a concrete spec for every dependency in the :term:`DAG`.
      Concrete specs are what Spack actually installs; they are identified by a :term:`DAG hash`.

   root spec
   root
      A spec the user requested directly: an argument to ``spack install`` or an entry in an :term:`environment`'s ``spack.yaml`` ``specs:`` list.
      Roots are the starting points of concretization; everything else in the resulting :term:`DAG` is a dependency pulled in to satisfy a root.
      Under ``concretizer:reuse:`` the ``roots:`` key controls whether roots themselves may be reused or must be solved fresh.

   explicit
   implicit
      A property of an installed spec recorded in the :term:`database`.
      A spec is *explicit* if it was requested directly (a ``spack install`` argument or an environment :term:`root spec <root>`); it is *implicit* if it was only installed as a dependency of something else.
      Explicit installs are preserved by ``spack gc``; implicit installs become eligible for garbage collection once no installed spec depends on them.
      ``spack mark -e/-i`` toggles the flag on an existing install, ``spack find --explicit`` / ``--implicit`` filters by it, and a :term:`spec group` with ``explicit: false`` installs its specs as implicit.

   fresh
      The concretizer policy of ignoring already-installed and cached specs and solving for the newest configuration allowed by the constraints.
      Selected with ``spack install --fresh`` / ``spack concretize --fresh``; the opposite of :term:`reuse`.
      ``--fresh-roots`` is a middle ground: solve :term:`root specs <root>` fresh while still reusing their dependencies.

   anonymous spec
      A spec without a package name, used to express constraints that should apply to any package (for example in ``packages.yaml``).
      See :ref:`anonymous_specs`.

   spec syntax
      The textual language used to write specs, with sigils for version (``@``), compiler (``%``), variants (``+`` / ``~`` / ``name=value``), dependencies (``^``), flags (``cflags=...``), architecture (``arch=...``), and hashes (``/``).
      See :doc:`spec_syntax`.

   propagation
      Pushing a variant value or compiler flag down through a spec's dependencies.
      Written with doubled sigils: ``++variant``, ``cflags==-O3``, ``%%compiler``.

   variant
      A named build option on a package.
      Variants can be boolean (``+mpi`` / ``~mpi``), single-valued (``build_type=Release``), or multi-valued (``fabrics=verbs,psm``).
      See :ref:`basic-variants`.

   sticky variant
      A variant the concretizer is not allowed to flip silently.
      The user (or a requirement) must set its value explicitly.

   version
      A specific release of a package, declared in ``package.py`` with the ``version(...)`` directive.
      Versions are ordered and can be compared, e.g. ``@1.2:1.4``.
      See :ref:`version-specifier`.

   version range
      A constraint of the form ``@low:high``, ``@low:``, or ``@:high`` that matches any version inside the interval.

   version list
      A comma-separated set of versions or ranges, e.g. ``@1.2,1.4:1.6``.

   architecture spec
      The platform, operating system, and target microarchitecture for a build, written as ``arch=platform-os-target`` (e.g. ``arch=linux-ubuntu22.04-zen3``).
      See :ref:`architecture_specifiers`.

   target
      The microarchitecture portion of an :term:`architecture spec`, resolved by ``archspec`` (e.g. ``zen3``, ``skylake_avx512``, ``neoverse_v2``).

   compiler flags
      Flags injected at build time via spec syntax, namespaced by language: ``cflags``, ``cxxflags``, ``fflags``, ``cppflags``, ``ldflags``, ``ldlibs``.
      See :ref:`compiler_flags`.

   compiler wrapper
      The script Spack puts in ``PATH`` in place of the real compiler.
      It rewrites the command line, injects RPATHs, filters flags, and enforces Spack's build environment.
      See :ref:`compiler-wrappers`.

   package
   recipe
      A Python class describing how to fetch, configure, build, and install a piece of software.
      Lives in a ``package.py`` file inside a :term:`repository <repo>`.
      See :doc:`package_fundamentals`.

   directive
      A decorator-style call used in a ``package.py`` body to declare package metadata: ``version``, ``depends_on``, ``variant``, ``provides``, ``conflicts``, ``requires``, ``patch``, ``resource``, ``extends``, and so on.

   build system
      A mixin base class that knows how to drive a particular build tool: ``Package``, :class:`~spack_repo.builtin.build_systems.cmake.CMakePackage`, :class:`~spack_repo.builtin.build_systems.autotools.AutotoolsPackage`, :class:`~spack_repo.builtin.build_systems.meson.MesonPackage`, and so on.
      See :doc:`build_systems`.

   virtual package
      A name (such as ``mpi``, ``blas``, ``lapack``, or ``c``) that represents an interface rather than a concrete implementation.
      Real packages :term:`provide <provider>` virtuals.

   provider
      A package that satisfies a :term:`virtual package`.
      For example, ``openmpi`` and ``mpich`` both provide ``mpi``.

   dependency type
      The role a dependency plays: ``build`` (only needed during the build), ``link`` (linked into the dependent), ``run`` (needed at run time), or ``test`` (needed only when running tests).
      A single ``depends_on`` may carry multiple types.
      See :ref:`dependency-types`.

   direct dependency
      A dependency that appears in a package's own ``depends_on`` declarations, i.e. one edge away in the :term:`DAG`.
      In :doc:`spec_syntax` the ``%`` sigil constrains direct dependencies (``hdf5 %gcc@15``); contrast with :term:`transitive dependency`.

   transitive dependency
      A dependency reachable through one or more intermediate packages, i.e. a dependency of a dependency.
      The ``^`` sigil constrains transitive dependencies (``hdf5 ^hwloc+cuda``).
      A view's ``link: run`` / ``link: all`` options pull in :term:`root spec <root>` transitive dependencies of the corresponding :term:`types <dependency type>`.

   phase
   install phase
   build phase
      One step of a :term:`build system`'s install lifecycle.
      The ordered list lives in the builder's ``phases`` attribute, for example ``("configure", "build", "install")`` for autotools or ``("build", "install")`` for ruby gems.
      Each phase is a method on the builder class and can be overridden, replaced, or wrapped with ``run_before`` / ``run_after``.
      *Install phase* names the specific ``install`` step (and, by extension, post-install hooks attached to it); *build phase* is used loosely for any phase in the lifecycle.
      See :ref:`overriding-phases`.

   build environment
      The shell environment Spack constructs for a package's build: ``PATH``, compiler wrappers, ``CC`` / ``CXX`` / ``F77`` / ``FC``, ``CPATH``, ``LIBRARY_PATH``, ``CMAKE_PREFIX_PATH``, jobserver ``MAKEFLAGS``, and any variables set by ``setup_build_environment`` or by dependencies' ``setup_dependent_build_environment``.
      ``spack build-env <spec>`` prints it; passing a shell as the command (``spack build-env <spec> sh``) drops you into it, and ``--dump`` / ``--pickle`` write it to a file.

   module set
      A named block under ``modules:`` in ``modules.yaml`` that produces its own collection of module files with its own install root, naming scheme, and inclusion rules.
      The default set is called ``default``; module commands target it unless ``--name <set>`` is given.
      See :ref:`modules-yaml`.

   build cache index
      A JSON manifest in a :term:`buildcache` listing every binary it contains together with their hashes and dependencies.
      The concretizer downloads it (or its OCI-manifest equivalent) to decide which binaries are eligible for :term:`reuse` without fetching every individual spec.
      Refreshed with ``spack buildcache update-index`` and ``spack buildcache push --update-index``; see :ref:`binary_caches`.

   spack instance
      A Spack installation itself, addressable in config as ``$spack``.
      In the context of :term:`chained install trees <chained install tree>`, "upstream instance" is often used informally to refer to that instance's :term:`store`.

   standalone test
   stand-alone test
      A test defined by a package's ``test_*`` methods and executed *after* installation by ``spack test run`` against an installed :term:`prefix`.
      Distinct from build-time tests run during the ``check`` :term:`build phase` of an autotools/cmake build.
      See :ref:`cmd-spack-test` and the testing section of the packaging guide.

   patch
      A source patch applied to a package before configuring.
      Declared with the ``patch(...)`` directive; see :ref:`patching`.

   resource
      An extra archive fetched alongside the main source and unpacked under the build stage.
      Declared with the ``resource(...)`` directive.

   extension
      A package installed into another package's prefix-like namespace, most commonly a Python extension installed into a Python ``site-packages`` view.
      See :ref:`packaging_extensions`.

   external package
      A package that is *not* built by Spack but found on the system and registered through ``packages.yaml``.
      Used for vendor-provided compilers, MPI, CUDA, system libraries, etc.

   repo
   repository
      A directory tree containing package recipes plus a ``repo.yaml``.
      Multiple repos can be layered, each contributing packages under a :term:`namespace`.
      See :doc:`repositories`.

   namespace
      A repo's identifier (``repo.yaml``'s ``namespace:`` key).
      Fully qualified package names take the form ``namespace.name`` (e.g. ``builtin.zlib``).
      See :ref:`namespaces`.

   DAG
      Directed acyclic graph.
      A concretized spec is a DAG of concrete specs (one per package), because in general a package may appear multiple times with different configurations or roles.

   concretization
      The process of turning an :term:`abstract spec` and the surrounding configuration into a :term:`concrete spec` DAG.
      Performed by the concretizer.

   concretizer
      Spack's solver.
      The current implementation translates specs and package constraints to Answer Set Programming, runs ``clingo``, and reads concrete specs back out.
      See :ref:`concretizer-options`.

   clingo
      The Answer Set Programming (ASP) solver used by the :term:`concretizer`.

   reuse
      The concretizer policy of preferring already-installed or cached specs over rebuilding from scratch.
      Tunable through ``concretizer:reuse``.

   requirement
      A hard constraint declared in ``packages.yaml`` under ``require:``.
      The concretizer must satisfy it or fail.
      See :ref:`package-requirements`.

   preference
      A soft constraint declared with ``prefer:`` (or via ``packages:all:`` ordering).
      Used as a tiebreaker; the concretizer may ignore it if it cannot be met.
      See :ref:`package-preferences`.

   toolchain
      A reusable bundle of compiler and library choices that packages can opt into, configured in ``toolchains.yaml``.
      See :doc:`toolchains_yaml`.

   store
   install tree
      The directory tree where Spack installs packages, one per :term:`prefix`.
      Backed by a :term:`database` that indexes every install.

   prefix
      The installation directory of a single concrete spec inside the :term:`store`.
      The default layout is ``<platform>-<target>/<name>-<version>-<hash>`` relative to the store root.

   database
      The JSON-backed index of every installed spec in the :term:`store`.
      Acts as a cache so Spack does not need to walk the install tree.

   manifest
      The ``spack.yaml`` file describing an :term:`environment`: the root specs, configuration overrides, and view settings.
      Concretizing the manifest produces the :term:`spack.lock` lockfile.

   DAG hash
      The cryptographic hash that identifies a :term:`concrete spec`.
      Computed over the full DAG (name, version, variants, compiler, flags, arch, and dependency hashes).
      Used as the directory suffix in the :term:`prefix` and as the spec's primary key.

   package hash
      A hash of the ``package.py`` source (and its build inputs), tracked so Spack can detect recipe changes.
      Distinct from the :term:`DAG hash`.

   environment
      A named, declarative collection of root specs plus configuration, stored in ``spack.yaml``, concretized to ``spack.lock``.
      The unit of reproducible deployments in Spack.
      See :doc:`environments`.

   managed environment
      An environment stored in Spack's environment directory and addressed by name (``spack env activate myenv``).

   anonymous environment
      An environment activated by directory path (``spack env activate ./my-env``).
      Not registered under a name.

   spack.yaml
      The human-edited manifest of an :term:`environment`: the specs to build, the configuration overrides, and the view settings.

   spack.lock
      The concretized lockfile of an :term:`environment`: a frozen DAG of concrete specs that Spack reuses across activations and machines.

   view
      A unified directory (symlinks, hardlinks, or copies) projecting an environment's installs into one tree, suitable for ``PATH``-style use.
      See :ref:`configuring_environment_views`.

   spec group
      A named set of specs inside an environment, sharing constraints and concretization rules.
      See :ref:`environment-spec-groups`.

   develop spec
      A spec that builds from a local source directory instead of a fetched archive, so edits to the sources trigger a rebuild on the next install.
      It carries a ``dev_path=<path>`` variant pointing at the working tree, and is set up with ``spack develop``.

   mirror
      A location (URL or path) Spack consults for source tarballs and patches before fetching upstream.
      See :doc:`mirrors`.

   binary mirror
   buildcache
      A mirror that hosts pre-built binary packages.
      Spack can both push to and install from build caches.
      See :doc:`binary_caches`.

   OCI buildcache
      A buildcache layered into an OCI registry (Docker Hub, GHCR, ...) so binaries can be distributed alongside container images.
      See :ref:`binary_caches_oci`.

   signing
      Cryptographic signing of buildcache contents with GPG so installers can verify provenance.
      See :doc:`signing`.

   bootstrap
      The process by which Spack provisions its own runtime dependencies (``clingo``, ``gnupg``, patchelf) on a fresh system.
      See :doc:`bootstrapping`.

   stage
      The temporary working directory where a package's sources are unpacked and built.

   jobserver
      A POSIX jobserver, compatible with GNU Make's protocol, that bounds the total number of concurrent build jobs across all packages building in parallel.
      Spack creates one when ``-j<N>`` is passed (or inherits an external one from ``MAKEFLAGS``) and forwards it to every package's build environment.
      See :ref:`installing`.

   build job
      A unit of work scheduled against the :term:`jobserver` (e.g. a single ``cc`` invocation).
      ``spack install -j<N>`` (or ``config:build_jobs``) caps the total number of in-flight build jobs across all concurrently building packages.

   concurrent packages
      The maximum number of packages Spack builds in parallel, controlled by ``spack install -p<N>`` / ``--concurrent-packages``.
      Unbounded by default; packages start as :term:`jobserver` tokens become available.

   fetch strategy
      The mechanism used to obtain a package's source: a URL tarball, ``git``, ``hg``, ``svn``, ``cvs``, or a buildcache.
      See :ref:`vcs-fetch`.

   sbang
      Spack's shebang trampoline for ``#!`` lines that exceed the kernel length limit.
      Installed as a post-install hook.

   RPATH
   runpath
      A linker-embedded library search path baked into installed binaries so they find their dependencies without ``LD_LIBRARY_PATH``.
      See :ref:`handling_rpaths`.

   hook
      A Python callback that runs at a defined point in the install lifecycle (pre-install, post-install, pre-uninstall, ...).

   module file
      A generated file (Lua for Lmod, TCL for environment-modules) that loads a package's run environment into the user's shell.
      See :doc:`module_file_support` and :ref:`modules-yaml`.

   Lmod
      A Lua-based module system Spack can generate module files for.

   TCL modules
      The classic environment-modules module system Spack can also target.

   configuration scope
   scope
      A named layer of YAML configuration.
      Scopes from lowest to highest precedence: ``defaults``, ``system``, ``site``, ``user``, custom (``-C``), environment, command line.
      See :ref:`configuration-scopes`.

   config.yaml
      The top-level configuration file controlling install paths, build concurrency, locks, modules, and similar settings.
      See :doc:`config_yaml`.

   packages.yaml
      Per-package configuration: external packages, version preferences, requirements, variants.
      See :doc:`packages_yaml`.

   mirrors.yaml
      Configuration of source and binary mirrors.

   modules.yaml
      Configuration of module file generation.

   repos.yaml
      The list of active package repositories.

   include chain
      A sequence of ``include:`` directives pulling additional YAML files (or environments) into a configuration.
      See :doc:`include_yaml`.

   CI pipeline
      A generated GitLab pipeline that builds and pushes binaries for the specs in an environment.
      See :doc:`pipelines`.

   container image
      A Docker/OCI image of a Spack-built software stack.
      Spack can produce one either by exporting already-installed specs with ``spack buildcache push --base-image`` to an OCI registry, or by generating a ``Dockerfile`` / Singularity definition from an environment with ``spack containerize``.
      See :doc:`containers`.

   chained install tree
      A read-only :term:`upstream` :term:`store` mounted into a downstream Spack installation so its installs can be reused.
      See :doc:`chain`.

   upstream
      Another :term:`spack instance` whose :term:`store` is registered (via ``upstreams.yaml``) as a read-only source of installed packages for the local instance.
      See :doc:`chain`.

   splice
   splicing
      Replacing a dependency in a :term:`concrete spec` with a different, ABI-compatible spec that provides the same package or :term:`virtual package`.
      A *transitive* splice also pulls in the replacement's own dependencies; an *intransitive* splice keeps the original root's dependencies.
      Spliced specs retain a ``build_spec`` pointing at the unspliced original.
      Splices are configured under ``concretizer:splice:`` (explicit) or via ``can_splice`` directives (automatic).
      Most often used to swap a generic MPI from a public buildcache for a site-tuned one.
      See :doc:`build_settings` and :ref:`automatic_splicing`.

   microarchitecture
      A specific CPU model recognized by ``archspec`` (``zen3``, ``skylake_avx512``, ``neoverse_v2``, ...) and used as the :term:`target` portion of an :term:`architecture spec`.
      The concretizer can label nodes either with full microarchitectures or with generic families (``x86_64_v3``) via ``concretizer:targets:granularity``.
      See :ref:`concretizer-options`.

   provenance
      Recorded information about how an install was produced: the source checksum or git commit, the compiler and its flags, the patches applied, and any develop-source path.
      Spack tracks provenance in the per-install ``install_manifest.json``, in the :term:`SBOM`, and in spec metadata such as the ``commit`` variant for git-based versions and the ``dev_path`` variant for develop specs.

   deprecate
   deprecation
      Marking a version (or whole package) as no longer supported.
      Package authors set ``deprecated=True`` on a ``version(...)`` directive; ``spack install`` then prompts before fetching, and ``spack info`` hides the version unless ``--deprecated`` is passed.
      Distinct from ``spack deprecate``, which replaces one installed spec with another in the :term:`store` by symlinking the old prefix at the new one.
      See :ref:`deprecate`.

   SBOM
      A Software Bill of Materials emitted by Spack in SPDX-2.3 format for every installation.
      Written under ``<prefix>/.spack/sbom/`` and meets NTIA minimum elements.
      See :ref:`sbom`.

   mixin
      A package base class that contributes variants, dependencies, and helper methods without being a full :term:`build system` on its own.
      :class:`~spack_repo.builtin.build_systems.cuda.CudaPackage`, :class:`~spack_repo.builtin.build_systems.rocm.ROCmPackage`, and :class:`~spack_repo.builtin.build_systems.sourceforge.SourceforgePackage` are typical examples, combined with a concrete build system via multiple inheritance.

   non-redistributable
      A package whose source or binaries may not be republished, expressed with the ``redistribute(source=False, binary=False, when=...)`` directive.
      ``spack mirror create`` and ``spack buildcache push`` skip such artifacts by default; ``--private`` opts them back in for internal mirrors.

   sandbox
   sandboxing
      An opt-in Linux build isolation mode that confines a package's build phase using Landlock, restricting filesystem and (optionally) network access.
      Configured under ``config:sandbox:`` with ``allow_read`` / ``allow_read_write`` paths; intended for reproducibility and bug containment, not as a strict security boundary.
      See :doc:`installing`.
