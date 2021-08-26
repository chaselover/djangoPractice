from django.contrib import admin

from .models import Choice, Question


# class ChoiceInline(admin.StackedInline):
# 좀 더 오밀조밀한 TarbularInline 테이블 기반 형식
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# Choice 객체는 Question 관리자 페이지에서 편집된다. 
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    # 필터 추가
    list_filter = ['pub_date']
    # 튜플 형태로 각항목 보여줌
    list_display = ('question_text', 'pub_date', 'was_published_recently')

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
