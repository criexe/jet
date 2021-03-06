#!/usr/bin/python3
#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

# cx.py [OPERATION] --param=value --param=value ...

import sys
import os
import time
import platform

_version = "v0.12"
_authors = "Mustafa Aydemir"

OP     = False
PARAMS = {}

OS = platform.system().lower()

CX_USR_SHARE_PATH = "/usr/local/share/criexe"
USR_SHARE_PATH    = "/usr/local/share/criexe/jet"

CX_TMP_PATH = "/tmp/criexe"
TMP_PATH    = "/tmp/criexe/jet"

JET_UPDATE_URL = "http://criexe.com/jet/source/release/"

COLOR_RED          = '\033[91m'
COLOR_GREEN        = '\033[92m'
COLOR_YELLOW       = '\033[93m'
COLOR_LIGHT_PURPLE = '\033[94m'
COLOR_PURPLE       = '\033[95m'
COLOR_END          = '\033[0m'


# Print : RED
def color_red(string):
    return str(COLOR_RED + str(string) + COLOR_END)
    
# Print : YELLOW
def color_yellow(string):
    return str(COLOR_YELLOW + str(string) + COLOR_END)
    
# Print : GREEN.
def color_green(string):
    return str(COLOR_GREEN + str(string) + COLOR_END)



# Execute Console Command
def cmd(command):
    import subprocess
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    return str(proc.stdout.read().decode().strip())

def output(cmd_arr):
    import subprocess
    return subprocess.check_output(cmd_arr)

# Clear Console
def clear():
    if OS == "windows":
        os.system("cls")
    else:
        os.system("clear")


# Overwrite the Previous Print
def pprint(string):
    sys.stdout.write("\r" + str(string))
    sys.stdout.flush()

    
# ARGV
argv = sys.argv
argv.pop(0)

if len(argv) <= 0:
    OP = False
else:
    OP = argv[0]
    argv.pop(0)

# PARAMS
if len(argv) > 0:
    for param in argv:
        if param.find("=") != -1 and param[0] == "-" and param[1] == "-":
            
            param = param[2:]
            param = param.split("=")
            PARAMS[param[0].strip()] = param[1]
        
        elif param.find("=") == -1 and param[0] == "-" and param[1] != "-":
            
            param = param[1:]
            PARAMS[param] = True
            

# Operation
# print_yellow("Operation : ", OP)
# print_yellow("User      : ", cmd("whoami"))



class net:
    
    follow_location = True
    charset         = "iso-8859-1"
    
    def connect(self, address):
        
        if address == None:
            return False
        
        # easy_install pycurl
        # pip3 install pycurl
        import pycurl
        from io import BytesIO

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, address)
        
        if self.follow_location == True:
            c.setopt(c.FOLLOWLOCATION, True)
        
        c.setopt(c.WRITEDATA, buffer)
#         c.setopt(c.SSL_VERIFYPEER, 1)
#         c.setopt(c.SSL_VERIFYHOST, 2)
        c.perform()
        code = c.getinfo(pycurl.HTTP_CODE)
        c.close()

        body = buffer.getvalue()
        data = body.decode(self.charset)
        
        result         = {}
        result["data"] = data
        result["code"] = code
        
        return result
    
class file:
    
    def append(self, file, string):
        with open(file, "a") as f:
            f.write(str(string))

    def write(self, file, data, mode = "w"):
        with open(file, mode) as f:
            f.write(str(data))

# TODO
class email:
    
    smtp_address = False
    smtp_port    = False
    username     = False
    password     = False
    
    to      = []
    subject = False
    body    = None
    
    content_type = "html"
    charset      = "utf-8"
    
    def send(self):
        
        try:
            
            import smtplib
            from email.mime.text import MIMEText

            mail = MIMEText(self.body, self.content_type, self.charset)
            mail["From"]    = self.username
            mail["Subject"] = self.subject
            mail["To"]      = ",".join(self.to)

            mail = mail.as_string()

            s = smtplib.SMTP(self.smtp_address, self.smtp_port)
            s.starttls()
            s.login(self.username, self.password)
            s.sendmail(self.username, self.to, mail)
            
            return True

        except Exception as e:
            
            raise Exception(e)
            return False


