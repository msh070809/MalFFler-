from django.shortcuts import render
from django.http import HttpResponse
# -------------------------- db  ----------------------------
from .models import lecture1 , lecture2 , problem , scenario, user , lecture3 , boards , boardAnwser , gpt_report# 모델 임포트
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



import datetime
import hashlib
import os

# 홈페이지 
def home(request):
    if 'web_id' in request.session:
        return render(request, 'bob/home.html' , {'web_id': request.session.get('web_id')})
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
                return render(request, 'bob/home.html', {'web_id': request.session.get('web_id')}) 
            else:
                messages.error(request, '회원 정보 불일치')
                return redirect("home")
        # messages.error(request, 'post실패')
        return redirect("home")




# 로그아웃
def logout(request):
    # 세션 초기화
    request.session.flush()

    # 홈 페이지로 리디렉션
    return redirect('home')



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
def lecture_table_1(request):
    lectures = lecture1.objects.all()
    if 'web_id' in request.session:
        return render(request, 'bob/lecture1.html' , {'web_id': request.session.get('web_id') , 'lectures': lectures})
    else:
       return render(request, 'bob/lecture1.html' , {'lectures': lectures})

# 제작
def lecture_table_2(request):
    lectures = lecture2.objects.all()
    if 'web_id' in request.session:
        return render(request, 'bob/lecture2.html' , {'web_id': request.session.get('web_id') , 'lectures': lectures})
    else:
       return render(request, 'bob/lecture2.html' , {'lectures': lectures})

# 분석
def lecture_table_3(request):
    lectures = lecture3.objects.all()
    if 'web_id' in request.session:
        return render(request, 'bob/lecture3.html' , {'web_id': request.session.get('web_id') , 'lectures': lectures})
    else:
       return render(request, 'bob/lecture3.html' , {'lectures': lectures})





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


