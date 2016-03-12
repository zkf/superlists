from django.shortcuts import render, redirect
from lists.models import Item, List
# from django.http import HttpResponse


def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {
        'list': the_list,
    })

def new_list(request):
    the_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],
                        list=the_list)
    return redirect('/lists/{}/'.format(the_list.id))

def add_item(request, list_id):
    the_list = List.objects.filter(id=list_id).first()
    Item.objects.create(
        text=request.POST['item_text'],
        list=the_list)
    return redirect('/lists/{}/'.format(list_id))
