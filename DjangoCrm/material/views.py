from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from newprintpress import settings
# from .filters import orderFilter
from printapp.filters import orderFilter
from .models import Msupplier, MOrder, MPayment
from .forms import MorderForm, MpaymentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .filters import orderFilter
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


@login_required(login_url='login')
def addMsupplier(request):
    if request.method == "POST":
        Name = request.POST['name']
        Company = request.POST['company']
        Mobile = request.POST['mobile']
        Address = request.POST['address']

        if Msupplier.objects.filter(Name=Name).exists():
            return render(request, "addsupplier.html", {'error': "user Name already Exist Please use another name"})

        else:
            Msupplier.objects.create(Name=Name, Mobile=Mobile, Company=Company, Address=Address)
            # supplier1.save()
            messages.success(request, 'Supplier as been successfully Created .')
            return redirect("dashboard")


    else:
        return render(request, "addMsupplier.html")



@login_required(login_url='login')
def Morder(request):
    if request.method == 'POST':

        form = MorderForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Order Please successfully .')
            form.save()
            return redirect('dashboard')
    else:
        supplier1 = Msupplier.objects.all()
        form = MorderForm()
        content = {'form': form, 'supplier': supplier1}
        return render(request, "MOrderform.html", content)


@login_required(login_url='login')
def Mpayment(request):
    if request.method == 'POST':
        form = MpaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:

        form = MpaymentForm()
        content = {'form': form}
        return render(request, "Mpaymentform.html", content)

def allMorders(request):
    order_table = MOrder.objects.all()
    # order_count = order_table.count()
    # order_amount = list(Order.objects.aggregate(Sum('Amount')).values())[0]
    # order_table = Order.objects.all().order_by('-id')
    # order_filter = orderFilter(request.GET, queryset=order_list)
    payment_table = MPayment.objects.all().order_by('-id')
    # Payment_filter = paymentFilter(request.GET, queryset=payment_list)

    context = {

        'filter': order_table,
        'filter2': payment_table,
    }
    return render(request, 'AllMorder.html', context)


def Invoicepage(request):
    order_list = MOrder.objects.all()
    order_filter = orderFilter(request.GET, queryset=order_list)
    try:
        if request.method == "POST":
            supplierid = request.POST['supplierName']
            Date = request.POST['Date']
            start_date = request.POST['Datefrom']
            end_date = request.POST['Dateto']

            sName = Msupplier.objects.all().get(id=supplierid)

            today = timezone.now()
            if Date:
                Damount = MOrder.objects.all().filter(supplierName_id=supplierid, Date=Date)
                Camount = MPayment.objects.all().filter(Msupplier_id=supplierid, Date=Date)
            elif start_date:
                if end_date:
                    Damount = MOrder.objects.all().filter(supplierName_id=supplierid, Date__gte=start_date,
                                                            Date__lte=end_date)
                    Camount = MPayment.objects.all().filter(Msupplier_id=supplierid, Date__gte=start_date,
                                                            Date__lte=end_date)
                else:
                    end_date = datetime.date.today()
                    Damount = MOrder.objects.all().filter(supplierName_id=supplierid, Date__gte=start_date,
                                                            Date__lte=end_date)
                    Camount = MPayment.objects.all().filter(Msupplier_id=supplierid, Date__gte=start_date,
                                                            Date__lte=end_date)

            else:
                Damount = MOrder.objects.all().filter(supplierName_id=supplierid)
                Camount = MPayment.objects.all().filter(Msupplier_id=supplierid)

            Dcount = Damount.count()
            Ccount = Camount.count()

            if Dcount == 0 or Ccount == 0:
                if Dcount == 0 and Ccount != 0:
                    debit_amount = 0
                    credit_amount = list(Camount.aggregate(Sum('Amount')).values())[0]
                    pflag = False
                elif Dcount != 0 and Ccount == 0:
                    debit_amount = list(Damount.aggregate(Sum('Amount')).values())[0]
                    credit_amount = 0
                    oflag = False
                else:
                    credit_amount = 0
                    debit_amount = 0
                    pflag = False
                    oflag = False
            else:
                credit_amount = list(Camount.aggregate(Sum('Amount')).values())[0]
                debit_amount = list(Damount.aggregate(Sum('Amount')).values())[0]

            balance_amount = debit_amount - credit_amount

            context = {
                    'filter': Damount,
                    'filter1': Camount,

                    'sname': sName,
                    'today': today,
                    'debit_amount': debit_amount,
                    'credit_amount': credit_amount,
                    'balance_amount': balance_amount,

                }
            return render(request, 'invoice.html', context)
    except:
        messages.error(request, 'Please select the Service provider Name before clicking Search .')
        return redirect("Minvoice")

    context = {

        'filter': order_filter,

    }
    return render(request, 'Minvoicefilter.html', context)







