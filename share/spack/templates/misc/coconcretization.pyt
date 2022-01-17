# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Concretizationroot(Package):
    url = 'fake_url'

    version('1.0')

{% for dep in specs %}
    depends_on('{{ dep }}')
{% endfor %}

