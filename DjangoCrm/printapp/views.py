from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from newprintpress import settings
from .models import supplier ,Order ,Payment,Balance,attachments
from .forms import supplierForm,orderForm,paymentForm,EmailForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum,Q
from .filters import supplierFilter,orderFilter ,paymentFilter,BalanceFilter
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver
import datetime
from django.core.files import File
#  django.core.files.File
from .signals import send_mail1


def chartdemo(request):
    pass
    
def Invoicepage(request):
    
    order_list = Order.objects.all()
    order_filter = orderFilter(request.GET, queryset=order_list)
    try:
        if request.method == "POST":
            supplierid=request.POST['supplierName']
            Date = request.POST['Date']
            start_date=request.POST['Datefrom']
            end_date =request.POST['Dateto']
            
            sName = supplier.objects.all().get(id=supplierid)
                
            today =timezone.now()
            if Date:
                Damount = Order.objects.all().filter(supplierName_id=supplierid,Date=Date)
                Camount = Payment.objects.all().filter(supplierName_id=supplierid,Date=Date)
            elif start_date:
                if end_date:
                    Damount = Order.objects.all().filter(supplierName_id=supplierid,Date__gte=start_date,Date__lte=end_date)
                    Camount = Payment.objects.all().filter(supplierName_id=supplierid,Date__gte=start_date,Date__lte=end_date)
                else:
                    end_date =datetime.date.today()
                    Damount = Order.objects.all().filter(supplierName_id=supplierid,Date__gte=start_date,Date__lte=end_date)
                    Camount = Payment.objects.all().filter(supplierName_id=supplierid,Date__gte=start_date,Date__lte=end_date)
            
            else:
                Damount = Order.objects.all().filter(supplierName_id=supplierid)
                Camount = Payment.objects.all().filter(supplierName_id=supplierid)
        
            
            Dcount =Damount.count()
            Ccount =Camount.count()

            
            if Dcount == 0 or Ccount == 0:
                if Dcount == 0 and Ccount != 0:
                    debit_amount =0
                    credit_amount = list(Camount.aggregate(Sum('credit')).values())[0]
                    pflag =False
                elif  Dcount != 0 and Ccount == 0:
                    debit_amount = list(Damount.aggregate(Sum('Amount')).values())[0]
                    credit_amount = 0
                    oflag =False
                else:
                    credit_amount= 0
                    debit_amount = 0
                    pflag =False
                    oflag = False   
            else:
                credit_amount = list(Camount.aggregate(Sum('credit')).values())[0]
                debit_amount = list(Damount.aggregate(Sum('Amount')).values())[0]
                
            balance_amount =debit_amount - credit_amount
            balance_flag = False
            if balance_amount < 0:
                balance_amount =abs(balance_amount)
                balance_flag=True
        
            context = {
                'filter': Damount,
                'filter1': Camount,
                'balance_flag':balance_flag,
                'sname':sName,
                'today':today, 
                'debit_amount':debit_amount,
                'credit_amount':credit_amount,
                'balance_amount':balance_amount,
        
                    }    
            return render(request,'invoice.html',context)    
    except:
        messages.error(request, 'Please select the Service provider Name before clicking Search .')
        return redirect("invoice")
    
    context = {
    
            'filter': order_filter,
        
                }
    return render(request, 'invocefilter.html',context)

def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, 'Invalid user credentials')
            return render(request, "Loginform.html")
    else:
        return render(request, "Loginform.html")


def logout(request):
    auth.logout(request)
    return render(request, 'loginform.html')





