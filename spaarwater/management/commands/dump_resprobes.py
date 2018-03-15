'''
Created on Mar 15, 2018

@author: theo
'''
'''
Created on Feb 13, 2014

@author: theo
'''
from django.core.management.base import BaseCommand
from acacia.data.models import Series
import os,logging
import pandas as pd

logger = logging.getLogger('acacia.data')
resprobes = (502,687)

class Command(BaseCommand):
    args = ''
    help = 'Dumps all series as csv files'
    
    def add_arguments(self,parser):
        
        parser.add_argument('-d', '--dest',
                action='store',
                dest = 'dest',
                default = '.',
                help = 'destination folder')

        parser.add_argument('-p', '--pk',
                action='store',
                type = int,
                dest = 'pk',
                default = None,
                help = 'dump single series')

    def handle1(self, *args, **options):
        dest = options.get('dest', '.')
        pk = options.get('pk', None)
        if pk is None:
            series = Series.objects.filter(pk__range=resprobes)
        else:
            series = Series.objects.filter(pk=pk)
        data = [s.to_pandas() for s in series]
        names = [s.pk for s in series]
        series_data = dict(zip(names,data))
        df = pd.DataFrame(series_data)
        df.to_csv('resprobes.csv')

    def handle(self, *args, **options):
        dest = options.get('dest', '.')
        if not os.path.exists(dest):
            os.makedirs(dest)
        pk = options.get('pk', None)
        if pk is None:
            series = Series.objects.filter(pk__range=resprobes)
        else:
            series = Series.objects.filter(pk=pk)
        for s in series:
            print s.id, s
            filename = os.path.join(dest,'{}.csv'.format(s.pk))
            with open(filename,'w') as f:
                for p in s.datapoints.order_by('date'):
                    f.write('{},{},{},{}\n'.format(p.id,p.series_id,p.date.strftime('%d/%m/%Y %H:%M'),p.value))
        