import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime



# Use the application default credentials
# cred = credentials.ApplicationDefault()
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'projectId': 'superchat-fced2',
})

# Use the application default credentials
# cred = credentials.ApplicationDefault()


# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred, {
#         'projectId': 'superchat-fced2',
#         'privateKey': 'AIzaSyALgLboaRpdiz584kKvzJ0qJNd-6SahHA4',
#         'databaseURL': 'https://superchat-fced2.firebaseio.com'
#     })

# firebase_admin.initializeApp({
#   credential: admin.credential.cert({
#     projectId: "<PROJECT_ID>",
#     clientEmail: "foo@<PROJECT_ID>.iam.gserviceaccount.com",
#     privateKey: "-----BEGIN PRIVATE KEY-----<KEY>-----END PRIVATE KEY-----\n"
#   }),
#   databaseURL: "https://<DATABASE_NAME>.firebaseio.com"
# });

db = firestore.client()

# def firebase_test():
#     doc_ref = db.collection(u'django-test').document(u'alovelace')
#     doc_ref.set({
#         u'first': u'Ada',
#         u'last': u'Lovelace',
#         u'born': 1815
#     })

def send_notification(recipient, content, link):
    """send firebase notification"""
    # doc_ref = db.collection(u'django-test').document(u'alovelace')
    # doc_ref = db.collection(u"notifications-{}".format(recipient)).document(u'alovelace2')
    collection = db.collection(u"notifications-{}".format(recipient))
    collection.add({
        u'content': content,
        u'createdAt': datetime.datetime.now(),
        u'link': link
    })