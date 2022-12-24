from calendar import MONDAY
from .forms import SignupForm, LoginForm, ScheduleForm, DaydutyForm, MessageForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CleaningModel, DayDutyModel, ScheduleModel, SchoolLunchModel, MessageModel
from users.models import CustomUser
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout



# class MySignupView(CreateView):
#     template_name = 'login/signup.html'
#     form_class = SignupForm
#     success_url = '/user/'

#     def get_context_data(self):
#         context = super().get_context_data()
#         context['form_cleaning'] = CleaningForm()
#         return context

#     def form_valid(self, form):
#         result = super().form_valid(form)
#         user = self.object
#         if form.is_valid and user is not None:
#             login(self.request, user)
#             CleaningModel.create(user = user)
        
#         return result

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        place= request.POST.get('place')
        schoollunch = request.POST.get('schoollunch')
        if form.is_valid() and place in {"0","1","2","3","4","5","6","7"} and schoollunch in {"A","B","C"}:
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            CleaningModel.objects.create(user = user, place = int(place) )
            SchoolLunchModel.objects.create(user = user, ABC = schoollunch)

            login(request, user)
           
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'login/signup.html', {'form': form})


def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        Email = request.POST.get('email')
        Pass = request.POST.get('password')
    

        # Djangoの認証機能
        print(Email, Pass)
        # user = CustomUser.objects.filter(username=Email, password=Pass)[0]
        user = authenticate(username=Email, password=Pass)

        # ユーザー認証
        if user:
            login(request, user)
            print("a")
            if user.is_teacher:
                
                return HttpResponseRedirect(reverse('teacher'))
            else:
                return HttpResponseRedirect(reverse('user_'))

            
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'login/login1.html')


class MyLogoutView(LogoutView):
    template_name = 'login/logout.html'

class MyteacherView(LoginRequiredMixin, TemplateView):
    template_name = 'school/teacher.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schedulekey"] = ScheduleForm()
        context["daydutykey"] = DaydutyForm()
        context['teacher'] = self.request.user
        
        return context

def logout_request(request):
    logout(request)
    return redirect('login')








class MyUserView(LoginRequiredMixin, TemplateView):
    template_name = 'login/user.html'
    
    def get_context_data(self, **kwargs):
        PLACE_CHOICES = ["教室ほうき","教室机寄せ","教室モップ","黒板","理科室","男子トイレ","女子トイレ","美化委員の仕事"]
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        user = self.request.user
        if MessageModel.objects.filter(teacher__classnum = user.classnum,teacher__gradenum = user.gradenum):
            context['message'] = MessageModel.objects.filter(teacher__classnum = user.classnum,teacher__gradenum = user.gradenum).order_by("created_at").reverse().all()
            
        cm = CleaningModel.objects.filter(user = self.request.user.id)[0] 
        context['cleaningplace'] = PLACE_CHOICES[cm.place]
        sl = SchoolLunchModel.objects.filter(user = self.request.user.id)[0]
        context['schoollunch'] = sl.ABC
        dd = DayDutyModel.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum)[0]
        dd_user = CustomUser.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum, attendancenum = dd.current_number)[0]
        context['dd_fullname'] = dd_user.last_name + dd_user.first_name
        sm = ScheduleModel.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum)[0]
        subject = {'国':'国語', '数':'数学','理':'理科','社':'社会','英':'英語','美':'美術','体':'体育','家':'家庭科','技':'技術','音':'音楽','道':'道徳','総':'総合','学':'学活'}
        schedule = [[],[],[],[],[],[]]
        week = [sm.monday,sm.tuesday,sm.wednesday,sm.thursday,sm.friday]
        for w in week:
            for i in range(len(w)):
                schedule[i].append(subject[w[i]])
            if len(w) < 6:
                for j in range(len(w),6):
                    schedule[j].append("")
        print(schedule)
        context["schedule"] = schedule


        return context
        

class MyOtherView(LoginRequiredMixin, TemplateView):
    template_name = 'login/other.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        
        return context


def check(input):
    subject = {'国','数','理','社','英','美','体','家','技','音','道','総','学'}
    flag = True
    for v in input:
        if v not in subject:
            flag = False

    return flag







class TeacherView(LoginRequiredMixin, TemplateView):
    template_name = 'school/teacher.html'
    # def get(self, request):
    #     return render(request, self.template_name, self.params)

    def post(self, request):
        # context=super().post(request, *args,**kwargs)
        context={}
        # form =ScheduleForm(request.POST)
        print(request.POST)
        print("message" in request.POST)
        print("is_important" in request.POST)
        if 'monday' in request.POST and check(request.POST.get('monday')) and check(request.POST.get('tuesday')) and check(request.POST.get('wednesday')) and check(request.POST.get('thursday')) and check(request.POST.get('friday')):
            sm = ScheduleModel.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum)[0]
            sm.monday=request.POST.get('monday')
            sm.tuesday=request.POST.get('tuesday')
            sm.wednesday=request.POST.get('wednesday')
            sm.thursday=request.POST.get('thursday')
            sm.friday=request.POST.get('friday')
            sm.save()
            context=self.get_context_data()
        elif 'current_number' in request.POST:
            dd = DayDutyModel.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum)[0]
            dd.current_number = request.POST.get('current_number')
            dd.save()
            context=self.get_context_data()
        elif ("message" in request.POST) and ("is_important" in request.POST):
            MessageModel.objects.create(teacher = self.request.user, message = request.POST.get("message"),category = 1)
            context=self.get_context_data()
        elif ("message" in request.POST):
            MessageModel.objects.create(teacher = self.request.user, message = request.POST.get("message"),category = 0)
            context=self.get_context_data()

        else:
            context=self.get_context_data()
            context['error_message']= "入力項目をもう一度確認してください。"
            



        return render(request, self.template_name, context)
    
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.get(username=self.request.user.username)
        dd = DayDutyModel.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum)[0]
        dd_user = CustomUser.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum, attendancenum = dd.current_number)[0]
        context['classnum'] = self.request.user.classnum
        context['gradenum'] = self.request.user.gradenum
        context['dd_fullname'] = dd_user.last_name + dd_user.first_name
        sm = ScheduleModel.objects.filter(classnum = self.request.user.classnum, gradenum = self.request.user.gradenum)[0]
        subject = {'国':'国語', '数':'数学','理':'理科','社':'社会','英':'英語','美':'美術','体':'体育','家':'家庭科','技':'技術','音':'音楽','道':'道徳','総':'総合','学':'学活'}
        schedule = [[],[],[],[],[],[]]
        week = [sm.monday,sm.tuesday,sm.wednesday,sm.thursday,sm.friday]
        for w in week:
            for i in range(len(w)):
                schedule[i].append(subject[w[i]])
            if len(w) < 6:
                for j in range(len(w),6):
                    schedule[j].append("")
        print(schedule)
        context["schedule"] = schedule
        scheduleForm = ScheduleForm()
        daydutyForm = DaydutyForm()
        messageForm = MessageForm()
        scheduleForm.fields['monday'].initial = sm.monday
        scheduleForm.fields['tuesday'].initial = sm.tuesday
        scheduleForm.fields['wednesday'].initial = sm.wednesday
        scheduleForm.fields['thursday'].initial = sm.thursday
        scheduleForm.fields['friday'].initial = sm.friday
        daydutyForm.fields['current_number'].initial = dd.current_number
        context["form_schedule"] = scheduleForm
        context["form_dayduty"] = daydutyForm
        context["form_message"] = messageForm

        self.params = context
        print(self.params)
        return context
    

    #ログイン



    
