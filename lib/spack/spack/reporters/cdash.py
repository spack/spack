# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import codecs
import hashlib
import os.path
import platform
import re
import socket
import time
import xml.sax.saxutils
from six import text_type
from six.moves.urllib.request import build_opener, HTTPHandler, Request
from six.moves.urllib.parse import urlencode

from llnl.util.filesystem import working_dir
import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.reporter import Reporter
from spack.util.crypto import checksum
from spack.util.executable import which
from spack.util.log_parse import parse_log_events

__all__ = ['CDash']

# Mapping Spack phases to the corresponding CTest/CDash phase.
map_phases_to_cdash = {
    'autoreconf': 'configure',
    'cmake':      'configure',
    'configure':  'configure',
    'edit':       'configure',
    'build':      'build',
    'install':    'build'
}

# Initialize data structures common to each phase's report.
cdash_phases = set(map_phases_to_cdash.values())
cdash_phases.add('update')


class CDash(Reporter):
    """Generate reports of spec installations for CDash.

    To use this reporter, pass the ``--cdash-upload-url`` argument to
    ``spack install``::

        spack install --cdash-upload-url=\\
            https://mydomain.com/cdash/submit.php?project=Spack <spec>

    In this example, results will be uploaded to the *Spack* project on the
    CDash instance hosted at https://mydomain.com/cdash.
    """

    def __init__(self, args):
        Reporter.__init__(self, args)
        self.template_dir = os.path.join('reports', 'cdash')
        self.cdash_upload_url = args.cdash_upload_url
        if args.package:
            packages = args.package
        else:
            packages = []
            for file in args.specfiles:
                with open(file, 'r') as f:
                    s = spack.spec.Spec.from_yaml(f)
                    packages.append(s.format())
        self.install_command = ' '.join(packages)
        self.buildname = args.cdash_build or self.install_command
        self.site = args.cdash_site or socket.gethostname()
        self.osname = platform.system()
        self.endtime = int(time.time())
        buildstamp_format = "%Y%m%d-%H%M-{0}".format(args.cdash_track)
        self.buildstamp = time.strftime(buildstamp_format,
                                        time.localtime(self.endtime))
        self.buildId = None
        self.revision = ''
        git = which('git')
        with working_dir(spack.paths.spack_root):
            self.revision = git('rev-parse', 'HEAD', output=str).strip()

    def build_report(self, filename, report_data):
        self.initialize_report(filename, report_data)

        for phase in cdash_phases:
            report_data[phase] = {}
            report_data[phase]['loglines'] = []
            report_data[phase]['status'] = 0
            report_data[phase]['endtime'] = self.endtime

        # Track the phases we perform so we know what reports to create.
        phases_encountered = []
        total_duration = 0

        # Parse output phase-by-phase.
        phase_regexp = re.compile(r"Executing phase: '(.*)'")
        cdash_phase = ''
        for spec in report_data['specs']:
            if 'time' in spec:
                total_duration += int(spec['time'])
            for package in spec['packages']:
                if 'stdout' in package:
                    current_phase = ''
                    cdash_phase = ''
                    for line in package['stdout'].splitlines():
                        match = None
                        if line.find("Executing phase: '") != -1:
                            match = phase_regexp.search(line)
                        if match:
                            current_phase = match.group(1)
                            if current_phase not in map_phases_to_cdash:
                                current_phase = ''
                                continue
                            cdash_phase = \
                                map_phases_to_cdash[current_phase]
                            if cdash_phase not in phases_encountered:
                                phases_encountered.append(cdash_phase)
                            report_data[cdash_phase]['loglines'].append(
                                text_type("{0} output for {1}:".format(
                                    cdash_phase, package['name'])))
                        elif cdash_phase:
                            report_data[cdash_phase]['loglines'].append(
                                xml.sax.saxutils.escape(line))

        phases_encountered.append('update')

        # Move the build phase to the front of the list if it occurred.
        # This supports older versions of CDash that expect this phase
        # to be reported before all others.
        if "build" in phases_encountered:
            build_pos = phases_encountered.index("build")
            phases_encountered.insert(0, phases_encountered.pop(build_pos))

        self.starttime = self.endtime - total_duration
        for phase in phases_encountered:
            report_data[phase]['starttime'] = self.starttime
            report_data[phase]['log'] = \
                '\n'.join(report_data[phase]['loglines'])
            errors, warnings = parse_log_events(report_data[phase]['loglines'])
            nerrors = len(errors)

            if phase == 'configure' and nerrors > 0:
                report_data[phase]['status'] = 1

            if phase == 'build':
                # Convert log output from ASCII to Unicode and escape for XML.
                def clean_log_event(event):
                    event = vars(event)
                    event['text'] = xml.sax.saxutils.escape(event['text'])
                    event['pre_context'] = xml.sax.saxutils.escape(
                        '\n'.join(event['pre_context']))
                    event['post_context'] = xml.sax.saxutils.escape(
                        '\n'.join(event['post_context']))
                    # source_file and source_line_no are either strings or
                    # the tuple (None,).  Distinguish between these two cases.
                    if event['source_file'][0] is None:
                        event['source_file'] = ''
                        event['source_line_no'] = ''
                    else:
                        event['source_file'] = xml.sax.saxutils.escape(
                            event['source_file'])
                    return event

                report_data[phase]['errors'] = []
                report_data[phase]['warnings'] = []
                for error in errors:
                    report_data[phase]['errors'].append(clean_log_event(error))
                for warning in warnings:
                    report_data[phase]['warnings'].append(
                        clean_log_event(warning))

            if phase == 'update':
                report_data[phase]['revision'] = self.revision

            # Write the report.
            report_name = phase.capitalize() + ".xml"
            phase_report = os.path.join(filename, report_name)

            with codecs.open(phase_report, 'w', 'utf-8') as f:
                env = spack.tengine.make_environment()
                if phase != 'update':
                    # Update.xml stores site information differently
                    # than the rest of the CTest XML files.
                    site_template = os.path.join(self.template_dir, 'Site.xml')
                    t = env.get_template(site_template)
                    f.write(t.render(report_data))

                phase_template = os.path.join(self.template_dir, report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))
            self.upload(phase_report)
        self.print_cdash_link()

    def concretization_report(self, filename, msg):
        report_data = {}
        self.initialize_report(filename, report_data)
        report_data['update'] = {}
        report_data['update']['starttime'] = self.endtime
        report_data['update']['endtime'] = self.endtime
        report_data['update']['revision'] = self.revision
        report_data['update']['log'] = msg

        env = spack.tengine.make_environment()
        update_template = os.path.join(self.template_dir, 'Update.xml')
        t = env.get_template(update_template)
        output_filename = os.path.join(filename, 'Update.xml')
        with open(output_filename, 'w') as f:
            f.write(t.render(report_data))
        self.upload(output_filename)
        self.print_cdash_link()

    def initialize_report(self, filename, report_data):
        if not os.path.exists(filename):
            os.mkdir(filename)
        report_data['buildname'] = self.buildname
        report_data['buildstamp'] = self.buildstamp
        report_data['install_command'] = self.install_command
        report_data['osname'] = self.osname
        report_data['site'] = self.site

    def upload(self, filename):
        if not self.cdash_upload_url:
            return

        # Compute md5 checksum for the contents of this file.
        md5sum = checksum(hashlib.md5, filename, block_size=8192)

        buildid_regexp = re.compile("<buildId>([0-9]+)</buildId>")
        opener = build_opener(HTTPHandler)
        with open(filename, 'rb') as f:
            params_dict = {
                'build': self.buildname,
                'site': self.site,
                'stamp': self.buildstamp,
                'MD5': md5sum,
            }
            encoded_params = urlencode(params_dict)
            url = "{0}&{1}".format(self.cdash_upload_url, encoded_params)
            request = Request(url, data=f)
            request.add_header('Content-Type', 'text/xml')
            request.add_header('Content-Length', os.path.getsize(filename))
            # By default, urllib2 only support GET and POST.
            # CDash needs expects this file to be uploaded via PUT.
            request.get_method = lambda: 'PUT'
            response = opener.open(request)
            if not self.buildId:
                match = buildid_regexp.search(response.read())
                if match:
                    self.buildId = match.group(1)

    def print_cdash_link(self):
        if self.buildId:
            # Construct and display a helpful link if CDash responded with
            # a buildId.
            build_url = self.cdash_upload_url
            build_url = build_url[0:build_url.find("submit.php")]
            build_url += "buildSummary.php?buildid={0}".format(self.buildId)
            print("View your build results here:\n  {0}\n".format(build_url))
