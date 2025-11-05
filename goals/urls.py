"""
URLs for Goals app.
"""

from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list, name='list'),
    path('create/', views.goal_create, name='create'),
    path('<int:pk>/', views.goal_detail, name='detail'),
    path('<int:pk>/edit/', views.goal_edit, name='edit'),
    path('<int:pk>/delete/', views.goal_delete, name='delete'),
    path('<int:pk>/replicate/', views.goal_replicate, name='replicate'),

    # Templates
    path('templates/', views.template_marketplace, name='templates'),

    # Milestones
    path('<int:goal_pk>/milestones/create/', views.milestone_create, name='milestone_create'),
    path('milestones/<int:pk>/complete/', views.milestone_complete, name='milestone_complete'),

    # Actions
    path('milestones/<int:milestone_pk>/actions/create/', views.action_create, name='action_create'),
    path('actions/<int:pk>/complete/', views.action_complete, name='action_complete'),
]
