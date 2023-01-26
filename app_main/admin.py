from django.contrib import admin

from app_main.models import Category, GeneralData, Product, Banner, Suscriptor, InfoUtil, Municipio, Orden, \
    ComponenteOrden


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_link', 'destacado')
    fields = ('name', 'image', 'destacado')
    actions = ['Activar_destacados', 'Quitar_destacados']

    def Activar_destacados(self, request, queryset):
        for p in queryset:
            p.destacado = True
            p.save()

    def Quitar_destacados(self, request, queryset):
        for p in queryset:
            p.destacado = False
            p.save()


class BannerInline(admin.TabularInline):
    model = Banner
    extra = 5
    fields = ('banner',)


class InfoUtilInline(admin.TabularInline):
    model = InfoUtil
    extra = 1
    # fields = '__all__'


class GeneralDataAdmin(admin.ModelAdmin):
    list_display = (
        'enterprise_name', 'email', 'phone_number', 'taza_cambio', 'logo_link',
        'img_principal_link',
    )
    fieldsets = [
        ('Datos principales', {
            'fields': ('enterprise_name', 'taza_cambio', 'logo', 'img_principal',)
        },),
        ('Redes Sociales', {
            'fields': ('facebook', 'instagram',)
        },),
        ('Contacto', {
            'fields': ('enterprise_address', 'email', 'phone_number')
        },),
    ]
    inlines = [BannerInline]

    def has_add_permission(self, request):
        user = request.user
        if not user.is_anonymous:
            return False if GeneralData.objects.filter().exists() else True
        return False


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1
    fieldsets = [
        ('Datos Principales:', {
            'fields': ('name', 'category', 'specifications', 'price', 'old_price')
        }),
        ('Descripción:', {
            'fields': ('info', 'about')
        })
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'img_link', 'moneda', 'price', 'info_tag', 'sales', 'stock', 'has_old_price', 'is_active')
    fieldsets = [
        ('Datos Principales:', {
            'fields': ('name', 'category', 'moneda', 'price', 'old_price', 'stock', 'delivery_time')
        }),
        ('Descripción:', {
            'fields': ('image', 'img_link', 'is_active', 'is_important', 'info', 'about')
        })
    ]
    search_fields = ('name',)
    list_filter = ('category',)
    actions = ['Desactivar_productos', 'Activar_productos', 'Activar_destacados', 'Quitar_destacados',
               'Quitar_descuento']
    change_list_template = 'admin/custom_list.html'
    readonly_fields = ('date_updated', 'sales', 'img_link')

    def Desactivar_productos(self, request, queryset):
        for p in queryset:
            p.is_active = False
            p.save()

    def Activar_productos(self, request, queryset):
        for p in queryset:
            p.is_active = True
            p.save()

    def Activar_destacados(self, request, queryset):
        for p in queryset:
            p.is_important = False
            p.save()

    def Quitar_destacados(self, request, queryset):
        for p in queryset:
            p.is_important = True
            p.save()

    def Quitar_descuento(self, request, queryset):
        for p in queryset:
            p.old_price = None
            p.save()


class InfoUtilAdmin(admin.ModelAdmin):
    list_display = ('title', 'text_tag')


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'precio_euro')


class OrdenAdmin(admin.ModelAdmin):
    list_display = ('status', 'uuid', 'date_created', 'total', 'moneda', 'nombre_comprador', 'municipio')
    list_filter = ('status', 'moneda', 'municipio')
    search_fields = ('uuid',)


class ComponenteOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'Componente')
    list_filter = ('producto',)
    search_fields = ('orden', 'producto')


admin.site.register(Product, ProductAdmin)
admin.site.register(InfoUtil, InfoUtilAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GeneralData, GeneralDataAdmin)
admin.site.register(Suscriptor)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(ComponenteOrden, ComponenteOrdenAdmin)
admin.site.register(Municipio, MunicipioAdmin)
