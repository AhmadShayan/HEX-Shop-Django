from .forms import RegistrationForm
from .models import Account
from carts.views import _cart_id, merge_session_cart

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from urllib.parse import urlparse, parse_qs



def _free_username(email):
    """The part of the address before the @, with a number added when someone already has it."""
    base = email.split('@')[0][:40] or 'user'
    username, n = base, 1
    while Account.objects.filter(username=username).exists():
        n += 1
        username = f'{base}{n}'
    return username


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = _free_username(email)
    
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            #USER_ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()            
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:  
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(request, email=email, password=password)
        
        if user is not None:
            # Must happen before auth.login, which changes the session key the visitor's basket is filed under.
            merge_session_cart(_cart_id(request), user)
            auth.login(request, user)
            messages.success(request, 'Logged In Successfully')
            referer = request.META.get('HTTP_REFERER', '')
            next_page = parse_qs(urlparse(referer).query).get('next', [''])[0]
            # Only a page on this site: an address like https://elsewhere.example or //elsewhere.example is never followed.
            if next_page and url_has_allowed_host_and_scheme(
                    next_page, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_page)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated Successfully')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    from orders.models import Order, OrderProduct
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    order_count = orders.count()
    context = {
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'accounts/dashboard.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        user = Account.objects.filter(email__exact=email).first()
        if user is not None:
            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            EmailMessage(mail_subject, message, to=[email]).send()
        # The same answer for every address, so the form cannot be used to find out who has an account.
        messages.success(request, 'If an account exists for that address, a password reset email has been sent.')
        return redirect('login')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.filter(pk=uid).first() if uid else None
            if user is None:
                messages.error(request, 'This reset link is missing or has expired.')
                return redirect('forgotPassword')
            user.set_password(password)
            user.save()
            del request.session['uid']
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')