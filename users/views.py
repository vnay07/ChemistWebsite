from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from . forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def activation_sent_view(request):
    return render(request, 'users/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return redirect('profile')
    else:
        return render(request,'users/activation_invalid.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            to_email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
        
            #sending confirmation mail
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Thankyou for Joining New Doon Medical. Verify Your account!!'
            message = render_to_string('users/acc_active_email.html',{
                'user': user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : account_activation_token.make_token(user),
            })
            
            msg= EmailMessage(mail_subject, message ,to=[to_email])
            msg.send(fail_silently=True)
            return redirect('activation_sent')
            
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html",{"form":form} )

@login_required
def profile(request):
    if request.method == 'POST':
        
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if  p_form.is_valid():
            
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            print("wrong happened") 
            return render(request, 'users/wrongPhoneNumber.html')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)



