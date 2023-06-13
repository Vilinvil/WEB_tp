from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class MyUser(models.Model):
    profile = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars/%y/%m/%d/',
                               default='default_avatar.jpg')

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

    def addTagsAndAvatars(self, posts):
        posts_dict = posts.select_related('user_id').values('id', 'title', 'text', 'mark', 'user_id')
        for i in range(len(posts_dict)):
            posts_dict[i]['avatar_url'] = posts[i].user_id.avatar.url
            tags = posts[i].tag_set.all()
            posts_dict[i]["tags"] = tags
        return posts_dict


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
               :10] + ' ' + self.is_correct.__str__() + " " + self.post_id.__str__() + " " + self.user_id.__str__() + " mark" + self.mark.__str__()


def paginate(page_num, count_pages, arr):
    cur_arr = arr[page_num * count_pages:(page_num + 1) * count_pages]
    pagination = {"pages": []}
    if page_num >= 1 and len(arr[(page_num - 1) * count_pages:page_num * count_pages]) != 0:
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


BEST_MEMBERS = [
    {
        "text": f"Member{i}",
        "href": f"#"
    } for i in range(8)
]
