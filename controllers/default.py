# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon.tools import Service
service = Service()
import gluon.contrib.simplejson as json

def index():
    return dict()

def alerts():
    form = SQLFORM.grid(db.plates.plate.contains(db.alerts.plate),
        fields=[db.plates.site_id,
        db.plates.camera_id,
        db.plates.plate,
        db.plates.epoch_time,
        db.plates.plate_img_uuid],
        csv=False,
        details=False,
        headers={'plates.site_id':'Sitio',
        'plates.camera_id':'Camara',
        'plates.plate':'Patente',
        'plates.epoch_time':'Fecha',
        'plates.plate_img_uuid':'Foto'})
    if not 'keywords' in request.vars:
        form[0][1][1] = ''
        form[2] = ''
    else:
        form[0][1][1] = ''
    return dict(form=form)

def search():
    form = SQLFORM.smartgrid(db.arrest, fields=[db.arrest.plate,
        db.arrest.arrest_reason,
        db.arrest.driver_information],
        csv=False,
        details=False,
        headers={'arrest.plate':'Patente',
        'arrest.arrest_reason':'Delito',
        'arrest.driver_information':'Informacion'},
        maxtextlength=50)
    form[0] = ''
    if not 'keywords' in request.vars:
        form[0] = ''
        form[1][1][1] = ''
        form[2] = ''
    else:
        form[1][1][1] = ''
    return dict(form=form)


def maps():
    return dict()

@service.json
def message():
    from gluon.contrib.websocket_messaging import websocket_send
    msg = request.body.read()
    data = json.loads(msg)
    insert = db.plates.insert(plate = data['results'][0]['plate'],
        confidence = data['results'][0]['confidence'],
        total_processing_time = data['processing_time_ms'],
        plate_processing_time = data['results'][0]['processing_time_ms'],
        epoch_time = data['epoch_time'],
        camera_id = data['camera_id'],
        site_id = data['site_id'],
        img_width = data['img_width'],
        img_height = data['img_height'],
        plate_img_uuid = data['uuid'])
    websocket_send('http://127.0.0.1:8888', msg, 'mykey', 'live_stream')
    pass

@service.json
def get_plates():
    from gluon.contrib.websocket_messaging import websocket_send
    data = request.body.read()
    query = db(db.arrest.arrest==True).select()
    return dict(arrest=query)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


