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
        
        if(len(uname) >=10 and len(password) >=5):
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

    def LogOutStudent(self):
        app.screen_manager.current = "loginscreen"

class TeacherScreen(Screen,Widget):    # class to display teacher activity once loggedin    
    def recognizeTeacher(self,name):
        self.ids["'teacherWelcomeLabel'"].text = "Hello "+name
        subjectName = []
        try:
            # Open database connection
            db = MySQLdb.connect("localhost","root","","facialattendancemanager" )  # format-> db_name,db_username,db_pass,db_name
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            sql = f"SELECT `sub_name` FROM `subjects`" 
            #executing the above sql statement
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = cursor.fetchall()
                for row in results:
                    subjectName.append(row[0])
            except:
                print("Connected to database but unable to perform query")
                # disconnect from server
                db.close()
        except:
            print("cannot connect to database")

        if(len(subjectName)==0):
            print("error connecting to server")
            app.screen_manager.current = "loginscreen"
        else:
            print(subjectName)
            dropdown = DropDown()
            for sub in subjectName:
                #adding dropdown
                btn = Button(text='%r' % sub, size_hint_y=None, height=50, width = 150)
                btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)
            mainbutton = Button(text='Select Subject', size_hint=(0.15, 0.095) , pos_hint={'top': 0.52,'right': 0.55} )
            mainbutton.bind(on_release=dropdown.open)
            dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
            self.add_widget(mainbutton)

    def LogOutTeacher(self):
        app.screen_manager.current = "loginscreen"
    
    def on_select(self, data):
        self.sub = data
    
    def LogAttendance(self):
        div = self.ids["'div'"].text
        print(div +" "+self.sub)

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