# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
'''Log formatting for integration with dashboards'''

import codecs
import functools
import os
import platform
import spack
import time
import xml.dom.minidom
import calendar

from spack.build_environment import InstallError
from spack.fetch_strategy import FetchError
import llnl.util.filesystem as fs
import xml.etree.ElementTree as ET


# Needed for test cases
class TestResult(object):
    PASSED = 0
    FAILED = 1
    SKIPPED = 2
    ERRORED = 3


class JUnitTestSuite(object):
    def __init__(self, spec, logfile):
        self.spec = spec
        self.root = ET.Element('testsuite')
        self.tests = []
        if logfile is not None:
            self.logfile = logfile
        else:
            fmt = 'test-{x.name}-{x.version}-{hash}.xml'
            basename = fmt.format(x=spec, hash=spec.dag_hash())
            dirname = fs.join_path(spack.var_path, 'junit-report')
            fs.mkdirp(dirname)
            self.logfile = fs.join_path(dirname, basename)

    def create_testcase(self, name, spec):
        item = JUnitTestCase(name, spec)
        self.tests.append(item)
        return item

    def dump(self):
        # Prepare the header for the entire test suite
        number_of_errors = sum(
            x.result_type == TestResult.ERRORED for x in self.tests
        )
        self.root.set('errors', str(number_of_errors))
        number_of_failures = sum(
            x.result_type == TestResult.FAILED for x in self.tests
        )
        self.root.set('failures', str(number_of_failures))
        self.root.set('tests', str(len(self.tests)))
        self.root.set('name', str(self.spec))
        self.root.set('hostname', platform.node())

        for item in self.tests:
            self.root.append(item.element)

        with codecs.open(self.logfile, 'wb', 'utf-8') as file:
            xml_string = ET.tostring(self.root)
            xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            file.write(xml_string)


class JUnitTestCase(object):

    results = {
        TestResult.PASSED: None,
        TestResult.SKIPPED: 'skipped',
        TestResult.FAILED: 'failure',
        TestResult.ERRORED: 'error',
    }

    def __init__(self, classname, name):
        self.element = ET.Element('testcase')
        self.element.set('classname', str(classname))
        self.element.set('name', str(name))
        self.result_type = None

    def set_duration(self, duration):
        self.element.set('time', str(duration))

    def set_result(self, result_type,
                   message=None, error_type=None, text=None):
        self.result_type = result_type
        result = JUnitTestCase.results[self.result_type]
        if result is not None and result is not TestResult.PASSED:
            subelement = ET.SubElement(self.element, result)
            if error_type is not None:
                subelement.set('type', error_type)
            if message is not None:
                subelement.set('message', str(message))
            if text is not None:
                subelement.text = text


class CDashTestCase(object):

    results = {
        TestResult.PASSED: 'passed',
        TestResult.SKIPPED: 'notrun',
        TestResult.FAILED: 'failed',
        TestResult.ERRORED: 'failed',
    }

    def __init__(self, classname, name):
        self.name = name
        self.element = ET.Element('Test')
        name_element = ET.SubElement(self.element, 'Name')
        name_element.text = name

        #path_element = ET.SubElement(self.element, 'Path')
        #path_element.text = ""
        cmd_line_element = ET.SubElement(self.element, 'FullCommandLine')
        cmd_line_element.text = "spack install"
        self.result = ET.SubElement(self.element, 'Results')

    def set_duration(self, duration):
        execution_time = ET.SubElement(self.result, 'NamedMeasurement')
        execution_time.set('type', 'numeric/double')
        execution_time.set('name', 'Execution Time')
        value = ET.SubElement(execution_time, 'Value')
        value.text = str(duration)

    def set_result(self, result_type,
                   message=None, error_type=None, text=None):
        self.element.set('Status', CDashTestCase.results[result_type])
        # Completion Status
        completion_status = ET.SubElement(self.result, 'NamedMeasurement')
        completion_status.set('type', 'text/string')
        completion_status.set('name', 'Completion Status')
        value = ET.SubElement(completion_status, 'Value')
        value.text = 'Completed'
        # Command line
        cmd_line = ET.SubElement(self.result, 'NamedMeasurement')
        cmd_line.set('type', 'text/string')
        cmd_line.set('name', 'Command Line')
        value = ET.SubElement(cmd_line, 'Value')
        value.text = "spack install"
        # Logs
        if message is not None:
            logs = ET.SubElement(self.result, 'Measurement')
            value = ET.SubElement(logs, 'Value')
            value.text = message


