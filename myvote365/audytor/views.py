from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import string
import requests

cred = credentials.Certificate('static/__PRIVATE__/myvote365-aa6f5-firebase-adminsdk-ipqcy-ce6c711131.json')
firebase_admin.initialize_app(cred)
db = firestore.client();


def audytor_register(request):
    if request.method == 'POST':

        is_error = False
        callback = [];

        # requested data
        first_last_name = str(request.POST.get('first_last_name')).strip()
        email = str(request.POST.get('email')).strip()
        password_1 = str(request.POST.get('password_1')).strip()
        password_2 = str(request.POST.get('password_2')).strip()
        reCaptcha_response = str(request.POST.get('reCaptcha_response'))
        register_date = str(datetime.now())

        # EMAIL check if email exist
        audytors_ref = db.collection(u'audytors')
        email_ref = audytors_ref.where(u'email', u'==', email)
        email_content = email_ref.get()
        index = 0;
        for tmp in email_content:
            index = index + 1
        if index > 0:
            is_error = True
            callback.append({
                'place': 'callback-register-email',
                'type': 'error',
                'msg': 'Podany email jest już w użyciu. Spróbuj się zalogować',
            })

        # PASSWORD-1 check if correct
        min_8_chars = False
        at_last_1_digit = False
        at_last_1_special_char = False
        at_last_1_uppercase = False
        at_last_1_lowercase = False

        password_lenght = len(password_1)
        # PASSWORD-1 min 8 chars
        if password_lenght >= 8:
            min_8_chars = True
        # PASSWORD-1 at last 1 digit
        for i in range(password_lenght):
            if password_1[i] in string.digits:
                at_last_1_digit = True
                break
        # PASSWORD-1 at last 1 special char
        for i in range(password_lenght):
            if password_1[i] in '`~!@#$%^&*()_-+={}[]\\|;;\'"<>,.?/':
                at_last_1_special_char = True
                break
        # PASSWORD-1 at last 1 uppercase
        for i in range(password_lenght):
            if password_1[i] in string.ascii_uppercase:
                at_last_1_uppercase = True
                break
        # PASSWORD-1 at last 1 lowercase
        for i in range(password_lenght):
            if password_1[i] in string.ascii_lowercase:
                at_last_1_lowercase = True
                break
        # PASSWORD-1 final check
        if min_8_chars and at_last_1_digit and at_last_1_special_char and at_last_1_uppercase and at_last_1_lowercase:
            pass
        else:
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
                'msg': 'Hasła nie są od siebie różnią',
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
            print(reCaptcha_json_result)
            if not reCaptcha_json_result['success']:
                is_error = True
                callback.append({
                    'place': 'callback-register-submit',
                    'type': 'error',
                    'msg': 'reChaptcha errror',
                })



    else:
        callback = [
            {
                'place': 'callback-register-submit',
                'type': 'error',
                'msg': 'Coś poszło nie tak, spróbuj ponownie później.',
            },
        ]

    json_callback = json.dumps(callback)
    return HttpResponse(json_callback)


def audytor_login(request):
    pass


def audytor_login_register(request):
    return render(request, 'audytor/login_register.html')


def audytor_logout(request):
    pass


def show_conference_list(request):
    pass
