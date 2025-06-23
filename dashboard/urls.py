from django.urls import path
from dashboard import views

app_name = "dashboard"

urlpatterns =[
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.teacherprofile, name="profile"),
    path("admissions/", views.admissions, name="admissions"),
    path("add_result/", views.add_result, name="add_results"),
    path("results/", views.results, name="results"),
    path('edit-product/<pk>', views.edit_result, name='edit_result'),
    path('delete/<pk>', views.delete_result, name='delete_result'),
    
    
    
    ######### student url ########
    
    path("student", views.student_dashboard, name="stu_dashboard"),
    path("fees/", views.pay_fees, name="pay_fees"),
    path('pay/review/', views.review_payment, name='review_payment'),
    path('pay/flutterwave/', views.process_flutterwave_payment, name='process_flutterwave_payment'),
    path('payment/callback/', views.flutterwave_callback, name='flutterwave_callback'),
    path('check-results/', views.check_result, name='check_result'),
    path('my-result/<int:session_id>/<int:semester_id>/', views.my_result, name='result_page'),
    path('hostel/', views.Hostel, name='hostel'),
    path('pay/review/', views.rev_hostelpay, name='review_hostel'),
    

    

    
    
    
    
    
]