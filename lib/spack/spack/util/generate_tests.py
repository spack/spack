import spack
import os
import spack.architecture as sarch
import spack.util.spack_yaml as yaml
# import llnl.util.tty as tty

from random import randint
from spack.spec import ArchSpec


description = "Generates a test files{days, all, xsdk}"


class GenerateTests(object):

    def __init__(self, use_system_compilers,
                 seperate_by_compiler, specific_test_type, latest_pkgs):
        self.latest_pkgs = latest_pkgs
        if use_system_compilers:
            arch = ArchSpec(str(sarch.platform()),
                            'default_os', 'default_target')
            self.compilers = [
                c.spec for c in spack.compilers.compilers_for_arch(arch)]
        else:
            # self.compilers = ['gcc@4.4.7', 'gcc@4.7', 'gcc@4.8.5',
            #                  'gcc@4.8', 'gcc@4.9.3', 'gcc@5.4.0',
            #                  'clang@3.4.2', 'clang@3.8',  'clang@3.7',
            #                  'clang@3.6', 'clang@3.5']"""
            # reduced set
            self.compilers = ['gcc@4.4.7', 'gcc@4.8.5',
                              'gcc@4.9.3', 'gcc@5.4.0',
                              'clang@3.4.2', 'clang@3.8.0-2ubuntu4']
        self.xsdk = ['xsdk', 'xsdktrilinos', 'trilinos', 'superlu-mt',
                     'superlu-dist', 'petsc', 'superlu', 'hypre', 'alquimia']

        self.cdash = "https://spack.io/cdash"
        self.seperate_by_compiler = seperate_by_compiler
        methods = {'all-tests': self.generate_all_tests,
                   'xsdk': self.generate_xsdk,
                   'days': self.generate_days}
        if specific_test_type in methods:
            methods[specific_test_type]()
        else:
            raise Exception("Method %s not implemented" % specific_test_type)

    def seperate_compilers(self, complr_list):
        rtn_dict = {'compilers': {}}
        for cmplr in complr_list:
            cmplr = str(cmplr)
            cmplr_name = cmplr.split('@')[0]
            cmplr_version = cmplr.split('@')[1]
            if cmplr_name not in rtn_dict['compilers'].keys():
                rtn_dict['compilers'][cmplr_name] = {'versions': []}
            rtn_dict['compilers'][cmplr_name]['versions'].append(cmplr_version)
        return rtn_dict

    def file_output(self, pkgs, compilers):
        file_dict = {}
        file_dict["test-suite"] = {}
        file_dict["test-suite"]["include"] = pkgs
        file_dict[
            "test-suite"]["matrix"] = self.generate_packages(pkgs, compilers)
        file_dict["test-suite"]["cdash"] = [self.cdash]
        return file_dict

    def write_file(self, path, pkgs, compilers):
        with open(path, 'w') as f:
            yaml.dump(self.file_output(pkgs, compilers), f,
                      default_flow_style=False)

    def generate_all_tests(self):
        self.generate_days()
        self.generate_all()
        self.generate_xsdk()

    def generate_packages(self,  pkg_list, compilers):
        pkgs = {}
        rm_list = []
        num_pkgs = len(pkg_list)
        for sub_pkg in pkg_list:
            # Fill in the entries one by one
            pkg_details = spack.repo.get(sub_pkg)
            version_list = []
            sorted_by_version = sorted(pkg_details.versions, reverse=True)
            if self.latest_pkgs:
                try:
                    if 'develop' in str(sorted_by_version[0]):
                        version_list.append(str(sorted_by_version[1]))
                    else:
                        version_list.append(str(sorted_by_version[0]))
                except IndexError as err:
                    continue
            else:
                for version in sorted(pkg_details.versions, reverse=True):
                    version_list.append(str(version))
            pkgs[sub_pkg] = {'versions': version_list}
        for rm_pkg in rm_list:
            tmp_pkg_list.remove(rm_pkg)
        num_pkgs = num_pkgs - len(rm_list)
        pkg_cmplrs = [{"packages": pkgs},
                      self.seperate_compilers(compilers)]
        return pkg_cmplrs

    def generate_days(self):
        # days 1-7
        all_pkgs = spack.repo.all_package_names()
        for day in range(1, 8):
            tmp_pkg_list = list(all_pkgs)
            num_pkgs = len(tmp_pkg_list)
            if self.seperate_by_compiler:
                for compiler in self.compilers:
                    path = os.path.join(os.getcwd(), "day" +
                                        str(day) + "_" +
                                        str(compiler).replace('@', '') +
                                        ".yaml")
                    rm_list = []
                    day_list = []
                    for x in range(num_pkgs / 7):
                        item = tmp_pkg_list[randint(0, num_pkgs - 1)]
                        while item in rm_list:
                            item = tmp_pkg_list[randint(0, num_pkgs - 1)]
                        rm_list.append(item)
                        day_list.append(item)
                        self.write_file(path, day_list, [str(compiler)])
            else:
                rm_list = []
                day_list = []
                for x in range(num_pkgs / 7):
                    item = tmp_pkg_list[randint(0, num_pkgs - 1)]
                    while item in rm_list:
                        item = tmp_pkg_list[randint(0, num_pkgs - 1)]
                    rm_list.append(item)
                    day_list.append(item)
                    path = os.path.join(os.getcwd(), "day" +
                                        str(day) + ".yaml")
                    self.write_file(path, day_list, self.compilers)

    def generate_all(self):
        all_pkgs = list(spack.repo.all_package_names())
        if self.seperate_by_compiler:
            for compiler in self.compilers:
                path = os.path.join(os.getcwd(), "all_" +
                                    str(compiler).replace('@', '') + ".yaml")
                self.write_file(path, all_pkgs, [str(compiler)])
        else:
            path = os.path.join(os.getcwd(), "all.yaml")
            self.write_file(path, all_pkgs, self.compilers)

    def generate_xsdk(self):
        if self.seperate_by_compiler:
            for compiler in self.compilers:
                path = os.path.join(os.getcwd(), "xsdk_" +
                                    str(compiler).replace('@', '') + ".yaml")
                self.write_file(path, self.xsdk, [str(compiler)])
        else:
            path = os.path.join(os.getcwd(), "xsdk.yaml")
            self.write_file(path, self.xsdk, self.compilers)
