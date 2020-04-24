from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import string
import requests
import bcrypt
import static.python.convert as convert
import random
import static.python.save_qr as save_qr

cred = credentials.Certificate('static/__PRIVATE__/myvote365-aa6f5-firebase-adminsdk-ipqcy-ce6c711131.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

dont_be_hacekr = [{
    'place': 'Hacker\'s computer',
    'type': 'hacked',
    'msg': 'Don\'t be hacker pls 👏',
}]


def panel(request):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        # logged
        return redirect('auditor:presentations_list')
    else:
        # NOT logged
        return render(request, 'auditor/login_register.html')


def login(request):
    if request.method == 'POST':
        # login
        callback = []

        # requested data
        email = str(request.POST.get('email')).strip()
        password = request.POST.get('password')

        # is only one audytor with mail & get audytor id
        index = 0
        auditor_id = None # audytor id to get user later on
        auditors_ref = db.collection(u'auditors')
        auditors_where_ref = auditors_ref.where(u'email', u'==', email)
        auditors = auditors_where_ref.get()
        for auditor in auditors:
            index = index + 1
            auditor_id = auditor.id

        # is only one auditor
        if index == 1:
            auditor_ref = db.collection(u'auditors').document(auditor_id)
            auditor = auditor_ref.get().to_dict()
            match = bcrypt.checkpw(str(password).encode('utf-8'), auditor['password'])
            if match:  # passwords match, login
                # add auditor to session
                request.session['auditor'] = {
                    'logged': True,
                    'name': auditor['name'],
                    'email': auditor['email'],
                    'auditor_id': auditor_id,
                }
                # add 'last logged' to db
                auditor_ref.update({
                    u'last_logged': datetime.now(),
                })
                # return msg
                callback.append({
                    'place': 'callback-login-submit',
                    'type': 'success',
                    'msg': 'Zalogowałeś się, już cię przekierowujemy!',
                })
            else:  # passwords doesn't match
                callback.append({
                    'place': 'callback-login-submit',
                    'type': 'error',
                    'msg': 'Email, lub hasło są błędne',
                })
        else:
            callback.append({
                'place': 'callback-login-submit',
                'type': 'error',
                'msg': 'Email, lub hasło są błędne',
            })
        json_callback = json.dumps(callback)
        return HttpResponse(json_callback)
    else:
        return login_register(request)


def register(request):
    if request.method == 'POST':
        # register
        is_error = False
        callback = [];

        # requested data
        first_last_name = str(request.POST.get('first_last_name')).strip()
        email = str(request.POST.get('email')).strip()
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        password_hash = bcrypt.hashpw(str(password_1).encode('utf-8'), bcrypt.gensalt())
        reCaptcha_response = str(request.POST.get('reCaptcha_response'))

        # NAME check if empty
        if first_last_name == '':
            is_error = True
            callback.append({
                'place': 'callback-register-name',
                'type': 'error',
                'msg': 'Imię i nazwisko nie może być puste!',
            })

        # EMAIL check if empty
        if email == '':
            is_error = True
            callback.append({
                'place': 'callback-register-email',
                'type': 'error',
                'msg': 'Email nie może być pusty!',
            })

        # EMAIL check if email exist
        if not email_exist(email):
            is_error = True
            callback.append({
                'place': 'callback-register-email',
                'type': 'error',
                'msg': 'Podany email jest już w użyciu. Spróbuj się zalogować',
            })

        # PASSWORD-1 check
        if not password_correct_pattern(password_1):
            is_error = True
            callback.append({
                'place': 'callback-register-password-1',
                'type': 'error',
                'msg': 'Hasło nie spełnia wymagań. Sprawdź je poniżej',
                # 'msg': 'Hasło nie spełnia wymagań. Sprawdź je poniżej' + str(min_8_chars) + str(at_last_1_digit) + str(at_last_1_special_char) + str(at_last_1_uppercase) + str(at_last_1_lowercase),
            })

        # PASSWORD-2 password are the same
        if password_1 != password_2:
            is_error = True
            callback.append({
                'place': 'callback-register-password-2',
                'type': 'error',
                'msg': 'Hasła muszą być identyczne',
            })

        # reCaptcha_response
        with open('static/__PRIVATE__/reChaptcha_keys.json', 'r') as f:
            reCaptcha_secret = json.loads(f.read())
            reCaptcha_secret = reCaptcha_secret['secretKey']
            reCaptcha_data = {
                'secret': reCaptcha_secret,
                'response': reCaptcha_response,
            }
            r = requests.post(url='https://www.google.com/recaptcha/api/siteverify', data=reCaptcha_data).text
            reCaptcha_json_result = json.loads(r)
            if reCaptcha_json_result['success'] in locals() and not reCaptcha_json_result['success']:
                is_error = True
                callback.append({
                    'place': 'callback-register-submit',
                    'type': 'error',
                    'msg': 'reChaptcha errror',
                })

        # if no errors, register
        if not is_error:
            auditors_ref = db.collection(u'auditors').document()
            auditors_ref.set({
                u'name': first_last_name,
                u'email': email,
                u'password': password_hash,
                u'register_date': datetime.now(),
            })
            callback.append({
                'place': 'callback-register-submit',
                'type': 'success',
                'msg': 'Zarejestrowałeś się! Za chwilę zostaniesz zalogowany!',
            })

        json_callback = json.dumps(callback)
        return HttpResponse(json_callback)
    else:
        return redirect('auditor:login')


def login_register(request):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        # logged
        return redirect('auditor:panel')
    else:
        # NOT logged
        return render(request, 'auditor/login_register.html')


def logout(request):
    # add 'last logged' to db
    auditor_ref = db.collection(u'auditors').document(request.session['auditor']['auditor_id'])
    auditor_ref.update({
        u'last_logged': datetime.now(),
    })
    request.session['auditor'] = {
        'logged': False,
        'name': None,
        'email': None,
        'auditor_id': None,
    }
    request.session.save()
    return redirect('auditor:panel')


def presentations_list(request):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        # logged
        presentations = []
        presentations_ref = db.collection(u'presentations')\
            .where(u'properties.auditor_id', u'==', request.session['auditor']['auditor_id'])\
            .get()
        for presentation_ref in presentations_ref:
            presentation = presentation_ref.to_dict()
            print(presentation['properties'])
            presentation_tmp = {
                'title': presentation['properties']['title'],
                'short_id_num': presentation['properties']['short_id_num'],
            }
            presentations.append(presentation_tmp)

        context = {
            'presentations': presentations,
        }
        return render(request, 'auditor/presentations_list.html', context=context)
    else:
        # NOT logged
        return redirect('auditor:panel')


def presentations_new(request):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        # logged
        conv = convert.Convert()
        short_id_dec = rand_short_id(4)
        short_id_num = conv.dec2num_n_digit(short_id_dec, 4)

        # save qr
        qr = save_qr.save_qr(short_id_num)

        # new presentation
        presentation_id = db.collection(u'presentations').document().id
        presentation_ref = db.collection(u'presentations').document(presentation_id)
        presentation_ref.set({
            u'properties': {
                u'title': 'Untitled',
                u'qr_code_on_start': False,
                u'short_id_dec': short_id_dec,
                u'short_id_num': short_id_num,
                u'auditor_id': request.session['auditor']['auditor_id'],
                u'presentation_url': 'web_url',
                u'presentation_qr_code': 'qr_url',
            },
        })

        lecture_id = presentation_ref.collection(u'lectures').document().id
        lecture_ref = presentation_ref.collection(u'lectures').document(lecture_id)
        lecture_ref.set({
            'properties': {
                'title': 'W1',
                'position': 0,
            }
        })

        slide_id = lecture_ref.collection(u'slides').document().id
        slide_ref = lecture_ref.collection(u'slides').document(slide_id)
        slide_ref.set({
            'properties': {
                'title': 'Czy się podobało?',
                'type': 'yesno',
                'position': 0,
            }
        })
        #
        # slide_id = lecture_ref.collection(u'slides').document().id
        # slide_ref = lecture_ref.collection(u'slides').document(slide_id)
        # slide_ref.set({
        #     'properties': {
        #         'title': 'Jakie są szanse, że polecisz wykład?',
        #         'type': 'slider_1to5',
        #         'position': 1,
        #     }
        # })
        #
        # lecture_id = presentation_ref.collection(u'lectures').document().id
        # lecture_ref = presentation_ref.collection(u'lectures').document(lecture_id)
        # lecture_ref.set({
        #     'properties': {
        #         'title': 'W2',
        #         'position': 1,
        #     }
        # })
        #
        # slide_id = lecture_ref.collection(u'slides').document().id
        # slide_ref = lecture_ref.collection(u'slides').document(slide_id)
        # slide_ref.set({
        #     'properties': {
        #         'title': 'Co byś zmienił?',
        #         'type': 'text',
        #         'position': 0,
        #     }
        # })

        if 'auditor' in request.session and request.session['auditor']['logged'] is True:
            return redirect('auditor:presentation_edit', short_id_num=short_id_num)
        else:
            return redirect('auditor:panel')
    else:
        # NOT logged
        return redirect('auditor:panel')


def presentations_edit(request, short_id_num, lecture_=None, lecture=None):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        # LOGGED

        def get_lectures():  # wyszukanie prezentacji
            presentations_id = None
            presentations_ref = db.collection(u'presentations')
            presentations_ref = presentations_ref.where(u'properties.short_id_num', u'==', short_id_num)
            presentations = presentations_ref.get()
            index = 0

            for presentation in presentations:
                index = index + 1
                presentations_id = presentation.id

            # pobranie prezentaci
            presentation_ref = db.collection(u'presentations').document(presentations_id)
            presentation = presentation_ref.get().to_dict()

            # lectures
            lectures_ref = presentation_ref.collection('lectures')
            lectures = lectures_ref.get()
            lectures_data = {}
            for lecture_ref in lectures:

                slides_data = {}
                lecture_id = lecture_ref.id
                lecture_data = lecture_ref.to_dict()
                lecture_position = lecture_data["properties"]["position"]
                slides_ref = presentation_ref.collection('lectures').document(lecture_ref.id).collection('slides')
                slides = slides_ref.get()

                for slide_ref in slides:
                    slide_id = slide_ref.id
                    slide_data = slide_ref.to_dict()
                    slide_data['id'] = slide_id
                    slide_position = slide_data["properties"]["position"]
                    slides_data[slide_position] = slide_data

                lectures_data[lecture_position] = {
                    'properties': lecture_data['properties'],
                    'id': lecture_id,
                    'slides': slides_data,
                }

            return {
                'presentation': presentation,
                'lectures_data': lectures_data,
                'lectures_json': json.dumps(lectures_data),
            }

        if request.method == 'POST': # updates to database
            option = str(request.POST.get('option')).strip()
            callback = []

            def get_ids_by_short_id_num():
                presentations_id = None
                presentations_ref = db.collection(u'presentations')
                presentations_ref = presentations_ref.where(u'properties.short_id_num', u'==', short_id_num)
                presentations = presentations_ref.get()
                index = 0
                for presentation in presentations:
                    index = index + 1
                    presentations_id = presentation.id

                # download presentation
                presentation_ref = db.collection(u'presentations').document(presentations_id)
                presentation = presentation_ref.get().to_dict()

                return {
                    'auditor_id': presentation['properties']['auditor_id'],
                    'presentation_id': presentations_id,
                }

            def user_presentation_verification():
                return get_ids_by_short_id_num()['auditor_id'] == request.session['auditor']['auditor_id']

            def delete_collection(coll_ref, batch_size):
                docs = coll_ref.limit(batch_size).stream()
                deleted = 0

                for doc in docs:
                    print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
                    doc.reference.delete()
                    deleted = deleted + 1

                if deleted >= batch_size:
                    return delete_collection(coll_ref, batch_size)

            presentation_ref = db.collection(u'presentations').document(get_ids_by_short_id_num()['presentation_id'])

            # UPDATES

            # update presentation title
            if option == 'update_presentation_title':
                new_title = str(request.POST.get('new_title')).strip()

                # check if short_id_num is created by logged user
                # if yes, update title
                if user_presentation_verification():
                    presentation_ref.update({
                        'properties.title': new_title,
                    })
                    callback.append({
                        'type': 'success',
                    })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # update lecture title
            elif option == 'update_lecture_title':
                new_title = str(request.POST.get('new_title')).strip()
                lecture_id = str(request.POST.get('lecture_id')).strip()
                # check if short_id_num is created by logged user
                # if yes, update title
                if user_presentation_verification():
                    try:
                        lecture_ref = presentation_ref.collection('lectures').document(lecture_id)
                        lecture_ref.update({
                            'properties.title': new_title,
                        })
                        callback.append({
                            'type': 'success',
                        })
                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # update lecture position
            elif option == 'update_lecture_position':
                cur_position = int(request.POST.get('cur_position'))-1
                new_position = int(request.POST.get('new_position'))-1
                print(f'LECTURE {cur_position} -> {new_position}')
                # if yes, update title
                if user_presentation_verification():
                    try:
                        # how many presentations? (is new position between 0 and max?)
                        how_many_presentations = 0
                        positions = []
                        lectures_ref = presentation_ref.collection('lectures').get()
                        for _ in lectures_ref:
                            how_many_presentations += 1
                            positions.append("")

                        # download presentations position
                        lectures_ref = presentation_ref.collection('lectures').get()
                        for lecture_ref in lectures_ref:
                            position = int(lecture_ref.to_dict()['properties']['position'])
                            positions[position] = lecture_ref.id

                        # update presentation
                        if 0 <= new_position < how_many_presentations:  # is between 0 and max

                            # update new position for changed element
                            lecture_ref = presentation_ref.collection('lectures').document(positions[cur_position])
                            lecture_ref.update({
                                'properties.position': int(new_position)
                            })

                            # is new position greater then old one
                            if new_position > cur_position:  # yes, it is greater
                                # for each element between old one and new one change position to -1
                                for i in range(cur_position+1, new_position+1):
                                    lecture_ref = presentation_ref.collection('lectures').document(positions[i])
                                    lecture_ref.update({
                                        'properties.position': (int(lecture_ref.get().to_dict()['properties']['position'])-1)
                                    })

                            elif new_position < cur_position:  # no, it is lesser
                                # for each element between old one and new one change position to +1
                                for i in range(new_position, cur_position):
                                    lecture_ref = presentation_ref.collection('lectures').document(positions[i])
                                    lecture_ref.update({
                                        'properties.position': (int(lecture_ref.get().to_dict()['properties']['position'])+1)
                                    })

                            else:  # is the same, do nothing
                                pass

                            lectures = get_lectures()
                            callback.append({
                                'type': 'success',
                                'msg': '',
                                'lectures_json': lectures['lectures_json'],
                            })

                        else:
                            callback.append({
                                'type': 'error',
                                'msg': 'wrong new position',
                            })

                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })

                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # update slide title
            elif option == 'update_slide_title':
                new_title = str(request.POST.get('new_title')).strip()
                lecture_id = str(request.POST.get('lecture_id')).strip()
                slide_id = str(request.POST.get('slide_id')).strip()

                # check if short_id_num is created by logged user
                # if yes, update title
                if user_presentation_verification():
                    try:
                        lecture_ref = presentation_ref.collection('lectures').document(lecture_id)
                        slide_ref = lecture_ref.collection('slides').document(slide_id)
                        slide_ref.update({
                            'properties.title': new_title,
                        })
                        callback.append({
                            'type': 'success',
                        })
                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture or slide doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # update slide type
            elif option == 'update_slide_type':
                new_type = str(request.POST.get('new_type')).strip()
                lecture_id = str(request.POST.get('lecture_id')).strip()
                slide_id = str(request.POST.get('slide_id')).strip()

                # check if short_id_num is created by logged user
                # if yes, update title
                if user_presentation_verification():
                    try:
                        lecture_ref = presentation_ref.collection('lectures').document(lecture_id)
                        slide_ref = lecture_ref.collection('slides').document(slide_id)
                        slide_ref.update({
                            'properties.type': new_type,
                        })
                        callback.append({
                            'type': 'success',
                        })
                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture or slide doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # update slide position
            elif option == 'update_slide_position':
                cur_position = int(request.POST.get('cur_position'))-1
                new_position = int(request.POST.get('new_position'))-1
                print(f'SLIDE {cur_position} -> {new_position}')
                lecture_id = str(request.POST.get('lecture_id')).strip()

                # if yes, update title
                if user_presentation_verification():
                    try:
                        # how many slides? (is new position between 0 and max?)
                        lectures_ref = presentation_ref.collection('lectures').document(lecture_id)
                        how_many_slides = 0
                        positions = []
                        slides_ref = lectures_ref.collection('slides').get()
                        for _ in slides_ref:
                            how_many_slides += 1
                            positions.append("")

                        # download slides position
                        slides_ref = lectures_ref.collection('slides').get()
                        for slide_ref in slides_ref:
                            position = int(slide_ref.to_dict()['properties']['position'])
                            positions[position] = slide_ref.id

                        # update slides
                        if 0 <= new_position < how_many_slides:
                            # update new position for changed element
                            slide_ref = lectures_ref.collection('slides').document(positions[cur_position])
                            slide_ref.update({
                                'properties.position': int(new_position)
                            })

                            # is new position greater then old one
                            if new_position > cur_position:  # yes, it is greater
                                # for each element between old one and new one change position to -1
                                for i in range(cur_position + 1, new_position + 1):
                                    slide_ref = lectures_ref.collection('slides').document(positions[i])
                                    slide_ref.update({
                                        'properties.position': (
                                                    int(slide_ref.get().to_dict()['properties']['position']) - 1)
                                    })

                            elif new_position < cur_position:  # no, it is lesser
                                # for each element between old one and new one change position to +1
                                for i in range(new_position, cur_position):
                                    slide_ref = lectures_ref.collection('slides').document(positions[i])
                                    slide_ref.update({
                                        'properties.position': (
                                                    int(slide_ref.get().to_dict()['properties']['position']) + 1)
                                    })

                            else:  # is the same, do nothing
                                pass

                            lectures = get_lectures()
                            callback.append({
                                'type': 'success',
                                'msg': '',
                                'lectures_json': lectures['lectures_json'],
                            })

                        else:
                            callback.append({
                                'type': 'error',
                                'msg': 'wrong new position',
                            })


                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })

                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })

            # add new slide to end of lecture
            elif option == 'append_slide':
                lecture_position = int(request.POST.get('lecture_position'))
                if user_presentation_verification():
                    try:
                        lectures_ref = presentation_ref.collection('lectures').where('properties.position', '==', lecture_position)
                        lectures = lectures_ref.get()
                        ids = []
                        for lecture in lectures:
                            ids.append(lecture.id)

                        if len(ids) != 1:  # too many or too less lectures with given position
                            callback.append({
                                'type': 'error',
                                'msg': 'too many or too less lectures with given position',
                            })
                        else:  # only one lecture find, go on
                            # how many slides already exists
                            new_position = 0
                            lecture_ref = presentation_ref.collection('lectures').document(ids[0])
                            slides_ref = lecture_ref.collection('slides').get()
                            for _ in slides_ref:
                                new_position += 1

                            slides_ref = lecture_ref.collection('slides').document()
                            slides_ref.set({
                                'properties': {
                                    'title': 'Nowy slide',
                                    'type': 'text',
                                    'position': new_position,
                                }
                            })
                            callback.append({
                                'type': 'success',
                                'lectures_json': get_lectures()['lectures_json'],
                            })
                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # remove slide
            elif option == 'remove_slide':
                lecture_position = int(request.POST.get('lecture_position'))
                slide_position = int(request.POST.get('slide_position'))
                if user_presentation_verification():
                    try:
                        lectures_ref = presentation_ref.collection('lectures').where('properties.position', '==', lecture_position)
                        lectures = lectures_ref.get()

                        lct_ids = []
                        for lecture in lectures:
                            lct_ids.append(lecture.id)

                        # too many or too less lectures with given position
                        if len(lct_ids) != 1:
                            callback.append({
                                'type': 'error',
                                'msg': 'too many or too less lectures with given position',
                            })

                        # only one lecture find, go on
                        else:
                            # find slide with given position
                            lecture_ref = presentation_ref.collection('lectures').document(lct_ids[0])
                            slides_ref = lecture_ref.collection('slides').where('properties.position', '==', slide_position)
                            slides = slides_ref.get()

                            sld_ids = []
                            for slide_ref in slides:
                                sld_ids.append(slide_ref.id)

                            # too many or too less slides with given position
                            if len(sld_ids) != 1:
                                callback.append({
                                    'type': 'error',
                                    'msg': 'too many or too less lectures with given position',
                                })

                            # only one slide find, go on
                            else:
                                # CHANGE POSITION OF LATER SLIDES
                                # download slides position
                                how_many_slides = 0
                                positions = []
                                # add as many position fields as needed
                                slides_ref = lecture_ref.collection('slides').get()
                                for _ in slides_ref:
                                    how_many_slides += 1
                                    positions.append("")
                                # assign id to position in array
                                slides_ref = lecture_ref.collection('slides').get()
                                for slide_ref in slides_ref:
                                    position = int(slide_ref.to_dict()['properties']['position'])
                                    positions[position] = slide_ref.id

                                for slide_position_tmp in range(slide_position+1, how_many_slides):
                                    slide_ref = lecture_ref.collection('slides').document(positions[slide_position_tmp])
                                    slide_ref.update({
                                        'properties.position': (
                                                    int(slide_ref.get().to_dict()['properties']['position']) - 1)
                                    })

                                # delete slide
                                slide_ref = lecture_ref.collection('slides').document(sld_ids[0])
                                slide_ref.delete()

                                callback.append({
                                    'type': 'success',
                                    'lectures_json': get_lectures()['lectures_json'],
                                })
                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # add new lecture to end of presentation
            elif option == 'append_lecture':
                if user_presentation_verification():
                    try:
                        # how many lectures already exists
                        lectures_count = 0
                        lectures_ref = presentation_ref.collection('lectures').get()
                        for _ in lectures_ref:
                            lectures_count += 1

                        # add new lecture
                        lectures_ref = presentation_ref.collection('lectures')
                        lecture_id = lectures_ref.document().id
                        lecture_ref = lectures_ref.document(lecture_id)
                        lecture_ref.set({
                            'properties': {
                                'position': lectures_count,
                                'title': f'W{lectures_count+1}',
                            }
                        })

                        # add one slide to lecture
                        slide_id = lecture_ref.collection('slides').document().id
                        slide_ref = lecture_ref.collection('slides').document(slide_id)
                        slide_ref.set({
                            'properties': {
                                'title': 'Nowy slide',
                                'type': 'text',
                                'position': 0,
                            }
                        })
                        # return
                        callback.append({
                            'type': 'success',
                            'lectures_json': get_lectures()['lectures_json'],
                        })

                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            # remove lecture
            elif option == 'remove_lecture':
                lecture_position = int(request.POST.get('lecture_position'))
                print(f'lecture_position: {lecture_position}')
                if user_presentation_verification():
                    try:
                        lectures_ref = presentation_ref.collection('lectures').where('properties.position', '==', lecture_position)
                        lectures = lectures_ref.get()

                        lct_ids = []
                        for lecture_ref in lectures:
                            lct_ids.append(lecture_ref.id)

                        # too many or too less lectures with given position
                        if len(lct_ids) != 1:
                            callback.append({
                                'type': 'error',
                                'msg': 'too many or too less lectures with given position',
                            })

                        # only one lecture find, go on
                        else:

                            # CHANGE POSITION OF LATER SLIDES
                            lectures_count = 0
                            lectures_position = []
                            lectures_ref = presentation_ref.collection('lectures').get()
                            for _ in lectures_ref:
                                lectures_position.append('')
                                lectures_count += 1

                            # download lectures position
                            lectures_ref = presentation_ref.collection('lectures').get()
                            for lecture_ref_tmp in lectures_ref:
                                position = int(lecture_ref_tmp.to_dict()['properties']['position'])
                                lectures_position[position] = lecture_ref_tmp.id

                            # chane other lecture positions
                            for lecture_position_tmp in range(lecture_position + 1, lectures_count):
                                lecture_ref = presentation_ref.collection('lectures').document(lectures_position[lecture_position_tmp])
                                lecture_ref.update({
                                    'properties.position': (
                                            int(lecture_ref.get().to_dict()['properties']['position']) - 1)
                                })

                            # delete lectures subcollection
                            lecture_ref = presentation_ref.collection('lectures').document(lct_ids[0])
                            slides_collection_ref = lecture_ref.collection('slides')
                            print(slides_collection_ref)
                            delete_collection(slides_collection_ref, 50)

                            # delete lecture document
                            lecture_ref.delete()

                            callback.append({
                                'type': 'success',
                                'lectures_json': get_lectures()['lectures_json'],
                            })

                    except:
                        callback.append({
                            'type': 'error',
                            'msg': 'lecture doesn\'t exists',
                        })
                else:
                    callback.append({
                        'type': 'error',
                        'msg': 'wrong option',
                    })
            else:
                callback = dont_be_hacekr

            json_callback = json.dumps(callback)
            return HttpResponse(json_callback)

        else:  # show web page

            lectures = get_lectures()

            context = {
                'properties': lectures['presentation']['properties'],
                'lectures_data': lectures['lectures_data'],
                'lectures_json': lectures['lectures_json'],
            }

            return render(request, 'auditor/presentation_edit.html', context=context)

    else:
        # NOT logged
        return redirect('auditor:panel')


