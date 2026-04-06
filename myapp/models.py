from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class caretaker_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.FileField()
    gender=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    dob=models.DateField()
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    status=models.CharField(max_length=100)


class user_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    image = models.FileField()
    place = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    PIN_code = models.IntegerField()

class  complaint_table(models.Model):
    USER = models.ForeignKey(user_table,on_delete=models.CASCADE)
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    date = models.DateField()

class patients_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    photo = models.FileField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    DOB = models.DateField()
    phone = models.BigIntegerField()
    medical_history = models.CharField(max_length=100)
    current_condition = models.CharField(max_length=100)


class request_table(models.Model):
    PATIENT = models.ForeignKey(patients_table, on_delete=models.CASCADE)
    date = models.DateField()
    time=models.TimeField()
    reply = models.CharField(max_length=100)

class assigned_caretaker_table(models.Model):
    REQUEST = models.ForeignKey(request_table, on_delete=models.CASCADE)
    CARETAKER = models.ForeignKey(caretaker_table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100)

class payment_table(models.Model):
    CARETAKER = models.ForeignKey(caretaker_table, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=100)


class pill_reminder_table(models.Model):
    CARETAKER=models.ForeignKey(caretaker_table,on_delete=models.CASCADE,default='')
    ASSIGNED = models.ForeignKey(assigned_caretaker_table, on_delete=models.CASCADE,default='')
    medical_name = models.CharField(max_length=100)
    time = models.TimeField()
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100)

class review_tabale(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    CARETAKER = models.ForeignKey(caretaker_table, on_delete=models.CASCADE)
    review = models.CharField(max_length=100)
    rating = models.FloatField()
    date = models.DateField()




class Fall_Notification(models.Model):
    patient = models.ForeignKey(patients_table, on_delete=models.CASCADE)
    image = models.FileField()
    status = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=15)




class fall_notification_status(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=100, default='pending')
    message = models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    FALL_NOTIFICATION=models.ForeignKey(Fall_Notification,on_delete=models.CASCADE)

