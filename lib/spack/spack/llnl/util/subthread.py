# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This file's main purpose is to portably and robustly handle `^C` to cancel a pyclingo background
thread without needing to bootstrap any additional native code or require special Python features.

Background workers will need to subclass :class:`SubthreadTask` and :class:`TaskSpawner`, both of
which can be given a single generic type parameter for the single successful result output type:

.. code-block:: python

   class MyTask(SubthreadTask[T]):
       ...

   class MySpawner(TaskSpawner[T]):
       def __init__(self, specs, control) -> None:
           super().__init__()
           self._specs = specs
           self._control = control

       def spawn_task(self, *args, **kwargs) -> MyTask[T]:
           return MyTask(self._control.solve(*args, **kwargs))

   spawner = MySpawner(specs)
   timer.start("solve")
   solve_result = spawner(**solve_kwargs)
   timer.stop("solve")

This file should work on windows, macOS, and Linux without relying on any platform-specific tricks.
It extends the approach used for pdb in CPython to serialize foreground SIGINTs and background
polling into a coherent and robust stream of messages.

Alternatives:
- The more bombastic SystemExit requires far less tact, but cannot be used for multiple
  solves within the same process lifetime, such as with `spack python` scripts.
- An IPC protocol could be developed for all of the in-memory modifications afforded by
  the pyclingo API, but unlike spack.llnl.util.tty.{log,pty}, we are not attempting to
  redirect stdio streams or otherwise proxying the output of a subprocess.
  - Note that the current approach could be readily modified to support multiple parallel solves by
    muxing the SIGINT handler.
- We could modify upstream pyclingo to capture SIGINT/^C and raise a custom exception to
  avoid polling by hand, but then we'd be stuck to that upstream polling strategy for all
  the platforms we want to support.
- We could write a custom Python native module, but then we'd force our users to bootstrap
  a special Python version just to get basic functionality like interrupting a solve.

