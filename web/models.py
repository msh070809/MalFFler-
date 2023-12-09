from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# 로그인 , 회원가입 , 회원정보 수정 db
class user(models.Model):
    web_id = models.CharField(max_length=30)
    pw = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    start= models.DateTimeField(auto_now_add=True)

    lec1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=0)
    lec2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=0)
    lec3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=0)

    A = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)
    B = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)
    C = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)
    D = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)
    E = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)
    F = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)




class Progress(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    filed = models.TextField(max_length=50 ,default='')
    progress_value = models.TextField(max_length=50)  # 최대 50글자의 문자열을 저장할 수 있는 TextField



class problem_exe_Progress(models.Model):
    user = models.TextField(max_length=50 ,default='')
    name = models.TextField(max_length=50 ,default='')


# 기초/분석 교육 db
class lecture1(models.Model):
    Contents_1 = models.CharField(max_length=255, default='기초 교육')     # ex)  교육과정 , 기초/분석 교육 ,  제작교육
    Contents_2 = models.CharField(max_length=255,default='')                   # ex)  악성코드 분석 소개 (토글 형식)     
    Contents_3 = models.TextField(default='')                                  # 다수의 값을 저장하기 위해 TextField 사용












# 제작 교육 db
class lecture2(models.Model): 
    Contents_1  = models.CharField(max_length=255, default='분석 교육')       # ex)  교육과정 , 기초/분석 교육 ,  제작교육
    Contents_2 = models.CharField(max_length=255,default='')                 # ex)  악성코드 분석 소개 (토글 형식)     
    Contents_3 = models.TextField(default='')                                # 다수의 값을 저장하기 위해 TextField 사용



# 제작 교육 db
class lecture3(models.Model): 
    Contents_1  = models.CharField(max_length=255, default='제작 교육')       # ex)  교육과정 , 기초/분석 교육 ,  제작교육
    Contents_2 = models.CharField(max_length=255,default='')                 # ex)  악성코드 분석 소개 (토글 형식)     
    Contents_3 = models.TextField(default='')                                # 다수의 값을 저장하기 위해 TextField 사용



# 마지막 페이지 저장
class lecture_page(models.Model): 
    toggle  = models.CharField(max_length=255, default='') 
    page = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=1)                              # 다수의 값을 저장하기 위해 TextField 사용

  


  

# exe 목차 db

# exe 목차 db
class problem(models.Model):
    PROBLEM_FIELD_CHOICES = (
        ('InfoStealer', 'InfoStealer'),
        ('RAT', 'RAT'),
        ('Downloader/Dropper', 'Downloader/Dropper'),
        ('Ransomware', 'Ransomware'),
        ('Backdoor', 'Backdoor'),
        ('Scenario', 'Scenario'),
    )
    
    LEVEL_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    
    problemTitle = models.CharField(max_length=255)
    problemInfo = models.CharField(max_length=150)
    sha256 = models.CharField(max_length=255)
    Field = models.CharField(
        max_length=255,
        choices=PROBLEM_FIELD_CHOICES,
        default='InfoStealer'
    )
    level = models.PositiveIntegerField(
        choices=LEVEL_CHOICES,  # 1에서 5까지의 선택지 정의
        default=1  # 기본 선택지 설정 (원하는 것으로 변경 가능)
    )
    status = models.CharField(max_length=255, default=0)
    table = models.TextField(default='')




class problem_exe(models.Model):
    name = models.CharField(max_length=255)
    answer = models.CharField(max_length=150)
    markdown = models.TextField(default='')
    A = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)], default=0)
    B = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)], default=0)
    C = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)], default=0)
    D = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)], default=0)
    E = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)], default=0)
    F = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)], default=0)







# 게시판
class boards(models.Model):
    BOARD_FIELD_CHOICES = (
        ('커뮤니티', '커뮤니티'),
        ('Qna', 'Qna'),
        ('공지사항', '공지사항')
    )

    web_id = models.CharField(max_length=30)
    title = models.CharField(max_length=50, default=0)
    filed = models.CharField(max_length=255, choices=BOARD_FIELD_CHOICES, default='커뮤니티') 
    text = models.TextField()
    answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=0)
    count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)], default=0)
    created_at = models.DateTimeField(default=timezone.now)  # 현재 시간을 기본값으로 설정



# 답변
class boardAnwser(models.Model):
    web_id = models.CharField(max_length=30)
    answer_id = models.CharField(max_length=30 , default="")
    title = models.CharField(max_length=50, default=0)
    text = models.TextField(default=0)
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # 현재 시간을 기본값으로 설정



# gpt 보고서
class gpt_report(models.Model):
    lecture= models.TextField()
    table= models.TextField()
    text1= models.TextField()
    answer= models.TextField()
    report = models.TextField()
    html = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # 현재 시간을 기본값으로 설정






    def save(self, *args, **kwargs):
        # 게시물이 저장될 때마다 현재 시간을 업데이트
        self.created_at = timezone.now()
        super().save(*args, **kwargs)

