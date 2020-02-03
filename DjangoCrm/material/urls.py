from django.urls import path
from . import views

urlpatterns = [

    path('addMsupplier/', views.addMsupplier, name='add-Msupplier'),
    path('Morder/', views.Morder, name='MOrder-place'),
    path('allMorders/', views.allMorders, name="all-Morders"),
    path('Mpayment/', views.Mpayment, name="Mpayment-form"),
    path('Minvoice', views.Invoicepage,name="Minvoice"),
]