from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.decorators import user_is_project_author
from .models import Project
from .forms import ProjectRegisterForm, ProjectUpdateForm
from functions import *
from django.core.serializers import serialize

@login_required
def main(request):
    all_projects = Project.objects.all().order_by('-DatePosted')
    projects = get_filtered_projects(request, all_projects)
    # shellScript()

    if request.method == "POST" and request.POST['search']!="":
        projects = get_searched_projects(request)

    projects = get_paginated_projects(request, projects)
    projects_id = get_user_projects_id(request.user)

    common_tags = get_most_common_tags(5)

    context = {
        'title': 'Home',
        'users':User.objects.all(),
        'tags': Tag.objects.all(),
        'users_html':serialize("json", User.objects.all()),
        'tags_html':serialize("json", Tag.objects.all()),
        'projects': projects,
        'projects_id': projects_id,
        'notifications': Notification.objects.filter(user = request.user).order_by('-time'),
        'common_tags':common_tags
    }

    return render(request, 'home/main.html', context)

@login_required
def projectRegister(request):
    if request.method == 'POST':
        project_form = ProjectRegisterForm(request.POST)
        if project_form.is_valid():

            newproj = Project(FloatedBy = request.user)
            newproj.save()

            project_form = ProjectRegisterForm(request.POST, instance = newproj)
            project_form.save()

            project_title = project_form.cleaned_data.get('Title')
            messages.success(request, f"Project-{project_title} created!")
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        project_form = ProjectRegisterForm()

    context = {
        'title': 'New-Project',
        'project_form': project_form,
        'notifications': Notification.objects.filter(user = request.user).order_by('-time'),
    }

    return render(request, 'home/projectsRegister.html', context)

def createNewTag(request):
    newTagTitle = request.GET.get('newTagTitle').upper()
    tag = Tag.objects.all().filter(Title = newTagTitle)
    if len(tag)!=0:
        message = 'Tag already exists'
        messages.error(request, message)
        print("Sent message-:", message)
        return JsonResponse({}, status = 404)
    tag = Tag.objects.create(Title = newTagTitle)
    tag.save()
    return JsonResponse({"tag_id":tag.id, "tag_title":tag.Title}, status = 200)

@login_required
def project(request):
    project_id = request.GET.get('project_id')
    project = Project.objects.get(id=project_id)

    projects_id = get_user_projects_id(request.user)

    context = {
        'title': 'Project',
        'project': project,
        'projects_id': projects_id,
        'notifications': Notification.objects.filter(user = request.user).order_by('-time'),
    }
    return render(request, 'home/project.html', context)


@login_required
@user_is_project_author
def projectUpdate(request):
    project_id = request.GET.get('project_id')
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project_update_form = ProjectUpdateForm(request.POST, instance=project)
        if project_update_form.is_valid():
            project_update_form.save()
            messages.success(request, "Project details has been updated!")
            return redirect(f"/project/?project_id={project_id}")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        project_update_form = ProjectUpdateForm(instance=project)

    context = {
        'title': 'Update-Project',
        'project_title': project.Title,
        'project_form': project_update_form,
        'notifications': Notification.objects.filter(user = request.user).order_by('-time'),
    }

    return render(request, 'home/projectUpdate.html', context)


@login_required
@user_is_project_author
def projectDelete(request):
    project_id = request.GET.get('project_id')
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project has been deleted!")
        return redirect('home')

    context = {
        'title': 'Update-Project',
        'project': project,
        'notifications': Notification.objects.filter(user = request.user).order_by('-time'),
    }

    return render(request, 'home/projectDelete.html', context)


@login_required
def projectTask(request):
    project_id = request.GET.get('project_id')
    task = request.GET.get('task')
    page_number = request.GET.get('page_number')

    do_task(request, task)

    if page_number:
        url = f'/?page={page_number}'
    else:
        project = Project.objects.get(id=project_id)
        url = f'/project/?project_id={project.id}'
    return redirect(url)

@login_required
@user_is_project_author
def projectAccept(request):
    project_id = request.GET.get('project_id')
    do_task(request, "Accept")
    return redirect(f'/project/?project_id={project_id}')

@login_required
@user_is_project_author
def projectReject(request):
    project_id = request.GET.get('project_id')
    do_task(request, "Reject")
    return redirect(f'/project/?project_id={project_id}')
