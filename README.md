# To-Do Web Application

To-Do Web Application uses a Flask back-end coupled with MongoDB for storing To-Dos of all users. Mulitple routes are used on the backend to communicate with MongoDB and render templates for each endpoint. I took a minimalist route when it came to styling, but I do love the colored backgrounds!

Side-note: MongoDB is used to keep track of all users To-Dos - Make sure MongoDB is installed on device

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Screenshots](#screenshots)
    - [Index](#index)
    - [Sign-Up](#sign-up)
    - [Dashboard](#dashboard)
    - [About](#about)
- [License](#license)

## Installation

To run the Remote Work Cafes locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Orangeliquid/To-Do-Web-App.git
   cd To-Do-Web-App
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure MongoDB is installed(Feel free to use MongoDBCompass to view the database)

2. Start the Flask application:
   ```bash
   python main.py
   ```
   
3. Open your web browser and navigate to http://127.0.0.1:5002/.

4. Create a profile on the Sign Up endpoint
   
5. Add To-Dos | Delete To-Dos | Mark To-Dos Finished

## Features

- Responsive index, about, header, footer, and dashboard.
- Multi profile sign up capabilites via MongoDB
- To-Dos are saved and deleted uniquely for all users
- Hashed passwords and dashboard denial for non-authenticated users

## Screenshots

### Index

![To-Do-Index](https://github.com/Orangeliquid/To-Do-Web-App/assets/127478612/d4ff86a4-f260-4224-bcf6-50e1ee124d7d)

### Sign Up

![To-Do-Register](https://github.com/Orangeliquid/To-Do-Web-App/assets/127478612/a859f997-4bce-4988-93e3-458bf5544420)

### Dashboard

![To-Do-Dashboard](https://github.com/Orangeliquid/To-Do-Web-App/assets/127478612/a7cb125c-19e4-4481-9da8-34231e81e8f0)

### About

![To-Do-About](https://github.com/Orangeliquid/To-Do-Web-App/assets/127478612/388df7f9-320d-459b-8529-e92868d512a5)

## License

This project is licensed under the [MIT License](LICENSE.txt).
