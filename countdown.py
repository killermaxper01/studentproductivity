import json
import os
import threading
import time
import logging
from datetime import datetime, timedelta
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from plyer import notification
import requests
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)

# Replace this with your Gemini API key
API_URL = "https://ai-doubt-solvers-api-2.onrender.com/get_ai_answer"
SECRET_AUTH_TOKEN = "R4@8j8v2erma/*+-iambigfanofmyselfR4@8j8v2erma/*+-iambigfanofmyself"


def handle_error(error, context=None):
    """Log errors and display user-friendly messages."""
    logging.error(f"Error in {context}: {error}", exc_info=True)
    dialog = MDDialog(
        title="Error",
        text=f"An error occurred: {str(error)}",
        buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
    )
    dialog.open()

# KivyMD UI Layout
KV = '''
MDNavigationLayout:
    ScreenManager:
        id: screen_manager

        WelcomeScreen:
            name: 'welcome'

        NameScreen:
            name: 'name'

        ExamScreen:
            name: 'exam'

        DateScreen:
            name: 'date'

        CountdownScreen:
            name: 'countdown'

        TaskScreen:
            name: 'tasks'

        StudyScreen:
            name: 'study'

        HistoryScreen:
            name: 'history'

        DescriptionScreen:
            name: 'description'

        AIChatScreen:
            name: 'ai_chat'

    MDNavigationDrawer:
        id: nav_drawer
        MDNavigationDrawerMenu:
            OneLineListItem:
                text: "Update Exam Details"
                on_release: app.update_exam_details()
            OneLineListItem:
                text: "Doubt Solver with Human AI"
                on_release: app.root.ids.screen_manager.current = 'ai_chat'
            OneLineListItem:
                text: "Task Manager"
                on_release: app.root.ids.screen_manager.current = 'tasks'
            OneLineListItem:
                text: "Study Timer"
                on_release: app.root.ids.screen_manager.current = 'study'
            OneLineListItem:
                text: "Toggle Theme"
                on_release: app.toggle_theme()
            OneLineListItem:
                text: "Description"
                on_release: app.root.ids.screen_manager.current = 'description'
            OneLineListItem:
                text: "Contact Owner"
                on_release: app.show_contact_dialog()
            OneLineListItem:
                text: "Close Menu"
                on_release: app.close_menu()

<WelcomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Welcome to Student Productivity App!"
            font_style: "H4"
            halign: "center"

        MDRaisedButton:
            text: "Get Started"
            on_release: root.go_to_name_screen()
            size_hint_x: None
            width: dp(200)
            pos_hint: {"center_x": 0.5}

<NameScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "What is your name?"
            font_style: "H5"
            halign: "center"

        MDTextField:
            id: name_input
            hint_text: "Enter your name"
            size_hint_x: None
            width: dp(300)
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Next"
            on_release: root.go_to_exam_screen()
            size_hint_x: None
            width: dp(200)
            pos_hint: {"center_x": 0.5}
        MDLabel:

<ExamScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "What is your exam name?"
            font_style: "H5"
            halign: "center"

        MDTextField:
            id: exam_input
            hint_text: "Enter exam name"
            size_hint_x: None
            width: dp(300)
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Next"
            on_release: root.go_to_date_screen()
            size_hint_x: None
            width: dp(200)
            pos_hint: {"center_x": 0.5}
        MDLabel:

<DateScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Select Exam Date"
            font_style: "H5"
            halign: "center"

        MDRaisedButton:
            text: "Pick Date"
            on_release: root.show_date_picker()
            size_hint_x: None
            width: dp(200)
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Start Countdown"
            on_release: root.start_countdown()
            size_hint_x: None
            width: dp(200)
            pos_hint: {"center_x": 0.5}
        MDLabel:

<CountdownScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        fits_system_windows: True  

        MDTopAppBar:
            id: md_top_app_bar  # ✅ Fix: Add ID for reference in Python
            title: "Hello, Student"  # ✅ Default text, updates dynamically
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]
            elevation: 4  
            pos_hint: {"top": 1}  

        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: 1  
            padding: dp(20)

            MDLabel:
                id: countdown_label
                text: "Countdown will appear here."
                font_style: "H5"
                halign: "center"
                markup: True
                size_hint_y: None
                height: self.texture_size[1]
                
            MDLabel:
                
                
                

<TaskScreen>:
    name: "tasks"
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Tasks"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, "current", "countdown")]]
            right_action_items: [["plus", lambda x: app.show_add_task_dialog()]]
        ScrollView:
            MDList:
                id: task_list

<StudyScreen>:
    name: "study"
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDLabel:
            text: "Study Timer"
            font_style: "H5"
            halign: "center"

        MDTextField:
            id: target_input
            hint_text: "Enter Study Time (Hours)"
            helper_text: "Leave blank to use last target"
            helper_text_mode: "on_focus"
            input_filter: "float"
            mode: "rectangle"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            id: study_button
            text: "Start Study Timer"
            md_bg_color: app.theme_cls.primary_color
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            on_release: app.toggle_study()

        MDLabel:
            id: timer_label
            text: "Time Elapsed: 00:00:00"
            font_style: "H6"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "View Study History"
            md_bg_color: app.theme_cls.accent_color
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            on_release: app.show_history()

<HistoryScreen>:
    name: "history"
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Study History"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, "current", "study")]]
        ScrollView:
            MDList:
                id: history_layout

<DescriptionScreen>:
    name: "description"
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "How to Use the App"
                font_style: "H4"
                halign: "center"
                color : 0.35,0.14,0.42,1
                bold: True

                
            MDSeparator:
                height: dp(2)  
            MDSeparator:
                height: dp(2)  
            MDLabel:
                text: '"saty pareshaan ho sakata hai parantu paraajit nahin"'
                font_style: "H6"
                halign: "center"
                theme_text_color: "Secondary"    
                color: 0.95,0.84,0.00,1   
            MDSeparator:
                height: dp(2)       
            MDLabel:
                text: "This app is best for students preparing for exams like JEE, NEET, or others. It saves your time and sends hourly notifications to remind you how much time is left for your exam. It motivates you to not waste time.because to many student only think about how many days left but not relise actually even for hour/secound left , if you wast 86400 secound then it is equivalant to 1 day  "
                font_style: "Body1"
                color: 0,0,0.5,1
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1]
           
            MDSeparator:
                height: dp(2)  
            MDSeparator:
                height: dp(2)  
               
            MDLabel:
                text: " Key Features:"
                font_style: "H5"
                halign: "center"
                bold: True
                color : 0.36,.25,.2,1
            MDSeparator:
                height: dp(1)  
            MDLabel:
                text:"Saves time with an **hourly countdown reminder"
                color:0,1,0,1
            MDSeparator:
                height: dp(1)     
                
            MDLabel:
                text:"Motivates you to stay focused"
                color : 0,1,0,1
            MDSeparator:
                height: dp(1)     
            MDLabel:
                text:"Every **hour and second** counts – make the most of your time!"
                color: 0,1,0,1
            MDSeparator:
                height: dp(1)      
                
            MDLabel:
                text:"Create task list "
                color : 0,1,0,1 
            MDSeparator:
                height: dp(1)     
                
            MDLabel:
                text:"count how many study time & track your study time history "
                color : 0,1,0,1
            MDSeparator:
                height: dp(1) 
            MDLabel:
                text: "Use the Advanced-Human-like AI feature** to solve doubts instantly and explore beyond the usual learning.  With **+3.7 billion parameters**, this AI is designed to assist students like you. This app is in the **development phase**, so your suggestions are always welcome!"
                font_style: "Body1"
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1]   
                bold: True       
                        
            MDSeparator:
                height: dp(1)  
            MDLabel:
                         
                text: " For feature suggestions, contact: **studyonlinejnv@gmail.com**"
                font_style: "Body2"
                halign: "center"
                theme_text_color: "Hint"
            MDSeparator:
                height: dp(1) 
            MDRaisedButton:
                text: "Back"
                on_release: app.root.ids.screen_manager.current = 'countdown'
                size_hint_x: None
                width: dp(200)
                pos_hint: {"center_x": 0.5}


<AIChatScreen>:
    name: "ai_chat"
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)
        padding: dp(10)

        MDLabel:
            id: query_count_label
            text: "Queries Left: {} / 10".format(app.ai_query_count)  # ✅ Dynamic Binding
            font_style: "H6"
            halign: "center"
            theme_text_color: "Primary"

        MDLabel:
            id: countdown_label
            text: "Next reset in: 60:00"
            font_style: "H6"
            halign: "center"
            theme_text_color: "Primary"
            color: (0, 1, 0, 1)  # Green color

        MDLabel:
            text: "Ask question with human ai "
            font_style: "H5"
            halign: "center"
            theme_text_color: "Primary"    

        MDTextField:
            id: question_input
            hint_text: "Enter your question"
            size_hint_x: 0.95
            pos_hint: {"center_x": 0.5}


        MDCard:
            size_hint: (0.95, 2)  # Increased height to 80% of the screen
            pos_hint: {"center_x": 0.5}
            padding: dp(20)  # Increased padding for better spacing
            radius: [10, 10, 10, 10]
            
            MDScrollView:
                MDBoxLayout:
                    id: answer_box
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)
                    
                    MDLabel:
                        id: answer_label
                        text: "AI response will appear here"
                        size_hint_y: None
                        height: self.texture_size[1]
                        theme_text_color: "Secondary"
                        font_size: "18sp"  # Increased font size for better readability
                        padding: dp(10)
                        
                        
        MDRaisedButton:
            text: "Get Answer"
            size_hint_x: 0.4
            pos_hint: {"center_x": 0.5}
            on_release: app.get_ai_answer()
                        

    
                        
'''

