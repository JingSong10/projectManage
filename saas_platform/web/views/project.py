from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models
from web.forms.ProjectModelForm import ProjectModelForm


def project_list(request):
    '''项目列表'''
    # print(request.user_obj)
    # print(request.price_policy)
    if request.method == 'GET':
        # 查看项目列表
        project_dict = {
            'star': [],
            'mine': [],
            'join': []
        }
        my_project_list = models.Project.objects.filter(creator=request.user_obj)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value': row, 'type': 'mine'})
            else:
                project_dict['mine'].append(row)
        join_project_list = models.ProjectUser.objects.filter(user=request.user_obj)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value': item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)


        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})
    form = ProjectModelForm(request, data = request.POST)
    if form.is_valid():
        form.instance.creator = request.user_obj
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def star(request, project_type, project_id):
    '''星标项目'''
    if project_type == 'mine':
        models.Project.objects.filter(id=project_id, creator=request.user_obj).update(star=True)
        return redirect('web:project_list')
    if project_type == 'star':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.user_obj).update(star=True)
        return redirect('web:project_list')
    return None


def unstar(request, project_type, project_id):

    if project_type == 'mine':
        models.Project.objects.filter(id=project_id, creator=request.user_obj).update(star=False)
        return redirect('web:project_list')
    if project_type == 'star':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.user_obj).update(star=False)
        return redirect('web:project_list')
    return None