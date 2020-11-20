from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .BasicAnalysis import ngram, ngramComparison, sentenceLengthComparison
import nltk
from nltk import word_tokenize

# Create your views here.
def index(request):
    return render(request, 'index.html', { 'name': 'viikkar'})

def test(request):
    return render(request, 'test.html')

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
        ngram_pct_similarity = ngramComparison(anontext, authoratext)
        sentence_length_pct_similarity = sentenceLengthComparison(anontext, authoratext)
        return render(request, 'direct.html', {
            'ngram_pct_similarity': ngram_pct_similarity,
            'sentence_length_pct_similarity': sentence_length_pct_similarity,
        })
    return render(request, 'direct.html')