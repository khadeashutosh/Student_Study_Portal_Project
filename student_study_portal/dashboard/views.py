from django.shortcuts import render, redirect
from . forms import*
from django.contrib import messages
from django.views import generic

def home(request):
  return render(request,'dashboard/home.html')

def notes(request):
  if request.method =='POST':
    form= NotesForm(request.POST)
    if form.is_valid():
      notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
      notes.save()
    messages.success(request,f"Notes Added from {request.user.username} Successfully")  
  else:
    form = NotesForm()
  notes=Notes.objects.filter(user=request.user)
  context={'notes':notes ,'form':form}
  return render(request,'dashboard/notes.html',context)

def delete_notes(request,pk=None):
  Notes.objects.get(id=pk).delete()
  return redirect ("notes")

class Notes_Detail_View(generic.DetailView):
  model=Notes

def homework(request):
  homework= Homework.objects.filter(user=request.user)
  
  return render (request, 'dashboard/homework.html')  