from django.urls import path

from .views import LogView 

urlpatterns = [
    path('log/register/', LogView.as_view(), name="register"),
    path('log/update/', LogView.as_view(), name="update")
]