from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from userauths.models import User, Profile
from userauths.forms import ProfileForm
from django.contrib import messages
from core.models import Application
from dashboard.forms import ResultForm, CheckResult
from dashboard.models import Result
from dashboard.models import Session
import uuid, requests
from django.conf import settings
from dashboard.models import AcceptancePayment, SchoolFeePayment, HostelPayment

# Create your views here.

@login_required
def dashboard(request):
    if request.user.user_type != 'teacher':
        return redirect('dashboard:stu_dashboard')
    
    teacher_student = request.user.profile.faculty
    admissions = Application.objects.filter(course__faculty=teacher_student, status="Accepted")
    accepted_students_count = Application.objects.filter(status='Accepted', course__faculty=teacher_student).count()
    pending_students_count = Application.objects.filter(status='Pending', course__faculty=teacher_student).count()
    rejected_students_count = Application.objects.filter(status='Rejected', course__faculty=teacher_student).count()
    total_students_count = Application.objects.filter(course__faculty=teacher_student).count()
    
    
    if total_students_count > 0:
        rejected_percentage = (rejected_students_count / total_students_count) * 100
        pending_percentage = (pending_students_count / total_students_count) * 100
    else:
        rejected_percentage = 0
        
    if total_students_count > 0:
        accepted_percentage = (accepted_students_count / total_students_count) * 100
    else:
        accepted_percentage = 0
        
    
    context = {
        "admissions":admissions,
        'accepted_students_count': accepted_students_count,
        "pending_students_count": pending_students_count,
        "rejected_students_count": rejected_students_count,
        "rejected_percentage":rejected_percentage,
        "accepted_percentage":accepted_percentage,
        "pending_percentage":pending_percentage
    }
    return render(request, "dashboard/index.html", context)

@login_required
def admissions(request):
    teacher_student = request.user.profile.faculty
    admissions = Application.objects.filter(course__faculty=teacher_student, status="Accepted")
    accepted_students_count = Application.objects.filter(status='Accepted', course__faculty=teacher_student).count()
    pending_students_count = Application.objects.filter(status='Pending', course__faculty=teacher_student).count()
    rejected_students_count = Application.objects.filter(status='Rejected', course__faculty=teacher_student).count()
    total_students_count = Application.objects.filter(course__faculty=teacher_student).count()
    
    
    if total_students_count > 0:
        rejected_percentage = (rejected_students_count / total_students_count) * 100
        pending_percentage = (pending_students_count / total_students_count) * 100
    else:
        rejected_percentage = 0
        
    if total_students_count > 0:
        accepted_percentage = (accepted_students_count / total_students_count) * 100
    else:
        accepted_percentage = 0
    
    

    
    context = {
        "admissions":admissions,
        'accepted_students_count': accepted_students_count,
        "pending_students_count": pending_students_count,
        "rejected_students_count": rejected_students_count,
        "rejected_percentage":rejected_percentage,
        "accepted_percentage":accepted_percentage,
        "pending_percentage":pending_percentage
    }
    return render(request, "dashboard/admissions.html", context)

@login_required
def teacherprofile(request):
    
    
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("dashboard:profile")
    else:
        form = ProfileForm(instance=profile, user=request.user)
        
    if request.user.user_type != 'teacher':
        application = Application.objects.get(email=request.user.email)
        
    context = {
        "form":form,
        "profile":profile,
    }
    
    if request.user.user_type != 'teacher':
        try:
            application = Application.objects.get(email=request.user.email)
            context["application"] = application
        except Application.DoesNotExist:
            pass  # Optional: Handle missing application gracefully
    return render(request, "dashboard/teacherprofile.html", context)



@login_required
def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST, teacher=request.user)
        if form.is_valid():
            result = form.save(commit=False)
            result.added_by = request.user  # teacher
            result.save()
            messages.success(request, "Result added successfully!")
            return redirect('dashboard:results')  # update with your own
    else:
        form = ResultForm(teacher=request.user)

    return render(request, 'dashboard/add_result.html', {'form': form})

