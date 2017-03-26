from django.shortcuts import get_object_or_404, render

from .models import Task, Olympiad, Person, Country, Participation


def olympiads(request):
    olympiads = Olympiad.objects.all()
    context = {'olympiads': olympiads}
    return render(request, 'olymp/olympiads.html', context)


def olympiad(request, olympiad_id):
    olympiad = get_object_or_404(Olympiad, pk=olympiad_id)
    countries = olympiad.participated_countries()
    participations = []
    for country in countries:
        participations.append((
            country,
            olympiad.participation_set.filter(country=country),
        ))
    context = {'olympiad': olympiad, 'participations': participations}
    return render(request, 'olymp/olympiad.html', context)


def ranking(request, olympiad_id):
    olympiad = get_object_or_404(Olympiad, pk=olympiad_id)
    context = {'olympiad': olympiad}
    return render(request, 'olymp/ranking.html', context)


def tasks(request):
    tasks = Task.objects.all()
    from random import choice
    chosen_task = choice(tasks)
    context = {'tasks': tasks, 'chosen_task': chosen_task}
    return render(request, 'olymp/tasks.html', context)


def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {'person': person}
    return render(request, 'olymp/person.html', context)


def people(request):
    people = Person.objects.all()
    context = {'people': people}
    return render(request, 'olymp/people.html', context)


def country(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    olympiads = country.organized_olympiads()
    participations = []
    for olympiad in country.participated_olympiads():
        participations.append(
            (olympiad,
             Participation.objects.filter(country=country, olympiad=olympiad)))
    context = {'country': country, 'olympiads': olympiads,
               'participations': participations}
    return render(request, 'olymp/country.html', context)


def hall_of_fame(request):
    treshold = sorted(Person.objects.all(),
                      key=lambda p: p.medals_score())[-10]
    people = [x for x in Person.objects.all()
              if x.medals_score() >= treshold.medals_score()]
    countries = Country.objects.all()
    context = {
        'people': reversed(sorted(people, key=lambda p: p.medals_score())),
        'countries': reversed(
            sorted(countries, key=lambda p: p.medals_score()))
    }
    return render(request, 'olymp/hall_of_fame.html', context)
