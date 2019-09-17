from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import string
import requests
import bcrypt
import static.python.convert as Convert
import random

cred = credentials.Certificate('static/__PRIVATE__/myvote365-aa6f5-firebase-adminsdk-ipqcy-ce6c711131.json')
firebase_admin.initialize_app(cred)
db = firestore.client();

dont_be_hacekr = [{
    'place': 'Hacker\'s computer',
    'type': 'hacked',
    'msg': 'Don\'t be hacker pls 👏',
}]


def audytor_register(request):
    if request.method == 'POST':
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
            audytors_ref = db.collection(u'audytors').document()
            audytors_ref.set({
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

    else:
        return audytor_login_register(request)

    json_callback = json.dumps(callback)
    return HttpResponse(json_callback)


def audytor_login(request):
    return HttpResponse('<h1>hi login here</h1>')
    if request.method == 'POST':

        callback = []

        # requested data
        email = str(request.POST.get('email')).strip()
        password = request.POST.get('password')

        # is only one audytor with mail & get audytor id
        index = 0
        audytor_id = None # audytor id to get user later on
        audytors_ref = db.collection(u'audytors')
        audytors_where_ref = audytors_ref.where(u'email', u'==', email)
        audytors = audytors_where_ref.get()
        for audytor in audytors:
            index = index + 1
            audytor_id = audytor.id

        # is only one audytor
        if index == 1:
            audytor_ref = db.collection(u'audytors').document(audytor_id)
            audytor = audytor_ref.get().to_dict()
            match = bcrypt.checkpw(str(password).encode('utf-8'), audytor['password'])
            if match: # passwords match, login
                # add audytor to session
                request.session['audytor'] = {
                    'logged': True,
                    'name': audytor['name'],
                    'email': audytor['email'],
                    'audytor_id': audytor_id,
                }
                # add 'last logged' to db
                audytor_ref.update({
                    u'last_logged': datetime.now(),
                })
                # return msg
                callback.append({
                    'place': 'callback-login-submit',
                    'type': 'success',
                    'msg': 'Zalogowałeś się, już cię przekierowujemy!',
                })
            else: # passwords doesn't match
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
    else:
        return HttpResponse('<h1>b hi</h1>')
        return audytor_login_register(request)
    json_callback = json.dumps(callback)
    return HttpResponse(json_callback)


def audytor_login_register(request):
    return HttpResponse('<h1>hi login / register here</h1>')
    # if 'audytor' in request.session and request.session['audytor']['logged'] is True:
    #     # return redirect('audytor:panel')
    #     return HttpResponse('<h1>C hi</h1>')
    #     # return render(request, 'audytor/login_register.html')
    # else:
    #     return HttpResponse('<h1>D hi</h1>')
    #     # return render(request, 'audytor/login_register.html')


def audytor_logout(request):
    # add 'last logged' to db
    audytor_ref = db.collection(u'audytors').document(request.session['audytor']['audytor_id'])
    audytor_ref.update({
        u'last_logged': datetime.now(),
    })
    request.session['audytor'] = {
        'logged': False,
        'name': None,
        'email': None,
        'audytor_id': None,
    }
    request.session.save()
    return redirect('audytor:panel')


def panel(request):
    if 'audytor' in request.session and request.session['audytor']['logged'] is True:
        # return render(request, 'audytor/presentations.html')
        return HttpResponse('<h1>A hi</h1>')
        return redirect('audytor:panel_presentations')
    else:
        # return HttpResponse('<h1>B hi</h1>')
        # return render(request, 'audytor/presentations.html')
        return redirect('audytor:login')


def presentations(request):
    if 'audytor' in request.session and request.session['audytor']['logged'] is True:
        return render(request, 'audytor/presentations.html')
    else:
        # return render(request, 'audytor/presentations.html')
        return HttpResponse('<h1>gfd</h1>')


def presentation_new(request):
    convert = Convert.Convert()
    short_id_dec = rand_short_id(4)
    short_id_num = convert.dec2num_n_digit(short_id_dec, 4)

    presentations_ref = db.collection(u'presentations').document()
    new_id = presentations_ref.id
    print('–––– id:', new_id, '––––')
    presentation_ref = db.collection(u'presentations').document(new_id)
    presentation_ref.set({
        u'properties': {
            u'name': 'Untitled',
            u'qr-code-on-start': False,
            u'short-id-dec': short_id_dec,
            u'short-id-num': short_id_num,
        },
        u'slides': [
            {
                u'type': '1_to_5_slider',
                u'title': 'Title',
            }
        ]
    })
    if 'audytor' in request.session and request.session['audytor']['logged'] is True:
        return redirect('audytor:panel_presentation_edit', presentation_id=short_id_num)
    else:
        return redirect('audytor:index')


def presentation_edit(request, presentation_id):
    if 'audytor' in request.session and request.session['audytor']['logged'] is True:
        return render(request, 'audytor/presentation_edit.html')
    else:
        return redirect('audytor:index')


def user_settings(request):
    if 'audytor' in request.session and request.session['audytor']['logged'] is True:
        return render(request, 'audytor/usersettings.html')
    else:
        return redirect('audytor:panel')






def user_settings_update_general(request):
    if request.method == 'POST':

        is_error = False
        callback = [];

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
            request.session['audytor']['name'] = name
            request.session.save()
            audytor_ref = db.collection(u'audytors').document(request.session['audytor']['audytor_id'])
            audytor_ref.update({
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


def user_settings_update_email(request):
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
        print('request.session.audytor.email', request.session['audytor']['email'])
        if not email_exist(email, request.session['audytor']['email']):
            is_error = True
            callback.append({
                'place': 'callback-user-settings-email-email',
                'type': 'error',
                'msg': 'Podany email jest już w użyciu. Spróbuj inny',
            })

        audytor_ref = db.collection(u'audytors').document(request.session['audytor']['audytor_id'])
        audytor = audytor_ref.get().to_dict()
        match = bcrypt.checkpw(str(password).encode('utf-8'), audytor['password'])
        if match:  # passwords match
            if not is_error:
                request.session['audytor']['email'] = email
                request.session.save()
                audytor_ref = db.collection(u'audytors').document(request.session['audytor']['audytor_id'])
                audytor_ref.update({
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


def user_settings_update_password(request):
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

        audytor_ref = db.collection(u'audytors').document(request.session['audytor']['audytor_id'])
        audytor = audytor_ref.get().to_dict()
        match = bcrypt.checkpw(str(password_old).encode('utf-8'), audytor['password'])
        if match:  # passwords match
            if not is_error:
                audytor_ref.update({
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
    audytors_ref = db.collection(u'audytors')
    email_ref = audytors_ref.where(u'email', u'==', email)
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

    :return:
    """
    # PASSWORD-1 check if correct
    min_8_chars = False
    at_last_1_digit = False
    at_last_1_special_char = False
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
    for i in range(password_lenght):
        if password[i] in '`~!@#$%^&*()_-+={}[]\\|;;\'"<>,.?/':
            at_last_1_special_char = True
            break
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
    convert = Convert.Convert()
    max_dec = convert.max_dec_from_n_digit(num_od_digit)
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

def create_qr_code_link():
    pass