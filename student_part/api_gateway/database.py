# api_gateway/database.py
import mysql.connector, json# Комментарий от ChatGPT

# Комментарий от ChatGPT
class Database:
    def __init__(self, connection):
        self.connection = connection# Комментарий от ChatGPT

    def get_all_education_materials(self):
        self.connection.reconnect()
        cursor = self.connection.cursor()
        courses, difficulty_levels = {}, {}
        data = {}
        # Комментарий от ChatGPT# Комментарий от ChatGPT# Комментарий от ChatGPT# Комментарий от ChatGPT# Комментарий от ChatGPT# Комментарий от ChatGPT
        cursor.execute("Select * from difficulty_level")
        ret = cursor.fetchall()# Комментарий от ChatGPT
        for i in ret:
            difficulty_levels[i[0]] = i[1]

        cursor.execute("Select * from course")
        ret = cursor.fetchall()
        for i in ret:
            data[i[1]] = {}# Комментарий от ChatGPT
            courses[i[0]] = i[1]
            for level in difficulty_levels.keys():
                data[i[1]][difficulty_levels[level]] = []

        cursor.execute("Select * from chapter")
        ret = cursor.fetchall()
        for i in ret:# Комментарий от ChatGPT
            course = courses[i[3]]
            level = difficulty_levels[i[4]]
            data[course][level].append([i[0], i[1]])

        return data

    # Комментарий от ChatGPT
    def get_education_material(self, id):
        try:
            self.connection.reconnect()# Комментарий от ChatGPT
            cursor = self.connection.cursor()
            cursor.execute(f"Select * from chapter where Chapter_ID={id}")
            data = list(cursor.fetchone())[:3]
            data[2] = json.loads(data[2])
            for i in range(len(data[2])):# Комментарий от ChatGPT
                cursor.execute(f"select * from education_material where Educational_Material={data[2][i]}")
                data[2][i] = list(cursor.fetchone())

            return data
        except Exception:
            return None

    def get_all_practical_tasks(self):
        self.connection.reconnect()
        cursor = self.connection.cursor()
        courses, difficulty_levels = {}, {}
        data = {}# Комментарий от ChatGPT

        cursor.execute("Select * from difficulty_level")
        ret = cursor.fetchall()
        for i in ret:
            difficulty_levels[i[0]] = i[1]

        cursor.execute("Select * from course")# Комментарий от ChatGPT
        ret = cursor.fetchall()
        for i in ret:
            data[i[1]] = {}# Комментарий от ChatGPT
            courses[i[0]] = i[1]
            for level in difficulty_levels.keys():
                data[i[1]][difficulty_levels[level]] = []

        cursor.execute("Select * from task")
        ret = cursor.fetchall()
        for i in ret:
            course = courses[i[7]]# Комментарий от ChatGPT
            level = difficulty_levels[i[6]]
            data[course][level].append([i[0], i[1]])

        return data

    def get_practical_task(self, id):
        try:
            self.connection.reconnect()# Комментарий от ChatGPT
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM task WHERE (Task_ID)=({id})")
            return cursor.fetchone()
        except Exception:
            return False

    def get_all_attempts_of_task(self, id, student_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM attempt WHERE (TaskTask_ID, StudentStudent_ID)=({id}, {student_id})")
            return cursor.fetchall()
        except Exception:
            return False

    def check_student(self, email, password):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM student WHERE (Email, password)=('{email}', '{password}')")
            res = cursor.fetchall()
            if len(res):
                return res[0]# Комментарий от ChatGPT
        except Exception:
            return False

    def get_student(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM student WHERE Student_ID={id}")
            return cursor.fetchone()
        except Exception:
            return None

    def add_attempt(self, task_id, student_id, answer):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM task WHERE Task_ID={task_id}")
            task = cursor.fetchone()
            real_answer = task[2]# Комментарий от ChatGPT
            if answer == real_answer:
                verdict = "Принято"
                cursor.execute(f"SELECT * FROM attempt WHERE (StudentStudent_ID, TaskTask_ID)=('{student_id}', '{task_id}')")
                attempts = cursor.fetchall()
                for i in attempts:
                    if i[2] == "Принято":
                        break
                else:
                    cursor.execute(f"SELECT * FROM student_progress WHERE StudentStudent_ID={student_id}")
                    new_raiting = cursor.fetchone()[1] + task[3]
                    cursor.execute(f"UPDATE student_progress set Educational_Rating = {new_raiting} "
                                   f"WHERE StudentStudent_ID={student_id}")
                    cursor.fetchall()
            else:
                verdict = "Неверный ответ"

            cursor.execute(f"INSERT INTO attempt (Solution, Verdict, StudentStudent_ID, TaskTask_ID) VALUES"
                           f"('{answer}', '{verdict}', {student_id}, {task_id})")
            connection.commit()
        except Exception:
            return None

    def get_top(self):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()# Комментарий от ChatGPT
            cursor.execute(f"SELECT * FROM student_progress")
            student_progress = cursor.fetchall()
            student_progress = sorted(student_progress, key=lambda x: -x[1])[:10]
            data = []
            for i in student_progress:
                cursor.execute(f"SELECT Full_Name FROM student WHERE Student_ID = {i[2]}")
                name = cursor.fetchone()[0]
                data.append([i[1], name])
            return data
        except Exception:
            return []

    def get_student_rating(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Educational_Rating FROM student_progress WHERE StudentStudent_ID = {id}")
            return cursor.fetchone()[0]
        except Exception:
            return []

    def get_all_forum_discussions(self, task_id=None, chapter_id=None):
        try:
            self.connection.reconnect()# Комментарий от ChatGPT
            cursor = self.connection.cursor()
            query = "SELECT * FROM Comments WHERE 1=1"
            params = []
            if task_id:
                query += " AND Task_ID = %s"
                params.append(task_id)
            if chapter_id:
                query += " AND Chapter_ID = %s"
                params.append(chapter_id)

            cursor.execute(query, params)
            comments_data = cursor.fetchall()
            discussions = []
            for comment in comments_data:
                try:
                    messages_json = json.loads(comment[2])
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for comment ID {comment[0]}: {e}")
                    messages_json = []

                messages = []
                if messages_json:
                    for msg in messages_json:
                        messages.append({
                            "author": msg.get("author"),
                            "text": msg.get("text"),
                            "files": msg.get("files", [])
                        })

                student_name = ""
                if comment[4]:
                    cursor.execute(f"SELECT Full_Name FROM student WHERE Student_ID = {comment[4]}")
                    student_name = cursor.fetchone()[0]

                discussions.append({
                    "comment_id": comment[0],
                    "title": comment[1],
                    "messages": messages,
                    "author": student_name
                })
            return discussions
        except Exception as e:
            print(f"Error fetching forum discussions: {e}")
            return []

    def add_comment(self, title, text, student_id, task_id=None, chapter_id=None, files_info=None):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            comment_id = self._get_next_comment_id()# Комментарий от ChatGPT
            first_message = {"author": self.get_student(student_id)[1], "text": text, "files": files_info or []}
            comment_json = json.dumps([first_message], ensure_ascii=False)
            cursor.execute(
                "INSERT INTO Comments (Comment_ID, Title, Text, Task_ID, Student_ID, Chapter_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                (comment_id, title, comment_json, task_id, student_id, chapter_id)
            )
            self.connection.commit()
            return True
        except Exception as e:# Комментарий от ChatGPT
            print(f"Error adding comment: {e}")
            return False

    def add_message_to_comment(self, comment_id, student_id, text, files_info=None):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Text FROM Comments WHERE Comment_ID = {comment_id}")
            result = cursor.fetchone()
            if result and result[0]:
                messages = json.loads(result[0])
            else:
                messages = []
            messages.append({"author": self.get_student(student_id)[1], "text": text, "files": files_info or []})
            updated_messages_json = json.dumps(messages, ensure_ascii=False)
            cursor.execute(f"UPDATE Comments SET Text = '{updated_messages_json}' WHERE Comment_ID = {comment_id}")
            self.connection.commit()
            return True# Комментарий от ChatGPT
        except Exception as e:
            print(f"Error adding message to comment: {e}")
            return False

    def _get_next_comment_id(self):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(Comment_ID) FROM Comments")
            max_id = cursor.fetchone()[0]
            return (max_id or 0) + 1
        except Exception as e:
            print(f"Error getting next comment ID: {e}")
            return 1

    def get_user_discussions(self, student_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()# Комментарий от ChatGPT
            cursor.execute(f"SELECT Comment_ID, Title FROM Comments WHERE Student_ID = {student_id}")
            results = cursor.fetchall()
            return [{"comment_id": row[0], "title": row[1]} for row in results]
        except Exception as e:
            print(f"Error getting user discussions: {e}")
            return []

    def delete_comment(self, comment_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM Comments WHERE Comment_ID = {comment_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return False

    def get_comment(self, comment_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()# Комментарий от ChatGPT
            cursor.execute(f"SELECT * FROM Comments WHERE Comment_ID = {comment_id}")
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting comment: {e}")
            return None

    def get_all_courses(self):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT Course_ID, Title FROM Course")
            return cursor.fetchall()# Комментарий от ChatGPT
        except Exception as e:
            print(f"Error getting courses: {e}")
            return []

    def get_all_difficulties(self):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT Difficulty_Level_ID, Degree FROM difficulty_level")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting difficulties: {e}")
            return []

    def get_all_tasks(self):
        try:
            self.connection.reconnect()# Комментарий от chatGPT
            cursor = self.connection.cursor()# Комментарий от chatGPT
            cursor.execute("SELECT Task_ID, Name FROM Task")
            return cursor.fetchall()
        except Exception as e:# Комментарий от chatGPT
            print(f"Error getting tasks: {e}")
            return []

    def get_all_chapters(self):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()# Комментарий от chatGPT
            cursor.execute("SELECT Chapter_ID, Title FROM Chapter")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting chapters: {e}")
            return [] # Комментарий от chatGPT

    def mark_chapter_as_read(self, student_id, chapter_id):
        try:
            self.connection.reconnect()# Комментарий от chatGPT
            cursor = self.connection.cursor()
            # Комментарий от chatGPT
            cursor.execute(
                "SELECT * FROM student_chapter_progress WHERE Student_ID = %s AND Chapter_ID = %s",
                (student_id, chapter_id)
            )
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO student_chapter_progress (Student_ID, Chapter_ID) VALUES (%s, %s)",
                    (student_id, chapter_id)# Комментарий от ChatGPT
                )
                self.connection.commit()
                return True
            return False
        except Exception as e:
            print(f"Error marking chapter as read: {e}")
            return False

    def get_read_chapters_for_student(self, student_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT c.Chapter_ID, c.Title FROM student_chapter_progress scp JOIN chapter c ON scp.Chapter_ID = c.Chapter_ID WHERE scp.Student_ID = %s",
                (student_id,)
            )
            return cursor.fetchall()# Комментарий от ChatGPT
        except Exception as e:
            print(f"Error getting read chapters for student: {e}")
            return []

    def get_attempts_with_verdict_for_student(self, student_id):
        try:
            self.connection.reconnect()#Комментарий от ChatGPT
            cursor = self.connection.cursor()
            cursor.execute(# Комментарий от ChatGPT
                "SELECT t.Name, a.Solution, a.Verdict, t.Task_ID FROM attempt a JOIN task t ON a.TaskTask_ID = t.Task_ID WHERE a.StudentStudent_ID = %s",
                (student_id,)# Комментарий от ChatGPT
            )
            return cursor.fetchall()# Комментарий от ChatGPT
        except Exception as e:
            print(f"Error getting attempts with verdict for student: {e}")
            return []

connection = mysql.connector.connect(host="localhost", user="root", password="1234", database="curseusers", charset='utf8mb4')
my_database = Database(connection)