from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django_currentuser.middleware import get_current_authenticated_user, get_current_user

from SitePC.forms import HelpForm
from SitePC.models import PC, Category
from accounts.models import User
from .cart import Cart
from .forms import CartAddPCForm
from SitePC.utils import DataMixin

menu = [{'title': 'О нас', 'url_name': 'about'},
        {'title': 'Отзывы', 'url_name': 'reviews'}]

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(PC, id=product_id)
    form = CartAddPCForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(PC, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request, **kwargs):
    cart = Cart(request)
    len = cart.__len__()
    for item in cart:
        item['update_quantity_form'] = CartAddPCForm(initial={'quantity': item['quantity'],
                                                              'update': True})
    context = kwargs
    cats = Category.objects.all()
    user = get_object_or_404(User, pk=get_current_authenticated_user().id)
    context['user'] = user
    context['menu'] = menu
    context['cats'] = cats
    if 'cat_selected' not in context:
        context['cat_selected'] = 0

    return render(request, 'cart/detail.html', {'cart': cart, 'menu':menu, 'cats':cats, 'title': "Корзина", 'user':user, 'len': len})

def cart_search(request, product_id):
    cart = Cart(request)
    key = cart.search(product_id)
    return key


