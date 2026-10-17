"""Visitor language and client IP.

Persian when the visitor is in Iran or the browser's preferred language is
Persian. Any other case is English, unless the visitor already picked a
language with the switcher (that choice is stored in the language cookie).
"""
import ipaddress
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.utils.translation.trans_real import parse_accept_lang_header

_DATA = Path(__file__).resolve().parent / 'data'
_LOCALHOST = {'127.0.0.1', '::1'}


@lru_cache(maxsize=1)
def iran_networks():
    """Iranian prefixes from ipdeny, stored next to this module."""
    networks = []
    for name in ('ir-ipv4.zone', 'ir-ipv6.zone'):
        path = _DATA / name
        if not path.exists():
            continue
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                networks.append(ipaddress.ip_network(line, strict=False))
            except ValueError:
                continue
    return tuple(networks)


def client_ip(request):
    """Address of the visitor, not a header the browser can invent.

    Behind nginx on this same machine, the socket address is localhost and
    nginx's X-Real-IP is the visitor. On shared hosting the socket address
    is already the visitor, so extra forwarding headers are ignored.
    """
    remote = (request.META.get('REMOTE_ADDR') or '').strip()
    if getattr(settings, 'TRUST_CLOUDFLARE', False):
        cloudflare = (request.META.get('HTTP_CF_CONNECTING_IP') or '').split(',')[0].strip()
        if cloudflare:
            return cloudflare
    if remote in _LOCALHOST:
        real = (request.META.get('HTTP_X_REAL_IP') or '').split(',')[0].strip()
        if real:
            return real
    return remote


def ip_in_iran(ip_text):
    try:
        address = ipaddress.ip_address((ip_text or '').strip())
    except ValueError:
        return False
    return any(address in network for network in iran_networks())


def visitor_in_iran(request):
    if getattr(settings, 'TRUST_CLOUDFLARE', False):
        country = (request.META.get('HTTP_CF_IPCOUNTRY') or '').strip().upper()
        if country == 'IR':
            return True
        if country and country not in {'XX', 'T1'}:
            return False
    return ip_in_iran(client_ip(request))


def browser_prefers_persian(request):
    header = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if not header:
        return False
    try:
        parsed = parse_accept_lang_header(header)
    except ValueError:
        return False
    if not parsed:
        return False
    primary = parsed[0][0].lower().replace('_', '-').split('-')[0]
    return primary == 'fa'


def choose_language(request):
    allowed = {code for code, _name in settings.LANGUAGES}
    chosen = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, '')
    if chosen in allowed:
        return chosen
    if visitor_in_iran(request) or browser_prefers_persian(request):
        return 'fa'
    return 'en'