@login_required
def results(request):
    
    result = Result.objects.all()
    
    context = {
        'result':result
    } 
    return render(request, "dashboard/results.html", context)

@login_required
def edit_result(request, pk):
    result = get_object_or_404(Result, pk=pk, added_by=request.user)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result, teacher=request.user)
        
        if form.is_valid():
            new_form  = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Results Updated successfully")
            return redirect("dashboard:results")
        
    else:
        form = ResultForm(instance=result, teacher=request.user)
        
    context = {
        'form':form
    }
    
    return render(request, "dashboard/edit_result.html", context)

def delete_result(request, pk):
    result = get_object_or_404(Result, pk=pk, added_by=request.user)
    result.delete()
    messages.success(request, "Result has been deleted successfully")
    return redirect("dashboard:results")
    


################# student dashboard #####################


def student_dashboard(request):
    
    return render(request, "dashboard/student_dashboard.html")

@login_required
def pay_fees(request):
    sessions = Session.objects.all()
    context ={
        'sessions':sessions
    }
    return render(request, "dashboard/pay_fees.html", context)

FEE_AMOUNTS = {
    'acceptance': 50000,
    'school_fees': 80000,
    'hostel': 60000,
    
}



@login_required
def review_payment(request):
    if request.method == 'POST':
        session_name = request.POST.get('session')
        payment_type = request.POST.get('payment_type')

        if not session_name or not payment_type:
            messages.error(request, "Please select both session and payment type.")
            return redirect('dashboard:pay_fees')

        try:
            session = Session.objects.get(name=session_name)
        except Session.DoesNotExist:
            messages.error(request, "Selected session does not exist.")
            return redirect('dashboard:pay_fees')

        # Check if user already paid
        if payment_type == "acceptance":
            if AcceptancePayment.objects.filter(student=request.user, session=session, is_paid=True).exists():
                messages.warning(request, f"You have already paid Acceptance Fee for {session.name}.")
                return redirect('dashboard:pay_fees')

        elif payment_type == "school_fees":
            if SchoolFeePayment.objects.filter(student=request.user, session=session, is_paid=True).exists():
                messages.warning(request, f"You have already paid School Fees for {session.name}.")
                return redirect('dashboard:pay_fees')

        amount = FEE_AMOUNTS.get(payment_type)
        request.session['payment_session'] = session.name
        request.session['payment_type'] = payment_type

        context = {
            "session": session.name,
            "payment_type": payment_type.replace('_', ' ').title(),
            "amount": amount,
            "user": request.user,
        }
        return render(request, 'dashboard/review_payment.html', context)

    return redirect('dashboard:pay_fees')

    
