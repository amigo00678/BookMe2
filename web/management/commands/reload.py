from django.core.management.base import BaseCommand, CommandError

from web.models import *
from web.constants import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def clear(self):
        User.objects.all().delete()
        Folder.objects.all().delete()
        File.objects.all().delete()

    def handle(self, *args, **options):
        self.clear()
        self.create_files()
        self.create_folders()
        self.create_users()

    def create_files(self):
        # create files in folder1
        folder1 = Folder.objects.create(name='Folder1')
        for i in range(10):
            File.objects.create(name='file_txt_'+str(i), type=1, parent=folder1)

        for i in range(10):
            File.objects.create(name='file_audio_'+str(i), type=2, parent=folder1)

        for i in range(10):
            File.objects.create(name='file_video_'+str(i), type=3, parent=folder1)

        for i in range(10):
            File.objects.create(name='file_binary_'+str(i), type=4, parent=folder1)

    def create_folders(self):
        # create folders
        for i in range(10):
            Folder.objects.create(name='Folder' + str(i + 1))

    def create_users(self):
        # create users
        User.objects.create_user(email='u@u.com', password='123',
            first_name="UFn", last_name="ULn")
