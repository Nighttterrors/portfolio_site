from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.contrib import messages


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

            try:

                send_mail(
                    subject="Portfolio Contact Form",
                    message = fullMessage,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["diegosalvadorgutierrez@outlook.com"],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, "Your message was sent succesfully!")
            return redirect("home") ##todo :  fix this redirect to show success message without refreshing the page

    else:
        form = ContactForm()
    return render(request, "portfolio/index.html", {"form":form})

