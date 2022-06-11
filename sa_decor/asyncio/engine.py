from functools import wraps

from sa_decor.engine import with_connection


class with_async_connection(with_connection):
    def __call__(self, func):
        @wraps(func)
        async def session_manager(*args, **kwargs):
            if kwargs.get("connection", None):
                return await func(*args, **kwargs)
            async with self.engine.connect() as conn:
                return await func(*args, **kwargs, connection=conn)

        return session_manager
