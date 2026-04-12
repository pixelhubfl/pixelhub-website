from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
import uuid
from django.core.files.storage import FileSystemStorage
import stripe
from django.conf import settings
from django.core.mail import EmailMessage

# 🔥 Stripe config
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'main/home.html')


def shop(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if min_price:
        products = products.filter(base_price__gte=min_price)

    if max_price:
        products = products.filter(base_price__lte=max_price)

    return render(request, 'main/shop.html', {
        'products': products,
        'query': query
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        return add_to_cart(request, id)

    return render(request, 'main/product.html', {'product': product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})

    quantity = int(request.POST.get('quantity', 1))

    width = request.POST.get('width')
    height = request.POST.get('height')
    notes = request.POST.get('notes')
    file = request.FILES.get('file')

    price = product.base_price

    design_service = request.POST.get('design_service')

    if design_service:
        price += 30

    if product.is_custom_size and width and height:
        price = float(width) * float(height) * product.base_price

    file_url = None
    if file:
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)

    unique_key = str(uuid.uuid4())

    cart[unique_key] = {
        'name': product.name,
        'price': price,
        'quantity': quantity,
        'notes': notes,
        'size': f"{width}ft x {height}ft" if width else "Standard",
        'file': file_url,
        'design': True if design_service else False,
    }

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, 'main/cart.html', {
        'cart': cart,
        'total': total
    })


def remove_from_cart(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    return redirect('cart')


# 💳 STRIPE CHECKOUT
def create_checkout_session(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('shop')

    line_items = []

    for item in cart.values():
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['name'],
                },
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })

    domain = 'https://pixelhubfl.com'

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=domain + '/success/',
        cancel_url=domain + '/cart/',
    )

    return redirect(session.url)


def success(request):
    request.session['cart'] = {}
    return render(request, 'main/success.html')


# 📩 SERVICES (QUOTE)
def services(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        details = request.POST.get('details')

        files = request.FILES.getlist('files')

        message = f"""
New Quote Request

Name: {name}
Email: {email}
Phone: {phone}
Service: {service}

Details:
{details}
"""

        email_message = EmailMessage(
            'New Quote - Pixel Hub',
            message,
            None,
            ['pixelhubflorida@gmail.com'],
        )

        for file in files:
            email_message.attach(file.name, file.read(), file.content_type)

        email_message.send()

        return render(request, 'main/success.html')

    return render(request, 'main/services.html')


# 🎨 DESIGN SERVICES
def design_services(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        package = request.POST.get('package')
        details = request.POST.get('details')

        files = request.FILES.getlist('files')

        message = f"""
New Design Service Request

Name: {name}
Email: {email}
Phone: {phone}
Package: {package}

Details:
{details}
"""

        email_message = EmailMessage(
            'New Design Service Request - Pixel Hub',
            message,
            None,
            ['pixelhubflorida@gmail.com'],
        )

        for file in files:
            email_message.attach(file.name, file.read(), file.content_type)

        email_message.send()

        return render(request, 'main/success.html')

    return render(request, 'main/design_services.html')