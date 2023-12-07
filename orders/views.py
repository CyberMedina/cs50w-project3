import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


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

    print(request.session['response_data'])

    return render(request, 'index.html', context)


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username= email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos. Por favor, inténtalo de nuevo.')
            
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

@csrf_exempt
def addCart(request, product_id):
    

    product_variant_price = get_object_or_404(ProductVariantPrice, id=product_id)

    response_data = product_variant_price.jsonProductVariantPrice()

    response_dict = {
    'id': response_data['id'],
    'Category': response_data['Category'],
    'productName': response_data['productName'],
    'price': str(response_data['price']),
    'size': response_data['size']
}

    # Obtener la lista de registros existentes en sesión
    response_data_list = request.session.get('response_data_list', [])

    # Agregar el nuevo registro a la lista
    response_data_list.append(response_dict)

    # Guardar la lista actualizada en sesión
    request.session['response_data_list'] = response_data_list




    

    # Devolver la respuesta en formato JSON
    return JsonResponse(response_data)


def createOrder(request):
    # Crear una nueva orden
    order = Order.objects.create(user=request.user)

    # Agregar cada elemento en response_data_list como un nuevo OrderItem
    for response_data in request.session.get('response_data_list', []):
        try:
            product_variant_price = ProductVariantPrice.objects.get(id=response_data['id'])
            product_variant = product_variant_price.product_variant
            size = product_variant_price.size
            quantity = '1'

            order_item = OrderItem.objects.create(
                order=order,
                product_variant=product_variant,
                size=size,
                quantity=quantity
            )
        except ProductVariantPrice.DoesNotExist:
            return JsonResponse({"error": "ProductVariantPrice does not exist"}, status=400)
        
    request.session['response_data_list'] = []

    return render(request, 'createOrder.html')


def deleteCart(request):
    request.session['response_data_list'] = []
    return redirect('index')












def logout_view(request):
    logout(request)
    return redirect('login')
