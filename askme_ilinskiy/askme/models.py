from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class User(models.Model):
    profile = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField()
    like = models.ManyToManyField("Like")

    def __str__(self):
        return self.username


class Like(models.Model):
    TYPE_POST = "p"
    TYPE_ANSWER = "a"
    TYPE_CHOICES = [
        (TYPE_POST, "Post"),
        (TYPE_POST, "Post"),
        (TYPE_ANSWER, "Answer"),
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, blank=False)

    class Value(models.IntegerChoices):
        MINUS = -1
        NEUTRAL = 0
        PLUS = 1

    value = models.IntegerField(choices=Value.choices, blank=False)


class Tag(models.Model):
    name = models.CharField(max_length=31)
    post = models.ManyToManyField("Post")


class PostManager(models.Manager):
    def new_posts(self, count_posts):
        posts = self.order_by("-data_time_creation")
        posts = posts[0:count_posts]
        return posts

    def popular_posts(self, count_posts):
        posts = self.order_by("-mark")
        posts = posts[0:count_posts]
        return posts

    def by_tag_posts(self, count_posts, cur_tag):
        posts = self.filter(tag, cur_tag)
        posts = posts[0:count_posts]
        return posts


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    mark = models.IntegerField(default=0)
    data_time_creation = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)


class Answer(models.Model):
    text = models.TextField(blank=False)
    mark = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    post_id = models.ForeignKey('Post', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)


def paginate(page_num, count_pages, arr):
    cur_arr = arr[page_num * count_pages:(page_num + 1) * count_pages]
    pagination = {"pages": []}
    if len(arr[(page_num - 1) * count_pages:page_num * count_pages]) != 0:
        pagination["pages"].append({"idPage": page_num - 1, "isActive": False})
        pagination["isExistPrev"] = True

    if len(cur_arr) == 0:
        page_num = 0
        cur_arr = arr[(page_num * count_pages): ((page_num + 1) * count_pages)]
        pagination = {"pages": [{"idPage": page_num, "isActive": True}], "isExistPrev": False}
    else:
        pagination["pages"].append({"idPage": page_num, "isActive": True})

    for i in range(1, 4):
        if len(arr[(page_num + i) * count_pages:(page_num + i + 1) * count_pages]) != 0:
            pagination["pages"].append({"idPage": page_num + i, "isActive": False})
            pagination["isExistNext"] = True

    return {"pagination": pagination, "cur_arr": cur_arr}


QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f'Text {i} Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum.',
        "answers": f"Answers: {i}",
        "tags": [{"name": f"tag{i}", "id": i},
                 {"name": f"tag{i + 1}", "id": i + 1}],
        "rating": f"{i}",
        "id": f"{i}",
    } for i in range(161)
]

TAGS = [
    {
        "text": f"Tag{i}",
        "color": f"black",
        "id": f"{i}"
    } for i in range(15)
]

BEST_MEMBERS = [
    {
        "text": f"Member{i}",
        "href": f"#"
    } for i in range(8)
]

AUTHOR = {
    "login": "dr_temp",
    "email": "temp@mail.ru",
    "nickname": "Dr. Temp",
}

ANSWERS = [
    {
        "text": f'Text answer {i}  Lorem Iporem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайнеsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для тек Lorem Ipsum является стандартной "рыбой" для текстов на латини Lorem Ipsum является стандартной "рыбой" для текстов на латини Lorem Ipsum является стандартной "рыбой" для текстов на латини Lorem Ipsum является стандартной "рыбой" для текстов на латинистов на латинице с',
        "rating": f'{i}',
        "isCorrect": True
    } for i in range(8)
]

PAGINATION = {
    "pages": [
        {"idPage": i, "isActive": True if i == 0 else False} for i in range(4)
    ],
    "isExistPrev": False,
    "isExistNext": True,
}
