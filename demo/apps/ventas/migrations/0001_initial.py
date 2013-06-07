# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'categoriaProducto'
        db.create_table(u'ventas_categoriaproducto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(max_length=400)),
        ))
        db.send_create_signal(u'ventas', ['categoriaProducto'])

        # Adding model 'producto'
        db.create_table(u'ventas_producto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('stock', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ventas', ['producto'])

        # Adding M2M table for field categorias on 'producto'
        m2m_table_name = db.shorten_name(u'ventas_producto_categorias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('producto', models.ForeignKey(orm[u'ventas.producto'], null=False)),
            ('categoriaproducto', models.ForeignKey(orm[u'ventas.categoriaproducto'], null=False))
        ))
        db.create_unique(m2m_table_name, ['producto_id', 'categoriaproducto_id'])

        # Adding model 'Factura'
        db.create_table(u'ventas_factura', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('comprador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('producto_comprado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.producto'])),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'ventas', ['Factura'])


    def backwards(self, orm):
        # Deleting model 'categoriaProducto'
        db.delete_table(u'ventas_categoriaproducto')

        # Deleting model 'producto'
        db.delete_table(u'ventas_producto')

        # Removing M2M table for field categorias on 'producto'
        db.delete_table(db.shorten_name(u'ventas_producto_categorias'))

        # Deleting model 'Factura'
        db.delete_table(u'ventas_factura')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ventas.categoriaproducto': {
            'Meta': {'object_name': 'categoriaProducto'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'ventas.factura': {
            'Meta': {'object_name': 'Factura'},
            'comprador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'producto_comprado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.producto']"}),
            'total': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ventas.producto': {
            'Meta': {'object_name': 'producto'},
            'categorias': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ventas.categoriaProducto']", 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stock': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['ventas']