from askme.models import Like2Post, Like2Answer, Tag, MyUser, Post, Answer

import random
from django.contrib.auth.models import User
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

        avatars = [f"static/img/ava/{i}.png" for i in range(1, 11)]
        # print(avatars)
        # print('\n')
        # print(count_el.TAGS)

        tags = [Tag(name=fake.word()[:31]) for _ in range(count_el.TAGS)]
        Tag.objects.bulk_create(tags)
        print("Tags filled success")
        # print(tags)

        users = []
        used_usernames = set()
        for i in range(count_el.USERS):
            while True:
                username = fake.first_name()
                if username not in used_usernames:
                    used_usernames.add(username)
                    break

            user = User.objects.create(username=username, email=fake.email(), password=fake.password())
            my_user = MyUser(profile=user, avatar=random.choice(avatars))
            users.append(my_user)
        MyUser.objects.bulk_create(users)
        print("MyUsers filled success")
        # print(users)

        posts = [Post(user_id=random.choice(users),
                      title=f"Question{i}",
                      text=fake.text(),
                      ) for i in range(count_el.POSTS)]
        Post.objects.bulk_create(posts)
        print("Posts filled success")
        # posts = Post.objects.all()
        for i in range(count_el.TAGS):
            tags[i].post.set([posts[random.randint(0, count_el.POSTS - 1)] for _ in range(random.randint(0, 10))])
        # print(tags)

        answers = []
        for i in range(count_el.POSTS):
            for _ in range(random.randint(0, 4)):
                answers.append(Answer(user_id=random.choice(users),
                                      post_id=random.choice(posts),
                                      text=fake.text(),
                                      is_correct=random.choice([True, False]),
                                      ))
        # print(answers)
        Answer.objects.bulk_create(answers)
        print("Answers filled success")

        likes2posts = [Like2Post(value=random.randint(-1, 1), post_id=random.choice(posts)) for _ in
                       range(count_el.LIKES * 2 // 3 )]
        # print(likes2posts)
        Like2Post.objects.bulk_create(likes2posts)
        print("Like2post filled success")

        likes2answers = [Like2Answer(value=random.randint(-1, 1), answer_id=random.choice(answers)) for _ in
                       range(count_el.LIKES // 3)]
        # print(likes2answers)
        Like2Answer.objects.bulk_create(likes2answers)
        print("Like2answer filled success")

        for post in posts:
            post.mark = Like2Post.objects.getMarkPost(post.id)

        print("LikesPosts upgrade  success")
        for answer in answers:
            answer.mark = Like2Answer.objects.getMarkAnswer(answer.id)
        print("LikesAnswer upgrade success")

        return "Filling db is OK"

        # likes2posts = [Like2Post(to_whom=choice(profiles), from_whom=choice(profiles)) for _ in range(Count.CONTENT_LIKES)]
        # Like.objects.bulk_create(likes)

        # for i in range(0, 30):
        #     user = User.objects.create_user(
        #         username=fake.username(),
        #         password=fake.password(length=12),
        #         email=fake.email(),
        #     )
        #     user.profile.nick_name = fake.username()
        #     user.save()
        # users = User.objects.all()
