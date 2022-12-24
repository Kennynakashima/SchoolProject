from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import jpholiday
from .models import DayDutyModel, SchoolLunchModel

def day_duty_schedule():
    today = date.today()
    if (today.weekday() >= 5 or jpholiday.is_holiday(today)):
        pass
    else:
        day_duties = DayDutyModel.objects.all()
        currentnumbers = []
        for dayduty in day_duties:
            currentnumbers.append(dayduty.current_number + 1)
        DayDutyModel.objects.bulk_update(currentnumbers, fields = ['current_number'])
        print(currentnumbers)
    

            
def school_lunch_schedule():
    schoollunch = SchoolLunchModel.objects.all()
    move_list = {"A":"B","B":"C","C":"A"}
    abcs = []
    for sl in schoollunch:
        abcs.append(move_list[sl.ABC])
    SchoolLunchModel.objects.bulk_update(abcs, fields = ['ABC'])     
    print(abcs) 



def start():
  scheduler = BackgroundScheduler()
  print("startが実行されました。")

  scheduler.add_job(day_duty_schedule, 'cron', hour=11,minute =25)
  scheduler.add_job(school_lunch_schedule, 'cron',hour =11, minute =25)
#   scheduler.add_job(day_duty_schedule, 'cron', hour=0,minute =1  day_of_week='mon-fri')
#   scheduler.add_job(school_lunch_schedule, 'cron', day_of_week ='mon',hour = 0, minute = 1)
  scheduler.start()


  
