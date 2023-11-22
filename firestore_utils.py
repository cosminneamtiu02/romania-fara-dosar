from google.cloud import storage, firestore


def commit_image_to_firestore(image_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket("hacathon-405514.appspot.com")
    blob = bucket.blob(image_path)

    blob.upload_from_filename(image_path)

    # Get the uploaded image URL
    image_url = blob.public_url

    return image_url


def commit_person_to_firestore(person_data, id_face, id_photo):
    person_data['face_url'] = commit_image_to_firestore(id_face)
    person_data['id_url'] = commit_image_to_firestore(id_photo)
    person_data['first_login'] = "True"
    person_data['password'] = person_data['cnp']
    db = firestore.Client()

    # Reference to a collection
    collection_ref = db.collection('users')

    # Create a document with specific ID
    doc_ref = collection_ref.document(person_data['cnp'])

    doc_ref.set(person_data)
