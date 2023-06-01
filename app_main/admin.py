import os
from datetime import datetime
from pathlib import Path

import xlsxwriter
from django.contrib import admin
from django.db.models import QuerySet
from django.http import FileResponse
from django.shortcuts import render

from app_main.models import Category, GeneralData, Product, Banner, Suscriptor, InfoUtil, Municipio, Orden, \
    ComponenteOrden, ContenidoInfo


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_link', 'destacado')
    fields = ('name', 'image', 'img_link', 'destacado')
    actions = ['Activar_destacados', 'Quitar_destacados']
    readonly_fields = ('img_link',)

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


class ContenidoInfoInline(admin.StackedInline):
    model = ContenidoInfo
    extra = 3
    fields = ('text', 'image', 'image_tag')
    readonly_fields = ('image_tag',)


class GeneralDataAdmin(admin.ModelAdmin):
    list_display = (
        'enterprise_name', 'email', 'phone_number', 'taza_cambio', 'tropipay_impuesto', 'logo_link',
        'img_principal_link',
    )
    fieldsets = [
        ('Datos principales', {
            'fields': ('enterprise_name', 'taza_cambio', 'tropipay_impuesto', 'logo', 'img_principal',)
        },),
        ('Redes Sociales', {
            'fields': ('facebook', 'instagram',)
        },),
        ('SEO', {
            'fields': ('meta_tittle', 'meta_description', 'meta_kw')
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
        'name', 'category', 'img_link', 'moneda', 'price', 'codigo', 'sales', 'stock', 'has_old_price', 'is_active')
    fieldsets = [
        ('Datos Principales:', {
            'fields': ('name', 'category', 'moneda', 'price', 'old_price', 'stock', 'delivery_time')
        }),
        ('Descripción:', {
            'fields': ('image', 'img_link', 'is_active', 'is_important', 'info', 'about')
        })
    ]
    search_fields = ('name', 'codigo')
    list_filter = ('category',)
    actions = ['Desactivar_productos', 'Activar_productos', 'Activar_destacados', 'Quitar_destacados',
               'Quitar_descuento']
    change_list_template = 'admin/custom_list.html'
    readonly_fields = ('date_updated', 'sales', 'img_link', 'codigo')

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
    list_display = ('title',)
    inlines = [ContenidoInfoInline]


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'precio_euro', 'visible')


class ComponenteOrdenInline(admin.TabularInline):
    model = ComponenteOrden
    extra = 0


class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'status', 'uuid', 'date_created', 'get_componente', 'get_total', 'moneda', 'correo', 'municipio',
    )
    list_display_links = ('status', 'uuid')
    list_filter = ('status', 'moneda', 'municipio')
    search_fields = ('uuid',)
    actions = ['Exportar_Excel', 'Exportar_PDF_de_entrega', 'Exportar_PDF_de_detalles', 'Cancelar_Orden']
    list_per_page = 10
    inlines = [ComponenteOrdenInline]
    readonly_fields = ['get_componente']

    def Exportar_Excel(self, request, queryset: QuerySet[Orden]):
        filas = [
            f'{i.nombre_receptor}\n{i.telefono_receptor}\n{i.municipio} calle: {i.calle} entre: {i.calle1} y ' \
            f'{i.calle2} No: {i.numero_edificio} {i.detalles_direccion}' for i in queryset]
        filas += ['TOTAL']
        columnas = [Product.objects.get(pk=i[0]) for i in
                    set(ComponenteOrden.objects.filter(orden__in=queryset).values_list('producto_id'))]
        columnas2 = [p.name for p in columnas]
        matriz = []
        for i in queryset:
            lista = []
            for c in columnas:
                if i.componente_orden.filter(producto=c).exists():
                    cant = i.componente_orden.filter(producto=c).first().cantidad
                    lista.append(cant)
                else:
                    lista.append('')
            matriz.append(lista)
        ruta = Path(os.getcwd())
        archivo = 'Ordenes {}.xlsx'.format(str(datetime.now().strftime("%m_%d_%Y")))
        workbook = xlsxwriter.Workbook(ruta.joinpath(archivo))
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('vcenter')
        cell_format.set_font_size(10)
        worksheet = workbook.add_worksheet()
        worksheet.set_column_pixels(0, 0, 300)
        worksheet.write_column(1, 0, filas, cell_format)
        worksheet.write_row(0, 1, columnas2, cell_format)
        row = 1
        for i in matriz:
            worksheet.write_row(row, 1, i, cell_format)
            row += 1
        last_row = [0 for i in range(len(columnas))]
        casd = 0
        for i in matriz:
            for j in i:
                if type(j) == int:
                    last_row[casd] += j
                casd += 1
            casd = 0
        worksheet.write_row(row, 1, last_row, cell_format)
        workbook.close()
        response = FileResponse(open(ruta.joinpath(archivo), 'rb'))
        return response

    def Exportar_PDF_de_entrega(self, request, queryset: QuerySet[Orden]):
        return render(request, 'ordenes_pdf.html', {
            'orden_list': queryset,
            'business': GeneralData.objects.all().first(),
        })

    def Exportar_PDF_de_detalles(self, request, queryset: QuerySet[Orden]):
        return render(request, 'ordenes_detalles_pdf.html', {
            'orden_list': queryset,
            'business': GeneralData.objects.all().first(),
        })

    def Cancelar_Orden(self, request, queryset):
        for o in queryset:
            if o.status != '3':
                o.status = '3'
                o.save()
                for c in o.componente_orden.all():
                    if c.producto:
                        prod = c.producto
                        prod.stock = prod.stock + c.cantidad
                        prod.sales -= c.cantidad
                        prod.save()


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
