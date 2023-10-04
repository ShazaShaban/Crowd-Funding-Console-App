import json
import re
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password, mobile):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile = mobile
        self.is_active = False  # Set to True after email confirmation

    def register(self):
        # Save user data to a JSON file
        user_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'mobile': self.mobile,
            'is_active': self.is_active
        }
        with open('users.json', 'a') as file:
            json.dump(user_data, file)
            file.write('\n')
toot toot shed 7elak ya katkot
    def login(self, email, password):
        # Check if the email and password match an existing user in the JSON file
        with open('users.json', 'r') as file:
            for line in file:
                user_data = json.loads(line)
                if user_data['email'] == email and user_data['password'] == password:
                    self.is_active = True
                    return True
            return False

class Project:
    def __init__(self, title, details, total_target, start_time, end_time, owner):
        self.title = title
        self.details = details
        self.total_target = total_target
        self.start_time = start_time
        self.end_time = end_time
        self.owner = owner

    def create(self):
        # Save project data to a JSON file
        project_data = {
            'title': self.title,
            'details': self.details,
            'total_target': self.total_target,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'owner': self.owner
        }
        with open('projects.json', 'a') as file:
            json.dump(project_data, file)
            file.write('\n')


    @staticmethod
    def is_valid_target_amount(total_target):
        try:
            total_target = float(total_target)
            if total_target <= 0:
                return False
            return True
        except ValueError:
            return False

        
    @staticmethod
    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_date_range(start_date, end_date):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
            return start_date < end_date
        except ValueError:
            return False

    def search_projects_by_date(date, search_type):
        projects = []

        # Define the search function based on the search_type
        def search_function(project_date):
            if search_type == 'start':
                return project_date >= date
            elif search_type == 'end':
                return project_date <= date
            return False

        with open('projects.json', 'r') as file:
            for line in file:
                project_info = json.loads(line)
                start_date = project_info['start_time']
                end_date = project_info['end_time']

                if search_function(start_date) or search_function(end_date):
                    projects.append(project_info)

        return projects
    



    @staticmethod
    def list_all():
        projects = []
        with open('projects.json', 'r') as file:
            for line in file:
                project_info = json.loads(line)
                projects.append(project_info)
        return projects
    
    


