from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from .forms import OrderForm,ProductForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import Round
<<<<<<< HEAD
from .utils import product_rating_filter
=======
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e




# Create your views here.


def index(request,category_id=None):
    search_query = request.GET.get('q','')
    filter_type = request.GET.get('filter','')
    categories = Category.objects.all()
    
    
    
    
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all() #.order_by('-price')
        
    
        
    if search_query:
        products = products.filter(name__icontains = search_query)
        
    products = products.annotate(avg_rating = Round(Avg('comments__rating'),precision = 2) )

<<<<<<< HEAD
    products = product_rating_filter(filter_type,products)
   
=======
        
    if filter_type == 'expensive':
        products = products.order_by('-price')
    
    elif filter_type == 'cheap':
        products = products.order_by('price')
        
    
    elif filter_type == 'rating':
        products = products.order_by('-avg_rating')
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e
    
    # DRY => Dont Repeat Yourself
    
        
    
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html',context)


def product_detail(request,product_id):
    try:
        product = Product.objects.get(id = product_id)
<<<<<<< HEAD
        related_products = Product.objects.filter(category = product.category).exclude(id=product.id)
        context = {
            'product':product,
            'related_products':related_products,
            }
=======
        context = {'product':product}
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e
        return render(request,'shop/detail.html',context)
    
    except Product.DoesNotExist:
        return HttpResponse('Product Not Found')
    
    
def order_detail(request,pk):
    # product = Product.objects.get(id = pk)
    product = get_object_or_404(Product,pk=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.amount < order.quantity or order.quantity == 0:
                # send message
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Don\'t have enough product quantity'
                )
              
               
            else:
                product.amount -= order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Item successfully ordered'
                )
<<<<<<< HEAD
                return redirect('shop:product_detail',pk)
=======
                return redirect('product_detail',pk)
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e
    context = {
        'form':form,
        'product':product
    }
            
    return render(request,'shop/detail.html',context = context)
            
            
@login_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return redirect('shop:index')
=======
            return redirect('index')
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e
    
    context = {
        'form':form
    }
    return render(request,'shop/product/create.html',context)


@login_required
def edit_product(request):
    pass


@login_required
def delete_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        product.delete()
<<<<<<< HEAD
        return redirect('shop:index')
=======
        return redirect('index')
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e
    return render(request,'shop/product/delete.html',{'product':product})




def comment_create(request,pk):
    product =  get_object_or_404(Product,pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.product = product
        comment.save()
<<<<<<< HEAD
        return redirect('shop:product_detail',pk)
=======
        return redirect('product_detail',pk)
>>>>>>> 7065014f6ba19135e4a15716eb87ce3569946d8e
    
    return render(request,'shop/detail.html',{'form':form})