@login_required(login_url='login')
def dashboard(request):
    supplier_table = supplier.objects.all()
    supplier_count = supplier_table.count()

    order_table = Order.objects.all().order_by('-id')[:5]
    order_count = Order.objects.all().count()
    order_amount = list(Order.objects.aggregate(Sum('Amount')).values())[0]
    if order_amount is None:
        order_amount=0
    payment_table = Payment.objects.all().order_by('-id')[:5]
    paid_amount = list(Payment.objects.aggregate(Sum('credit')).values())[0]
    if paid_amount is None:
        paid_amount=0
 
    # The aggregate() method returns a dictionary.
    # If you know you're only returning a single-entry dictionary you could use .values()[0].
    # https://stackoverflow.com/questions/19138609/django-aggreagtion-sum-return-value-only

    context = {
        'supplier_table': supplier_table,
        'supplier_count': supplier_count,
        'order_table': order_table,
        'order_count': order_count,
        'order_amount':order_amount,
        'payment_table' : payment_table,
        'paid_amount':paid_amount,

    }
    return render(request, 'dashboard.html', context)



@login_required(login_url='login')
def addsupplier(request):
    
    if request.method == "POST":
        Name = request.POST['name']
        Company = request.POST['company']
        Mobile = request.POST['mobile']
        Email = request.POST['email']
        Address = request.POST['address']

        if supplier.objects.filter(Name=Name).exists():
            return render(request, "addsupplier.html", {'error': "user Name already Exist Please use another name"})

        # elif supplier.objects.filter(Email=Email).exists():
        #     return render(request, "addsupplier.html", {'error': "Email already exist"})
        else :
            supplier.objects.create(Name=Name, Mobile=Mobile, Email=Email,Company=Company,Address=Address)
            # supplier1.save()
            messages.success(request, 'Supplier as been successfully Created .')
            return redirect("dashboard")


    else:
        return render(request, "addsupplier.html")


@login_required(login_url='login')
def update(request, id):
    supplier1 = supplier.objects.get(id=id)
    form = supplierForm(request.POST or None, instance=supplier1)
    if form.is_valid():
        form.save()
        messages.info(request, 'Supplier Details as been successfully Updated')
        return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'updateform.html', context)

@login_required(login_url='login')
def delete(request, id):
    supplier1 = supplier.objects.get(id=id)
    supplier1.delete()
    messages.warning(request, 'Supplier Details as been successful Deleted')
    return redirect("dashboard")

@login_required(login_url='login')
def deletepayment(request, id):
    payment = Payment.objects.get(id=id)
    payment.delete()
    messages.warning(request, 'Payment detailes  as been successful Deleted')
    return redirect("dashboard")

