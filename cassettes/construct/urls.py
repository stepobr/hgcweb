from django.urls import path
from cassettes.construct.views import view_step, next_step, prev_step,place_part,CassetteCreate,WorkstationView,StepView,WorkstationUpdate
from . import views
urlpatterns = [
  path('view_step/<int:parent_id>/', view_step, name='view_step'),
  path('next_step/<int:parent_id>/', next_step, name='next_step'),
  path('prev_step/<int:parent_id>/', prev_step, name='prev_step'),
  path('place_part/<int:parent_id>/', place_part, name='place_part'),
  path('cassette_create',CassetteCreate.as_view(),name= "cassette_create"),
  path('',WorkstationView.as_view(),name= "workstation_view"),
  path('steps_view',StepView.as_view(),name= "steps_view"),
  path('workstation_update/<int:parent_id>/',WorkstationUpdate,name= "workstation_update"),
]
