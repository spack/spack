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

import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.reporter import Reporter
from spack.util.crypto import checksum
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


class CDash(Reporter):
    """Generate reports of spec installations for CDash."""

    def __init__(self, install_command, cdash_upload_url):
        Reporter.__init__(self, install_command, cdash_upload_url)
        self.template_dir = os.path.join('reports', 'cdash')
        self.hostname = socket.gethostname()
        self.osname = platform.system()
        self.starttime = int(time.time())
        # TODO: remove hardcoded use of Experimental here.
        #       Make the submission model configurable.
        self.buildstamp = time.strftime("%Y%m%d-%H%M-Experimental",
                                        time.localtime(self.starttime))

    def build_report(self, filename, report_data):
        self.initialize_report(filename, report_data)

        for phase in cdash_phases:
            report_data[phase] = {}
            report_data[phase]['log'] = ""
            report_data[phase]['status'] = 0
            report_data[phase]['starttime'] = self.starttime
            report_data[phase]['endtime'] = self.starttime

        # Track the phases we perform so we know what reports to create.
        phases_encountered = []

        # Parse output phase-by-phase.
        phase_regexp = re.compile(r"Executing phase: '(.*)'")
        for spec in report_data['specs']:
            for package in spec['packages']:
                if 'stdout' in package:
                    current_phase = ''
                    for line in package['stdout'].splitlines():
                        match = phase_regexp.search(line)
                        if match:
                            current_phase = match.group(1)
                            if current_phase not in map_phases_to_cdash:
                                current_phase = ''
                                continue
                            beginning_of_phase = True
                        else:
                            if beginning_of_phase:
                                cdash_phase = \
                                    map_phases_to_cdash[current_phase]
                                if cdash_phase not in phases_encountered:
                                    phases_encountered.append(cdash_phase)
                                report_data[cdash_phase]['log'] += \
                                    text_type("{0} output for {1}:\n".format(
                                        cdash_phase, package['name']))
                                beginning_of_phase = False
                            report_data[cdash_phase]['log'] += \
                                xml.sax.saxutils.escape(line) + "\n"

        for phase in phases_encountered:
            errors, warnings = parse_log_events(
                report_data[phase]['log'].splitlines())
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

            # Write the report.
            report_name = phase.capitalize() + ".xml"
            phase_report = os.path.join(filename, report_name)

            with codecs.open(phase_report, 'w', 'utf-8') as f:
                env = spack.tengine.make_environment()
                site_template = os.path.join(self.template_dir, 'Site.xml')
                t = env.get_template(site_template)
                f.write(t.render(report_data))

                phase_template = os.path.join(self.template_dir, report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))
            self.upload(phase_report)

    def concretization_report(self, filename, msg):
        report_data = {}
        self.initialize_report(filename, report_data)
        report_data['starttime'] = self.starttime
        report_data['endtime'] = self.starttime
        report_data['msg'] = msg

        env = spack.tengine.make_environment()
        update_template = os.path.join(self.template_dir, 'Update.xml')
        t = env.get_template(update_template)
        output_filename = os.path.join(filename, 'Update.xml')
        with open(output_filename, 'w') as f:
            f.write(t.render(report_data))
        self.upload(output_filename)

    def initialize_report(self, filename, report_data):
        if not os.path.exists(filename):
            os.mkdir(filename)
        report_data['install_command'] = self.install_command
        report_data['buildstamp'] = self.buildstamp
        report_data['hostname'] = self.hostname
        report_data['osname'] = self.osname

    def upload(self, filename):
        if not self.cdash_upload_url:
            return

        # Compute md5 checksum for the contents of this file.
        md5sum = checksum(hashlib.md5, filename, block_size=8192)

        opener = build_opener(HTTPHandler)
        with open(filename, 'rb') as f:
            url = "{0}&MD5={1}".format(self.cdash_upload_url, md5sum)
            request = Request(url, data=f)
            request.add_header('Content-Type', 'text/xml')
            request.add_header('Content-Length', os.path.getsize(filename))
            # By default, urllib2 only support GET and POST.
            # CDash needs expects this file to be uploaded via PUT.
            request.get_method = lambda: 'PUT'
            url = opener.open(request)
