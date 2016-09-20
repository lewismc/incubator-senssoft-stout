# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.shortcuts import render, redirect
from op_tasks.models import UserProfile, Product, Dataset, OpTask, TaskListItem, Experiment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from base import LOGIN_URL

def user_authorized(request):
	user = request.user
	return user.is_staff


@login_required(login_url=LOGIN_URL)
def view_tasks(request):
	if user_authorized(request):
		tasks = OpTask.objects.all()
		datasets = Dataset.objects.all()
		return render(request, 'tasks.html', {'tasks': tasks, 'datasets':datasets})


@login_required(login_url=LOGIN_URL)
def view_completed(request):
	if user_authorized(request):
		completed_tasks = TaskListItem.objects.all().filter(task_complete=True).order_by('-date_complete')
		return render(request, 'completed.html', {'completed_tasks': completed_tasks})



@login_required(login_url=LOGIN_URL)
def view_incomplete(request):
	if user_authorized(request):
		incomplete_tasks = TaskListItem.objects.all().filter(task_complete=False)
		return render(request, 'incomplete.html', {'incomplete_tasks': incomplete_tasks})


@login_required(login_url=LOGIN_URL)
def add_task(request):
	if user_authorized(request):
		datasets = Dataset.objects.all()
		return render(request, 'add_task.html', {'datasets': datasets})


@login_required(login_url=LOGIN_URL)
def new_task(request):
	if user_authorized(request):
		dataset = Dataset.objects.get(name=request.POST['task_dataset'])
		task = OpTask()
		task.dataset = dataset
		task.survey_url = request.POST['task_url']
		task.name = request.POST['task_name']
		task.instructions = request.POST['task_instructions']
		task.exit_url = request.POST['task_exit_url']
		task.save()
		return redirect('exp_portal:view_tasks')


@login_required(login_url=LOGIN_URL)
def manage_tasks(request):
	if user_authorized(request):
		return view_tasks(request)


@login_required(login_url=LOGIN_URL)
def view_task_details(request, taskname):
	if user_authorized(request):
		task = OpTask.objects.all().filter(name=taskname)[0]
		datasets = Dataset.objects.all()
		print task.dataset.name
		for dataset in datasets:
			print dataset.name
		return render(request, 'task_details.html', {'task': task, 'datasets': datasets})


@login_required(login_url=LOGIN_URL)
def edit_task(request, taskpk):
	if user_authorized(request):
		task = OpTask.objects.get(id=taskpk)
		task.name = request.POST['task_name']
		task.survey_url = request.POST['task_url']
		task.exit_url = request.POST['task_exit_url']
		task.instructions =request.POST['task_instructions']
		dataset = Dataset.objects.get(name=request.POST['task_dataset'])
		task.dataset = dataset
		task.is_active = request.POST.get('task_active', False)
		task.save()
		return redirect('exp_portal:view_tasks')


@login_required(login_url=LOGIN_URL)
def delete_task(request, taskpk):
	if user_authorized(request):
		task = OpTask.objects.get(id=taskpk)
		task.delete()
		return redirect('exp_portal:view_tasks')
