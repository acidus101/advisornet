from django.urls import path
from django.urls.resolvers import URLPattern
from .api import RegisterAPI, LoginAPI, UserAPI, LogoutAPI, AdvisorsViewAPI, MakeBookingApi, ViewBookingsAPI

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('user', UserAPI.as_view()),
    path('logout', LogoutAPI.as_view()),
    path('<int:user_id>/advisor', AdvisorsViewAPI.as_view()),
    path('<int:user_id>/advisor/<int:advisor_id>', MakeBookingApi.as_view()),
    path('<int:user_id>/advisor/booking', ViewBookingsAPI.as_view()),
]
