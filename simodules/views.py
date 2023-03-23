from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime

from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.views.generic.base import TemplateView

from django.db import connections
import os
# from django.db import connection
from .models import VisualInspection, Part
from base.models import HGCROCTest, CondRun


def index(request):
    query="SELECT PART_ID, KIND_OF_PART_ID, BATCH_NUMBER, BARCODE, SERIAL_NUMBER, LOCATION_ID FROM CMS_HGC_CORE_CONSTRUCT.PARTS WHERE KIND_OF_PART_ID IN (8200, 8220, 16580,16620,16600,16460,16560,16540,16520,16500,16360,16440,16420,16400,16380,16260,16340,16320,16300,16240,16180,16200,16060,16160,16140,16120,16100,15960,16040,16020,16000,15980,15860,15940,15920,15900,15840,15740,15800,15780,15760,15640,15720,15700,15660,15540,15620,15600,15580,15560,15440,15520,15500,15460,15360,15400,15380,15260,15340,15320,15300,15140,15240,15220,15200,15180,15160,15040,15120,15100,15060) AND is_record_deleted='F'"
    res = connections['construct-dev'].cursor().execute(query)
    modules_all = res.fetchall()
    return render(request, 'si_index.html', {'modules_all': modules_all})

def pcbs(request):
    # PCB_HD_FULL = 14000, PCB_LD_FULL = 14120
    # pcbs_full_all = Parts.objects.filter(kind_of_parts_id=14120).filter(kind_of_parts_id=14000).use('construct-dev')
    # pcbs_full_all = Parts.objects.raw("SELECT * FROM CMS_HGC_CORE_CONSTRUCT.PARTS WHERE KIND_OF_PART_ID=14120 OR KIND_OF_PART_ID=14000 AND is_record_deleted='F'").using('construct-dev')
    
    the_query  = "SELECT PART_ID, KIND_OF_PART_ID, BARCODE, SERIAL_NUMBER, LOCATION_ID, MANUFACTURER_ID, PRODUCTION_DATE FROM CMS_HGC_CORE_CONSTRUCT.PARTS WHERE KIND_OF_PART_ID=14120 OR KIND_OF_PART_ID=14000 AND is_record_deleted='F'"
    res = connections['construct-dev'].cursor().execute(the_query)
    pcbs_full_all = res.fetchall()

    return render(request, 'pcbs.html', {'pcbs_full_all': pcbs_full_all})

def pcb_view(request, pcb_id):
    query="SELECT BARCODE, BATCH_NUMBER, KIND_OF_PART_ID, LOCATION_ID, SERIAL_NUMBER, VERSION, PRODUCTION_DATE, INSTALLED_DATE  FROM CMS_HGC_CORE_CONSTRUCT.PARTS WHERE PART_ID={} AND is_record_deleted='F'".format(pcb_id)
    res = connections['construct-dev'].cursor().execute(query)
    pcb = res.fetchall()
    return render(request, 'pcb_view.html', {'pcb': pcb})


def hgcrocs(request):
    # cr = CondRun.objects.filter(cond_run_id=12180)
    roc = HGCROCTest( hgcroc_status='PASSED',
                     comments='InsTest')
    roc.save(using='construct-dev')
    return render(request, 'hgcrocs.html')


def qc_pcb(request):
    the_query  = "select * from CMS_HGC_HGCAL_COND.HGC_BARE_PCB_DATA"
    res = connections['construct-dev'].cursor().execute(the_query)
    query_output = res.fetchall()

    qc_visual_data_new = VisualInspection.objects.all()

    data = {'data': query_output, 'qc_visual_data_new':qc_visual_data_new }

    return render(request, 'qc_pcb.html', data)

