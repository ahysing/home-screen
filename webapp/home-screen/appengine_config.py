#!/usr/bin/env python
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
# https://cloud.google.com/appengine/docs/python/tools/libraries27#vendoring
# vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
