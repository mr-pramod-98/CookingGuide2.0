from django.urls import path
from . import views


urlpatterns = [
    # MAKE "index" PAGE OF THE "cook" APP AS THE MAIN PAGE
    path('', views.index, name="index"),
    path('cook_guide/<str:username>/', views.cook_guide, name="cook_guide"),
    path('cook_guide/<str:username>/delete/<str:title>/', views.delete, name="delete_item"),
    path('cook_guide/<str:username>/delete_account/', views.delete_account, name="delete_account"),
]
