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

        views.home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new list item')

    def test_home_page_redirect_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = views.home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],
                         '/lists/the-only-list-in-the-world')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        views.home_page(request)

        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_can_save_and_retreive_items(self):
        item1 = Item(text='First item')
        item1.save()
        item2 = Item(text='Second item')
        item2.save()

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)
        self.assertEqual(list(items), [item1, item2])


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='Item A')
        Item.objects.create(text='Item B')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Item A')
        self.assertContains(response, 'Item B')
