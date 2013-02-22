import spack.stage as stage

description = "Remove all temporary build files and downloaded archives"

def purge(parser, args):
    stage.purge()
