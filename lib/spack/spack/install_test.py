# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import llnl.util.filesystem as fs
import spack.util.prefix

def get_test_stage_dir():
    return spack.util.path.canonicalize_path(
        spack.config.get('config:test_stage', '~/.spack/test'))

def get_test_stage(name):
    return spack.util.prefix.Prefix(os.path.join(get_test_stage_dir(), name))

def get_results_file(name):
    return get_test_stage(name).join('results.txt')

def get_test_by_name(name):
    test_suite_dir = os.path.join(get_test_stage_dir(), name)
    if not os.path.isdir(test_suite_dir):
        raise Exception



class TestSuite(object):
    def __init__(self, name, specs):
        self.name = name
        # copy so that different test suites have different package objects
        # even if they contain the same spec
        self.specs = [spec.copy() for spec in specs]
        self.current_test_spec = None

    def __call__(self, *args, **kwargs):
        remove_directory = kwargs.get('remove_directory', True)
        dirty = kwargs.get('dirty', False)
        fail_first = kwargs.get('fail_first', False)

        for spec in self.specs:
            try:
                msg = "A package object cannot run in two test suites at once"
                assert not spec.package.test_suite, msg
                spec.package.test_suite = self
                spec.package.do_test(
                    name=self.name,
                    remove_directory=remove_directory,
                    dirty=dirty
                )
                self.write_test_result(spec, 'PASSED')
            except BaseException as exc:
                if isinstance(exc, SyntaxError):
                    # Create the test log file and report the error.
                    self.ensure_stage()
                    msg = 'Testing package {0}\n{1}'\
                        .format(self.test_pkg_id(spec), str(err))
                    _add_msg_to_file(self.log_file_for_spec(spec), msg)

                self.write_test_result(spec, 'FAILED')
                if fail_first:
                    break
            finally:
                spec.package.test_suite = None
                self.current_test_spec = None

    def ensure_stage(self):
        if not os.path.exists(self.stage):
            fs.mkdirp(self.stage)

    @property
    def stage(self):
        return get_test_stage(self.name)

    @property
    def results_file(self):
        return get_results_file(self.name)

    @classmethod
    def test_pkg_id(cls, spec):
        """Build the standard install test package identifier

        Args:
        spec (Spec): instance of the spec under test

        Returns:
        (str): the install test package identifier
        """
        return spec.format('{name}-{version}-{hash:7}')

    @classmethod
    def test_log_name(cls, spec):
        return '%s-test-out.txt' % cls.test_pkg_id(spec)

    def log_file_for_spec(self, spec):
        return self.stage.join(self.test_log_name(spec))

    def test_dir_for_spec(self, spec):
        return self.stage.join(self.test_pkg_id(spec))

    @property
    def current_test_data_dir(self):
        assert self.current_test_spec
        spec = self.current_test_spec
        return self.test_dir_for_spec(spec).data.join(spec.name)

    def write_test_result(self, spec, result):
        msg = "{0} {1}".format(self.test_pkg_id(spec), result)
        _add_msg_to_file(self.results_file, msg)


def _add_msg_to_file(filename, msg):
    """Add the message to the specified file

    Args:
        filename (str): path to the file
        msg (str): message to be appended to the file
    """
    with open(filename, 'a+') as f:
        f.write('{0}\n'.format(msg))
