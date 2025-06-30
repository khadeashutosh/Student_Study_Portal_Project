from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.shortcuts import render, redirect
from . forms import*
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch

import requests
import wikipedia
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
  return render(request,'dashboard/home.html')
@login_required
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

@login_required
def delete_notes(request,pk=None):
  Notes.objects.get(id=pk).delete()
  return redirect ("notes")
class Notes_Detail_View(generic.DetailView):
  model=Notes

@login_required
def homework(request):
  if request.method == 'POST':
    form = HomeworkForm(request.POST)
    if form.is_valid():
      try:
        finished = request.POST['is_finished']
        if finished == 'on':
          finished =True
        else:
          finished = False
      except :
        finished = False

      homeworks = Homework(
        user = request.user,
        subject =request.POST['subject'],
        title =request.POST['title'],
        description =request.POST['description'],
        due =request.POST['due'],
        is_finished =finished
      )        
      homeworks.save()
      messages.success(request,f'Homework Added from {request.user.username}!!')
  else:
    form = HomeworkForm()
  homework=Homework.objects.filter(user=request.user)
  if len (homework) ==0:
    homework_done = True
  else:
    homework_done = False  

  context={'homeworks':homework, 'homeworks_done':homework_done, 'form':form,}

  return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request, pk=None):
  homework = Homework.objects.get(id=pk)
  if homework.is_finished == True:
    homework.is_finished = False
  else:
    homework.is_finished = True  
  homework.save()
  return redirect('homework')

@login_required
def delete_homework(request,pk=None):
  Homework.objects.get(id=pk).delete()
  return redirect("homework")


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                video = VideosSearch(text, limit=10)
                results_raw = video.result().get('result', [])
                result_list = []

                for i in results_raw:
                    result_dict = {
                        'input': text,
                        'title': i.get('title'),
                        'duration': i.get('duration'),
                        'thumbnail': i.get('thumbnails', [{}])[0].get('url'),
                        'channel': i.get('channel', {}).get('name'),
                        'link': i.get('link'),
                        'views': i.get('viewCount', {}).get('short'),
                        'published': i.get('publishedTime'),
                        'description': ''.join([j.get('text', '') for j in i.get('descriptionSnippet', [])]) if i.get('descriptionSnippet') else ''
                    }
                    result_list.append(result_dict)

                context = {'form': form, 'results': result_list}
                return render(request, 'dashboard/youtube.html', context)
            except Exception as e:
                messages.error(request, f"Failed to fetch YouTube videos: {str(e)}")
    else:
        form = DashboardForm()

    return render(request, 'dashboard/youtube.html', {'form': form})

@login_required
def todo(request):
  if request.method == 'POST':
    form = TodoForm(request.POST)
    if form.is_valid():
      try:
        finished =request.POST['is_finished']
        if finished == 'on':
          finished = True

        else:
          finished = False

      except:
        finished = False
      
      todos = Todo(
        user = request.user,
        title = request.POST['title'],
        is_finished = finished

      )
      todos.save()
      messages.success(request, F'Todo added from {request.user.username}!!')
  else: 
    form = TodoForm()
  todo = Todo.objects.filter(user=request.user)
  if len(todo) == 0:
    todos_done = True
  else:
    todos_done = False  
  context = {
    'form': form,
    'todos' : todo,
    'todos_done' : todos_done
  }
  return render(request,'dashboard/todo.html',context)

@login_required
def update_todo(request,pk=None):
  todo =Todo.objects.get(id=pk)
  if todo.is_finished==True:
    todo.is_finished = False

  else:
    todo.is_finished =True

  todo.save()
  return redirect('todo')  

@login_required
def delete_todo(request, pk=None):
  Todo.objects.get(id=pk).delete()
  return redirect("todo")

