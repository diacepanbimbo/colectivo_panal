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
    lista += "],"
    
    lista_links=  """"collections": {"links":["""
    for activity_link in ActivityLink.objects.all():
        #print str(activity_link.as_json()) 
        lista_links += str(activity_link.as_json()) + ","
    
    if lista_links.endswith(","):
        lista_links = lista_links[:-1]
    lista_links += "]}}"
        
    returned_text=str(lista)+str(lista_links)

    test ="""{ "data":[{"id":"1455152499324","start_date":"2013-04-01 00:00:00","duration":"5","text":"Project #1","progress":"0.8","parent":"0","open":1},
    {"id":"1455152499328","start_date":"2013-04-01 00:00:00","duration":"6","text":"New task","progress":"0","parent":"0","open":1}],
     "collections": {"links":[{"id":"0","source":"17","target":"2","type":"0"}]}}"""
    #print returned_text
    return HttpResponse(returned_text)


@csrf_exempt
def modify_project(request):
    query_dict = request.POST #json.dumps(urlparse.parse_qs(request.META['QUERY_STRING'])
    query_string_json = json.loads(json.dumps(urlparse.parse_qs(request.META['QUERY_STRING'])))
    if query_dict.__contains__('ids'):
        ids = query_dict.get("ids")
        for id in ids.split(","):
            
            if query_string_json['gantt_mode'][0].encode('utf8') == "tasks":
                try:
                    activity = Activity.objects.get(id=id)
                except ObjectDoesNotExist:
                    activity = Activity(id=id)
                d={}
                for key, value in query_dict.iteritems():
                    if key.startswith(id):
                        d[key.replace(id+"_", "")] = value
                
                print "-"+d['!nativeeditor_status']+"-"
                if d['!nativeeditor_status'] == 'deleted':
                    deleted_activity = activity.delete()
                    print "deleted_activitydeleted_activitydeleted_activitydeleted_activity deleted_activity"
                else:    
                        
                    d2=dict(
                        id = d['id'],
                        responsible_user = get_responsible_user_from_id(1),
                        short_description = d['text'],
                        long_description = d['text'],
                        start_date = d['start_date'],
                        end_date = get_end_date_from_start_plus_duration(d['start_date'],d['duration']),
                        parent = get_parent_activity_from_id(d['parent']),
                        activity_type = get_activity_type_from_id(1))
    
                    if 'progress' in d:
                        d2['progress'] = d['progress']
                        #print "progersssss inserted"
                        
                    for key, value in d2.iteritems():
                        setattr(activity, key, value)
    
                    saving = activity.save()
                    
                returned_text="{\"data\":{\"type\":\""+d['!nativeeditor_status']+"\", \"sid\":\"" + str(id) + "\", \"tid\":\"" + str(id) + "\"}}"

            if query_string_json['gantt_mode'][0].encode('utf8') == "links":
                
                try:
                    activity_link = ActivityLink.objects.get(id=id)
                except ObjectDoesNotExist:
                    activity_link = ActivityLink(id=id)
                d={}
                for key, value in query_dict.iteritems():
                    if key.startswith(id):
                        d[key.replace(id+"_", "")] = value
                
                print "-"+d['!nativeeditor_status']+"-"
                if d['!nativeeditor_status'] == 'deleted':
                    deleted_activity_link = activity_link.delete()
                else:    
                          
                            
                    d2=dict(
                        id = d['id'],
                        source = Activity.objects.get(id=d['source']),
                        target = Activity.objects.get(id=d['target']),
                        link_type = get_activity_link_type_from_id(int(d['type'])+1)
                        )
                    
                    for key, value in d2.iteritems():
                        setattr(activity_link, key, value)
    
                    saving = activity_link.save()
                returned_text="{\"data\":{\"type\":\""+d['!nativeeditor_status']+"\", \"sid\":\"" + str(id) + "\", \"tid\":\"" + str(id) + "\"}}"


            #print returned_text
            
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

def get_activity_link_type_from_id(activity_link_type_id):
    #print "                              searching for activity_type : " + str(activity_type_id)
    activity_link_type = get_object_or_404(ActivityLinkType, pk=activity_link_type_id)
    return activity_link_type


def get_end_date_from_start_plus_duration(start, duration):
    date_array = start.split("-")
    start_date = date(int(date_array[0]),int(date_array[1]),int(date_array[2]))
    end_date = start_date + timedelta(days=int(duration))
    return end_date
