from flask import Flask, url_for, request, redirect, render_template
import pyperclip
import json
import time
from pathlib import Path
app = Flask(__name__)

file = "passwords.txt"
pathFile = Path("passwords.txt")
if pathFile.is_file():
    open(file, "r+")
    passwordsFile = json.load(open(file))
else:
    open(file, "w+")
    passwordsFile = {}
@app.route("/", methods=['GET', 'POST'])
def masterPassword():
    data = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['masterPass'] != '123456':
            data = 'Invalid login info, try again'
        else:
            return redirect(url_for('password_Locker'))
    return render_template('login.html', data=data)

@app.route("/menu", methods=["GET", "POST"])
def password_Locker():
    return render_template("main.html")

@app.route("/find_pass", methods=["GET", "POST"])
def passFinder():
    data = 'error'
    userFindPass = request.form.get('userFindPass')
    if userFindPass in passwordsFile.keys():
        passEncrypted = passwordsFile[userFindPass]
        pyperclip.copy(decode(passEncrypted))
        time.sleep(10)
    data = 'success'
    return render_template("find_pass.html", data=data)
@app.route("/update_pass", methods=["GET", "POST"])
def passUpdate():
    data = 'error'
    acc_name_update = request.form.get('acc_name_update')
    if acc_name_update in passwordsFile.keys():
        #newpass = input("Enter new password: ")
        new_pass = request.form.get('new_pass')
        passwordsFile[acc_name_update] = encode(new_pass)
        json.dump(passwordsFile, open(file, "w"))
    data = 'success'
        #print("New Password Saved")

    return render_template("update_pass.html")

@app.route("/delete_pass", methods=['GET', 'POST'])
def passDelete():
    data = None
    del_acc_name = request.form.get('del_acc_name')
    if del_acc_name in passwordsFile.keys():
        passwordsFile.pop(del_acc_name)
        json.dump(passwordsFile, open(file, "w"))
    else:
        data = 'Account does not exist'
    return render_template('delete_pass.html')

def decode(passEncrypted):
    decodedPass = []
    for i in range(len(passEncrypted)):
        decodePass = chr(ord(passEncrypted[i]) + len(passEncrypted))
        decodedPass.append(decodePass)
    passDecoded = "".join(decodedPass)
    return passDecoded

@app.route("/save_pass", methods=["GET", "POST"])
def passSave():
    data = 'error'
    acc_name = request.form.get('acc_name')
    save_acc_pass = request.form.get('save_acc_pass')
    if save_acc_pass != None:
        passwordsFile[acc_name] = encode(save_acc_pass)
        json.dump(passwordsFile, open(file, "w"))
    data = 'success'
    return render_template("save_pass.html")

def encode(save_acc_pass):
    encodedPass = []
    for i in range(len(save_acc_pass)):
        encodePass = chr(ord(save_acc_pass[i]) - len(save_acc_pass))
        encodedPass.append(encodePass)
    passEncrypted = "".join(encodedPass)
    return passEncrypted

'''
else:
   print("incorrect Password")
'''
if __name__ == '__main__':
   app.debug = True
   app.run()