def presentation_play(request, short_id_num):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        if request.method == 'POST':
            pass
        else:
            context = {
                'short_id_num': short_id_num
            }
            return render(request, 'auditor/presentation_play.html', context=context)
    else:
        return redirect('auditor:panel')


def settings(request):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        # logged
        return render(request, 'auditor/settings.html')
    else:
        # NOT logged
        return redirect('auditor:panel')




def settings_update_general(request):
    if request.method == 'POST':

        is_error = False
        callback = []

        # requested data
        name = str(request.POST.get('name')).strip()

        # NAME check if empty
        if name == '':
            is_error = True
            callback.append({
                'place': 'callback-register-name',
                'type': 'error',
                'msg': 'Imię i nazwisko nie może być puste!',
            })

        # if no errors, register
        if not is_error:
            request.session['auditor']['name'] = name
            request.session.save()
            auditor_ref = db.collection(u'auditors').document(request.session['auditor']['auditor_id'])
            auditor_ref.update({
                u'name': name,
            })
            callback = [{
                'place': 'callback-user-settings-general-submit',
                'type': 'success',
                'msg': 'Zapisano',
            }]

    else:
        callback = dont_be_hacekr

    json_callback = json.dumps(callback)
    return HttpResponse(json_callback)


def settings_update_email(request):
    if request.method == 'POST':

        is_error = False
        callback = []

        # requested data
        email = str(request.POST.get('email'))
        password = str(request.POST.get('password'))

        # EMAIL check if empty
        if email == '':
            is_error = True
            callback.append({
                'place': 'callback-user-settings-email-email',
                'type': 'error',
                'msg': 'Email nie może być pusty!',
            })

        # EMAIL check if email exist
        print('request.session.auditor.email', request.session['auditor']['email'])
        if not email_exist(email, request.session['auditor']['email']):
            is_error = True
            callback.append({
                'place': 'callback-user-settings-email-email',
                'type': 'error',
                'msg': 'Podany email jest już w użyciu. Spróbuj inny',
            })

        auditor_ref = db.collection(u'auditors').document(request.session['auditor']['auditor_id'])
        auditor = auditor_ref.get().to_dict()
        match = bcrypt.checkpw(str(password).encode('utf-8'), auditor['password'])
        if match:  # passwords match
            if not is_error:
                request.session['auditor']['email'] = email
                request.session.save()
                auditor_ref = db.collection(u'auditors').document(request.session['auditor']['auditor_id'])
                auditor_ref.update({
                    u'email': email,
                })
        else:
            callback.append({
                'place': 'callback-user-settings-email-password',
                'type': 'error',
                'msg': 'Błędne hasło',
            })

    else:
        callback = dont_be_hacekr

    json_callback = json.dumps(callback)
    return HttpResponse(json_callback)


