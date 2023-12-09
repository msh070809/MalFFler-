from django.shortcuts import render
from django.http import HttpResponse
# -------------------------- db  ----------------------------
from .models import  lecture_page , lecture1 , lecture2 , problem , user , lecture3 , boards , boardAnwser , gpt_report ,Progress ,problem_exe, problem_exe_Progress 
# -----------------------------------------------------------
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.http import HttpResponseNotFound #추가
from django.db import IntegrityError
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# 암호화
from Crypto.Cipher import AES
from Crypto.Hash import SHA256 as SHA
import sys
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import urllib.request


from django.http import HttpResponse, FileResponse
import os



import datetime
import hashlib
import os
import requests
import hashlib
import time
import json
import time



def start(request):
    if 'web_id' in request.session:
        user_instance = user.objects.get(web_id=request.session.get('web_id'))
        return render(request, 'bob/home2.html' , {'web_id': request.session.get('web_id') ,'user_instance':user_instance})
    else:
       return render(request, 'bob/home2.html')
    

# 홈페이지 
def home(request):
    if 'web_id' in request.session:
        user_instance = user.objects.get(web_id=request.session.get('web_id'))
        return render(request, 'bob/home.html' , {'web_id': request.session.get('web_id') ,'user_instance':user_instance})
    else:
       return render(request, 'bob/home.html')
    
# 로그인 페이지
def login_page(request):
    if 'web_id' in request.session:
        return redirect('home')
    else:
       return redirect('home')
    


# 로그인 후 로직
# 로그인 후 접근 금지
def login_logic(request):
    if 'web_id' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()

            try:
                WebUser = user.objects.get(web_id=username)
            except user.DoesNotExist:
                WebUser = None

            try:
                WebUser = user.objects.get(pw=password , web_id=username)
            except user.DoesNotExist:
                WebUser = None

            if WebUser:
                request.session['web_id'] = username
                return redirect("home")
            else:
                messages.error(request, '회원 정보 불일치')
                return redirect("home")
        # messages.error(request, 'post실패')
        return redirect("home")


#마이페이지
def my_profile(request):
    if 'web_id' in request.session:
        user_instance = user.objects.get(web_id=request.session.get('web_id'))
        return render(request, 'bob/my_profile.html' , {'web_id': request.session.get('web_id') ,'user_instance':user_instance})
    else:
       return render(request, 'bob/No_login.html')



# 로그아웃
def logout(request):
    # 세션 초기화
    request.session.flush()

    # 홈 페이지로 리디렉션
    return redirect('start')



# 회원가입 (1)법적 동의
# 비로그인 시에만 접근 가능
def member_insert1(request):
    if 'web_id' in request.session:
        return redirect('home')
    else:
       return render(request, 'bob/member_insert_1.html')


# 회원 가입 (2)정보입력
def member_insert2(request):
    if 'web_id' in request.session:
        return redirect('home')
    else:
       return render(request, 'bob/member_insert_2.html')



# 회원가입 (3)축하
def member_insert3(request):
    if 'web_id' in request.session:
        return redirect('home')
    else:
       return render(request, 'bob/member_insert_3.html')


# 회원 가입 로직
# 비로그인시에만 접근 가능
def member_insert_logic(request):
    if 'web_id' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
            password_confirm = hashlib.sha256(request.POST['password_confirm'].encode('utf-8')).hexdigest()

            # 비밀번호와 비밀번호 확인이 일치하는지 확인
            if password != password_confirm:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
                return redirect('member_insert2')

            # 중복된 username이 데이터베이스에 존재하는지 확인
            if user.objects.filter(web_id=username).exists():
                messages.error(request, '이미 사용 중인 사용자 이름입니다.')
                return redirect('member_insert2')

            WebUser = user(web_id=username, pw=password)
            WebUser.save()

            return redirect('member_insert3')
        else:
            messages.error(request, '웹 오류.')
            return redirect('member_insert2')  


# 회원 정보 수정
# 로그인시에만 접근 가능
def member_info_change(request):
    if 'web_id' in request.session:
        return render(request, 'bob/member_info_change.html', {'web_id': request.session.get('web_id')})
    else:
       return redirect('home')



def info_change_logic(request):
    if 'web_id' in request.session:
        if request.method == 'POST':
            past_password = hashlib.sha256(request.POST['past_password'].encode('utf-8')).hexdigest()
            new_password = hashlib.sha256(request.POST['new_password'].encode('utf-8')).hexdigest()
            new_password_confirm = hashlib.sha256(request.POST['new_password_confirm'].encode('utf-8')).hexdigest()

            try:
                WebUser = user.objects.get(pw=past_password)

            except user.DoesNotExist:
                messages.error(request, '기존 비밀번호가 일치하지 않습니다.')
                return redirect('member_info_change')

            if new_password == new_password_confirm:
                WebUser.pw = new_password
                WebUser.save()

                messages.success(request, "정보가 수정 되었습니다.")
                return redirect('member_info_change')
            else:
                messages.error(request, '변경할 비밀번호가 일치하지 않습니다.')
                return redirect('member_info_change')
        else:
            messages.error(request, '웹 오류.')
            return redirect('member_info_change')
    else:
       return redirect('home')


### 강의 
# 네비

# 교육 과정
def lecture_table_0(request):
    if 'web_id' in request.session:
        return render(request, 'bob/lecture0.html' , {'web_id': request.session.get('web_id')})
    else:
       return render(request, 'bob/lecture0.html')








# 기초
lec1 = [
    "악성코드 분석이란",
    "악성코드 분석의 종류",
    "악성코드의 종류",
    "어셈블리 및 디버깅",
    "컴퓨터 기초",
    "CPU 레지스터",
    "어셈블리 명령어",
    "디버깅",
    "x64 아키텍처",
    "PE파일 구조",
    "악성코드 유포에 악용되는 파일 유형",
    "ZIP파일 구조",
    "MS Office 문서파일 구조",
    "악성코드 지속 방법(1)",
    "악성코드 지속 방법(2)",
    "악성코드 지속 방법(3)",
    "악성코드 탐지 회피를 위한 기법",
    "바이너리 보호를 위한 기법",
    "안티 디버깅을 위한 기법",
    "권한 상승을 위한 기법",
    "악성코드 은닉 기법",
    "악성코드 유포 경로",
    "악성코드 유포 기법",
    "정적분석(1)",
    "정적분석(2)",
    "정적분석을 이용한 악성코드 비교 및 분류",
    "IDA 디스어셈블리",
    "분석환경 개요",
    "동적분석(모니터링) 도구",
    "악성코드 실행 파일 분석",
    "동적 링크 라이브러리 분석",
    "자동화 분석",
    "악성코드 case 사례",
    "3.20 사이버테러 사건",
    "Sony Pictures 해킹 사건"
]



