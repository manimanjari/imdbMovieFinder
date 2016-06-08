import json
import logging
import re
import sys


from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader


from mechanize import Browser
from BeautifulSoup import BeautifulSoup


# It is used to Display the movie details it takes\n
# name as input and gives movies details
def name(request, string):

    movie = string.replace("_", "+")
    br = Browser()
    br.open("http://www.imdb.com/find?s=tt&q="+movie)
    link = br.find_link(url_regex=re.compile(r"/title/tt.*"))
    data = br.follow_link(link)
    soup = BeautifulSoup(data.read())

    title = soup.find('h1').contents[0].strip()
    name = title.replace("&nbsp;", "")
    rating = soup.find('span', itemprop='ratingValue').contents[0]
    duration = soup.find('time', itemprop='duration').contents[0].strip()
    releaseDate = soup.find('a', title='See more release dates').contents[0]
    director = soup.find('span', itemprop='director').getText()
    actor_all = []
    actors = soup.findAll('span', itemprop='actors')
    for i in range(len(actors)):
        actor_all.append((actors[i].contents[1]).getText())
    genres_all = []
    genres = soup.findAll('span', itemprop='genre')
    for i in range(len(genres)):
        genres_all.append(genres[i].getText())

    jsonObject = {}
    jsonObject['Name:'] = name
    jsonObject['IMDB Rating:'] = rating
    jsonObject['Duration'] = duration
    jsonObject["Actors: "] = actor_all
    jsonObject['Director:'] = director
    jsonObject['Genres'] = genres_all
    jsonObject['Release Date'] = releaseDate
    movie_details = json.dumps(jsonObject)
    return HttpResponse(movie_details)


# It is used to render the html template
def search_form(request):
    template = loader.get_template('search_form.html')
    return HttpResponse(template.render())
