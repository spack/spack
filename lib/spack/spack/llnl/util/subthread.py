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
import enum
import errno
import selectors
import signal
import socket
import threading
import time
import warnings
from contextlib import closing, contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, Type, TypeVar, Union

import spack.llnl.util.tty as tty

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import TracebackType

    from typing_extensions import Self


_Result = TypeVar("_Result")


@dataclass(frozen=True)
class _PollConfig:
    """A nonzero time to wait for between iterations of a ``SubthreadTask``."""

    period: float
    limit: Optional[float]

    def __post_init__(self) -> None:
        assert self.period > 0, self
        if self.limit is not None:
            assert self.limit >= self.period, self

    def _description(self) -> str:
        polling = f"polling output every {self.period!r} seconds"
        if self.limit is None:
            return f"{polling}, without limit"
        return f"{polling}, until {self.limit!r} seconds total"

    @classmethod
    def create(cls, *, poll_period: float, time_limit: Optional[float]) -> "Self":
        if not (isinstance(poll_period, float) and poll_period > 0):
            raise TypeError(f"poll period must be nonzero fractional seconds: {poll_period!r}")
        if time_limit is not None:
            assert isinstance(time_limit, float) and time_limit > 0, time_limit
            if poll_period > time_limit:
                tty.debug(f"clamping poll period {poll_period!r} to match limit {time_limit!r}")
                poll_period = time_limit

        ret = cls(period=poll_period, limit=time_limit)
        tty.debug(ret._description())
        return ret


class SubthreadTask(abc.ABC, Generic[_Result]):
    """Work to perform in a subthread."""

    @abc.abstractmethod
    def thread_name(self) -> str:
        """How to name the thread spawned to perform this work."""

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
    def __enter__(self) -> None:
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


class _ResultFlag(metaclass=abc.ABCMeta):
    """Handle to an asynchronous worker from the main thread."""

    @abc.abstractmethod
    def has_error(self) -> bool:
        """Whether the worker process has an error for the main thread to read."""

    @abc.abstractmethod
    def has_result(self) -> bool:
        """Whether the worker process has a successful result for the main thread to read!"""


class _CancellableResult(_ResultFlag, Generic[_Result]):
    """Worker handle with a type parameter which provides access to the result objects."""

    @abc.abstractmethod
    def send_cancel(self) -> None:
        """Interrupt any ongoing computations and set any asynchronous quit flags.

        This will not induce an "error" result, but instead return a best-effort result from the
        work performed.

        See `SubthreadTask.send_cancel()`.
        """

    @abc.abstractmethod
    def require_error(self) -> Exception:
        """Extract an error result.

        NB:
        - This method will only be called after `self.has_error()` has returned True.
        """

    @abc.abstractmethod
    def require_result(self) -> _Result:
        """Extract a success result.

        NB:
        - This method will only be called after `self.has_result()` has returned True.
        """


class _ThreadHandle(_CancellableResult[_Result]):
    """Worker handle that exposes a contextmanager interface to send results to the main thread."""

    @abc.abstractmethod
    def send_exit_without_feedback(self) -> None:
        """Exit asynchronously without blocking at all.

        This should call `self.send_cancel()`, but additionally set any extra flags to avoid
        writing to any pipes or checking any outputs, or calling any destructors.

        This method exists as an analogy to `SystemExit` for quick destruction, but avoids exiting
        the entire process to allow for library usage.
        """

    @abc.abstractmethod
    def __enter__(self) -> "Self":
        """Ensure the thread work has started."""

    @abc.abstractmethod
    def __exit__(
        self,
        exc_ty: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        _tb: Optional["TracebackType"],
    ) -> Optional[bool]:
        """Translate results from the main thread into the worker thread."""


class _TimeoutError(Exception):
    """Wrap an error produced from overrunning a polling time limit.

    This is used to wrap the result of `TaskSpawner.generate_timeout_error()`, so that the
    asynchronous worker process can manage the timeout logic. This is differentiated from
    unexpected errors from the background and/or main thread, since a timeout may generate
    a fallback or best-effort (but still successful) result.
    """

    def __init__(self, inner: Exception) -> None:
        super().__init__(f"timeout: {inner}")
        self.inner = inner


