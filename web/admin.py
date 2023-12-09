from django.contrib import admin
from .models import user , lecture1,lecture2 , lecture_page  , problem  ,boardAnwser , lecture3 ,boards , gpt_report , Progress , problem_exe , problem_exe_Progress

admin.site.register(user)

admin.site.register(lecture1)
admin.site.register(lecture2)
admin.site.register(lecture3)

admin.site.register(problem)

admin.site.register(boards)
admin.site.register(boardAnwser)


admin.site.register(gpt_report)

admin.site.register(Progress)

admin.site.register(problem_exe)




admin.site.register(problem_exe_Progress)


admin.site.register(lecture_page)



