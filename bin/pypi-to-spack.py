from __future__ import print_function
import xmlrpclib
import os
import sys

# https://wiki.python.org/moin/PyPIXmlRpc

ext_sortorder = {'.tar.gz':0, '.zip':1}

depends_on_template = "    depends_on('{package}', when='@{version}')"

version_template = \
"""    version('{version}', '{md5_digest}',
        url='{url}')"""


package_template = """
from spack import *
import platform


class {package}(PyPIPackage):
    \"\"\"{description}\"\"\"

    homepage = "{home_page}"

{versions}

{depends_ons}

    extends('python')
"""




def get_source_url(name, version):
    """Returns the URL needed to download a package from PyPI.
    name:
        Name of the package in PyPI
    version: (str)
        Version of the pacakge to download
    extension:
        Filename extension desired

    Raises KeyError if the desired PyPI URL cannot be located.

    See: https://wiki.python.org/moin/PyPIXmlRpc
    """

    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    releases = client.release_urls(name, version)

    good_url_recs = []
    for release in releases:
        if release['packagetype'] != 'sdist':
            continue
        _,ext = os.path.splitext(release['filename'])
        good_url_recs.append((ext_sortorder.get(ext,len(ext_sortorder)), release))

    good_url_recs.sort()
    if len(good_url_recs) > 0:
        return good_url_recs[0][1]
    else:
        return None

def get_versions(pypi, package):
    # Get all version info for this package
    versions = []
    for ver in pypi.package_releases(package, True):
        data = pypi.release_data(package, ver)

        # Not all package versions have a valid URL that is useful to us.
        url = get_source_url(package,ver)
        if url is not None:
            data.update(url)
        else:
            data['url'] = data['download_url']
            data['md5_digest'] = ''    # TODO: Download and figure this out
        versions.append(data)
    return versions


def write_package_list(pypi):
    with open('pypi-packages.txt', 'w') as fout:
        for package in pypi.list_packages():
            fout.write(package + '\n')


def convert_package(pypi, package):
    versions = get_versions(pypi, package)
    version_lines = []
    depends_on_lines = []
    for ver in versions:
        version_lines.append(version_template.format(
            version=ver['version'],
            md5_digest=ver['md5_digest'],
            url=ver['url']))
        for requires in ver.get('requires_dist', []):
            depends_on_lines.append(depends_on_template.format(
                package=requires,
                version=ver['version']))

    ver0 = versions[0]

    spack_package = package_template.format(
        package = ver0['name'],
        description = '\n    '.join(ver0['description'].splitlines()),
        home_page = ver0['home_page'],
        versions = '\n'.join(version_lines),
        depends_ons = '\n'.join(depends_on_lines)
    )

    print(spack_package)


def dump_package(pypi, package):
    versions = get_versions(pypi, package)
    print(package)
    for ver in versions:
        print('  {0}'.format(ver['version']))
        for k,v in ver.items():
            print('    {0}: {1}'.format(k,v))

def main():
    pypi = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
#    write_package_list(pypi)
#    walk_pypi(pypi)
    convert_package(pypi, sys.argv[1])
#    dump_package(pypi, 'basemap')

main()
