from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class MyUser(models.Model):
    profile = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="static/img/ava", default="static/img/default_avatar.jpg")

    like2post = models.ManyToManyField("Like2Post")
    like2answer = models.ManyToManyField("Like2Answer")

    def __str__(self):
        return self.profile.username


class ValueLike(models.IntegerChoices):
    MINUS = -1
    NEUTRAL = 0
    PLUS = 1


class ManagerLike2Post(models.Manager):
    def getMarkPost(self, post_id):
        likes = self.filter(post_id=post_id)
        mark = 0
        for like in likes:
            mark += like.value
        return mark


class Like2Post(models.Model):
    value = models.IntegerField(choices=ValueLike.choices, blank=False)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)

    objects = ManagerLike2Post()

    def __str__(self):
        return self.value.__str__()


class ManagerLike2Answer(models.Manager):
    def getMarkAnswer(self, answer_id):
        likes = self.filter(answer_id=answer_id)
        mark = 0
        for like in likes:
            mark += like.value
        return mark


class Like2Answer(models.Model):
    value = models.IntegerField(choices=ValueLike.choices, blank=False)
    answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE)

    objects = ManagerLike2Answer()

    def __str__(self):
        return self.value.__str__()


class Tag(models.Model):
    name = models.CharField(max_length=31)
    post = models.ManyToManyField("Post")

    def __str__(self):
        return self.name


class ManagerPost(models.Manager):
    def popularPosts(self, left, right):
        posts = self.order_by("-mark")
        return posts[left:right]

    def byTagPosts(self, cur_tag, left, right):
        posts = self.filter(tag=cur_tag)
        return posts[left:right]

    def newPosts(self, left, right):
        posts = self.order_by('-data_time_creation')
        return posts[left:right]

    def addTags(self, posts):
        posts_list = posts.values()
        for i in range(len(posts_list)):
            tags = posts[i].tag_set.all()
            posts_list[i]["tags"] = tags
        return posts_list


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    mark = models.IntegerField(default=0)
    data_time_creation = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('MyUser', on_delete=models.PROTECT)

    objects = ManagerPost()

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(blank=False)
    mark = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    post_id = models.ForeignKey('Post', on_delete=models.PROTECT)
    user_id = models.ForeignKey('MyUser', on_delete=models.PROTECT)

    def __str__(self):
        return self.text[
               :10] + ' ' + self.is_correct.__str__() + " " + self.post_id.__str__() + " " + self.user_id.__str__()


def paginate(page_num, count_pages, arr):
    cur_arr = arr[page_num * count_pages:(page_num + 1) * count_pages]
    pagination = {"pages": []}
    if page_num >=1 and len(arr[(page_num - 1) * count_pages:page_num * count_pages]) != 0:
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
