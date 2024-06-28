from django.urls import path

from .views import TaskView, StepView

urlpatterns = [
    path('create/', TaskView.as_view(), name='create_task'),
    path('get/<int:id>', TaskView.as_view(), name='get_task'),
    path('update/', TaskView.as_view(), name='update_task'),
    path('delete/<int:id>', TaskView.as_view(), name='delete_task')
]