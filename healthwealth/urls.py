from django.urls import path
from .views import LoginView, RegistrationView, EditUserView, ListDocumentView, AddDocumentAccessView, UploadDocumentView

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path('user/', EditUserView.as_view()),
    path("upload/", UploadDocumentView.as_view()),
    path("documents/", ListDocumentView.as_view()),
    path("documents/access/", AddDocumentAccessView.as_view()),
]
