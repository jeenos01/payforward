from mercurial.dispatch import request
from django.shortcuts import render_to_response, redirect
from tasks.models import *
from forms import *
from django.template import RequestContext
from django.http import HttpResponseBadRequest
from users.views import complete_registration
import random
from loginza.models import UserMap
from django.utils import simplejson as json
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    tasks = Task.objects.all()
    important_tasks = tasks.order_by('-rate')[0:4]
    fresh_tasks = tasks.order_by('-create_date')[0:4]
    response = {'important_tasks':important_tasks,'fresh_tasks':fresh_tasks}
    if 'users_complete_reg_id' in request.session:
        form = complete_registration(request)
        response['form'] = form

    if request.user.is_authenticated():
        try:
            user_map  = UserMap.objects.get(user=request.user)
            data = json.loads(user_map.identity.data)
            response['avatar'] = data.get('photo', None)
        except ObjectDoesNotExist:
            pass



    return render_to_response('index.html',response, context_instance=RequestContext(request))

def create_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, request.FILES,)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.task_photo:
                number = random.randint(1,6)
                task.task_photo = 'task_photos/page4-img'+str(number)+'.jpg'
            task.user = request.user
            task.save()
            return redirect('/task/'+str(task.id))
    return HttpResponseBadRequest()

def tasks(request):
    tasks = Task.objects.all()

    return render_to_response('tasks.html',{'tasks':tasks})

def task(request,task_id):
    task = Task.objects.get(id=task_id)
    tasks = Task.objects.exclude(id=task_id)[0:3]

    return render_to_response('task.html',{'task':task, 'tasks':tasks})

def profile(request,user_id):
    return render_to_response('profile.html')

def people(request):
    return render_to_response('people.html')
