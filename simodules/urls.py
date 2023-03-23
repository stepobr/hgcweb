from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='simodules'),
    
    # path('modules/', views.parts, name='modules'),
    # path('module/view/<int:mod_id>', views.parts, name='modules'),
    # path('module/new', views.parts, name='modules'),
    # path('module/edit', views.parts, name='modules'),

    path('hgcrocs/', views.hgcrocs, name='hgcrocs'),
    # path('hgcrocs/<int:roc_id>', views.hgcroc, name='hgcroc'),

    path('pcbs/', views.pcbs, name='pcbs'),
    path('pcb/view/<int:pcb_id>', views.pcb_view, name='pcb_view'),
    # path('modules/pcb/new', views.pcb_new, name='pcb_new'),
    
    path('pcbs/qc', views.qc_pcb, name='qc_pcb'),
    # path('pcbs/qc/new-visual', views.qc_new_visual, name='qc_new_visual'),
    path('pcbs/qc/new-visual',views.QCNewVisual.as_view(), name='qc_new_visual'),

    # path('qc/add-visual', views.qc_add_visual, name='qc_add_visual'),
    path('pcbs/qc/new-electrical', views.qc_new_electrical, name='qc_new_electrical'),

    path('pcbs/statistics',views.Graph.as_view(), name='pcb_stats'),
]