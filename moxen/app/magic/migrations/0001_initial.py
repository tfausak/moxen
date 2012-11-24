# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Color'
        db.create_table('magic_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=1)),
        ))
        db.send_create_signal('magic', ['Color'])

        # Adding model 'ManaSymbol'
        db.create_table('magic_manasymbol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('magic', ['ManaSymbol'])

        # Adding M2M table for field colors on 'ManaSymbol'
        db.create_table('magic_manasymbol_colors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('manasymbol', models.ForeignKey(orm['magic.manasymbol'], null=False)),
            ('color', models.ForeignKey(orm['magic.color'], null=False))
        ))
        db.create_unique('magic_manasymbol_colors', ['manasymbol_id', 'color_id'])

        # Adding model 'ManaCost'
        db.create_table('magic_manacost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mana_symbol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.ManaSymbol'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal('magic', ['ManaCost'])

        # Adding unique constraint on 'ManaCost', fields ['mana_symbol', 'count']
        db.create_unique('magic_manacost', ['mana_symbol_id', 'count'])

        # Adding model 'SuperType'
        db.create_table('magic_supertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=9)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=9)),
        ))
        db.send_create_signal('magic', ['SuperType'])

        # Adding model 'CardType'
        db.create_table('magic_cardtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=12)),
        ))
        db.send_create_signal('magic', ['CardType'])

        # Adding model 'SubType'
        db.create_table('magic_subtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=24)),
        ))
        db.send_create_signal('magic', ['SubType'])

        # Adding model 'Set'
        db.create_table('magic_set', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=39)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=39)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=3)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('magic', ['Set'])

        # Adding model 'Rarity'
        db.create_table('magic_rarity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=1)),
        ))
        db.send_create_signal('magic', ['Rarity'])

        # Adding model 'Ruling'
        db.create_table('magic_ruling', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('magic', ['Ruling'])

        # Adding model 'Card'
        db.create_table('magic_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=141)),
            ('ascii_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=141)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=141)),
            ('rules_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('power', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('toughness', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('converted_power', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('converted_toughness', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('loyalty', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('hand_modifier', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('life_modifier', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('other_card', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['magic.Card'], unique=True, null=True, blank=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(default='n', max_length=1)),
            ('reserved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('magic', ['Card'])

        # Adding M2M table for field mana_cost on 'Card'
        db.create_table('magic_card_mana_cost', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['magic.card'], null=False)),
            ('manacost', models.ForeignKey(orm['magic.manacost'], null=False))
        ))
        db.create_unique('magic_card_mana_cost', ['card_id', 'manacost_id'])

        # Adding M2M table for field super_types on 'Card'
        db.create_table('magic_card_super_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['magic.card'], null=False)),
            ('supertype', models.ForeignKey(orm['magic.supertype'], null=False))
        ))
        db.create_unique('magic_card_super_types', ['card_id', 'supertype_id'])

        # Adding M2M table for field card_types on 'Card'
        db.create_table('magic_card_card_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['magic.card'], null=False)),
            ('cardtype', models.ForeignKey(orm['magic.cardtype'], null=False))
        ))
        db.create_unique('magic_card_card_types', ['card_id', 'cardtype_id'])

        # Adding M2M table for field sub_types on 'Card'
        db.create_table('magic_card_sub_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['magic.card'], null=False)),
            ('subtype', models.ForeignKey(orm['magic.subtype'], null=False))
        ))
        db.create_unique('magic_card_sub_types', ['card_id', 'subtype_id'])

        # Adding M2M table for field colors on 'Card'
        db.create_table('magic_card_colors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['magic.card'], null=False)),
            ('color', models.ForeignKey(orm['magic.color'], null=False))
        ))
        db.create_unique('magic_card_colors', ['card_id', 'color_id'])

        # Adding M2M table for field rulings on 'Card'
        db.create_table('magic_card_rulings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['magic.card'], null=False)),
            ('ruling', models.ForeignKey(orm['magic.ruling'], null=False))
        ))
        db.create_unique('magic_card_rulings', ['card_id', 'ruling_id'])

        # Adding model 'Printing'
        db.create_table('magic_printing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Card'])),
            ('set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Set'])),
            ('rarity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Rarity'])),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('flavor_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('magic', ['Printing'])

        # Adding model 'Block'
        db.create_table('magic_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('magic', ['Block'])

        # Adding M2M table for field sets on 'Block'
        db.create_table('magic_block_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('block', models.ForeignKey(orm['magic.block'], null=False)),
            ('set', models.ForeignKey(orm['magic.set'], null=False))
        ))
        db.create_unique('magic_block_sets', ['block_id', 'set_id'])

        # Adding model 'Format'
        db.create_table('magic_format', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, blank=True)),
        ))
        db.send_create_signal('magic', ['Format'])

        # Adding M2M table for field sets on 'Format'
        db.create_table('magic_format_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('format', models.ForeignKey(orm['magic.format'], null=False)),
            ('set', models.ForeignKey(orm['magic.set'], null=False))
        ))
        db.create_unique('magic_format_sets', ['format_id', 'set_id'])

        # Adding model 'Legality'
        db.create_table('magic_legality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Card'])),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Format'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('magic', ['Legality'])

        # Adding model 'Deck'
        db.create_table('magic_deck', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('magic', ['Deck'])

        # Adding model 'DeckCard'
        db.create_table('magic_deckcard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deck', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Deck'])),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Card'])),
            ('sideboard', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('magic', ['DeckCard'])

        # Adding unique constraint on 'DeckCard', fields ['deck', 'card', 'sideboard']
        db.create_unique('magic_deckcard', ['deck_id', 'card_id', 'sideboard'])

        # Adding model 'Collection'
        db.create_table('magic_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('magic', ['Collection'])

        # Adding model 'CollectionCard'
        db.create_table('magic_collectioncard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Collection'])),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Card'])),
        ))
        db.send_create_signal('magic', ['CollectionCard'])

        # Adding unique constraint on 'CollectionCard', fields ['collection', 'card']
        db.create_unique('magic_collectioncard', ['collection_id', 'card_id'])

        # Adding model 'CollectionPrinting'
        db.create_table('magic_collectionprinting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Collection'])),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('printing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['magic.Printing'])),
        ))
        db.send_create_signal('magic', ['CollectionPrinting'])

        # Adding unique constraint on 'CollectionPrinting', fields ['collection', 'printing']
        db.create_unique('magic_collectionprinting', ['collection_id', 'printing_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CollectionPrinting', fields ['collection', 'printing']
        db.delete_unique('magic_collectionprinting', ['collection_id', 'printing_id'])

        # Removing unique constraint on 'CollectionCard', fields ['collection', 'card']
        db.delete_unique('magic_collectioncard', ['collection_id', 'card_id'])

        # Removing unique constraint on 'DeckCard', fields ['deck', 'card', 'sideboard']
        db.delete_unique('magic_deckcard', ['deck_id', 'card_id', 'sideboard'])

        # Removing unique constraint on 'ManaCost', fields ['mana_symbol', 'count']
        db.delete_unique('magic_manacost', ['mana_symbol_id', 'count'])

        # Deleting model 'Color'
        db.delete_table('magic_color')

        # Deleting model 'ManaSymbol'
        db.delete_table('magic_manasymbol')

        # Removing M2M table for field colors on 'ManaSymbol'
        db.delete_table('magic_manasymbol_colors')

        # Deleting model 'ManaCost'
        db.delete_table('magic_manacost')

        # Deleting model 'SuperType'
        db.delete_table('magic_supertype')

        # Deleting model 'CardType'
        db.delete_table('magic_cardtype')

        # Deleting model 'SubType'
        db.delete_table('magic_subtype')

        # Deleting model 'Set'
        db.delete_table('magic_set')

        # Deleting model 'Rarity'
        db.delete_table('magic_rarity')

        # Deleting model 'Ruling'
        db.delete_table('magic_ruling')

        # Deleting model 'Card'
        db.delete_table('magic_card')

        # Removing M2M table for field mana_cost on 'Card'
        db.delete_table('magic_card_mana_cost')

        # Removing M2M table for field super_types on 'Card'
        db.delete_table('magic_card_super_types')

        # Removing M2M table for field card_types on 'Card'
        db.delete_table('magic_card_card_types')

        # Removing M2M table for field sub_types on 'Card'
        db.delete_table('magic_card_sub_types')

        # Removing M2M table for field colors on 'Card'
        db.delete_table('magic_card_colors')

        # Removing M2M table for field rulings on 'Card'
        db.delete_table('magic_card_rulings')

        # Deleting model 'Printing'
        db.delete_table('magic_printing')

        # Deleting model 'Block'
        db.delete_table('magic_block')

        # Removing M2M table for field sets on 'Block'
        db.delete_table('magic_block_sets')

        # Deleting model 'Format'
        db.delete_table('magic_format')

        # Removing M2M table for field sets on 'Format'
        db.delete_table('magic_format_sets')

        # Deleting model 'Legality'
        db.delete_table('magic_legality')

        # Deleting model 'Deck'
        db.delete_table('magic_deck')

        # Deleting model 'DeckCard'
        db.delete_table('magic_deckcard')

        # Deleting model 'Collection'
        db.delete_table('magic_collection')

        # Deleting model 'CollectionCard'
        db.delete_table('magic_collectioncard')

        # Deleting model 'CollectionPrinting'
        db.delete_table('magic_collectionprinting')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'magic.block': {
            'Meta': {'ordering': "['name']", 'object_name': 'Block'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Set']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'magic.card': {
            'Meta': {'ordering': "['name']", 'object_name': 'Card'},
            'ascii_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '141'}),
            'card_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.CardType']", 'symmetrical': 'False'}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Color']", 'symmetrical': 'False', 'blank': 'True'}),
            'converted_power': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'converted_toughness': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'hand_modifier': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'life_modifier': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'loyalty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'mana_cost': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.ManaCost']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '141'}),
            'other_card': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['magic.Card']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'power': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rules_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rulings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Ruling']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '141'}),
            'sub_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.SubType']", 'symmetrical': 'False', 'blank': 'True'}),
            'super_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.SuperType']", 'symmetrical': 'False', 'blank': 'True'}),
            'toughness': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'magic.cardtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'CardType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '12'})
        },
        'magic.collection': {
            'Meta': {'object_name': 'Collection'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Card']", 'through': "orm['magic.CollectionCard']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Printing']", 'through': "orm['magic.CollectionPrinting']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'magic.collectioncard': {
            'Meta': {'unique_together': "(['collection', 'card'],)", 'object_name': 'CollectionCard'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Card']"}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'magic.collectionprinting': {
            'Meta': {'unique_together': "(['collection', 'printing'],)", 'object_name': 'CollectionPrinting'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'printing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Printing']"})
        },
        'magic.color': {
            'Meta': {'ordering': "['name']", 'object_name': 'Color'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '1'})
        },
        'magic.deck': {
            'Meta': {'ordering': "['name']", 'object_name': 'Deck'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Card']", 'through': "orm['magic.DeckCard']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'magic.deckcard': {
            'Meta': {'ordering': "['sideboard', 'card__name']", 'unique_together': "(['deck', 'card', 'sideboard'],)", 'object_name': 'DeckCard'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Card']"}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Deck']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sideboard': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'magic.format': {
            'Meta': {'ordering': "['name']", 'object_name': 'Format'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Card']", 'symmetrical': 'False', 'through': "orm['magic.Legality']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Set']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'})
        },
        'magic.legality': {
            'Meta': {'ordering': "['card__name']", 'object_name': 'Legality'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Card']"}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Format']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'magic.manacost': {
            'Meta': {'unique_together': "(['mana_symbol', 'count'],)", 'object_name': 'ManaCost'},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mana_symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.ManaSymbol']"})
        },
        'magic.manasymbol': {
            'Meta': {'ordering': "['value', 'name']", 'object_name': 'ManaSymbol'},
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['magic.Color']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'magic.printing': {
            'Meta': {'ordering': "['-set__release_date', 'number', 'card__name']", 'object_name': 'Printing'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Card']"}),
            'flavor_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'rarity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Rarity']"}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magic.Set']"})
        },
        'magic.rarity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rarity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '1'})
        },
        'magic.ruling': {
            'Meta': {'object_name': 'Ruling'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'magic.set': {
            'Meta': {'ordering': "['name']", 'object_name': 'Set'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '39'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '39'})
        },
        'magic.subtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'SubType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '24'})
        },
        'magic.supertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'SuperType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '9'})
        }
    }

    complete_apps = ['magic']