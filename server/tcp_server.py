from socket import *
import socket
import threading
import hashlib

IP = "127.0.0.1"
PORT = 7788
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP,PORT))
server_socket.listen(5)
print("Server Running....")

list_of_book = {"1" : "file1.txt", "2" : "file2.txt", "3" : "file3.txt"}

def myThread(client_socket,client_address):
    while True:
        msg_to_client = "Hello! Please select the book you want to download: \n"
        msg_to_client += "(1) file1.txt\n"
        msg_to_client += "(2) file2.txt\n"
        msg_to_client += "(3) file3.txt\n"
        msg_to_client += "or \"exit\" to exit\n"
        #print(msg_to_client)
        client_socket.send(msg_to_client.encode())
        book_number = client_socket.recv(1024).decode()
        #print(book_number)
        words = ""
        if book_number == "exit":
            break
        try:
            file = open("books/" + list_of_book[book_number], "r")

            for row in file:
                words_of_row = row.split()
                for word in words_of_row:
                    words += word + " "
                words += "\n"
            #print(list_of_book[book_number])
            print(words)
            md5_words = hashlib.md5(words.encode('utf-8')).hexdigest()

            client_socket.send(words.encode())
            client_socket.send(md5_words.encode())

            is_secure = client_socket.recv(1024).decode()
            print(is_secure)
        except socket.error as e:
            print(e)
            client_socket.send(str(e).encode())
        except KeyError as e:
            client_socket.send("This file is not exist.".encode())


(client_socket ,client_address) = server_socket.accept()
th = threading.Thread(target=myThread,args=(client_socket,client_address))
th.start()

