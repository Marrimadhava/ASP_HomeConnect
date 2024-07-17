from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm, PropertyForm, InquiryForm, ReviewForm, LoginForm
from .models import Property, Inquiry, Review, CustomUser, PropertyPurchaser, Salesperson
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Property

def home(request):
    query = request.GET.get('query', '')
    if query:
        properties = Property.objects.filter(
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        properties = Property.objects.all()
    
    user_role = request.user.user_role if request.user.is_authenticated else None
    
    return render(request, 'home.html', {
        'properties': properties,
        'user_role': user_role
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('home')  # Redirect to home after login
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')  # Redirect to home after logout

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                if user.user_role == 'property_purchaser':
                    PropertyPurchaser.objects.create(
                        user=user,
                        phone_number='1234567890',  # Placeholder values
                        specialties='Residential',  # Placeholder values
                        service_areas='New York'  # Placeholder values
                    )

                login(request, user)
                messages.success(request, 'Successfully signed up!')
                return redirect('home')  # Redirect to home after signup
            except IntegrityError:
                messages.error(request, 'Username already exists. Please choose a different username.')
        else:
            messages.error(request, 'Failed to sign up. Please check the form for errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'profile.html', {'user': user})

@login_required
def create_property(request):
    if request.user.user_role != 'property_purchaser':
        return HttpResponseForbidden("You are not allowed to add properties.")

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.property_purchaser = PropertyPurchaser.objects.get(user=request.user)
            property_instance.save()
            messages.success(request, 'Property created successfully!')
            return redirect('property_list')
    else:
        form = PropertyForm()

    return render(request, 'create_property.html', {'form': form})


@login_required
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})

@login_required
def property_detail(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property_instance})


@login_required
def create_inquiry(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.client = request.user
            inquiry.property = property_instance
            inquiry.save()
            messages.success(request, 'Inquiry created successfully!')
            return redirect('inquiry_list')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form.')
    else:
        form = InquiryForm()
    return render(request, 'create_inquiry.html', {'form': form, 'property': property_instance})

@login_required
def inquiry_list(request):
    if request.user.user_role == 'salesperson':
        inquiries = Inquiry.objects.all()  # Fetch all inquiries for salespeople
    else:
        inquiries = Inquiry.objects.filter(client=request.user)  # Fetch only client's inquiries for clients
    return render(request, 'inquiry_list.html', {'inquiries': inquiries})


@login_required
def inquiry_detail(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    if request.user.user_role != 'salesperson' and request.user != inquiry.client:
        return HttpResponseForbidden("You are not allowed to view this inquiry.")

    if request.method == 'POST' and request.user.user_role == 'salesperson':
        response = request.POST.get('response', '')
        inquiry.response = response
        inquiry.status = 'Closed'
        inquiry.save()
        messages.success(request, 'Inquiry has been responded to and closed successfully!')
        return redirect('inquiry_list')

    return render(request, 'inquiry_detail.html', {'inquiry': inquiry})


@login_required
def create_review(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = request.user
            review.property = property_instance
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('property_detail', property_id=property_id)
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'property': property_instance})

@login_required
def review_list(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    reviews = Review.objects.filter(property=property_instance)
    return render(request, 'review_list.html', {'property': property_instance, 'reviews': reviews})
@login_required
def review_list(request):
    if request.user.user_role in ['salesperson', 'property_purchaser']:
        reviews = Review.objects.filter(property_purchaser__user=request.user)
    else:
        reviews = Review.objects.filter(client=request.user)
    return render(request, 'review_list.html', {'reviews': reviews})

def search(request):
    query = request.GET.get('query', '')
    price = request.GET.get('price', None)
    category = request.GET.get('category', None)
    filters = Q()
    if query:
        filters &= Q(address__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
    if price:
        filters &= Q(price__lte=price)
    if category:
        filters &= Q(category__icontains=category)
    
    properties = Property.objects.filter(filters) if filters else Property.objects.none()
    return render(request, 'search.html', {'properties': properties, 'query': query})

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', user_id=user.id)
        else:
            messages.error(request, 'Failed to update profile. Please check the form for errors.')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'update_profile.html', {'form': form})


@login_required
def promote_property(request, property_id):
    if request.user.user_role != 'salesperson':
        return HttpResponseForbidden("You are not allowed to promote properties.")
    
    property_instance = get_object_or_404(Property, id=property_id)
    share_url = request.build_absolute_uri(property_instance.get_absolute_url())
    share_text = f"Check out this property: {property_instance.address} - {share_url}"
    
    return render(request, 'promote_property.html', {'property': property_instance, 'share_text': share_text})



@login_required
def property_purchaser_reviews(request):
    if request.user.user_role != 'property_purchaser':
        return HttpResponseForbidden("You are not allowed to view this page.")

    property_purchaser = get_object_or_404(PropertyPurchaser, user=request.user)
    reviews = Review.objects.filter(property__property_purchaser=property_purchaser)
    return render(request, 'property_purchaser_reviews.html', {'reviews': reviews})