from django.contrib import admin

from .models import \
    Core_sample, \
    Fragment, \
    Markup, \
    Oil_layer, \
    Rock_layer, \
    Carbon_layer, \
    Ruin_layer


class Core_sample_admin(admin.ModelAdmin):
    """Керн"""
    list_display = [field.name for field in Core_sample._meta.fields]

    search_fields = ['name']
    list_filter = ['user_id', 'deposit', 'hole', 'status', 'date']

    class Meta:
        model = Core_sample


class Fragment_admin(admin.ModelAdmin):
    """Фрагменты керна"""
    list_display = [field.name for field in Fragment._meta.fields]

    list_filter = ['cs_id']
    exclude = ['dl_src', 'uv_src']

    class Meta:
        model = Fragment


class Markup_admin(admin.ModelAdmin):
    """Разметка керна"""
    list_display = [field.name for field in Markup._meta.fields]

    list_filter = ['user_id', 'cs_id', 'date']
    search_fields = ['id']

    class Meta:
        model = Markup


class Oil_layer_admin(admin.ModelAdmin):
    """Слой нефтенасыщенности"""
    list_display = [field.name for field in Oil_layer._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Oil_layer


class Rock_layer_admin(admin.ModelAdmin):
    """Слой породы"""
    list_display = [field.name for field in Rock_layer._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Rock_layer


class Carbon_layer_admin(admin.ModelAdmin):
    """Слой карбонатности"""
    list_display = [field.name for field in Carbon_layer._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Carbon_layer


class Disruption_layer_admin(admin.ModelAdmin):
    """Слой разрушенности"""
    list_display = [field.name for field in Ruin_layer._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Ruin_layer


admin.site.register(Core_sample, Core_sample_admin)
admin.site.register(Fragment, Fragment_admin)
admin.site.register(Markup, Markup_admin)
admin.site.register(Oil_layer, Oil_layer_admin)
admin.site.register(Rock_layer, Rock_layer_admin)
admin.site.register(Carbon_layer, Carbon_layer_admin)
admin.site.register(Ruin_layer, Disruption_layer_admin)


