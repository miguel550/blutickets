from django.http import HttpResponse
from django.shortcuts import render
import os

def load_text_view(request, *args):
    page = args[0]
    file = page + '.html'
    path = 'resources/text'
    content = open(os.path.join(path, file)).read()

    return render(request, 'text.html', {'text_content': content})
