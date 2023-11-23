from django.contrib import admin
from .models import user , lecture1,lecture2  , problem , board , boardAnwser ,scenario , lecture3 ,boards , gpt_report

admin.site.register(user)

admin.site.register(lecture1)
admin.site.register(lecture2)
admin.site.register(lecture3)

admin.site.register(problem)

admin.site.register(board)
admin.site.register(boards)
admin.site.register(boardAnwser)

admin.site.register(scenario)

admin.site.register(gpt_report)