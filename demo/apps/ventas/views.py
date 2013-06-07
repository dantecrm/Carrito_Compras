from django.db.models.expressions import F
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from demo.apps.ventas.forms import addProductForm
from demo.apps.ventas.models import producto, Factura, Cliente
from django.http import HttpResponseRedirect
from datetime import date,timedelta


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
        p = producto.objects.get(id=id_prod)
        dic = request.session["carrito_de_compra"]
        keys = dic.keys()
        if not p.nombre in keys:
            dic[p.nombre] = [1,p]
        else:
            dic[p.nombre] = [dic[p.nombre][0]+1,p]
        request.session['carrito_de_compras'] = dic
        print dic
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
