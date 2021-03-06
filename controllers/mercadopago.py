# -*- coding: utf-8 -*-

import mercadopago
import json
import os, sys

def index():
    descripcion= request.args[0]
    total=request.args[1]
    id_cxa=request.args[2]
    preference = {
        "items": [
            {
                "title": descripcion,
                "currency_id": "ARS",
                "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
                "quantity": 10,
                "unit_price": 1 #total
            }
        ],
        "back_urls": {
            "success": "https://nazoz.pythonanywhere.com/SEF/default/index",
            "failure": "https://nazoz.pythonanywhere.com/SEF/default/index",
            "pending": "https://nazoz.pythonanywhere.com/SEF/default/index"
        },
        "auto_return": "approved",
        "notification_url": "https://nazoz.pythonanywhere.com/SEF/mercadopago/notificacion",
        "external_reference": id_cxa,
    }
    mp = mercadopago.MP(myconf.take('mercadopago.client_id'), myconf.take('mercadopago.client_secret'))

    preferenceResult = mp.create_preference(preference)

    try:
        url = preferenceResult["response"]["init_point"]
        redirect(url)
    except:
        raise
        response.view = "generic.html"
        return {"pref": preferenceResult}


def notificacion():
    mp = mercadopago.MP("5736858946061665", "kpNLy0Ikt7mpMscl0REBJecuKfN6H35i")

    info = request.vars['id']

    paymentInfo = mp.get_payment_info(info)
    mp_id=int(paymentInfo["response"]["id"])
    cxa_id=int(paymentInfo["response"]["external_reference"])

    if paymentInfo["status"] == 200:
        f= db(mp_id==db.notificaciones.id_mp).select()
        if not f:
            k="None"
            if k=="None":
                noti=db.notificaciones.insert(
                            id_mp=int(paymentInfo["response"]["id"]),
                            id_cxa=int(paymentInfo["response"]["external_reference"]),
                            estado_mp=str(paymentInfo["response"]["status"])
                          )
        else:
            g=9

        q= mp_id==db.notificaciones.id_mp
        #db(q).update(estado_mp="approved") # simular que el pago fue realizado

        consulta= db((mp_id==db.notificaciones.id_mp) & (cxa_id==db.cxa.id)).select(db.notificaciones.estado_mp)
        reg=consulta[0].estado_mp
        if reg=="approved":
            db(cxa_id==db.cxa.id).update(estado="Pago")
        resul= db((mp_id==db.notificaciones.id_mp) & (cxa_id==db.cxa.id)).select()
        response.view = "generic.html"
        return {"pref": resul}
    else:
        return None
    return dict()

def prueba():
    mp_id=5046169359
    f= db(db.notificaciones).select()
    resul= db(mp_id==db.notificaciones.id_mp).select()
    if not resul:
        k="None"
        response.view = "generic.html"
        return {"pref": k}
    else:
        g='hola?'
    
    #cxa_id=5
    #consulta= db((mp_id==db.notificaciones.id_mp) & (cxa_id==db.cxa.id)).select(db.notificaciones.estado_mp)
    #la=consulta[0].estado_mp
    #if la=="approved":
        #q=cxa_id==db.cxa.id
        #db(q).update(estado="Pago")
        #a=1
        #response.view = "generic.html"
        #return {"pref": a}
    response.view = "generic.html"
    return {"pref": g}


def buscar():
    # Create an instance with your MercadoPago credentials (CLIENT_ID and CLIENT_SECRET): 
    # Argentina: https://www.mercadopago.com/mla/herramientas/aplicaciones 
    # Brasil: https://www.mercadopago.com/mlb/ferramentas/aplicacoes
    mp = mercadopago.MP("5736858946061665", "kpNLy0Ikt7mpMscl0REBJecuKfN6H35i")
    
    filters = {
        "id": "5046169359"
    }

    # Search payment data according to filters
    searchResult = mp.search_payment(filters)
    
    resul=searchResult["response"]#["results"][0]["status"]
    # Show payment information
    response.view = "generic.html"

    return {"pref": resul}
