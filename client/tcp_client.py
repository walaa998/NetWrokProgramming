from socket import *
import hashlib
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = "127.0.0.1"
PORT = 7788
client_socket.connect((IP,PORT))
cnt = 1

while True :
     msg_from_server = client_socket.recv(1024).decode()
     book_number = input(msg_from_server)

     if book_number == "exit":
         break

     client_socket.send(book_number.encode())

     book_content = client_socket.recv(2048).decode()
     hash_book_content_from_server = client_socket.recv(1024).decode()

     hash_book_content = md5_words = hashlib.md5(book_content.encode('utf-8')).hexdigest()
     print("hash_book_content_from_server: " +hash_book_content_from_server)
     print("hash_book_content: " + hash_book_content)

     if(hash_book_content == hash_book_content_from_server):
         print("The connection is secure")
         client_socket.send("The connection is secure".encode())
     else:
         print("The connection is not secure")
         client_socket.send("The connection is not secure".encode())
         break

     try:
         file = open("downloads/download"+str(cnt)+".txt", "w")
         file.write(book_content)
         cnt += 1
         file.close()
     except error as e:
         print(e)


client_socket.close()