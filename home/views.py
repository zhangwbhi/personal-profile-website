from django.shortcuts import render, redirect
from .models import Project, Skill, Message
from .forms import ProjectForm, MessageForm, SkillForm, CommentForm
from django.contrib import messages



# Create your views here.


def homePage(request):
    projects = Project.objects.all()
    detailedSkills = Skill.objects.exclude(body='')

    skills = Skill.objects.filter(body='')

    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You message was successfully sent!.')

    context = {'projects': projects, 'skills': skills,
               'detailedSkills': detailedSkills, 'form': form}
    return render(request, 'home/home.html', context)



def projectPage(request, pk):
    project = Project.objects.get(id=pk)
    count = project.comment_set.count()

    comments = project.comment_set.all().order_by('-created')

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.save()
            messages.success(request, 'Your comment was successfully added!')

    context = {'project': project, 'count': count,
               'comments': comments, 'form': form}
    return render(request, 'home/project.html', context)


def addProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'home/project_form.html', context)


def editProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'home/project_form.html', context)


def inboxPage(request):
    inbox = Message.objects.all().order_by('is_read')

    unreadCount = Message.objects.filter(is_read=False).count()
    context = {'inbox': inbox, 'unreadCount': unreadCount}
    return render(request, 'home/inbox.html', context)


def messagePage(request, pk):
    message = Message.objects.get(id=pk)
    message.is_read = True
    message.save()
    context = {'message': message}
    return render(request, 'home/message.html', context)


def addSkill(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        form.save()
        messages.success(request, 'Your skill was successfully added!')
        return redirect('home')
    context = {'form': form}
    return render(request, 'home/skill_form.html', context)






