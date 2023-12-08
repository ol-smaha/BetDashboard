from . import models


def RequestExposerMiddleware(get_response):
    def middleware(request):
        models.current_request = request
        response = get_response(request)
        return response

    return middleware
