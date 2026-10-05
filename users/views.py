from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django import forms
from .models import CustomUser
from jobs.models import JobPosting, Category
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500'
        }), 
        label='비밀번호 / Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500'
        }), 
        label='비밀번호 확인 / Password Confirm'
    )

    class Meta:
        model = CustomUser
        fields = [
            'user_type', 'username', 'phone_number', 
            'birth_year', 'gender', 'nationality', 'visa_type', 'agree_privacy_policy'
        ]
        widgets = {
            'user_type': forms.Select(attrs={
                'id': 'id_user_type',
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500',
                'placeholder': '이름 또는 사용자명을 입력하세요'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500',
                'placeholder': '01012345678'
            }),
            'birth_year': forms.NumberInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500',
                'placeholder': '예: 1995'
            }),
            'gender': forms.Select(choices=[('', '선택하세요 / Select Gender'), ('M', '남성 / Male'), ('F', '여성 / Female')], attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500'
            }),
            'nationality': forms.Select(choices=[
                ('', '국적을 선택하세요 / Select Nationality'),
                ('Vietnam', '베트남 / Vietnam'),
                ('Uzbekistan', '우즈베키스탄 / Uzbekistan'),
                ('China', '중국 / China'),
                ('Philippines', '필리핀 / Philippines'),
                ('Thailand', '태국 / Thailand'),
                ('Mongolia', '몽골 / Mongolia'),
                ('Cambodia', '캄보디아 / Cambodia'),
                ('Indonesia', '인도네시아 / Indonesia'),
                ('Nepal', '네팔 / Nepal'),
                ('Myanmar', '미얀마 / Myanmar'),
                ('Sri Lanka', '스리랑카 / Sri Lanka'),
                ('Bangladesh', '방글라데시 / Bangladesh'),
                ('Pakistan', '파키스탄 / Pakistan'),
                ('Other', '기타 / Other')
            ], attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500'
            }),
            'visa_type': forms.Select(choices=[
                ('', '비자 종류를 선택하세요 / Select Visa Type'),
                ('E-7', 'E-7 (특정활동 / Professional Employment)'),
                ('E-9', 'E-9 (비전문취업 / Non-professional Employment)'),
                ('H-2', 'H-2 (방문취업 / Working Visit)'),
                ('F-2', 'F-2 (거주 / Residence)'),
                ('F-4', 'F-4 (재외동포 / Overseas Korean)'),
                ('F-5', 'F-5 (영주 / Permanent Residence)'),
                ('F-6', 'F-6 (결혼이민 / Marriage Migrant)'),
                ('D-2', 'D-2 (유학 / Studying)'),
                ('D-10', 'D-10 (구직 / Job Seeking)'),
                ('Other', '기타 / Other')
            ], attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500'
            }),
            'agree_privacy_policy': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-indigo-600 bg-slate-700 border-slate-600 rounded focus:ring-indigo-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].label = '사용자 유형 / User Type'
        self.fields['username'].label = '이름 / Full Name'
        self.fields['phone_number'].label = '전화번호 / Phone Number'
        self.fields['birth_year'].label = '출생연도 / Birth Year'
        self.fields['gender'].label = '성별 / Gender'
        self.fields['nationality'].label = '국적 / Nationality'
        self.fields['visa_type'].label = '비자 종류 / Visa Type'
        self.fields['agree_privacy_policy'].label = '개인정보 수집 및 이용 동의 (필수) / Agree to Privacy Policy'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        agree_policy = cleaned_data.get("agree_privacy_policy")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다. / Passwords do not match.")
        
        if not agree_policy:
            raise forms.ValidationError("개인정보 수집 및 이용에 동의해주세요. / You must agree to the privacy policy.")

        return cleaned_data

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/signup.html', {'form': form})

def home_view(request):
    """로그인한 사용자에게 환영 메시지와 카테고리, 구인 공고 목록을 보여주는 메인 뷰"""
    # 1. 데이터베이스에서 모든 구인 공고를 최신순으로 가져옵니다.
    job_list = JobPosting.objects.all().order_by('-created_at')
    
    # 2. 데이터베이스에서 모든 카테고리를 정렬 순서(order)대로 가져옵니다.
    categories = Category.objects.all().order_by('order', 'id')
    
    # 3. 템플릿에 전달할 데이터 묶음(context)을 만듭니다.
    context = {
        'job_list': job_list,
        'categories': categories,  # 카테고리 데이터 추가!
    }
    
    # 4. users/home.html에 context 데이터를 함께 전달하며 렌더링합니다.
    return render(request, 'users/home.html', context)

def custom_logout_view(request):
    """안전한 로그아웃 처리 후 메인 페이지로 이동"""
    logout(request)
    return redirect('home')