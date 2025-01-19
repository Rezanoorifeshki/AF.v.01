from django import forms
from .models import CostomUser
import re
from django.core.exceptions import ValidationError

class CostomUserForm(forms.ModelForm):
    address=forms.CharField(max_length=500,label="آدرس")
    current_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="رمز عبور فعلی")
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="رمز عبور جدید")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="تایید رمز عبور جدید")

    class Meta:
        model=CostomUser
        fields = ['first_name', 'last_name', 'email', 'phonenumber', 'postalcode', 'address']
        
    def clean(self):
        cleaned_data = super().clean() 
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        phonenumber=cleaned_data.get('phonenumber')
        postalcode=cleaned_data.get('postalcode')
        address = cleaned_data.get('address')

        if not first_name:
            self.add_error('first_name', 'لطفاً نام خود را وارد کنید.')
        if not last_name:
            self.add_error('last_name', 'لطفاً نام خانوادگی خود را وارد کنید.')
        if not email:
            self.add_error('email', 'لطفاً ایمیل خود را وارد کنید.')
        if not phonenumber:
            self.add_error('phonenumber', 'لطفاً شماره تماس خود را وارد کنید.')
        if not postalcode:
            self.add_error('postalcode', 'لطفاً کد پستی خود را وارد کنید.')
        if not address:
            self.add_error('address', 'لطفاً آدرس خود را وارد کنید.')

        password = cleaned_data.get("new_password")  
        confirm_password = cleaned_data.get("confirm_password") 

        if (password and password != confirm_password):  
            self.add_error("confirm_password", "رمز عبور جدید و تایید رمز عبور باید یکسان باشند.")  

        if (password):
            if len(password) < 8:  
                 self.add_error("new_password", "رمز عبور باید حداقل 8 کاراکتر باشد.")
            if not re.findall('[A-Z]', password): 
                self.add_error("new_password", "رمز عبور باید حداقل یک حرف بزرگ داشته باشد.")
            if not re.findall('[a-z]', password):  
                self.add_error("new_password", "رمز عبور باید حداقل یک حرف کوچک داشته باشد.")
            if not re.findall('[0-9]', password): 
                self.add_error("new_password", "رمز عبور باید حداقل یک عدد داشته باشد.")
            if not re.findall('[!@#$%^&*(),.?\":{}|<>]', password): 
                self.add_error("new_password", "رمز عبور باید حداقل یک نماد خاص داشته باشد.")

        return cleaned_data  