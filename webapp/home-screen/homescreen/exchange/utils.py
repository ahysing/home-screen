import logging

logger = logging.getLogger(__name__)


def remove_namespace(namespace):
    namespace_str = str(namespace)
    logger.debug(namespace_str)


def get_testuser_username(given_name, family_name):
    pass