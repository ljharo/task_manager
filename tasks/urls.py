from django.urls import path

from .views import TaskView, StepView

urlpatterns = [
    path('create/', TaskView.as_view(), name='create_task')
]