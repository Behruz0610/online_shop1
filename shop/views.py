from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib import messages
from django.http.response import HttpResponse
from .forms import OrderForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def index(request, category_id=None):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)

def product_detail(request, product_id):
    product = Product.objects.annotate(
        avg_rating=Avg('orders__rating')  # 'orders' - Order modelida related_name, rating maydoni bo'lishi shart!
    ).filter(id=product_id).first()
    if not product:
        return HttpResponse('Product Not Found')
    context = {
        'product': product,
        'avg_rating': product.avg_rating
    }
    return render(request, 'shop/detail.html', context)

def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.amount < order.quantity or order.quantity == 0:
                messages.error(request, "Don't have enough product quantity")
            else:
                product.amount -= order.quantity
                product.save()
                order.save()
                messages.success(request, 'Item successfully ordered')
                return redirect('product_detail', product_id=pk)
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'shop/detail.html', context)

@login_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'shop/product/create.html', context)

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.pk)
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'shop/product/edit.html', context)

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    return render(request, 'shop/product/delete.html', {'product': product})