from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def index(request):
    categories_with_sizes = []
    all_categories = ProductCategory.objects.prefetch_related(
        'product_set__productvariant_set__productvariantprice_set',
        'product_set__productvariant_set__productvariantprice_set__size'
    ).all()

    for category in all_categories:
        # Filtrando los tamaños basándose en los productos de esta categoría
        size_ids_in_use = ProductVariantPrice.objects.filter(
            product_variant__product__category=category
        ).values_list('size_id', flat=True).distinct()
        sizes = Size.objects.filter(id__in=size_ids_in_use)

        categories_with_sizes.append({
            'category': category,
            'sizes': sizes
        })

    context = {
        'categories_with_sizes': categories_with_sizes,
        'Topings': Topping.objects.all(),
    }

    return render(request, 'index.html', context)


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username= email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
            
    context = {}

    return render(request, 'auth/login.html', context)

def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            return redirect('login')
        


    context = {'form' : form}
    return render(request, 'auth/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')











