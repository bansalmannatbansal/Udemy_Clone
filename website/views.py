from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Course


def home(request):
    categories = Category.objects.all()
    featured_courses = Course.objects.all()[:4]
    context = {"categories": categories, "featured_courses": featured_courses}
    return render(request, "home.html", context)


def courses(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")

    course_list = Course.objects.all()
    selected_category = None

    if category_slug:
        course_list = course_list.filter(category__slug=category_slug)
        selected_category = Category.objects.filter(slug=category_slug).first()

    if query:
        course_list = course_list.filter(title__icontains=query)

    context = {
        "courses": course_list,
        "categories": Category.objects.all(),
        "selected_category": selected_category,
        "query": query,
    }
    return render(request, "courses.html", context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    related_courses = Course.objects.filter(category=course.category).exclude(id=course.id)
    context = {"course": course, "category": course.category, "related_courses": related_courses}
    return render(request, "course_detail.html", context)


PLANS = [
    {
        "name": "Personal Plan",
        "audience": "For you",
        "size": "Individual",
        "icon": "person",
        "price": "Starting at ₹500.00/month",
        "billing": "Billed monthly or annually. Cancel anytime.",
        "button": "Start subscription",
        "features": [
            "Access to 28,000+ top courses",
            "Certification prep",
            "Goal-focused recommendations",
            "AI-powered coding exercises",
        ],
    },
    {
        "name": "Team Plan",
        "audience": "For your team",
        "size": "2 to 50 people",
        "icon": "team",
        "price": "₹2,000.00 a month per user",
        "billing": "Billed annually. Cancel anytime.",
        "button": "Start subscription",
        "features": [
            "Access to 13,000+ top courses",
            "Certification prep",
            "Goal-focused recommendations",
            "AI-powered coding exercises",
            "Analytics and adoption reports",
        ],
    },
    {
        "name": "Enterprise Plan",
        "audience": "For your whole organization",
        "size": "More than 20 people",
        "icon": "team",
        "price": "Contact sales for pricing",
        "billing": "",
        "button": "Request a demo",
        "features": [
            "Access to 30,000+ top courses",
            "Certification prep",
            "Goal-focused recommendations",
            "AI-powered coding exercises",
            "Advanced analytics and insights",
            "Dedicated customer success team",
            "International course collection featuring 15 languages",
            "Customizable content",
            "Hands-on tech training with add-on",
        ],
    },
]


def pricing(request):
    return render(request, "pricing.html", {"plans": PLANS})


def signup_view(request):
    errors = {}
    full_name = ""
    email = ""

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if full_name == "":
            errors["full_name"] = "This field is required."

        if email == "":
            errors["email"] = "This field is required."
        else:
            try:
                validate_email(email)
                if User.objects.filter(username=email).exists():
                    errors["email"] = "An account with this email already exists."
            except ValidationError:
                errors["email"] = "Enter a valid email address."

        if password == "":
            errors["password"] = "This field is required."
        else:
            try:
                validate_password(password)
            except ValidationError as error:
                errors["password"] = " ".join(error.messages)

        if confirm_password == "":
            errors["confirm_password"] = "This field is required."
        elif password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if len(errors) == 0:
            User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,
            )
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
        messages.error(request, "Please correct the errors below.")

    context = {"errors": errors, "full_name": full_name, "email": email}
    return render(request, "signup.html", context)


def login_view(request):
    email = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if email == "" or password == "":
            messages.error(request, "Please enter your email and password.")
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect("home")
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html", {"email": email})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("home")
