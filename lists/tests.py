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

        new_list = List.objects.first()
        self.assertRedirects(
            response,
            '/lists/{}/'.format(new_list.id),
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
        the_list = List.objects.create()
        response = self.client.get(
            '/lists/{}/'.format(the_list.id))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        the_list = List.objects.create()
        a = Item.objects.create(text='Item A', list=the_list)
        b = Item.objects.create(text='Item B', list=the_list)

        another_list = List.objects.create()
        Item.objects.create(text='Another Item A', list=another_list)
        Item.objects.create(text='Another Item B', list=another_list)

        response = self.client.get(
            '/lists/{}/'.format(the_list.id))

        self.assertContains(response, 'Item A')
        self.assertContains(response, 'Item B')
        self.assertNotContains(response, 'Another Item A')
        self.assertNotContains(response, 'Another Item B')

    def test_passes_correct_view_to_template(self):
        the_list = List.objects.create()
        response = self.client.get(
                '/lists/{}/'.format(the_list.id))
        self.assertEqual(response.context['list'], the_list)

class NewItemTest(TestCase):

    def test_can_save_POST_request_to_an_existing_list(self):
        the_list = List.objects.create()
        item_text = 'new item for existing list'

        self.client.post(
            '/lists/{}/add_item'.format(the_list.id),
            data={'item_text': item_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, item_text)
        self.assertEqual(item.list, the_list)

    def test_redirects_to_list_view(self):
        the_list = List.objects.create()
        item_text = 'new item for existing list'

        response = self.client.post(
            '/lists/{}/add_item'.format(the_list.id),
            data={'item_text': item_text}
        )
        self.assertRedirects(
            response,
            '/lists/{}/'.format(the_list.id))

