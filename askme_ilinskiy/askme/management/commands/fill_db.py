from askme.models import Like2Post, Like2Answer, Tag, MyUser, Post, Answer

import random
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
import datetime
from faker import Faker


class CountElements:
    USERS = 0
    POSTS = 0
    ANSWERS = 0
    TAGS = 0
    LIKES = 0

    def set_values(self, ratio):
        self.USERS = ratio
        self.POSTS = ratio * 10
        self.ANSWERS = ratio * 100
        self.TAGS = ratio
        self.LIKES = ratio * 200


class Command(BaseCommand):
    help = 'Script fill_db'

    def add_arguments(self, parser):
        parser.add_argument(
            '-r',
            '--ratio',
            nargs=1,
            default=1,
            type=int,
            help='ratio that be used in fill db',
        )

    def handle(self, *args, **options):
        # Очистка таблиц
        Like2Post.objects.all().delete()
        Like2Answer.objects.all().delete()
        Answer.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        MyUser.objects.all().delete()
        User.objects.all().delete()

        users = MyUser.objects.all()
        if len(users) != 0:
            print(users)
            return "Error"

        ratio = options['ratio'][0]
        count_el = CountElements()
        count_el.set_values(ratio)
        Faker.seed(datetime.time())
        fake = Faker()

        avatars = [f"avatars_fill_db/{i}.png" for i in range(1, 11)]

        tags = [Tag(name=fake.word()[:31]) for _ in range(count_el.TAGS)]
        Tag.objects.bulk_create(tags)
        print("Tags filled success")

        users = [User(username=f"Username {i}",
                      password=make_password(f"password{i}"),
                      email=f'user{i}@user{i}.com') for i in range(count_el.USERS)]
        User.objects.bulk_create(users)
        print("users")

        my_users = [MyUser(profile=user, avatar=random.choice(avatars)) for user in users]
        MyUser.objects.bulk_create(my_users)
        print("MyUsers filled success")

        posts = [Post(user_id=random.choice(my_users),
                      title=f"Question{i}",
                      text=fake.text(),
                      ) for i in range(count_el.POSTS)]
        Post.objects.bulk_create(posts)
        print("Posts filled success")

        for i in range(count_el.TAGS):
            tags[i].post.set([posts[random.randint(0, count_el.POSTS - 1)] for _ in range(random.randint(0, 10))])

        answers = []
        for i in range(count_el.POSTS):
            for _ in range(random.randint(0, 4)):
                answers.append(Answer(user_id=random.choice(my_users),
                                      post_id=random.choice(posts),
                                      text=fake.text(),
                                      is_correct=random.choice([True, False]),
                                      ))
        Answer.objects.bulk_create(answers)
        print("Answers filled success")

        likes2posts = [Like2Post(value=random.randint(-1, 1), post_id=random.choice(posts)) for _ in
                       range(count_el.LIKES * 2 // 3)]
        Like2Post.objects.bulk_create(likes2posts)
        print("Like2post filled success")

        likes2answers = [Like2Answer(value=random.randint(-1, 1), answer_id=random.choice(answers)) for _ in
                         range(count_el.LIKES // 3)]
        Like2Answer.objects.bulk_create(likes2answers)
        print("Like2answer filled success")

        left = 0
        right = Post.objects.count()
        size = 10000
        while left <= right:
            posts = Post.objects.all()[left:left+size]
            for post in posts:
                post.mark = Like2Post.objects.getMarkPost(post.pk)
            Post.objects.bulk_update(posts, ["mark"])
            left += size
            print("likes filled in posts from " + left.__str__() + " to " + (left + size).__str__())
        print("LikesPosts upgrade  success")

        left = 0
        right = Answer.objects.count()
        size = 10000
        while left <= right:
            answers = Answer.objects.all()[left:left + size]
            for answer in answers:
                answer.mark = Like2Answer.objects.getMarkAnswer(answer.pk)
            Answer.objects.bulk_update(answers, ["mark"])
            left += size
            print("likes filled in answers from " + left.__str__() + " to " + (left + size).__str__())
        return "Filling db is OK"
