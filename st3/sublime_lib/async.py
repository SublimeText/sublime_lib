from concurrent.futures import Future
from functools import partial, wraps
from traceback import print_exception
from inspect import isgenerator
from threading import Thread, Event
from time import sleep, monotonic
from queue import Queue, PriorityQueue, Empty


def wait_for_condition(condition, period=100, iterations=5):
    for i in range(iterations):
        result = condition()
        if result:
            return result
        else:
            yield period

    raise TimeoutError("Timed out after {}ms.".format(iterations * period))


def promise(function):
    future = Future()
    function(future)
    return future


def run(function, scheduler):
    future = Task(function, scheduler).future
    future.add_done_callback(log_error)
    future.add_done_callback(lambda future: scheduler(None, 0))
    return future


def log_error(future):
    ex = future.exception(0)
    if ex:
        print_exception(type(ex), ex, ex.__traceback__)


class Task():
    def __init__(self, function, scheduler):
        self._schedule = scheduler
        self.future = Future()

        self._schedule(partial(self._start, function), 0)

    def _start(self, function):
        try:
            result = function()
        except Exception as ex:
            self.future.set_exception(ex)
        else:
            if isgenerator(result):
                self.generator = result
                self._next()
            else:
                self.future.set_result(result)

    def _next(self, future=None):
        try:
            if future is None:
                action = next(self.generator)
            else:
                try:
                    result = future.result(0)
                except Exception as ex:
                    action = self.generator.throw(ex)
                else:
                    action = self.generator.send(result)
        except StopIteration as ex:
            self.future.set_result(ex.value)
        except Exception as ex:
            self.future.set_exception(ex)
        else:
            if callable(action):
                action = Task(partial(wait_for_condition, action), self._schedule).future
            elif action is None:
                action = 0

            if isinstance(action, int):
                delay = action
                self._schedule(self._next, delay)
            elif isinstance(action, Future):
                action.add_done_callback(
                    lambda f: self._schedule(partial(self._next, f), 0)
                )
            else:
                raise TypeError("Task returned invalid action.")


def async_decorator(run):
    def decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            return run(partial(function, *args, **kwargs))

        return wrapped

    return decorator


def _single_thread_runner_worker(get):
    while True:
        function, delay = get()
        if function is None:
            return
        if delay:
            sleep(delay / 1000)
        function()


def thread_scheduler():
    queue = Queue(maxsize=1)
    thread = None

    def _schedule(function, delay):
        queue.put_nowait((function, delay))

        nonlocal thread
        if thread is None:
            thread = Thread(target=partial(_single_thread_runner_worker, queue.get))
            thread.start()

    return _schedule


class SharedThreadRunner():
    def __init__(self, *, persist=False):
        self.persist = persist

        self.queue = PriorityQueue()
        self.event = Event()
        self.thread = None

        if self.persist:
            self._start()

    def _start(self):
        self.thread = Thread(target=self._worker)
        self.thread.start()

    def _worker(self):
        while True:
            try:
                at, function = self.queue.get(block=self.persist)
            except Empty:
                self.thread = None
                return

            time_remaining = at - monotonic()
            if time_remaining <= 0:
                if function:
                    function()
            else:
                self.queue.put_nowait((at, function))
                self.event.clear()
                self.event.wait(timeout=time_remaining)

    def schedule(self, function, delay):
        at = monotonic() + delay / 1000
        self.queue.put((at, function))
        self.event.set()
        if self.thread is None:
            self._start()
