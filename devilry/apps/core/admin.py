from django.contrib import admin
from devilry.apps.core.models import AssignmentGroup


class AssignmentGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'long_displayname')
    search_fields = [
        'id',
    ]
    readonly_fields = [
        'parentnode',
        'feedback',
        'last_deadline'
    ]

    def get_queryset(self, request):
        return super(AssignmentGroupAdmin, self).get_queryset(request)\
            .select_related(
                'parentnode', 'parentnode__parentnode',
                'parentnode__parentnode__parentnode')

    # def admins_as_string(self, obj):
    #     return ', '.join([user.username for user in obj.admins.all()])
    # admins_as_string.short_description = "Admins"

admin.site.register(AssignmentGroup, AssignmentGroupAdmin)
