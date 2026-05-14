import logging
import os

from django.conf import settings


def get_logger(name: str):
    # Default to INFO, but use WARNING in production when DEBUG is False
    level = logging.INFO

    try:
        if not settings.DEBUG:
            level = logging.WARNING
    except Exception:
        pass

    # Allow overriding from environment variables
    env_level = os.environ.get("LOG_LEVEL")
    if env_level:
        level = getattr(logging, env_level.upper(), level)

    logging.basicConfig(
        level=level, format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    return logging.getLogger(name)
