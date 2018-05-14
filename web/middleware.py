from web.constants import *


class DataMiddleware(object):

    def process_request(self, request):
        if request.method == 'POST':
            if 'start_date' in request.POST:
                request.session['start_date'] = request.POST.get('start_date')
            if 'end_date' in request.POST:
                request.session['end_date'] = request.POST.get('end_date')
            if 'guest_number' in request.POST:
                request.session['guest_number'] = request.POST.get('guest_number')
            if 'rooms_number' in request.POST:
                request.session['rooms_number'] = request.POST.get('rooms_number')
