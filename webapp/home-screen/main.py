#!/usr/bin/env python
import google
import logging
import homescreen
"""
This module works as a bootstrapr for Google App Engine.
"""


logger = logging.getLogger('main')


app = None

try:
    import inspect
    import os
    imports = [
        inspect.getfile(google),
        inspect.getfile(homescreen),
        inspect.getfile(logging),
        inspect.getfile(os),
    ]
    imports_s = '\n'.join(imports)
    message = 'module path:\n{0}'.format(imports_s)
    logger.debug(message)
except ImportError:
    logger.warn('Module \'inspect\' is not available. Can not print imported modules file path.')
logging.info('Starting app from main.py')


app = homescreen.main(None)
