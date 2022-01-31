from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_plan/', views.create_plan, name='create_plan'),
    path("single_plan/<int:id>", views.single_plan, name="single_plan"),
    path("edit_plan/<str:id>", views.edit_plan, name="edit_plan"),
    path("delete_plan/<str:id>", views.delete_plan, name="delete_plan"),
    path('<str:id>/create_cost/', views.create_cost, name='create_cost'),
    path('edit_cost/<str:id>', views.edit_cost, name='edit_cost'),
    path('delete_cost/<str:id>', views.delete_cost, name='delete_cost'),
    path('<str:id>/generated_link', views.generated_link, name='generated_link'),
    path('home/', views.index, name='')

]
