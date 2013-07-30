from django.db import models
from demo.apps.home.models import Cliente
from django.conf import settings

class categoriaProducto(models.Model):
    nombre 	= models.CharField(max_length=200)
    descripcion = models.TextField(max_length=400)

    def __unicode__(self):
        return self.nombre

class producto(models.Model):

    def url(self,filename):
        ruta = "MultimediaData/Producto/%s/%s"%(self.nombre,str(filename))
        return ruta


    nombre		= models.CharField(max_length=100)
    descripcion	= models.TextField(max_length=300)
    status		= models.BooleanField(default=True)
    imagen 		= models.ImageField(upload_to=url,null=True,blank=True)
    precio		= models.DecimalField(max_digits=6,decimal_places=2)
    stock		= models.IntegerField()
    categorias	= models.ManyToManyField(categoriaProducto,null=True,blank=True)
    iva         = models.FloatField()
    campo_en_blanco = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Factura(models.Model):
    total = models.IntegerField()
    comprador = models.ForeignKey(settings.AUTH_USER_MODEL)
    producto_comprado = models.ManyToManyField(producto)
    fecha = models.DateField()
    fecha_cambio = models.DateField(verbose_name="Fecha Maxima de retorno")
    def __unicode__(self):
        return u"%s %s"%(self.comprador,self.fecha)