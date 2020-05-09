import kivy
kivy.require('1.11.1') 
from kivy.uix.widget import Widget  # class to display widgets from kv file
from kivy.app import App    # base class to run kivy application  
import MySQLdb  #class for accessing database
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition    # Screen Manager Class to manage different Screens of the app
from kivy.uix.label import Label    # Label widget
from faces import face  # import the faces.py file containing the opencv code for face recognition
#imports for a dropdown button
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp


class LoginScreen(Screen,Widget): # class to display UI components linked in kv file
    def signIn(self):
        uname = self.ids["'uname'"].text.strip()
        password = self.ids["'password'"].text.strip()
        t_status = self.ids["'teacher'"].active
        s_status = self.ids["'student'"].active
        
        if(len(uname) >=5 and len(password) >=5):
            try:
                # Open database connection
                db = MySQLdb.connect("localhost","root","","facialattendancemanager" )  # format-> db_name,db_username,db_pass,db_name
                # prepare a cursor object using cursor() method
                cursor = db.cursor()
                #setting up a query depending on type of user
                if(s_status==True):
                    sql = f"SELECT `sname` FROM `student` WHERE username = '{uname}' and password = '{password}'" # the adjacent method is called f-string formatting
                    flag=1
                elif(t_status==True):
                    sql = f"SELECT `tname` FROM `teacher` WHERE username = '{uname}' and password = '{password}'"
                    flag=0
                #executing the above sql statement
                try:
                    # Execute the SQL command
                    cursor.execute(sql)
                    # Fetch all the rows in a list of lists.
                    results = cursor.fetchall()
                    for row in results:
                        name = row[0]
                        # Now print fetched result
                        print("the id is : {name} ".format(name=name))
                        print("value of flag is {flag}".format(flag=flag))
                        if(flag):
                            app.student_screen.recognizeStudent(name)
                            app.screen_manager.current = "studentscreen"
                        else:
                            app.teacher_screen.recognizeTeacher(name)
                            app.screen_manager.current = "teacherscreen"
                except:
                    print("Connected to database but unable to perform query")
                    # disconnect from server
                    db.close()
            except:
                print("cannot connect to database")

        else:
            print("enter details properly in loginScreeen parameters")

    def Exit(self):
        app.stop()

class StudentScreen(Screen,Widget):    # class to display student activity once loggedin
    def recognizeStudent(self,name):
        self.ids["'studentWelcomeLabel'"].text = "Hello "+name
        recognizedName  = face()
        if name == recognizedName:
            self.ids["'status'"].text = "Your attendance has been marked successfully "+ recognizedName
        try:
            # Open database connection
            db = MySQLdb.connect("localhost","root","","facialattendancemanager" )  # format-> db_name,db_username,db_pass,db_name
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            try:
                print("commiting")
                # Execute the SQL command
                cursor.execute('INSERT INTO `attendance`(`subid`, `dept_id`, `div_id`, `sem_id`, `t_id`) VALUES ("%d" ,"%d" ,"%d" ,"%d" ,"%d" )' % \
             (sub_id,dept_id,div_id,sem_id,tid))
                # Commit your changes in the database
                db.commit()
            except:
                print("rolling back")
                # Rollback in case there is any error
                db.rollback()
            # disconnect from server
            db.close()
        except:
            print("cannot connect to database student")

    def LogOutStudent(self):
        app.screen_manager.current = "loginscreen"

class TeacherScreen(Screen,Widget):    # class to display teacher activity once loggedin    
    def recognizeTeacher(self,name):
        self.ids["'teacherWelcomeLabel'"].text = "Hello "+name
        
    def LogOutTeacher(self):
        app.screen_manager.current = "loginscreen"
    
    def LogAttendance(self):
        subject = self.ids["'subject'"].text.strip()
        subject = subject.title()
        div = self.ids["'div'"].text.strip()
        div_dict = {"A":1,"B":2}
        div_id = div_dict[div]
        tid = self.ids["'teacherWelcomeLabel'"].text
        tid = tid[13:]
        print(subject)
        try:
            # Open database connection
            db = MySQLdb.connect("localhost","root","","facialattendancemanager" )  # format-> db_name,db_username,db_pass,db_name
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            #setting up a query depending on subject and division
            sql = f"SELECT `sub_id`, `dept_id`, `sem_id` FROM `subjects` WHERE sub_name = '{subject}'"
            #executing the above sql statement
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = cursor.fetchall()
                for row in results:
                    sub_id = row[0]
                    dept_id = row[1]
                    sem_id = row[2]
                cursor.close()
            except:
                print("Connected to database but unable to perform query to extract subject details")
                # disconnect from server
                db.close()
        except:
            print("cannot connect to database 1")

        try:
            print(sub_id)
            sub_id = int(sub_id)
            print(dept_id)
            dept_id = int(dept_id)
            print(div_id)
            div_id = int(div_id)
            print(sem_id)
            sem_id = int(sem_id)
            print(tid)
            tid = int(tid)

            # Open database connection
            db = MySQLdb.connect("localhost","root","","facialattendancemanager" )  # format-> db_name,db_username,db_pass,db_name
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            try:
                print("commiting")
                # Execute the SQL command
                cursor.execute('INSERT INTO `attendance`(`subid`, `dept_id`, `div_id`, `sem_id`, `t_id`) VALUES ("%d" ,"%d" ,"%d" ,"%d" ,"%d" )' % \
             (sub_id,dept_id,div_id,sem_id,tid))
                # Commit your changes in the database
                db.commit()
            except:
                print("rolling back")
                # Rollback in case there is any error
                db.rollback()
            # disconnect from server
            db.close()
            print("done")

            self.ids["'teacherWelcomeLabel'"].text = "Attendance marked for "+subject
        except:
            print("cannot connect to database 2")

class Controller(App): # Driver class 
    def build(self):
        self.screen_manager = ScreenManager(transition = FadeTransition())

        # adding login screen to the screen manager
        self.login_screen = LoginScreen()
        screen = Screen(name="loginscreen")
        screen.add_widget(self.login_screen)
        self.screen_manager.add_widget(screen)

        # adding student screen to the screen manager
        self.student_screen = StudentScreen()
        screen = Screen(name="studentscreen")
        screen.add_widget(self.student_screen)
        self.screen_manager.add_widget(screen)

        # adding teacher screen to the screen manager
        self.teacher_screen = TeacherScreen()
        screen = Screen(name="teacherscreen")
        screen.add_widget(self.teacher_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == '__main__':
    app = Controller()
    app.run() 