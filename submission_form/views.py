from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .forms import UploadFilesForm

from chardet.universaldetector import UniversalDetector
import chardet

# Create your views here.

class IndexView(generic.base.TemplateView):
  template_name = 'submission_form/index.html'

class UploadFilesView(generic.edit.FormView):
  form_class = UploadFilesForm
  template_name = 'submission_form/upload_file.html'
  success_url = reverse_lazy('submission_form:upload') # urlsの項目からURLを生成するメソッド

  def post(self, request, *args, **kwargs):
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    files = request.FILES.getlist('files')
    if form.is_valid():
      files_data = []
      for f in files: # ファイルデータをリストに挿入
        files_data.append(read_file(f))
      return render(request, 'submission_form/upload_success.html', { # アップロード完了ページに遷移
        'files_data': files_data,
      })
    else:
      return self.form_invalid(form)

# メモリ展開されたバイトデータを文字列に変換する
def read_file(file_source):
  data = file_source.name + ' : '
  charcode=chardet.detect(file_source.read())
  for chunk in file_source.chunks():
    data = data + chunk.decode(charcode['encoding'])

  return data
