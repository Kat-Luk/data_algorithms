class StudentNode:
    #one node is one student record

    def __init__(self, record, next_=None):
        self.record = record   # records content is in dictionary (keys: student_id, student_name, course_id, score)
        self.next = next_ 

class StudentList:
    # linked list of student records

    def __init__(self):
        self._head = None

    # helper function to check if the list is empty
    def is_empty(self):
        return self._head is None

    #iterate through list and yieald each record ... so dictionary
    def __iter__(self):
        p = self._head
        while p is not None:
            yield p.record
            p = p.next


    # functions required from the exercise

    def insert_sorted(self, record):
        new_node = StudentNode(record)
        new_key = record["student_id"]

        # empty list, or the new record is less then head, so insert in front
        if self._head is None or new_key < self._head.record["student_id"]:
            new_node.next = self._head
            self._head = new_node
            return
 
        # find p, the last node that ID is <= the new ID.
        # while is using p.next so we stop at the last node
        p = self._head
        while p.next is not None and p.next.record["student_id"] <= new_key:
            p = p.next
        new_node.next = p.next
        p.next = new_node

    # True if deleted, False if not found
    def delete(self, student_id, course_id):

        # helper function to check if node matches student_id AND course_id
        def matches(node):
            r = node.record
            return r["student_id"] == student_id and r["course_id"] == course_id

        if self._head is None:
            return False

        # if head is the one to be delted O(1)
        if matches(self._head):
            self._head = self._head.next
            return True

        # if node is in the middle or last O(n)
        p = self._head
        while p.next is not None:
            if matches(p.next):
                p.next = p.next.next
                return True
            p = p.next
        return False

    def filter(self, pred):
        p = self._head
        while p is not None:
            if pred(p.record):
                yield p.record
            p = p.next


student_records = StudentList()

