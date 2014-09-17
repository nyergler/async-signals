from celery import task
from django.dispatch.dispatcher import (
    _make_id,
    Signal,
)


class AsyncSignal(Signal):

    def __init__(self, providing_args=None, queue=None):

        super(AsyncSignal, self).__init__(providing_args=providing_args)
        self.queue = queue

    def send(self, sender, **named):
        """Send the signal via Celery."""

        self.propagate_signal.apply_async(
            args=(sender),
            kwargs=named,
            queue=self.queue,
        )

    @task
    def propagate_signal(self, sender, **named):
        """
        Send signal from sender to all connected receivers catching errors.

        Arguments:

            sender The sender of the signal. Can be any python object
                (normally one registered with a connect if you
                actually want something to occur).

            named
                Named arguments which will be passed to receivers. These
                arguments must be a subset of the argument names defined in
                providing_args.

        Return a list of tuple pairs [(receiver, response), ... ]. May raise
        DispatcherKeyError.

        If any receiver raises an error (specifically any subclass of
        Exception), the error instance is returned as the result for that
        receiver.
        """

        # Call each receiver with whatever arguments it can accept.
        for receiver in self._live_receivers(_make_id(sender)):
            try:
                receiver(signal=self, sender=sender, **named)
            except Exception:
                pass