@login_required
def process_flutterwave_payment(request):
    payment_type = request.session.get('payment_type')
    session_name = request.session.get('payment_session')
    amount = FEE_AMOUNTS.get(payment_type)

    if not payment_type or not session_name or not amount:
        return redirect('dashboard:pay_fees')

    session = Session.objects.get(name=session_name)
    tx_ref = str(uuid.uuid4())

    payload = {
        "tx_ref": tx_ref,
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": request.build_absolute_uri('/dashboard/payment/callback/'),
        "payment_options": "card",
        "customer": {
            "email": request.user.email,
            "name": request.user.get_full_name()
        },
        "customizations": {
            "title": "School Payment",
            "description": f"{payment_type.replace('_', ' ').title()} for {session}"
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
    data = response.json()

    if data.get("status") == "success":
        return redirect(data["data"]["link"])

    return redirect("dashboard:pay_fees")


@login_required
def flutterwave_callback(request):
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    # Fallback response
    if status != 'successful':
        return render(request, "dashboard/payment_failed.html", {
            "message": "Payment was not successful.",
            "tx_ref": tx_ref,
        })

    # Check if we already recorded this payment
    if AcceptancePayment.objects.filter(tx_ref=tx_ref).exists() or SchoolFeePayment.objects.filter(tx_ref=tx_ref).exists() or HostelPayment.objects.filter(tx_ref=tx_ref).exists():
        return render(request, "dashboard/payment_success.html", {
            "message": "Payment already recorded.",
            "tx_ref": tx_ref
        })

    # Re-fetch session and type from session variables
    session_name = request.session.get("payment_session")
    payment_type = request.session.get("payment_type")

    if not session_name or not payment_type:
        return render(request, "dashboard/payment_success.html", {
            "message": "Payment processed, but session data expired.",
            "tx_ref": tx_ref
        })

    try:
        session = Session.objects.get(name=session_name)
    except Session.DoesNotExist:
        return render(request, "dashboard/payment_failed.html", {
            "message": "Session not found.",
            "tx_ref": tx_ref
        })

    amount = FEE_AMOUNTS.get(payment_type)

    # Create appropriate payment record
    if payment_type == "acceptance":
        AcceptancePayment.objects.create(
            student=request.user,
            session=session,
            amount_paid=amount,
            is_paid=True,
            tx_ref=tx_ref
        )
    elif payment_type == "school_fees":
        SchoolFeePayment.objects.create(
            student=request.user,
            session=session,
            amount_paid=amount,
            is_paid=True,
            tx_ref=tx_ref
        )
    elif payment_type == "hostel":
        HostelPayment.objects.create(
            student=request.user,
            session=session,
            amount_paid=amount,
            is_paid=True,
            tx_ref=tx_ref
        )

    # Clean up session variables
    request.session.pop("payment_session", None)
    request.session.pop("payment_type", None)

    return render(request, "dashboard/payment_success.html", {
        "message": "Payment successful!",
        "payment_type": payment_type.replace("_", " ").title(),
        "amount": amount,
        "tx_ref": tx_ref
    })


@login_required
def check_result(request):
    if request.method == 'POST':
        form = CheckResult(request.POST)
        if form.is_valid():
            session = form.cleaned_data['session'].id
            semester = form.cleaned_data['semester'].id

            return redirect('dashboard:result_page', session_id=session, semester_id=semester)
    else:
        form = CheckResult()

    return render(request, "dashboard/check_result.html", {'form': form})
  
        
        
@login_required
def my_result(request, session_id, semester_id):
    profile = Profile.objects.get(user=request.user)
    
    try:
        result = Result.objects.get(
            student=request.user,
            session_id=session_id,
            semester_id=semester_id
        )
    except Result.DoesNotExist:
        messages.error(request, "Result not found for the selected session and semester.")
        return redirect('dashboard:check_result')

    # Process results_detail into a list of (subject, grade) pairs
    result_lines = []
    for line in result.results_detail.splitlines():
        if " - " in line:
            subject, grade = line.split(" - ")
            result_lines.append((subject.strip(), grade.strip()))

    context = {
        'result': result,
        'result_lines': result_lines,
        'profile': profile
    }
    return render(request, 'dashboard/result_page.html', context)

def Hostel(request):
    sessions = Session.objects.all()
    context ={
        'sessions':sessions
    }
    return render(request, "dashboard/hostel.html", context)


def rev_hostelpay(request):
    if request.method == 'POST':
        session_name = request.POST.get('session')
        payment_type = request.POST.get('payment_type')
        
        if not session_name or not payment_type:
            messages.error(request, "Please select both session and payment type.")
            return redirect('dashboard:hostel')
        
        try:
            session = Session.objects.get(name=session_name)
        except Session.DoesNotExist:
            messages.error(request, "Selected session does not exist.")
            return redirect('dashboard:hostel')
        
        if payment_type == "hostel":
            if HostelPayment.objects.filter(student=request.user, session=session, is_paid=True).exists():
                messages.warning(request, f"You have already paid School Fee for {session.name}.")
                return redirect("dashboard:hostel")
            
        amount = FEE_AMOUNTS.get(payment_type)
        request.session['payment_session'] = session.name
        request.session['payment_type'] = payment_type
        
        context = {
            "session": session.name,
            "payment_type": payment_type.replace('_', ' ').title(),
            "amount": amount,
            "user": request.user,
        }
        return render(request, 'dashboard/review_hostelpayment.html', context)

    return redirect('dashboard:hostel')