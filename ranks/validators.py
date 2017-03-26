from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from olymp.models import Olympiad, Task, Person, Participation, Score, Country
from .utils import identify_person, identify_problem
import csv


def check_header(header):
    if header[0] != "first name":
        return False
    if header[1] != "last name":
        return False
    if header[2] != "country":
        return False
    if header[-1] != "sum":
        return False
    return True


def check_score(problem, score):
    try:
        score = float(score)
        if not (0.0 <= score and score <= problem.perfect_score):
            raise ValidationError("Invalid score: "+str(score) +
                                  "(should be between 0.0 and " +
                                  str(problem.perfect_score)+")")
    except ValueError:
        pass


def check_country(country):
    candidates = Country.objects.filter(name=country)
    if len(candidates) != 1:
        raise ValidationError("country "+country+" has "+str(len(candidates)) +
                              " candidates to match (should be exactly one)")


def validate_ranking(ranking):
    try:
        the_csv = ranking.ranking.read().decode("utf-8").splitlines()
        reader = csv.DictReader(the_csv, delimiter=',')
    except Exception as e:
        raise ValidationError("Error while parsing: "+str(e))
    if not check_header(reader.fieldnames):
        raise ValidationError("Invalid header, should be: "
                              "['first name', 'last name', 'country', "
                              "'aaa', 'bbb', ..., 'sum']"
                              " found '"+str(reader.fieldnames)+"'")
    problems = reader.fieldnames[3:-1]
    identifiedProblems = []
    for problem in problems:
        identifiedProblems.append(identify_problem(ranking.olympiad,
                                                   problem))
    for row in reader:
        identify_person(row["first name"], row["last name"])
        check_country(row["country"])
        for problem in identifiedProblems:
            check_score(problem, row[problem.shortcut])
