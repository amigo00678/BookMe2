from django.core.management.base import BaseCommand, CommandError

from web.models import *
from web.constants import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def clear(self):
        Folder.objects.all().delete()
        File.objects.all().delete()

    def handle(self, *args, **options):
        self.clear()
        folder1 = Folder.objects.create(name='Folder1')
        for i in range(10):
            File.objects.create(name='file_txt_'+str(i), type=FileTypeE.TXT, parent=folder1)