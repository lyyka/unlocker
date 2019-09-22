# Unlocker
Python CLI app used to find processes that are using (locking) the file. The app can unlock (kill proceses) the file, and delete it if needed.

## Prerequisites
In order to be able to run this app from the command prompt, you first need to install Python on your machine. You can download it from [here](https://www.python.org/). Also make sure to add python install directory to PATH variable.

## How to install?
When you have successfully installed python, go to this project root directory where **setup.py** is located. Open command prompt there and run the following command:
> python setup.py install

After the successful installation, the **unlocker** command will be available anywhere in Windows!

## Usage
The basic command to run the CLI is **unlocker**, and the basic usage is:
> unlocker -f=file_to_unlock.txt

## Arguments
1. **-f, --file** -> File name from your command prompt current working directory you wish to unlock/delete.
2. **-u, --unlock** -> If present, tells the script that you wish to automatically kill all processes that are locking the file.
