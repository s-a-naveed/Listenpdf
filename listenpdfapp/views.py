from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import pyttsx3, PyPDF2
from PyPDF2.errors import PdfReadError
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
import sys
# Create your views here.
def home(request):
    try:
        if request.method == "POST":
            pdffile = request.FILES['pdf_file']
            pdf_data = extract_text_from_pdf(pdffile)
            print('PDF Extracted Successfully')
            request.session['data']=pdf_data
            return HttpResponseRedirect('/readpage/')
    except PdfReadError:
        messages.add_message(request, messages.ERROR ,'Please choose right pdf file which contains only text!!!')
        return HttpResponseRedirect('/')
    except MultiValueDictKeyError:
        messages.add_message(request, messages.ERROR ,'Please select any file!!!')
        return HttpResponseRedirect('/')
    else:
        return render(request, 'home.html')


def readpage(request):
    data = request.session.get('data')
    bot = pyttsx3.init()
    if request.method=="POST":
        pdf_data = data
        
        voices = bot.getProperty('voices')
        bot.setProperty('voice', voices[1].id)
        bot.setProperty('rate', 150) 
        bot.setProperty('volume', 1)
        
        bot.say(pdf_data)
        try:
            bot.runAndWait()
        except RuntimeError:
            messages.add_message(request, messages.ERROR, '''We are sorry for the inconvinience, as you are not able to stop or pause the speech while playing.''')
            return HttpResponseRedirect('/error/')
    return render(request, 'readpage.html', {'data':data})


def extract_text_from_pdf(pdf_file):
    text = ''
    reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def errorpage(request):
    return render(request, 'error.html')