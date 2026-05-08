from django import forms
from .models import Review, Profile, Book, DiscussionPost
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]
        widgets = {
            "rating" : forms.Select(choices=[(i, i) for i in range(1, 6)]),
            "content": forms.Textarea(attrs={"rows":4 , "placeholder" : "Share your thoughts ❤️" }),
        }




class  UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        




class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birthday', 'profile_picture']



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'cover',
            'month',
            'is_current'
        ]




class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['content']