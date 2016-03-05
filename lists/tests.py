from django.core.urlresolvers import resolve
from django.test import TestCase
import lists.views as views
from django.http import HttpRequest
from django.template.loader import render_to_string


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home_page(request)
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        new_item_text = 'A new list item'
        request.POST['item_text'] = new_item_text

        response = views.home_page(request)

        self.assertIn(new_item_text, response.content.decode())
        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text': new_item_text}
        )
        self.assertEqual(response.content.decode(), expected_html)
