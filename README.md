# TinyGreen :teacher: :handshake: :school:
> A job board specifically designed for ESL teachers and recruiters in Korea.<br>
 Providing transparency in a niche market riddled with labor issues!

### To run project locally (*7 steps*)
#### 1. make a new directory
Create a new directory named "TinyGreen" and navigating into it.

`mkdir TinyGreen`

`cd TinyGreen`
#### 2. git clone this repository 
Use git clone to clone the repository into the newly created directory.

`git clone https://github.com/FredericGariepy/TinyGreen/.git`

#### 3. Actiate python virtual environment 
Create and activate a Python virtual environment named "venv". 

On macOS and Linux:

`python3 -m venv venv`

`source venv/bin/activate`

On Windows:

`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

*Note: this may be neccesary on your machine, the ExecutionPolicy will reset after you close the window*

`python -m venv venv`

`.\venv\Scripts\activate`

#### 4. Installing the python package from requirements.txt
You will install the required packages using the pip package manager inside your virtual environment.

`pip install -r requirements.txt`

#### 5. Initalize a SQLite databse
Use python to create a local SQLite database to interact with the project locally

`python`

```
from run import app, db
with app.app_context():
    db.create_all()
```
Press Enter, then type `exit()` and press Enter again to exit the Python interpreter.

#### 6. Making the myconfig.py file
Navigate into the "tinyGreen" project file folder and create the **myconfig.py** file..

`cd tinyGreeen`

Linux/macOS:

`touch myconfig.py`

On Windows:

`type nul > myconfig.py`

Copy & Paste into the *myconfig.py* file:

```
# myconfig.py

# Secret key for Flask session
secretkey = 'examplesecretkey123'

# Secret salt for Flask session
secretsalt = 'examplesalt123'

# Secret email username
secretemailusr = 'email@email.com'

# Secret email password
secretemailpsw = 'exampleemailpassword123'

# Secret email server
secretemailserver = 'examplemailserver123'

# Secret email port
secretmailport = 587

# Secret database URI
secretdburi = 'sqlite:///tinyGreen.db'
```
save & exit

#### 7. Run the project and open Browser with URL http://127.0.0.1:5000
You will finally run the project locally and access it through your browser!

`python run.py`

In a browser, paste into URL:

`http://127.0.0.1:5000`
