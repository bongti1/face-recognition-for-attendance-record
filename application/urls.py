from django.urls import path
from . import views
urlpatterns = [
    path('', views.Dashboard, name='Dashboard'),
    path('create_student/', views.Create_student, name='Create_student'),
    path('student/', views.Retrieve_student, name='Retrieve_student'),
    path('register/', views.Register, name= 'Register'),
    path("login/", views.Login, name='Login'),
    path("logout/", views.LogOut, name="Logout"),
    path("profile/", views.Profile, name="Profile"),
    path("vedio_stream/", views.FaceRecognition, name="Vedio_Stream"),
    path("create_student/training_model/", views.Loading, name="Loading"),
    path("create_student/dataset/", views.CreateDataset, name="CreateDataset"),
    path("student/edit/<int:pk>", views.Update_student, name="Update_student"),
    path("student/delete/<int:pk>", views.Delete_student, name="Delete_student")
]
