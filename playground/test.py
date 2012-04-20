# Include the Dropbox SDK libraries
from dropbox import client, rest, session
from os import system
from pickle import dump, load

tokendb = {}
try:
  tokendb = load(open('token.db','r'))
except:
  pass

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'dypmsdyctp1jiv4'
APP_SECRET = 'ihiakn2tr86h48e'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

def authorize(email):
  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

  if email in tokendb:
    access_token = tokendb[email]
    sess.token = access_token
    try:
      client.DropboxClient(sess).account_info()
    except dropbox.rest.ErrorResponse:
      sess.token = None

  if sess.token == None:
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)

    # Make the user sign in and authorize this token
    print "url:", url
    system('open "'+url+'"')
    print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
    raw_input()

    # This will fail if the user didn't visit the above URL and hit 'Allow'
    try:
      access_token = sess.obtain_access_token(request_token)
    except dropbox.rest.ErrorResponse:
      # User denied request
      print "User denied request"
      return

    if email != client.DropboxClient(sess).account_info()['email']:
      # Requesting user and authorizing user don't agree
      print "Requesting user and authorizing user don't agree"
      return

    tokendb[email] = sess.token

  print 'access_token:', access_token

  myclient = client.DropboxClient(sess)
  print "dir(client):", dir(myclient)
  print "linked account:", myclient.account_info()

  f = open('test.py')
  response = myclient.put_file('/magnum-opus.py', f)
  print "uploaded:", response

  folder_metadata = myclient.metadata('/')
  print "metadata:", folder_metadata

  f, metadata = myclient.get_file_and_metadata('/magnum-opus.py',rev='1')
  print "Returned f:", f
  print dir(f)

  out = open('magnum-opus.py', 'w')
  out.write(f.read())
  print(metadata)

authorize('blickly@berkeley.edu')

dump(tokendb, open('token.db','w'))
