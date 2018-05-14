from web.constants import *


class DataMiddleware(object):

    def process_request(self, request):
        if request.method == 'POST' and 'start_date' in request.POST and 'end_date' in request.POST:
            request.session['start_date'] = request.POST.get('start_date')
            request.session['end_date'] = request.POST.get('end_date')
