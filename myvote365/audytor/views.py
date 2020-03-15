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
            }
        })

        slide_id = lecture_ref.collection(u'slides').document().id
        slide_ref = lecture_ref.collection(u'slides').document(slide_id)
        slide_ref.set({
            'properties': {
                'title': 'Czy się podobało?',
                'type': 'yesno',
            }
        })

        slide_id = lecture_ref.collection(u'slides').document().id
        slide_ref = lecture_ref.collection(u'slides').document(slide_id)
        slide_ref.set({
            'properties': {
                'title': 'Jakie są szanse, że polecisz wykład?',
                'type': 'slider_1to5',
            }
        })

        lecture_id = presentation_ref.collection(u'lectures').document().id
        lecture_ref = presentation_ref.collection(u'lectures').document(lecture_id)
        lecture_ref.set({
            'properties': {
                'title': 'W2',
            }
        })

        slide_id = lecture_ref.collection(u'slides').document().id
        slide_ref = lecture_ref.collection(u'slides').document(slide_id)
        slide_ref.set({
            'properties': {
                'title': 'Co byś zmienił?',
                'type': 'text',
            }
        })

        if 'auditor' in request.session and request.session['auditor']['logged'] is True:
            return redirect('auditor:presentation_edit', short_id_num=short_id_num)
        else:
            return redirect('auditor:panel')
    else:
        # NOT logged
        return redirect('auditor:panel')


def presentations_edit(request, short_id_num):
    if 'auditor' in request.session and request.session['auditor']['logged'] is True:
        print('\n\n-----------------------------\n\n')

        # wyszukanie prezentacji
        print(f'short_id_num: "{short_id_num}"')
        presentations_id = None
        presentations_ref = db.collection(u'presentations')
        presentations_ref = presentations_ref.where(u'properties.short_id_num', u'==', short_id_num)
        presentations = presentations_ref.get()
        index = 0
        for presentation in presentations:
            index = index + 1
            presentations_id = presentation.id
        # print(f'index: "{index}"')
        # print(f'presentations_id: "{presentations_id}"')

        # pobranie prezentaci
        presentation_ref = db.collection(u'presentations').document(presentations_id)
        presentation = presentation_ref.get().to_dict()
        print(presentation)

        # lectures
        lectures_ref = presentation_ref.collection('lectures')
        lectures = lectures_ref.get()
        # print(lectures_ref)
        print(f'\n\n---------------\nlectures:')
        for lecture_ref in lectures:
            # print(lecture_ref)
            # print(lecture_ref.id)
            print(lecture_ref.to_dict())
            slides_ref = presentation_ref.collection('lectures').document(lecture_ref.id).collection('slides')
            slides = slides_ref.get()
            for slide_ref in slides:
                # print(f'\t{slide_ref}')
                # print(f'\t{slide_ref.id}')
                print(f'\t{slide_ref.to_dict()}')
                print(f'\t- - - -')
            print('- - - - - - -')


        # logged
        conv = convert.Convert()
        context = {
            'properties': presentation['properties'],
        }
        return render(request, 'auditor/presentation_edit.html', context=context)
    else:
        # NOT logged
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

