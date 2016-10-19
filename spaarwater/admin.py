'''
Created on Oct 18, 2016

@author: theo
'''
from django.contrib.admin import AdminSite

class SpaarwaterAdminSite(AdminSite):
    site_header = 'Spaarwater beheer'

admin_site = SpaarwaterAdminSite(name='admin')
