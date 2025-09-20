from django import forms
from .models import User,Profile,Product,Cart,Order

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit = True):
      user = super().save(commit=False)
      user.set_password(self.cleaned_data['password'])
      if commit:
          user.save()
      return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Enter username')
    password = forms.CharField(widget=forms.PasswordInput,label='Enter password')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo', 'bio']

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image']

class CartForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = []