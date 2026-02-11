from django.conf import settings
from django.http import HttpResponseRedirect


class ExportDownloadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        try:
            self.base_url = settings.IDEMS_EXPORT_BASE_URL
        except AttributeError:
            self.base_url = ""

        try:
            self.s3_url = settings.AWS_S3_ENDPOINT_URL
        except AttributeError:
            self.s3_url = ""

    def __call__(self, request):
        response = self.get_response(request)

        if (
            self.base_url
            and request.path.startswith("/export/download/")
            and isinstance(response, HttpResponseRedirect)
        ):
            response["location"] = response["location"].replace(
                self.s3_url, self.base_url
            )

        return response
