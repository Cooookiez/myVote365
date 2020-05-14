from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials, firestore
import static.python.convert as Convert
from datetime import datetime


db = firestore.client()


def index(request):
    # short_id_num = str(short_id_num).upper()
    # convert = Convert.Convert()
    # short_id_dec = convert.num2dec(short_id_num)
    # context = {
    #     'short_id_num': short_id_num,
    #     'short_id_dec': short_id_dec,
    # }
    return render(request, 'spectator/index.html')

def presentation_show(request, short_id_num):

    delay_s = 5
    short_id_num = str(short_id_num).upper()
    time_now = round(datetime.now().timestamp())
    lowest_expect_time = time_now - delay_s

    # find presentations_active with given short id
    presentations_active_ref = db.collection('presentations_active').where('short_id_num', '==', short_id_num)
    presentations_active = presentations_active_ref.get()
    ids = []
    for presentation_active in presentations_active:
        ids.append(presentation_active.id)
    if len(ids) is not 1:
        # error
        pass
    else:
        presentation_ref = db.collection('presentations_active').document(ids[0])
        presentation = presentation_ref.get().to_dict()
        last_log = int(presentation['last_log']['int'])

        # presentation is inactive
        if last_log < lowest_expect_time:
            return render(request, 'spectator/presentation_inactive.html')
        # presentation is active
        else:
            return render(request, 'spectator/presentation_active.html')

    return render(request, 'spectator/presentation_active.html')
