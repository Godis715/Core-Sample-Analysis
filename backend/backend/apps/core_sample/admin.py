from django.contrib import admin

from .models import Core_sample
from .models import Fragment


class Core_sample_admin(admin.ModelAdmin):
    """Керн"""
    list_display = [field.name for field in Core_sample._meta.fields]

    search_fields = ['name']
    list_filter = ['user_id', 'deposit', 'hole', 'status']

    class Meta:
        model = Core_sample


class Fragment_admin(admin.ModelAdmin):
    """Фрагменты керна"""
    list_display = [field.name for field in Fragment._meta.fields]

    list_filter = ['cs_id']
    exclude = ['dl_src', 'uv_src']

    class Meta:
        model = Fragment


admin.site.register(Core_sample, Core_sample_admin)
admin.site.register(Fragment, Fragment_admin)


