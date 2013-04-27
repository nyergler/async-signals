===============
 Async Signals
===============

*Async Signals* provides an implementation of `Django signals`_ that
are fired asynchronously. When you send a Django signal, all receivers
are called synchronously. Sometimes you want to just send the signal,
and move on. *Async Signals* let you do just that, in a way that can
be easily mixed and matched with normal, synchronous signals. *Async
Signals* uses Celery_ for signal routing.


Sending an Async Signal
=======================

You can send an asynchronous signal just like you would a normal one::

   >>> from async_signals.signals import request_started
   >>> request_started.send(None)

When you fire an asynchronous signal, a task is sent to Celery, which
will propagate the signal to any listeners. If Celery is not
configured, Async Signals will emit a Warning and trigger the
receivers synchronously.


Registering a Signal Receiver
=============================

*Async Signals* are registered exactly like "normal" Django signals.
You can either register them manually::

    from async_signals.signals import request_finished

    request_finished.connect(my_callback)

You can also use the decorator included with Django::

    from async_signals.signals import request_finished
    from django.dispatch import receiver

    @receiver(request_finished)
    def my_callback(sender, **kwargs):
        print "Request finished!"

.. admonition:: Where should this code live?

    You can put signal handling and registration code anywhere you like.
    However, you'll need to make sure that the module it's in gets imported
    early on so that the signal handling gets registered before any signals need
    to be sent. This makes your app's ``models.py`` a good place to put
    registration of signal handlers.


Defining Your Own Signals
=========================

You can define your own signals by calling the ``AsyncSignal`` class.
::

   from async_signals import AsyncSignal

   my_signal = AsyncSignal()

You can also specify arguments that will be passed along to your
signal's receivers::

   from async_signals import AsyncSignal

   request_started = AsyncSignal(providing_args=('host', 'path',))

Routing Signals via Queues
==========================

You can route signals to different `Celery queues`_ by providing an
explicit ``queue`` when creating your Signal::

   routed_signal = AsyncSignal(queue='high_priority')

The queue name will be used for the signal notification. Note that
only one Celery task is created each time a signal is emitted; once
picked up by the worker, the receivers are still processed
synchronously.

If no queue is specified, the default Celery queue will be used.


License
=======
