from web.constants import *
from web.models import *


class DataMiddleware(object):

    def process_request(self, request):
        if request.method == 'POST':

            fids = []
            rfids = []
            rates = []

            for key, value in request.POST.iteritems():
                if key.startswith('feature_'):
                    fids.append(int(value))
                elif key.startswith('room_feature_'):
                    rfids.append(int(value))
                elif key.startswith('rate_'):
                    rates.append(int(value))

            if fids:
                features = Feature.objects.filter(id__in=fids)
                request.session['features'] = '<br>'.join(features.values_list('name', flat=True))
            if rfids:
                rfeatures = RoomFeature.objects.filter(id__in=rfids)
                request.session['room_features'] = '<br>'.join(rfeatures.values_list('name', flat=True))

            if rates:
                rates_names = []
                for key, value in RATINGS_E:
                    if key in rates:
                        rates_names.append(value)
                request.session['rates'] = '<br>'.join(rates_names)

            if 'start_date' in request.POST:
                request.session['start_date'] = request.POST.get('start_date')
            if 'end_date' in request.POST:
                request.session['end_date'] = request.POST.get('end_date')

            if 'start_date' in request.POST and 'end_date' in request.POST:
                start_date = datetime.strptime(request.POST.get('start_date'), "%m/%d/%Y")
                end_date = datetime.strptime(request.POST.get('end_date'), "%m/%d/%Y")
                date_diff = (end_date - start_date).days
                request.session['date_diff'] = date_diff

            if 'guest_number' in request.POST:
                request.session['guest_number'] = request.POST.get('guest_number')
            if 'rooms_number' in request.POST:
                request.session['rooms_number'] = request.POST.get('rooms_number')
