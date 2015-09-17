from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from django.views.generic import TemplateView, View
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from proj.settings import BASE_DIR


class MyFirstView(TemplateView):
    template_name = "firstpage.html"

    def get(self, request):
        return self.render_to_response({})


class MyReportView(TemplateView):
    template_name = 'reportpage.html'

    def get(self, request):
        return self.render_to_response({})


class MyPdfView(View):
    def get(self, request, *args, **kwargs):
        file_name = BASE_DIR + 'testreport.pdf'
        filefrom = BASE_DIR + '/convertpdf.js'
        url = 'http://' + request.get_host() + '/pdfreport'
        external_process = Popen(["/usr/local/bin/phantomjs", filefrom, url, file_name],
                                 stdout=PIPE, stderr=STDOUT)

        external_process.wait()
        return_file = FileWrapper(open(file_name, 'r'))
        download_file_name = 'myreport'
        response = StreamingHttpResponse(return_file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename= %s.pdf' % download_file_name
        return response
