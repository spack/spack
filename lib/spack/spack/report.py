##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Tools to produce reports of spec installations"""
import collections
import functools
import itertools
import os.path
import time
import traceback

import llnl.util.lang
import spack.build_environment
import spack.fetch_strategy
import spack.package

templates = {
    'junit': os.path.join('reports', 'junit.xml')
}

#: Allowed report formats
valid_formats = list(templates.keys())

__all__ = [
    'valid_formats',
    'collect_info'
]


def fetch_package_log(pkg):
    try:
        with open(pkg.build_log_path, 'r') as f:
            return ''.join(f.readlines())
    except Exception:
        return 'Cannot open build log for {0}'.format(
            pkg.spec.cshort_spec
        )


class InfoCollector(object):
    """Decorates PackageBase.do_install to collect information
    on the installation of certain specs.

    When exiting the context this change will be rolled-back.

    The data collected is available through the ``test_suites``
    attribute once exited, and it's organized as a list where
    each item represents the installation of one of the spec.

    Args:
        specs (list of Spec): specs whose install information will
           be recorded
    """
    #: Backup of PackageBase.do_install
    _backup_do_install = spack.package.PackageBase.do_install

    def __init__(self, specs):
        #: Specs that will be installed
        self.specs = specs
        #: Context that will be used to stamp the report from
        #: the template file
        self.test_suites = []

    def __enter__(self):
        # Initialize the test suites with the data that
        # is available upfront
        for spec in self.specs:
            name_fmt = '{0}_{1}'
            name = name_fmt.format(spec.name, spec.dag_hash(length=7))

            suite = {
                'name': name,
                'nerrors': None,
                'nfailures': None,
                'ntests': None,
                'time': None,
                'timestamp': time.strftime(
                    "%a, %d %b %Y %H:%M:%S", time.gmtime()
                ),
                'properties': [],
                'testcases': []
            }

            self.test_suites.append(suite)

            Property = collections.namedtuple('Property', ['name', 'value'])
            suite['properties'].append(
                Property('architecture', spec.architecture)
            )
            suite['properties'].append(Property('compiler', spec.compiler))

            # Check which specs are already installed and mark them as skipped
            for dep in filter(lambda x: x.package.installed, spec.traverse()):
                test_case = {
                    'name': dep.name,
                    'id': dep.dag_hash(),
                    'elapsed_time': '0.0',
                    'result': 'skipped',
                    'message': 'Spec already installed'
                }
                suite['testcases'].append(test_case)

        def gather_info(do_install):
            """Decorates do_install to gather useful information for
            a CI report.

            It's defined here to capture the environment and build
            this context as the installations proceed.
            """
            @functools.wraps(do_install)
            def wrapper(pkg, *args, **kwargs):

                # We accounted before for what is already installed
                installed_on_entry = pkg.installed

                test_case = {
                    'name': pkg.name,
                    'id': pkg.spec.dag_hash(),
                    'elapsed_time': None,
                    'result': None,
                    'message': None
                }

                start_time = time.time()
                value = None
                try:

                    value = do_install(pkg, *args, **kwargs)
                    test_case['result'] = 'success'
                    if installed_on_entry:
                        return

                except spack.build_environment.InstallError as e:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    test_case['result'] = 'failure'
                    test_case['stdout'] = fetch_package_log(pkg)
                    test_case['message'] = e.message or 'Installation failure'
                    test_case['exception'] = e.traceback

                except (Exception, BaseException) as e:
                    # Everything else is an error (the installation
                    # failed outside of the child process)
                    test_case['result'] = 'error'
                    test_case['stdout'] = fetch_package_log(pkg)
                    test_case['message'] = str(e) or 'Unknown error'
                    test_case['exception'] = traceback.format_exc()

                finally:
                    test_case['elapsed_time'] = time.time() - start_time

                # Append the case to the correct test suites. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # test suites.
                for s in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = name_fmt.format(s.name, s.dag_hash(length=7))
                    try:
                        item = next((
                            x for x in self.test_suites
                            if x['name'] == name
                        ))
                        item['testcases'].append(test_case)
                    except StopIteration:
                        pass

                return value

            return wrapper

        spack.package.PackageBase.do_install = gather_info(
            spack.package.PackageBase.do_install
        )

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Restore the original method in PackageBase
        spack.package.PackageBase.do_install = InfoCollector._backup_do_install

        for suite in self.test_suites:
            suite['ntests'] = len(suite['testcases'])
            suite['nfailures'] = len(
                [x for x in suite['testcases'] if x['result'] == 'failure']
            )
            suite['nerrors'] = len(
                [x for x in suite['testcases'] if x['result'] == 'error']
            )
            suite['time'] = sum([
                float(x['elapsed_time']) for x in suite['testcases']
            ])


class collect_info(object):
    """Collects information to build a report while installing
    and dumps it on exit.

    If the format name is not ``None``, this context manager
    decorates PackageBase.do_install when entering the context
    and unrolls the change when exiting.

    Within the context, only the specs that are passed to it
    on initialization will be recorded for the report. Data from
    other specs will be discarded.

    Examples:

        .. code-block:: python

            # The file 'junit.xml' is written when exiting
            # the context
            specs = [Spec('hdf5').concretized()]
            with collect_info(specs, 'junit', 'junit.xml'):
                # A report will be generated for these specs...
                for spec in specs:
                    spec.do_install()
                # ...but not for this one
                Spec('zlib').concretized().do_install()

    Args:
        specs (list of Spec): specs to be installed
        format_name (str or None): one of the supported formats
        filename (str or None): name of the file where the report wil
            be eventually written

    Raises:
        ValueError: when ``format_name`` is not in ``valid_formats``
    """
    def __init__(self, specs, format_name, filename):
        self.specs = specs
        self.format_name = format_name

        # Check that the format is valid
        if format_name not in itertools.chain(valid_formats, [None]):
            raise ValueError('invalid report type: {0}'.format(format_name))

        self.filename = filename
        self.collector = InfoCollector(specs) if self.format_name else None

    def __enter__(self):
        if self.format_name:
            # Start the collector and patch PackageBase.do_install
            self.collector.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.format_name:
            # Close the collector and restore the
            # original PackageBase.do_install
            self.collector.__exit__(exc_type, exc_val, exc_tb)

            # Write the report
            with open(self.filename, 'w') as f:
                env = spack.tengine.make_environment()
                t = env.get_template(templates[self.format_name])
                f.write(t.render({'test_suites': self.collector.test_suites}))
