from django.contrib import admin
from .models import Parent, Skill, LSAProfile, BookingRequest

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "created_at")
    search_fields = ("name", "email")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(LSAProfile)
class LSAProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "email")
    filter_horizontal = ("skills",)

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "parent", "lsa", "start_time", "end_time", "status", "payment_status",)
    list_filter = ("status", "payment_status")
    search_fields = ("parent__name", "lsa__name")
