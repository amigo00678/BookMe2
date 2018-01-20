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

        # create files in folder1
        folder1 = Folder.objects.create(name='Folder1')
        for i in range(10):
            File.objects.create(name='file_txt_'+str(i), type=FileTypeE.TXT, parent=folder1)

        for i in range(10):
            File.objects.create(name='file_audio_'+str(i), type=FileTypeE.AUDIO, parent=folder1)

        for i in range(10):
            File.objects.create(name='file_video_'+str(i), type=FileTypeE.VIDEO, parent=folder1)

        for i in range(10):
            File.objects.create(name='file_binary_'+str(i), type=FileTypeE.BINARY, parent=folder1)

        # create folders
        for i in range(10):
            Folder.objects.create(name='Folder' + str(i + 1))

