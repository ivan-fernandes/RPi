from bottle import route, run

@route('/')
def hello():
    return {"data": {"message": ["Hello World", "Ivan", "Teste"], "date": None}, "status": 200}

run(host='192.168.8.39', port=80, debug=True, reloader=True)


if __name__ == "__main__":
    run(host='192.168.8.39', port=80, debug=True, reloader=True)
