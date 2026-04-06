from datetime import datetime, date

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from myapp.models import *


def main(request):
    # dd = User.objects.all()
    # for i in dd:
    #     i.set_password("admin")
    #     print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
    #     i.save()
    return render(request,"login.html")


def logout(request):

    return render(request,"login.html")

def login_get(request):
    # dd = User.objects.all()
    # for i in dd:
    #     i.set_password("admin")
    #     print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
    #     i.save()
    if request.method=="POST":
        username=request.POST["username"]
        password = request.POST["password"]
        print((username,password))
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.groups.filter(name="Agency").exists():
                login(request,user)
                return redirect('/myapp/home/')
            # elif user.groups.filter(nme="Expert").exists():
            #     login(request,user)
            #     return redirect('/myapp/viewusers/')
        else:
            return redirect('/myapp/main/')
    return redirect('/myapp/main/')


def home(request):
    return render(request,"homepage.html")


def add_caretaker(request):
    return render(request, "Agency/add_caretaker.html")

def add_caretaker_post(request):
    photo = request.FILES['photo']
    name=request.POST['name']
    gender=request.POST['gender']
    dob = request.POST['dob']
    Qualification = request.POST['qualification']
    email = request.POST['email']
    phone = request.POST['phone']
    status = request.POST['status']
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.create(username=username,
        password=make_password(password),
        email=email,
        first_name=request.POST.get('name')
    )
    user.save()
    user.groups.add(Group.objects.get(name='Caretaker'))


    ob=caretaker_table()
    ob.name=name
    ob.image = photo
    ob.gender = gender
    ob.qualification = Qualification
    ob.dob = dob
    ob.email = email
    ob.phone = phone
    ob.status = 'pending'
    ob.LOGIN=user
    ob.save()

    return redirect('/myapp/view_request_assigned/')


def edit_caretaker(request,id):
    request.session['id']=id
    b=caretaker_table.objects.get(id=id)
    return render(request,"Agency/edit_caretaker.html",{'data':b})

