# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.timer as timer


class Tick:
    def __init__(self):
        self.time = 0.0

    def tick(self):
        self.time += 1
        return self.time


def test_timer():
    # Every call to now is +1 second.
    t = timer.Timer(now=Tick().tick)

    # tick 1
    t.start()
    t.start("wrapped")

    # tick 3-4
    t.start("first")
    t.stop("first")
    assert t.duration("first") == 1.0

    # tick 5-6
    t.start("second")
    t.stop("second")
    assert t.duration("second") == 1.0

    # tick 2-7
    t.stop("wrapped")
    assert t.duration("wrapped") == 5.0

    # tick 8-11
    t.start("not-stopped")
    assert t.duration("not-stopped") == 1.0
    assert t.duration("not-stopped") == 2.0
    assert t.duration("not-stopped") == 3.0

    # tick 1-12
    assert t.duration() == 11.0
    t.stop()
