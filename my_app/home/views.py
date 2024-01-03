from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Customer, Product, ProductManager
# from.models import Product, Cart, CartItem
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
# print(make_password('12345'))
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.db import connection

from django.db import IntegrityError


# Create your views here.
def home(request):
    if request.method == "POST":
        product = request.POST.get('product')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])

    prs = Product.get_all_products()
    print(prs)
    print(request.session.get('email'))
    # Access the logged-in user object
    user = request.user
    print(user)

    # Now you can use 'user' to access properties of the logged-in user
    # username = user.username
    # email = user.email

    return render(request, 'home.html', {"product": prs})


# Create a logger
logger = logging.getLogger(__name__)


def search(request):
    if request.method == "POST":
        search_term = request.POST.get('search_query')
        results = list(Product.objects.filter(
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term)
        ))

    return render(request, 'home.html', {"product": results})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        try:
            # return HttpResponse('post request')
            # return HttpResponse(request.POST)
            postData = request.POST
            name = postData.get('name')
            email = postData.get('email')
            mobile = postData.get('mobile')
            password = postData.get('password')

            # print(name)
            # return HttpResponse(request.POST.get('password'))
            # Check if the email already exists
            if Customer.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error_message': 'This email address is already in use.'})

            customer = Customer(name=name,
                                email=email,
                                mobile=mobile,
                                password=password)
            customer.password = make_password(customer.password)
            customer.save()
            messages.success(request, 'Signup successful!')
            return redirect('home')
        except IntegrityError:
            customer.add_error('email', 'This email address is already in use.')


# def log(request):
#         if request.method == 'GET':
#             return render(request, 'login.html')
#         elif request.method=='POST':
#             email=request.POST.get('email')
#             password=request.POST.get('password')
#             # print(email)
#             # print(password)
#             print(User.objects.filter(email=email))
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 user = None
#             print(user)  

#         return HttpResponse('Login successful')

def log(request):
    if request.method == 'GET':
        return render(request, 'login.html')  # Render your login template
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email)
        # customer=Customer()

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        # Check if the authentication was successful
        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to the home page or any desired page
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password.')

        # Fetch the user by email
        print(User.objects.filter(email=email))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        print(user)

        # Validate the password if the user exists
        # passe=check_password(password,customer.password)
        # print(user.check_password(password))
        if user and check_password(password, user.password):
            # User authentication successful
            # Perform additional actions like login or redirect
            print("User authenticated successfully:", user)
            return redirect('home')
        else:
            # User authentication failed
            print("Invalid email or password.")

    return render(request, 'login.html')


# def add_to_cart(request, product_id):
#     # Retrieve the product based on the product_id passed in the URL
#     product = get_object_or_404(Product, pk=product_id)

#     # Get or create a Cart instance associated with the current user
#     user_cart, created = Cart.objects.get_or_create(user=request.user)

#     # Check if the product already exists in the user's cart
#     cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

#     # If the cart item already exists, increment its quantity
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     # Redirect to the cart detail view after adding the item to the cart
#     return redirect('cart:cart_detail')

# def my_cart(request):

#     return render(request, 'my_cart.html')

def my_cart(requests):
    cart = requests.session.get('cart', {})

    # Get the product IDs from the cart
    product_ids = cart.keys()

    # Fetch the products based on their IDs
    products_in_cart = Product.objects.filter(id__in=product_ids)

    # Create a dictionary to map product IDs to their details
    cart_with_details = {}
    total_quantity = 0
    total_price = 0

    # for product in products_in_cart:
    #     cart_with_details[product.id] = {
    #         'name': product.name,
    #         'image': product.image.url,  # Assuming image is a field in your Product model
    #         'price': product.price,
    #         'quantity': cart[str(product.id)],  # Get quantity from the cart
    #         'subtotal': product.price * cart[str(product.id)],
    #     }
    #     total_quantity += quantity
    #     total_price += product_details['subtotal']

    for product in products_in_cart:
        quantity = cart.get(str(product.id), 0)  # Use get method to avoid KeyError
        if quantity > 0:
            product_details = {
                'name': product.name,
                'image': product.image.url,
                'price': product.price,
                'quantity': quantity,
                'subtotal': product.price * quantity,
            }
            total_quantity += quantity
            total_price += product_details['subtotal']
            cart_with_details[product.id] = product_details

    # Pass the detailed product information to the cart template
    return render(requests, 'my_cart.html',
                  {'cart': cart_with_details, 'total_quantity': total_quantity, 'total_price': total_price})