@login_required(login_url='login')
def deleteorder(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.warning(request, 'Order detailes  as been successful Deleted')
    return redirect("dashboard")



@login_required(login_url='login')
def notification(request, id):
    name = supplier.objects.get(id=id)
    func = 'delete-supplier'
    service ="Service provider"
    note ="Note :If you delete this service provider ,all Transaction Details will be Delete "
    context = { 'func':func,
                'name':name.Name,
                'id':id,
                'note' :note,
                'service':service,
               }
    return render(request,"deletenotification.html",context)


def Ordernotification(request, id):
    order = Order.objects.get(id=id)
    supplierid =order.supplierName_id
    func = 'delete-order'
    service ="Order Details of "
    name = supplier.objects.get(id=supplierid)

    context = { 'func' :func,
            'name':name,
                'id':id,
                'service':service,
               }
    return render(request,"deletenotification.html",context)

def paymentnotification(request, id):
    payment = Payment.objects.get(id=id)
    supplierid =payment.supplierName_id
    name = supplier.objects.get(id=supplierid)

    func = 'delete-payment'
    service ="Payment Details of "

    context = { 'func' :func,
                'name':name,
                'id':id,
                'service':service,
               }
    return render(request,"deletenotification.html",context)


@login_required(login_url='login')
def supplierdetails(request, id):
    supplier1 = supplier.objects.get(id=id)

    order_table=Order.objects.filter(supplierName_id=id)
    order_count = order_table.count()
    order_amount = list(order_table.aggregate(Sum('Amount')).values())[0]

    order_filter = orderFilter(request.GET, queryset=order_table)


    payment_table = Payment.objects.filter(supplierName_id=id)
    payment_count = payment_table.count()
    payment_filter = paymentFilter(request.GET, queryset=payment_table)
    pflag = True
    oflag = True
    
    if payment_count == 0 or order_count == 0:
        if payment_count == 0 and order_count != 0:
            paid_amount =0
            total_amount = list(order_table.aggregate(Sum('Amount')).values())[0]
            pflag =False
        elif  order_count == 0 and payment_count != 0:
            paid_amount = list(payment_table.aggregate(Sum('credit')).values())[0]
            total_amount = 0
            oflag =False
        else:
            paid_amount= 0
            total_amount = 0
            pflag =False
            oflag = False   
    else:
        paid_amount = list(payment_table.aggregate(Sum('credit')).values())[0]
        total_amount = list(order_table.aggregate(Sum('Amount')).values())[0]
        
        
    balance_amount =total_amount - paid_amount
    balance_flag = False
    if balance_amount < 0:
        balance_amount =abs(balance_amount)
        balance_flag=True
    
    context = {'supplier': supplier1,
               'order' :order_table,
               'order_count':order_count,
               'order_amount':order_amount,
               'filter': order_filter,
               'filter2': payment_filter,
               'balance_flag':balance_flag,
               'payment_table':payment_table,
               'total_amount':total_amount,
               'paid_amount':paid_amount,
               'payment_count':payment_count,
               'total_amount':total_amount,
               'balance_amount':balance_amount,
               'pflag':pflag,'oflag':oflag,}
    return render(request, 'supplierdetails.html', context)

@login_required(login_url='login')
def order(request):
    if request.method == 'POST':
        form = orderForm(request.POST, request.FILES)
        files = request.FILES.getlist('document') #field name in model
        ordername =request.POST['OrderName']
        mail_check =request.POST.getlist('sendMail')
        #  = len(send_mail)
        # return HttpResponse("send_mail {}".format(lenthg))

        
        print(send_mail)
        fileCount = len(files) #file count
        
        if form.is_valid():
            messages.success(request, 'Order Please successfully .')
            order_instance = form.save()
            if fileCount >=1:
                for i in files:
                    attachments.objects.create(order=order_instance,files =i)
        if len(mail_check) == 1 :
            post_save.connect(email, sender=attachments)
 
            # orders="helllo word "
            # send_mail1.send(sender=Order,order=orders)
           
            # return HttpResponse("send_mail {}".format(send_mail))
            # post_save.connect(email, sender=Order)
            
        return redirect('dashboard')
    else :
        supplier1 =supplier.objects.all()
        form = orderForm()
        content = {'form': form,'supplier':supplier1}
        return render(request, "orderForm.html",content)

     



# @receiver(post_save, sender=Order)
# def email(sender, instance, **kwargs):
#     # testint the instance value fetching
#     # message = str(instance.supplierName_id)+ str(instance.OrderName)+ str(instance.Quantity)+ str(instance.Amount)+ str(instance.Comment)
#     # attch = str(instance.document)
#     # print(type(instance.document)) files
#     # print(type(instance.OrderName)) str
#     # print("hello wolrd .............."+str(instance.id))
    
#     try:
    
#         email =supplier.objects.values('Email').get(id=instance.supplierName_id)
#         if email is not None:
#             email = supplier.objects.values_list('Email', flat=True).get(id=instance.supplierName_id)
#             subject =instance.OrderName
#             document = instance.document
#             print(instance.id)

#             files2 = attachments.objects.values_list('files', flat=True).filter(order=instance.id)
#             print(files2.count())
#             attach =' '
#             for i in files2:
#                 attach =' http://127.0.0.1:8000/media/'+str(i)
            
#             message = "Order Name : "+subject+ "\n Size :"+str(instance.Size)+ "\n GSM :"+str(instance.gsm) +"\n Quantity :"+str(instance.Quantity)+ "\n Amount :"+str(instance.Amount)+ "\n Note :"+ str(instance.Comment)+"Please Click on Below link to download attachment \n"+"\n \n"+' http://127.0.0.1:8000/media/'+str(document)+ "\n \n \n \n warm regards,\n Jagdamba \n Mobile No : 9260015600"+attach+str(files2 )
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [email]
#             email = EmailMessage(subject,message,email_from,recipient_list)
#             # print(document.file.size)
#             if document.file.size < 20971520:
#                 email.attach_file('media/'+str(document))
#             email.send()
#     except :
#         return HttpResponse("Unable to send the Email Please try Again ")

# @receiver(post_save, sender=attachments)
def email(sender, instance, **kwargs):

    
    # print(instance.order)
    # print(instance.order_id)
    # print(instance.id)
    try:
        orderdetails = Order.objects.get(id=instance.order_id)
        print(orderdetails)
        email = supplier.objects.values_list('Email', flat=True).get(id=orderdetails.supplierName_id)
        subject =orderdetails.OrderName
        document = instance.files
        # print(instance.id)

        files2 = attachments.objects.values_list('files', flat=True).filter(order=instance.order)
        print(files2.count())
        attach =' '
        for i in files2:
            # print("---------email2----------------------------")
            # print(i)
            attach +='\n http://127.0.0.1:8000/media/'+str(i)
                
        # message = ' http://127.0.0.1:8000/media/'+str(document)     
        message = "Order Name : "+subject+ "\n Size :"+str(orderdetails.Size)+ "\n GSM :"+str(orderdetails.gsm) +"\n Quantity :"+str(orderdetails.Quantity)+ "\n Amount :"+str(orderdetails.Amount)+ "\n Note :"+ str(orderdetails.Comment)+"Please Click on Below link to download attachment \n"+"\n \n"+attach+ "\n \n \n \n warm regards,\n Jagdamba \n Mobile No : 9260015600"
            
        # message = "attachment = "+attach
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject,message,email_from,recipient_list)
        if document.file.size < 20971520:
            for i in files2:
                email.attach_file('media/'+str(i))
        email.send()
            # return HttpResponse("Unable to send the Email Please try Again ")
    except:
        return HttpResponse("<h3>Sorry ,Unable to send Email . Please Try Again </h3>")

