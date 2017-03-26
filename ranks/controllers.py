from olymp.models import Olympiad, Task, Person, Participation, Score, Country
from .utils import identify_person, identify_problem
import csv


def process_ranking(ranking):
    with open(ranking.ranking.path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        problems = reader.fieldnames[3:-1]
        identifiedProblems = []
        for problem in problems:
            identifiedProblems.append(identify_problem(ranking.olympiad,
                                                       problem))
        for row in reader:
            person = identify_person(row["first name"], row["last name"])
            if person is None:
                person = Person.objects.create(
                    first_name=row["first name"],
                    last_name=row["last name"])
                person.save()
            country = Country.objects.get(name=row["country"])
            pt = Participation.objects.create(
                person=person,
                olympiad=ranking.olympiad,
                country=country,
                function="PAR"
            )
            pt.save()
            for problem in identifiedProblems:
                try:
                    score = float(row[problem.shortcut])
                except ValueError:
                    score = None
                s = Score.objects.create(
                    participation=pt,
                    task=problem,
                    result=score
                )
                s.save()
