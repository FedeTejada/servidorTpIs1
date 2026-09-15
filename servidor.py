from wsgiref.simple_server import make_server
import json 

task = {}
next_id = 0



def app(environ, start_response):
    global next_id

    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    header = [("Content-Type", "application/json")]
    path_parts = path.strip("/").split("/")

    #GET /tasks
    if method == "GET" and len(path_parts) == 1 and path_parts[0] == "tasks":
        status = '200 OK'
        start_response(status,header)
        return[json.dumps(task).encode("utf-8")]
    #GET /task/{id}
    if method == "GET" and len(path_parts) == 2 and path_parts[0] == "tasks":
        id = int(path_parts[1])
        if id in task:
            status = "200 OK"
            data = task.get(id)
            start_response(status,header)
            return [json.dumps(data).encode("utf-8")]
        else:
            status = "404 Not Found"
            start_response(status,header)
            return[b'{"error": "No encontrado"}']
        #POST
    elif method == "POST" and len(path_parts) == 1 and path_parts[0] == "tasks":
        content_length = int(environ.get("CONTENT_LENGTH", 0))

        body = environ["wsgi.input"].read(content_length)

        data = json.loads(body.decode("utf-8"))
        data["id"] = next_id
        task[next_id] = data
        next_id += 1
        print(data)
        status = "201 Created"
        start_response(status, header)
        return [json.dumps(data).encode("utf-8")]
    #PATCH
    elif method == "PATCH" and len(path_parts) == 2 and path_parts[0] == "tasks":
        id = int(path_parts[1])
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        
        body = environ["wsgi.input"].read(content_length)
        
        data = json.loads(body.decode("utf-8"))
        
        if id in task:
            task[id].update(data)
            status = "200 OK"
            start_response(status, header)
            return [json.dumps(task[id]).encode("utf-8")]
        else:
            status = "404 Not Found"
            start_response(status, header)
            return [b'{"error": "No encontrado"}']    

    #DELETED
    elif method == "DELETE" and len(path_parts) == 2 and path_parts[0] == "tasks":
        status = "200 OK"
        id = int(path_parts[1])
        if id in task:
            task.pop(id)
            start_response(status,header)
            return[B'{"mensaje": "Eliminado"}']
        else:
            status = "404 Not Found"
            start_response(status,header)
            return[b'{"error": "No encontrador"}']
    else:
        status = "404 Not Found"
        start_response(status, header)
        return [b'{"error": "No encontrado"}']

with make_server("",9292,app) as server:
    print("Listening on http://localhost:9292")
    server.serve_forever()
