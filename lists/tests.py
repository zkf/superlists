from django.core.urlresolvers import resolve
from django.test import TestCase
import lists.views as views
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


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


class ItemModelTest(TestCase):

    def test_can_save_and_retreive_item(self):
        item1 = Item(text='First item')
        item1.save()
        item2 = Item.objects.all()[0]

        self.assertEqual(item1, item2)

    def test_can_save_and_retreive_items(self):
        item1 = Item(text='First item')
        item1.save()
        item2 = Item(text='Second item')
        item2.save()

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)
        self.assertEqual(set(items), set([item1, item2]))
