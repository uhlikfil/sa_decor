from functools import wraps

from sa_decor import globals as G


class with_connection:
    def __init__(self, *, engine=None):
        """Decorate a function and declare it with a named only parameter `connection`
        `def foo(a, b, c=False, *, connection):`
        Then call the function either with an existing connection to pass it to the function
        `foo(1, 2, session=my_connection)`
        Or let the decorator create one for you
        `foo(1, 2)`

        :param engine: Pass an engine if the global is not set (e.g. when using multiple engines in the application)
        """
        self._engine = None
        self._supplied_engine = engine

    def __call__(self, func):
        @wraps(func)
        def session_manager(*args, **kwargs):
            if kwargs.get("connection", None):
                return func(*args, **kwargs)
            with self.engine.connect() as conn:
                return func(*args, **kwargs, connection=conn)

        return session_manager

    @property
    def engine(self):
        if self._engine is None:
            if self._supplied_engine is None and G._engine is None:
                raise ValueError("specify engine or set_global_engine")
            self._engine = (
                self._supplied_engine
                if self._supplied_engine is not None
                else G._engine
            )
        return self._engine
