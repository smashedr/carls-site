from django.test import TestCase
from django.core.urlresolvers import reverse


class TestViews(TestCase):
    def setUp(self):
        self.views = ['home', 'github']
        self.redirects = ['add', 'discord']

    def test_views(self):
        for view in self.views:
            print('Testing reverse for view: %s' % view)
            response = self.client.get(reverse(view))
            self.assertEqual(response.status_code, 200)

    def test_redirects(self):
        for redirect in self.redirects:
            print('Testing reverse for redirect: %s' % redirect)
            response = self.client.get(reverse(redirect))
            self.assertEqual(response.status_code, 302)
