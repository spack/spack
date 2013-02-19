import os

def parse_rpaths(arguments):
    """argparse, for all its features, cannot understand most compilers'
       rpath arguments.  This handles '-Wl,', '-Xlinker', and '-R'"""
    linker_args = []
    other_args = []

    def get_next(arg, args):
        """Get an expected next value of an iterator, or die if it's not there"""
        try:
            return next(args)
        except StopIteration:
            # quietly ignore -rpath and -Xlinker without args.
            return None

    # Separate linker args from non-linker args
    args = iter(arguments)
    for arg in args:
        if arg.startswith('-Wl,'):
            sub_args = [sub for sub in arg.replace('-Wl,', '', 1).split(',')]
            linker_args.extend(sub_args)
        elif arg == '-Xlinker':
            target = get_next(arg, args)
            if target != None:
                linker_args.append(target)
        else:
            other_args.append(arg)

    # Extract all the possible ways rpath can appear in linker args
    # and append non-rpaths to other_args
    rpaths = []
    largs = iter(linker_args)
    for arg in largs:
        if arg == '-rpath':
            target = get_next(arg, largs)
            if target != None:
                rpaths.append(target)

        elif arg.startswith('-R'):
            target = arg.replace('-R', '', 1)
            if not target:
                target = get_next(arg, largs)
                if target == None: break

            if os.path.isdir(target):
                rpaths.append(target)
            else:
                other_args.extend(['-Wl,' + arg, '-Wl,' + target])
        else:
            other_args.append('-Wl,' + arg)
    return rpaths, other_args