def edit_caretaker_post(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    Qualification = request.POST['qualification']
    email = request.POST['email']
    phone = request.POST['phone']
    status = request.POST['status']

    ob = caretaker_table.objects.get(id=request.session['id'])


    ob.name = name
    if 'image' in request.FILES:
        image=request.FILES['image']
        ob.image=image
        ob.save()

    ob.gender = gender
    ob.qualification = Qualification
    ob.dob = dob
    ob.email = email
    ob.phone = phone
    ob.status = status
    ob.save()

    return redirect('/myapp/view_request_assigned/')

    # user = User.objects.create(
    #     username=username,
    #     password=make_password('password'),
    #     email=email,
    #     first_name=request.POST.get('name')
    # )

def delete_caretaker(request,id):
    ob=caretaker_table.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/view_request_assigned/')




def send_reply(request,id):
    request.session['cid']=id
    return render(request, "Agency/send_reply.html")
def send_reply_post(request):
    reply=request.POST['reply']
    a=complaint_table.objects.get(id=request.session['cid'])
    a.reply=reply
    a.save()
    return redirect('/myapp/view_complaint_send_reply/')
def view_complaint_send_reply(request):
    a=complaint_table.objects.all()
    return render(request, "Agency/view_complaint_send_reply.html",{"data":a})

def view_request_assigned(request):
    a=caretaker_table.objects.all()
    return render(request, "Agency/view_request_assigned.html",{'data':a})

def view_request_for_caretaker(request):

    data = request_table.objects.all()
    caretakers = caretaker_table.objects.filter(status='active')  # Only available caretakers
    return render(request, "Agency/view req.html", {"data": data, "caretakers": caretakers})


from django.shortcuts import redirect
from .models import request_table, caretaker_table, assigned_caretaker_table
from django.utils import timezone


def assign_caretaker(request, id):
    if request.method == "POST":
        caretaker_id = request.POST.get("caretaker_id")

        # Fetch request and caretaker
        req = request_table.objects.get(id=id)
        caretaker = caretaker_table.objects.get(id=caretaker_id)

        # Update request status
        req.reply = "assigned"
        req.save()

        # Update caretaker status
        caretaker.status = "busy"
        caretaker.save()

        # Insert into assigned_caretaker_table
        assigned_caretaker_table.objects.create(
            REQUEST=req,
            CARETAKER=caretaker,
            date=req.date,
            time=req.time,
            status="assigned"  # or "pending", depending on your logic
        )

        return redirect('/myapp/view_request_for_caretaker/')


        ##################flutter####################

def loginpost(request):
    username=request.POST['username']
    print(username)
    password=request.POST['password']
    print(password)
    u=authenticate(request,username=username,password=password)
    print(u,"lllllllllllllllllll")
    if u is not None:
        if u.groups.filter(name='User').exists():
            # print('1111111')
            login(request,u)
            return JsonResponse({"status":"ok",'lid': u.id,'type':'user'})
        elif u.groups.filter(name='Caretaker').exists():
            login(request,u)
            return JsonResponse({"status":"ok",'lid': u.id,'type':'Caretaker'})

        else:
            return JsonResponse({"status":"no"})
    print('errrrrrrr')
    return JsonResponse({"status":"no"})

def view_aasigned_user(request):
    lid=request.POST['lid']
    a=assigned_caretaker_table.objects.filter(LOGIN_id=lid)
    l=[]
    for i in a:
        l.append({"id":str(i.id),"request":i.REQUEST.PATIENT.USER.name,"date":str(i.date),"time":str(i.time),"status":i.status})
    return JsonResponse({"status":"ok","data":l})

def pill_reminder(request):
    uid=request.POST['lid']
    medical_name=request.POST['medical_name']
    time=request.POST['time']
    frequency=request.POST['frequency']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']

    a=pill_reminder_table()
    a.medical_name=medical_name
    a.time=time
    a.frequency=frequency
    a.start_date=start_date
    a.end_date=end_date
    a.USER_id=uid
    a.status='remind'
    a.save()
    return JsonResponse({"status":"ok"})

#####################################################################

def user_view_caretaker(request):
    a=caretaker_table.objects.filter(status='active')
    l=[]
    for i in a:
        l.append({"id":str(i.id),
                  "name":i.name,
                  "gender":i.gender,
                  "image":i.image.url,
                  "qualification":i.qualification,
                  "dob":i.dob,
                  "email":i.email,
                  "phone":i.phone,
                  })
    return JsonResponse({"status":"ok","data":l})

# def user_view_assigned_caretaker(request):
#     lid=request.POST['lid']
#     a=assigned_caretaker_table.objects.filter(REQUEST__PATIENT__USER__LOGIN_id=lid)
#     l=[]
#     for i in a:
#         l.append({"id":str(i.id),
#                   "CARETAKER":i.CARETAKER.name,
#                   "phone":i.CARETAKER.phone,
#                   "date":i.date,
#                   "time":i.time,
#                   "status":i.status
#                   })
#     return JsonResponse({"status":"ok","data":l})

def user_view_assigned_caretaker(request):
    lid = request.POST['lid']
    a = assigned_caretaker_table.objects.filter(REQUEST__PATIENT__USER__LOGIN_id=lid)
    l = []
    for i in a:
        l.append({
            "id": str(i.id),
            "REQUEST": str(i.REQUEST.id),   # ← ADD THIS
            "CARETAKER": i.CARETAKER.name,
            "phone": i.CARETAKER.phone,
            "date": str(i.date),
            "time": str(i.time),
            "status": i.status
        })
    return JsonResponse({"status": "ok", "data": l})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def delete_patient(request):
    id=request.POST['id']
    patients_table.objects.get(id=id).delete()
    return JsonResponse({'status':'ok'})

@csrf_exempt
def add_patient(request):
    if request.method == 'POST':
        try:
            # Getting data from request.POST
            lid = request.POST.get('lid')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            dob = request.POST.get('DOB')
            phone = request.POST.get('phone')
            med_history = request.POST.get('medical_history')
            cur_condition = request.POST.get('current_condition')

            photo = request.FILES.get('photo')

            a = patients_table()
            a.USER = user_table.objects.get(LOGIN_id=lid)
            a.name = name
            a.gender = gender
            a.DOB = dob
            a.phone = phone
            a.medical_history = med_history
            a.current_condition = cur_condition
            a.photo = photo

            a.save()

            return JsonResponse({"status": "ok", "task": "valid"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "failed"})





@csrf_exempt
def edit_patient(request):
    if request.method == 'POST':
        try:
            # Getting data from request.POST
            id = request.POST.get('id')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            dob = request.POST.get('DOB')
            phone = request.POST.get('phone')
            med_history = request.POST.get('medical_history')
            cur_condition = request.POST.get('current_condition')
            a = patients_table.objects.get(id=id)

            if 'photo' in request.FILES:
                photo = request.FILES.get('photo')
                a.photo=photo
                a.save()
            a.name = name
            a.gender = gender
            a.DOB = dob
            a.phone = phone
            a.medical_history = med_history
            a.current_condition = cur_condition

            a.save()

            return JsonResponse({"status": "ok", "task": "valid"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "failed"})



from django.http import JsonResponse
from .models import patients_table, request_table

def user_view_patients(request):

    lid = request.POST.get('lid')

    # Patients belonging to this user
    patients = patients_table.objects.filter(USER__LOGIN_id=lid)

    data_list = []

    for i in patients:

        # Check if caretaker request already exists
        request_exists = request_table.objects.filter(PATIENT=i).exists()

        data_list.append({
            "id": str(i.id),
            "name": i.name,
            "gender": i.gender,
            "dob": str(i.DOB),
            "phone": str(i.phone),
            "medical_history": i.medical_history,
            "current_condition": i.current_condition,
            "photo": request.build_absolute_uri(i.photo.url) if i.photo else "",
            "request_sent": request_exists
        })

    return JsonResponse({"status": "ok", "data": data_list})

from .models import request_table

def send_caretaker_request(request):

    if request.method == "POST":

        date = request.POST.get('date')
        time = request.POST.get('time')
        pid = request.POST.get('pid')

        req = request_table()
        req.date = date
        req.time = time
        req.PATIENT_id = pid
        req.reply = "pending"
        req.save()

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


from django.http import JsonResponse
from .models import pill_reminder_table


def user_view_pill_notifications(request):
    try:
        lid = request.POST.get('lid')

        # We navigate: Pill -> Assignment -> Request -> Patient -> User
        reminders = pill_reminder_table.objects.filter(
            ASSIGNED__REQUEST__PATIENT__USER__LOGIN_id=lid
        ).order_by('time')

        data_list = []
        for i in reminders:
            data_list.append({
                "id": str(i.id),
                "patient_name": i.ASSIGNED.REQUEST.PATIENT.name,  # Getting patient name
                "medicine": i.medical_name,
                "time": i.time.strftime("%I:%M %p"),  # Formatting for UI
                "frequency": i.frequency,
                "start_date": str(i.start_date),
                "end_date": str(i.end_date),
                "status": i.status,
            })

        return JsonResponse({"status": "ok", "data": data_list})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def registration(request):
    if request.method == "POST":

        photo = request.FILES.get('photo')  # ✅ SAFE
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        place = request.POST.get('place')
        email = request.POST.get('email')
        PIN_code = request.POST.get('PIN_code')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password,"pppppppppppp")


        if User.objects.filter(username=username).exists():
            return JsonResponse({'status':'no'})

        user=User.objects.create(username=username,password=make_password(password),first_name=name,email=email)
        user.save()
        user.groups.add(Group.objects.get(name='User'))




        ob = user_table()
        ob.name = name
        ob.gender = gender
        ob.phone = phone
        ob.place = place
        ob.email = email
        ob.PIN_code = PIN_code
        ob.LOGIN = user

        if photo:                # ✅ only assign if exists
            ob.image = photo

        ob.save()

        return JsonResponse({"status": "valid"})



