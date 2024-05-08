import socket
import os
import json
import math

class Server:

    def __init__(self):
        self.server_address = 'socket_file'
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def accept_connections(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass
        self.server.bind(self.server_address)
        print('Server started')

    def listen(self):
        # 30秒間クライアントからの接続を待ち、接続がない場合はタイムアウトする
        self.server.settimeout(30)
        self.server.listen(1)
        while True:
            connection, client_address = self.server.accept()
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
        return math.floor(float(x))
    
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
    
class ErrorHandler:
    def handle_error():
        print('An error occurred')
    
    def log_error():
        print('Error logged')

class RequestHandler:
    rpc_methods = {
        'floor': RPCFunctions.floor,
        'nroot': RPCFunctions.nroot,
        'reverse': RPCFunctions.reverse,
        'validAnagram': RPCFunctions.validAnagram,
        'sort': RPCFunctions.sort
    }

    def parseRequest(request):
        try:
            parsed_request = json.loads(request.decode())
            print('Parsed request:', parsed_request)
            return parsed_request
        except json.JSONDecodeError:
            print('Error!! Invalid JSON format')
            return {"error": "Invalid JSON format"}
        except json.UnicodeDecodeError:
            print('Error!! Invalid Unicode')
            return {"error": "Invalid Unicode"}
        except Exception as e:
            print('Error!! An error occurred while parsing the request:', e)
            return {"error": "An error occurred while parsing the request: " + str(e)},

    def handleRequest(parsed_request):
        print('Please wait a moment. Processing your request....')

        request_method = parsed_request['method']
        request_params = parsed_request['params']
        request_param_type = parsed_request['params_type']

        response = {}

        try:
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
        except KeyError:
            response = {
            'error': 'Invalid method',
            'id': parsed_request['id']
            }
        except Exception as e:
            response = {
            'error': 'An error occurred while processing the request: ' + str(e),
            'id': parsed_request['id']
            }
            print('Error:', e)

        return response
     
    def sendResponse(connection, response):
        try:
            connection.sendall(json.dumps(response).encode())
            print('Response sent:', response)
        except Exception as e:
            print('Error occurred while sending response:', e)

def main():
    server = Server()
    server.accept_connections()
    server.listen()

main()
