from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None 
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User 
        fields = ['username','first_name','last_name','email']

class CustomChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None 
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean_new_password2(self) -> str:
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn’t match.")
        return password2      