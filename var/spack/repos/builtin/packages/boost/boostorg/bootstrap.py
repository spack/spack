def options_windows(spec, toolset_version):
    """
    The only bootstrapping command line option that is accepted by
    'bootstrap.bat' is the compiler information: either the vc version
    (e.g. MSVC 14.3.x would be vc143) or gcc or clang.
    """
    opts = list()

    if spec.satisfies("%msvc"):
        opts.append(f"vc{toolset_version}")
    elif spec.satisfies("%gcc"):
        opts.append("gcc")
    elif spec.satisfies("%clang"):
        opts.append("clang")

    return opts


def options(spec, toolset, with_libs):
    opts = list()

    # Arm compiler bootstraps with 'gcc' (but builds as 'clang')
    if spec.satisfies("%arm") or spec.satisfies("%fj"):
        opts.append("--with-toolset=gcc")
    else:
        opts.append("--with-toolset=%s" % toolset)

    if with_libs:
        opts.append("--with-libraries=%s" % ",".join(with_libs))
    else:
        opts.append("--with-libraries=headers")

    if spec.satisfies("+python"):
        opts.append("--with-python=%s" % spec["python"].command.path)

    if spec.satisfies("+icu"):
        opts.append("--with-icu")
    else:
        opts.append("--without-icu")

    return opts
