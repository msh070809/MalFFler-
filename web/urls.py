from django.urls import path, include
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [


#홈
path('', views.home),
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

# 기초분석 편집기
path('size1/',views.lecture_editor1),


# 분석 교육 강의 목차
path('lecture2/',views.lecture_study2),

# 분석 교육편집기
path('size2/',views.lecture_editor2),


# 제작 교육 강의 목차
path('lecture3/',views.lecture_study3),

# 제작 교육편집기
path('size3/',views.lecture_editor3),




### 문제
# 문제 종류
path('exe/',views.exe),


# 문제 풀이
path('problem/',views.exe2),

# 문제 정답 처리
path('exe_answer/',views.exe3),



### 시나리오
# 시나리오 종류
path('scenario/',views.scenario1),

# 시나리오 풀이
path('scenario_problem/',views.scenario2),

# 시나리오 정답 처리
path('scenario_answer/',views.scenario3),





### 게시판

path('board/',views.board,  name='board'),
path('board2/',views.board2,  name='board2'),
path('board3/',views.board3 ,  name='board3'),

# 게시판 작성
path('board_write/',views.board_write),

# 게시판 뷰
path('board_view/',views.board_view),



# 답변
path('board_answer_save/',views.board_answer_save ),





# gpt 보고서
path('report/',views.report ),

path('report2/',views.report2 ),



### 쿠키

path('cookie_reset/',views.cookie_reset),






path('save/',views.save_problem),








# path('mpt/',views.mpt ,  name='mpt')


]
