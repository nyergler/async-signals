from async_signals.dispatcher import AsyncSignal

# Request lifecycle signals
request_started = AsyncSignal()
request_finished = AsyncSignal()
