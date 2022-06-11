_engine = None
_session_mkr = None


def set_global_engine(engine) -> None:
    """Set a global SQLAlchemy engine to avoid passing engine to each decorator

    :param engine: SQLAlchemy engine to set
    """
    global _engine
    _engine = engine


def set_global_sessionmaker(sessionmaker) -> None:
    """Set a global SQLAlchemy session maker to avoid passing it to each decorator

    :param engine: SQLAlchemy session maker to set
    """
    global _session_mkr
    _session_mkr = sessionmaker
