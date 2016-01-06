import threading


class LogTracker(object):
    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

        # one-time configuration code goes here

    def __call__(self, request):
        """
        Credits goes to Alex Contrad for inventing this technique
        http://www.alexconrad.org/2012/08/log-unique-request-ids-with-pyramid.html
        :param handler: Pyramid request handler
        :param registry:
        :return:
        """
        current_thread = threading.current_thread()
        original_name = current_thread.name
        current_thread.name = "%s][request=%s" % (original_name, request.id)
        try:
            response = self.handler(request)
        finally:
            # Restore the thread's original name when done
            current_thread.name = original_name
        return response
