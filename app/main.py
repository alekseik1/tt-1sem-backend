def wsgi_application(environ, start_response):
    status = "200 OK"
    headers = [
        ('Content-Type', 'text/plain')
    ]
    body = 'Hello, world meme!'.encode('utf-8')
    print(environ['wsgi.version'])
    start_response(status, headers)
    return [body]
