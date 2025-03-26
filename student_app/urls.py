from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),  # Home page or Student List page
    # Student URLs
    path('students/create/', views.create_student, name='create_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),  # New detail view
    path('students/export/', views.export_students, name='export_students'),
    path('students/import/', views.import_students, name='import_students'),

    # Subject URLs
    path('subjects/create/', views.create_subject, name='create_subject'),
    path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subject/export/', views.export_subjects, name='export_subjects'),
    path('subject/import/', views.import_subjects, name='import_subjects'),


]