class CDashSimpleTestSuite(object):
    def __init__(self, spec, filename, slot='Experimental'):
        self.spec = spec
        self.slot = slot
        self.tests = []
        self.buildstamp = "%s-%s" % (time.strftime("%Y%d%m-%H:%M:%S"), slot)
        self.filename = filename


    def create_filename(self, spec, subdir, step):
        if "build" in str(step):
            if self.filename is not None:
                return "%s.%s.xml" % (self.filename, step)
            else:
                fmt = '%s-{x.name}-{x.version}-{hash}.xml' % step
                basename = fmt.format(x=spec, hash=spec.dag_hash())
                dirname = fs.join_path(spack.var_path, subdir)
                fs.mkdirp(dirname)
                return fs.join_path(dirname, basename)

    def create_template(self):
        template = ET.Element('Site')
        buildName = str(self.spec.short_spec)
        buildName = buildName.split('=')
        template.set('BuildName',str(buildName[0]) + " " + str(buildName[1]))
        template.set('BuildStamp', self.buildstamp)
        template.set('CompilerName', str(self.spec.compiler.name)) 
        template.set('CompilerVersion', str(self.spec.compiler.version))
        if "linux" in platform.system().lower():
            linuxInfo = str(platform.linux_distribution()[0])+"."+str(platform.linux_distribution()[1])
            template.set('Hostname', linuxInfo)
            template.set('Name', linuxInfo)
            template.set('OSName', platform.system())
        elif "darwin" in platform.system().lower():
            macInfo = "OS X " + platform.mac_ver()[0]
            template.set('Hostname', macInfo)
            template.set('Name', macInfo)
            template.set('OSName', "Mac")
        else:
            template.set('Name', platform.node())
            template.set('Hostname', platform.node())
            template.set('OSName', platform.system())
        #template.set('Type', self.slot)
        return template

    def create_testcase(self, name, spec):
        item = CDashTestCase(name, spec)
        self.tests.append(item)
        return item

    def dump(self):
        build_report = self.prepare_build_report()
        filename = self.create_filename(self.spec, 'cdash', 'build')
        self.dump_report(build_report, filename)
        

    def dump_report(self, report, filename):
        with codecs.open(filename, 'wb', 'utf-8') as file:
            xml_string = ET.tostring(report)
            xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            file.write(xml_string)

    def now(self):
        #return time.strftime("%a %b %d %H:%M:%S %Z")
        return time.strftime("%b %d %H:%M %Z")

    def epoch(self):
        return str(calendar.timegm(time.gmtime()))


    def prepare_build_report(self):
        report = self.create_template()
        build = ET.SubElement(report, 'Build')
        start_element = ET.SubElement(build, 'StartDateTime')
        start_element.text = self.now()
        startBuild_element = ET.SubElement(build, 'StartBuildTime')
        startBuild_element.text = self.epoch()
        command_element = ET.SubElement(build, 'BuildCommand')
        command_element.text = 'spack install'
        log_element = ET.SubElement(build, 'Log')
        log_element.set('Encoding', 'base64')
        end_element = ET.SubElement(build, 'EndDateTime')
        end_element.text = self.now()
        endBuild_element = ET.SubElement(build, 'EndBuildTime')
        endBuild_element.text = self.epoch()
        ElapsedMinutes = ET.SubElement(build, 'ElapsedMinutes')
        ElapsedMinutes.text = '0' #fix this
        return report

def fetch_text(path):
    if not os.path.exists(path):
        return ''

    with codecs.open(path, 'rb', 'utf-8') as f:
        return '\n'.join(
            list(line.strip() for line in f.readlines())
        )


