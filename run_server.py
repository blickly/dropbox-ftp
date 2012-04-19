import ftpserver

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = ftpserver.DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('user', password="12345", homedir='.', perm='elradfmw')

    # Instantiate FTP handler class
    handler = ftpserver.FTPHandler
    handler.authorizer = authorizer

    # Instantiate FTP server class and listen to 0.0.0.0:21
    address = ('', 2121)
    server = ftpserver.FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()

