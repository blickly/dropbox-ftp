# Include the Dropbox SDK libraries
from dropbox import client, rest, session

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'dypmsdyctp1jiv4'
APP_SECRET = 'ihiakn2tr86h48e'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

url = sess.build_authorize_url(request_token)

# Make the user sign in and authorize this token
print "url:", url
import os
os.system('open "'+url+'"')
print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
raw_input()

# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)
print 'access_token:', access_token


client = client.DropboxClient(sess)
print "dir(client):", dir(client)
print "linked account:", client.account_info()

f = open('test.py')
response = client.put_file('/magnum-opus.py', f)
print "uploaded:", response

folder_metadata = client.metadata('/')
print "metadata:", folder_metadata

f, metadata = client.get_file_and_metadata('/magnum-opus.py',rev='1')
print "Returned f:", f
print dir(f)

out = open('magnum-opus.py', 'w')
out.write(f.read())
print(metadata)

