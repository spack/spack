# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Aggregate the target processor, the operating system and the target
platform into an architecture object.

On a multiple architecture machine, the architecture spec field can be set to
build a package against any target and operating system that is present on the
platform. On Cray platforms or any other architecture that has different front
and back end environments, the operating system will determine the method of
compiler detection.

There are two different types of compiler detection:

    1. Through the $PATH env variable (front-end detection)
    2. Through the module system. (back-end detection)

Depending on which operating system is specified, the compiler will be detected
using one of those methods.

For platforms such as linux and darwin, the operating system is autodetected.

The command line syntax for specifying an architecture is as follows:

    target=<Target name> os=<OperatingSystem name>

If the user wishes to use the defaults, either target or os can be left out of
the command line and Spack will concretize using the default. These defaults
are set in the 'platforms/' directory which contains the different subclasses
for platforms. If the machine has multiple architectures, the user can
also enter frontend, or fe or backend or be. These settings will concretize
to their respective frontend and backend targets and operating systems.

Platforms are an abstract class that are extended by subclasses. If the user
wants to add a new type of platform (such as cray_xe), they can create a
subclass and set all the class attributes such as priority, front_target,
back_target, front_os, back_os. Platforms also contain a priority class
attribute. A lower number signifies higher priority. These numbers are
arbitrarily set and can be changed though often there isn't much need unless a
new platform is added and the user wants that to be detected first.

Targets are created inside the platform subclasses. Most architecture
(like linux, and darwin) will have only one target family (x86_64) but in the case of
Cray machines, there is both a frontend and backend processor. The user can
specify which targets are present on front-end and back-end architecture

Depending on the platform, operating systems are either autodetected or are
set. The user can set the frontend and backend operating setting by the class
attributes front_os and back_os. The operating system as described earlier,
will be responsible for compiler detection.
"""
