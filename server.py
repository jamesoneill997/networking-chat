import socket
import threading


ip_addr = "0.0.0.0"
port = 8800

#setup, 32 bit ipv4, TCP/IP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_	running = True
#give socket ip address and port
socket_details = (ip_addr, port)
serversocket.bind(socket_details)
serversocket.listen(100)

#store connected devices
connected_devices = {}

#function to create a thread
def start_client_thread(connection, address):
	th = threading.Thread(target = client_thread, args = (connection, address))
	th.start()
	connected_devices[connection]["thread"] = th


def broadcast(message, original_conn):
	for conn in connected_devices:
		if conn != original_conn:
			conn.send(message.encode())




#function to handle a client connection thread
def client_thread(conn, addr):
	welcome ="Welcome to the chatroom"
	conn.send(welcome.encode())

	#if the client sends us data, send the data to every other client
	while server_running:
		try:
			message = conn.recv(1024)
			if message:
				enc_message = message.decode()
				message_to_send = "<{}>{}".format(addr, enc_message)

				print(message_to_send)
				broadcast(message_to_send, conn)
			else:
				pass
		except:
			continue

#main loop
try:
	while server_running:
		conn, addr = serversocket.accept()
		connected_devices[conn] = {'addr':addr}
		print("{} connected".format(addr))
		start_client_thread(conn,addr)

except KeyboardInterrupt:
	print("Server shutting down")
	for conn in connected_devices:
		conn.close()
	serversocket.close()
	server_running = False
	print("Goodbye")
	sys.exit(0)