def view_profile(request):
    lid=request.POST['lid']
    ob=user_table.objects.get(LOGIN_id=lid)
    image_url=request.build_absolute_uri(ob.image.url)if ob.image else""
    return JsonResponse({
        "status":"ok",
        "name": ob.name,
        "gender":ob.gender,
        "phone":str(ob.phone),
        "image":image_url,
        "place":ob.place,
        "email":ob.email,
        "PIN_code":ob.PIN_code

    })





def caretaker_view_profile(request):
    lid=request.POST['lid']
    ob=caretaker_table.objects.get(LOGIN_id=lid)
    image_url=request.build_absolute_uri(ob.image.url)if ob.image else""
    return JsonResponse({
        "status":"ok",
        "name": ob.name,
        "gender":ob.gender,
        "qualification":ob.qualification,
        "dob":str(ob.dob),
        "phone":str(ob.phone),
        "image":image_url,
        "email":ob.email,


    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import user_table  # Adjust based on your app name


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            place = request.POST.get('place')
            email = request.POST.get('email')
            pin_code = request.POST.get('PIN_code')

            # Fetch existing user record
            ob = user_table.objects.get(LOGIN_id=lid)

            # Update Text Fields
            ob.name = name
            ob.gender = gender
            ob.phone = phone
            ob.place = place
            ob.email = email
            ob.PIN_code = pin_code

            # Handle File Upload (Case Sensitive: 'Image' matches Flutter request)
            if 'Image' in request.FILES:
                ob.image = request.FILES['Image']

            ob.save()
            return JsonResponse({"status": "ok"})

        except user_table.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})