def command_loop(cmd, sleep=None):

    if sleep == None:
        sleep = 1

    while True:
        os.system(cmd)
        time.sleep(sleep)


def install_jet():

    import importlib
    if importlib.find_loader('pycurl') ==  None:
        print(color_red("Not Found : ") + "pycurl")
        print(color_yellow("Installing : ") + "pycurl")
        os.system("pip3 install pycurl")


install_jet()
# =================================================

if OP == False:

    # Install
    install_jet()

    # Print Help Message
    clear()
    print(color_green("JET"))
    print(color_yellow("HELP MESSAGE"))

elif OP == "auto":
    
    # Auto Git Push
    if argv[0] == "push":

        while True:

            # Branch - Default : "origin master"
            if "branch" in PARAMS:
                branch = PARAMS["branch"]
            else:
                branch = "origin master"

            # Setting Sleep
            if "sleep" in PARAMS:
                sleep = PARAMS["sleep"]
            else:
                sleep = 1

            # Hold or Auto
            if "hold" in PARAMS: 
                clear()
                # Input Commit Message
                commit_msg = input(color_green("Commit Message : "))
            else:
                # Diff Files
                diff_files = output(["git", "diff", "--name-only"])
                # Commit Message (Auto Generated)
                commit_msg = str(diff_files.decode().strip().replace("\n", ", "))

            if commit_msg != "":
                # Preview Commit Message
                clear()
                print(color_yellow("Commit Message"))
                print(commit_msg)

                clear()
                print(color_yellow("Pulling..."))
                os.system("git pull " + str(branch))

                clear()
                print(color_yellow("Adding Files..."))
                os.system("git add --all")

                clear()
                print(color_yellow("Committing..."))
                os.system('git commit -m "' + str(commit_msg) + '"')

                clear()
                print(color_yellow("Pushing...")) 
                os.system("git push " + branch)

                clear()
                print(color_green("Done : ") + color_yellow(commit_msg) )
                time.sleep(sleep)            


elif OP == "loop":
    
    try:
        
        if "command" in PARAMS:
            
            # Command
            command = PARAMS["command"]

            # Sleep
            if "sleep" in PARAMS:
                sleep = PARAMS["sleep"]
            else:
                sleep = None

            command_loop(command, sleep)
                    
    except Exception as e:
        print(color_red(str(e)))

elif OP == "update":
    
    if False:
        pass
    else:

        clear()
        print(color_yellow("Updating JET..."))
        print(color_yellow("Downloading Source Codes..."))
        connect_update = net().connect(JET_UPDATE_URL + OS)
        try:
            if connect_update["code"] == 200:
                if OS == "darwin" or OS == "linux":
                    data = connect_update["data"]
                    print(color_green("Downloaded !"))
                    os.makedirs(TMP_PATH, exist_ok = True)
                    file().write(TMP_PATH + "/jet", data)
                    os.rename(TMP_PATH + "/jet", "/usr/local/bin/jet")
                    os.system("chmod 755 /usr/local/bin/jet")
                    os.system("jet")

            else:
                raise Exception("No downloadable files found")
        except Exception as e:
                print(color_red("Update Error : ") + str(e))
            

elif OP == "generate":
    
    if argv[0] == "ssh-key":
        os.system("ssh-keygen -t rsa")
        os.system("cat ~/.ssh/id_rsa.pub")

elif OP == "get":
    
    if argv[0] == "ssh-key":
        clear()
        pprint(COLOR_GREEN)
        os.system("cat ~/.ssh/id_rsa.pub")
        pprint(COLOR_END)


# jet zip output.zip /folder/path
elif OP == "zip" and argv[0] != None and argv[1] != None:

    if OS == "darwin" or OS == "linux":
        print(color_yellow("Zipping..."))
        os.system("zip -r " + argv[0] + " " + argv[1])
    elif OS == "windows":
        print(color_red("Windows is not ready !"))