class _Subthread(threading.Thread, _ThreadHandle[_Result]):
    """Thread class to perform some very complex polling and cleanup logic.

    This thread should never be joined, but should instead use its `__enter__()`/`__exit__()`
    implementation to translate between calling and worker thread state changes.
    """

    def __init__(
        self,
        *,
        task: SubthreadTask[_Result],
        signal_write: socket.socket,
        success_write: socket.socket,
        stop_iteration_flag: threading.Event,
        poll: _PollConfig,
    ) -> None:
        threading.Thread.__init__(self, name=task.thread_name())
        self._task = task
        self._signal_write = signal_write
        self._success_write = success_write

        self._stop_iteration_flag = stop_iteration_flag
        self._exit_without_feedback: bool = False

        self._poll = poll

        self._error: Optional[Exception] = None
        self._result: Optional[_Result] = None

    def _send_error_signal(self) -> None:
        # This value isn't read, it's just a nonzero amount of bytes to trigger the read.
        try:
            self._signal_write.sendall(b"placeholder")
        except Exception:
            # Can't do anything here if our error channel is closed.
            pass

    @contextmanager
    def _handle_thread_error(self) -> "Iterator[None]":
        with self._task:
            try:
                yield
            except Exception as e:
                if self._exit_without_feedback:
                    pass
                elif isinstance(e, OSError) and e.errno == errno.EBADF:
                    # If the receiving end is closed, we want to exit immediately.
                    pass
                else:
                    self._error = e
                    self._send_error_signal()

    def _send_notification(self, msg: bytearray) -> None:
        assert b"\0" not in msg, msg
        msg += b"\0"
        self._success_write.sendall(msg)

    def _send_elapsed_notification(self, elapsed: float) -> None:
        msg = bytearray(b"elapsed:")
        # TODO: some loss of precision when stringifying numerics. Not worth worrying about.
        msg += f"{elapsed:_.5f}".encode("utf-8")
        self._send_notification(msg)

    def _send_timeout_notification(self) -> None:
        self._send_notification(bytearray(b"timeout"))

    def _send_finished_notification(self) -> None:
        self._send_notification(bytearray(b"finished"))

    def run(self) -> None:
        """Repeatedly poll the result of the worker task in a background thread context."""
        with self._handle_thread_error():
            start = time.monotonic()

            while not self._stop_iteration_flag.is_set():
                finished = self._task.poll_for(self._poll.period)
                if finished:
                    break
                elapsed = time.monotonic() - start
                self._send_elapsed_notification(elapsed)
                if self._poll.limit is None:
                    continue
                assert self._poll.limit is not None
                if elapsed > self._poll.limit:
                    self._send_timeout_notification()
                    break
            if not self._exit_without_feedback:
                self._result = self._task.block_on()
                self._send_finished_notification()

    def send_cancel(self) -> None:
        # (1) Ensure no more polling will occur.
        self._stop_iteration_flag.set()
        # (2) Interrupt any poll occurring at this very moment.
        self._task.send_cancel()

    def send_exit_without_feedback(self) -> None:
        # (3) Avoid sending any further success or error notifications.
        self._exit_without_feedback = True
        self.send_cancel()

    def has_error(self) -> bool:
        return self._error is not None

    def require_error(self) -> Exception:
        assert self._error is not None
        return self._error

    def has_result(self) -> bool:
        return self._result is not None

    def require_result(self) -> _Result:
        assert self._result is not None
        return self._result

    def __enter__(self) -> "Self":
        """Ensure the thread work has started."""
        self.start()
        return self

    def __exit__(
        self,
        exc_ty: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        _tb: Optional["TracebackType"],
    ) -> Optional[bool]:
        """Translate results from the main thread into the worker thread."""
        # (1) If we're returning without error, then this thread must already have completed with
        #     a success result!
        if exc_ty is None:
            return None
        # (2) If we're reporting a timeout error, that must have come after this thread essentially
        #     completed all of its work.
        #     We don't have any checks to bypass, so just unwrap the inner error from the
        #     main thread.
        if issubclass(exc_ty, _TimeoutError):
            assert isinstance(exc_val, _TimeoutError), exc_val
            raise exc_val.inner from exc_val
        # (3) Here, we're handling a non-timeout exception from the main thread (which typically
        #     means a KeyboardInterrupt). In this case, we want to immediately return control to
        #     the user and do not care whatsoever about the results from this worker thread.
        #
        #     Unfortunately, our worker thread has worked very hard to get where it is, and has
        #     laid a veritable obstacle course for us to jump through to avoid blocking further.
        #
        #     Typically, blocking such as SubthreadTask.__exit__() would occur off the
        #     main thread, and the cancellation from self.send_cancel() is still intended to gather
        #     the best-effort result, in the case of `config:concretizer:error_on_timeout: false`.
        #
        #     TODO: consider simpler ways to achieve the early-exit control flow in
        #           self._handle_thread_error().
        self.send_exit_without_feedback()
        # (4) The exception in the main thread continues to propagate up the call stack as this
        #     worker makes an asynchronous french exit.
        return False


