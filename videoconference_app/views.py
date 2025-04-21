from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User

# These constants are used for session handling
SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Custom login to avoid the MongoDB update issue
            try:
                # Set the backend attribute if it's not set
                if not hasattr(user, 'backend'):
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                
                # Add the user's ID to the session
                request.session[SESSION_KEY] = user.id
                # Add the backend to the session
                if hasattr(user, 'backend'):
                    request.session[BACKEND_SESSION_KEY] = user.backend
                
                # Django's signal to indicate login
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                
                # Redirect the user after login
                return redirect("/dashboard")
            except Exception as e:
                # Fall back to standard login if custom approach fails
                try:
                    login(request, user)
                    return redirect("/dashboard")
                except:
                    # Last resort: just set session directly
                    request.session['user_id'] = user.id
                    return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

# Custom decorator to handle both standard and custom auth
def custom_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check for standard authentication
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        
        # Check for our custom authentication
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                # Add user to request
                request.user = user
                return view_func(request, *args, **kwargs)
            except User.DoesNotExist:
                pass
        
        # User not authenticated, redirect to login
        return redirect("/login")
    return wrapped_view

@custom_login_required
def dashboard(request):
    # Get user info
    if hasattr(request, 'user') and request.user.is_authenticated:
        first_name = request.user.first_name
    else:
        # Fallback for custom auth
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                first_name = user.first_name
            except:
                first_name = "User"
        else:
            first_name = "User"
            
    return render(request, 'dashboard.html', {'name': first_name})

@custom_login_required
def videocall(request):
    # Get user info for full name
    if hasattr(request, 'user') and request.user.is_authenticated:
        full_name = request.user.first_name + " " + request.user.last_name
    else:
        # Fallback for custom auth
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                full_name = user.first_name + " " + user.last_name
            except:
                full_name = "User"
        else:
            full_name = "User"
            
    return render(request, 'videocall.html', {'name': full_name})

@custom_login_required
def logout_view(request):
    # Clear all session data
    request.session.flush()
    logout(request)
    return redirect("/login")

@custom_login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')
