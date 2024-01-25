import logging
from typing import Any, Dict, Union

import structlog


def add_module_and_lineno(
    logger: Union[logging.Logger, structlog.stdlib.BoundLogger],
    name: str,
    event_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Add module and line number to the event dict
    Args:
        logger(structlog.stdlib.BoundLogger): structlog logger
        name(str): logger method (info/debug/..)
        event_dict(dict): log event dict
    Returns:
        event_dict (dict)
    """
    # see https://github.com/hynek/structlog/issues/253 for a feature request to get this done better
    # noinspection PyProtectedMember,PyUnresolvedReferences
    frame, module_str = structlog._frames._find_first_app_frame_and_name(
        additional_ignores=[__name__, "logging"]
    )
    event_dict["modline"] = f"{module_str}:{frame.f_lineno}"
    return event_dict


def configure_structlog():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(remove_positional_args=True),
            structlog.processors.StackInfoRenderer(),
            add_module_and_lineno,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
