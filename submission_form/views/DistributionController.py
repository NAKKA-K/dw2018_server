#django module
from django.urls import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView
from django.utils import timezone
from django.http import Http404
from django.conf import settings

#app module
from submission_form.models import Distribution,Organization,Classification
from submission_form.forms import FileForm,CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from submission_form.views.StudentOrTeacherGetter import StudentOrTeacherGetter
from submission_form.views.LoginRequiredMessageMixin import LoginRequiredMessageMixin

import os


class FileIndexView(LoginRequiredMessageMixin, generic.ListView):
  """ファイル一覧"""

  model = Distribution
  template_name = 'submission_form/dist_list.html'
  context_object_name='file_list'
  queryset = Distribution.objects.order_by('-published_date')
  paginate_by = 20


class FileCategoryView(LoginRequiredMessageMixin, generic.ListView):
  """カテゴリ別の配布ファイル一覧"""

  model = Distribution
  paginate_by = 20

  def get_queryset(self):
    """カテゴリ(分類)ごとにフィルターかける"""
    category_pk = self.kwargs['category_pk']
    return Distribution.objects.filter(
      category__pk=category_pk).order_by('-published_date')

  def get_context_data(self):
    """カテゴリのpkをテンプレートへ渡す"""
    context = super().get_context_data(*args, **kwargs) 
    context['category_pk'] = self.kwargs.get('category_pk')

    user_info = StudentOrTeacherGetter.getInfo(self.request.user)
    if user_info is None:
      return context

    context['class_list'] = Classification.objects.filter(organization_id = user_info.organization_id)
    context['is_teacher'] = StudentOrTeacherGetter.is_teacher(self.request.user)

    return context


class FileCreateView(LoginRequiredMessageMixin, FormView):
  """ファイルの作成"""

  template_name = 'submission_form/dist_form.html'
  form_class = FileForm
  success_url = reverse_lazy('submission_form:dist_index')

  def get(self, request, **kwargs):
    is_teacher = StudentOrTeacherGetter.is_teacher(request.user)
    if not is_teacher:
      raise Http404 # 先生でなければ、PageNotFound
    return super().get(request, **kwargs)

  def get_form(self, form_class = None):
    user_info = StudentOrTeacherGetter.getInfo(self.request.user)
    if user_info is None:
      return FileForm()   

    return FileForm(org_id = user_info.organization_id) 

  def post(self, request, *args, **kwargs):
    form = FileForm(request.POST)

    file = request.FILES['file']
    class_id = request.POST.get('classification', None)
    print(form.is_valid, form.errors,type(form.errors))
    if not bool(form.errors):
      file_dir = '{}{}/'.format(settings.MEDIA_ROOT, request.user)
      self.make_dir(file_dir)
      file_path = '{}{}'.format(file_dir, file.name)

      with open(file_path, 'wb+') as dest:
        for chunk in file.chunks():
          dest.write(chunk)

      org = StudentOrTeacherGetter.getInfo(request.user).organization_id
      res = Distribution.objects.create(
        organization_id = org,
        user_id = request.user,
        classification_id = get_object_or_404(Classification, id = class_id),
        name = file.name,
        path = file_path,
      )
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def make_dir(self, file_dir):
    if not os.path.exists(file_dir):
      os.makedirs(self.file_dir)


class FileUpdateView(LoginRequiredMessageMixin, generic.UpdateView):
  """ファイルの更新."""

  model = Distribution
  template_name = 'submission_form/dist_form.html'
  form_class = FileForm
  success_url = reverse_lazy('submission_form:dist_index')

  def get(self, request, **kwargs):
    is_teacher = StudentOrTeacherGetter.is_teacher(request.user)
    if not is_teacher:
      raise Http404 # 先生でなければ、PageNotFound
    return super().get(request, **kwargs)


class FileDeleteView(LoginRequiredMessageMixin, generic.DeleteView):
  """ファイルの削除."""

  model = Distribution
  context_object_name = 'file'
  template_name = 'submission_form/dist_confirm_delete.html'
  success_url = reverse_lazy('submission_form:dict_index')

  def get(self, request, **kwargs):
    is_teacher = StudentOrTeacherGetter.is_teacher(request.user)
    if not is_teacher:
      raise Http404 # 先生でなければ、PageNotFound
    return super().get(request, **kwargs)


class CategoryIndexView(LoginRequiredMessageMixin, generic.ListView):
  """科目の一覧."""

  model = Classification
  template_name = 'submission_form/category_list.html'
  context_object_name='category_list'
  queryset = Classification.objects.order_by('-published_date')
  paginate_by = 20


class CategoryCreateView(LoginRequiredMessageMixin, generic.CreateView):
  """科目の作成."""

  model = Classification
  template_name = 'submission_form/category_form.html'
  form_class = CategoryForm
  success_url = reverse_lazy('submission_form:category_index')
    
  def get(self, request, **kwargs):
    is_teacher = StudentOrTeacherGetter.is_teacher(request.user)
    if not is_teacher:
      raise Http404 # 先生でなければ、PageNotFound
    return super().get(request, **kwargs)

  def form_valid(self, form):
    category = form.save(commit = False)
    category.user_id = self.request.user
    user_info = StudentOrTeacherGetter.getInfo(self.request.user)
    category.organization_id = user_info.organization_id
    category.save()
    return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMessageMixin, generic.UpdateView):
  """科目名の更新."""

  model = Classification
  template_name = 'submission_form/category_form.html'
  form_class = CategoryForm
  success_url = reverse_lazy('submission_form:category_index')

  def get(self, request, **kwargs):
    is_teacher = StudentOrTeacherGetter.is_teacher(request.user)
    if not is_teacher:
      raise Http404 # 先生でなければ、PageNotFound
    return super().get(request, **kwargs)


class CategoryDeleteView(LoginRequiredMessageMixin, generic.DeleteView):
  """科目の削除."""

  model = Classification
  context_object_name='category'
  template_name = 'submission_form/category_confirm_delete.html'
  success_url = reverse_lazy('submission_form:category_index')

  def get(self, request, **kwargs):
    is_teacher = StudentOrTeacherGetter.is_teacher(request.user)
    if not is_teacher:
      raise Http404 # 先生でなければ、PageNotFound
    return super().get(request, **kwargs)

