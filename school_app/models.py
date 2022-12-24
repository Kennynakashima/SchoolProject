from django.db import models
from users.models import CustomUser

# Create your models here.


class CleaningModel(models.Model):
    PLACE_CHOICES =((0,"教室ほうき"),(1,"教室机寄せ"),(2,"教室モップ"),(3,"黒板"),(4,"理科室"),(5,"男子トイレ"),(6,"女子トイレ"),(7,"美化委員の仕事"))
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    place = models.IntegerField(choices = PLACE_CHOICES)



class SchoolLunchModel(models.Model):
    ABC_CHOICES =(("A","A"),("B","B"),("C","C"))

    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    ABC = models.CharField(choices = ABC_CHOICES,max_length = 1)

class DayDutyModel(models.Model):
    current_number = models.IntegerField(default = 1)
    classnum = models.IntegerField(blank=True, default = 0)
    gradenum = models.IntegerField(blank=True, default = 0)
    #daydutyクラスごとに違う。年と組のfieldが必要。

class ScheduleModel(models.Model):
    monday =models.CharField(max_length = 7)
    tuesday =models.CharField(max_length = 7)
    wednesday =models.CharField(max_length = 7)
    thursday =models.CharField(max_length = 7)
    friday =models.CharField(max_length = 7)
    classnum = models.IntegerField(blank=True, default = 0)
    gradenum = models.IntegerField(blank=True, default = 0)

class MessageModel(models.Model):
    CATEGORYCHOICES = ((0,"お知らせ"),(1,"重要"))
    teacher = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    message = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add = True)
    category = models.IntegerField(choices=CATEGORYCHOICES)



#class DayDutyModel(models.Model):
    #外部キー


#class AbsentDateModel(models.Model):

    #datetime = models.DateTimeField()


