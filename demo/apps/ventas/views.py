from django.db.models.expressions import F
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from demo.apps.ventas.forms import addProductForm
from demo.apps.ventas.models import producto, Factura, Cliente
from django.http import HttpResponseRedirect
from datetime import date,timedelta
#to erase
from wkhtmltopdf.views import PDFTemplateResponse


def edit_product_view(request,id_prod):
	info = "iniciado"
	prod = producto.objects.get(pk=id_prod)
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES,instance=prod)
		if form.is_valid():
			edit_prod = form.save(commit=False)
			form.save_m2m()
			edit_prod.status = True
			edit_prod.save() # Guardamos el objeto
			info = "Correcto"
			return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
	else:
		form = addProductForm(instance=prod)
	ctx = {'form':form,'informacion':info}
	return render_to_response('ventas/editProducto.html',ctx,context_instance=RequestContext(request))

def add_product_view(request):
	info = "iniciado"
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES)
		if form.is_valid():
			add = form.save(commit=False)
			add.status = True
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones de ManyToMany
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/producto/%s'%add.id)
	else:
		form = addProductForm()
	ctx = {'form':form,'informacion':info}
	return render_to_response('ventas/addProducto.html',ctx,context_instance=RequestContext(request))


def compra_view(request,id_prod):
    if request.user.is_authenticated():
        print request.user
        p = producto.objects.get(id=id_prod)
        print "p: %s "  % p
        dic = request.session["carrito_de_compra"]
        keys = dic.keys()
        if not p.nombre in keys:
            dic[p.nombre] = [1,p]
        else:
            dic[p.nombre] = [dic[p.nombre][0]+1,p]
        request.session['carrito_de_compras'] = dic
        print "diccionario: %s" % dic
        return HttpResponseRedirect('/productos/page/1/')
    else:
        return HttpResponseRedirect('/login/')

def get_carrito_compras(request):
    productos = request.session["carrito_de_compra"]
    return render_to_response("ventas/c_compra.html",{"productos":productos},context_instance=RequestContext(request))

def borrar_carrito(request):
    dic = {}
    request.session["carrito_de_compra"] = dic
    return render_to_response("ventas/c_compra.html",{"productos":dic},context_instance=RequestContext(request))

def vicompra(request):
    c_compra = request.session["carrito_de_compra"]
    print "c_compra: %s" % c_compra
    vtotal = 0
    igv = 0
    bas_imp = 0
    f = Factura.objects.count() + 1
    for key,value in c_compra.items():
        p_pro = value[1].precio
        iva = value[1].iva
        p_total = (float(p_pro)*(1+iva))*float(value[0])
        value.append(p_total)
        vtotal += p_total
    print "vtotal: %s" % vtotal
    igv = (vtotal/1.18)*0.18
    print "igv: %s" % igv
    bas_imp = vtotal/1.18
    print "Base Imponible: %s" % bas_imp
    fecha = date.today()
    return render_to_response("ventas/factura.html",{"vtotal":vtotal,"productos":c_compra,"igv":igv,"bas_imp":bas_imp, "fecha":fecha,"nf":f},context_instance=RequestContext(request))
#to erase
def to_pdf(request):
    c_compra = request.session["carrito_de_compra"] #obtengo el carrito de compras de la session
    vtotal = 0 # valor donde acumulare el monto total a pagar por el usuario
    f = Factura.objects.count() + 1 #obtengo el numero de facturas existentes y le sumo uno, como un preview del n de la fact.
    for key,value in c_compra.items(): # el carrito es un diccionario, lo recorro key= nombre del producto
                                       # el value es una lista donde la pos 0 es la cantidad y la pos 1 el producto
        p_pro = value[1].precio # obtengo el valor del producto
        iva = value[1].iva # obtengo el iva aplicado al producto
        p_total = (float(p_pro)*(1+iva))*float(value[0]) # obtengo el valor total del producto x iva x cantidad
        value.append(p_total) # agrego al final de la lista (value) del diccionario el valor total
        vtotal += p_total # sumatoria de los valores totales
    fecha = date.today() # obtengo la fecha de hoy
    return PDFTemplateResponse(request,"ventas/facturapdf.html",{"vtotal":vtotal,"productos":c_compra,"fecha":fecha,"nf":f})
