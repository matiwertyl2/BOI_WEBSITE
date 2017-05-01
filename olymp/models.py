from django.db import models
import datetime
from django.core.exceptions import ValidationError
from collections import defaultdict
from memoize import memoize
from collections import defaultdict
from boi.settings import TIMEOUT


class Entity(models.Model):

    class Meta:
        abstract = True

    @memoize(timeout=TIMEOUT)
    def awards(self):
        awards = defaultdict(int)
        for part in self.participation_set.all():
            awards[part.award()] += 1
        return awards

    def golden_medals(self):
        return self.awards()['golden medal']

    def silver_medals(self):
        return self.awards()['silver medal']

    def bronze_medals(self):
        return self.awards()['bronze medal']

    def medals_score(self):
        medals = self.awards()
        return (medals["golden medal"], medals["silver medal"],
                medals["bronze medal"])


class Country(Entity):
    name = models.CharField(max_length=200)
    code = models.CharField('ISO 3166-1 alpha-2 code', max_length=2,
                            primary_key=True)

    class Meta:
        ordering = [
         'name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def organized_olympiads(self):
        return self.olympiad_set.all()

    def organized_olympiads_no(self):
        return len(self.organized_olympiads())

    def participated_olympiads(self):
        return list(reversed(sorted(list(set(
            [x.olympiad for x in self.participation_set.all()])),
            key=lambda x: x.start_date)))

    def participated_olympiads_no(self):
        return len(self.participated_olympiads())

    def first_partcipation(self):
        participations = [x.year() for x in self.participated_olympiads()]
        if participations:
            return min(participations)


class Person(Entity):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(null=True, upload_to='photos/', blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    sexes = [
     ('M', 'Male'),
     ('F', 'Female')]
    sex = models.CharField(choices=sexes, max_length=1, null=True, blank=True)

    class Meta:
        ordering = [
         'last_name', 'first_name']
        verbose_name_plural = 'People'

    def participated_olympiads_no(self):
        return len(self.participation_set.filter(function="PAR"))

    def participations_list(self):
        olympiads = set([x.olympiad for x in self.participation_set.all()])
        list = []
        for olympiad in olympiads:
            list.append((olympiad,
                         self.participation_set.filter(olympiad=olympiad)))
        return list

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Olympiad(models.Model):
    city = models.CharField(max_length=200)
    country = models.ForeignKey(Country)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.FileField(blank=True, upload_to='logos/')
    gold_threshold = models.FloatField(null=True, blank=True)
    silver_threshold = models.FloatField(null=True, blank=True)
    bronze_threshold = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = [
         '-start_date']

    def year(self):
        return self.start_date.year

    def __str__(self):
        return 'BOI ' + str(self.year())

    def problems(self):
        return self.task_set.all()

    def sorted_problems(self):
        problems = [task.shortcut for task in self.task_set.all()]
        problems.sort()
        return problems

    def people(self):
        return set(x.person for x in self.participation_set.all())

    def participants(self):
        return list(sorted(filter(
            lambda x: x.function == 'PAR',
            self.participation_set.all()), key=lambda x: -x.final_score()))

    def all_participants(self):
        return list(sorted(filter(
            lambda x: x.function == 'PAR' or x.function == 'OOC',
            self.participation_set.all()), key=lambda x: -x.final_score()))

    def president(self):
        return self.participation_set.filter(function="PRE")

    def organizing_committee(self):
        return self.participation_set.filter(function="ORG")

    def scientific_committee(self):
        return self.participation_set.filter(function="SC")

    def technical_committee(self):
        return self.participation_set.filter(function="TC")

    def golden_medalists(self):
        return list(filter(
            lambda x: x.award() == 'golden medal', self.participants()))

    def participants_number(self):
        return len(self.participants())

    def participated_countries(self):
        return list(sorted(list(set(
            [x.country for x in self.participation_set.all()])),
            key=lambda x: x.name))

    def countries_number(self):
        return len(self.participated_countries())

    def scores(self):
        return list(
            filter(None, [x.final_score() for x in self.participants()]))


class Task(models.Model):
    olympiad = models.ForeignKey(Olympiad, default=0)
    name = models.CharField(max_length=200)
    shortcut = models.CharField(max_length=10)
    day_choices = ((0, '0'), (1, '1'), (2, '2'))
    test = models.BooleanField('Test task (not counted in final score)?',
                               default=False)
    day = models.IntegerField(choices=day_choices, blank=True, null=True)
    #statement = models.FileField(blank=True, null=True)
    #solution = models.FileField(blank=True, null=True)
    #tests = models.FileField(blank=True, null=True)
    #spoiler = models.FileField(blank=True, null=True)
    perfect_score = models.FloatField(default=100.0)

    class Meta:
        ordering = [
         'olympiad', 'day', 'shortcut']

    def average_score_for_task(self):
        submissions = list(filter(
            lambda x: x.result is not None, self.score_set.all()))
        if submissions:
            return round(
                sum([x.result for x in submissions]) / len(submissions), 2)
        else:
            return 0.0

    def perfect_scores_for_task(self):
        return list(filter(
            lambda x: x.result == self.perfect_score, self.score_set.all()))

    def perfect_score_example(self):
        ps = self.perfect_scores_for_task()
        if ps:
            from random import choice
            return choice(ps)
        return None

    def files(self):
        return self.taskfile_set.all()

    def __str__(self):
        return 'Problem {} ({}) on {}'.format(self.name, self.shortcut,
                                              str(self.olympiad))


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(blank=True, upload_to='tasks/')
    file_types = [(x, x) for x in
                  ['statement', 'tests', 'solution', 'spoiler', 'other']]
    type = models.CharField(choices=file_types, max_length=10, blank=True,
                            null=True)
    language = models.ForeignKey(Country, blank=True, null=True)


class Participation(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    country = models.ForeignKey(Country)
    sizes = [(x, x) for x in ['S', 'M', 'L', 'XL', 'XXL']]
    T_shirt_size = models.CharField(choices=sizes, max_length=5, blank=True,
                                    null=True)
    function_list = [
     ('PAR', 'participant'),
     ('LEA', 'team leader'),
     ('OOC', 'second team (out of competition)'),
     ('PRE', 'main organizer'),
     ('ORG', 'organization committee'),
     ('SC', 'scientific committee'),
     ('TC', 'technical committee'),
     ('GUE', 'guest')]
    function = models.CharField(choices=function_list, default='participant',
                                max_length=3)

    def function_name(self):
        return dict(Participation.function_list)[self.function]

    @memoize(timeout=TIMEOUT)
    def final_score(self):
        scores = self.score_set.all()
        scores_without_test_tasks = list(filter(
            lambda x: x.task.test is False, scores))
        final_scores = list(
            filter(None, [x.result for x in scores_without_test_tasks]))
        if final_scores:
            return sum(final_scores)
        return 0.0

    @memoize(timeout=TIMEOUT)
    def award(self):
        if self.function != 'PAR':
            return None
        if self.olympiad.gold_threshold is not None and \
                self.final_score() >= self.olympiad.gold_threshold:
            return 'golden medal'
        if self.olympiad.silver_threshold is not None and \
                self.final_score() >= self.olympiad.silver_threshold:
            return 'silver medal'
        if self.olympiad.bronze_threshold is not None and \
                self.final_score() >= self.olympiad.bronze_threshold:
            return 'bronze medal'

    def scores(self):
        scores = []
        for problem in self.olympiad.problems():
            scores.append(self.score_set.get(task=problem).result)
        return scores

    @memoize(timeout=TIMEOUT)
    def place(self):
        if self.function != 'PAR':
            return
        return len(list(
            filter(lambda x: x > self.final_score(),
                   self.olympiad.scores()))) + 1

    def __str__(self):
        return 'Participation of ' + \
            str(self.person) + ' in ' + str(self.olympiad)

    class Meta:
        ordering = ['olympiad', 'person']


class Score(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE)
    result = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{}: {} ({} - task {})'.format(
            self.participation.person,
            self.result, self.participation.olympiad, self.task.name)

    def clean(self):
        if self.task.olympiad != self.participation.olympiad:
            raise ValidationError('Olympiad differs in task/participation.')
            if self.result < 0:
                raise ValidationError('Result cannot be negative.')
                if self.result > self.task.perfect_score:
                    pass
            raise ValidationError(
                'Result cannot be larger than perfect score for this task.')
