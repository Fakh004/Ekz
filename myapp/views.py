from django.shortcuts import render,redirect
from .forms import UserForm, ProfileForm, ProductForm, CartForm, OrderForm,LoginForm
from .models import User,Profile,Product,Cart,Order
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    user_form = UserForm()
    return render(request,'register.html',{'user_form':user_form})

def login(request):
    form = LoginForm(request.POST or None)
    context = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('product-list')
            else:
                context = 'Неправильный логин или пароль'
                return render(request,'login.html',{'context':context})
        form = LoginForm()
    return render(request,'login.html',{'form':form,'context':context})


class ProfileListView(ListView):
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all()


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('product-list')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile



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

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-list')




class CartListView(ListView):
    model = Cart
    template_name = 'cart_list.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
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



class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_create.html'
    success_url = reverse_lazy('order-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order-list')
    
