from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import BuisnessForm
from .models import Buisness
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings

from email.mime.base import MIMEBase # New line
from email import encoders # New line
from email.mime.text import MIMEText
from email.utils import formataddr
from django.core.mail import send_mail

@login_required
def submitBusinessForm(request):
    if request.method == 'POST':
        b_form = BuisnessForm(request.POST, request.FILES)
        if(b_form.is_valid()):
            b_form.save()
            name = b_form.cleaned_data.get('name')
            order = Buisness.objects.filter(name = name).last()
            order_id  = order.id               
            id = b_form.cleaned_data.get("id")
            name = b_form.cleaned_data.get('name')
            reciever_email = request.POST.get('email_field')
            
            image_dr = request.POST.get('myImage')
            address = request.POST.get('address_field')
            phone_number = request.POST.get('phoneNumber')
            ordered_date = b_form.cleaned_data.get('ordered_date')
            

            #medicine_name = request.POST.get('medicine_name')
            #medicine_qty = request.POST.get('medicine_qty')           
            #medicine_mg = request.POST.get('medicine_mg')

            medical_details = request.POST.get('medical_details')
            
            sender_name = 'NewDoonChemist'
            sender_email = settings.EMAIL_HOST_USER
            reciever_name = name

            flag = 0
            

            try:
                file = request.FILES['myImage']
                #print(file.name)
                #print(file.size)
                #print(file.content_type)
                
              
            except Exception as e:
                flag=1
                print(f"Could not retrive image file\n{e}")
            
            print(sender_email)
        
            msg_to =formataddr((reciever_name, reciever_email))
            msg_from = formataddr((sender_name, sender_email))

            msg = MIMEText('<h3 style="display:inline;">Order has been placed By : </h3>'+'<span style="color:black;">' + name + '</span><br>' 
            +'<h3 style="display:inline;">Order Id : </h3>'+'<span style="color:black;">' +str(order_id) +'</span><br>'+
            '<h3 style="display:inline;">Address : </h3>'+'<span style="color:black;">'+str(address)+'</span><br>' +
            '<h3 style="display:inline;">Phone Number : </h3>'+'<span style="color:black;">' +str(phone_number) +'</span><br>'+
            '<h3 style="display:inline;">Ordered Date : </h3>'+'<span style="color:black;">' +str(ordered_date) +'</span><br>'+
            '<h3 style="display:inline;">Addition Things(Medicine Name, Medicine quantity and Medicine Power(mg) respectively) : </h3><br>' + str(medical_details),_subtype='html')

            subject = 'A New Order has been Placed!'

            try:
                server = EmailMessage(subject, None ,to=[msg_from],from_email=msg_from)
                if flag == 0:
                    server.attach(file.name, file.read(), file.content_type)
                server.attach(msg)
                server.send(fail_silently=True)
                
            except Exception as e:
                print(f'Ohh No! Something went wrong while sending email!\n{e}')
                return render(request, 'main/mail_not_send.html')
            
            subject_1 = 'Your Order has been Placed!'
            msg_1 = MIMEText('<p>Your Order has been confirmed!<br>Your Order Id : '+ str(order_id)+'<br>Your Order Will be delivered within 2 to 6 hours<br>Thankyou for using our service.</p>' ,_subtype='html')
            try:
                server_1 = EmailMessage(subject_1, None ,to=[msg_to],from_email=msg_from)
                server_1.attach(msg_1)
                server_1.send(fail_silently=True)
                
            except Exception as e:
                print(f'Ohh No! Something went wrong while sending email!\n{e}')
                return render(request, 'main/mail_not_send.html')
        
            messages.success(request, f'Your Order has been successfullt placed!!!')
            return render(request, 'main/order_placed.html',{'order_id' : order_id})

        else:
            messages.warning(request, f'Something went wrong, Please check your email!!!')
    else:
        b_form = BuisnessForm
    context = {
    'b_form':b_form
    }
    return render(request, 'main/index.html', context)
