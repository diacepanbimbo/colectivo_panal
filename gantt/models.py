from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import datetime

def get_sentinel_user():
    return get_user_model().objects.get_or_create(name='deleted')[0]

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    def __str__(self):
        return self.name

def get_sentinel_activity_type():
    return get_user_model().objects.get_or_create(name='deleted')[0]

class ActivityType(models.Model):
    short_description = models.CharField(max_length=200)
    long_description = models.CharField(max_length=2000)
    def __str__(self):
        return self.short_description

class Activity(MPTTModel):
    short_description = models.CharField(max_length=200)
    long_description = models.CharField(max_length=2000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    responsible_user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    parent = TreeForeignKey('self',null = True, blank = True, related_name = 'sub_activities', db_index=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET(get_sentinel_activity_type))
    progress = models.FloatField(default=0.0)
    class MPTTMeta:
        order_insertion_by = ['short_description']

    def __str__(self):
        return str(self.start_date.date()) + " " + str(self.short_description)
    def duration(self):
        return (self.end_date -self.start_date).days

    def as_json(self):
        if self.parent == None:
            aux_parent = ""
        else:
            aux_parent = self.parent.id
        return dict(
            id = self.id,
            user = self.responsible_user.name,
            text = self.short_description,
            start_date = self.start_date.date().isoformat(),
            parent = aux_parent,
            progress = self.progress)

    def as_xml(self):
        if self.parent == None:
            aux_parent = "0"
        else:
            aux_parent = self.parent.id
        return "{\"id\":\"" + str(self.id) +\
        "\",\"start_date\":\"" + str(datetime.date.strftime(self.start_date.date(), "%Y-%m-%d"))+" 00:00:00" +\
        "\",\"duration\":\""+ str(self.duration())+\
        "\",\"text\":\"" + str(self.short_description) +\
        "\",\"progress\":\"" + str(self.progress) +\
        "\",\"parent\":\"" + str(aux_parent) +\
        "\",\"open\":1}"

        #"\", \"start_date\":\"" + str(datetime.date.strftime(self.start_date.date(), "%d/%m/%Y")) +\

class ActivityLinkType(models.Model):
    dependency = models.CharField(max_length=20)
    def __str__(self):
        return str(self.dependency)

class ActivityLink(models.Model):
    source = models.ForeignKey(Activity, related_name = 'target', on_delete=models.CASCADE)
    target = models.ForeignKey(Activity, related_name = 'source', on_delete=models.CASCADE)
    link_type = models.ForeignKey(ActivityLinkType, on_delete=models.CASCADE)
    
    def as_json(self):
        
        return "{\"id\":\""+str(self.id).encode('utf8')+"\","+\
            "\"source\":\""+str(self.source.id).encode('utf8')+"\","+\
            "\"target\":\""+str(self.target.id).encode('utf8')+"\","+\
            "\"type\":\""+str(int(self.link_type.id)-1).encode('utf8')+"\"}"
