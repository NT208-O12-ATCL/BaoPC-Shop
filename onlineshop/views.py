from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from .forms import EmailForm
from .models import EmailAddress
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Order


@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart': cart})

@csrf_exempt
def checkout(request):
    return render(request, 'checkout.html')

@csrf_exempt
def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.all()
    return render(request, 'detail.html', {'product': product, 'products': products})

@csrf_exempt
def login_form(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/index')
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def shop(request):
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 6)  
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {'products': products})

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        product_info = {
            'name': data.get('name'),
            'price': int(data.get('price')),
            'size': data.get('size'),
            'quantity': int(data.get('quantity', 1))
        }
        
        cart = request.session.get('cart')

        if cart is None or not isinstance(cart, list):
            cart = []
            
        found = False
        for item in cart:
            if item['name'] == product_info['name'] and item['size'] == product_info['size']:
                item['quantity'] += product_info['quantity']
                found = True
                break

        if not found:
            cart.append(product_info)
        print(cart)
        
        request.session['cart'] = cart
        
        total_quantity = sum(item['quantity'] for item in cart)
    
        return JsonResponse({'status': 'success', 'total_quantity': total_quantity })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def send_email_view(request, email_ids):
    # Tách chuỗi thành danh sách các ID
    email_id_list = email_ids.split(',')

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Lọc email dựa trên danh sách ID
            emails = EmailAddress.objects.filter(id__in=email_id_list).values_list('email', flat=True)

            send_mail(subject, message, 'từ@example.com', emails, fail_silently=False)

            # Redirect sau khi gửi email
            return redirect('/admin/onlineshop/emailaddress/')

    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})

@csrf_exempt
def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]  # Lấy 5 sản phẩm phù hợp đầu tiên
    results = [{'name': product.name, 'price': product.price, 'image': product.image.url, 'url': reverse('product_detail', args=[product.id])} for product in products]
    return JsonResponse(results, safe=False)

@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        if not email:
            return JsonResponse({"message": "Email field is empty."}, status=400)
        
        try:
            EmailAddress.objects.get(email=email)
            return JsonResponse({"message": "Email already subscribed."}, status=400)
        except EmailAddress.DoesNotExist:
            try:
                email_obj = EmailAddress(email=email)
                email_obj.full_clean()  # Perform model validation
                email_obj.save()
                return JsonResponse({"message": "Email subscribed successfully."})
            except ValidationError as e:
                return JsonResponse({"message": e.message}, status=400)
          
@csrf_exempt  
def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        email_content = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        try:
            send_mail(
                subject,
                email_content,
                email,
                ['truongbao371500@gmail.com'],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Message sent successfully.'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('product_name')
        product_size = data.get('product_size')
        cart = request.session.get('cart', [])

        if product_name is not None and product_size is not None:
            cart = [item for item in cart if not (item.get('name') == product_name and item.get('size') == product_size)]
            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone_number = data.get('phone_number')
        address = data.get('address')
        note = data.get('note')
        order_details = data.get('order_details')
        total = data.get('total')

        # Tạo đơn hàng
        order = Order.objects.create(
            name=name,
            phone_number=phone_number,
            address=address,
            note=note,
            order_details=order_details,
            total=total
        )

        return JsonResponse({'message': 'Order created successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)