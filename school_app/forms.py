from django import forms
from django.forms import Widget
from school_app.models import DayDutyModel, ScheduleModel, MessageModel
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'classnum', 'gradenum', 'attendancenum', 'username', 'email', 'password1', 'password2']
        labels = {'first_name':'名前','last_name':'苗字', 'classnum':'クラス', 'gradenum':'学年', 'attendancenum':'出席番号', 'username':'ユーザーネーム', 'email':'emailアドレス', 'password1':'パスワード1', 'password2':'パスワード2'}

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        labels = {'email':'emailアドレス','password':'パスワード'}

class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monday'].widget.attrs['class'] = 'monday'
        self.fields['tuesday'].widget.attrs['class'] = 'tuesday'
        self.fields['wednesday'].widget.attrs['class'] = 'wednesday'
        self.fields['thursday'].widget.attrs['class'] = 'thursday'
        self.fields['friday'].widget.attrs['class'] = 'friday'

    class Meta:
        model = ScheduleModel
        fields = ['monday','tuesday','wednesday','thursday','friday']
        labels = {'monday':'月曜日','tuesday':'火曜日','wednesday':'水曜日','thursday':'木曜日','friday':'金曜日'} # def __init__(self,*args,**kwargs):
        # super(ScheduleForm,self).__init__(*args,**kwargs)
        # self.fields['monday'].initial = self.model.objects.monday

class DaydutyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_number'].widget.attrs['class'] = 'current_num'

    class Meta:
        model = DayDutyModel
        fields = ['current_number']
        labels = {'current_number':'日直の出席番号'}

class MessageForm(forms.Form):
    message = forms.CharField(
    required=True,
    label = 'メッセージ',
    max_length=1024,
    widget=forms.Textarea(
        attrs={
            'placeholder': '内容を1,024文字以内で入力してください。',
        }
    )
    )
    is_important = forms.BooleanField(
        label = '重要',
        required = False,
        widget = forms.CheckboxInput(attrs={'class':'check'})
    )

    # def __init__(self,*args,**kwargs):
        # super(ScheduleForm,self).__init__(*args,**kwargs)
        # self.fields['monday'].initial = self.model.objects.monday

# class CleaningForm(forms.ModelForm):
#     class Meta:
#         model = CleaningModel
#         fields = ['place']
#         labels = {'place':'場所(0なら教室ほうき 1なら教室机寄せ 2なら教室モップ 3なら黒板 4なら理科室 5なら男子トイレ 6なら女子トイレ 7なら美化委員の仕事)'}