# 기초 /분석 
def lecture_study1(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture1"
            result = (count_html_files_with_word_in_filename(folder_path , table)//2)

   
            if int(page) > int(result):
                return render(request ,'bob/last_page.html')
            else:
                return render(request, 'bob/lecture_study1.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})
    else:
       return render(request ,'bob/No_login.html')



# 기초 / 분석 교육 이미지 편집기
def lecture_editor1(request):
    if 'web_id' in request.session:
        session_web_id = request.session['web_id']
        try:
            user_obj = user.objects.get(web_id=session_web_id)  # 모델에서 해당 web_id에 해당하는 레코드 가져오기
            if user_obj.auth == "1":
                if request.method == 'GET':
                    table = request.GET.get('table')
                    page = request.GET.get('page')
                    file=table+page
                    return render(request, 'bob/lecture_study_editor1.html', {'file': file , 'web_id': request.session.get('web_id')})
                elif request.method == 'POST':
                    image_width = request.POST.get('image_width')
                    image_height = request.POST.get('image_height')
                    image_margin_left = request.POST.get('image_margin_left')
                    image_margin_top = request.POST.get('image_margin_top')
                    fileName = request.POST.get('file')

                    if image_width == "":
                        image_width = 650
                    if image_height == "":
                        image_height = 500
                    if image_margin_left == "":
                        image_margin_left = 0
                    if image_margin_top == "":
                        image_margin_top = 0


                    # print(image_width)
                    # print(image_height)
                    # print(image_margin_left)
                    # print(image_margin_top)
                    # print(fileName)
                    
                    css =  f"img {{\n"
                    css += f"  width: {image_width}px;\n"
                    css += f"  height: {image_height}px;\n"
                    css += f"  margin-left: {image_margin_left}px;\n"
                    css += f"  margin-top: {image_margin_top}px;\n"
                    css += f"}}"
                    # print(css)

                    # 슬래시('/')로 변경하여 파일 경로 생성
                    with open(f"web/static/web/lecture1/{fileName}.css", "wt") as f:
                        f.write(css)
                    return HttpResponseRedirect(request.get_full_path())
        except user.DoesNotExist:
            return redirect('home')




# 분석 강의
def lecture_study2(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture2"
            result = (count_html_files_with_word_in_filename(folder_path , table)//2)


            if int(page) > int(result):
                return render(request ,'bob/last_page.html')
            else:
                return render(request, 'bob/lecture_study2.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})

    # if 'web_id' in request.session:
    #     if request.method == 'GET':
    #         table = request.GET.get('table')
    #         page = request.GET.get('page')
    #         file=table+page
    #         return render(request, 'bob/lecture_study2.html', {'web_id': request.session.get('web_id') , 'file': file})
    else:
       return render(request ,'bob/No_login.html')





#  분석 교육 이미지 편집기
def lecture_editor2(request):
    if 'web_id' in request.session:
        session_web_id = request.session['web_id']
        try:
            user_obj = user.objects.get(web_id=session_web_id)  # 모델에서 해당 web_id에 해당하는 레코드 가져오기
            if user_obj.auth == "1":
                if request.method == 'GET':
                    table = request.GET.get('table')
                    page = request.GET.get('page')
                    file=table+page
                    return render(request, 'bob/lecture_study_editor2.html', {'file': file , 'web_id': request.session.get('web_id')})
                elif request.method == 'POST':
                    image_width = request.POST.get('image_width')
                    image_height = request.POST.get('image_height')
                    image_margin_left = request.POST.get('image_margin_left')
                    image_margin_top = request.POST.get('image_margin_top')
                    fileName = request.POST.get('file')

                    if image_width == "":
                        image_width = 650
                    if image_height == "":
                        image_height = 500
                    if image_margin_left == "":
                        image_margin_left = 0
                    if image_margin_top == "":
                        image_margin_top = 0


                    # print(image_width)
                    # print(image_height)
                    # print(image_margin_left)
                    # print(image_margin_top)
                    # print(fileName)
                    
                    css =  f"img {{\n"
                    css += f"  width: {image_width}px;\n"
                    css += f"  height: {image_height}px;\n"
                    css += f"  margin-left: {image_margin_left}px;\n"
                    css += f"  margin-top: {image_margin_top}px;\n"
                    css += f"}}"
                    # print(css)

                    # 슬래시('/')로 변경하여 파일 경로 생성
                    with open(f"web/static/web/lecture2/{fileName}.css", "wt") as f:
                        f.write(css)
                    return HttpResponseRedirect(request.get_full_path())
        except user.DoesNotExist:
            return redirect('home')






# 제작 강의
def lecture_study3(request):
    if 'web_id' in request.session:
        if request.method == 'GET':
            table = request.GET.get('table')
            page = request.GET.get('page')
            file=table+page
            folder_path = "web/static/web/lecture3"
            result = (count_html_files_with_word_in_filename(folder_path , table)//2)

            if int(page) > int(result):
                return render(request ,'bob/last_page.html')
            else:
                return render(request, 'bob/lecture_study3.html', {'web_id': request.session.get('web_id') , 'file': file , 'page':page , 'result' : result})
    else:
       return render(request ,'bob/No_login.html' )


#  제작 교육 이미지 편집기
#  로그인 시 권한이 있는 계정만 접근 가능
def lecture_editor3(request):
    if 'web_id' in request.session:
        session_web_id = request.session['web_id']
        try:
            user_obj = user.objects.get(web_id=session_web_id)  # 모델에서 해당 web_id에 해당하는 레코드 가져오기
            if user_obj.auth == "1":
                if request.method == 'GET':
                    table = request.GET.get('table')
                    page = request.GET.get('page')
                    file=table+page
                    return render(request, 'bob/lecture_study_editor3.html', {'file': file, 'web_id': request.session.get('web_id')})
                elif request.method == 'POST':
                    image_width = request.POST.get('image_width')
                    image_height = request.POST.get('image_height')
                    image_margin_left = request.POST.get('image_margin_left')
                    image_margin_top = request.POST.get('image_margin_top')
                    fileName = request.POST.get('file')

                    if image_width == "":
                        image_width = 650
                    if image_height == "":
                        image_height = 500
                    if image_margin_left == "":
                        image_margin_left = 0
                    if image_margin_top == "":
                        image_margin_top = 0


                    # print(image_width)
                    # print(image_height)
                    # print(image_margin_left)
                    # print(image_margin_top)
                    # print(fileName)
                    
                    css =  f"img {{\n"
                    css += f"  width: {image_width}px;\n"
                    css += f"  height: {image_height}px;\n"
                    css += f"  margin-left: {image_margin_left}px;\n"
                    css += f"  margin-top: {image_margin_top}px;\n"
                    css += f"}}"
                    # print(css)

                    # 슬래시('/')로 변경하여 파일 경로 생성
                    with open(f"web/static/web/lecture3/{fileName}.css", "wt") as f:
                        f.write(css)
                    return HttpResponseRedirect(request.get_full_path())
        except user.DoesNotExist:
            return redirect('home')










# 문제풀이 목차
def exe(request):
    page = request.GET.get('page', 1)  # 페이지, 기본값을 1로 설정
    search_filed= request.GET.get('search_filed')
    search_term = request.POST.get('search')  # POST 요청으로 받은 검색어

    # 모든 문제 목록을 가져옵니다.
    question_list = problem.objects.all()

    # 검색어가 포함된 문제만 필터링합니다.
    tag_list =  ["Print_out_level1__questions" , "Print_out_level2__questions" , "Print_out_level3__questions" , "Print_out_level4__questions" , "Print_out_level5__questions"  ]

    filed_list =  ["Print_out_all_filed","InfoStealer" , "Adware" , "Downloader/Dropper" , "Ransomware" , "Backdoor" , "Scenario" ]

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




# 문제풀이 
# 로그인시에만 접근 가능
def exe2(request):
    if 'web_id' in request.session:  
        file = request.GET.get('table')  
        if file:
            exes = problem.objects.filter(problemTitle=file)
            return render(request, 'bob/exe2.html', {'file': file, 'exes': exes , 'web_id': request.session.get('web_id')})
    else:
        return render(request, 'bob/No_login.html')






# 문제풀이 정답처리
# 로그인시에만 접근 가능
def exe3(request):
    if request.method == 'POST':
        problem_name = request.POST.get('problem_name').strip()
        file = request.POST.get('problem_name2')
        answer = request.POST.get('answer')
        
        print(file)
        # 외부 텍스트 파일의 경로
        file_path = f'web/static/web/problem/{file}/answer.txt'


        answers = {}  # 딕셔너리 초기화

        # 파일에서 데이터를 읽어와서 answers 딕셔너리를 초기화
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 줄 끝의 공백 및 개행 문자를 제거합니다.
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    answers[key] = value

        # problem_name과 answer가 answers 딕셔너리에 존재하면 333을 출력
        if problem_name in answers and answer == answers[problem_name]:
            return render(request, 'bob/answer1.html')
        else:
            return render(request, 'bob/answer2.html')




# 시나리오 목차

def scenario1(request):
    page = request.GET.get('page', 1)  # 페이지, 기본값을 1로 설정
    search_term = request.POST.get('search')  # POST 요청으로 받은 검색어

    # 모든 문제 목록을 가져옵니다.
    question_list = scenario.objects.all()  # Use your problem model here

    # 검색어가 포함된 문제만 필터링합니다.
    tag_list =  ["Print_out_level1__questions" , "Print_out_level2__questions" , "Print_out_level3__questions" , "Print_out_level4__questions" , "Print_out_level5__questions"  ]


    if search_term:
        if search_term =="Print_out_all_the_questions":
            question_list = scenario.objects.all() 
        elif search_term in tag_list:
            tag = tag_list.index(search_term) +1 
            question_list = question_list.filter(level=tag)
        else:
            question_list = question_list.filter(problemTitle__icontains=search_term)

    question_list = question_list.order_by('level')
    paginator = Paginator(question_list, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)
    
    if 'web_id' in request.session:
        return render(request, 'bob/scenario.html', {'question_list': page_obj, 'web_id': request.session.get('web_id') , "search_term": search_term})
    else:
        return render(request, 'bob/scenario.html', {'question_list': page_obj ,"search_term": search_term})







# 시나리오 문제풀이
def scenario2(request):
    if 'web_id' in request.session:  
        file = request.GET.get('table')
        if request.method == 'GET':
            exes = scenario.objects.filter(problemTitle=file)
            return render(request, 'bob/scenario2.html', {'file': file, 'exes': exes  , 'web_id': request.session.get('web_id')})
    else:
        return render(request, 'bob/No_login.html')




# 시나리오 정답처리
def scenario3(request):
    if request.method == 'POST':
        problem_name = request.POST.get('problem_name').strip()
        answer = request.POST.get('answer')

        # 외부 텍스트 파일의 경로
        file_path = 'web/static/web/scenario/answer.txt'

        answers = {}  # 딕셔너리 초기화

        # 파일에서 데이터를 읽어와서 answers 딕셔너리를 초기화
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 줄 끝의 공백 및 개행 문자를 제거합니다.
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    answers[key] = value

        # problem_name과 answer가 answers 딕셔너리에 존재하면 333을 출력
        if problem_name in answers and answer == answers[problem_name]:
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





# # 게시글 작성
# def board_save(request):
#     if 'web_id' in request.session:      
#         if request.method == 'POST':
#             title = request.POST.get('title')
#             category = request.POST.get('category')
#             content = request.POST.get('content')

#             print(f"{request.session['web_id']} {title}")
#             # board 모델에 데이터 저장
#             board(web_id=request.session['web_id'], title=title ,filed=category, text=content).save()
        
#             return redirect('board')




def board_view(request):
    if request.method == 'GET':
        web_id = request.GET.get('web_id')
        text = request.GET.get('text')
        title = request.GET.get('title')
        
        record = boards.objects.filter(web_id=web_id, text=text, title=title)

        answers = boardAnwser.objects.filter(web_id=web_id, text=text, title=title)

        return render(request, 'bob/board_view.html', {'record': record , 'web_id': request.session.get('web_id') , "answers":answers})
    # 댓글 작성
    elif request.method == 'POST':
        web_id = request.POST.get('web_id')
        text = request.POST.get('text')
        title = request.POST.get('title')
        filed = request.POST.get('filed')
        answer = request.POST.get('answer')
        
        # boardAnswer 모델에 답변 저장
        boardAnwser(web_id=web_id, text=text, title=title, answer=answer).save()
        return redirect(f'/board_view/?web_id={web_id}&title={title}&text={text}&filed={filed}')



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






'''
import openai
import time
from bs4 import BeautifulSoup

openai.api_key = ""

def mpt(request):
    if 'web_id' in request.session:
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

                # 우측   
                html_file_path1  = f"web/static/web/lecture{lecture}/{table}(좌).html"
                
                # 좌측
                html_file_path2  = f"web/static/web/lecture{lecture}/{table}(우).html"

                with open(html_file_path1, 'r', encoding='utf-8') as file:
                    html_doc1 = file.read()

                with open(html_file_path2, 'r', encoding='utf-8') as file:
                    html_doc2 = file.read()

                soup1 = BeautifulSoup(html_doc1, 'html.parser')
                soup2 = BeautifulSoup(html_doc2, 'html.parser')

                # 좌,우를 합친 모든 문자열을 가져오기
                all_text = soup1.get_text() +"\n" + soup2.get_text()         
                
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
'''


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








            # # 보고서 작성
            # messages = [{
            #         "role": "system",
            #         "content": "I am a producer of a malicious code education platform."
            #     }, {
            #         "role": "user",
            #         "content":f"{text1} is the textbook content. The current students read this and asked the question {text2} after learning. Is the textbook provided insufficient to answer the question? If it is deemed insufficient, please write a report on how to modify the contents of the textbook. Please give me the answer in Korean and don't give me anything else." 
            # }]


            # completion = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo-16k",
            #         messages=messages,
            #     )
            
            # t_text2 = completion["choices"][0].get("message").get("content").encode("utf8").decode()
            # print(t_text2)



            # # 보고서 기반 html 작성
            # messages = [{
            #         "role": "system",
            #         "content": "I am a producer of a malicious code education platform."
            #     }, {
            #         "role": "user",
            #         "content": f"{t_text2} is a report that organizes corrections, additions, and other opinions on the textbook content provided by current students based on the problem {text2} after reading and studying the textbook content {text1}. If report recommend modifications and additions to the report. Please write as an HTML file in the most efficient format. Please write the text in Korean and do not include any other content. and do not give anything else.",
            #     # "content": f"{t_text2} is a report that organizes corrections or additions and other opinions to the contents of the textbook provided based on the question {text2} asked by current students after reading and studying the textbook content {text1}. Based on this, text1 Please write in HTML in the most efficient form for learning. Please provide text in Korean and do not give anything else.",
        
            #     }]

            # completion = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo-16k",
            #         messages=messages,
            #     )



            # t_text3 = completion["choices"][0].get("message").get("content").encode("utf8").decode()
            # print(t_text3)
            
        