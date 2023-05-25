# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse

import llnl.util.tty as tty

import spack.paths
import spack.util.windows_registry as wr


class FlagAppendAction(argparse.Action):
    def __init__(
        self,
        option_strings,
        dest,
        const=None,
        default=None,
        required=False,
        help=None,
        metavar=None,
    ):
        super(FlagAppendAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            const=const,
            nargs=0,
            default=default,
            required=required,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string):
        flag_lst = getattr(namespace, self.dest)
        if not flag_lst:
            setattr(namespace, self.dest, [option_string])
        else:
            flag_lst.append(option_string)


description = "check facets of Windows system configuration relevant to Spack"
section = "basic"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "-lp",
        "--long-path",
        action=FlagAppendAction,
        dest="checks",
        help="Perform system check for Long Path support",
    )
    subparser.add_argument(
        "-dm",
        "--developer-mode",
        action=FlagAppendAction,
        dest="checks",
        help="Perform system check for DeveloperMode activation",
    )
    subparser.add_argument(
        "-i",
        "--install-prefix-length",
        action=FlagAppendAction,
        dest="checks",
        help="Perform check for a long install prefix",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="Perform all system checks, takes precedence over provided flags",
    )
    subparser.add_argument(
        "--require",
        action="store_true",
        default=False,
        dest="req",
        required=False,
        help="Require that the specified checks pass. If not the command will exit failure",
    )
    subparser.add_argument(
        "--require-only",
        action="store_true",
        default=False,
        dest="req_only",
        required=False,
        help="""Require that specified checks pass. If not, the command will exit failure,
with no output to stdout""",
    )


def _get_reg_val_from_key(key, val, root):
    regpath = wr.WindowsRegistryView(key, root_key=root)
    return regpath.get_value(val).value


def long_path_check():
    long_path_support = _get_reg_val_from_key(
        "SYSTEM\\CurrentControlSet\\Control\\FileSystem",
        "LongPathsEnabled",
        wr.HKEY.HKEY_LOCAL_MACHINE,
    )
    health = True
    if long_path_support == 1:
        long_path_support = "Enabled"
    else:
        long_path_support = """Disabled ...
        Windows requires LongPathSupport to allow applications to handle paths greater than 260 characters in total.
        It is recommended to enable support while using Spack.
        This can be accomplished by following the instructions at:
        https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#enable-long-paths-in-windows-10-version-1607-and-later"""
        health = False
    msg = f"Long Path Support: {long_path_support}"
    return msg, health


def developer_mode_check():
    dev_mode = _get_reg_val_from_key(
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppModelUnlock",
        "AllowDevelopmentWithoutDevLicense",
        wr.HKEY.HKEY_LOCAL_MACHINE,
    )
    health = True
    if dev_mode == 1:
        dev_mode_support_string = "Enabled"
    else:
        dev_mode_support_string = """Disabled ...
        Spack requires developer mode for some basic functions.
        Developer mode can be turned on by following these instructions:
        https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development"""
        health = False
    msg = f"Developer Mode: {dev_mode_support_string}"
    return msg, health


def install_prefix_length_check():
    opt_dir = spack.paths.opt_path
    opt_char_count = len(opt_dir)
    health = True
    if opt_char_count > 260:
        excess_chars = opt_char_count - 260
        status_msg = f"""Install prefix: Danger
    Install prefix exceeds max path length by {excess_chars} characters.
    You must enable long path support to use this path
    and even then some Windows features/tools may not work"""
        health = False
    elif abs(opt_char_count - 260) < 100:
        # 100 characters is chosen here as Spack adds about 80 to the install prefix
        # not including any files the packages themselves may install, so that seems
        # like a good margin to warn on
        margin_char_count = 260 - opt_char_count
        status_msg = f"""Install prefix: Warning
    Install prefix is within {margin_char_count} of max path length.
    You may encounter issues without long path support
    and even then some Windows features/tools may not work"""
    else:
        status_msg = f"Install prefix: Healthy\n\t\tInstall prefix length is {opt_char_count}"
    return status_msg, health


check_map = {
    "-lp": long_path_check,
    "--long_path": long_path_check,
    "-dm": developer_mode_check,
    "--developer-mode": developer_mode_check,
    "-i": install_prefix_length_check,
    "--install-prefix-length": install_prefix_length_check,
}


def win_system_check(parser, args, unknown_args):
    system_status_report = """
Windows System Status Check:
****************************
"""

    if (not args.checks and not args.all) or args.all:
        long_path_report, lp_status = long_path_check()
        dev_mode_report, dm_status = developer_mode_check()
        ip_report, ip_status = install_prefix_length_check()
        for report in (long_path_report, dev_mode_report, ip_report):
            system_status_report += report + "\n"
        status = lp_status and dm_status and ip_status
    else:
        status = True
        for check in args.checks:
            report, check_status = check_map[check]()
            system_status_report += report + "\n"
            status = status and check_status
    system_status_report += "****************************"
    if not args.req_only:
        tty.info(system_status_report)
    if (args.req or args.req_only) and not status:
        tty.die("Windows system configuration is invalid for Spack useage")