import socket, threading



#Server Setup
host = socket.gethostname()
port = 4005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)
ip = socket.gethostbyname(host)

clients = {}
addresses = {}

print(host)
print(ip)
print("Server is ready...")
serverRunning = True

def handle_client(conn):

    try:
        username = conn.recv(1024).decode('utf8')
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % username
        conn.send(bytes(welcome, "utf8"))
        print('|-[name set to : %s]' % username)
        msg = "%s has joined the chat" % username
        broadcast(bytes(msg, "utf8"))
        clients[conn] = username
        while True:
            found = False
            response = 'Number of People Online\n'
            msg1 = conn.recv(1024)

            if msg1 != bytes("{quit}", "utf8"):
                broadcast(msg1, username+": ")
            elif msg1 == 'Error':
                print('Error: client.pyw function echo_Data, line 45 - 51')
            else:
                conn.send(bytes("{quit}", "utf8"))
                conn.close()
                del clients[conn]
                broadcast(bytes("%s has left the chat." % username, "utf8"))
                break
    except:
        print("%s has left the chat(Broken Program)." % username)

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


while True:
    conn,addr = s.accept()
    conn.send("Enter username: ".encode("utf8"))
    print("|-[ %s:%s has connected.]" % addr)
    addresses[conn] = addr
    threading.Thread(target = handle_client, args = (conn,)).start()
