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
        print(f"Register form posted: {request.POST.get('email')}")
        
        if form.is_valid():
            print("Form is valid, saving user...")
            try:
                user = form.save()
                print(f"User created: {user.id} - {user.username}")
                
                # Optional: Auto-login user after registration
                # request.session['user_id'] = user.id
                # return redirect("/dashboard")
                
                return render(request, 'login.html', {'success': "Registration successful. Please login."})
            except Exception as e:
                print(f"User save error: {e}")
                return render(request, 'register.html', {'error': f"Registration failed: {str(e)}"})
        else:
            error_message = form.errors.as_text()
            print(f"Form errors: {error_message}")
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    context = {}
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"Login attempt: email={email}")
        
        try:
            # Try to authenticate with the username first
            user = authenticate(request, username=email, password=password)
            
            # If that fails, try with email as username
            if user is None:
                # Get user by email
                try:
                    user_obj = User.objects.get(email=email)
                    user = authenticate(request, username=user_obj.username, password=password)
                    print(f"Authenticated with email: {email}")
                except User.DoesNotExist:
                    user = None
                    print(f"No user found with email: {email}")
            
            if user is not None:
                login(request, user)
                print(f"User logged in: {user.username}, ID: {user.id}")
                
                # Store both user_id and user_email in session
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                
                return redirect('dashboard')
            else:
                print("Authentication failed")
                context['error'] = 'Invalid email or password'
        except Exception as e:
            print(f"Login error: {str(e)}")
            context['error'] = 'An error occurred during login'
    
    return render(request, 'login.html', context)

# Custom decorator to handle both standard and custom auth
def custom_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Skip Django's standard authentication
        # as it's causing issues with MongoDB
        user_id = None
        user_email = None
        
        # Try to get ID from our custom session
        try:
            user_id = request.session.get('user_id')
        except:
            pass
        
        # Try to get email from our custom session
        try:
            user_email = request.session.get('user_email')
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
        
        # If we have a user email, try to get the user by email
        if user_email:
            try:
                user = User.objects.get(username=user_email)
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

def admin_view(request):
    """Admin view to list all users - for debugging only"""
    # For security in production, you should restrict this to admin users
    # This is just for debugging purposes
    
    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
        })
    
    # Add authentication debugging
    debug_info = {
        'session_keys': list(request.session.keys()),
        'user_id_in_session': request.session.get('user_id'),
        'django_auth_user_id': request.session.get(SESSION_KEY),
    }
    
    return render(request, 'admin_view.html', {
        'users': user_list,
        'debug_info': debug_info,
        'user_count': len(user_list)
    })
