import ftpserver
import tornado_server
import threading
import sys

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = ftpserver.DropboxAuthorizer()

    # Instantiate FTP handler class
    handler = ftpserver.FTPHandler
    handler.authorizer = authorizer

    # Instantiate FTP server class and listen to 0.0.0.0:21
    address = ('', 2121)
    server = ftpserver.FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start http server
    tornado_thread = threading.Thread(target=tornado_server.tornado_main, args=(authorizer,))
    tornado_thread.start()

    # start ftp server
    server.serve_forever()

    sys.exit()

if __name__ == '__main__':
    main()

