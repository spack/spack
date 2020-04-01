# From https://gist.github.com/evansd/2375136
#
# The MIT License (MIT)
#
# Copyright (c) 2013 David Evans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import signal
import six


class defer_signals(object):
    """
    Context manager to defer signal handling until context exits.

    Takes optional list of signals to defer (default: SIGHUP, SIGINT, SIGTERM).
    Signals can be identified by number or by name.

    Allows you to wrap instruction sequences that ought to be atomic and ensure
    that they don't get interrupted mid-way.
    """

    def __init__(self, signal_list=None):
        # Default list of signals to defer
        if signal_list is None:
            signal_list = [signal.SIGHUP, signal.SIGINT, signal.SIGTERM]
        # Accept either signal numbers or string identifiers
        self.signal_list = [
            getattr(signal, sig_id) if isinstance(sig_id, six.string_types) else sig_id
            for sig_id in signal_list
        ]
        self.deferred = []
        self.previous_handlers = {}

    def defer_signal(self, sig_num, stack_frame):
        self.deferred.append(sig_num)

    def __enter__(self):
        # Replace existing handlers with deferred handler
        for sig_num in self.signal_list:
            # signal.signal returns None when no handler has been set in Python,
            # which is the same as the default handler (SIG_DFL) being set
            self.previous_handlers[sig_num] = (
                signal.signal(sig_num, self.defer_signal) or signal.SIG_DFL)
        return self

    def __exit__(self, *args):
        # Restore handlers
        for sig_num, handler in self.previous_handlers.items():
            signal.signal(sig_num, handler)
        # Send deferred signals
        while self.deferred:
            sig_num = self.deferred.pop(0)
            os.kill(os.getpid(), sig_num)

    def __call__(self):
        """
        If there are any deferred signals pending, trigger them now

        This means that instead of this code:

            for item in collection:
                with defer_signals():
                    item.process()

        You can write this:

            with defer_signals() as handle_signals:
                for item in collection:
                    item.process()
                    handle_signals()

        Which has the same effect but avoids having to embed the context
        manager in the loop
        """
        if self.deferred:
            # Reattach the signal handlers and fire signals
            self.__exit__()
            # Put our deferred signal handlers back in place
            self.__enter__()
