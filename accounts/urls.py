
from django.urls import path
from .views import UserLogout
from .views import UserRegistrationView, UserLoginView,ProfileView
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile' ),
]