from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Certificate
import hashlib


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 📝 REGISTER
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'User already exists'})

        User.objects.create(name=name, email=email, password=password, role=role)
        return redirect('login')

    return render(request, 'register.html')


# 🔐 LOGIN
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            request.session['role'] = user.role

            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'college':
                return redirect('college_dashboard')
            elif user.role == 'company':
                return redirect('company_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# 🎓 ADD CERTIFICATE (NO LOGIN REQUIRED)
def add_certificate(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course = request.POST.get('course')
        grade = request.POST.get('grade')
        issued_by = request.POST.get('issued_by')

        student = User.objects.filter(name=name, role='student').first()

        if not student:
            return render(request, 'college/add_certificate.html', {'error': 'Student not found'})

        data = name + course + grade + issued_by
        cert_hash = hashlib.sha256(data.encode()).hexdigest()

        Certificate.objects.create(
            student=student,
            course=course,
            grade=grade,
            issued_by=issued_by,
            certificate_hash=cert_hash
        )

        return render(request, 'college/add_certificate.html', {'success': True})

    return render(request, 'college/add_certificate.html')


# ✅ VERIFY CERTIFICATE (NO LOGIN REQUIRED)
def verify_certificate(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course = request.POST.get('course')
        grade = request.POST.get('grade')
        issued_by = request.POST.get('issued_by')

        data = name + course + grade + issued_by
        new_hash = hashlib.sha256(data.encode()).hexdigest()

        cert = Certificate.objects.filter(certificate_hash=new_hash).first()

        if cert:
            return render(request, 'company/verify.html', {'verified': True, 'cert': cert})
        else:
            return render(request, 'company/verify.html', {'error': True})

    return render(request, 'company/verify.html')


# 🎓 STUDENT DASHBOARD
def student_dashboard(request):
    user_id = request.session.get('user_id')
    name = request.session.get('name')

    certificates = Certificate.objects.filter(student_id=user_id)

    return render(request, 'student/dashboard.html', {
        'name': name,
        'certificates': certificates
    })


# 🏫 COLLEGE DASHBOARD
def college_dashboard(request):
    name = request.session.get('name')
    return render(request, 'college/dashboard.html', {'name': name})


# 🏢 COMPANY DASHBOARD
def company_dashboard(request):
    name = request.session.get('name')
    return render(request, 'company/dashboard.html', {'name': name})


# 🚪 LOGOUT
def logout(request):
    request.session.flush()
    return redirect('login')