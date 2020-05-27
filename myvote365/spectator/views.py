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

    if request.method == 'POST':
        return render(request, 'spectator/forms/yesno.html')

    else:

        delay_s = 10 * 60
        short_id_num = str(short_id_num).upper()
        time_now = round(datetime.now().timestamp())
        lowest_expect_time = time_now - delay_s

        # find presentations_active with given short id
        presentations_active_ref = db.collection('presentations_active').where('presentation.short_id_num', '==', short_id_num)
        presentations_active = presentations_active_ref.get()
        ids = []
        for presentation_active in presentations_active:
            ids.append(presentation_active.id)
        if len(ids) is not 1:
            # error
            pass
        else:
            doc_id = ids[0]
            presentation_ref = db.collection('presentations_active').document(doc_id)
            presentation = presentation_ref.get().to_dict()
            last_log = int(presentation['last_log']['int'])
            print(f'{lowest_expect_time} = {time_now} - {delay_s}')
            print(f'{last_log}')

            # presentation is inactive
            if last_log < lowest_expect_time:
                return render(request, 'spectator/presentation_inactive.html')
            # presentation is active
            else:
                return render(request, 'spectator/presentation_active.html', context={
                    'doc_id': doc_id,
                    'short_id_num': short_id_num,
                })

        return render(request, 'spectator/presentation_active.html')
