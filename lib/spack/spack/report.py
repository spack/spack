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
import codecs
import collections
import functools
import time
import traceback

import llnl.util.lang
import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.reporter import Reporter
from spack.reporters.cdash import CDash
from spack.reporters.junit import JUnit

report_writers = {
    None: Reporter,
    'junit': JUnit,
    'cdash': CDash
}

#: Allowed report formats
valid_formats = list(report_writers.keys())

__all__ = [
    'valid_formats',
    'collect_info'
]


def fetch_package_log(pkg):
    try:
        with codecs.open(pkg.build_log_path, 'r', 'utf-8') as f:
            return ''.join(f.readlines())
    except Exception:
        return 'Cannot open build log for {0}'.format(
            pkg.spec.cshort_spec
        )


class InfoCollector(object):
    """Decorates PackageBase.do_install to collect information
    on the installation of certain specs.

    When exiting the context this change will be rolled-back.

    The data collected is available through the ``specs``
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
        self.input_specs = specs
        #: This is where we record the data that will be included
        #: in our report.
        self.specs = []

    def __enter__(self):
        # Initialize the spec report with the data that is available upfront.
        for input_spec in self.input_specs:
            name_fmt = '{0}_{1}'
            name = name_fmt.format(input_spec.name,
                                   input_spec.dag_hash(length=7))

            spec = {
                'name': name,
                'nerrors': None,
                'nfailures': None,
                'npackages': None,
                'time': None,
                'timestamp': time.strftime(
                    "%a, %d %b %Y %H:%M:%S", time.gmtime()
                ),
                'properties': [],
                'packages': []
            }

            self.specs.append(spec)

            Property = collections.namedtuple('Property', ['name', 'value'])
            spec['properties'].append(
                Property('architecture', input_spec.architecture)
            )
            spec['properties'].append(
                Property('compiler', input_spec.compiler))

            # Check which specs are already installed and mark them as skipped
            for dep in filter(lambda x: x.package.installed,
                              input_spec.traverse()):
                package = {
                    'name': dep.name,
                    'id': dep.dag_hash(),
                    'elapsed_time': '0.0',
                    'result': 'skipped',
                    'message': 'Spec already installed'
                }
                spec['packages'].append(package)

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

                package = {
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
                    package['result'] = 'success'
                    if installed_on_entry:
                        return

                except spack.build_environment.InstallError as e:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    package['result'] = 'failure'
                    package['stdout'] = fetch_package_log(pkg)
                    package['message'] = e.message or 'Installation failure'
                    package['exception'] = e.traceback

                except (Exception, BaseException) as e:
                    # Everything else is an error (the installation
                    # failed outside of the child process)
                    package['result'] = 'error'
                    package['stdout'] = fetch_package_log(pkg)
                    package['message'] = str(e) or 'Unknown error'
                    package['exception'] = traceback.format_exc()

                finally:
                    package['elapsed_time'] = time.time() - start_time

                # Append the package to the correct spec report. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # spec reports.
                for s in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = name_fmt.format(s.name, s.dag_hash(length=7))
                    try:
                        item = next((
                            x for x in self.specs
                            if x['name'] == name
                        ))
                        item['packages'].append(package)
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

        for spec in self.specs:
            spec['npackages'] = len(spec['packages'])
            spec['nfailures'] = len(
                [x for x in spec['packages'] if x['result'] == 'failure']
            )
            spec['nerrors'] = len(
                [x for x in spec['packages'] if x['result'] == 'error']
            )
            spec['time'] = sum([
                float(x['elapsed_time']) for x in spec['packages']
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
        format_name (str or None): one of the supported formats
        install_command (str): the command line passed to spack
        cdash_upload_url (str or None): where to upload the report

    Raises:
        ValueError: when ``format_name`` is not in ``valid_formats``
    """
    def __init__(self, format_name, install_command, cdash_upload_url):
        self.filename = None
        self.format_name = format_name
        # Check that the format is valid.
        if self.format_name not in valid_formats:
            raise ValueError('invalid report type: {0}'
                             .format(self.format_name))
        self.report_writer = report_writers[self.format_name](
            install_command, cdash_upload_url)

    def concretization_report(self, msg):
        self.report_writer.concretization_report(self.filename, msg)

    def __enter__(self):
        if self.format_name:
            # Start the collector and patch PackageBase.do_install
            self.collector = InfoCollector(self.specs)
            self.collector.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.format_name:
            # Close the collector and restore the
            # original PackageBase.do_install
            self.collector.__exit__(exc_type, exc_val, exc_tb)

            report_data = {'specs': self.collector.specs}
            self.report_writer.build_report(self.filename, report_data)