class _MessageSplitter:
    """Statefully concatenate byte chunks and split across a separator byte.

    While socket buffering handles this by default, we want to precisely interleave any success or
    error results in `TaskSpawner.__call__()`. This allows reading any error results immediately
    (avoiding any user-visible delays) while maintaining sequential consistency of buffer contents
    in a multithreaded environment.
    """

    def __init__(self, *, separator: bytes) -> None:
        assert len(separator) == 1, separator
        self._separator = separator
        self._read_buf = bytearray()

    def process_data(self, data: bytes) -> "Iterator[str]":
        """Add the new chunk of data to the end, then split the result by separator.

        Any leftover data is retained to start off the next chunk.
        """
        last_null = data.rfind(self._separator)
        if last_null == -1:
            self._read_buf += data
            return

        first_null = data.find(self._separator)
        assert first_null >= 0, first_null
        assert first_null <= last_null, data
        self._read_buf += data[:first_null]

        yield self._read_buf.decode("utf-8")

        self._read_buf.clear()

        if first_null < last_null:
            for msg in data[first_null + 1 : last_null].split(self._separator):
                yield msg.decode()

        self._read_buf += data[last_null + 1 :]


@dataclass(frozen=True)
class TimeoutConfig:
    """How long to wait for a worker task and whether to accept a best-effort result."""

    time_limit: Optional[float]
    error_on_timeout: bool

    def __post_init__(self) -> None:
        if self.time_limit is not None:
            assert self.time_limit > 0, self

    @classmethod
    def create(cls, *, time_limit: Optional[Union[float, int]], error_on_timeout: bool) -> "Self":
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
        return cls(time_limit=time_limit, error_on_timeout=error_on_timeout)

    @classmethod
    def from_config(cls) -> "Self":
        import spack.config

        return cls(
            time_limit=float(spack.config.CONFIG.get("concretizer:timeout", 0)),
            error_on_timeout=bool(spack.config.CONFIG.get("concretizer:error_on_timeout", True)),
        )


class _MessageType(enum.Enum):
    """Kinds of messages which can be received asynchronously from a worker thread."""

    interrupt = enum.auto()
    error = enum.auto()
    elapsed = enum.auto()
    timeout = enum.auto()
    finished = enum.auto()


@dataclass(frozen=True)
class _TaskMessage:
    """Tagged union of message types from a worker thread."""

    kind: _MessageType
    payload: Optional[Union[_TimeoutError, float, str]]

    @classmethod
    def interrupt(cls) -> "Self":
        return cls(kind=_MessageType.interrupt, payload=None)

    @classmethod
    def error(cls) -> "Self":
        return cls(kind=_MessageType.error, payload=None)

    @classmethod
    def elapsed(cls, elapsed: float) -> "Self":
        return cls(kind=_MessageType.elapsed, payload=elapsed)

    @classmethod
    def timeout(cls, payload: Union[_TimeoutError, str]) -> "Self":
        return cls(kind=_MessageType.timeout, payload=payload)

    @classmethod
    def finished(cls) -> "Self":
        return cls(kind=_MessageType.finished, payload=None)


