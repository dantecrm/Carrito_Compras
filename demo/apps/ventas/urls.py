from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('demo.apps.ventas.views',
	url(r'^add/producto/$','add_product_view',name= "vista_agregar_producto"),
	url(r'^edit/producto/(?P<id_prod>.*)/$','edit_product_view',name= "vista_editar_producto"),
    url(r'^buy/producto/(?P<id_prod>.*)/$','compra_view',name= "comprar_producto"),
)