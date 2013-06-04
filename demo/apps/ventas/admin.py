from django.contrib	import admin
from demo.apps.ventas.models import cliente,producto,categoriaProducto,Factura

class AdminFactura(admin.ModelAdmin):
    readonly_fields = ('total','producto_comprado','comprador','fecha')

admin.site.register(cliente)
admin.site.register(producto)
admin.site.register(categoriaProducto)
admin.site.register(Factura,AdminFactura)