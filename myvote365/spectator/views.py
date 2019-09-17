from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
import static.python.convert as Convert

# Create your views here.


def index(request, short_id_num):
    short_id_num = str(short_id_num).upper()
    convert = Convert.Convert()
    short_id_dec = convert.num2dec(short_id_num)
    context = {
        'short_id_num': short_id_num,
        'short_id_dec': short_id_dec,
    }
    return render(request, 'spectator/index.html', context=context)
