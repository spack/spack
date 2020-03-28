# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Manages the details on the images used in the build and the run stage."""
import json
import os.path

#: Global variable used to cache in memory the content of images.json
_data = None


def data():
    """Returns a dictionary with the static data on the images.

    The dictionary is read from a JSON file lazily the first time
    this function is called.
    """
    global _data
    if not _data:
        json_dir = os.path.abspath(os.path.dirname(__file__))
        json_file = os.path.join(json_dir, 'images.json')
        with open(json_file) as f:
            _data = json.load(f)
    return _data


def build_info(image, spack_version):
    """Returns the name of the build image and its tag.

    Args:
        image (str): image to be used at run-time. Should be of the form
            <image_name>:<image_tag> e.g. "ubuntu:18.04"
        spack_version (str): version of Spack that we want to use to build

    Returns:
        A tuple with (image_name, image_tag) for the build image
    """
    # Don't handle error here, as a wrong image should have been
    # caught by the JSON schema
    image_data = data()[image]
    build_image = image_data['build']

    # Try to check if we have a tag for this Spack version
    try:
        build_tag = image_data['build_tags'][spack_version]
    except KeyError:
        msg = ('the image "{0}" has no tag for Spack version "{1}" '
               '[valid versions are {2}]')
        msg = msg.format(build_image, spack_version,
                         ', '.join(image_data['build_tags'].keys()))
        raise ValueError(msg)

    return build_image, build_tag


def package_info(image):
    """Returns the commands used to update system repositories, install
    system packages and clean afterwards.

    Args:
        image (str): image to be used at run-time. Should be of the form
            <image_name>:<image_tag> e.g. "ubuntu:18.04"

    Returns:
        A tuple of (update, install, clean) commands.
    """
    image_data = data()[image]
    update = image_data['update']
    install = image_data['install']
    clean = image_data['clean']
    return update, install, clean
