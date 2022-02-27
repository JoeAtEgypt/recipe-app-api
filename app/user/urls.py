from django.urls import path

from . import views


# we can define our app name and the app name is
# set to help identify which app we're creating the URL from when we use our reverse function
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
