from django.contrib import admin

from app_main.models import Category, GeneralData, Product, Banner


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_link', 'description')


class BannerInline(admin.TabularInline):
    model = Banner
    extra = 5
    fields = ('banner',)


class GeneralDataAdmin(admin.ModelAdmin):
    list_display = (
        'enterprise_name', 'email', 'logo_link',
        'img_principal_link',
    )
    fieldsets = [
        ('Datos principales', {
            'fields': ('enterprise_name', 'logo', 'img_principal',)
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
    list_display = ('name', 'category', 'img_link', 'price', 'info_tag', 'is_active')
    fieldsets = [
        ('Datos Principales:', {
            'fields': ('name', 'category', 'price', 'old_price')
        }),
        ('Descripción:', {
            'fields': ('image', 'is_active', 'is_important', 'info', 'about')
        })
    ]
    # form = ProductForm
    search_fields = ('name',)
    list_filter = ('category',)
    actions = ['Desactivar_productos', 'Activar_productos', 'Activar_destacados', 'Quitar_destacados']
    change_list_template = 'admin/custom_list.html'

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


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GeneralData, GeneralDataAdmin)
