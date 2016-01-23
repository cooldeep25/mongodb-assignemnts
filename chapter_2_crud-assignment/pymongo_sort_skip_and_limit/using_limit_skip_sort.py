
import pymongo
import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the school database
db=connection.school
scores = db.scores


def find():

    print ("find, reporting for duty")

    query = {}

    try:

        cursor = scores.find(query).skip(4)
        cursor = cursor.limit(2)

        #cursor = cursor.sort('student_id', pymongo.ASCENDING).skip(4).limit(1)
        
        cursor = cursor.sort([('student_id',pymongo.ASCENDING),
                              ('score',pymongo.DESCENDING)])



    except Exception as e:
        print ("Unexpected error:", type(e), e)

    for doc in cursor:
        print (doc)
        


def find_one():

    print ("find one, reporting for duty")
    query = {'student_id':10}
    
    try:
        doc = scores.find_one(query)
        
    except Exception as e:
        print ("Unexpected error:", type(e), e)

    
    print (doc)


find()

