def config(spec):
    toolsets = {
        "%gcc": "gcc",
        "%intel": "intel",
        "%oneapi": "intel",
        "%clang": "clang",
        "%arm": "clang",
        "%xl": "xlcpp",
        "%xl_r": "xlcpp",
        "%nvhpc": "pgi",
        "%fj": "clang",
    }

    if spec.satisfies("@1.47:"):
        toolsets["%intel"] += "-linux"
        toolsets["%oneapi"] += "-linux"

    for cc, toolset in toolsets.items():
        if spec.satisfies(cc):
            return toolset

    # fallback to gcc if no toolset found
    return "gcc"
