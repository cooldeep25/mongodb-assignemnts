
use school
db.scores.drop();
var types = ['exam', 'homework', 'quiz']
for (student_id = 0; student_id < 100; student_id++) {
    for (type=0; type < 3; type++) {
	var r = {'student_id':student_id, 'type':types[type], 'score':Math.random() * 100};
	db.scores.insert(r);
    }
}



//for(i=0; i < 1000; i++){ names = ["exam","essay", "quiz"]; for( j=0; j<3; j++) {db.scores.insert({"student":i, "type":names[j], score: Math.round(Math.random()* 100)});} };