def dashboard_output(spec, test_suite):
    # Cycle once and for all on the dependencies and skip
    # the ones that are already installed. This ensures that
    # for the same spec, the same number of entries will be
    # displayed in the XML report
    for x in spec.traverse(order='post'):
        package = spack.repo.get(x)
        if package.installed:
            test_case = test_suite.create_testcase(package.name, x.short_spec)
            test_case.set_duration(0.0)
            test_case.set_result(
                TestResult.SKIPPED,
                message='Skipped [already installed]',
                error_type='already_installed'
            )

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, ** kwargs):

            # Check if the package has been installed already
            if self.installed:
                return

            test_case = test_suite.create_testcase(self.name,
                                                   self.spec.short_spec)
            # Try to install the package
            try:
                # If already installed set the spec as skipped
                start_time = time.time()
                # PackageBase.do_install
                func(self, *args, **kwargs)
                duration = time.time() - start_time
                test_case.set_duration(duration)
                test_case.set_result(TestResult.PASSED)
            except InstallError:
                # Check if the package relies on dependencies that
                # did not install
                duration = time.time() - start_time
                test_case.set_duration(duration)
                if [x for x in self.spec.dependencies(('link', 'run')) if not spack.repo.get(x).installed]:  # NOQA: ignore=E501
                    test_case.set_duration(0.0)
                    test_case.set_result(
                        TestResult.SKIPPED,
                        message='Skipped [failed dependencies]',
                        error_type='dep_failed'
                    )
                else:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    text = fetch_text(self.build_log_path)
                    test_case.set_result(
                        TestResult.FAILED,
                        message='Installation failure',
                        text=text
                    )
            except FetchError:
                # A FetchError is considered an error as
                # we didn't even start building
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unable to fetch package',
                    text=text
                )
            except Exception:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unexpected exception thrown during install',
                    text=text
                )
            except:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unknown error',
                    text=text
                )

        return wrapper
    return decorator


class CDashCompleteTestSuite(object):
    def __init__(self, spec, filename, slot='Experimental'):
        self.spec = spec
        self.slot = slot
        self.tests = []
        self.buildstamp = "%s-%s" % (time.strftime("%Y%d%m-%H:%M:%S"), slot)
        self.configure_report = self.prepare_configure_report_()
        self.filename = filename
        #tempcompiler = spec.short_spec.split('%')[1].split(' ')[0]
        #self.CompilerName = tempcompiler.split('@')[0]
        #self.CompilerVersion = tempcompiler.split('@')[1]
        

    def create_filename(self, spec, subdir, step):
        if self.filename is not None:
            return "%s.%s.xml" % (self.filename, step)
        else:
            fmt = '%s-{x.name}-{x.version}-{hash}.xml' % step
            basename = fmt.format(x=spec, hash=spec.dag_hash())
            dirname = fs.join_path(spack.var_path, subdir)
            fs.mkdirp(dirname)
            return fs.join_path(dirname, basename)

    def create_template(self):
        template = ET.Element('Site')
        buildName = str(self.spec.short_spec)
        buildName = buildName.split('=')
        template.set('BuildName',str(buildName[0]) + " " + str(buildName[1]))
        template.set('BuildStamp', self.buildstamp)
        template.set('CompilerName', str(self.spec.compiler.name)) 
        template.set('CompilerVersion', str(self.spec.compiler.version))
        if "linux" in platform.system().lower():
            linuxInfo = str(platform.linux_distribution()[0])+"."+str(platform.linux_distribution()[1])
            template.set('Hostname', linuxInfo)
            template.set('Name', linuxInfo)
            template.set('OSName', platform.system())
        elif "darwin" in platform.system().lower():
            macInfo = "OS X " + platform.mac_ver()[0]
            template.set('Hostname', macInfo)
            template.set('Name', macInfo)
            template.set('OSName', "Mac")
        else:
            template.set('Name', platform.node())
            template.set('Hostname', platform.node())
            template.set('OSName', platform.system())
        #template.set('Type', self.slot)
        return template

    def create_testcase(self, name, spec):
        item = CDashTestCase(name, spec)
        self.tests.append(item)
        return item

    def dump(self):
        filename = self.create_filename(self.spec, 'cdash', 'configure')
        self.dump_report(self.configure_report, filename)
        build_report = self.prepare_build_report()
        filename = self.create_filename(self.spec, 'cdash', 'build')
        self.dump_report(build_report, filename)
        test_report = self.prepare_test_report()
        filename = self.create_filename(self.spec, 'cdash', 'test')
        self.dump_report(test_report, filename)

    def dump_report(self, report, filename):
        with codecs.open(filename, 'wb', 'utf-8') as file:
            xml_string = ET.tostring(report)
            xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            file.write(xml_string)

    def now(self):
        #return time.strftime("%a %b %d %H:%M:%S %Z")
        return time.strftime("%b %d %H:%M %Z")

    def epoch(self):
        return str(calendar.timegm(time.gmtime()))

    def prepare_configure_report_(self):
        report = self.create_template()
        configure = ET.SubElement(report, 'Configure')
        start_time = ET.SubElement(configure, 'StartDateTime')
        start_time.text = self.now()
        startConfigure_element = ET.SubElement(configure, 'StartConfigureTime')
        startConfigure_element.text = self.epoch()
        command = ET.SubElement(configure, "ConfigureCommand")
        command.text = "spack install"
        log = ET.SubElement(configure, 'Log')
        log.text = str(self.spec)
        status = ET.SubElement(configure, "ConfigureStatus")
        status.text = '0'
        end_time = ET.SubElement(configure, 'EndDateTime')
        end_time.text = self.now()
        endConfigure_element = ET.SubElement(configure, 'EndConfigureTime')
        endConfigure_element.text = self.epoch()
        minutes = ET.SubElement(configure, "ElapsedMinutes")
        minutes.text = '0'#fix this
        return report

    def prepare_build_report(self):
        report = self.create_template()
        build = ET.SubElement(report, 'Build')
        start_element = ET.SubElement(build, 'StartDateTime')
        start_element.text = self.now()
        startBuild_element = ET.SubElement(build, 'StartBuildTime')
        startBuild_element.text = self.epoch()
        command_element = ET.SubElement(build, 'BuildCommand')
        command_element.text = 'spack install'
        log_element = ET.SubElement(build, 'Log')
        log_element.set('Encoding', 'base64')
        end_element = ET.SubElement(build, 'EndDateTime')
        end_element.text = self.now()
        endBuild_element = ET.SubElement(build, 'EndBuildTime')
        endBuild_element.text = self.epoch()
        ElapsedMinutes = ET.SubElement(build, 'ElapsedMinutes')
        ElapsedMinutes.text = '0' #fix this
        return report

    def prepare_test_report(self):
        report = self.create_template()
        testing = ET.SubElement(report, 'Testing')
        start_element = ET.SubElement(testing, 'StartDateTime')
        start_element.text = self.now()
        print type(self.now())
        startTest_element = ET.SubElement(testing, 'StartTestTime')
        startTest_element.text = self.epoch()
        testlist = ET.SubElement(testing, 'TestList')
        for item in self.tests:
            test_element = ET.SubElement(testlist, "Test")
            test_element.text = item.name
            testing.append(item.element)
        end_element = ET.SubElement(testing, 'EndDateTime')
        end_element.text = self.now()
        endTest_element = ET.SubElement(testing, 'EndTestime')
        endTest_element.text = self.epoch()
        ElapsedMinutes = ET.SubElement(testing, 'ElapsedMinutes')
        ElapsedMinutes.text = '0' #fix this
        return report

