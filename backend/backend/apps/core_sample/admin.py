from django.contrib import admin

from .models import \
    Core_sample_m, \
    Fragment_m, \
    Markup_m, \
    Oil_layer_m, \
    Rock_layer_m, \
    Carbon_layer_m, \
    Ruin_layer_m


class Core_sample_admin(admin.ModelAdmin):
    """Керн"""
    list_display = [field.name for field in Core_sample_m._meta.fields]

    search_fields = ['name']
    list_filter = ['user_id', 'deposit', 'hole', 'status', 'date']

    class Meta:
        model = Core_sample_m


class Fragment_admin(admin.ModelAdmin):
    """Фрагменты керна"""
    list_display = [field.name for field in Fragment_m._meta.fields]

    list_filter = ['cs_id']
    exclude = ['dl_src', 'uv_src']

    class Meta:
        model = Fragment_m


class Markup_admin(admin.ModelAdmin):
    """Разметка керна"""
    list_display = [field.name for field in Markup_m._meta.fields]

    list_filter = ['user_id', 'cs_id', 'date']
    search_fields = ['id']

    class Meta:
        model = Markup_m


class Oil_layer_admin(admin.ModelAdmin):
    """Слой нефтенасыщенности"""
    list_display = [field.name for field in Oil_layer_m._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Oil_layer_m


class Rock_layer_admin(admin.ModelAdmin):
    """Слой породы"""
    list_display = [field.name for field in Rock_layer_m._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Rock_layer_m


class Carbon_layer_admin(admin.ModelAdmin):
    """Слой карбонатности"""
    list_display = [field.name for field in Carbon_layer_m._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Carbon_layer_m


class Disruption_layer_admin(admin.ModelAdmin):
    """Слой разрушенности"""
    list_display = [field.name for field in Ruin_layer_m._meta.fields]

    list_filter = ['markup_id']
    search_fields = ['id']

    class Meta:
        model = Ruin_layer_m


admin.site.register(Core_sample_m, Core_sample_admin)
admin.site.register(Fragment_m, Fragment_admin)
admin.site.register(Markup_m, Markup_admin)
admin.site.register(Oil_layer_m, Oil_layer_admin)
admin.site.register(Rock_layer_m, Rock_layer_admin)
admin.site.register(Carbon_layer_m, Carbon_layer_admin)
admin.site.register(Ruin_layer_m, Disruption_layer_admin)


