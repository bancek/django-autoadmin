from django.db import models as django_models
from django.contrib import admin
from django.utils.text import truncate_words
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.utils.html import escape
from django.contrib import databrowse
from django.conf import settings

class Dummy(list):
    id = 1
    pk = 1
    
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    
    def __getattr__(self, *args, **kwargs):
        return Dummy()
    
    def __setattr__(self, *args, **kwargs):
        return Dummy()
    
    def __getitem__(self, *args, **kwargs):
        return Dummy()
    
    def __call__(self, *args, **kwargs):
        if 'app_label' in kwargs and 'model' in kwargs:
            return Dummy(*args, **kwargs), False
        return Dummy(*args, **kwargs)
    
    def model_class(self):
        return django_models.get_model(self.app_label, self.model)

if getattr(settings, 'AUTOADMIN_FAKEAUTH', False):
    fa_username = getattr(settings, 'AUTOADMIN_FAKEAUTH_USERNAME', '')
    fa_password = getattr(settings, 'AUTOADMIN_FAKEAUTH_PASSWORD', '')
    
    class User(object):
        id = 1
        pk = 1
        username = 'admin'
        first_name = 'Admin'
        last_name = ''
        email = ''
        is_active = True
        is_staff = True
        
        get_and_delete_messages = lambda *a,**kwa:[]
        message_set = Dummy()
        save = Dummy()
        
        is_authenticated = lambda self, *args, **kwargs: True
        has_module_perms = lambda self, *args, **kwargs: True
        has_perm = lambda self, *args, **kwargs: True

    class FakeAuth(object):
        user = User()
        
        def get_user(self, *args, **kwargs):
            return self.user
        
        def authenticate(self, username, password):
            if fa_username and fa_password:
                if fa_username == username and fa_password == password:
                    return self.user
            else:
                return self.user
    
    settings.AUTHENTICATION_BACKENDS.append('autoadmin.FakeAuth')
    
    #if model in admin.site._registry:
    #    admin.site.unregister(model)
    
    LogEntry.objects.filter = Dummy()
    LogEntry.objects.create = Dummy()
    LogEntry.save = Dummy()

    if getattr(settings, 'AUTOADMIN_FAKECONTENTTYPE', True):
        ContentType.objects.get_or_create = Dummy()

def autoadmin(allowed):
    def col(field):
        if isinstance(field, django_models.ForeignKey):
            def func(obj):
                f = getattr(obj, field.name)
                url_name = 'admin:%s_%s_change' % (f._meta.app_label,
                                                   f._meta.module_name)
                url = urlresolvers.reverse(url_name, args=(f.pk,))
                name = escape(truncate_words(unicode(f), 10))
                return u'<a href="%s">%s</a>' % (url, name)
            
            func.allow_tags = True
        else:
            def func(obj):
                return truncate_words(unicode(getattr(obj, field.name)), 10)
        
        func.short_description = field.name
        func.admin_order_field = field.name
        
        return func
    
    is_text = lambda x: isinstance(x, (django_models.CharField,
                                           django_models.TextField))
    is_fk = lambda x: isinstance(x, django_models.ForeignKey)
    
    for model in django_models.get_models():
        if model._meta.app_label == allowed:
            searchable = [f.name for f in model._meta.fields if is_text(f)]
            cols = [col(f) for f in model._meta.fields]
            fkeys = [f.name for f in model._meta.fields if is_fk(f)]
            
            class DummyModelAdmin(admin.ModelAdmin):
                search_fields = searchable
                list_display = cols
                raw_id_fields = fkeys
            
            admin.site.register(model, DummyModelAdmin)
            
            if (not getattr(model, '__unicode__', None)
                        and model.__str__ == django_models.Model.__str__):
                
                model.__unicode__ = lambda self: u'<%s pk=%d>' % (
                                        self.__class__.__name__, self.pk or 0)

def autodatabrowse(allowed):
    for model in django_models.get_models():
        if model._meta.app_label == allowed:
            databrowse.site.register(model)
