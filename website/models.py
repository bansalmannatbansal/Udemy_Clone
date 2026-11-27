from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField()
    reviews = models.IntegerField()
    price = models.IntegerField()
    original_price = models.IntegerField()
    hours = models.IntegerField()
    lectures = models.IntegerField()
    level = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    description = models.TextField()
    learn = models.TextField(help_text="One point per line")

    def learn_points(self):
        return self.learn.splitlines()

    def __str__(self):
        return self.title