def settings_update_password(request):
    if request.method == 'POST':

        is_error = False
        callback = []

        # requested data
        password_new_1 = str(request.POST.get('password_new_1'))
        password_new_2 = str(request.POST.get('password_new_2'))
        password_hash = bcrypt.hashpw(str(password_new_1).encode('utf-8'), bcrypt.gensalt())
        password_old = str(request.POST.get('password_old'))

        if not password_correct_pattern(password_new_1):
            is_error = True
            callback.append({
                'place': 'callback-user-settings-password-new-password-1',
                'type': 'error',
                'msg': 'Hasło nie spełnia wymagań. Sprawdź je poniżej',
            })

        if password_new_1 != password_new_2:
            is_error = True
            callback.append({
                'place': 'callback-user-settings-password-new-password-2',
                'type': 'error',
                'msg': 'Hasła muszą być identyczne',
            })

        auditor_ref = db.collection(u'auditors').document(request.session['auditor']['auditor_id'])
        auditor = auditor_ref.get().to_dict()
        match = bcrypt.checkpw(str(password_old).encode('utf-8'), auditor['password'])
        if match:  # passwords match
            if not is_error:
                auditor_ref.update({
                    u'password': password_hash,
                })
                callback.append({
                    'place': 'callback-user-settings-password-submit',
                    'type': 'success',
                    'msg': 'Hasło zmienione',
                })
        else:
            callback.append({
                'place': 'callback-user-settings-password-old-password',
                'type': 'error',
                'msg': 'Błędne hasło',
            })

    else:
        callback = dont_be_hacekr
    json_callback = json.dumps(callback)
    return HttpResponse(json_callback)




