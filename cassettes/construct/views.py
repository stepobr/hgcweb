from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import FileResponse,HttpResponse
from cassettes.construct.models import Cassette,CassetteAssembly,Step,Workstation,Modulemap
from django.views.generic import CreateView,ListView,UpdateView,FormView
from .forms import PlacePart,CassetteForm,WorkstationForm, CassetteAssemblyForm
from .utils import generate_svg


# Create your views here.

def myView(request):
  return render(request, "construct/create.html")

# def WorkstationUpdate(request,parent_id):
#     selectedworkstation = Workstation.objects.get(pk=parent_id)
#     selectedworkstation.cassette = Cassette.objects.get(workstation = selectedworkstation)
#     selectedworkstation.save()
#     return redirect('workstation_view')

class CassetteCreate(CreateView):
  model = Cassette
  form_class = CassetteForm
  template_name = 'construct/create.html'
  def get_success_url(self):
    workstation_id = self.object.workstation.pk
    return reverse_lazy('workstation_update', kwargs={'parent_id': workstation_id})

def create_cassette_assembly(request):
    if request.method == 'POST':
        form = CassetteAssemblyForm(request.POST)
        if form.is_valid():
            cassette_assembly = form.save()
            name = str(form.cleaned_data['cassette_name'])
            layer = str(int(name.replace('CEE',''))*2 + int(form.cleaned_data['side']) - 2)
            parts = Modulemap.objects.filter(icassette="1",plane=layer)
            #cassette_barcode = form.cleaned_data['cassette_barcode']
            cassette = Cassette.objects.get(barcode = form.cleaned_data['cassette_barcode'])
            for part in parts:
               cassette_assembly = CassetteAssembly.objects.create()
               cassette_assembly.cassette = cassette
               cassette_assembly.workstation = Workstation.objects.get(name=form.cleaned_data['cassette_workstation'])
               cassette_assembly.layer = int(layer)
               cassette_assembly.step = Step.objects.get(name = 1)
               cassette_assembly.module = part
               cassette_assembly.side = form.cleaned_data['side']
               cassette_assembly.save()

            return redirect('workstation_view')  # Redirect to a success page after creating the models
    else:
        form = CassetteAssemblyForm()
    return render(request, 'construct/create.html', {'form': form})

  

class WorkstationView(ListView):
  model = Workstation
  template_name = 'construct/work.html'
  def get_context_data(self):
    context = super().get_context_data()
    context["workstations"] = Workstation.objects.all()
    context["cassettes"] = Cassette.objects.all()
    context["cassetteassemblies"] = CassetteAssembly.objects.select_related('workstation')
    return context

class StepView(ListView):
  model = Step
  template_name = 'construct/steps.html'
  def get_context_data(self):
    context = super().get_context_data()
    context["steps"] = Step.objects.all()
    return context

def view_step(request, parent_id):
    cassetteinstance = CassetteAssembly.objects.filter(layer=parent_id)[0]
    stepinstance = Step.objects.filter(pk=str(cassetteinstance.step))
    svg_str = generate_svg(parent_id)
    context = {'svg_str': svg_str, 'cassetteinstance':cassetteinstance, 'stepinstance':stepinstance}
    return render(request, 'construct/assembly.html', context)

def place_part(request,parent_id):
    module = CassetteAssembly.objects.get(pk=request.POST.get('id'))
    form = PlacePart(request.POST,instance=module)
    if form.is_valid():
        print (form)
        module.barcode = form.cleaned_data['barcode']
        module.placed = True
        module.save()
    return redirect('view_step', parent_id=parent_id)

def next_step(request,parent_id):
    cassette = CassetteAssembly.objects.filter(layer=parent_id)
    for cas in cassette:
       cas.step = Step.objects.get(pk=(cas.step.name + 1))
       cas.save()
    return redirect('view_step', parent_id=parent_id)

def prev_step(request,parent_id):
    cassette = CassetteAssembly.objects.filter(layer=parent_id)
    for cas in cassette:
       if cas.step.name > 1:
        cas.step = Step.objects.get(pk=(cas.step.name - 1))
        cas.save()
    return redirect('view_step', parent_id=parent_id)
