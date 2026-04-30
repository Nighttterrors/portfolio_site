from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]
        widgets = {
            "rating" : forms.Select(choices=[(i, i) for i in range(1, 6)]),
            "content": forms.Textarea(attrs={"rows":4 , "placeholder" : "Share your thoughts ❤️" }),
        }
