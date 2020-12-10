from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .BasicAnalysis import ngram, ngramComparison, sentenceLengthComparison, add_new_author, list_authors
import nltk
from nltk import word_tokenize

# Create your views here.
def index(request):
    return render(request, 'index.html', { 'name': 'viikkar'})
def home(request):
    return render(request, 'home.html')

def help(request):
    return render(request, 'help.html')

def upload(request):
    # If the file is the anonymous file
    if request.method == 'POST' and request.FILES['anonfile']:
        anonfile = request.FILES['anonfile']
        fs = FileSystemStorage()
        print("File ext: " + str(anonfile.name)[-3:])
        print(anonfile.name)
        if(anonfile.name[-3:] == 'txt'):
            filename = fs.save('anonfile.txt', anonfile)
        else:
            return render(request, 'upload.html', {
                'upload_error': 'Incompatible Format',
            })
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })



    # If the file is
    return render(request, 'upload.html')


def direct(request):
    if request.method == 'POST':
        anontext = request.POST.get('anontext', None)
        authoratext = request.POST.get('authoratext', None)
        try:
            ngram_pct_similarity = ngramComparison(anontext, authoratext)
            sentence_length_pct_similarity = sentenceLengthComparison(anontext, authoratext)
        except:
            ngram_pct_similarity = ''
            sentence_length_pct_similarity = ''
        return render(request, 'direct.html', {
            'ngram_pct_similarity': ngram_pct_similarity,
            'ngram_pct_similarity': ngram_pct_similarity,
            'sentence_length_pct_similarity': sentence_length_pct_similarity,
        })
    return render(request, 'direct.html')


def addauthor(request):
    if request.method == 'POST':
        authoroutput = ''
        authorname = request.POST.get('authorname', None)
        firstsample = request.POST.get('firstsample', None)
        secondsample = request.POST.get('secondsample', None)
        thirdsample = request.POST.get('thirdsample', None)
        fourthsample = request.POST.get('fourthsample', None)
        fifthsample = request.POST.get('fifthsample', None)
        try:
            add_new_author(authorname, firstsample, secondsample, thirdsample, fourthsample, fifthsample)
            print("Success!")
            authoroutput = "Author successfully added to the database!"
        except:
            print("Error, unable to add author.")
            authoroutput = "Error, Incorrect Formatting"

        return render(request, 'addauthor.html', {
            'authoroutput': authoroutput,
        })
    return render(request, 'addauthor.html')


def listauthors(request):
    authorlist = list_authors()
    return render(request, 'listauthors.html', {
        'authorlist': authorlist,
    })