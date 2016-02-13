from django.contrib import admin

from .models import User, Activity, ActivityType, ActivityLink, ActivityLinkType

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 3


class ActivityAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = Activity.objects.filter(parent_activity = 1)
#         return qs
#     fieldsets = [
#         ('Descriptions',     {'fields': ['short_description', 'long_description']}),
#         ('Date information', {'fields': ['start_date','end_date'], 'classes': ['collapse']}),
#         ('Assigned To ', {'fields': ['responsible_user'], 'classes': ['collapse']}),
#         ('Parent', {'fields': ['parent_activity'], 'classes': ['collapse']}),
#         ('Type', {'fields': ['activity_type'], 'classes': ['collapse']}),
#     ]
    inlines = [ActivityInline]
    #list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['start_date']
    #search_fields = ['question_text']


admin.site.register(User)
admin.site.register(ActivityType)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityLink)
admin.site.register(ActivityLinkType)


# Register your models here.
