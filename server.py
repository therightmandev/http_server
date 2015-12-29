import socket, datetime


def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def listen_sock(s, host, port):
    s.bind((host, port))
    s.listen(1)
    print("Server listening on port", port)

def accept_conn(s):
    conn, addr = s.accept()
    print ("Connected to", addr)
    return conn, addr

def receive(conn_sock):
    rcvd = conn_sock.recv(1024).decode()
    if rcvd:
        return rcvd

def parse_req(req):
    try:
        drctry = req.split("\n")[0].split(" ")[1].replace(r'/', '\\').strip("\\")
        file_to_send = open(drctry)
        text = file_to_send.read()
        file_to_send.close()
        return text
    except FileNotFoundError as f:
        print(f)

headers = "HTTP/1.1 200 OK\n\r\
        Cache-Control: max-age=1800, pre-check=1800\n\r\
        Content-Type: text/html; charset=utf-8\n\r\
        Content-Length: bla\n\r\
        Transfer-Encoding: (not)chunked ahah, this is copied...\n\r\
        Date: Tue, 29 Dec 2015 00:41:00 GMT(yes, I copied the date)\n\r\
        Age: 1562\n\r\
        Connection: close\n\r\
        X-Cache: HIT\n\r\
        Vary: Accept-Encoding, User-Agent\n\r"

def make_headers(cont_len="bla"):
    hdrs = {
    "HTTP/1.1": "200 OK",
    "Cache-Control": "max-age=1800, pre-check=1800",
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": str(cont_len),
    "Transfer-Encoding": "(not)chunked ahah, this is copied...",
    "Date": str(datetime.datetime.now()),
    "Age": "1562",
    "Connection": "close",
    "X-Cache": "HIT",
    "Vary": "Accept-Encoding, User-Agent"
    }

    hdrs_str = "HTTP/1.1 "+ hdrs["HTTP/1.1"] + "\n\r\
            Cache-Control: " + hdrs["Cache-Control"] + "\n\r\
            Content-Type: " + hdrs["Content-Type"] + "\n\r\
            Content-Length: " + hdrs["Content-Length"] + "\n\r\
            Transfer-Encoding: " + hdrs["Transfer-Encoding"] + "\n\r\
            Date: " + hdrs["Date"] + "\n\r\
            Age: " + hdrs["Age"] + "\n\r\
            Connection: " + hdrs["Connection"] + "\n\r\
            X-Cache: " + hdrs["X-Cache"] + "\n\r\
            Vary: " + hdrs["Vary"] + "\n\r"
    return hdrs_str

def send_file(res, conn, hdrs=headers):
    if res:
        data = res.encode()
        hdrs = make_headers(cont_len=len(data)).encode()
        data = hdrs + data
        conn.sendall(data)
        return 1
    else:
        return 0

def close_conn(conn):
    conn.close()



def main():
    HOST = ''
    PORT = 3001

    sock = create_socket()
    listen_sock(sock, HOST, PORT)

    while 1:
        try:
            conn_socket, address = accept_conn(sock)
            request = receive(conn_socket)
            response = parse_req(request)
            send_file(response, conn_socket)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
