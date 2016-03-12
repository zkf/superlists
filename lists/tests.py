from django.core.urlresolvers import resolve
from django.test import TestCase
import lists.views as views
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home_page(request)
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(response.content.decode(), expected_html)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        new_item_text = 'A new list item'

        self.client.post(
            '/lists/new',
            data={'item_text': new_item_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, new_item_text)

    def test_redirects_after_POST(self):
        new_item_text = 'A new list item'

        response = self.client.post(
            '/lists/new',
            data={'item_text': new_item_text}
        )

        self.assertRedirects(
            response,
            '/lists/the-only-list-in-the-world/',
        )

class ListAndItemModelTest(TestCase):
    def test_saving_and_retreiving_items(self):
        the_list = List()
        the_list.save()

        item1 = Item(text='First item', list=the_list)
        item1.save()
        item2 = Item(text='Second item', list=the_list)
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, the_list)

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)
        self.assertEqual(list(items), [item1, item2])


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        the_list = List.objects.create()
        Item.objects.create(text='Item A', list=the_list)
        Item.objects.create(text='Item B', list=the_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Item A')
        self.assertContains(response, 'Item B')
