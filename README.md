"# Team-Planner" 
Team Project Planner Tool
Overview
This Team Project Planner Tool provides a robust platform for managing project teams and tasks, utilizing a clean API to manage users, teams, and team boards. Designed for simplicity and efficiency.

Features
User Management
    Create User: Add new users to the system.
    Update User: Modify existing user details.
    Describe user: Describe user details
    List Users: Retrieve a list of all users.
    User Team: Get a user team
Team Management
    Create Team: Form new teams.
    Describe Team: Describe the teams
    Update Team: Update details of existing teams.
    Add User to Team: Add new user to the team
    Remove User from Team: Remove user from the team
    List Teams User: Get a list of all User teams.
Board and Task Management
    Create Board: Start new project boards within a team.
    Add Task: Insert tasks to a board.
    Update Task: Change details of a task.
    closed board: Closed the board.
    List Board: Display all boards.
    Export Board: Export the task details for a respective board
Technical Design
Architecture
The application is structured into modules each corresponding to a key aspect of the tool: users, teams, and boards/tasks.
Base abstract classes define the necessary API endpoints and functionalities which are then implemented by concrete classes.
Persistence
Local file storage is used to maintain simplicity and avoid external database dependencies.
Data is stored in JSON format for easy serialization and deserialization.
A dedicated db directory houses all persisted data, ensuring clean separation of concerns and ease of maintenance.
Error Handling
Comprehensive exception handling ensures that invalid inputs and errors do not crash the system but instead provide meaningful error messages.