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
from django.contrib.auth.models import User
from django.db.models import Count, Min


@csrf_exempt
def index(request):
    first_product_ids = Product.objects.values('category').annotate(first_product_id=Min('id')).values_list('first_product_id', flat=True)

    categories_with_first_product = Product.objects.filter(id__in=first_product_ids)

    categories_count = Product.objects.values('category').annotate(product_count=Count('id'))

    categories = []
    for category in categories_count:
        category['first_product'] = next((prod for prod in categories_with_first_product if prod.category == category['category']), None)
        categories.append(category)

    top_products = Product.objects.all().order_by('-purchase_count')[:8]
    return render(request, 'index.html', {'top_products': top_products, 'categories': categories})

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
    category_name = request.GET.get('category')
    if category_name:
        products = Product.objects.filter(category=category_name)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {'products': products, 'category_name': category_name})

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
    email_id_list = email_ids.split(',')

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            emails = EmailAddress.objects.filter(id__in=email_id_list).values_list('email', flat=True)

            send_mail(subject, message, 'từ@example.com', emails, fail_silently=False)

            return redirect('/admin/onlineshop/emailaddress/')

    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})

@csrf_exempt
def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]
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
                email_obj.full_clean()
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
        try:
            data = json.loads(request.body)

            name = data.get('name')
            phone_number = data.get('phone_number')
            address = data.get('address')
            note = data.get('note')
            total = data.get('total')

            order_details_json = data.get('order_details')
            order_details_list = json.loads(order_details_json)

            formatted_order_details = []
            for item in order_details_list:
                product = Product.objects.get(name=item['name'])

                product.purchase_count += item['quantity']
                product.save()

                formatted_item = f"{item['name']}, size {item['size']} x {item['quantity']}"
                formatted_order_details.append(formatted_item)

            formatted_order_details_str = "\n".join(formatted_order_details)

            user = request.user if request.user.is_authenticated else None

            order = Order.objects.create(
                user=user,
                name=name,
                phone_number=phone_number,
                address=address,
                note=note,
                order_details=formatted_order_details_str,
                total=total
            )
            
            request.session['cart'] = []
            request.session.modified = True

            return JsonResponse({'message': 'Order created successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def order_done(request):
    return render(request, 'order_done.html')

@csrf_exempt
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-create_at')
    
    return render(request, 'profile.html', {'orders': orders})

@csrf_exempt
def product_categories(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    return JsonResponse(list(categories), safe=False)