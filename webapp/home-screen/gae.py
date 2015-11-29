from google.appengine.ext import vendor

"""
This module works as a bootstrapper for Google app engine.
on start this file is running as __main__.
"""

app = None

def make_app():
    from homescreen import main
    main(None)

if __name__ == '__main__':
    # Third-party libraries are stored in "lib", vendoring will make
    # sure that they are importable by the application.
    vendor.add('lib')
    app = make_app()
