import json
import datetime
from pprint import pprint


def debug_print(env):
    pprint(env.keys())
    for key in env.keys():
        pprint(pprint("=== KEY: {} == VALUE: {} ===".format(key, env[key])))


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    answer = json.dumps({"time": datetime.datetime.now().isoformat(),
                         "url": '{}:{}{}'.format(env['SERVER_NAME'], env['SERVER_PORT'], env['PATH_INFO'])})
    # debug_print(env)      # Нужно было, чтобы посмотреть на методы
    return [answer.encode('utf-8')]
