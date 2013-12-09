from django.http import HttpResponse
from django.shortcuts import render

from chesire.core.utils.scrape import WikipediaScraper
from chesire.core.models import Article

def home(request):
    context = {}

    return render(request, 'index.html', context)

def testing(request):
    context = {}
    return HttpResponse(Article.objects.all(), context)

def wikipedia(request):
    keyword = request.GET.get('keyword')

    scraper = WikipediaScraper()
    wiki_answer = scraper.query(keyword)

    return HttpResponse(wiki_answer)

