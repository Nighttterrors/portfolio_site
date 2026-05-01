from django.contrib import admin
from .models import Book, Review, Profile

admin.site.register(Book)
admin.site.register(Review)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "isApproved", "createdAt")
    list_filter = ("isApproved",)
    search_fields = ("user__username", "user__email")

