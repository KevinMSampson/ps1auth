from argparse import ArgumentTypeError
from django.core.management.base import BaseCommand, CommandError
from member_management.models import Person
from accounts.models import PS1User
from getpass import getpass
import re

def username(username):
    if not re.match(r"^[a-z][a-z0-9]{2,30}$", username):
        error_string = """
        Username must be all lower case,
        start with a letter,
        contain only letters and numbers,
        and be between 3 and 30 characters"""
        raise(ArgumentTypeError(error_string))

    users = PS1User.objects.get_users_by_field('sAMAccountName', username)
    if len(users) > 0:
        error_string = "The username {0} already exists.".format(username)
        raise ArgumentTypeError(error_string)

    return username


class Command(BaseCommand):
    help = "Create a person."
    def add_arguments(self, parser):
        parser.add_argument('username', type=username)
        parser.add_argument('-n', '--name')
        parser.add_argument('-m', '--email')
        parser.add_argument('-p', '--password')


    def handle(self, *args, **options):
        if options['name'] and ' ' in options['name']:
            first_name, last_name = options['name'].split(' ')
        elif options['name']:
            first_name = options['name']
            last_name = ""
        else:
            first_name = options['username']
            last_name = ""

        if options['password']:
            password = options['password']
        else:
            password = getpass()

        person = Person(
            first_name=first_name,
            last_name=last_name,
            email=options['email'],
        )
        person.save()
        user = PS1User.objects.create_superuser(
            options['username'],
            email=options['email'],
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        person.user = user
        person.save()
