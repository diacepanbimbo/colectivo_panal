from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
from django.http import QueryDict

from json import dumps, loads
import urlparse


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")

    #for activitiy in Activity.objects.filter(pk=3):
    #    lista = activitiy.as_xml()

    context = {}#{'lista': lista,}

    return render(request, 'gantt/index.html',context)

def project(request):
    lista = "{ \"data\":["
    for activitiy in Activity.objects.all():
        lista += activitiy.as_xml()+","
    lista = lista[:-1]
    lista += "],"+ """ "collections": {"links":[{"id":"0","source":"1","target":"2","type":"0"}]}}"""

    test ="""{ "data":[{"id":"1455152499324","start_date":"2013-04-01 00:00:00","duration":"5","text":"Project #1","progress":"0.8","parent":"0","open":1},
    {"id":"1455152499328","start_date":"2013-04-01 00:00:00","duration":"6","text":"New task","progress":"0","parent":"0","open":1}],
     "collections": {"links":[{"id":"0","source":"17","target":"2","type":"0"}]}}"""
    return HttpResponse(lista)


@csrf_exempt
def modify_project(request):
    print "------------------------------------------------>"
    query_dict = request.POST #json.dumps(urlparse.parse_qs(request.META['QUERY_STRING'])
    query_string_json = json.loads(json.dumps(urlparse.parse_qs(request.META['QUERY_STRING'])))
    print query_string_json['gantt_mode'][0].encode('utf8')
    print "tasks".encode('utf8')
    if query_dict.__contains__('ids'):
        ids = query_dict.get("ids")
        for id in ids.split(","):
            if query_string_json['gantt_mode'][0].encode('utf8') == "tasks":
                print "------------------------------------------------>"
                try:
                    activity = Activity.objects.get(id=id)
                except ObjectDoesNotExist:
                    activity = Activity(id=id)
                d={}
                for key, value in query_dict.iteritems():
                    if key.startswith(id):
                        d[key.replace(id+"_", "")] = value
                        print d[key.replace(id+"_", "")] +"=>"+ str(value)
                
                print "auxxxxxxxxxxxxxxxx"
                d2=dict(
                    id = d['id'],
                    responsible_user = get_responsible_user_from_id(1),
                    short_description = d['text'],
                    long_description = d['text'],
                    start_date = d['start_date'],
                    end_date = get_end_date_from_start_plus_duration(d['start_date'],d['duration']),
                    parent = get_parent_activity_from_id(d['parent']),
                    activity_type = get_activity_type_from_id(1))

                print d
                if 'progress' in d:
                    d2['progress'] = d['progress']
                    print "progersssss inserted"
                print d2
                for key, value in d2.iteritems():
                    print str(key) + " :: " + str(value)
                    setattr(activity, key, value)

                activity.save()

            if query_string_json['gantt_mode'] == "links":
                pass

            #!nativeeditor_status
            returned_text="{\"data\":{\"type\":\"inserted\", \"sid\":\"" + str(id) + "\", \"tid\":\"" + str(id) + "\"}}"
            print returned_text
            
    #{"type":"updated", "sid":15, "tid":15} or {"action":"error", ...}
    return HttpResponse(returned_text)

def get_responsible_user_from_id(responsible_user_id):
    #print "                              searching for user : " + str(responsible_user_id)
    responsible_user = get_object_or_404(User, pk=responsible_user_id)
    return responsible_user

def get_parent_activity_from_id(parent_activity_id):
    #print "                              searching for activity : " + str(parent_activity_id)
    try:
        parent_activity = Activity.objects.get(pk=parent_activity_id)
    except ObjectDoesNotExist:
        parent_activity = None
    return parent_activity

def get_activity_type_from_id(activity_type_id):
    #print "                              searching for activity_type : " + str(activity_type_id)
    activity_type = get_object_or_404(ActivityType, pk=activity_type_id)
    return activity_type

def get_end_date_from_start_plus_duration(start, duration):
    date_array = start.split("-")
    start_date = date(int(date_array[0]),int(date_array[1]),int(date_array[2]))
    end_date = start_date + timedelta(days=int(duration))
    return end_date
