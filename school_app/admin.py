from django.contrib import admin
from .models import CleaningModel, SchoolLunchModel, ScheduleModel, DayDutyModel, MessageModel

admin.site.register(CleaningModel)
admin.site.register(SchoolLunchModel)
admin.site.register(ScheduleModel)
admin.site.register(DayDutyModel)
admin.site.register(MessageModel)


