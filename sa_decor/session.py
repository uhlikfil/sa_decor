from functools import wraps

from sa_decor import globals as G


class with_session:
    def __init__(
        self, *, commit: bool = None, force_commit: bool = None, session_maker=None
    ):
        """Decorate a function and declare it with a named only parameter `session`
        `def foo(a, b, c=False, *, session):`
        Then call the function either with an existing session to pass it to the function
        `foo(1, 2, session=my_session)`
        Or let the decorator create one for you
        `foo(1, 2)`

        :param commit: Commit the session after the function
        :param force_commit: Commit even when an exception occurs
        :param session_maker: Pass a session maker if the global is not set (e.g. when using multiple session makers in the application)
        :raises ValueError: If the combination of arguments is invalid
        """
        if commit is None and force_commit is None:
            raise ValueError("commit or force_commit must be specified")
        if commit is False and force_commit:
            raise ValueError("cannot force commit and not commit")

        self.commit = commit
        self.force_commit = force_commit
        self._session_maker = None
        self._supplied_session_maker = session_maker

    def __call__(self, func):
        @wraps(func)
        def session_manager(*args, **kwargs):
            if kwargs.get("session", None):
                return func(*args, **kwargs)
            with self.session_maker() as sess:
                error = False
                try:
                    result = func(*args, **kwargs, session=sess)
                    if self.commit:
                        sess.commit()
                    return result
                except Exception:
                    error = True
                    raise
                finally:
                    if self.force_commit and error:
                        sess.commit()

        return session_manager

    @property
    def session_maker(self):
        if self._session_maker is None:
            if self._supplied_session_maker is None and G._session_mkr is None:
                raise ValueError("specify session_maker or set_global_session_maker")
            self._session_maker = (
                self._supplied_session_maker
                if self._supplied_session_maker is not None
                else G._session_mkr
            )
        return self._session_maker
