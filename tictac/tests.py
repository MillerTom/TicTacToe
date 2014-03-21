from django.test import TestCase
from django.conf import settings
from django.utils.importlib import import_module


class ViewTests(TestCase):

    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_board(self):
        session = self.session
        session['player_letter'] = 'X'
        session['player_name'] = 'human'
        session.save()
        response = self.client.get('/board', follow=True)
        self.assertEqual(response.context['player_letter'], 'X')
        self.assertEqual(response.context['computer_letter'], 'O')