import logging

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from handler import CsvHandler
from validator import CsvValidator
from models import CsvJob

class CsvUploader(APIView):

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse("Access Denied..", content_type='text/plain')
        return Response(data=dict(action_names= CsvValidator.available_actions()
                                  , action_json=CsvValidator.available_actions_json())
                        , template_name='csv_uploader.html')

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(self.__class__.__name__)
        template_name = 'csv_uploader.html'
        if not request.user.is_authenticated():
            return HttpResponse("Access Denied..", content_type='text/plain')
        try:
            handler = CsvHandler(str(request.POST['action_name']), request.FILES['csv_file'])
            handler.process(request.user)

            return Response(data=dict(status_message= handler.display_message()
                                      ,action_names=CsvValidator.available_actions()
                                      , action_json=CsvValidator.available_actions_json()),
                            template_name='csv_uploader.html')

        except MultiValueDictKeyError as e:
            logger.exception("Error in  upload file: %s", e.message)
            return Response(data={'status_message': 'csv file missing', 'action_names': CsvValidator.available_actions()
                , 'action_json': CsvValidator.available_actions_json()}, template_name=template_name)
        except Exception as e:

            logger.exception("Error in  upload file: %s", e.message)
            return Response(data={'status_message': e.message, 'action_names': CsvValidator.available_actions()
                                  , 'action_json': CsvValidator.available_actions_json()}, template_name=template_name)

class CsvUploaderCallback(APIView):
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(self.__class__.__name__)
        CsvHandler.callback(request.data['job_item_id'], request.data['status'], request.data['message'][0:199])
        return Response('OK')

class CsvUploaderCleanup(APIView):
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(self.__class__.__name__)
        CsvJob.purge()
        return Response('OK')