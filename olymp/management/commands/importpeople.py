from ...models import Olympiad, Person, Participation, Country
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DatabaseError
import os


class Command(BaseCommand):
    help = ("Updates the list of participants of <olympiad_id> from the given"
            " text file <first_name> <last_name> <country_code> <function>.\n"
            "Lines starting with '#' are ignored.")

    requires_model_validation = True

    def add_arguments(self, parser):
        parser.add_argument('olympiad_id', nargs='+', type=int)
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):

        try:
            _olympiad = Olympiad.objects.get(id=options['olympiad_id'][0])
        except Olympiad.DoesNotExist:
            raise CommandError("Olympiad %s does not exist"
                               % options['olympiad_id'])

        arg = options['filename'][0]

        if not os.path.exists(arg):
            raise CommandError("File not found: " + arg)
        stream = open(arg, 'r')

        with transaction.atomic():
            ok = True
            all_count = 0
            for line in stream:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                all_count += 1

                try:
                    decodedLine = line.split(" ")
                    if len(decodedLine) < 4:
                        self.stdout.write("Line %(line)s should consist of "
                                          "at least fuur words"
                                          % {'line': line})
                        ok = False
                    firstName = decodedLine[0]
                    lastName = " ".join(decodedLine[1:-2])
                    country = decodedLine[-2]
                    function = decodedLine[-1]
                    _person, _ = Person.objects.get_or_create(
                                    first_name=firstName,
                                    last_name=lastName)
                    if function not in \
                            [x for (x, _) in Participation.function_list]:
                        self.stdout.write("Invalid function %(function)s"
                                          % {'function': function})
                        ok = False
                    try:
                        _country = Country.objects.get(code=country)
                    except Country.DoesNotExist:
                        self.stdout.write("Country doesn't exists: "
                                          "%(country)s"
                                          % {'country': country})
                    _participation, _ = Participation.objects.get_or_create(
                                            person=_person,
                                            olympiad=_olympiad,
                                            country=_country,
                                            function=function)
                except DatabaseError as e:
                    message = e.message.decode('utf-8')
                    self.stdout.write(
                            "DB Error for line=%(line)s: %(message)s\n"
                            % {'line': line, 'message': message})
                    ok = False
            if ok:
                self.stdout.write("Processed %d entries" % (all_count))
            else:
                raise CommandError("There were some errors. Database not "
                                   "changed.\n")