def lecture_table_1(request):
    lectures = lecture1.objects.all()
    if 'web_id' in request.session:
        web_id = request.session.get('web_id')
        user_instance = user.objects.get(web_id=web_id)  # 해당 web_id에 해당하는 user 객체 가져오기
        progress_values = Progress.objects.filter(user=user_instance).values_list('progress_value', flat=True)
        
        # 진도률
        filed_set = set(lec1)
        progress_values_set = set(list(progress_values))
        rate = round(len(filed_set.intersection(progress_values_set))/len(lec1)*100)
        
        # home 에서 불러오기 위한 진도률 저장 
        user_instance.lec1 = rate
        user_instance.save()

        # 수강완료 색
        color = "#D5DCFF"
        return render(request, 'bob/lecture1.html', {'web_id': web_id, 'lectures': lectures, 'progress_values': progress_values , 'color': color , 'rate':rate })
    else:
        rate = 0
        return render(request, 'bob/lecture1.html', {'lectures': lectures , 'rate':rate })





# 제작
lec2 = [
    "컴퓨터 프로그램의 이해",
    "프로그래밍 환경 구축",
    "윈도우 API 프로그래밍",
    "레지스트리 값 확인하여 VM 탐지",
    "IsDebuggerPresent",
    "이벤트로그 삭제",
    "레지스트리 값 삭제",
    "자가 삭제",
    "cipher를 이용한 데이터 파괴",
    "서비스 등록",
    "레지스트리 등록",
    "작업 스케줄러 등록",
    "XOR 암호화",
    "MBR 파괴",
    "키로깅",
    "액세스 토큰을 이용한 권한 상승",
    "핵심원리 문제풀이1",
"핵심원리 문제풀이2",
"핵심원리 문제풀이3",
"핵심원리 문제풀이4"
]




def lecture_table_2(request):
    lectures = lecture2.objects.all()
    if 'web_id' in request.session:
        web_id = request.session.get('web_id')
        user_instance = user.objects.get(web_id=web_id)  # 해당 web_id에 해당하는 user 객체 가져오기
        progress_values = Progress.objects.filter(user=user_instance).values_list('progress_value', flat=True)

        # 진도률
        filed_set = set(lec2)
        progress_values_set = set(list(progress_values))
        rate = round(len(filed_set.intersection(progress_values_set))/len(lec2)*100)
        
        # home 에서 불러오기 위한 진도률 저장 
        user_instance.lec2 = rate
        user_instance.save()

        # 수강완료 색깔
        color = "#D5DCFF"
        return render(request, 'bob/lecture2.html', {'web_id': web_id, 'lectures': lectures, 'progress_values': progress_values , 'color': color , 'rate':rate})
    else:
       rate=0 
       return render(request, 'bob/lecture2.html' , {'lectures': lectures , 'rate':rate})

# 분석



lec3 = [
    "1단계",
    "2단계",
    "3단계",
    "4단계",
    ".net",
    "go",
    "문서형"
]


def lecture_table_3(request):
    lectures = lecture3.objects.all()
    if 'web_id' in request.session:
        web_id = request.session.get('web_id')
        user_instance = user.objects.get(web_id=web_id)  # 해당 web_id에 해당하는 user 객체 가져오기
        progress_values = Progress.objects.filter(user=user_instance).values_list('progress_value', flat=True)

        # 진도률
        filed_set = set(lec3)
        progress_values_set = set(list(progress_values))
        rate = round(len(filed_set.intersection(progress_values_set))/len(lec3)*100)
        
        # home 에서 불러오기 위한 진도률 저장 
        user_instance.lec3 = rate
        user_instance.save()

        # 수강완료 색깔
        color = "#D5DCFF"
        return render(request, 'bob/lecture3.html', {'web_id': web_id, 'lectures': lectures, 'progress_values': progress_values , 'color': color , 'rate':rate})
    else:
       rate=0
       return render(request, 'bob/lecture3.html' , {'lectures': lectures , 'rate':rate})





# 학습페이지
# 로그인시에만 접속 가능



import os
# 전체 페이지 수 

def count_html_files_with_word_in_filename(folder_path, search_word):
    # 폴더 내의 모든 파일 목록 가져오기
    file_list = os.listdir(folder_path)

    # HTML 파일 중에서 검색할 단어를 포함하는 파일 수를 저장할 변수 초기화
    count = 0

    # 파일 목록을 순회하면서 HTML 파일명에서 단어를 검색
    for filename in file_list:
        # 파일명에서 확장자를 분리
        file_name, file_extension = os.path.splitext(filename)

        # 파일이 HTML 파일인지 확인
        if file_extension.lower() == ".html":
            # 파일명에 단어가 포함되어 있는지 확인
            if search_word.lower() in file_name.lower():
                count += 1

    return count