TODO: See if free threading in CPython 3.15 introduces any improved performance or parallelism!
"""

import abc
import asyncio
import concurrent.futures
import enum
import time
import warnings
from collections.abc import AsyncIterator
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    ClassVar,
    Generic,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import spack.vendor.attrs as attrs

import spack.llnl.util.tty as tty

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self


_Result = TypeVar("_Result")


@attrs.frozen(slots=True, kw_only=True, auto_attribs=True, init=True)
class TimeoutConfig:
    """How long to wait for a worker task and whether to accept a best-effort result."""

    time_limit: Optional[float]
    error_on_timeout: bool
    poll_period: float

    def __attrs_post_init__(self) -> None:
        assert self.poll_period > 0, self
        if self.time_limit is not None:
            assert self.time_limit > 0, self
            assert self.poll_period <= self.time_limit
        if self.error_on_timeout:
            assert self.time_limit is not None

    def _description(self) -> str:
        msg = f"polling output every {self.poll_period!r} seconds"
        if self.time_limit is None:
            msg += ", without limit"
        else:
            msg += f", until {self.time_limit!r} seconds total"
        if self.error_on_timeout:
            msg += ", or raising a timeout error"
        else:
            msg += ", then returning the best result"
        return msg

    #: How long to wait in between printing debug logs.
    #:
    #: This must be a floating-point number > 0. If there is a finite timeout limit in
    #: `TimeoutConfig.time_limit`, this will be clamped to at most that limit (polling just once).
    POLL_PERIOD: ClassVar[float] = 0.25

    @classmethod
    def create(
        cls,
        *,
        time_limit: Optional[Union[float, int]],
        error_on_timeout: bool,
        poll_period: float | None = None,
    ) -> "Self":
        """Coerce arguments (e.g. from config) and raise :class:`TypeError` for invalid values."""
        if time_limit == 0:
            tty.debug("converting 0 wait to -1")
            time_limit = -1
        if time_limit == -1:
            tty.debug("waiting indefinitely (-1)")
            time_limit = None
        if isinstance(time_limit, int):
            time_limit = float(time_limit)
        if not (time_limit is None or time_limit > 0):
            raise TypeError(f"time limit must be nonzero fractional seconds: {time_limit!r}")

        if poll_period is None:
            poll_period = cls.POLL_PERIOD
        if not (isinstance(poll_period, float) and poll_period > 0):
            raise TypeError(f"poll period must be nonzero fractional seconds: {poll_period!r}")
        if time_limit is not None:
            assert isinstance(time_limit, float) and time_limit > 0, time_limit
            if poll_period > time_limit:
                tty.debug(f"clamping poll period {poll_period!r} to match limit {time_limit!r}")
                poll_period = time_limit

        if error_on_timeout and time_limit is None:
            raise TypeError(
                f"time_limit {time_limit!r} must be nonzero fractional seconds "
                f"if error_on_timeout {error_on_timeout!r} is set"
            )

        # mypy doesn't like attrs for some reason.
        ret = cls(  # type: ignore[call-arg]
            time_limit=time_limit, error_on_timeout=error_on_timeout, poll_period=poll_period
        )
        tty.debug(ret._description())
        return ret


@attrs.define(slots=True, auto_attribs=True)
class _TaskGeneratorProgressMessage:
    """A message sent from the coroutine for every regular poll of the background task."""
    elapsed: float

    def __attr_post_init__(self) -> None:
        assert self.elapsed >= 0, self

    @classmethod
    def elapsed_time(cls, elapsed: float) -> "Self":
        # mypy doesn't like attrs.
        return cls(elapsed)  # type: ignore[call-arg]

    def __str__(self) -> str:
        return f"<elapsed: {self.elapsed:_.3f} seconds>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(elapsed={self.elapsed!r})"


class Timeout(Exception):
    """Wrap an error produced from overrunning a polling time limit."""

    def __init__(self, elapsed: float, limit: float) -> None:
        assert elapsed > limit and limit > 0, (elapsed, limit)
        super().__init__(f"timed out with {elapsed} seconds (> {limit} seconds)")
        self.elapsed = elapsed
        self.limit = limit


class _TaskGeneratorResultType(enum.Enum):
    """Tags for the single output result of a background task."""
    error = enum.auto()
    success = enum.auto()
    timeout = enum.auto()


@attrs.frozen(slots=True, kw_only=True, auto_attribs=True, init=True)
class _TaskGeneratorResultMessage(Generic[_Result]):
    """Classification of all possible end states of the background task."""
    kind: _TaskGeneratorResultType
    payload: Optional[Union[BaseException, _Result, "Timeout", Tuple["Timeout", _Result]]]

    @classmethod
    def error(cls, error: BaseException) -> "Self":
        return cls(kind=_TaskGeneratorResultType.error, payload=error)  # type: ignore[call-arg]

    @classmethod
    def success(cls, result: _Result) -> "Self":
        return cls(kind=_TaskGeneratorResultType.success, payload=result)  # type: ignore[call-arg]

    @classmethod
    def timeout_best_effort(cls, result: Tuple["Timeout", _Result]) -> "Self":
        return cls(kind=_TaskGeneratorResultType.timeout, payload=result)  # type: ignore[call-arg]

    @classmethod
    def timeout_failed(cls, error: "Timeout") -> "Self":
        return cls(kind=_TaskGeneratorResultType.timeout, payload=error)  # type: ignore[call-arg]


_Out = TypeVar("_Out", covariant=True)


class _BlockingThunk(Protocol[_Out]):
    @abc.abstractmethod
    def __call__(self, *args: Any) -> _Out: ...


@attrs.define(slots=True, auto_attribs=True, init=True)
class ThreadExecutor:
    """Wrapper for a thread-pool executor.

    This kind of executor is necessary to block on pyclingo's computation within the same process
    as spack, but they don't make it easy.
    """

    exe: concurrent.futures.ThreadPoolExecutor

    @classmethod
    def create(cls, **kwargs: Any) -> "Self":
        return cls(  # type: ignore[call-arg]
            concurrent.futures.ThreadPoolExecutor(
                thread_name_prefix="subthread-executor", **kwargs
            )
        )

    def run_blocking(
        self, loop: asyncio.AbstractEventLoop, thunk: _BlockingThunk[_Result], *args: Any
    ) -> asyncio.Future[_Result]:
        return loop.run_in_executor(self.exe, thunk, *args)


@attrs.define(slots=True, auto_attribs=True)
class Looper:
    """Wrapper for an asyncio event loop."""

    loop: asyncio.AbstractEventLoop

    @classmethod
    def create(cls, *, debug: bool = False) -> "Self":
        loop = asyncio.new_event_loop()
        if debug:
            tty.debug("set new asyncio loop to debug mode")
            loop.set_debug(True)
        return cls(loop)  # type: ignore[call-arg]


@attrs.define(slots=True, auto_attribs=True)
class EventLoop:
    """Class to orchestrate thread pools and event loops.

    These two have to work together pretty closely to integrate blocking operations into the async
    model, so this class decouples their interactions together from the act of allocating them.
    """

    exe: ThreadExecutor
    looper: Looper

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        return self.looper.loop

    def _poll_single(self, task: "SubthreadTask[_Result]", poll_period: float) -> Awaitable[bool]:
        return self.exe.run_blocking(self._get_loop(), task.poll_for, poll_period)

    async def _poll_long_running_blocking(
        self, start: float, task: "SubthreadTask[_Result]", poll_period: float
    ) -> AsyncIterator[_TaskGeneratorProgressMessage]:
        assert poll_period > 0, poll_period

        yield _TaskGeneratorProgressMessage.elapsed_time(0.0)

        while not await self._poll_single(task, poll_period):
            elapsed = time.monotonic() - start
            yield _TaskGeneratorProgressMessage.elapsed_time(elapsed)

    async def _handle_progress_updates(
        self, task: "SubthreadTask[_Result]", timeout: TimeoutConfig
    ) -> _TaskGeneratorResultMessage[_Result]:
        start = time.monotonic()

        try:
            async for msg in self._poll_long_running_blocking(start, task, timeout.poll_period):
                tty.debug(str(msg))
                if timeout.time_limit is not None:
                    if msg.elapsed > timeout.time_limit:
                        raise Timeout(msg.elapsed, timeout.time_limit)
            return _TaskGeneratorResultMessage.success(task.block_on())
        except Timeout as e:
            if timeout.error_on_timeout:
                return _TaskGeneratorResultMessage.timeout_failed(e)
            task.send_cancel()
            return _TaskGeneratorResultMessage.timeout_best_effort((e, task.block_on()))
        except BaseException as e:
            return _TaskGeneratorResultMessage.error(e)
        finally:
            task.send_cancel()

        raise AssertionError("should never get here")

    async def _subthread_top_level(
        self, spawner: "TaskSpawner[_Result]", *args: Any, **kwargs: Any
    ) -> _Result:
        with spawner.spawn_task(*args, **kwargs) as task:
            msg = await self._handle_progress_updates(task, spawner.timeout)
            if msg.kind == _TaskGeneratorResultType.success:
                return cast(_Result, msg.payload)
            if msg.kind == _TaskGeneratorResultType.error:
                assert isinstance(msg.payload, BaseException), msg
                raise msg.payload from msg.payload
            assert msg.kind == _TaskGeneratorResultType.timeout
            if isinstance(msg.payload, Timeout):
                # This was a failed timeout, with no best-effort result.
                exc = spawner.generate_timeout_error(msg.payload)
                raise exc from exc
            # This was a best-effort timeout, with a success result.
            assert isinstance(msg.payload, tuple), msg
            timeout, result = msg.payload
            warn_msg = spawner.generate_timeout_warning(timeout)
            warnings.warn(warn_msg)
            return cast(_Result, result)

    def execute_subthread_task(
        self, spawner: "TaskSpawner[_Result]", *args: Any, **kwargs: Any
    ) -> _Result:
        """Start the coroutine from `spawner` in a new task, then wait for the result."""
        coro = self._subthread_top_level(spawner, *args, **kwargs)
        return self._get_loop().run_until_complete(coro)


class SubthreadTask(abc.ABC, Generic[_Result]):
    """Work to perform in a subthread."""

    @abc.abstractmethod
    def poll_for(self, poll_period: float) -> bool:
        """Wait for maximum `poll_period` seconds, returning whether the computation is complete.

        NB:
        - `poll_period` will always be > 0.
        - This method will be strictly performed within a background/worker thread.
        """

    @abc.abstractmethod
    def block_on(self) -> _Result:
        """Return the result of the computation, possibly by blocking.

        NB:
        - This method will only be called after `self.poll_for()` has returned True.
        - This method will be strictly performed within a background/worker thread.
        """

    @abc.abstractmethod
    def send_cancel(self) -> None:
        """Interrupt any ongoing computations and set any asynchronous quit flags.

        NB:
        - Unlike other methods, this will be called from the main thread and therefore must be
          thread-safe.
        - This method should also be idempotent.
        """

    @abc.abstractmethod
    def __enter__(self) -> "Self":
        """Allocate any memory or begin any computation.

        NB:
        - This method will be strictly performed within a background/worker thread.
        """

    @abc.abstractmethod
    def __exit__(
        self,
        exc_ty: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        _tb: Optional["TracebackType"],
    ) -> Optional[bool]:
        """Call any destructors or other cleanup.

        NB:
        - This method will be strictly performed within a background/worker thread.
        """


class TaskSpawner(abc.ABC, Generic[_Result]):
    """Unwieldy wrapper for spawning a background thread.

    This class's entry point is the synchronous `self.__call__()` method, which will trap SIGINT
    and periodically write a debug log for the total elapsed time. When the process completes, its
    destructor in :func:`SubthreadTask.__exit__()` will be invoked asynchronously as the
    main thread progresses with the in-memory result.
    """

    def __init__(self, timeout: TimeoutConfig) -> None:
        self.timeout = timeout

    @abc.abstractmethod
    def generate_timeout_error(self, timeout_result: Timeout) -> Exception:
        """Hook method called to generate an error upon polling past the time limit.

        The return value of this method will be raised from within `self.__call__()`, which will
        result in calling the destructor from :func:`SubthreadTask.__exit__()`.
        """

    @abc.abstractmethod
    def generate_timeout_warning(self, timeout_result: Timeout) -> str:
        """Hook method called to generate a warning message upon polling past the time limit.

        This will result in calling :func:`SubthreadTask.block_on()` in a background thread to
        generate a best-effort success result.
        """

    @abc.abstractmethod
    def spawn_task(self, *args: Any, **kwargs) -> SubthreadTask[_Result]:
        """Kick off a task in the calling thread.

        This handle will subsequently be moved into a background thread, which will generate
        a stream of progress messages which will be propagated into debug-level logs from the
        calling thread.
        """

    def __call__(self, loop: EventLoop, *args: Any, **kwargs: Any) -> _Result:
        """Invoke the background process within an event loop."""
        return loop.execute_subthread_task(self, *args, **kwargs)
