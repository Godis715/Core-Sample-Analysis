from django.contrib import admin

from .models import Workstation


class WorkstationAdmin(admin.ModelAdmin):
    """Рабочие окружения"""

    list_display = ('title', 'description', 'creator', 'invited_worker', 'date')

    def invited_worker(self, obj):
        return '\n'.join([worker.username for worker in obj.invited.all()])


admin.site.register(Workstation, WorkstationAdmin)