def fetch_text(path):
    if not os.path.exists(path):
        return ''

    with codecs.open(path, 'rb', 'utf-8') as f:
        return '\n'.join(
            list(line.strip() for line in f.readlines())
        )

def dashboard_output(spec, test_suite):
    # Cycle once and for all on the dependencies and skip
    # the ones that are already installed. This ensures that
    # for the same spec, the same number of entries will be
    # displayed in the XML report
    for x in spec.traverse(order='post'):
        package = spack.repo.get(x)
        if package.installed:
            test_case = test_suite.create_testcase(package.name, x.short_spec)
            test_case.set_duration(0.0)
            test_case.set_result(
                TestResult.SKIPPED,
                message='Skipped [already installed]',
                error_type='already_installed'
            )

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, ** kwargs):

            # Check if the package has been installed already
            if self.installed:
                return

            test_case = test_suite.create_testcase(self.name,
                                                   self.spec.short_spec)
            # Try to install the package
            try:
                # If already installed set the spec as skipped
                start_time = time.time()
                # PackageBase.do_install
                func(self, *args, **kwargs)
                duration = time.time() - start_time
                test_case.set_duration(duration)
                test_case.set_result(TestResult.PASSED)
            except InstallError:
                # Check if the package relies on dependencies that
                # did not install
                duration = time.time() - start_time
                test_case.set_duration(duration)
                if [x for x in self.spec.dependencies(('link', 'run')) if not spack.repo.get(x).installed]:  # NOQA: ignore=E501
                    test_case.set_duration(0.0)
                    test_case.set_result(
                        TestResult.SKIPPED,
                        message='Skipped [failed dependencies]',
                        error_type='dep_failed'
                    )
                else:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    text = fetch_text(self.build_log_path)
                    test_case.set_result(
                        TestResult.FAILED,
                        message='Installation failure',
                        text=text
                    )
            except FetchError:
                # A FetchError is considered an error as
                # we didn't even start building
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unable to fetch package',
                    text=text
                )
            except Exception:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unexpected exception thrown during install',
                    text=text
                )
            except:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unknown error',
                    text=text
                )

        return wrapper
    return decorator


# announce the existing test suites
test_suites = {"junit": JUnitTestSuite,
               "cdash-simple": CDashSimpleTestSuite,
               "cdash-complete": CDashCompleteTestSuite,}
