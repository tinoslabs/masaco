from django.contrib import admin
from .models import CoachingProgram, CoachingFAQ

class CoachingFAQInline(admin.TabularInline):
    model = CoachingFAQ
    extra = 1

class CoachingProgramAdmin(admin.ModelAdmin):
    inlines = [CoachingFAQInline]

admin.site.register(CoachingProgram, CoachingProgramAdmin)
