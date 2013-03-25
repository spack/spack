import os
from subprocess import check_call, check_output
import spack
from spack import new_path
import spack.tty as tty

description = "Create a new installation of spack in another prefix"

def setup_parser(subparser):
    subparser.add_argument('prefix', help="names of prefix where we should install spack")


def get_origin_url():
    git_dir = new_path(spack.prefix, '.git')
    origin_url = check_output(
        ['git', '--git-dir=%s' % git_dir, 'config', '--get', 'remote.origin.url'])
    return origin_url.strip()


def install_spack(parser, args):
    origin_url = get_origin_url()
    prefix = args.prefix

    tty.msg("Fetching spack from origin: %s" % origin_url)

    if os.path.exists(new_path(prefix, '.git')):
        tty.die("There already seems to be a git repository in %s" % prefix)

    files_in_the_way = os.listdir(prefix)
    if files_in_the_way:
        tty.die("There are already files there!  Delete these files before installing spack.",
                *files_in_the_way)

    tty.msg("Installing:",
            "%s/bin/spack" % prefix,
            "%s/lib/spack/..." % prefix)

    os.chdir(prefix)
    check_call(['git', 'init', '--shared', '-q'])
    check_call(['git', 'remote', 'add', 'origin', origin_url])
    check_call(['git', 'fetch', 'origin', 'master:refs/remotes/origin/master', '-n', '-q'])
    check_call(['git', 'reset', '--hard', 'origin/master', '-q'])

    tty.msg("Successfully installed spack in %s" % prefix,
            "Run %s/bin/spack to use this installation." % prefix)