def send_complaint(request):
    lid=request.POST['lid']
    complaint=request.POST['complaint']
    ob=complaint_table()
    ob.complaint=complaint
    ob.reply='pending'
    ob.date=datetime.today()
    ob.USER=user_table.objects.get(LOGIN_id=lid)
    ob.save()
    return JsonResponse({"status": "ok"})

def view_complaint(request):
    lid=request.POST['lid']
    ob=complaint_table.objects.filter(USER__LOGIN_id=lid)
    mdata=[]
    for i in ob:
        data={
            'complaint':i.complaint,
            'reply':i.reply,
            'date':i.date,
        }

        mdata.append(data)
    print(mdata)

    return JsonResponse({"status": "ok",'data':mdata})

def user_view_request(request):
    pid=request.POST['pid']
    a=request_table.objects.filter(PATIENT__id=pid)
    l=[]
    for i in a:
        l.append({'id':i.id,'date':i.date,'time':i.time,'reply':i.reply})
    return JsonResponse({"status":"ok","data":l})
def caretaker_view_assigned(request):
    lid = request.POST['lid']
    assignments = assigned_caretaker_table.objects.filter(CARETAKER__LOGIN_id=lid)
    l = []
    for i in assignments:
        photo_url = i.REQUEST.PATIENT.photo.url if i.REQUEST.PATIENT.photo else ""
        l.append({
            "assignment_id": i.id, # This is the ID of the assignment
            "patient_id": i.REQUEST.PATIENT.id, # THIS is the ID needed for pills
            "patient": i.REQUEST.PATIENT.name,
            "photo": photo_url,
        })
    return JsonResponse({"status": "ok", "data": l})

from django.http import JsonResponse
from .models import pill_reminder_table


def caretaker_view_pills(request):
    pid = request.POST.get('patient_id')
    pills = pill_reminder_table.objects.filter(ASSIGNED__REQUEST__PATIENT_id=pid)

    data_list = []
    for p in pills:
        data_list.append({
            'id': p.id,
            'medicine': p.medical_name,
            'time': p.time.strftime("%I:%M %p"),
            'frequency': p.frequency,
            'start_date': p.start_date.strftime("%Y-%m-%d"),
            'end_date': p.end_date.strftime("%Y-%m-%d"),
            'status': p.status,
        })
    return JsonResponse({'status': 'ok', 'data': data_list})


