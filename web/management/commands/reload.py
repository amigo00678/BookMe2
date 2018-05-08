from random import randint

from django.core.management.base import BaseCommand, CommandError

from web.models import *
from web.constants import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def clear(self):
        User.objects.all().delete()
        Folder.objects.all().delete()
        File.objects.all().delete()
        Feature.objects.all().delete()

    def handle(self, *args, **options):
        self.clear()
        self.create_features()
        self.create_room_features()
        self.create_users()
        self.create_files()
        self.create_folders()

    def create_features(self):
        Feature.objects.create(name="First Feature", key="feature_1", image="uploads/f1.JPG", is_main=True)
        Feature.objects.create(name="Second Feature", key="feature_2", image="uploads/f2.JPG", is_main=True)
        Feature.objects.create(name="Feature 3", key="feature_3", image="uploads/f3.JPG", is_main=True)
        Feature.objects.create(name="Feature 4", key="feature_4", image="uploads/f4.JPG", is_main=True)

        Feature.objects.create(name="Fifth Feature", key="feature_5", image="uploads/f5.JPG", is_main=False)
        Feature.objects.create(name="Sixth Feature", key="feature_6", image="uploads/f6.JPG", is_main=False)

    def create_room_features(self):
        RoomFeature.objects.create(name='Room feature 1', image="uploads/f1.JPG")
        RoomFeature.objects.create(name='Room feature 2', image="uploads/f2.JPG")
        RoomFeature.objects.create(name='Room feature 3')
        RoomFeature.objects.create(name='Room feature 4')

    def create_images(self):
        slider = ImageSlider.objects.create()

        image = SliderImage.objects.create(image="uploads/img_01NS.JPG")
        slider.images.add(image)

        image = SliderImage.objects.create(image="uploads/img_5UZ8.jpg")
        slider.images.add(image)

        image = SliderImage.objects.create(image="uploads/img_8GK0.JPG")
        slider.images.add(image)

        return slider

    def create_reviews(self, file, count, from_user):
        for i in range(count):
            Review.objects.create(rate=i, user=from_user, item=file, type=randint(1, 5),
                heading="<strong>Lorem ipsum!</strong>",
                pros="<strong>Lorem ipsum!</strong>Lorem ipsum! Lorem ipsum! Lorem ipsum!",
                cons="<strong>Lorem ipsum!</strong>Lorem ipsum! Lorem ipsum! Lorem ipsum!"
            )


    def create_files(self):
        # create files in folder1
        folder1 = Folder.objects.create(name='Folder1')
        features = Feature.objects.all()

        slider = self.create_images()

        top_content = "<p><strong>Lorem ipsum!</strong></p>"
        middle_content = "<p>Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum! Lorem ipsum!</p>"

        for i in range(10):
            file = File.objects.create(name='file_txt_'+str(i), type=1, parent=folder1,
                top_content=top_content, middle_content=middle_content, owner=User.objects.last())
            file.features = features
            file.top_slider = slider
            file.save()
            self.create_reviews(file, 10 - i,
                User.objects.filter(email="c@c.com").first())

        for i in range(10):
            File.objects.create(name='file_audio_'+str(i), type=2, parent=folder1,
                top_content=top_content, middle_content=middle_content, owner=User.objects.last())
            file.features = features
            file.save()

        for i in range(10):
            File.objects.create(name='file_video_'+str(i), type=3, parent=folder1,
                top_content=top_content, middle_content=middle_content, owner=User.objects.last())
            file.features = features
            file.save()

        for i in range(10):
            File.objects.create(name='file_binary_'+str(i), type=4, parent=folder1,
                top_content=top_content, middle_content=middle_content, owner=User.objects.last())
            file.features = features
            file.save()

    def create_folders(self):
        # create folders
        for i in range(10):
            Folder.objects.create(name='Folder' + str(i + 1))

    def create_users(self):
        # create users
        User.objects.create_user(email='u@u.com', password='123',
            first_name="UFn", last_name="ULn", type=1)
        User.objects.create_user(email='c@c.com', password='123',
            first_name="CFn", last_name="CLn", type=2)
