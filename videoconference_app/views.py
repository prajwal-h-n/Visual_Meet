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
            # Store user info in session the simplest way possible
            try:
                # Store user ID in our custom session key
                request.session['user_id'] = user.id
                
                # Skip Django's standard login as it's problematic with MongoDB
                # Manually add the signal for compatibility with other code
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                
                # Redirect the user after login
                return redirect("/dashboard")
            except Exception as e:
                # If something went wrong, log it and show a friendly message
                print(f"Login error: {e}")
                return render(request, 'login.html', {'error': "Login failed. Please try again."})
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

# Custom decorator to handle both standard and custom auth
def custom_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Skip Django's standard authentication
        # as it's causing issues with MongoDB
        user_id = None
        
        # Try to get ID from our custom session
        try:
            user_id = request.session.get('user_id')
        except:
            pass
            
        # Try to get ID from Django's session
        try:
            session_key = request.session.get(SESSION_KEY)
            # Handle 'None' string value
            if session_key == 'None':
                session_key = None
            if session_key and str(session_key).isdigit():
                user_id = int(session_key)
        except:
            pass
        
        # If we have a user ID, try to get the user
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
