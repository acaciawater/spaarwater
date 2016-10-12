# -*- coding: utf-8 -*-
'''
Created on May 19, 2016

@author: theo
'''
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt

from acacia.data.models import MeetLocatie, KeyFigure
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.response import TemplateResponse
import datetime, math, pytz
utc=pytz.UTC

templates = {'gauge': 'pict/gauge.html',
             'column': 'pict/column.html'
             }

class VisualizeView(TemplateView):

    def get_context_data(self, **kwargs):
        type = self.request.GET.get('type', 'column')
        primkeys = self.request.GET.get('values', 0)
        title = self.request.GET.get('title', '')
        ymax = self.request.GET.get('ymax', '25000.0')
        context = super(VisualizeView,self).get_context_data(**kwargs)
        self.template_name = templates[type]
        keyfigure_keys = primkeys.split(',')
        if type == 'column':
            context['ymax'] = ymax
            opvang = KeyFigure.objects.get(pk=keyfigure_keys[0])
            afvoer = KeyFigure.objects.get(pk=keyfigure_keys[1])
            context['opvang'] = str(opvang.value)
            context['afvoer'] = str(afvoer.value)
            if min(opvang.last_update,afvoer.last_update) < utc.localize((datetime.datetime.now() - datetime.timedelta(days=3))):
                context['too_old'] = 1
            else:
                context['too_old'] = 0
        if type == 'gauge':
            kf = KeyFigure.objects.get(pk=keyfigure_keys[0])
            context['value'] = str(kf.value)
            if title == '':
                title = kf.name
        context['title'] =  title
        return context

class PictureView(TemplateView):
    template_name = 'picture.html'
     
    def get_context_data(self, **kwargs):
        context = super(PictureView,self).get_context_data(**kwargs)
        pk = context.get('pk',1)
        locatie = get_object_or_404(MeetLocatie,pk=pk)
        context['locatie'] = locatie
        keys = KeyFigure.objects.filter(locatie=locatie)
        for key in keys:
            context[key.name] = str(key.value)
        return context    
         
class PFView(PictureView):
    template_name = 'pict/pf.html'
     
class PFDripView(PFView):
    template_name = 'pict/pfdrip.html'
     
class PFRefView(PFView):
    template_name = 'pict/pfref.html'
 
class InfiltratieView(PictureView):
    template_name = 'pict/infiltratie.html'
         
class OpslagView(PictureView):
    template_name = 'pict/opslag.html'