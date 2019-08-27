from app import mongo


#------------Function for doc serializer-------------

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


