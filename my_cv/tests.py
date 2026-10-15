from django.test import RequestFactory, TestCase

from my_cv.geo import choose_language, client_ip


class LanguageChoiceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_english_browser_outside_iran_is_english(self):
        request = self.factory.get('/', HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9', REMOTE_ADDR='8.8.8.8')
        self.assertEqual(choose_language(request), 'en')

    def test_persian_browser_is_persian(self):
        request = self.factory.get('/', HTTP_ACCEPT_LANGUAGE='fa-IR,en;q=0.8', REMOTE_ADDR='8.8.8.8')
        self.assertEqual(choose_language(request), 'fa')

    def test_iran_ip_is_persian_even_with_english_browser(self):
        request = self.factory.get('/', HTTP_ACCEPT_LANGUAGE='en-US', REMOTE_ADDR='2.144.1.1')
        self.assertEqual(choose_language(request), 'fa')

    def test_manual_choice_wins(self):
        request = self.factory.get('/', HTTP_ACCEPT_LANGUAGE='fa-IR', REMOTE_ADDR='2.144.1.1')
        request.COOKIES['cv_language'] = 'en'
        self.assertEqual(choose_language(request), 'en')

    def test_forwarded_for_is_ignored_from_a_public_socket(self):
        request = self.factory.get(
            '/',
            REMOTE_ADDR='8.8.8.8',
            HTTP_X_FORWARDED_FOR='2.144.1.1',
            HTTP_X_REAL_IP='2.144.1.1',
        )
        self.assertEqual(client_ip(request), '8.8.8.8')
        self.assertEqual(choose_language(request), 'en')
