import socket
import os
import json
import math

class Server:
    def accept_connections(server):
        server_address = 'socket_file'
        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass
        server.bind(server_address)
        print('Server started')

    def listen(server):
        # 30秒間クライアントからの接続を待ち、接続がない場合はタイムアウトする
        server.settimeout(30)
        server.listen(1)
        while True:
            connection, client_address = server.accept()
            print('Connection from', client_address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print('Received', data.decode())
                parsed_request = RequestHandler.parseRequest(data)
                response = RequestHandler.handleRequest(parsed_request)
                RequestHandler.sendResponse(connection, response)
                connection.close()
class RPCFunctions:
    # xを最も近い整数に切り捨て、その値を返す
    def floor(x):
        return math.floor(x)
    
    # 方程式r ** n = xを満たすrを求める
    def nroot(x, n):
        x = float(x)
        n = int(n)
        return x ** (1 / n)

    # 文字列sを入力として受け取り、その文字列を逆順にして返す
    def reverse(s):
        return s[::-1]
    
    # ２つの文字列が互いにアナグラムであるかどうかを判定する
    def validAnagram(s, t):
        return sorted(s) == sorted(t)

    # 文字列の配列を入力として受け取り、ソート後の配列を返す
    def sort(s):
        return sorted(s)
    
class RequestHandler:
    rpc_methods = {
        'floor': RPCFunctions.floor,
        'nroot': RPCFunctions.nroot,
        'reverse': RPCFunctions.reverse,
        'validAnagram': RPCFunctions.validAnagram,
        'sort': RPCFunctions.sort
    }

    def parseRequest(request):
        parsed_request = json.loads(request.decode())
        print('Parsed request:', parsed_request)
        return parsed_request

    def handleRequest(parsed_request):
        print('Please wait a moment. Processing your request....')

        request_method = parsed_request['method']
        request_params = parsed_request['params']
        request_param_type = parsed_request['params_type']

        response = {}

        if request_method == 'nroot' or request_method == 'validAnagram':
            response = {
                'results': RequestHandler.rpc_methods[request_method](request_params[0], request_params[1]),
                'result_type': request_param_type,
                'id': parsed_request['id']
            }
        else:
            response = {
                'results': RequestHandler.rpc_methods[request_method](request_params),
                'result_type': request_param_type,
                'id': parsed_request['id']
            }

        return response
     
    def sendResponse(connection, response):
        connection.sendall(json.dumps(response).encode())
        print('Response sent:', response)

def main():
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.settimeout(30)
    Server.accept_connections(server)
    Server.listen(server)

main()
