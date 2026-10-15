import secrets

from django.conf import settings
from django.utils import translation

from .geo import choose_language


class CookieLanguageMiddleware:
    """Honor a manual language choice. Otherwise Persian for Iran or a Persian browser."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = choose_language(request)
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        translation.deactivate()
        return response


class SecurityHeadersMiddleware:
    """Extra response headers. The admin theme keeps its own scripts, so CSP skips it."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        response.setdefault(
            'Permissions-Policy',
            'camera=(), microphone=(), geolocation=(), payment=()',
        )
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin')
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        if _csp_applies(request):
            nonce = request.csp_nonce
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                f"script-src 'self' 'nonce-{nonce}'; "
                "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
                "font-src 'self' https://cdn.jsdelivr.net data:; "
                "img-src 'self' data: blob:; "
                "connect-src 'self'; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "frame-ancestors 'none'; "
                "form-action 'self'"
            )
        return response


def _csp_applies(request):
    path = request.path or '/'
    admin_url = (getattr(settings, 'ADMIN_URL', 'admin/') or 'admin/').strip('/')
    if admin_url and (path == f'/{admin_url}' or path.startswith(f'/{admin_url}/')):
        return False
    if path == '/reset' or path.startswith('/reset/'):
        return False
    return True