@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else :

  
  
  
  
  
  
  
  
  
  
  
  
  
        form = paymentForm()
        content = {'form': form}
        return render(request, "paymentform.html",content)


# Testing 

# @receiver(post_save, sender=Order)
# def Damount(sender, instance, **kwargs):
#     supplierName = instance.supplierName
#     # print(supplierName)
#     Damount = instance.Amount
#     Date = instance.Date
#     Amount = instance.Amount + 0
#     Balance.objects.create(supplierName=supplierName,Date=Date, debit=Damount,Amount=Amount)



# @receiver(post_save, sender=Payment)
# def Camount(sender, instance, **kwargs):
#     supplierName = instance.supplierName
#     # print(supplierName)
#     Amount = instance.credit
#     Date = instance.Date

#     Balance.objects.create(supplierName=supplierName,Date=Date, credit=Amount)




def allorders(request):
    order_table = Order.objects.all()
    # order_count = order_table.count()
    # order_amount = list(Order.objects.aggregate(Sum('Amount')).values())[0]
    order_list = Order.objects.all().order_by('-id')
    order_filter = orderFilter(request.GET, queryset=order_list)
    context = {

        'filter': order_filter,
    }
    return render(request, 'Allorders.html', context)


def allpayments(request):
    
    # payment_table = Payment.objects.all()
    # payment_count = payment_table.count()
    # payment_amount = list(Payment.objects.aggregate(Sum('credit')).values())[0]
    payment_list = Payment.objects.all().order_by('-id')
    Payment_filter = paymentFilter(request.GET, queryset=payment_list)
    context = {

        'filter2': Payment_filter,
    }
    return render(request, 'Allpayment.html', context)






