from decimal import Decimal
from lib2to3.fixes.fix_input import context
from re import search

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request

from ecommerce.forms import ProductCommentForm, ProductModelForm
from ecommerce.models import Product, ProductAttribute, Customers


# Create your views here.


def index(request):
    products = Product.objects.all()
    product_attributes = ProductAttribute.objects.all()

    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'ecommerce/product-list.html', context=context)

    # paginator = Paginator(products, 4)
    # page_number = request.GET.get("page")
    # page_obj = paginator,get_page(page_number)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }

    return render(request, 'ecommerce/product-details.html', context=context)

def customers(request):
    return render(request, 'ecommerce/customers.html')

def customer_details(request):
    return render(request, 'ecommerce/customer-details.html')


@login_required
def product_like_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user in product.likes.all():
        product.likes.remove(request.user)
    else:
        product.likes.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def send_product_comment(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        comment_form = ProductCommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.rating = Decimal(request.POST.get('rating', 0))
            comment.save()
            return redirect('ecommerce:product-detail', pk=product.pk)

    else:
        comment_form = ProductCommentForm()

    context = {
        'product': product,
        'comment_form': comment_form
    }

    return render(request, 'ecommerce/product-details.html', context=context)


def product_create(request):
    # form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:index')
    else:
        form = ProductModelForm()
    context = {
        'form': form,
        'action': 'Create'
    }
    return render(request, 'ecommerce/create.html', context=context)


def product_delete(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        product.delete()
        return redirect('index')
    except Product.DoesNotExist as e:
        print(e)


def product_edit(request, slug):
    product = Product.objects.get(slug=slug)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:product-detail', slug=product.slug)
    context = {
        'form': form,
        'product': product,
        'action': 'Edit New'
    }
    return render(request, 'ecommerce/create.html', context=context)


def search_view(request):
    search_query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=search_query)
    context = {
        'products': products
    }
    return render(request, 'ecommerce/product-list.html', context=context)



def customer_list(request):
    customers = Customers.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'ecommerce/customers.html', context=context)

