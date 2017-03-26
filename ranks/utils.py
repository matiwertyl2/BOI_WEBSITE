from olymp.models import Person
from django.core.exceptions import ValidationError


def identify_problem(olympiad, problem):
    candidates = [x for x in olympiad.problems() if x.shortcut == problem]
    if len(candidates) != 1:
        raise ValidationError("problem "+problem+" has "+str(len(candidates)) +
                              " candidates to match (should be exactly one)")
    return candidates[0]


def identify_person(first_name, last_name):
    candidates = Person.objects.filter(
        first_name=first_name,
        last_name=last_name)
    if len(candidates) > 1:
        raise ValidationError(first_name+" "+last_name+" has " +
                              str(len(candidates)) +
                              " candidates to match (should be at most one)")
    if candidates:
        return candidates[0]
    else:
        return None