#HELPER FUNCTIONS:
# user must send number for id, keep asking until ok
# (int("") also fails, so empty input is covered by the same message)
def read_id(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return int(text)
        except ValueError:
            print("ID must be a whole number. Try again.")

# Menu option 1: add student record
def add_student_record():
    student_id = read_id("Enter student ID: ")
    student_name = input("Enter student name: ").strip()
    course_id = read_id("Enter course ID: ")

    # check if score is number between 0-100 or keep asking until ok
    while True:
        try:
            score = float(input("Enter score: "))
        except ValueError:
            print("Score must be a number. Try again.")
            continue
        if 0 <= score <= 100:
            break
        print("Score must be between 0 and 100. Try again.")

    # No duplicates with same student id AND course id.
    for record in student_records:
        if record["student_id"] == student_id and record["course_id"] == course_id:
            print(f"A record for student {student_id} in course {course_id} already exists.")
            return

    student_records.insert_sorted({
        "student_id": student_id,
        "student_name": student_name,
        "course_id": course_id,
        "score": score,
    })
    print("Added succesfully.")

#menu option 2: display all records
def display_all_records():
    if student_records.is_empty():
        print("No student records found.")
        return
    print("All student records (ascending student ID):")
    for record in student_records:
        print(f"Student ID: {record['student_id']}, Name: {record['student_name']}, "
              f"Course ID: {record['course_id']}, Score: {record['score']}")

#menu option 3: delete record by student id and course id
def delete_record():
    student_id = read_id("Enter student ID to delete: ")
    course_id = read_id("Enter course ID to delete: ")
    if student_records.delete(student_id, course_id):
        print(f"Record for student ID {student_id} and course ID {course_id} deleted.")
    else:
        print(f"No record found for student ID {student_id} and course ID {course_id}.")


#menu option 4: display records sorted by course id and score
def display_sorted_records():
    if student_records.is_empty():
        print("No student records found.")
        return
    sorted_records = sorted(student_records, key=lambda r: (r["course_id"], -r["score"]))
    print("Student records sorted by course ID and score (descending):")
    for record in sorted_records:
        print(f"Student ID: {record['student_id']}, Name: {record['student_name']}, "
              f"Course ID: {record['course_id']}, Score: {record['score']}")

#Menu option 5: query records by student id
def query_records_by_student_id():
    student_id = read_id("Enter student ID to query: ")
    found = list(student_records.filter(lambda r: r["student_id"] == student_id))
    if not found:
        print(f"No records found for student ID {student_id}.")
        return
    print(f"Records for student ID {student_id} ({found[0]['student_name']}):")
    for record in found:
        print(f"  Course ID: {record['course_id']}, Score: {record['score']}")



#Main menu

MENU = """
===== Student Grade Management System =====
1. Add student record
2. Display all records
3. Delete a record (by student ID and course ID)
4. Display records sorted by course ID and score (descending)
5. Query records by student ID
0. Exit
"""

# run the main menu loop until the user chooses 0 (match needs Python 3.10+)
def main():
    while True:
        print(MENU)
        choice = input("Please select an option (0-5): ").strip()
        match choice:
            case "1":
                add_student_record()
            case "2":
                display_all_records()
            case "3":
                delete_record()
            case "4":
                display_sorted_records()
            case "5":
                query_records_by_student_id()
            case "0":
                print("Exiting the program.")
                break   # match is not a loop, so this exits the while loop
            case _:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()


# TEST CASES
#
# Each test starts from a fresh run of the program (empty list).
#
# TC1 - Records are stored in ascending order of student ID
#   Input:    Add 3/Cat/101/70, Add 1/Ann/101/60, Add 2/Bob/102/95, then option 2
#   Expected: Student ID: 1, Name: Ann, Course ID: 101, Score: 60.0
#             Student ID: 2, Name: Bob, Course ID: 102, Score: 95.0
#             Student ID: 3, Name: Cat, Course ID: 101, Score: 70.0
#   Checks:   insert at head (1 before 3) and insert in the middle (2 between 1 and 3)
#
# TC2 - IDs are compared as numbers, not text
#   Input:    Add 10/A/101/50, Add 9/B/101/50, then option 2
#   Expected: ID 9 is listed before ID 10
#
# TC3 - Duplicate record (same student ID and course ID) is rejected
#   Input:    Add 1/Ann/101/60, Add 1/Ann/101/90, then option 2
#   Expected: "A record for student 1 in course 101 already exists."
#             Only one record is listed, with score 60.0
#
# TC4 - Invalid score is rejected until a valid one is entered
#   Input:    Option 1, ID 1, name Ann, course 101, then scores: abc, 150, -5, 80
#   Expected: "Score must be a number. Try again."            (for abc)
#             "Score must be between 0 and 100. Try again."   (for 150 and -5)
#             "Added succesfully." with score 80.0
#
# TC5 - Invalid ID is rejected until a valid one is entered
#   Input:    Option 1, then IDs: abc, (empty), 1
#   Expected: "ID must be a whole number. Try again." twice, then the add continues
#
# TC6 - Sort by course ID, then score descending within a course
#   Input:    Add 3/Cat/101/70, Add 1/Ann/101/60, Add 2/Bob/102/95, then option 4
#   Expected: Student ID: 3, Name: Cat, Course ID: 101, Score: 70.0
#             Student ID: 1, Name: Ann, Course ID: 101, Score: 60.0
#             Student ID: 2, Name: Bob, Course ID: 102, Score: 95.0
#
# TC7 - Query all courses for one student
#   Input:    Add 1/Ann/101/60, Add 1/Ann/102/85, Add 2/Bob/101/95,
#             then option 5 with ID 1, then option 5 with ID 9
#   Expected: Records for student ID 1 (Ann):
#               Course ID: 101, Score: 60.0
#               Course ID: 102, Score: 85.0
#             "No records found for student ID 9."
#
# TC8 - Delete from the middle, the tail, the head, and a missing record
#   Input:    Add 1/A/101/50, Add 2/B/101/50, Add 3/C/101/50, then delete:
#             2/101 (middle), 3/101 (tail), 1/101 (head, last one left), 5/101 (missing)
#             with option 2 after each delete
#   Expected: after 2/101: records 1, 3
#             after 3/101: record 1
#             after 1/101: "No student records found."
#             5/101: "No record found for student ID 5 and course ID 101."
#
# TC9 - Every option works on an empty list
#   Input:    Options 2, 4, 5 (ID 1), 3 (ID 1, course 101)
#   Expected: "No student records found." for options 2 and 4
#             "No records found for student ID 1."
#             "No record found for student ID 1 and course ID 101."
#
# TC10 - Invalid menu option
#   Input:    7, then abc, then 0
#   Expected: "Invalid option. Please try again." twice, then "Exiting the program."