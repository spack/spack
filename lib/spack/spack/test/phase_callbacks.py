# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.phase_callbacks as pc


def test_phase_callbacks_basic():
    """Test that PhaseCallbacksMeta correctly aggregates and flushes callbacks."""
    # Ensure temporary lists are initially empty
    assert len(pc._RUN_BEFORE.callbacks) == 0
    assert len(pc._RUN_AFTER.callbacks) == 0

    class BaseBuilder(metaclass=pc.PhaseCallbacksMeta):
        @pc.run_before("install")
        def before_install_base(self):
            pass

        @pc.run_after("install", when="@1.0")
        def after_install_base(self):
            pass

    # Metaclass should have populated the attributes and flushed the temporary lists
    assert len(pc._RUN_BEFORE.callbacks) == 0
    assert len(pc._RUN_AFTER.callbacks) == 0

    assert hasattr(BaseBuilder, "_run_before_callbacks")
    assert hasattr(BaseBuilder, "_run_after_callbacks")

    before_cbs = BaseBuilder._run_before_callbacks
    after_cbs = BaseBuilder._run_after_callbacks

    assert len(before_cbs) == 1
    assert before_cbs[0][0] == ("install", None)
    assert before_cbs[0][1].__name__ == "before_install_base"

    assert len(after_cbs) == 1
    assert after_cbs[0][0] == ("install", "@1.0")
    assert after_cbs[0][1].__name__ == "after_install_base"


def test_phase_callbacks_inheritance():
    """Test that phase callbacks are correctly inherited and derived precedes base."""

    class BaseBuilder(metaclass=pc.PhaseCallbacksMeta):
        @pc.run_before("build")
        def base_build(self):
            pass

    class DerivedBuilder(BaseBuilder):
        @pc.run_before("build")
        def derived_build(self):
            pass

        @pc.run_before("install")
        def derived_install(self):
            pass

    cbs = DerivedBuilder._run_before_callbacks
    assert len(cbs) == 3

    # Derived class callbacks precede base class callbacks
    assert cbs[0][1].__name__ == "derived_build"
    assert cbs[1][1].__name__ == "derived_install"
    assert cbs[2][1].__name__ == "base_build"

    # Base callbacks remain untouched
    base_cbs = BaseBuilder._run_before_callbacks
    assert len(base_cbs) == 1
    assert base_cbs[0][1].__name__ == "base_build"


def test_phase_callbacks_adapter_skip():
    """Test that the metaclass skips processing for the old-style Adapter class."""

    class Base(metaclass=pc.PhaseCallbacksMeta):
        @pc.run_after("configure")
        def some_callback(self):
            pass

    # Normally, Adapter is skipped and temporary lists are NOT flushed by the metaclass.
    # We must manually flush to avoid leaking state into other tests.
    class Adapter(Base):
        @pc.run_after("build")
        def adapter_build(self):
            pass

    # Because it is skipped, it just inherits Base._run_after_callbacks exactly,
    # and the new adapter_build callback remains stuck in the global _RUN_AFTER list.
    assert Adapter._run_after_callbacks == Base._run_after_callbacks
    assert any(fn.__name__ == "adapter_build" for _, fn in pc._RUN_AFTER.callbacks)

    # Cleanup leaked callbacks since Adapter skips flushing
    pc._RUN_AFTER.callbacks.clear()
