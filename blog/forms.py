from django import forms
from .models import BlogPost, Comment, Reply # Make sure to import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cellphone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ("username" , "email", "cellphone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Since User model doesn't have cellphone field, we need to save it separately
            user.profile.cellphone = self.cleaned_data["cellphone"]
            user.profile.save()
        return user

# ... other forms ...

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','author_name','against', 'content', 'province', 'suburb', 'incident_date', 'file1', 'file2', 'file3', 'file4', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descriptive Title'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name '}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us what happened'}),
            'against': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Who wronged you?'}),
            'suburb': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter suburb'}),
            'incident_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_name'].required = False
        self.fields['file1'].required = False
        self.fields['file2'].required = False
        self.fields['file3'].required = False
        self.fields['file4'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...', 'class': 'form-control'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your reply here...', 'class': 'form-control'}),
        }

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profession']
        


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15, required=False)
    profession = forms.CharField(max_length=15, required=False )

    class Meta:
        model = User
        fields = ['username','first_name' ,'profession', 'email', 'phone_number', 'password1', 'password2']
        