class TaskSpawner(abc.ABC, Generic[_Result]):
    """Unwieldy wrapper for spawning a background thread.

    This class's entry point is the synchronous `self.__call__()` method, which will trap SIGINT
    and periodically write a debug log for the total elapsed time. When the process completes, its
    destructor in :func:`SubthreadTask.__exit__()` will be invoked asynchronously as the
    main thread progresses with the in-memory result.
    """

    #: How long to wait in between printing debug logs.
    #:
    #: This must be a floating-point number > 0. If there is a finite timeout limit in
    #: `TimeoutConfig.time_limit`, this will be clamped to at most that limit (polling just once).
    #:
    #: This class uses :func:`signal.set_wakeup_fd()`, so this shouldn't affect the frequency of
    #: checking for `KeyboardInterrupt`.
    POLL_PERIOD: ClassVar[float] = 0.25
    #: How many bytes should be read from a non-blocking socket per message.
    #:
    #: This value must be an integer > 0.
    #:
    #: This precise value shouldn't really matter because socket messages are very small, and most
    #: data is instead sent in-memory with the GIL held.
    READ_LEN: ClassVar[int] = 1024

    def __init__(self, timeout: Optional[TimeoutConfig] = None) -> None:
        self._timeout = timeout or TimeoutConfig.from_config()

        self._was_interrupted: Optional[bool] = None
        self._signal_read: Optional[socket.socket] = None
        self._signal_write: Optional[socket.socket] = None
        self._success_read: Optional[socket.socket] = None
        self._success_write: Optional[socket.socket] = None

        assert (
            isinstance(self.__class__.READ_LEN, int) and self.__class__.READ_LEN > 0
        ), self.__class__

    @abc.abstractmethod
    def generate_timeout_error(self) -> Exception:
        """Hook method called to generate an error upon polling past the time limit.

        The return value of this method will be raised from within `self.__call__()`, which will
        result in calling the destructor from :func:`SubthreadTask.__exit__()`.
        """

    @abc.abstractmethod
    def generate_timeout_warning(self) -> str:
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

    @contextmanager
    def _sigint_handler(self) -> "Iterator[None]":
        """Generate a pair of sockets which are used to stagger ^C/SIGINT inputs.

        This approach is adapted from ``pdb.py`` in the CPython stdlib, and should work equally
        on Windows:
        https://github.com/python/cpython/blob/20d5494c88985beb925b557ec29937b05e54779c/Lib/pdb.py#L3171-L3211
        """
        assert self._was_interrupted is None, self._was_interrupted
        assert self._signal_read is None, self._signal_read
        assert self._signal_write is None, self._signal_write

        def handler(sig, frame):
            self._was_interrupted = True
            raise KeyboardInterrupt

        sentinel = object()
        old_handler: Any = sentinel
        old_wakeup_fd: Any = sentinel

        self._was_interrupted = False
        self._signal_read, self._signal_write = socket.socketpair()
        with closing(self._signal_read), closing(self._signal_write):
            self._signal_read.setblocking(False)
            self._signal_write.setblocking(False)
            try:
                old_handler = signal.signal(signal.SIGINT, handler)
                try:
                    old_wakeup_fd = signal.set_wakeup_fd(
                        self._signal_write.fileno(), warn_on_full_buffer=False
                    )
                    yield
                finally:
                    # Restore the old wakeup fd if we installed a new one.
                    if old_wakeup_fd is not sentinel:
                        signal.set_wakeup_fd(old_wakeup_fd)
            finally:
                self._signal_read = self._signal_write = None
                # Restore the old handler if we installed a new one.
                if old_handler is not sentinel:
                    signal.signal(signal.SIGINT, old_handler)

    @contextmanager
    def _success_outputs(self) -> "Iterator[None]":
        """Set up a pair of sockets used to write progress and result notifications."""
        assert self._success_read is None, self._success_read
        assert self._success_write is None, self._success_write

        self._success_read, self._success_write = socket.socketpair()
        with closing(self._success_read), closing(self._success_write):
            self._success_read.setblocking(False)
            self._success_write.setblocking(False)
            try:
                yield
            finally:
                self._success_read = self._success_write = None

    @contextmanager
    def _selector(self) -> "Iterator[selectors.DefaultSelector]":
        """Convert the two read sockets into a selector which serializes their chunks."""
        assert self._signal_read is not None
        assert self._success_read is not None

        # Wait for either a SIGINT or a result from the handle.
        selector = selectors.DefaultSelector()
        selector.register(self._signal_read, selectors.EVENT_READ)
        selector.register(self._success_read, selectors.EVENT_READ)

        with selector:
            yield selector

    @contextmanager
    def _thread(self, *args: Any, **kwargs: Any) -> "Iterator[_Subthread[_Result]]":
        """Create and enter the context which serializes calling and background thread events."""
        assert self._signal_write is not None
        assert self._success_write is not None

        with _Subthread(
            task=self.spawn_task(*args, **kwargs),
            signal_write=self._signal_write,
            success_write=self._success_write,
            stop_iteration_flag=threading.Event(),
            poll=_PollConfig.create(
                poll_period=self.__class__.POLL_PERIOD, time_limit=self._timeout.time_limit
            ),
        ) as thread:
            yield thread

    def _iter_messages(
        self, selector: selectors.DefaultSelector, flag: _ResultFlag
    ) -> "Iterator[_TaskMessage]":
        """Serialize the two input streams into discrete messages in the calling thread.

        Note that this stream of messages does not close any sockets or cancel background work.
        This means that (like pdb in the stdlib) exceptions can be caught and handled before
        allowing them to propagate to the :func:`_Subthread.__exit__()` omnibus handler.
        """
        assert self._was_interrupted is not None

        # Check for pending unhandled SIGINT.
        if self._was_interrupted:
            self._was_interrupted = False
            yield _TaskMessage.interrupt()

        # Wait for either a SIGINT or a result from the handle.
        read_buf = _MessageSplitter(separator=b"\0")
        while not flag.has_result():
            for key, _ in selector.select():
                if key.fileobj is self._signal_read:
                    # NB: Arbitrary nonzero amount.
                    self._signal_read.recv(self.__class__.READ_LEN)
                    # See if we've already processed this interrupt.
                    if self._was_interrupted:
                        self._was_interrupted = False
                        yield _TaskMessage.interrupt()
                    if flag.has_error():
                        yield _TaskMessage.error()
                else:
                    assert key.fileobj is self._success_read, key
                    data = self._success_read.recv(self.__class__.READ_LEN)
                    assert len(data) > 0
                    for msg in read_buf.process_data(data):
                        if msg == "finished":
                            yield _TaskMessage.finished()
                        elif msg == "timeout":
                            if self._timeout.error_on_timeout:
                                yield _TaskMessage.timeout(
                                    _TimeoutError(self.generate_timeout_error())
                                )
                            else:
                                yield _TaskMessage.timeout(self.generate_timeout_warning())
                        else:
                            # TODO: This loses precision because we use null bytes as a delimiter
                            #       over a real message encoding.
                            assert msg.startswith("elapsed:"), msg
                            elapsed = float(msg[len("elapsed:") :])
                            yield _TaskMessage.elapsed(elapsed)
        yield _TaskMessage.finished()

    def _process_messages(
        self, selector: selectors.DefaultSelector, flag: _CancellableResult[_Result]
    ) -> _Result:
        """Convert the stream of messages into logging, exceptions, and a return value."""
        for msg in self._iter_messages(selector, flag):
            if msg.kind == _MessageType.interrupt:
                assert msg.payload is None, msg
                tty.debug(f"interrupt: {msg}")
                raise KeyboardInterrupt
            elif msg.kind == _MessageType.error:
                assert msg.payload is None, msg
                tty.debug(f"err: {msg}")
                raise flag.require_error()
            elif msg.kind == _MessageType.elapsed:
                assert isinstance(msg.payload, float), msg
                tty.debug(f"elapsed time: {msg.payload}")
            elif msg.kind == _MessageType.timeout:
                assert isinstance(msg.payload, (_TimeoutError, str)), msg
                tty.debug(f"timeout: {msg}")
                flag.send_cancel()
                if isinstance(msg.payload, _TimeoutError):
                    raise msg.payload
                warnings.warn(msg.payload)
            else:
                assert msg.kind == _MessageType.finished, msg
                assert msg.payload is None, msg
                tty.debug(f"success: {msg}")
                return flag.require_result()
        raise AssertionError("should never get here")

    def __call__(self, *args: Any, **kwargs: Any) -> _Result:
        """Invoke the background process, then move it to a background thread.

        The background thread will do its best to delay any cleanup work until after returning
        a value to this method.
        """
        with self._sigint_handler(), self._success_outputs():
            with self._thread(*args, **kwargs) as thread:
                with self._selector() as selector:
                    tty.debug(f"waiting on subthread: {thread.name!r}")
                    return self._process_messages(selector, thread)