# Screen Classes


class LoadingScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_main, 3)  # Show for 3 seconds

    def switch_to_main(self, dt):
        self.manager.current = "main"

# Add this screen to ScreenManager in your app



class WelcomeScreen(Screen):
    def go_to_name_screen(self):
        self.manager.current = 'name'

class NameScreen(Screen):
    def go_to_exam_screen(self):
        user_name = self.ids.name_input.text.strip()
        if not user_name:
            self.show_alert("Please enter your name.")
            return

        self.manager.get_screen('exam').user_name = user_name
        self.manager.current = 'exam'

    def show_alert(self, message):
        dialog = MDDialog(title="Alert", text=message, buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()

class ExamScreen(Screen):
    def go_to_date_screen(self):
        exam_name = self.ids.exam_input.text.strip()
        if not exam_name:
            self.show_alert("Please enter exam name.")
            return

        self.manager.get_screen('date').exam_name = exam_name
        self.manager.get_screen('date').user_name = self.user_name
        self.manager.current = 'date'

    def show_alert(self, message):
        dialog = MDDialog(title="Alert", text=message, buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()

class DateScreen(Screen):
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.exam_date = datetime.combine(value, datetime.min.time())

    def start_countdown(self):
        if not hasattr(self, 'exam_date'):
            self.show_alert("Please select an exam date.")
            return
    
        countdown_screen = self.manager.get_screen('countdown')
    
        # ✅ Directly pass user data (no need to assign variables twice)
        countdown_screen.user_name = self.user_name
        countdown_screen.exam_name = self.exam_name
        countdown_screen.exam_date = self.exam_date
    
        # ✅ Start countdown and update UI
        countdown_screen.start_countdown()
        countdown_screen.update_top_bar()  # ✅ Ensure top bar updates with the student’s name
    
        self.manager.current = 'countdown'
    
        # ✅ Save user data for persistence
        JsonStore('data.json').put(
            'user_data',
            user_name=self.user_name,
            exam_name=self.exam_name,
            exam_date=self.exam_date.isoformat()
        )

    def show_alert(self, message):
        dialog = MDDialog(title="Alert", text=message, buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()

class CountdownScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = ""
        self.exam_name = ""
        self.exam_date = None
        self.countdown_event = None
        self.notification_thread = None

    def start_countdown(self):
        self.update_top_bar()
        Clock.schedule_interval(self.update_countdown, 0.1)
        if self.countdown_event:
            self.countdown_event.cancel()
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 0.1)

        # Start notification thread
        if self.notification_thread is None or not self.notification_thread.is_alive():
            self.notification_thread = threading.Thread(target=self.run_notifications, daemon=True)
            self.notification_thread.start()

        # Notify when app is opened
        self.notify_on_open()


    def update_top_bar(self):
        """Update top bar with student's name"""
        if "md_top_app_bar" in self.ids:
            if self.user_name:
                self.ids.md_top_app_bar.title = f"Hello, {self.user_name}"
            else:
                self.ids.md_top_app_bar.title = "Hello, Student"



    def update_countdown(self, dt):
        if not self.exam_date:
            return

        now = datetime.now()
        time_left = self.exam_date - now

        if time_left.total_seconds() <= 0:
            self.ids.countdown_label.text = "Exam Time!"
            self.countdown_event.cancel()
            return

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int(time_left.microseconds / 1000)

        countdown_text = (
            f"[b][color=#964B00] time is like sand on your palm [/color][/b]\n\n"
            f"[b][color=2F4F7F][size=60]exception[/size][/color][/b]\n\n"
           # f"Total: [b][color=#FF0000]{days}[/color][/b] days left for your exam \n\n"
           f"Total: [b][color=#FF0000]{days}[/color][/b] days left for your [b][color=#FF0000]{self.exam_name}[/color][/b] exam.\n\n"
            f"[b][color=#800080][size=60]Welcome to reality[/size][/color][/b]\n\n"
            f"Total: [b][color=#FF0000]{days * 24 + hours}[/color][/b] hours left\n"
            f"Total: [b][color=#FF0000]{days * 1440 + hours * 60 + minutes}[/color] [/b]minutes left\n"
            f"Total: [b][color=#00FFFF]{days * 86400 + hours * 3600 + minutes * 60 + seconds}[/color][/b] seconds left\n"
            f"Total:[b][color=#00FFFF] {days * 86400000 + hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds}[/color] [/b] milliseconds left"
        )

        self.ids.countdown_label.text = countdown_text

        if minutes == 0 and seconds == 0:
            notification.notify(
                title="Exam Countdown",
                message=f"Hi {self.user_name}, {days * 24 + hours} hours left for {self.exam_name}!",
                timeout=10
            )

    def run_notifications(self):
        while True:
            now = datetime.now()
            time_left = self.exam_date - now

            if time_left.total_seconds() <= 0:
                return

            hours_left = time_left.days * 24 + time_left.seconds // 3600
            notification.notify(
                title="Exam Countdown",
                message=f"Hi {self.user_name}, {hours_left} hours left for {self.exam_name}.",
                timeout=10
            )
            threading.Event().wait(3600)  # Sleep for 1 hour

    def notify_on_open(self):
        now = datetime.now()
        time_left = self.exam_date - now

        if time_left.total_seconds() <= 0:
            return

        hours_left = time_left.days * 24 + time_left.seconds // 3600
        notification.notify(
            title="Exam Countdown",
            message=f"Hi {self.user_name}, {hours_left} hours left for {self.exam_name}.",
            timeout=10
        )

class TaskScreen(Screen):
    pass

class TaskItem(TwoLineAvatarIconListItem):
    task_name = StringProperty()
    task_category = StringProperty()
    is_completed = BooleanProperty(False)

    def __init__(self, task_name, task_category, is_completed=False, **kwargs):
        super().__init__(**kwargs)
        self.task_name = task_name
        self.task_category = task_category
        self.is_completed = is_completed
        self.text = task_name
        self.secondary_text = f"Category: {task_category}"

        # ✅ Task complete button (Left)
        self.checkbox = IconLeftWidget(icon="check-circle" if is_completed else "checkbox-blank-circle-outline")
        self.checkbox.bind(on_release=self.toggle_complete)
        self.add_widget(self.checkbox)

        # ✅ Task delete button (Right)
        self.delete_button = IconRightWidget(icon="delete")
        self.delete_button.bind(on_release=lambda x: MDApp.get_running_app().delete_task(self))
        self.add_widget(self.delete_button)

    def toggle_complete(self, instance):
        """Mark task as complete or incomplete and update notifications."""
        try:
            self.is_completed = not self.is_completed
            instance.icon = "check-circle" if self.is_completed else "checkbox-blank-circle-outline"
    
            # ✅ Update task status in `task_data`
            app = MDApp.get_running_app()
            for task in app.task_data:
                if task["name"] == self.task_name and task["category"] == self.task_category:
                    task["completed"] = self.is_completed
                    break
    
            app.save_tasks()  # ✅ Save updated tasks
            app.update_task_list()  # ✅ Refresh UI
            # ✅ Update notification immediately
    
        except Exception as e:
            MDApp.get_running_app().handle_error(e)

class StudyScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

class DescriptionScreen(Screen):
    pass

class AIChatScreen(Screen):
    pass

# Main App Class
class StudentProductivityApp(MDApp):
    task_data = []
    dialog = None
    json_file = "tasks.json"
    study_data = {}
    target_time = 0
    elapsed_time = 0
    start_time = None
    is_studying = False
    timer_event = None
    ai_query_count = NumericProperty(10)  
    last_query_date = None
    reset_timer_event = None
    user_name = ""
   
    def build(self):
        self.theme_cls.theme_style = "Light"  # Set default mode to Light
        self.theme_cls.primary_palette = "Red"  # Set Primary Color to Red
        self.theme_cls.accent_palette = "Blue"  # Set Accent Color to Blue
        self.load_theme_preference()  # Load the last saved preference
        Window.bind(on_keyboard=self.on_back_button)
        return Builder.load_string(KV)






    def on_start(self):
        """Load tasks, user data, and update countdown."""
        self.load_theme_preference()  # ✅ Load UI theme
        self.load_tasks()  # ✅ Load task list
        self.study_data = self.load_study_data()  # ✅ Load study data
    
        # ✅ Load user data (Name, Exam Name, Exam Date)
        store = JsonStore('data.json')
        if store.exists('user_data'):
            user_data = store.get('user_data')
    
            countdown_screen = self.root.ids.screen_manager.get_screen('countdown')
    
            # ✅ Directly update the countdown screen (self.user_name is already in __init__)
            countdown_screen.user_name = user_data.get('user_name', '')
            countdown_screen.exam_name = user_data.get('exam_name', '')
            countdown_screen.exam_date = datetime.fromisoformat(user_data.get('exam_date', ''))
    
            countdown_screen.start_countdown()  # ✅ Start countdown first
            countdown_screen.update_top_bar()  # ✅ Then update top bar with student name
    
            self.root.ids.screen_manager.current = 'countdown'
    
        # ✅ Load AI query count and last query date
        self.load_ai_query_data()
    
        # ✅ Start the reset timer
        self.start_reset_timer()

    def start_reset_timer(self):
        """Start the timer to reset AI queries every hour."""
        if self.reset_timer_event:
            self.reset_timer_event.cancel()
        self.reset_timer_event = Clock.schedule_interval(self.reset_ai_query_data, 60)  # Check every minute

    def reset_ai_query_data(self, *args):
        """Reset AI query data to default values and save a new JSON file."""
        self.ai_query_count = 10  # ✅ Set correct reset value
        self.last_query_date = datetime.now()
        
        self.save_ai_query_data()  # ✅ Save new data
        self.save_ai_query_data()
        self.update_query_count_label()
        self.update_countdown_label()

    def update_countdown_label(self):
        """Update the countdown label with the time remaining until the next reset."""
        if self.last_query_date:
            time_since_last_query = (datetime.now() - self.last_query_date).total_seconds()
            time_remaining = max(0, 3600 - time_since_last_query)
            minutes, seconds = divmod(int(time_remaining), 60)
            self.root.ids.screen_manager.get_screen("ai_chat").ids.countdown_label.text = f"Next reset in: {minutes:02d}:{seconds:02d}"
        else:
            self.root.ids.screen_manager.get_screen("ai_chat").ids.countdown_label.text = "Next reset in: 60:00"

    def toggle_theme(self):
        """Toggle between light and dark mode."""
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.save_theme_preference()  # ✅ Save after toggling
        
    def save_theme_preference(self):
        """Save user's theme preference to a JSON file."""
        try:
            with open("theme_preference.json", "w") as f:
                json.dump({"theme": self.theme_cls.theme_style}, f)
        except Exception as e:
            print(f"Error saving theme preference: {e}")  # ✅ Prevent crashes
            
    def load_theme_preference(self):
        """Load theme preference from JSON and apply it."""
        if os.path.exists("theme_preference.json"):
            try:
                with open("theme_preference.json", "r") as f:
                    data = json.load(f)
                    self.theme_cls.theme_style = data.get("theme", "Dark")  # ✅ Default: Dark mode
            except Exception as e:
                print(f"Error loading theme preference: {e}")  # ✅ Prevent crashes
    
    def show_add_task_dialog(self):
        """Show dialog to add a task."""
        try:
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                title="Add Task",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(hint_text="Task Name", id="task_name"),
                    MDTextField(hint_text="Category (Homework/Exams )", id="task_category"),
                    orientation="vertical",
                    spacing=10,
                    size_hint_y=None,
                    height="120dp",
                ),
                buttons=[
                    MDRaisedButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="Add", on_release=self.add_task),
                ],
            )
            self.dialog.open()
        except Exception as e:
            self.handle_error(e)

    def add_task(self, instance):
        """Add a task from the dialog input."""
        try:
            if not self.dialog or not self.dialog.content_cls:
                raise ValueError("Dialog content is missing")

            content = self.dialog.content_cls
            task_name = content.ids.get("task_name", None).text.strip() if content.ids.get("task_name") else ""
            task_category = content.ids.get("task_category", None).text.strip() if content.ids.get("task_category") else "General"

            if not task_name:
                self.handle_error("Task name cannot be empty.")
                return

            new_task = {"name": task_name, "category": task_category, "completed": False}
            self.task_data.append(new_task)
            self.save_tasks()
            self.update_task_list()
           
            self.dialog.dismiss()
        except Exception as e:
            self.handle_error(e)

    def delete_task(self, task_item):
        """Delete a task with animation."""
        try:
            anim = Animation(opacity=0, duration=0.3)
            anim.bind(on_complete=lambda *args: self.remove_task_from_list(task_item))
            anim.start(task_item)
        except Exception as e:
            self.handle_error(e)

    def remove_task_from_list(self, task_item):
        """Remove task after animation."""
        self.task_data = [task for task in self.task_data if task["name"] != task_item.task_name]
        self.save_tasks()
        self.update_task_list()
       

    def update_task_list(self):
        """Refresh the task list."""
        try:
            task_list = self.root.ids.screen_manager.get_screen("tasks").ids.task_list
            task_list.clear_widgets()
            for task in self.task_data:
                task_list.add_widget(TaskItem(task_name=task["name"], task_category=task["category"], is_completed=task["completed"]))
        except Exception as e:
            self.handle_error(e)

    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.json_file, "w") as f:
                json.dump(self.task_data, f, indent=4)
        except Exception as e:
            self.handle_error(e)

    def load_tasks(self):
        """Load tasks from JSON file."""
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, "r") as f:
                    self.task_data = json.load(f)
            self.update_task_list()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.task_data = []  # Reset if file is corrupt
            self.handle_error(f"Error loading tasks: {e}")

    def format_elapsed_time(self, seconds):
        """Format elapsed time as HH:MM:SS."""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"    
        
            
                            

            
            

    def handle_error(self, error):
        """Handle errors safely."""
        handle_error(error, context="StudentProductivityApp")

    def toggle_study(self):
        """Start or pause study timer."""
        if self.is_studying:
            self.stop_study()
        else:
            self.start_study()

    def start_study(self):
        """Start the study timer using latest data if available."""
        try:
            user_input = self.root.ids.screen_manager.get_screen("study").ids.target_input.text.strip()

            # If user provides a new target, use it
            if user_input:
                target_hours = float(user_input)
                if target_hours <= 0:
                    raise ValueError("Enter a valid number of hours!")
                self.target_time = int(target_hours * 3600)  # Convert to seconds
                self.save_latest_target(target_hours)

            # If no input, use the latest target from JSON
            elif self.get_latest_target():
                self.target_time = int(self.get_latest_target() * 3600)
                self.root.ids.screen_manager.get_screen("study").ids.target_input.hint_text = f"Last Target: {self.get_latest_target()} hrs"

            else:
                self.show_dialog("No Data", "No previous target found. Please enter a study time.")
                return

            self.start_time = time.time()  # Save start time
            self.is_studying = True
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
            self.root.ids.screen_manager.get_screen("study").ids.study_button.text = "Pause Study Timer"
            self.show_dialog("Study Started", "Timer is running. Focus on your studies!")

        except ValueError as e:
            self.show_dialog("Error", str(e))

    def update_timer(self, dt):
        """Update timer every second."""
        elapsed = int(time.time() - self.start_time) + self.elapsed_time
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.root.ids.screen_manager.get_screen("study").ids.timer_label.text = f"Time Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}"

        if elapsed >= self.target_time:
            self.stop_study()
            self.send_notification("Study Completed", "You have reached your target time!")

    def stop_study(self):
        """Pause the study timer and save data, then update history immediately."""
        if not self.start_time:
            self.show_dialog("Error", "Timer not started!")
            return
    
        elapsed = int(time.time() - self.start_time)
        self.elapsed_time += elapsed  # Add elapsed time
        self.start_time = None
        self.is_studying = False
        Clock.unschedule(self.timer_event)
        self.root.ids.screen_manager.get_screen("study").ids.study_button.text = "Resume Study Timer"
    
        today = datetime.today().strftime('%Y-%m-%d')
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        actual_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
        # ✅ Update self.study_data immediately
        if today not in self.study_data:
            self.study_data[today] = []
    
        self.study_data[today].append({
            "target_hours": round(self.target_time / 3600, 2),
            "actual_time": actual_time_str
        })
    
        self.save_study_data()  # ✅ Save updated study data
        self.update_table()  # ✅ Refresh history instantly
        self.send_notification("Study Saved", f"Target: {self.study_data[today][-1]['target_hours']} hrs, Actual: {actual_time_str}")

    def show_history(self):
        """Show study history with error handling and ensure it's updated."""
        try:
            self.study_data = self.load_study_data()  # ✅ Load latest data before showing history
            self.update_table()  # ✅ Ensure UI is updated instantly
            self.root.ids.screen_manager.current = 'history'  # ✅ Switch to history screen
        except Exception as e:
            print(f"⚠ Error displaying history: {e}")  # ✅ Log error
            self.show_dialog("Error", "Unable to display history. Please try again.")

    def update_table(self):
        """Display study history with latest sessions first (reverse order)."""
        history_layout = self.root.ids.screen_manager.get_screen("history").ids.history_layout
        history_layout.clear_widgets()  # Clear previous UI to prevent duplicate entries
    
        if not isinstance(self.study_data, dict) or not self.study_data:
            self.show_dialog("Info", "No study history available.")
            return
    
        history_layout.height = dp(40) * sum(len(sessions) for sessions in self.study_data.values())
    
        try:
            # ✅ Reverse sorting to show latest first
            for date, sessions in sorted(self.study_data.items(), reverse=True):
                for session in reversed(sessions):  # ✅ Reverse each day's sessions too
                    if not isinstance(session, dict):
                        print(f"⚠ Skipping invalid session: {session}")
                        continue
    
                    label = MDLabel(
                        text=f"{date} | Target: {session.get('target_hours', 0)} hrs | Actual: {session.get('actual_time', '00:00:00')}",
                        halign="center",
                        theme_text_color="Primary",
                        size_hint_y=None,
                        height=dp(40)
                    )
                    history_layout.add_widget(label)  # ✅ Add latest study session first
        except Exception as e:
            print(f"⚠ Error updating study history: {e}")
            self.show_dialog("Error", "Unable to load history. Try again later.")
            
                      
                                          
            
    def load_study_data(self):
        """Load study history safely, ensuring it returns a dictionary."""
        file_path = "study_data.json"
    
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)  # ✅ Load JSON
                    
                    if isinstance(data, dict):  
                        return data  # ✅ Return valid dictionary
                    
                    print("⚠ Invalid JSON format detected. Resetting study data.")
                    return {}  # ✅ Reset if JSON is corrupted
    
            except (json.JSONDecodeError, ValueError, TypeError):
                print("⚠ Error loading study data. Resetting to default.")
                return {}  # ✅ Return empty dictionary if file is broken
    
        return {}  # ✅ Return empty dictionary if file does not exist
        
    
    def save_study_data(self):
        """Save study records safely without overwriting previous entries."""
        file_path = "study_data.json"
    
        study_data = self.load_study_data()  # ✅ Load existing data properly
        today = datetime.today().strftime('%Y-%m-%d')
    
        # Ensure today's entry is a list (for multiple sessions)
        if today not in study_data:
            study_data[today] = []
    
        # Append new study session
        study_data[today].append({
            "target_hours": round(self.target_time / 3600, 2),
            "actual_time": self.format_elapsed_time(self.elapsed_time)
        })
    
        try:
            with open(file_path, "w") as f:
                json.dump(study_data, f, indent=4)  # ✅ Save properly formatted JSON
        except Exception as e:
            print(f"⚠ Error saving study data: {e}")  # ✅ Handle file errors gracefully
            
            
    def save_latest_target(self, target):
        """Save the latest study target time to a JSON file."""
        try:
            with open("latest_target.json", "w") as f:
                json.dump({"latest_target": target}, f)
        except Exception as e:
            print(f"⚠ Error saving latest target: {e}")
                
                

    def get_latest_target(self):
        """Retrieve latest target study time."""
        if os.path.exists("latest_target.json"):
            with open("latest_target.json", "r") as f:
                return json.load(f).get("latest_target", 0)
        return 0

    def show_dialog(self, title, message):
        """Show error or info dialog."""
        MDDialog(title=title, text=message).open()

    def send_notification(self, title, message):
        """Send notification using Plyer."""
        notification.notify(title=title, message=message, timeout=5)

    def update_exam_details(self):
        self.root.ids.screen_manager.current = 'name'
        self.close_menu()

    def show_motivation(self):
        dialog = MDDialog(title="DOUBT_KILLER", text="This feature comming $OON \n doubt solve with advanced -----  Human Ai--- ", buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()

    def show_contact_dialog(self):
        dialog = MDDialog(
            title="Contact Owner",
            text="Email: studyonlyjnv@gmail.com",
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

    def close_menu(self):
        self.root.ids.nav_drawer.set_state("close")
        
            
    def on_back_button(self, window, key, *args):
        """Prevent accidental exit and always show a confirmation dialog."""
        if key == 27:  # Android back button keycode
            screen_manager = self.root.ids.screen_manager
            current_screen = screen_manager.current
    
            if current_screen == "welcome":
                if JsonStore('data.json').exists('user_data'):
                    screen_manager.current = 'countdown'
                else:
                    Clock.schedule_once(lambda dt: self.show_exit_dialog(), 0.1)  # ✅ Show exit confirmation
                return True  # ✅ Prevent immediate app exit
    
            screen_transitions = {
                "name": "welcome",
                "exam": "name",
                "date": "exam",
                "tasks": "countdown",
                "study": "countdown",
                "history": "study",
                "description": "countdown",
                "ai_chat": "countdown"
            }
    
            if current_screen in screen_transitions:
                screen_manager.current = screen_transitions[current_screen]
            else:
                Clock.schedule_once(lambda dt: self.show_exit_dialog(), 0.1)  # ✅ Always show exit confirmation
                return True  # ✅ Prevent app from closing accidentally
    
            return True  # ✅ Consume back button event
        return False
    
    def show_exit_dialog(self):
        """Show exit confirmation dialog, preventing double back press exit."""
        if hasattr(self, "exit_dialog") and self.exit_dialog:  
            return  # ✅ Prevent multiple dialogs from stacking
    
        self.exit_dialog = MDDialog(
            title="Exit App",
            text="Are you sure you want to exit?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: self.close_exit_dialog()
                ),
                MDRaisedButton(
                    text="Exit",
                    on_release=lambda x: self.stop()
                )
            ]
        )
    
        Clock.schedule_once(lambda dt: self.exit_dialog.open(), 0.1)  # ✅ Delay to ensure stability
    
    def close_exit_dialog(self):
        """Close exit dialog and reset its reference."""
        if hasattr(self, "exit_dialog") and self.exit_dialog:
            self.exit_dialog.dismiss()
            self.exit_dialog = None  # ✅ Reset so a new dialog can be shown later
       
    def get_ai_answer(self):
        """Runs API request in a separate thread for smooth UI."""
        try:
            question = self.root.ids.screen_manager.get_screen("ai_chat").ids.question_input.text
            if not question:
                self.root.ids.screen_manager.get_screen("ai_chat").ids.answer_label.text = "[b]Please enter a question.[/b]"
                return
    
            # Check if AI query limit is reached
            if self.ai_query_count <= 0:
                self.root.ids.screen_manager.get_screen("ai_chat").ids.answer_label.text = "[b]Daily AI query limit reached. Try again tomorrow.[/b]"
                return
    
            self.root.ids.screen_manager.get_screen("ai_chat").ids.answer_label.text = "[i]Fetching AI response...[/i]"
            self.ai_query_count -= 1
            self.update_query_count_label()
    
            Thread(target=self.fetch_answer, args=(question,), daemon=True).start()
        except Exception as e:
            self.handle_error(e)

    def fetch_answer(self, question):
        """Sends the request to AI API securely."""
        headers = {
            "Authorization": SECRET_AUTH_TOKEN,
            "Content-Type": "application/json"
        }
        data = {"question": question}
    
        try:
            response = requests.post(API_URL, json=data, headers=headers)
    
            if response.status_code == 200:
                answer = response.json().get("answer", "No response.")
            elif response.status_code == 429:
                answer = "[b]Rate Limit Exceeded! Try again later.[/b]"
            elif response.status_code == 403:
                answer = "[b]Unauthorized! Check API Token.[/b]"
            else:
                answer = f"[b]Error {response.status_code}:[/b] {response.text}"
    
        except Exception as e:
            answer = f"[b]Error:[/b] {str(e)}"
    
        self.update_ui(answer)
    
    @mainthread
    def update_ui(self, answer):
        try:
            screen = self.root.ids.screen_manager.get_screen("ai_chat")
            screen.ids.answer_label.text = answer
        except AttributeError:
            Clock.schedule_once(lambda dt: self.update_ui(answer), 0.1)  # Retry after a short delay

    def update_query_count_label(self):
        """Update the query count label on the AI chat screen."""
        screen = self.root.ids.screen_manager.get_screen("ai_chat")
        screen.ids.query_count_label.text = f"Queries Left: {self.ai_query_count}/10"
    
    def load_ai_query_data(self):
        """Load AI query count and last query date, handling errors safely."""
        file_path = "ai_query_data.json"
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)  # ✅ Load JSON
                    
                    # Validate loaded data
                    self.ai_query_count = data.get("ai_query_count", 10)  #  Old default 10
                    last_query_date_str = data.get("last_query_date")
                    
                    if last_query_date_str:
                        self.last_query_date = datetime.fromisoformat(last_query_date_str)
                        
                        # ✅ Reset to 10 if a new hour has started
                        if (datetime.now() - self.last_query_date).total_seconds() >= 3600:
                            self.ai_query_count = 10  
    
            except (json.JSONDecodeError, ValueError, KeyError):
                print("⚠ Error loading AI query data. Resetting to default.")
                self.reset_ai_query_data()  # ✅ Reset to default if file is corrupted
    
        else:
            self.reset_ai_query_data()  # ✅ Create file if it doesn't exist
    
    def reset_ai_query_data(self, *args):
        """Reset AI query data to 10 queries per hour and save a new JSON file."""
        self.ai_query_count = 10  # ✅ Correct value
        self.last_query_date = datetime.now()
        self.save_ai_query_data()
        self.update_query_count_label()  # ✅ Update UI Immediately
    
    def save_ai_query_data(self):
        """Save AI query count and last query date safely."""
        data = {
            "ai_query_count": self.ai_query_count,
            "last_query_date": self.last_query_date.isoformat()
        }
        with open("ai_query_data.json", "w") as f:
            json.dump(data, f, indent=4)  # ✅ Now it actually saves!

    def on_stop(self):
        """Save AI query data when app is closed."""
        self.save_ai_query_data()
            
if __name__ == "__main__":
    StudentProductivityApp().run()