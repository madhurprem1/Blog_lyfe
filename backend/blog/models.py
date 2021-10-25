from django.db import models
from datetime import datetime
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify, title


class Categories(models.TextChoices):
    WORLD = 'world'
    ENVOIRMENT = 'envoirment'
    TECHNOLOGY = 'technology'
    DESIGN = 'design'
    CULTURE = 'culture'
    BUSINESS = 'business'
    POLITCS = 'politics'
    OPINION = 'opinion'
    SCIENCE = 'science'
    HEALTH = 'health'
    STYLE = 'style'
    TRAVEL = 'travel'


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.CharField(max_length=50, choices=Categories.choices, default='World')
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d')
    excerpt = models.CharField(max_length=150)
    month = models.CharField(max_length=5)
    day = models.CharField(max_length=2)
    content = models.TextField()
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(datetime.now, blank=True)

    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = BlogPost.objects.all().filter(slug__iexact=original_slug).count()
        
        count = 1
        slug = original_slug

        while(queryset):
            slug = original_slug + '-' + str(count)
            count+=1
            queryset = BlogPost.objects.all().filter(slug__iexact=slug).count()
        
        self.slug = slug

        if  self.featured:
            try:
                temp = BlogPost.objects.get(featured=True)
            except BlogPost.DoesNotExist:
                print("Blog post does not exsist !")
                pass

        super(BlogPost, self).save(*args, **kwargs)

        def __str__(self):
            return self.title