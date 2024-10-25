Welcome to CyberIOT: The Hub for Tech and IOT enthusiasts!

============================
============================

I will explain the project structure in folders, simplifying it for those who want to modify it.

accounts - Extends the Django authentication system. Login, signup and reset. Reset page isn't implemented.

bug - vulnerability tracking module, handles all things related to blogposts.

channel, channelaccount, video - these are the learninghub modules working together to present the youtube-like video platform in one place.

chatzone2 - Chatting application.

cyberiot - The core Django app that handles the combined settings for all the other modules.

exploits - The Vulnerability reporting module.

machina - A bit more complex than the other modules. Customized from Django machina.

mainpage  - landing page where you see all the six modules.

marketchat, marketdash, marketitem, marketcore - all the 4 marketplace modules.

media - folder that handles media resources.

notifications - notifications app that was to display notifications, not yet implement.

profiles - user's profile app, takes the data from accounts after you sign up and updates it on your profile.

settings - not implemented. I wanted features like dark mode, but they are a bit difficult and not important.

static - handles all the static files for the project.

templates - I tried to label them properly so that you can find the specific app's templates.

terms - privacy policy page, terms and conditions page.

============================
============================

Mainpage: Displays the 6 modules for the whole forum. The official landing page for the entire application.

![image](https://github.com/user-attachments/assets/0da19965-6640-4aad-8f9f-5f443d3e31bb)

**Forums:** Discuss about IoT. A mosh pit for tech nerds. Based on Django Machina, but with a unique CyberIOT twist.

![image](https://github.com/user-attachments/assets/96e0051e-a16f-4bc2-a5aa-11c2a59de634)

**IoT Marketplace:** Buy and sell gadgets. It's a tiny Amazon for IOT/tech people who want to sell their cutting-edge gadgets or do some window shopping.😄

![image](https://github.com/user-attachments/assets/10ba4f74-3a85-4118-9fb7-1131849fe679)

**LearningHub:** Watch videos about IoT. Simpler than YouTube! Upload videos and watch existing ones. Knowledge is power, and power is voltage divided by current!

![image](https://github.com/user-attachments/assets/18e9ec34-749e-4755-8dce-602e773a5ea5)

**VulnerabilitiesHub:** Found a bug? Then here's your confessional booth, a booth for white-hat hackers. "Forgive me, admin, for I have stumbled upon a zero-day exploit and I do not desire to use it for harm, so take they exploit and report it, but will I get paid?"

![image](https://github.com/user-attachments/assets/34c64e2e-0023-4616-8290-7f78ffe48979)

![image](https://github.com/user-attachments/assets/ee7f8590-fae2-46ce-9ede-f7a5d375b13f)

**Vulnerability Tracking:** Fixed IOT vulnerabilities news, part cybersecurity news, part personal blog. Read about the latest patched vulnerabilities or Bob's journey to grow the perfect digital tomato. It's a weird mix, but hey, so is IoT!

![image](https://github.com/user-attachments/assets/7bbbf659-87e9-484a-972a-120afd68d2c5)

**Chat:** Search for users, chat privately, and update your profile to show off your IoT street cred. Message other users. Make friends with fellow IoT lovers. 

![image](https://github.com/user-attachments/assets/4284c241-ca4f-4d27-95a8-a2152cd9047e)

![image](https://github.com/user-attachments/assets/1a1e97ee-84f1-495f-a09a-932c0d4fffa8)

CyberIOT: Where we connect people who connect everything else!

How to run the project:

Load your project in your preferred IDE.

![image](https://github.com/user-attachments/assets/34345679-550e-4800-b5d5-5e2fc875a23b)

Ensure you're in the project's root folder, where manage.py is located. If you're not in that folder, navigate to it with change directory command.

Try loading the project using my existing venv, and if it doesn’t automatically load into the virtual environment when you run it, delete my existing venv and create a new one.

Creating a virtual environment.

![image](https://github.com/user-attachments/assets/2d74c433-f3b5-4a2f-bd2b-9211dc864268)

You can name it as you like, eg myenv can also be python -m venv venv // python -m venv env // python -m venv my_custom_env_name (that's up to you).

Once the venv is created, it will appear over there as a folder. 

Activate the virtual environment(venv):

![image](https://github.com/user-attachments/assets/0c092e2d-4cc6-4db1-bb84-6fe357ea615c)

On MacOS and linux:

![image](https://github.com/user-attachments/assets/0ae198e2-9e41-4acd-9a3b-e36995254033)

It will reflect in your terminal.

![image](https://github.com/user-attachments/assets/55b443b6-dbdc-4811-a659-70e8ea0f06e0)

Install django on your main computer using pip:

![image](https://github.com/user-attachments/assets/7e9fe40a-729e-4a15-a071-5c3c303ee9be)

Then come back and install the requirements.txt, it will take lots of time and also if you're using pycharm, indexing can take around 10 to 20 minutes: 

![image](https://github.com/user-attachments/assets/7337d02b-dc9f-4655-a02c-9a62373b3e7e)

You don't need to do migrations, unless you've changed the tables structures:

![image](https://github.com/user-attachments/assets/25821ea9-a982-4237-af8f-64baef53d3c4)

The project has an sqlite database with migrations already done, so you don't need to setup anything else.

Optional: Create another superuser, ensure you're in venv before you create the superadmin:

![image](https://github.com/user-attachments/assets/3721d020-2315-4f2b-8145-fcdfef3c7e62)

Every user's username and password is: username, ghoster123@@# 

The database is sqlite(file-based) you don't need to install anything, django automatically supports it.

Registered users (Visit the chat app search functionality to see all users listed).

Just type their name or their email and the password in the login page.

Current's superadmin username and password is: cyberiot || ghoster123@@#@@#

NOTE: The project has some unfinished parts, like the settings page, reset password page, and a few more things like 404 pages for access control.

For pycharm users, ensure that you've configured you server properly, else the project won't work.

Ensure python is well installed and added to path on your main computer. And django is installed too. Then you can load pycharm and configure the server in settings. 

![image](https://github.com/user-attachments/assets/9c3cd3af-24d8-4b2a-a650-fdf16f7b31fd)

![image](https://github.com/user-attachments/assets/919466f2-31b8-460b-9377-50bedbb40c89)







