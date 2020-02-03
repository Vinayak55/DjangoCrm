
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('',views.logout,name="logout"),
    path('chart/',views.chartdemo,name='chart'),
    path('home/',views.dashboard,name="dashboard"),
    path('addsupplier/', views.addsupplier, name='add-supplier'),
    path('order/',views.order,name="Order-place"),
    path('payment/',views.payment,name="payment-form"),
    path('email/', views.email, name='email'),
    path('orderdelete/<int:id>', views.deleteorder, name='delete-order'),

    path('paymentdelete/<int:id>', views.deletepayment, name='delete-payment'),
    path('notification/<int:id>', views.notification, name='notification'),
    path('ordernotification/<int:id>', views.Ordernotification, name='Ordernotification'),
    path('paymentnotification/<int:id>', views.paymentnotification, name='paymentnotification'),


    path('supplierDetails/<int:id>', views.supplierdetails, name='details-supplier'),
    path('update/<int:id>', views.update,name="update-supplier"),
    path('delete/<int:id>', views.delete,name="delete-supplier"),
    
    path('invoice', views.Invoicepage,name="invoice"),
    path('allorders/', views.allorders, name="all-orders"),
    path('allpayment/', views.allpayments, name="all-payment"),

    # path('addMsupplier/', views.addMsupplier, name='add-Msupplier'),
    # path('Morder/',views.Morder,name='MOrder-place'),
    # path('allMorders/', views.allMorders, name="all-Morders"),
    # path('Mpayment/',views.Mpayment,name="Mpayment-form"),


]
