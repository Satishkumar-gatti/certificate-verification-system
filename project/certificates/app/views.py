import hashlib
from django.shortcuts import redirect, render, HttpResponse
from .models import User, Certificate


# Home Page
def home(request):
    return render(request, 'home.html')


# Register Page
def register(request):
    if request.method == "POST":
        name = request.POST['name'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        role = request.POST['role'].strip()

        # Empty Fields Check
        if not name or not email or not password or not role:
            return render(request, 'register.html', {
                'error': 'All fields are required!'
            })

        # Already Exists Check
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already registered!'
            })

        if User.objects.filter(name=name).exists():
            return render(request, 'register.html', {
                'error': 'Username already taken!'
            })

        # Save User
        User.objects.create(
            name=name,
            email=email,
            password=password,
            role=role
        )

        return render(request, 'register.html', {
            'message': 'Registered Successfully ✅'
        })

    return render(request, 'register.html')


# Login Page
def login(request):
    if request.method == "POST":
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        if not email or not password:
            return render(request, 'login.html', {
                'error': 'Please enter email and password!'
            })

        user = User.objects.filter(email=email, password=password).first()

        if user:
            if user.role == 'student':
                return render(request, 'student/dashboard.html', {'user': user})

            elif user.role == 'college':
                return render(request, 'college/dashboard.html', {'user': user})

            elif user.role == 'company':
                return render(request, 'company/dashboard.html', {'user': user})

        return render(request, 'login.html', {
            'error': 'Invalid Login Details!'
        })

    return render(request, 'login.html')


# Generate Hash
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


# Add Certificate
def add_certificate(request):
    if request.method == "POST":
        name = request.POST['name'].strip()
        course = request.POST['course'].strip()
        grade = request.POST['grade'].strip()
        issued_by = request.POST['issued_by'].strip()

        if not name or not course or not grade or not issued_by:
            return HttpResponse("❌ All fields required")

        student = User.objects.filter(name=name, role='student').first()

        if not student:
            return HttpResponse("❌ Student not found")

        data = student.name + course + grade + issued_by
        cert_hash = generate_hash(data)

        Certificate.objects.create(
            student=student,
            course=course,
            grade=grade,
            issued_by=issued_by,
            certificate_hash=cert_hash
        )

        return HttpResponse("✅ Certificate Added Successfully")

    return render(request, 'college/add_certificate.html')


# Verify Certificate
def verify_certificate(request):
    if request.method == "POST":
        name = request.POST['name'].strip()
        course = request.POST['course'].strip()
        grade = request.POST['grade'].strip()
        issued_by = request.POST['issued_by'].strip()

        if not name or not course or not grade or not issued_by:
            return HttpResponse("❌ All fields required")

        data = name + course + grade + issued_by
        new_hash = generate_hash(data)

        cert = Certificate.objects.filter(
            certificate_hash=new_hash
        ).first()

        if cert:
            return HttpResponse("✅ Certificate is VALID")
        else:
            return HttpResponse("❌ Certificate is FAKE")

    return render(request, 'company/verify.html')


# About Page
def about(request):
    return render(request, 'about.html')


# Logout
def logout(request):
    return redirect('/')