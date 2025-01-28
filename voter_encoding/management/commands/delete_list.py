from django.core.management.base import BaseCommand
from voter_encoding.models import VotersList

class Command(BaseCommand):
    help = 'Delete all rows from the VotersList table'

    def handle(self, *args, **kwargs):
        # Deleting all records from the VotersList table
        VotersList.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all voter data from the VotersList table.'))
