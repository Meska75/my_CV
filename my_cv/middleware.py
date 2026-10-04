from django.conf import settings
from django.utils import translation


class CookieLanguageMiddleware:
    """Use the language cookie only — default stays Persian, not the browser header."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed = {code for code, _name in settings.LANGUAGES}
        lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
        if lang not in allowed:
            lang = settings.LANGUAGE_CODE
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        translation.deactivate()
        return response
