from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import FileResponse,HttpResponse
from cassettes.construct.models import Cassette,Part,Step,Workstation,Modulemap
from django.views.generic import CreateView,ListView,UpdateView,FormView
from .forms import PlacePart,CassetteForm,WorkstationForm
from .utils import generate_svg


# Create your views here.

def myView(request):
  return render(request, "construct/create.html")

def WorkstationUpdate(request,parent_id):
    selectedworkstation = Workstation.objects.get(pk=parent_id)
    selectedworkstation.cassette = Cassette.objects.get(workstation = selectedworkstation)
    selectedworkstation.save()
    return redirect('workstation_view')

class CassetteCreate(CreateView):
  model = Cassette
  form_class = CassetteForm
  template_name = 'construct/create.html'
  def get_success_url(self):
    workstation_id = self.object.workstation.pk
    return reverse_lazy('workstation_update', kwargs={'parent_id': workstation_id})
  

class WorkstationView(ListView):
  model = Workstation
  template_name = 'construct/work.html'
  def get_context_data(self):
    context = super().get_context_data()
    context["workstations"] = Workstation.objects.all()
    context["cassettes"] = Cassette.objects.all()
    return context

class StepView(ListView):
  model = Step
  template_name = 'construct/steps.html'
  def get_context_data(self):
    context = super().get_context_data()
    context["steps"] = Step.objects.all()
    return context

def view_step(request, parent_id):
    cassetteinstance = Cassette.objects.filter(pk=parent_id)
    stepinstance = Step.objects.filter(pk=str(cassetteinstance[0].step))
    svg_str = generate_svg(parent_id)
    context = {'svg_str': svg_str, 'cassetteinstance':cassetteinstance, 'stepinstance':stepinstance}
    return render(request, 'construct/assembly.html', context)

def place_part(request,parent_id):
    module = Part.objects.get(pk=request.POST.get('id'))
    form = PlacePart(request.POST,instance=module)
    if form.is_valid():
        print (form)
        module.barcode = form.cleaned_data['barcode']
        module.placed = True
        module.save()
    return redirect('view_step', parent_id=parent_id)

def next_step(request,parent_id):
    cassette = Cassette.objects.get(pk=parent_id)
    cassette_next_step = cassette.step + 1
    cassette.step = cassette_next_step
    cassette.save()
    return redirect('view_step', parent_id=cassette.id)

def prev_step(request,parent_id):
    cassette = Cassette.objects.get(pk=parent_id)
    if cassette.step > 1:
        cassette_next_step = cassette.step - 1
        cassette.step = cassette_next_step
    cassette.save()
    return redirect('view_step', parent_id=cassette.id)