def caretaker_add_pill(request):
    lid=request.POST['lid']
    aid=request.POST['aid']
    medical_name=request.POST['medical_name']
    time=request.POST['time']
    frequency=request.POST['frequency']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']

    a=pill_reminder_table()
    a.medical_name=medical_name
    a.time=time
    a.frequency=frequency
    a.start_date=start_date
    a.end_date=end_date
    a.status='pending'
    a.ASSIGNED_id=aid
    a.CARETAKER=caretaker_table.objects.get(LOGIN_id=lid)
    a.save()
    return JsonResponse({"status":"ok"})


def upload(request):
    print(request.POST)
    pid = request.POST['pid']
    image = request.FILES['image']

    ob = Fall_Notification()
    ob.patient = patients_table.objects.get(id=pid)
    ob.image = image
    ob.status = 'pending'
    ob.date = datetime.today()
    ob.time = datetime.now().strftime("%H:%M:%S")
    ob.save()
    return JsonResponse({'status': 'ok'})



# views.py
from django.http import JsonResponse
from .models import Fall_Notification

def get_fall_notifications(request):
    if request.method == 'POST':
        lid = request.POST.get('patient_id', '')
        ob=assigned_caretaker_table.objects.filter(CARETAKER__LOGIN__id=lid)
        pids=[]
        for i in ob:
            pids.append(i.REQUEST.PATIENT.id)
        print(pids)

        try:
            notifications = Fall_Notification.objects.filter(
                patient__id__in=pids
            ).order_by('-date', '-time')

            data = []
            for notif in notifications:

                data.append({
                    'id': notif.id,
                    'patient': notif.patient.name,  # adjust field name
                    'patient_id': notif.patient.id,
                    'image': request.build_absolute_uri(notif.image.url) if notif.image else '',
                    'status': notif.status,
                    'date': str(notif.date),
                    'time': notif.time,
                })
                notif.status = "viwed"
                notif.save()
            print(data)
            return JsonResponse({'status': 'ok', 'data': data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})





###############################3
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.models import User

def get_notifications_emergency(request):

    today = date.today()
    lid = request.POST.get('lid')

    if not lid:
        return JsonResponse({"status": "error", "msg": "Login id missing"})

    try:
        user = User.objects.get(id=lid)
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "User not found"})

    # Get all assignments for caretaker
    assignments = assigned_caretaker_table.objects.filter(
        CARETAKER__LOGIN_id=lid
    )

    if not assignments.exists():
        return JsonResponse({"status": "error", "msg": "Caretaker not assigned"})

    # Get patient ids
    patient_ids = assignments.values_list('REQUEST__PATIENT_id', flat=True)

    # Already notified
    notified_ids = fall_notification_status.objects.filter(
        LOGIN=user,
        date=today
    ).values_list('FALL_NOTIFICATION_id', flat=True)

    # Get latest notification
    notification = Fall_Notification.objects.filter(
        date=today,
        patient_id__in=patient_ids
    ).exclude(
        id__in=notified_ids
    ).order_by('-id').first()

    if notification:
        msg = f"Fall Alert at {notification.patient.name}"

        fall_notification_status.objects.create(
            LOGIN=user,
            FALL_NOTIFICATION=notification,
            date=today,
            status='viewed',
            message=msg
        )

        return JsonResponse({
            "status": "ok",
            "msg": msg
        })

    return JsonResponse({"status": "na"})




def get_pill_reminder(request):

    lid = request.POST.get('lid')

    if not lid:
        return JsonResponse({"status": "error", "msg": "Login id missing"})

    today = date.today()
    current_time = datetime.now().time()

    try:
        caretaker = caretaker_table.objects.get(LOGIN_id=lid)
    except caretaker_table.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "Caretaker not found"})

    # Get pill reminders for today
    reminder = pill_reminder_table.objects.filter(
        CARETAKER=caretaker,
        start_date__lte=today,
        end_date__gte=today,
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).first()

    if reminder:
        msg = f"Time to give medicine: {reminder.medical_name}"

        return JsonResponse({
            "status": "ok",
            "msg": msg,
            "medicine": reminder.medical_name,
            "time": str(reminder.time)
        })

    return JsonResponse({"status": "na"})


