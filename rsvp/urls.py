from django.urls import path
from . import views

urlpatterns = [
    path('', views.rsvp_entry_point, name='rsvp'),
    # path('start/', views.rsvp_start, name='rsvp_start'),
    path('confirm/<int:guest_id>/', views.confirm_guest, name='confirm_guest'),
    path('confirm/<int:guest_id>/attending/', views.rsvp_confirm_attendance, name='rsvp_confirm_attendance'),
    path('confirm/<uuid:group_id>/attending/', views.confirm_group_attendance, name='confirm_group_attendance'),
    path('questions/<int:guest_id>/yes/', views.rsvp_questions_yes, name='rsvp_questions_yes'),
    path('questions/<int:guest_id>/no/', views.rsvp_questions_no, name='rsvp_questions_no'),
    path('group-questions/<uuid:group_id>/', views.group_rsvp_questions, name='group_rsvp_questions'),
    path('group-declined/<uuid:group_id>/', views.group_declined, name='group_declined'),
    path('group-thank-you/<uuid:group_id>/', views.group_thank_you, name='group_thank_you'),
]