def lecture_study1(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture1"

            lecture_page_obj = lecture_page.objects.get(toggle=table)  # toggle과 table이 같은 경우의 레코드 찾기
            result = lecture_page_obj.page  # 해당 레코드의 페이지 가져오기
            # result = (count_html_files_with_word_in_filename(folder_path , table)//2)

   
            if int(page) > int(result):
                web_id = request.session.get('web_id')
                current_user = user.objects.get(web_id=web_id)
                existing_progress = Progress.objects.filter(user=current_user,progress_value=table).exists()
                if not existing_progress:  # 진행 상황이 없을 경우에만 추가
                    progress = Progress(user=current_user, filed= "기초강의" , progress_value=table)
                    progress.save()
                return render(request ,'bob/complete_page1.html')
            else:
                return render(request, 'bob/lecture_study1.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})
    else:
       return render(request ,'bob/No_login.html')




# 분석 강의
# 분석 강의

def lecture_study2(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture2"
            lecture_page_obj = lecture_page.objects.get(toggle=table)  # toggle과 table이 같은 경우의 레코드 찾기
            result = lecture_page_obj.page  # 해당 레코드의 페이지 가져오기
            # result = (count_html_files_with_word_in_filename(folder_path , table)//2)


            if int(page) > int(result):
                web_id = request.session.get('web_id')
                current_user = user.objects.get(web_id=web_id)
                existing_progress = Progress.objects.filter(user=current_user,progress_value=table).exists()
                if not existing_progress:  # 진행 상황이 없을 경우에만 추가
                    progress = Progress(user=current_user, filed= "핵심원리" , progress_value="핵심원리 문제풀이1")
                    progress.save()
                return render(request ,'bob/complete_page2.html')
            else:
                return render(request, 'bob/lecture_study2.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})
    else:
       return render(request ,'bob/No_login.html')











# 제작 강의

def lecture_study3(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture3"
            lecture_page_obj = lecture_page.objects.get(toggle=table)  # toggle과 table이 같은 경우의 레코드 찾기
            result = lecture_page_obj.page  # 해당 레코드의 페이지 가져오기
            # result = (count_html_files_with_word_in_filename(folder_path , table)//2)
   
            if int(page) > int(result):
                web_id = request.session.get('web_id')
                current_user = user.objects.get(web_id=web_id)
                existing_progress = Progress.objects.filter(user=current_user,progress_value=table).exists()
                if not existing_progress:  # 진행 상황이 없을 경우에만 추가
                    progress = Progress(user=current_user, filed= "핵심원리" , progress_value=table)
                    progress.save()
                return render(request ,'bob/complete_page3.html')
            else:
                return render(request, 'bob/lecture_study3.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})
    else:
       return render(request ,'bob/No_login.html')










# pip install markdown
import markdown

def get_toggle_content(request):
    toggle_content = lecture_content.objects.filter(toggle="악성코드 분석이란1(좌)")

    for content in toggle_content:
        # Contents 필드의 마크다운을 HTML로 변환
        content.Contents = markdown.markdown(content.Contents)

    return render(request, 'bob/z1.html', {'toggle_content': toggle_content})



# 문제풀이 목차
# 문제풀이 목차
def exe(request):
    page = request.GET.get('page', 1)  # 페이지, 기본값을 1로 설정
    search_filed= request.GET.get('search_filed')
    search_term = request.POST.get('search')  # POST 요청으로 받은 검색어

    # 모든 문제 목록을 가져옵니다.
    question_list = problem.objects.all()

    # 검색어가 포함된 문제만 필터링합니다.
    tag_list =  ["Print_out_level1__questions" , "Print_out_level2__questions" , "Print_out_level3__questions" , "Print_out_level4__questions" , "Print_out_level5__questions"  ]

    filed_list =  ["Print_out_all_filed","InfoStealer" , "RAT" , "Downloader/Dropper" , "Ransomware" , "Backdoor" , "Scenario" ]

    question_list = problem.objects.all() 
    if search_term:
        if search_term in tag_list:
            tag = tag_list.index(search_term) +1 
            question_list = question_list.filter(level=tag)
        else:
            question_list = question_list.filter(problemTitle__icontains=search_term)

    if filed_list:
        if search_filed in filed_list:
            question_list = question_list.filter(Field=search_filed)



    question_list = question_list.order_by('level')
    paginator = Paginator(question_list, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)

    if 'web_id' in request.session:
        return render(request, 'bob/exe.html', {'question_list': page_obj, 'web_id': request.session.get('web_id') ,"search_term": search_term , "filed_list" : filed_list , "search_filed": search_filed})
    else:
        return render(request, 'bob/exe.html', {'question_list': page_obj ,"search_term": search_term , "filed_list" : filed_list , "search_filed": search_filed})


def exe2(request):
    if 'web_id' in request.session:  
        file = request.GET.get('table')  

        if file:
            exes = problem.objects.filter(problemTitle=file)
   
            records_with = problem_exe.objects.filter(name__icontains=file)
            
            for record in records_with:
                record.markdown = markdown.markdown(record.markdown)

            context = {
                'file': file,
                'exes': exes,
                'web_id': request.session.get('web_id'),
                'records_with': records_with
            }
            
            return render(request, 'bob/exe2.html', context)
    else:
        return render(request, 'bob/No_login.html')



def exe3(request):
    if request.method == 'POST':
        problem_name = request.POST.get('problem_name').strip()
        answer = request.POST.get('answer')

        # 모델에서 해당 problem_name에 해당하는 데이터를 가져옵니다.
        problem = get_object_or_404(problem_exe, name=problem_name)

        user_instance = user.objects.get(web_id=request.session.get('web_id'))

        # 모델에서 가져온 'answer' 값과 'cleaned_exe' 값을 비교합니다.
        if problem.answer == answer:    
            existing_progress = problem_exe_Progress.objects.filter(user=request.session.get('web_id'),name=problem_name).exists()
            if not existing_progress:  # 진행 상황이 없을 경우에만 추가
                    
                # 문제를 맞췄을 때 user_instance.A에 problem.A등을 더합니다
                user_instance.A += problem.A
                user_instance.B += problem.B
                user_instance.C += problem.C
                user_instance.D += problem.D
                user_instance.E += problem.E
                user_instance.F += problem.F
                user_instance.save()  # 변경된 값을 저장합니다.
                progress = problem_exe_Progress(user=request.session.get('web_id') , name=problem_name)
                progress.save()


            return render(request, 'bob/answer1.html')
        else:
            return render(request, 'bob/answer2.html')









# 게시판
from django.db.models import Q

def board(request):
    page = request.GET.get('page', 1)  # 페이지, 기본값을 1로 설정
    search_term = request.GET.get('search')  # GET 요청으로 받은 검색어

    # 모든 문제 목록을 가져옵니다.
    question_list = boards.objects.all()  # Use your problem model here
    question_list = question_list.filter(filed="커뮤니티")

    # 검색어가 제목에 포함된 게시물을 필터링합니다.
    if search_term:
        question_list = question_list.filter(title__icontains=search_term)

    question_list = question_list.order_by('-created_at')
    paginator = Paginator(question_list, 5)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
        
    if 'web_id' in request.session:
        return render(request, 'bob/board.html', {'question_list': page_obj, 'web_id': request.session.get('web_id'), "search_term": search_term})
    else:
        return render(request, 'bob/board.html', {'question_list': page_obj, "search_term": search_term})



def board2(request):
    page = request.GET.get('page', 1)  # 페이지, 기본값을 1로 설정
    search_term = request.GET.get('search')  # GET 요청으로 받은 검색어

    # 모든 문제 목록을 가져옵니다.
    question_list = boards.objects.all()  # Use your problem model here
    question_list = question_list.filter(filed="Qna")

    # 검색어가 제목에 포함된 게시물을 필터링합니다.
    if search_term:
        question_list = question_list.filter(title__icontains=search_term)

    question_list = question_list.order_by('-created_at')
    paginator = Paginator(question_list, 5)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
        
    if 'web_id' in request.session:
        return render(request, 'bob/board2.html', {'question_list': page_obj, 'web_id': request.session.get('web_id'), "search_term": search_term})
    else:
        return render(request, 'bob/board2.html', {'question_list': page_obj, "search_term": search_term})



def board3(request):
    page = request.GET.get('page', 1)  # 페이지, 기본값을 1로 설정
    search_term = request.GET.get('search')  # GET 요청으로 받은 검색어

    # 모든 문제 목록을 가져옵니다.
    question_list = boards.objects.all()  # Use your problem model here
    question_list = question_list.filter(filed="공지사항")

    # 검색어가 제목에 포함된 게시물을 필터링합니다.
    if search_term:
        question_list = question_list.filter(title__icontains=search_term)

    question_list = question_list.order_by('-created_at')
    paginator = Paginator(question_list, 5)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
        
    if 'web_id' in request.session:
        return render(request, 'bob/board3.html', {'question_list': page_obj, 'web_id': request.session.get('web_id'), "search_term": search_term})
    else:
        return render(request, 'bob/board3.html', {'question_list': page_obj, "search_term": search_term})



# 게시판에 글쓰기 / 저장
def board_write(request):
    if 'web_id' in request.session:      
        if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            content = request.POST.get('content')

            print(f"{request.session['web_id']} {title}")
            # board 모델에 데이터 저장
            boards(web_id=request.session['web_id'], title=title ,filed=category, text=content).save()
            return redirect('board')

        else:
            return render(request, 'bob/board_write.html' , {'web_id': request.session.get('web_id')})
    else:
       return render(request, 'bob/No_login.html')






# 게시글 보기
def board_view(request):
    if request.method == 'GET':
        web_id = request.GET.get('web_id')
        text = request.GET.get('text')
        title = request.GET.get('title')
        
        
        record = boards.objects.filter(web_id=web_id, text=text, title=title)

        answers = boardAnwser.objects.filter(web_id=web_id, text=text, title=title)

        # if record != None or answers != None:
        #     return redirect('home')


        return render(request, 'bob/board_view.html', {'record': record , 'web_id': request.session.get('web_id') , "answers":answers})
    # 댓글 작성
    elif request.method == 'POST':
        if 'web_id' in request.session:
            web_id = request.POST.get('web_id')
            answer_id = request.session.get('web_id')
            text = request.POST.get('text')
            title = request.POST.get('title')
            filed = request.POST.get('filed')
            answer = request.POST.get('answer')

            if answer.strip() == "":
                return render(request, 'bob/write.html' )
                       
            
            # boardAnswer 모델에 답변 저장
            boardAnwser(web_id=web_id, answer_id=answer_id , text=text, title=title, answer=answer).save()
            return redirect(f'/board_view/?web_id={web_id}&title={title}&text={text}&filed={filed}')
        else:
            # return render(request, 'bob/No_login.html')
            return render(request, 'bob/EasterEgg.html')




def board_answer_save(request):
    if request.method == 'post':
        web_id = request.POST.get('web_id')
        text = request.POST.get('text')
        title = request.POST.get('title')
        answer = request.POST.get('answer')
        record = boardAnwser.objects.filter(web_id=web_id, text=text, title=title , answer=answer)

        return render(request, 'bob/board.html', {'record': record , 'web_id': request.session.get('web_id')})



def cookie_reset(request):
    request.session.flush()
    response = HttpResponse("Cookie Cleared")
    response.delete_cookie('cookie_name')
    return render(request, 'bob/board.html')




def save_problem(request):
    # Jigsaw
    jigsaw_problem = problem(
        problemTitle='Jigsaw',
        problemInfo="국내 사용자들을 겨냥한 랜섬웨어로, 공포 영화로 알려진 '쏘우'에 나온 가면을 사용자에게 보여주고 일정 시간이 지나면 차폐로 파일을 삭제하는 행위를 한다.",
        sha256='3ae96f73d805e1d3995253db4d910300d8442ea603737a1428b613061e7f61e7',
        Field='Ransomware',
        level=3,
        status=0,
        table='Jigsaw Q1@Jigsaw Q2@Jigsaw Q3@Jigsaw Q4@Jigsaw Q5@Jigsaw Q6@Jigsaw Q7@Jigsaw Q8'
    )
    jigsaw_problem.save()

    # Mirage
    mirage_problem = problem(
        problemTitle='Mirage',
        problemInfo='Mirage는 특정 APT 그룹이 사용한 가장 오래된 툴로, 원격 쉘용 코드와 C&C 구성 데이터 복호화 기능이 포함되어있다.',
        sha256='28d6a9a709b9ead84aece250889a1687c07e19f6993325ba5295410a478da30a',
        Field='Backdoor',
        level=1,
        status=0,
        table='Mirage Q1@Mirage Q2@Mirage Q3@Mirage Q4@Mirage Q5@Mirage Q6@Mirage Q7@Mirage Q8'
    )
    mirage_problem.save()

    # Sepsis
    sepsis_problem = problem(
        problemTitle='Sepsis',
        problemInfo='침입 직후에 저장된 데이터 대부분을 암호화하고 이메일 주소를 통해 공격자에게 연락하도록 권장한다.',
        sha256='3c7d9ecd35b21a2a8fac7cce4fdb3e11c1950d5a02a0c0b369f4082acf00bf9a',
        Field='Ransomware',
        level=3,
        status=0,
        table='Sepsis Q1@Sepsis Q2@Sepsis Q3@Sepsis Q4@Sepsis Q5@Sepsis Q6@Sepsis Q7@Sepsis Q8'
    )
    sepsis_problem.save()

    # KPOT v2.0
    kpot_problem = problem(
        problemTitle='KPOT v2.0',
        problemInfo='정보를 훔치는 트로이 목마로, 피싱 메일, 악성 사이트 등을 통해 유포된다.',
        sha256='7d7667ddce8fd69a0fd50bb08c287d10',
        Field='InfoStealer',
        level=5,
        status=0,
        table='KPOT Q1@KPOT Q2@KPOT Q3@KPOT Q4@KPOT Q5@KPOT Q6@KPOT Q7@KPOT Q8'
    )
    kpot_problem.save()







import openai
import time
from bs4 import BeautifulSoup





def mpt(request):

    file_path = 'web/templates/bob/mpt_key1.txt'

    if os.path.exists(file_path):
        print(3333)
        return render(request, 'bob/gpt_lock.html')
    else:

        if 'web_id' in request.session:
            with open('web/templates/bob/mpt_key.txt', 'r') as file:
                # 파일 전체 내용을 읽기
                openai.api_key = file.read()


            if request.method == 'GET':  
                table = request.GET.get('table')
                lecture = request.GET.get('lecture')
                return render(request, 'bob/mpt.html', {'web_id': request.session.get('web_id') , "table" : table , 'lecture': lecture})


            if request.method == 'POST':  
                lecture = request.POST.get('lecture')
                table = request.POST.get('table')
                answer = request.POST.get('answer')

                if answer.strip() == "":
                    return render(request, 'bob/mpt.html', {'web_id': request.session.get('web_id') , "t_text":"모르는 내용을 질문해주세요." , "table" : table , 'lecture': lecture })
            
                else:

                    url = f'https://mal-ffler.github.io/BoB/lecture{lecture}/{table}(좌).html'
                    response = requests.get(url)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text1 = soup.get_text()

                    url = f'https://mal-ffler.github.io/BoB/lecture{lecture}/{table}(우).html'
                    response = requests.get(url)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text2 = soup.get_text()

                    soup1 = text1 # 우측   
                    soup2 = text2 # 좌측

                    # 좌,우를 합친 모든 문자열을 가져오기
                    all_text = soup1 +"\n" + soup2        
                    
                    # 크롤링한 웹 페이지
                    text1 = all_text
                    # print(text1)

                    # 질문
                    text2 = answer
                
                    # 질문에 대한 맞춤 답변
                    messages = [{
                            "role": "system",
                            "content": "I'm a teacher on a malicious code education platform."
                        }, {
                            "role": "user",
                            "content": f"Currently, students read {text1} and asked questions after learning. Return only the answer in Korean and nothing else:\n{text2}",
                        }
                        ]

                    completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                        )
                    
                    t_text = completion["choices"][0].get("message").get("content").encode("utf8").decode()
                    
            
                    # print(f"{text1} \n\n  {answer} \n\n  {lecture} \n\n {table}  ")

                    return render(request, 'bob/mpt.html', {'web_id': request.session.get('web_id') , "t_text":t_text , "table" : table , 'lecture': lecture })


                    # 보고서 작성
                    messages = [{
                            "role": "system",
                            "content": "I am a producer of a malicious code education platform."
                        }, {
                            "role": "user",
                # "content": f"{text1} is the content of the textbook The current students read this and asked the question {text2} after learning. Based on the question, is the content of the textbook provided poor for students to learn?d? If you think it's poor, how should you revise the contents of the textbook Please write it in the form of a report Just give me the answer in korean and don't give me anything else", 
                "content": f"{text1} is the textbook content. Currently, students read this and asked the question {text2} after learning, but is the content of the textbook provided based on the question poor for students to learn? If you think it's poor, how should I revise the contents of the textbook? Write it in the form of a report and send it to me Write it in Korean and don't give anything else",
                    }]


                    completion2 = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                        )
            
                    t_text2 = completion2["choices"][0].get("message").get("content").encode("utf8").decode()
        

                # gpt_report
                    report = gpt_report(
                        text1= text1,
                        answer=answer,
                        lecture=lecture,
                        table=table,
                        report = t_text2,
                    #  html = t_text3
                    )
                    report.save()



                    return render(request, 'bob/mpt.html', {'web_id': request.session.get('web_id') , "t_text":t_text , "table" : table , 'lecture': lecture })
            else:
                return render(request, 'bob/mpt.html', {'web_id': request.session.get('web_id')  })
        else:
            return render(request, 'bob/No_login.html')

# 보고서 참
def report(request):
    if 'web_id' in request.session:
        # 기초 강의 보고서
        report1s = gpt_report.objects.filter(lecture='1').values('table').distinct()
        report1s_count = gpt_report.objects.filter(lecture='1').count()

        # 제작 강의 보고서
        report2s = gpt_report.objects.filter(lecture='2').values('table').distinct()
        report2s_count = gpt_report.objects.filter(lecture='2').count()

        # 분석 강의 보고서
        report3s = gpt_report.objects.filter(lecture='3').values('table').distinct()
        report3s_count = gpt_report.objects.filter(lecture='3').count()

        return render(request, 'bob/mpt_report.html', {'web_id': request.session.get('web_id'), 'report1s': report1s, 'report2s': report2s, 'report3s': report3s , "report1s_count" : report1s_count , "report2s_count" : report2s_count , "report3s_count" : report3s_count})
    else:
        return render(request, 'bob/No_login.html')


# 보고서 참
def report(request):
    if 'web_id' in request.session:
        # 기초 강의 보고서
        report1s = gpt_report.objects.filter(lecture='1').values('table').distinct()
        report1s_count = gpt_report.objects.filter(lecture='1').count()

        # 제작 강의 보고서
        report2s = gpt_report.objects.filter(lecture='2').values('table').distinct()
        report2s_count = gpt_report.objects.filter(lecture='2').count()

        # 분석 강의 보고서
        report3s = gpt_report.objects.filter(lecture='3').values('table').distinct()
        report3s_count = gpt_report.objects.filter(lecture='3').count()

        return render(request, 'bob/mpt_report.html', {'web_id': request.session.get('web_id'), 'report1s': report1s, 'report2s': report2s, 'report3s': report3s , "report1s_count" : report1s_count , "report2s_count" : report2s_count , "report3s_count" : report3s_count})
    else:
        return render(request, 'bob/No_login.html')






# 보고서 참
def report2(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            report = request.GET.get('report')
            print(report)
            # table 필드와 report 필드가 동일한 값을 가지는 모델을 필터링
            matching_reports = gpt_report.objects.filter(table=report)
        return render(request, 'bob/mpt_report2.html', {'web_id': request.session.get('web_id'), 'report': report, 'matching_reports': matching_reports})
    else:
        return render(request, 'bob/No_login.html')



def save_problem(request):
    gpt_report.objects.all().delete()
    # Jigsaw
    jigsaw_problem = gpt_report(
        text1='1',
        answer="문자열 분석: 악성 코드 내에 포함된 문자열을 확인하여 유용한 정보를 얻습니다. 이게 정확히 무슨 말인지 자세히 설명해줘",
        lecture='2',
        table='악성코드 분석의 종류3',
    )
    jigsaw_problem.save()
    return render(request, 'bob/mpt.html', {'web_id': request.session.get('web_id')  })









# api 문제풀이


# 파일명 hash
def calculate_sha256(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    hashed = sha256_hash.hexdigest()
    return hashed



def vi_api_num1(request):
    try:
        if 'web_id' in request.session:
            if request.method == 'POST':
                
                # 바이러스 토탈 설정 ------------------------------------------------------------------------------------------------------
                # 예시 정답
                answer = "T1053.005" #저희가 문제 만들 때 문제에 대한 정답을 이런 형식으로 전달드릴 예정이에요!

                # 사용자가 제출한 코드에서 추출한 techniques 번호들을 모을 리스트
                techniques = []

                # VirusTotal API 키
                VT_API_KEY = "74cb12a0b35a99b7a8d43ba3d09f16e92bcac7fc04be9683b8e3762750285a52" # 제 개인 VT 키인데 키 변경을 원하시면 virustotal 가입하시고 api 페이지 들어가셔서 확인하시면 돼요!

                # VirusTotal API 엔드포인트
                VT_API_SCAN_URL = "https://www.virustotal.com/vtapi/v2/file/scan"
                VT_API_URL = "https://www.virustotal.com/api/v3/files"
                # -----------------------------------------------------------------------------------------------------------------------
            
                var = calculate_sha256(str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(time.localtime().tm_sec))
                global api_answer
                if 'file' in request.FILES:
                    with open(f"web/templates/bob/api/{var}.exe", "wb") as f:
                        f.write(request.FILES['file'].read())
                        f.close()

                        def calculate_md5(file_path):
                            # 파일 내용을 읽어와 MD5 해시 계산
                            with open(file_path, 'rb') as file:
                                md5_hash = hashlib.md5(file.read()).hexdigest()
                            return md5_hash

                        def upload_to_virustotal(file_path):
                            # 파일의 MD5 해시 계산
                            md5_hash = calculate_md5(file_path)

                            # 파일을 업로드하기 위한 POST 요청
                            files = {'file': (file_path, open(file_path, 'rb'))}
                            params = {'apikey': VT_API_KEY}
                            
                            response = requests.post(VT_API_SCAN_URL, files=files, params=params)

                            # 응답을 JSON 형식으로 변환
                            try:
                                result = response.json()

                                # 업로드 결과 출력
                                if result['response_code'] == 1:
                                    print("File successfully uploaded to VirusTotal.")
                                    print(f"MD5 Hash: {md5_hash}")
                                    print("VirusTotal Scan ID:", result['scan_id'])

                                    # 보고서 얻기
                                    get_report(md5_hash)
                                else:
                                    print("File upload to VirusTotal failed.")
                                    print("Response Code:", result['response_code'])
                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def get_report(md5_hash):
                            # 보고서를 얻기 위한 GET 요청
                            VT_API_REPORT_URL = VT_API_URL + "/" + str(md5_hash) + "/behaviour_mitre_trees"

                            headers = {"accept": "application/json","x-apikey": VT_API_KEY}
                            response = requests.get(VT_API_REPORT_URL, headers=headers)

                            # 응답을 JSON 형식으로 변환
                            try:
                                report = response.json()

                                # JSON 파일로 저장
                                save_to_json(md5_hash, report)

                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def save_to_json(md5_hash, report):
                            # 파일 이름은 MD5 해시를 사용
                            file_name = f"{md5_hash}.json"
                            json_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'w') as json_file:
                                json.dump(report, json_file, indent=4)

                            print(f"VirusTotal report saved to {file_name}")
                            parshing_json(md5_hash, json_file_path)

                        def parshing_json(md5_hash, json_file_path):
                            global api_answer
                            file_name = f"{md5_hash}.txt"
                            output_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'r') as file:
                                data = json.load(file)

                            # virustotal report에서 tecniques 번호를 파싱해서 바탕화면에 txt 파일로 저장
                            with open(output_file_path, 'w') as output_file:
                                for tool_name, tool_data in data['data'].items():
                                    for tactic in tool_data['tactics']:
                                        for technique in tactic['techniques']:
                                            technique_id = technique['id'] 
                                            output_file.write(f"{technique_id}\n") 
                                            techniques.append(technique_id) # 정답 비교를 위해 리스트에 technique 번호 저장
                            print(f"VirusTotal report techniques saved to: {output_file_path}")

                            if answer in technique_id: # techniques 리스트에 정답이 있다면 정답, 불일치하면 오답 => 이 부분을 사용자에게 보여지도록 구현해주시면 돼요!
                                api_answer = "정답"
                            else:
                                api_answer = "오답"
                                
                            # print(api_answer)
                            # print(answer)
                            # print(technique_id)
                            os.remove(output_file_path)
                            os.remove(json_file_path)
                            


                        # VirusTotal에 파일 업로드    
                        def main(file_path):
                            upload_to_virustotal(file_path)

                        main(f"web/templates/bob/api/{var}.exe")    


                        os.remove(f"web/templates/bob/api/{var}.exe")
        
    
                        if api_answer == "정답":
                            current_user = user.objects.get(web_id=web_id)
                            progress = Progress(user=current_user, filed= "핵심원리" , progress_value="핵심원리 문제풀이1")
                            progress.save()
                            return render(request, 'bob/answer1.html')
                        else:
                            return render(request, 'bob/answer2.html')

            else:
                return render(request, 'bob/vi1.html' , {'web_id': request.session.get('web_id')})  
        else:
            return render(request, 'bob/No_login.html')
    except:
        return render(request, 'bob/vi1.html' , {'web_id': request.session.get('web_id')})  









def vi_api_num2(request):
    try:
        if 'web_id' in request.session:
            if request.method == 'POST':
                
                # 바이러스 토탈 설정 ------------------------------------------------------------------------------------------------------
                # 예시 정답
                answer = "T1053.005" #저희가 문제 만들 때 문제에 대한 정답을 이런 형식으로 전달드릴 예정이에요!

                # 사용자가 제출한 코드에서 추출한 techniques 번호들을 모을 리스트
                techniques = []

                # VirusTotal API 키
                VT_API_KEY = "74cb12a0b35a99b7a8d43ba3d09f16e92bcac7fc04be9683b8e3762750285a52" # 제 개인 VT 키인데 키 변경을 원하시면 virustotal 가입하시고 api 페이지 들어가셔서 확인하시면 돼요!

                # VirusTotal API 엔드포인트
                VT_API_SCAN_URL = "https://www.virustotal.com/vtapi/v2/file/scan"
                VT_API_URL = "https://www.virustotal.com/api/v3/files"
                # -----------------------------------------------------------------------------------------------------------------------
            
                var = calculate_sha256(str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(time.localtime().tm_sec))
                global api_answer
                if 'file' in request.FILES:
                    with open(f"web/templates/bob/api/{var}.exe", "wb") as f:
                        f.write(request.FILES['file'].read())
                        f.close()

                        def calculate_md5(file_path):
                            # 파일 내용을 읽어와 MD5 해시 계산
                            with open(file_path, 'rb') as file:
                                md5_hash = hashlib.md5(file.read()).hexdigest()
                            return md5_hash

                        def upload_to_virustotal(file_path):
                            # 파일의 MD5 해시 계산
                            md5_hash = calculate_md5(file_path)

                            # 파일을 업로드하기 위한 POST 요청
                            files = {'file': (file_path, open(file_path, 'rb'))}
                            params = {'apikey': VT_API_KEY}
                            
                            response = requests.post(VT_API_SCAN_URL, files=files, params=params)

                            # 응답을 JSON 형식으로 변환
                            try:
                                result = response.json()

                                # 업로드 결과 출력
                                if result['response_code'] == 1:
                                    print("File successfully uploaded to VirusTotal.")
                                    print(f"MD5 Hash: {md5_hash}")
                                    print("VirusTotal Scan ID:", result['scan_id'])

                                    # 보고서 얻기
                                    get_report(md5_hash)
                                else:
                                    print("File upload to VirusTotal failed.")
                                    print("Response Code:", result['response_code'])
                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def get_report(md5_hash):
                            # 보고서를 얻기 위한 GET 요청
                            VT_API_REPORT_URL = VT_API_URL + "/" + str(md5_hash) + "/behaviour_mitre_trees"

                            headers = {"accept": "application/json","x-apikey": VT_API_KEY}
                            response = requests.get(VT_API_REPORT_URL, headers=headers)

                            # 응답을 JSON 형식으로 변환
                            try:
                                report = response.json()

                                # JSON 파일로 저장
                                save_to_json(md5_hash, report)

                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def save_to_json(md5_hash, report):
                            # 파일 이름은 MD5 해시를 사용
                            file_name = f"{md5_hash}.json"
                            json_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'w') as json_file:
                                json.dump(report, json_file, indent=4)

                            print(f"VirusTotal report saved to {file_name}")
                            parshing_json(md5_hash, json_file_path)

                        def parshing_json(md5_hash, json_file_path):
                            global api_answer
                            file_name = f"{md5_hash}.txt"
                            output_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'r') as file:
                                data = json.load(file)

                            # virustotal report에서 tecniques 번호를 파싱해서 바탕화면에 txt 파일로 저장
                            with open(output_file_path, 'w') as output_file:
                                for tool_name, tool_data in data['data'].items():
                                    for tactic in tool_data['tactics']:
                                        for technique in tactic['techniques']:
                                            technique_id = technique['id'] 
                                            output_file.write(f"{technique_id}\n") 
                                            techniques.append(technique_id) # 정답 비교를 위해 리스트에 technique 번호 저장
                            print(f"VirusTotal report techniques saved to: {output_file_path}")

                            if answer in technique_id: # techniques 리스트에 정답이 있다면 정답, 불일치하면 오답 => 이 부분을 사용자에게 보여지도록 구현해주시면 돼요!
                                api_answer = "정답"
                            else:
                                api_answer = "오답"
                                
                            # print(api_answer)
                            # print(answer)
                            # print(technique_id)
                            os.remove(output_file_path)
                            os.remove(json_file_path)
                            


                        # VirusTotal에 파일 업로드    
                        def main(file_path):
                            upload_to_virustotal(file_path)

                        main(f"web/templates/bob/api/{var}.exe")    


                        os.remove(f"web/templates/bob/api/{var}.exe")
        
    
                        if api_answer == "정답":
                            current_user = user.objects.get(web_id=web_id)
                            progress = Progress(user=current_user, filed= "핵심원리" , progress_value="핵심원리 문제풀이2")
                            progress.save()
                            return render(request, 'bob/answer1.html')
                        else:
                            return render(request, 'bob/answer2.html')

            else:
                return render(request, 'bob/vi2.html' , {'web_id': request.session.get('web_id')})  
        else:
            return render(request, 'bob/No_login.html')
    except:
        return render(request, 'bob/vi2.html' , {'web_id': request.session.get('web_id')})  










def vi_api_num3(request):
    try:
        if 'web_id' in request.session:
            if request.method == 'POST':
                
                # 바이러스 토탈 설정 ------------------------------------------------------------------------------------------------------
                # 예시 정답
                answer = "T1497" #저희가 문제 만들 때 문제에 대한 정답을 이런 형식으로 전달드릴 예정이에요!

                # 사용자가 제출한 코드에서 추출한 techniques 번호들을 모을 리스트
                techniques = []

                # VirusTotal API 키
                VT_API_KEY = "74cb12a0b35a99b7a8d43ba3d09f16e92bcac7fc04be9683b8e3762750285a52" # 제 개인 VT 키인데 키 변경을 원하시면 virustotal 가입하시고 api 페이지 들어가셔서 확인하시면 돼요!

                # VirusTotal API 엔드포인트
                VT_API_SCAN_URL = "https://www.virustotal.com/vtapi/v2/file/scan"
                VT_API_URL = "https://www.virustotal.com/api/v3/files"
                # -----------------------------------------------------------------------------------------------------------------------
            
                var = calculate_sha256(str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(time.localtime().tm_sec))
                global api_answer
                if 'file' in request.FILES:
                    with open(f"web/templates/bob/api/{var}.exe", "wb") as f:
                        f.write(request.FILES['file'].read())
                        f.close()

                        def calculate_md5(file_path):
                            # 파일 내용을 읽어와 MD5 해시 계산
                            with open(file_path, 'rb') as file:
                                md5_hash = hashlib.md5(file.read()).hexdigest()
                            return md5_hash

                        def upload_to_virustotal(file_path):
                            # 파일의 MD5 해시 계산
                            md5_hash = calculate_md5(file_path)

                            # 파일을 업로드하기 위한 POST 요청
                            files = {'file': (file_path, open(file_path, 'rb'))}
                            params = {'apikey': VT_API_KEY}
                            
                            response = requests.post(VT_API_SCAN_URL, files=files, params=params)

                            # 응답을 JSON 형식으로 변환
                            try:
                                result = response.json()

                                # 업로드 결과 출력
                                if result['response_code'] == 1:
                                    print("File successfully uploaded to VirusTotal.")
                                    print(f"MD5 Hash: {md5_hash}")
                                    print("VirusTotal Scan ID:", result['scan_id'])

                                    # 보고서 얻기
                                    get_report(md5_hash)
                                else:
                                    print("File upload to VirusTotal failed.")
                                    print("Response Code:", result['response_code'])
                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def get_report(md5_hash):
                            # 보고서를 얻기 위한 GET 요청
                            VT_API_REPORT_URL = VT_API_URL + "/" + str(md5_hash) + "/behaviour_mitre_trees"

                            headers = {"accept": "application/json","x-apikey": VT_API_KEY}
                            response = requests.get(VT_API_REPORT_URL, headers=headers)

                            # 응답을 JSON 형식으로 변환
                            try:
                                report = response.json()

                                # JSON 파일로 저장
                                save_to_json(md5_hash, report)

                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def save_to_json(md5_hash, report):
                            # 파일 이름은 MD5 해시를 사용
                            file_name = f"{md5_hash}.json"
                            json_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'w') as json_file:
                                json.dump(report, json_file, indent=4)

                            print(f"VirusTotal report saved to {file_name}")
                            parshing_json(md5_hash, json_file_path)

                        def parshing_json(md5_hash, json_file_path):
                            global api_answer
                            file_name = f"{md5_hash}.txt"
                            output_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'r') as file:
                                data = json.load(file)

                            # virustotal report에서 tecniques 번호를 파싱해서 바탕화면에 txt 파일로 저장
                            with open(output_file_path, 'w') as output_file:
                                for tool_name, tool_data in data['data'].items():
                                    for tactic in tool_data['tactics']:
                                        for technique in tactic['techniques']:
                                            technique_id = technique['id'] 
                                            output_file.write(f"{technique_id}\n") 
                                            techniques.append(technique_id) # 정답 비교를 위해 리스트에 technique 번호 저장
                            print(f"VirusTotal report techniques saved to: {output_file_path}")

                            if answer in technique_id: # techniques 리스트에 정답이 있다면 정답, 불일치하면 오답 => 이 부분을 사용자에게 보여지도록 구현해주시면 돼요!
                                api_answer = "정답"
                            else:
                                api_answer = "오답"
                                
                            # print(api_answer)
                            # print(answer)
                            # print(technique_id)
                            os.remove(output_file_path)
                            os.remove(json_file_path)
                            


                        # VirusTotal에 파일 업로드    
                        def main(file_path):
                            upload_to_virustotal(file_path)

                        main(f"web/templates/bob/api/{var}.exe")    


                        os.remove(f"web/templates/bob/api/{var}.exe")
        
    
                        if api_answer == "정답":
                            current_user = user.objects.get(web_id=web_id)
                            progress = Progress(user=current_user, filed= "핵심원리" , progress_value="핵심원리 문제풀이3")
                            progress.save()
                            return render(request, 'bob/answer1.html')
                        else:
                            return render(request, 'bob/answer2.html')

            else:
                return render(request, 'bob/vi3.html' , {'web_id': request.session.get('web_id')})  
        else:
            return render(request, 'bob/No_login.html')
    except:
        return render(request, 'bob/vi3.html' , {'web_id': request.session.get('web_id')})  









