import datetime

COOKIE_KEY = "doormat_seen"


class DoormatMiddleware(object):

    def process_request(self, request):

        request.show_doormat = COOKIE_KEY not in request.COOKIES

    def process_response(self, request, response):

        if request.show_doormat:
            response.set_cookie(COOKIE_KEY, value=datetime.datetime.utcnow().isoformat())

        return response