def book(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
        r = requests.get(url)
        answer = r.json()
        result_list = []

        if 'items' in answer:
            for i in range(min(10, len(answer['items']))):
                item = answer['items'][i]
                volume_info = item.get('volumeInfo', {})
                image_links = volume_info.get('imageLinks', {})

                result_dict = {
                    'title': volume_info.get('title', 'No Title'),
                    'subtitle': volume_info.get('subtitle', ''),
                    'description': volume_info.get('description', ''),
                    'count': volume_info.get('pageCount', ''),
                    'categories': volume_info.get('categories', []),
                    'rating': volume_info.get('averageRating', ''),  # corrected to averageRating
                    'thumbnail': image_links.get('thumbnail', ''),
                    'preview': volume_info.get('previewLink', '#'),
                }
                result_list.append(result_dict)

        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/books.html', context)

    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/books.html', context)

def dictionary(request):
  if request.method == 'POST':
    form = DashboardForm(request.POST)
    text = request.POST.get('text', '')
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
    r = requests.get(url)
    answer = r.json()
    print("API Response:", answer)
    try:
      phonetics = answer[0].get('phonetics', [{}])[0].get('text', 'N/A')
      audio = answer[0].get('phonetics', [{}])[0].get('audio', 'N/A')
      meanings = answer[0].get('meanings', [])
      if meanings:
        definitions = meanings[0].get('definitions', [{}])
        definition = definitions[0].get('definition', 'Definition not available')
        example = definitions[0].get('example', 'Example not available')
        synonyms = definitions[0].get('synonyms', [])
      else:
        definition = 'Definition not available'
        example = 'Example not available'
        synonyms = []
      context = {'form': form, 'input': text, 'phonetics': phonetics, 'audio': audio, 'definition': definition, 'example': example, 'synonyms': synonyms}
    except Exception as e:
      print(f"Error: {e}")
      context = {'form': form, 'input': text, 'phonetics': 'N/A', 'audio': 'N/A', 'definition': 'Definition not available', 'example': 'Example not available', 'synonyms': []}
      return render(request, "dashboard/dictionary.html", context)
  else:
    form = DashboardForm()
    context = {'form': form}
  return render(request, "dashboard/dictionary.html", context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)

        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }

        except wikipedia.DisambiguationError as e:
            context = {
                'form': form,
                'title': f"Multiple results found for '{text}'",
                'options': e.options,
                'details': f"The term '{text}' is ambiguous. Please refine your search.",
            }

        except wikipedia.PageError:
            context = {
                'form': form,
                'title': "Page not found",
                'details': f"No results found for '{text}'. Try a different query."
            }

        return render(request, 'dashboard/wiki.html', context)

    form = DashboardForm()
    return render(request, 'dashboard/wiki.html', {'form': form})

def conversion(request):
  if request.method == 'POST':
    form = ConversionForm(request.POST)
    if request.POST['measurement'] == 'length':
      measurement_form =ConversionLengthForm()
      context = {
           'form':form, 
           'm_form':measurement_form,
           'input':True
      }
      if 'input' in request.POST:
        first = request.POST['measure1']
        second = request.POST['measure2']
        input = request.POST['input']
        answer = ''

        if input and int(input) >= 0:
          if first == 'yard' and second =='foot':
            answer = f'{input} yard = {int(input)*3} foot'
          
          if first == 'foot' and second =='yard':
            answer = f'{input} foot = {int(input)/3} yard'  
        context = {
          'form':form,
          'm_form':measurement_form,
          'input':True,
          'answer':answer
        }    

    if request.POST['measurement'] == 'mass':
      measurement_form =ConversionMassForm()
      context = {
           'form':form, 
           'm_form':measurement_form,
           'input':True
      }
      if 'input' in request.POST:
        first = request.POST['measure1']
        second = request.POST['measure2']
        input = request.POST['input']
        answer = ''

        if input and int(input) >= 0:
          if first == 'pound' and second =='kilogram':
            answer = f'{input} pound = {int(input)*0.453592} kilogram'
          
          if first == 'kilogram' and second =='pound':
            answer = f'{input} kilogram = {int(input)*2.20462} pound'  
        context = {
          'form':form,
          'm_form':measurement_form,
          'input':True,
          'answer':answer
        }   
  else:  
    form = ConversionForm()
    context = {
      'form':form,
      'input': False
     }
  return render(request,'dashboard/conversion.html',context)

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account Created for {username}!!')
      return redirect ("login")

  else:    
    form = UserCreationForm()
  context = {
    'form':form
    }
  return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
  homeworks = Homework.objects.filter(is_finished = False, user=request.user)
  todos = Todo.objects.filter(is_finished = False, user=request.user)
  if len(homeworks) == 0:
    homework_done =True
  else:
    homework_done =False

  if len(todos) == 0:
    todos_done=True
  else:
    todos_done=True
  
  context = {
    'homeworks': homeworks,
    'todos': todos,
    'homework_done':homework_done,
    'todos_done':todos_done
  }
  return render(request,'dashboard/profile.html',context)

def custom_logout(request):
    logout(request)
    return redirect('login')  