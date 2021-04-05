from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import tasks
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework import permissions
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import *
from django.views import generic
from django.shortcuts import get_object_or_404
# Create your views here.


def home(request):
    products = Product.objects.all().order_by('-product_quantity')[:20]
    print(products)
    return render(request, "index.html", {"products": products})


class home_generic(generic.ListView):
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('-product_quantity')[:20]
    template_name = 'index1.html'


def login_page(request):
    return render(request, "login.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return redirect("home")
        else:
            messages.warning(request, "Username or Password is incorrect")
            return render(request, 'login.html',)
    else:
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(request, 'login.html')


@login_required(login_url="/accounts/login/")
def user_logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('home')
    else:
        return redirect("/")


@login_required(login_url="/accounts/login/")
def add_to_cart(request):
    user_id = request.GET.get("user_id")
    product_id = request.GET.get("product_id")
    order_quantity = request.GET.get("order_quantity")
    print(user_id)
    print(product_id)
    user_object = User.objects.get(id=user_id)
    product_object = Product.objects.get(id=product_id)
    order = Order(user_id=user_object, product_id=product_object, order_quantity=order_quantity)
    order.save()
    return HttpResponse("Product Added In Cart")


@login_required(login_url="/accounts/login/")
def cart(request):
    user = request.user
    order_item = Order.objects.filter(user_id=user.id, is_purchase=False)
    user_data = Profile.objects.get(user_id=user.id)
    print(len(order_item))
    address = user_data.address.first()
    print(address)
    if len(order_item) <= 0:
        messages.warning(request, "No products in your cart")
        return redirect("home")
    else:
        return render(request, "cart.html", {"orders": order_item, "user_data": user_data, "address": address})


@login_required(login_url="/accounts/login/")
def checkout(request):
    if request.method == "POST":
        user = request.user
        order_item = Order.objects.filter(user_id=user.id, is_purchase=False)
        if len(order_item) <= 0:
            messages.warning(request,"Add Product in Cart for Checkout")
            return redirect("home")
        else:
            user_data = Profile.objects.get(user_id=user)
            print(order_item)
            for i in order_item:
                remaining = i.product_id.product_quantity - i.order_quantity
                print(remaining)
                print(i.product_id)
                if remaining >= 0:
                    product_object = Product.objects.get(pk=i.product_id.id)
                    product_object.product_quantity = remaining
                    product_object.save()
                else:
                    messages.warning(request, i.product_id.name + "     Product is Out of Stock")
                    out_of_order_object = Order.objects.get(id=i.id)
                    out_of_order_object.delete()
                    order_item = Order.objects.filter(user_id=user.id, is_purchase=False)
                    user_data = Profile.objects.get(user_id=user)
                    return render(request, "cart.html", {"orders": order_item, "user_data": user_data})
            user_additional_data = Profile.objects.get(id=request.user.id)
            address = Address.objects.get(id=user_additional_data.address.first().id)
            return render(request, "checkout.html", {"orders": order_item, "user_data": user_data, "user": user, "user_profile": user_additional_data, "address": address})
    else:
        return redirect('cart')


@login_required(login_url="/accounts/login/")
def payment(request):
    if request.method == "POST":
        user = request.user
        total = request.POST.get("hidden_total")
        print(total)
        shipping = request.POST.get("hidden_shipping")
        print(shipping)
        order_item = Order.objects.filter(user_id=user.id, is_purchase=False)
        for i in order_item:
            i.is_purchase = True
            i.save()
        print(request.user.email)
        # send_mail("Hello", "Thank You for Your Order", 'ridhamdata@gmail.com', [request.user.email])
        tasks.sent_mail.delay(request.user.email)
        return redirect("confirm_order")
    else:
        return redirect('cart')


@login_required(login_url="/accounts/login/")
def confirm_order(request):
    return render(request, "confirm_order.html")


def search_result(request):
    search_list = []
    query = request.GET.get("query")
    query_list = query.split(" ")
    print(query_list)
    for q in query_list:
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(brand_id__brand__icontains=q) | Q(category_id__category__icontains=q)).distinct()
        for j in products:
            search_list.append(j)
    search_result_list = list(set(search_list))
    product_object = Product.objects.filter(name__in=search_result_list)
    print(product_object)
    return render(request, "search_result.html", {"products": product_object})


