from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product, Order, OrderItem, Signup
from django.contrib.auth import authenticate, login as auth_login, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# User Registration
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Order
from django.http import JsonResponse
# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return redirect('register')

        else:
            user = Signup(username=username, password=password)
            user.save()
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(username=username, password=password)
            request.session['user_id'] = user.id  # Store user ID in session
            return redirect('home')  # Redirect to the home page after successful login
        except Signup.DoesNotExist:
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Home Page
def home(request):
    context = {}
    if request.session.get('user_id'):
        user = Signup.objects.get(id=request.session['user_id'])
        context['username'] = user.username
    return render(request, 'home.html', context)


# Ensure only logged-in users can access the cart
  # Redirects to login page if user is not authenticated
def view_cart(request):
    # Check if the user is authenticated using your custom Signup model
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Retrieve the user object from the session
    user = Signup.objects.get(id=request.session['user_id'])

    # Retrieve or create the cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=user)

    # Get all items in the cart
    cart_items = cart.items.all()

    # Add the cart items to the context if needed
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)
def get_cart(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')  # Redirect unauthenticated users to the login page
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    if cart is not None:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('product_list')
    else:
        return redirect('login')

# Remove from Cart

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

# Checkout View

def checkout(request):
    # Check if the user is authenticated based on the Signup model
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirect to login if no user_id is in the session

    try:
        user = Signup.objects.get(id=user_id)  # Retrieve user from Signup model
    except Signup.DoesNotExist:
        return redirect('login')  # Redirect if user does not exist

    # Proceed with checkout if the user is authenticated
    return render(request, 'checkout.html', {'user': user})
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

# Process Order (Optional View)

def process_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    for item in cart.cartitem_set.all():
        Order.objects.create(user=request.user, product=item.product, quantity=item.quantity)
    cart.cartitem_set.all().delete()
    return redirect('order_success')

# Order Success View
def order_success(request):
    return render(request, 'order_success.html')

# User Login
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid username or password.'})
#
#     return render(request, 'login.html')

def some_default_cart_function():
    return Cart.objects.first()


def place_order(request):
    if request.method == 'POST':
        # Extract form data (billing details, cart items, etc.)
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        street_address = request.POST['streetAddress']
        city = request.POST['city']
        state = request.POST['state']
        postcode = request.POST['postcode']
        phone = request.POST['phone']
        email = request.POST['email']
        payment_method = request.POST['payment']

        # Assuming cart details are passed via the request or stored in session
        cart = request.session.get('cart', [])

        total_price = sum(item['price'] * item['quantity'] for item in cart)

        # Save the order to the database
        order = Order(
            first_name=first_name,
            last_name=last_name,
            street_address=street_address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            total_price=total_price,
            payment_method=payment_method
        )
        order.save()

        # Prepare email content
        order_details = f"""
        Order Details:
        Name: {first_name} {last_name}
        Address: {street_address}, {city}, {state}, {postcode}
        Phone: {phone}
        Email: {email}
        Payment Method: {payment_method}
        Total Price: ₹{total_price}

        Cart Items:
        """
        for item in cart:
            order_details += f"{item['name']} (₹{item['price']} x {item['quantity']}) = ₹{item['price'] * item['quantity']}\n"

        # Send email to admin (or the desired recipient)
        send_mail(
            'New Order Received',
            order_details,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        # Clear cart (optional)
        request.session['cart'] = []

        # Redirect to success page
        return redirect('order_success')

    return render(request, 'checkout.html')
def order_summary(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.items.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_summary.html', context)

def contact(request):
    return render(request, 'contact.html')

def profile_view(request):
    """
    Display the profile of the logged-in user.
    """
    return render(request, 'profile.html')

def edit_profile(request):
    """
    Handle the profile editing process without using Django forms.
    """
    if request.method == 'POST':
        # Get the data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Ensure that the user submitted valid data
        if first_name and last_name and email:
            # Update the user object directly
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            # Display success message
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fill out all fields.')
            return redirect('edit_profile')

    return render(request, 'edit_profile.html', {'user': request.user})


def update_profile(request):
    # Get the profile associated with the logged-in user
    profile = request.user.profile

    if request.method == 'POST':
        # Update the user details
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        # Update the profile details
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        # Display success message
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')  # Redirect to the profile page

    return render(request, 'profile.html')

def product1_view(request):
    return render(request, 'product1.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def return_policy(request):
    return render(request, 'return_policy.html')

def seller_terms(request):
    return render(request, 'Seller_Terms_and_Conditions.html')

def terms_of_use(request):
    return render(request, 'Terms_of_Use.html')

def cancellation_policy(request):
    return render(request, 'cancellation_policy.html')

def faq(request):
    return render(request, 'FAQ.html')

def about_us(request):
    return render(request, 'about_us.html')

def customer_care(request):
    """Display the 24/7 Customer Care page with contact form and chat"""
    return render(request, 'customer-care.html')


def submit_query(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Send email logic
        try:
            send_mail(
                subject=f"Query from {name}",
                message=message,
                from_email=email,
                recipient_list=["dkumar11dec2003@gmail.com"],  # Replace with your email
            )
            return JsonResponse({"success": True})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})


def order_history(request):
    # Fetch the user_id from session (if logged in)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Assuming that user_id corresponds to the user's email, adjust as necessary
    # If the user is identified by email in your session, fetch orders for that email
    orders = Order.objects.filter(email=request.user.email)  # Or use the user_id logic if email isn't sufficient

    return render(request, 'order_history.html', {'orders': orders})


def cancel_order(request, order_id):
    # Fetch the user_id from session (if logged in)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Fetch the order and ensure it belongs to the logged-in user (if you're using user_id to identify users)
    order = get_object_or_404(Order, id=order_id)

    # Optionally, you can add a check to ensure the order is linked to the authenticated user.
    if order.email != request.user.email:  # Adjust this if you're using user_id
        messages.error(request, "You do not have permission to cancel this order.")
        return redirect('order_history')

    # Ensure only 'Pending' orders can be canceled
    if order.status == 'Pending':
        order.status = 'Canceled'
        order.save()
        messages.success(request, "Order canceled successfully.")
    else:
        messages.error(request, "Only pending orders can be canceled.")

    return redirect('order_history')

def send_cancellation_email(order):
    subject = f"Order #{order.id} Canceled"
    message = f"Dear {order.first_name},\n\nYour order #{order.id} has been canceled.\n\nThank you for shopping with us!"
    send_mail(subject, message, 'dkumar11dec2003@gmail.com', [order.email])