def email_exist(email, email_cur=None):
    """
    :email: email to check
    :email_cur: [optional] if one email exist, check if not the same as this
    :return:bool
        true if email doesnt exist or exist only one adn is the same as email_cur
        false otherwise
    """

    # EMAIL check if email exist
    auditors_ref = db.collection(u'auditors')
    email_ref = auditors_ref.where(u'email', u'==', email)
    email_content = email_ref.get()
    index = 0;
    for tmp in email_content:
        index = index + 1
    if index == 0:
        return True
    elif index > 0 and email == email_cur:
        return True
    else:
        return False


def password_correct_pattern(password):
    """
    :password: - password to check
    :return:bool
        true if password is correct
    """
    # PASSWORD-1 check if correct
    min_8_chars = False
    at_last_1_digit = False
    at_last_1_special_char = True
    at_last_1_uppercase = False
    at_last_1_lowercase = False

    password_lenght = len(password)
    # PASSWORD-1 min 8 chars
    if password_lenght >= 8:
        min_8_chars = True

    # PASSWORD-1 at last 1 digit
    for i in range(password_lenght):
        if password[i] in string.digits:
            at_last_1_digit = True
            break

    # PASSWORD-1 at last 1 special char
    # for i in range(password_lenght):
    #     if password[i] in '`~!@#$%^&*()_-+={}[]\\|;;\'"<>,.?/':
    #         at_last_1_special_char = True
    #         break

    # PASSWORD-1 at last 1 uppercase
    for i in range(password_lenght):
        if password[i] in string.ascii_uppercase:
            at_last_1_uppercase = True
            break

    # PASSWORD-1 at last 1 lowercase
    for i in range(password_lenght):
        if password[i] in string.ascii_lowercase:
            at_last_1_lowercase = True
            break

    # PASSWORD-1 final check
    if min_8_chars and at_last_1_digit and at_last_1_special_char and at_last_1_uppercase and at_last_1_lowercase:
        return True
    else:
        return False


def rand_short_id(num_od_digit=4):
    conv = convert.Convert()
    max_dec = conv.max_dec_from_n_digit(num_od_digit)
    its_first_short_id = False
    random_short_id_dec = 0
    while not its_first_short_id:
        random_short_id_dec = random.randint(0, max_dec)
        # check if current id dec doesn't exist
        tmp_presentations = db.collection(u'presentations').where(u'properties.short_id_dec', u'==', random_short_id_dec).get()
        index = 0
        for tmp in tmp_presentations:
            index = index + 1
        if index == 0:
            its_first_short_id = True
    return random_short_id_dec