def vi_api_num4(request):
    try:
        if 'web_id' in request.session:
            if request.method == 'POST':
                
                # 바이러스 토탈 설정 ------------------------------------------------------------------------------------------------------
                # 예시 정답
                answer = "T1059.003" #저희가 문제 만들 때 문제에 대한 정답을 이런 형식으로 전달드릴 예정이에요!

                # 사용자가 제출한 코드에서 추출한 techniques 번호들을 모을 리스트
                techniques = []

                # VirusTotal API 키
                VT_API_KEY = "74cb12a0b35a99b7a8d43ba3d09f16e92bcac7fc04be9683b8e3762750285a52" # 제 개인 VT 키인데 키 변경을 원하시면 virustotal 가입하시고 api 페이지 들어가셔서 확인하시면 돼요!

                # VirusTotal API 엔드포인트
                VT_API_SCAN_URL = "https://www.virustotal.com/vtapi/v2/file/scan"
                VT_API_URL = "https://www.virustotal.com/api/v3/files"
                # -----------------------------------------------------------------------------------------------------------------------
            
                var = calculate_sha256(str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(time.localtime().tm_sec))
                global api_answer
                if 'file' in request.FILES:
                    with open(f"web/templates/bob/api/{var}.exe", "wb") as f:
                        f.write(request.FILES['file'].read())
                        f.close()

                        def calculate_md5(file_path):
                            # 파일 내용을 읽어와 MD5 해시 계산
                            with open(file_path, 'rb') as file:
                                md5_hash = hashlib.md5(file.read()).hexdigest()
                            return md5_hash

                        def upload_to_virustotal(file_path):
                            # 파일의 MD5 해시 계산
                            md5_hash = calculate_md5(file_path)

                            # 파일을 업로드하기 위한 POST 요청
                            files = {'file': (file_path, open(file_path, 'rb'))}
                            params = {'apikey': VT_API_KEY}
                            
                            response = requests.post(VT_API_SCAN_URL, files=files, params=params)

                            # 응답을 JSON 형식으로 변환
                            try:
                                result = response.json()

                                # 업로드 결과 출력
                                if result['response_code'] == 1:
                                    print("File successfully uploaded to VirusTotal.")
                                    print(f"MD5 Hash: {md5_hash}")
                                    print("VirusTotal Scan ID:", result['scan_id'])

                                    # 보고서 얻기
                                    get_report(md5_hash)
                                else:
                                    print("File upload to VirusTotal failed.")
                                    print("Response Code:", result['response_code'])
                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def get_report(md5_hash):
                            # 보고서를 얻기 위한 GET 요청
                            VT_API_REPORT_URL = VT_API_URL + "/" + str(md5_hash) + "/behaviour_mitre_trees"

                            headers = {"accept": "application/json","x-apikey": VT_API_KEY}
                            response = requests.get(VT_API_REPORT_URL, headers=headers)

                            # 응답을 JSON 형식으로 변환
                            try:
                                report = response.json()

                                # JSON 파일로 저장
                                save_to_json(md5_hash, report)

                            except ValueError as e:
                                print(f"Error decoding JSON response from VirusTotal: {e}")

                        def save_to_json(md5_hash, report):
                            # 파일 이름은 MD5 해시를 사용
                            file_name = f"{md5_hash}.json"
                            json_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'w') as json_file:
                                json.dump(report, json_file, indent=4)

                            print(f"VirusTotal report saved to {file_name}")
                            parshing_json(md5_hash, json_file_path)

                        def parshing_json(md5_hash, json_file_path):
                            global api_answer
                            file_name = f"{md5_hash}.txt"
                            output_file_path = "web/templates/bob/api2/"+file_name

                            with open(json_file_path, 'r') as file:
                                data = json.load(file)

                            # virustotal report에서 tecniques 번호를 파싱해서 바탕화면에 txt 파일로 저장
                            with open(output_file_path, 'w') as output_file:
                                for tool_name, tool_data in data['data'].items():
                                    for tactic in tool_data['tactics']:
                                        for technique in tactic['techniques']:
                                            technique_id = technique['id'] 
                                            output_file.write(f"{technique_id}\n") 
                                            techniques.append(technique_id) # 정답 비교를 위해 리스트에 technique 번호 저장
                            print(f"VirusTotal report techniques saved to: {output_file_path}")

                            if answer in technique_id: # techniques 리스트에 정답이 있다면 정답, 불일치하면 오답 => 이 부분을 사용자에게 보여지도록 구현해주시면 돼요!
                                api_answer = "정답"
                            else:
                                api_answer = "오답"
                                
                            # print(api_answer)
                            # print(answer)
                            # print(technique_id)
                            os.remove(output_file_path)
                            os.remove(json_file_path)
                            


                        # VirusTotal에 파일 업로드    
                        def main(file_path):
                            upload_to_virustotal(file_path)

                        main(f"web/templates/bob/api/{var}.exe")    


                        os.remove(f"web/templates/bob/api/{var}.exe")
        
    
                        if api_answer == "정답":
                            current_user = user.objects.get(web_id=web_id)
                            progress = Progress(user=current_user, filed= "핵심원리" , progress_value="핵심원리 문제풀이4")
                            progress.save()
                            return render(request, 'bob/answer1.html')
                        else:
                            return render(request, 'bob/answer2.html')

            else:
                return render(request, 'bob/vi4.html' , {'web_id': request.session.get('web_id')})  
        else:
            return render(request, 'bob/No_login.html')
    except:
        return render(request, 'bob/vi4.html' , {'web_id': request.session.get('web_id')})  




