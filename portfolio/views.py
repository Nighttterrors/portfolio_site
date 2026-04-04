from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.contrib import messages
from django.urls import reverse


# Create your views here.

def home(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Save message to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            fullMessage = f"""
                Message from: {name}
                Email: {email}
                {message}
                """  
            print(fullMessage)       

            try:
                print("About to send email...")
                send_mail(
                    subject="Portfolio Contact Form",
                    message = fullMessage,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["diegosalvadorgutierrez@outlook.com"],
                    fail_silently=False,
                )
                print("Email sent successfully")
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, "Your message was sent succesfully!😍")

            url = reverse("home") + "#contact"
            return redirect(url)
            

    else:
        form = ContactForm()
    return render(request, "portfolio/index.html", {"form":form})