class QCNewVisual(View):
    template_name = 'qc_new_visual.html'

    def get(self, request):
        # do it normally 
        if request.session.get('user'):
            username = request.session.get('user')
        else:
            username = None

        response_data = {'user':username}
        return render(request, self.template_name, response_data)
    
    def post(self, request, *args, **kwargs):
        # do it normally 
        if request.session.get('user'):
            username = request.session.get('user')['name']
        else:
            username = None
        ##
        if request.POST.get('test_date'):
            test_date = datetime.strptime(request.POST.get('test_date'),"%Y-%m-%d") 
        else:
            test_date = datetime.now()


        board_id              = request.POST.get('board_id')
        # test_date             = datetime.now() 
        test_type             = request.POST.get('test_type')
        input_manufacturer    = request.POST.get('input_manufacturer')
        input_batch           = request.POST.get('input_batch')
        input_version         = request.POST.get('input_version')
        comments_general      = request.POST.get('comments_general')
        input_thickness       = request.POST.get('input_thickness')
        switch_flatness       = self.switch_correction(request.POST.get('switch_flatness'))
        comment_flatness      = request.POST.get('comment_flatness')
        switch_plating_bga    = self.switch_correction(request.POST.get('switch_plating_bga'))
        comment_plating_bga   = request.POST.get('comment_plating_bga')
        switch_plating_holes  = self.switch_correction(request.POST.get('switch_plating_holes'))
        comment_plating_holes = request.POST.get('comment_plating_holes')
        switch_soldermask     = self.switch_correction(request.POST.get('switch_soldermask'))
        comment_soldermask    = request.POST.get('comment_soldermask')
        switch_glue           = self.switch_correction(request.POST.get('switch_glue'))
        comment_glue          = request.POST.get('comment_glue')
        switch_accepted       = self.switch_correction(request.POST.get('switch_accepted'))
        file_pcb_photo        = request.POST.get('file_pcb_photo')

        vis = VisualInspection( pcb_id        = board_id,
                                test_date     = test_date,
                                tested_by     = username,
                                stage         = test_type,
                                comments      = comments_general,
                                flatness      = switch_flatness,
                                thikness      = input_thickness,
                                plating_bga   = switch_plating_bga,
                                plating_holes = switch_plating_holes,
                                mask_aligment = switch_soldermask,
                                glue          = switch_glue,
                                accepted      = switch_accepted )
        vis.save()
        
        # file handler
        uploaded_file_url = ""
        if request.FILES:
            pcbfile = request.FILES['file_pcb_photo']
            fs = FileSystemStorage(location='media/visual')
            file_extention = os.path.splitext(pcbfile.name)[1]
            new_file_name =  "pcb-{}-{}{}".format(board_id, test_type, file_extention)
            filename = fs.save(new_file_name, pcbfile)
            uploaded_file_url = fs.url(filename)


        # response_data = {"Success": True }
        response_data = {
            "Board":                 board_id,             
            "Test Date":             test_date,         
            "test_type":             test_type,
            "input_manufacturer":    input_manufacturer,
            "input_batch":           input_batch,
            "input_version":         input_version,
            "comments_general":      comments_general,
            "input_thickness":       input_thickness,
            "switch_flatness":       switch_flatness,
            "comment_flatness":      comment_flatness,
            "switch_plating_bga":    switch_plating_bga,
            "comment_plating_bga":   comment_plating_bga,
            "switch_plating_holes":  switch_plating_holes,
            "comment_plating_holes": comment_plating_holes,
            "switch_soldermask":     switch_soldermask,
            "comment_soldermask":    comment_soldermask,
            "switch_glue":           switch_glue,
            "comment_glue":          comment_glue,
            "switch_accepted":       switch_accepted,
            "uploaded_file_url":     uploaded_file_url,
            "user":                  username
            }
        
        
        return JsonResponse(response_data)
    
    
    def switch_correction(self, switch):
        if switch == "on":
            return "OK"
        elif switch == None:
            return "FAIL"
        else:
            return "FAIL"



def qc_new_electrical(request):
    return render(request, 'qc_new_electrical.html')


def qc_add_visual(request):
    # save_path = os.path.join(settings.MEDIA_ROOT, 'visual', request.FILES['file'])
    # path = default_storage.save(save_path, request.FILES['file'])
    # document = Document.objects.create(document=path, upload_by=request.user)
    # return JsonResponse({'document': document.id})
    pass




# plots test
import plotly.graph_objects as go


class Graph(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):

        query_electrical  = "SELECT PWR_ON_ANLG_WATTS, INIT_ANLG_WATTS FROM CMS_HGC_HGCAL_COND.HGC_BARE_PCB_ELEC_DATA"
        res = connections['construct-dev'].cursor().execute(query_electrical)
        query_el_output = res.fetchall()
        
        pwr_on = []
        pwr_init = []
        for output in query_el_output:
            pwr_on.append(output[0])
            pwr_init.append(output[1])
        


        context = super(Graph, self).get_context_data(**kwargs)

        # x1 = [-2,4,4,6,7]
        # x2 = [-2,0,6,3,7]
        # y = [q**2-q+3 for q in x1]
        x = [x * 0.1 for x in range(2, 3)]
        y1 = pwr_on #[x * 0.1 for x in range(2, 3)]
        y2 = pwr_init
        trace1 = go.Scatter(y=y1, marker={'color': 'red', 'symbol': 104, 'size': (0,10)},
                            mode="lines",  name='PWR_ON_ANLG_WATTS')
        trace2 = go.Scatter(y=y2, marker={'color': 'green', 'symbol': 104, 'size': (0,10)},
                            mode="lines",  name='INIT_ANLG_WATTS')

        layout=go.Layout(title="Power", xaxis={'title':'boards'}, yaxis={'title':'watts'})
        figure=go.Figure(data=[trace1,trace2], layout=layout)

        context['graph'] = figure.to_html()


        # flatness  = "select FLATNESS from CMS_HGC_HGCAL_COND.HGC_BARE_PCB_DATA"
        # res = connections['construct-dev'].cursor().execute(flatness)
        # flatness_output = res.fetchall()
        # x2 = [a * 1 for a in range(0, 38)]
        # bars = go.Bar(x=flatness_output)
        # layout_bars = go.Layout(title=go.layout.Title(text="A Figure Specified By A Graph Object"))
        # figure_bar = go.Figure(data=bars,layout=layout_bars)
        # context['bar'] = figure_bar.to_html()

        return context