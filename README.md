# sa_decor

SQLAlchemy decorators for an optional connection/session dependency injection.

## usage with SQLAlchemy Core
You can set a global **engine** if you're using only one in your application.
```
import sa_decor

sa_decor.set_global_engine(my_engine)
```

Annotate a function and add a named parameter **connection**.
```
from sa_decor import with_connection

@with_connection()
def foo(a, b, *, connection):
    ...
    connection.execute(stmt)
    ...
```

If you're using multiple engines, you can provide them to each function separately.
```
@with_connection(engine=my_other_engine)
def bar(a, b, *, connection):
    ...
    connection.execute(stmt)
    ...
```

Then either call the function without the parameter to let the decorator connect for you, or supply an existing connection.
```
foo(1, 2)
foo(1, 2, connection=my_connection)
``` 

## usage with SQLAlchemy ORM sessions
There is a similar functionality available for ORM sessions, but you need to provide a **sessionmaker** object instead of an **engine** and add a **session** parameter. You also need to choose whether the session should be committed when the function finishes or even when the function raises an exception.
```
sa_decor.set_global_sessionmaker(my_engine)


@with_session(commit=False)
def function_that_only_queries_data(*, session):
    ...
    session.execute(select_stmt)
    ...

@with_session(commit=True)
def function_that_updates_the_db(*, session):
    ...
    session.execute(insert_stmt)
    ...
    raise Exception  # the insert **will not** be commited

@with_session(force_commit=True)
def function_that_commits_no_matter_what(*, session):
    ...
    session.execute(insert_stmt)
    ...
    raise Exception  # the insert **will** be commited
```

The commit behaviour is ignored when the function is called with an existing session.
```
function_that_commits_no_matter_what(session=my_session)
# not commited automatically!
my_session.commit()
```

## notes
This is the most useful when you have a bunch of functions that all rely on a connection/session but are sometimes called independently and sometimes from within a different function that also needs a connection.
```
@with_connection()
def get_stuff(*, connection):
    ...

@with_connection()
def do_stuff(*, connection):
    ...
    get_stuff(connection=connection)  # nested calls can use the same connection
    ...


# somewhere else in the code, e.g. an API controller
def get():
    ...
    stuff = get_stuff()
    ...

def post():
    ...
    result = do_stuff()
    ...
```
