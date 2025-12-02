from django.shortcuts import render,redirect
from .forms import UserForm, ProfileForm, ProductForm, CartForm, OrderForm,LoginForm
from .models import User,Profile,Product,Cart,Order
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if not username or not email or not password or not confirmPassword:
                return HttpResponse('ALL FIELDS ARE REQUIRED !!!')
    
        if password != confirmPassword:
                return HttpResponse("Passwords don't match!")
    
        if User.objects.filter(username=username).exists():
                return HttpResponse("Username already taken!")
    
        user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name,
                last_name=surname
            )
        return redirect ('login')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            return redirect('product-list')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')

def logout_profile(request):
    logout(request)
    return redirect('login')

class ProfileListView(ListView):
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all()


def profile_update_view(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "❌ Вы не вошли в систему! Пожалуйста, выполните вход.")
        return redirect('login')
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})


def profile_detail(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "❌ Вы не вошли в систему! Пожалуйста, выполните вход.")
        return redirect('login')

    profile = Profile.objects.get(id=pk)
    return render(request, 'profile_detail.html', {'profile': profile})

def profile_delete_view(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "❌ Вы не вошли в систему! Пожалуйста, выполните вход.")
        return redirect('login')
    profile = Profile.objects.filter(id=pk).first()
    if not profile:
        return HttpResponse(f"Profile with id {pk} not found")
    if request.method == "GET":
        return render(request, "profile_confirm_delete.html", context={"profile":profile})
    elif request.method == "POST":
        profile.delete()
        return redirect("profile-list")

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('product-list')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('product-list')

def product_delete_view(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "❌ Вы не вошли в систему! Пожалуйста, выполните вход.")
        return redirect('login')
    product = Product.objects.filter(id=pk).first()
    if not product:
        return HttpResponse(f"Product with id {pk} not found")
    if request.method == "GET":
        return render(request, "product_confirm_delete.html", context={"product":product})
    elif request.method == "POST":
        product.delete()
        return redirect("product-list")




def cart_list(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        return render(request, 'cart_list.html', {'carts': carts})
    else:
        return redirect('register')

            
    
class CartCreateView(CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'cart_create.html'
    success_url = reverse_lazy('cart-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart_detail.html'

class CartUpdateView(UpdateView):
    model = Cart
    form_class = CartForm
    template_name = 'cart_create.html'
    success_url = reverse_lazy('cart-list')

class CartDeleteView(DeleteView):
    model = Cart
    template_name = 'cart_confirm_delete.html'
    success_url = reverse_lazy('cart-list')    

class OrderCreateView(CreateView):
    model = Order
    fields = [] 
    template_name = 'order_create.html'
    success_url = reverse_lazy('order-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)

        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity

        if cart_items.exists():
            form.instance.user = user
            form.instance.total_amount = total
            form.instance.status = 'в обработке'
            response = super().form_valid(form)
            cart_items.delete()
            return response
        else:
            return redirect('cart-list')



class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order-list')

def order_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "❌ Ошибка: вы не вошли в систему!")
        return redirect('register')  

    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})

    
