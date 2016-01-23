
import pymongo
import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the school database
db=connection.school
scores = db.scores


def find():

    print ("find, reporting for duty")

    query = {'type':'exam', 'score':{'$gt':50, '$lt':70}}

    try:
        cursor = scores.find(query)
		

    except Exception as e:
        print ("Unexpected error:", type(e), e)

    sanity = 0
    for doc in cursor:
        print (doc)
        sanity += 1
        if (sanity > 10):
            break
    return sanity    

def research():
	print("IN Research Mode")
	query1 = {'type':'quiz', 'student_id':{'$gte':10,'$lt': 15},'score':{'$lt': 29}}
	projection1 = {'student_id':1,'type':1,'score':1,'_id':0}
	try:
		cur = scores.find(query1,projection1)
	except Exception as e:
		print("Exception in Research:", type(e),e)
	for doc in cur:
		print(doc)
		
find()
print("\n\n first find completed" )

i = find()
print("\n\n Count of Students:" , i)

print("\n\n Invoking Research Mode")
research()