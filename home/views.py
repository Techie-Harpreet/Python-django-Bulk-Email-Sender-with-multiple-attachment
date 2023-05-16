from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
import pandas as pd
from django.core.mail import send_mass_mail   
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import authenticate,  login, logout

def Home(request):
    return render(request , 'index.html')

@login_required(login_url='/login')
def Bulk_mail_send(request):  
        
  if request.method == "POST" and request.FILES['myfile']:
        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        try :
            data = pd.read_csv('media/'+filename)

        except :
            data = pd.read_excel('media/'+filename)


        filter_data = list(data['Emails'])
        
        subject = request.POST["subject"]
        mailbody = request.POST["mailbody"]

   

        mail = EmailMessage(
                  subject,
                  mailbody,
                  settings.EMAIL_HOST_USER,
                  filter_data,
                  )
        
        files= request.FILES.getlist("attach")

        for file in files:
           mail.attach(file.name, file.read(), file.content_type)
                
        mail.send()
        messages.success(request, 'Mail Sent Successfully')


        return redirect(request.META['HTTP_REFERER'])
  
  return render(request, 'bulk-mail.html')





@login_required(login_url='/login')
def Single_mail_send(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        k = email.split(',')
        subject = request.POST["subject"]
        mailbody = request.POST["mailbody"]
        mail = EmailMessage(subject,
                  mailbody,
                  settings.EMAIL_HOST_USER,
                  k,
                  )
        
        files= request.FILES.getlist("attach")
        for file in files:
           mail.attach(file.name, file.read(), file.content_type)
                
        mail.send()
        messages.success(request, 'Mail Sent Successfully')

        return redirect(request.META['HTTP_REFERER'])
    
    return render(request, 'single-mail.html')
    


def register_page(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already exist')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create( email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'Successfully Register' , extra_tags='register')

        return redirect('/login')

    
    return render(request ,'register.html')



def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Invalid email and password' , extra_tags='login-error')





        user_obj = authenticate(username = email , password = password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')
            
        return HttpResponseRedirect(request.path_info)
    return render(request ,'login.html')




def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')