class MainApp:
    def __init__(self):
        self.registered_emails = set()
        self.user = None

    # Validation functions
    def is_valid_egyptian_mobile(self, mobile):
        # Define a regular expression pattern for Egyptian mobile numbers
        pattern = r'^(01|\+201)[0-9]{9}$'
        if re.match(pattern, mobile):
            return True
        else:
            return False

    def is_valid_name(self, name):
        # Check if the name contains only letters and no spaces
        return name.isalpha()

    def is_valid_email(self, email):
        # Define a regular expression pattern for a basic email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            return False

    def is_duplicate_email(self, email):
        # Check if the email is already registered
        return email in self.registered_emails




    def register_user(self):
        while True:
            first_name = input("Enter your first name: ")
            if self.is_valid_name(first_name):
                break
            else:
                print("Invalid first name format. Please try again.")

        while True:
            last_name = input("Enter your last name: ")
            if self.is_valid_name(last_name):
                break
            else:
                print("Invalid last name format. Please try again.")

        while True:
            email = input("Enter your email: ")
            if self.is_valid_email(email):
                if not self.is_duplicate_email(email):
                    self.registered_emails.add(email)
                    break
                else:
                    print("Email is already registered. Please use a different email.")
            else:
                print("Invalid email format. Please try again.")

        while True:
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")
            if password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")

        while True:
            mobile = input("Enter your mobile number (e.g., 01012345678 or +201012345678): ")
            if self.is_valid_egyptian_mobile(mobile):
                break
            else:
                print("Invalid mobile number format. Please try again.")

        self.user = User(first_name, last_name, email, password, mobile)
        self.user.register()
        print("Registration successful! Please log in.")

    def login_user(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        self.user = User('', '', email, password, '')  # Create a User object
        if self.user.login(email, password):
            print("Login successful. Welcome! ")
            self.user.is_active = True

            while self.user.is_active:
                print("1. Create a project")
                print("2. Edit your projects")
                print("3. Delete your projects")
                print("4. List all projects")
                print("5. Logout")

                user_choice = input("Enter your choice: ")

                if user_choice == '1':
                    self.create_project()

                elif user_choice == '2':
                    self.edit_project()

                elif user_choice == '3':
                    self.delete_project()

                elif user_choice == '4':
                    self.list_projects()

                elif user_choice == '5':
                    self.user.is_active = False
                    print("Logged out successfully!")

                else:
                    print("Invalid choice. Please try again.")

        else:
            print("Login failed. Please check your email and password.")





    def project_exists(self, title):
        # Check if a project with the given title already exists in the JSON file
        with open('projects.json', 'r') as file:
            for line in file:
                project_data = json.loads(line)
                if project_data['title'] == title:
                    return True
        return False
    

    def create_project(self):
        title = input("Enter project title: ")
        
        if self.project_exists(title):
            print("A project with the same title already exists. Please choose a different title.")
            return  # Don't create the project if it already exists
        
        details = input("Enter project details: ")
        
        while True:
            total_target = input("Enter total target amount: ")
            if Project.is_valid_target_amount(total_target):
                break
            else:
                print("Invalid target amount. Please enter a valid numeric value greater than 0.")

        while True:
            start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
            if Project.is_valid_date(start_time):
                break
            else:
                print("Invalid start date format. Please use the format 'YYYY-MM-DD HH:MM'.")

        while True:
            end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
            if Project.is_valid_date(end_time) and Project.is_valid_date_range(start_time, end_time):
                break
            else:
                print("Invalid end date format or end date should be after start date. Please use the format 'YYYY-MM-DD HH:MM'.")

        project = Project(title, details, total_target, start_time, end_time, self.user.email)
        project.create()
        print("Project created successfully!")


    def edit_project(self):
        print("Editing your own project")
        title = input("Enter the title of the project you want to edit: ")

        projects = Project.list_all()  # Get a list of all projects

        for project in projects:
            if project['title'] == title and project['owner'] == self.user.email:
                # Found the project with the specified title and owned by the user
                print("Project found! You can now edit it.")

                print("Select what you want to edit:")
                print("1. Title")
                print("2. Details")
                print("3. Total Target Amount")
                print("4. Start Time")
                print("5. End Time")
                choice = input("Enter your choice: ")

                if choice == '1':
                    new_title = input("Enter a new title: ")
                    project['title'] = new_title
                elif choice == '2':
                    new_details = input("Enter new details: ")
                    project['details'] = new_details
                elif choice == '3':
                    new_total_target = input("Enter a new total target amount: ")
                    project['total_target'] = new_total_target
                elif choice == '4':
                    new_start_time = input("Enter a new start time (YYYY-MM-DD HH:MM): ")
                    project['start_time'] = new_start_time
                elif choice == '5':
                    new_end_time = input("Enter a new end time (YYYY-MM-DD HH:MM): ")
                    project['end_time'] = new_end_time

                # Save the updated project information back to the JSON file
                with open('projects.json', 'w') as file:
                    for proj in projects:
                        json.dump(proj, file)
                        file.write('\n')

                print("Project updated successfully!")
                return

        # If the loop completes without finding the project, it means it doesn't exist or doesn't belong to the user
        print("Project with the specified title not found or you do not have permission to edit it.")


    def search_projects_by_date(self):
        date = input("Enter the date (YYYY-MM-DD): ")
        search_type = input("Search by start date ('start') or end date ('end'): ")

        if search_type not in ['start', 'end']:
            print("Invalid search type. Please enter 'start' or 'end'.")
            return

        projects = Project.search_projects_by_date(date, search_type)

        if not projects:
            print("No projects found for the specified date and search type.")
        else:
            print("Projects found:")
            for index, project in enumerate(projects, 1):
                print(f"{index}. Title: {project['title']}, Owner: {project['owner']}, Start Date: {project['start_time']}, End Date: {project['end_time']}")
    

    def delete_project(self):
        title = input("Enter the Project Title to delete: ")
        if self.delete_by_title(title):
            print("Project deleted successfully.")
        else:
            print("Project with the specified title not found or you do not have permission to delete it.")

    def delete_by_title(self, title):
        # Delete the project by its title
        projects = []
        found = False  # To track whether the project with the specified title was found

        with open('projects.json', 'r') as file:
            for line in file:
                project_info = json.loads(line)
                if project_info['title'] != title:
                    projects.append(project_info)
                else:
                    # Check if the project belongs to the logged-in user
                    if project_info['owner'] == self.user.email:
                        found = True  # Project with the specified title was found and belongs to the user
                    else:
                        projects.append(project_info)  # Add the project back to the list

        with open('projects.json', 'w') as file:
            for project_info in projects:
                json.dump(project_info, file)
                file.write('\n')

        return found  # Return True if the project was found and deleted, False otherwise



    def list_projects(self):
        projects = Project.list_all()
        print("Your current Projects are:")
        print("\n")
        for index, project in enumerate(projects, 1):
            print(f"{index}. Title: {project['title']}, Owner: {project['owner']}")





            
    def main(self):
        while True:
            print("Welcome to the Crowdfunding Console App")
            print("1. Register")
            print("2. Login")
            print("3. Search Projects by Date")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.register_user()

            elif choice == '2':
                self.login_user()

            elif choice == '3':
                self.search_projects_by_date()

            elif choice == '4':
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = MainApp()
    app.main()
