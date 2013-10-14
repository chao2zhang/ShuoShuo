import requests
import web
import mocks
import json
mock = True

def get(url, **kwargs):
    if mock:
        return mocks.get(url, **kwargs)
    else:
        r = requests.get(url, **kwargs);
        return r.status_code, web.storify(r.json())

def options(url, **kwargs):
    if mock:
        return mocks.options(url, **kwargs)
    else:
        r = requests.options(url, **kwargs);
        return r.status_code, web.storify(r.json())

def head(url, **kwargs):
    if mock:
        return mocks.head(url, **kwargs)
    else:
        r = requests.head(url, **kwargs);
        return r.status_code, web.storify(r.json())

def post(url, data={}, **kwargs):
    if mock:
        return mocks.post(url, data=json.dumps(data), **kwargs)
    else:
        r = requests.post(url, data=json.dumps(data), **kwargs);
        return r.status_code, web.storify(r.json())

def put(url, data={}, **kwargs):
    if mock:
        return mocks.put(url, data=json.dumps(data), **kwargs)
    else:
        r = requests.put(url, data=json.dumps(data), **kwargs);
        return r.status_code, web.storify(r.json())

def patch(url, data={}, **kwargs):
    if mock:
        return mocks.patch(url, data=json.dumps(data), **kwargs)
    else:
        r = requests.patch(url, data=json.dumps(data), **kwargs);
        return r.status_code, web.storify(r.json())

def delete(url, **kwargs):
    if mock:
        return mocks.delete(url, **kwargs)
    else:
        r = requests.delete(url, **kwargs);
        return r.status_code, web.storify(r.json())