# pip install pycryptodomex


class myAES():
    def __init__(self, keytext, ivtext):
        hash=SHA.new()
        key=hash.digest()
        self.key=key[:16]
        hash.update(ivtext.encode('utf-8'))
        iv=hash.digest()
        self.iv=iv[:16]
    def makeEnabled(self,plaintext):
        fillersize=0
        textsize=len(plaintext)
        if textsize%16 !=0:
            fillersize= 16-textsize%16
        filler='0'*fillersize 
        header='%d'%(fillersize)
        gap=16-len(header)
        header +='#'*gap
        return header+plaintext+filler
    def enc(self, plaintext):
        a=plaintext
        me=sys.getsizeof(a)
        ik=1
        while True:
            if ik-me>=16:
                break
            else:
                ik+=16
        p=int((ik-me)%16) 
        list=[b'0', b'1' , b'2' , b'3' , b'4' , b'5' , b'6' , b'7' , b'8' , b'9' , b'10' , b'11' , b'12' , b'13' ,b'14' , b'15']
        if p<10:
            a=list[p]+b'###############'+a
        else:
            a=list[p]+b'##############'+a

        for i in range(p):
            a+=b'0'
        aes=AES.new(self.key, AES.MODE_CBC,self.iv)
        encmsg=aes.encrypt(a)
        return encmsg
    def dec(self, ciphertext):
        aes=AES.new(self.key, AES.MODE_CBC,self.iv)
        decmsg=aes.decrypt(ciphertext)
        header=decmsg[:16].decode()
        fillersize=int(header.split('#')[0])
        if fillersize !=0:
            decmsg=decmsg[16:-fillersize]
        else:
            decmsg =decmsg[16:]   
        return decmsg
        
        
 
        
        
        
