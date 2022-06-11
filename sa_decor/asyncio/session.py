from functools import wraps

from sa_decor.session import with_session


class with_async_session(with_session):
    def __call__(self, func):
        @wraps(func)
        async def session_manager(*args, **kwargs):
            if kwargs.get("session", None):
                return await func(*args, **kwargs)
            async with self.session_maker() as sess:
                error = False
                try:
                    result = await func(*args, **kwargs, session=sess)
                    if self.commit:
                        await sess.commit()
                    return result
                except Exception:
                    error = True
                    raise
                finally:
                    if self.force_commit and error:
                        await sess.commit()

        return session_manager