def contact(request):
    return render(request, "contact.html")


@login_required(login_url="/accounts/login/")
def user_profile(request):
    user = request.user
    user_additional_data = Profile.objects.get(id=request.user.id)
    address = Address.objects.get(id=user_additional_data.address.first().id)
    return render(request, "user_profile.html", {"user": user, "user_profile": user_additional_data, "address": address})


def single_product(request, pk=None):

    product = get_object_or_404(Product, pk=pk)
    print(product)
    if product:
        return render(request, "single-product.html", {"product":product})
    else:
        messages.warning(request, "no_products_available")
        return render(request, "single-product.html")


def shop_category(request):
    category = Category.objects.all()
    return render(request, "category.html", {"category": category},)


def category_result(request):
    category = Category.objects.all()
    search_category = request.GET.get("category")
    print(search_category)
    if search_category == "Select Category":
        messages.warning(request, "Select Category")
        return render(request, "category.html", {"category": category}, )
    else:
        search_category_object = Category.objects.get(category=search_category)
        print(search_category_object)
        print(search_category_object.id)
        products = Product.objects.filter(category_id = search_category_object.id)
        print(products)
        return render(request, "category.html", {"category": category, "products":products},)


def shop_brand(request):
    brand = Brand.objects.all()
    return render(request, "shop_by_brand.html", {"brand": brand},)


def brand_result(request):

    brand = Brand.objects.all()
    search_brand = request.GET.get("brand")
    print(search_brand)
    if search_brand == "Select Brand":
        messages.warning(request, "Select Brand")
        return render(request, "shop_by_brand.html", {"brand": brand}, )
    else:
        search_brand_object = Brand.objects.get(brand=search_brand)
        print(search_brand)
        print(search_brand_object.id)
        products = Product.objects.filter(brand_id=search_brand_object.id)
        print(products)
        return render(request, "shop_by_brand.html", {"brand": brand, "products":products},)


@login_required(login_url="/accounts/login/")
def update(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')
        add_1 = request.POST.get('add_1')
        add_2 = request.POST.get('add_2')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user__profile = Profile.objects.get(user_id=request.user.id)
        user__profile.mobile_no = mobile_number
        user__profile.save()
        address = Address.objects.get(id=user__profile.address.first().id)
        address.add_line_1 = add_1
        address.add_line_2 = add_2
        address.city = city
        address.country = country
        address.zipcode = zip
        address.save()
        print(user__profile)
        user_additional_data = Profile.objects.get(id=request.user.id)
        address = Address.objects.get(id=user_additional_data.address.first().id)
        return redirect('user_profile')
    else:
        return redirect('home')


@login_required(login_url="/accounts/login/")
def delete_cart(request):
    if request.method == "POST":
        order_id = int(request.POST.get('order_id'))
        order_object = Order.objects.get(id = order_id)
        order_object.delete()
        messages.warning(request,"Product Deleted")
        return redirect('cart')
    else:
        return redirect('home')



































# def post(self, request):
#     serializer = User_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data["user"]
#     login(request, user)
#     token, created = Token.objects.get_or_create(user=user)
#     return Response({"token": token.key}, status=200, template_name="index.html")

# class logout_api(APIView):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     def post(self, request):
#         logout(request)
#         return Response(status=204)


# class add_to_cart(APIView):
#     # authentication_classes = [SessionAuthentication, ]
#     permission_classes = [AllowAny,]
#     def get(self, request):
#         serializer = add_to_cart_serializer(data=request.data)
#         print(request.data)
#         print(serializer)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.data)
#         # serializer.save()
