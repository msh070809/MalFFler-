from django.urls import path, include
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [


#홈
path('', views.start ,name="start"),


path('home', views.home, name='home'),


#로그인
path('login_logic',views.login_logic, name='login_logic'),
path('login_page',views.login_page, name='login_page'),

#로그아웃
path('logout',views.logout, name='logout'),

#회원 가입
path('member_insert1',views.member_insert1, name='member_insert1'),
path('member_insert2',views.member_insert2, name='member_insert2'),
path('member_insert3',views.member_insert3, name='member_insert3'),
path('member_insert_logic',views.member_insert_logic, name='member_insert_logic'),

#마이페이지
path('my_profile.html', views.my_profile, name='my_profile'),

#멤버 정보 수정
path('info_change_logic',views.info_change_logic, name='info_change_logic'),
path('member_info_change',views.member_info_change, name='member_info_change'),

### 강의

# 교육 과정 네비
# path('education0', views.lecture_table_0),
path('education1', views.lecture_table_1),
path('education2', views.lecture_table_2),
path('education3', views.lecture_table_3),


# 기초분석 강의 목차
path('lecture1/',views.lecture_study1),


# 분석 교육 강의 목차
path('lecture2/',views.lecture_study2),


# 제작 교육 강의 목차
path('lecture3/',views.lecture_study3),





### 문제
# 문제 종류
path('exe/',views.exe),


# 문제 풀이
path('problem/',views.exe2),

# 문제 정답 처리
path('exe_answer/',views.exe3),



### 게시판

path('board/',views.board,  name='board'),
path('board2/',views.board2,  name='board2'),
path('board3/',views.board3 ,  name='board3'),

# 게시판 작성
path('board_write/', views.board_write, name='board_write'),

# 게시판 뷰
path('board_view/',views.board_view),
path('board_view/?web_id=<str:web_id>&title=<str:title>&text=<str:text>',views.board_view),

# 답변
path('board_answer_save/',views.board_answer_save ),





# gpt 보고서
path('report/',views.report ),

path('report2/',views.report2 ),



### 쿠키

path('cookie_reset/',views.cookie_reset),






path('save/',views.save_problem),


path('핵심원리 문제풀이1/',views.vi_api_num1),
path('핵심원리 문제풀이2/',views.vi_api_num2),
path('핵심원리 문제풀이3/',views.vi_api_num3),
path('핵심원리 문제풀이4/',views.vi_api_num4),





path('mpt/',views.mpt ,  name='mpt'),


path('mpt_key/',views.mpt_key),

###가상화 
 path('virtualize/', views.virtualize, name='virtualize'),


# path('<path:var>', TemplateView.as_view(template_name="bob/404.html")),


]