def write(key):
    keytext = key
    ivtext=''   
    with open("web/templates/bob/mpt_key.txt", "rb") as f:
        a=f.read()
        f.close()
    myCipher = myAES(keytext, ivtext)
    ciphered = myCipher.enc(a)
    with open("web/templates/bob/mpt_key1.txt", "wb") as f:
        os.remove("web/templates/bob/mpt_key.txt")
        f.write(ciphered)
        f.close() 




def read(key):
    keytext = key
    ivtext=''   
    myCipher = myAES(keytext, ivtext)
    with open("web/templates/bob/mpt_key1.txt", "rb") as f:
        deciphered = myCipher.dec(f.read())
        f.close()    
    with open("web/templates/bob/mpt_key.txt", "wb") as f:
        os.remove("web/templates/bob/mpt_key1.txt")
        f.write(deciphered)
        f.close()




def mpt_key(request):
    try:
        if request.method == 'GET':
            key=request.GET.get('key')
            if key == "enc": 
                write(key)
            elif key == "dec":
                read(key)
            else:
                return redirect('home') 
        return redirect('home')
    except:
        return redirect('home')




#  <iframe src="{% static 'web/lecture1/'|add:file|add:'(좌).html' %}" style="width: 100%; height: 585px;" ></iframe>
'''



def lecture_study1(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture1"
            result = (count_html_files_with_word_in_filename(folder_path , table)//2)

   
            if int(page) > int(result):
                web_id = request.session.get('web_id')
                current_user = user.objects.get(web_id=web_id)
                existing_progress = Progress.objects.filter(user=current_user,progress_value=table).exists()
                if not existing_progress:  # 진행 상황이 없을 경우에만 추가
                    progress = Progress(user=current_user, filed= "기초강의" , progress_value=table)
                    progress.save()
                return render(request ,'bob/complete_page1.html')
            else:
                return render(request, 'bob/lecture_study1.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})
    else:
       return render(request ,'bob/No_login.html')

'''