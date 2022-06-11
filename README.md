# sa_decor

SQLAlchemy decorators for an optional connection/session dependency injection.

## usage
Annotate a function with one of the decorators and add a named parameter.
```
@with_connection()
def foo(a, b, *, connection):
    ...
    connection.execute(...)
    ...
```
Then either call the function without the parameter to let the decorator connect for you,
```
foo(1, 2)
```
or supply an existing connection/session.
```
foo(1, 2, connection=my_connection)
``` 
