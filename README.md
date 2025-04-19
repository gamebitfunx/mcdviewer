<<<<<<< HEAD
# mcd_viewer

mcd_viewer is a PlayStation 2 memory card manager for use with .mc2 files created by the PSXMemCard GEN2.

It is based on [mymc+](https://git.sr.ht/~thestr4ng3r/mymcplus) by Florian Märkl and the classic [mymc](http://www.csclub.uwaterloo.ca:11068/mymc/) utility created by Ross Ridge.

### How to build:

#### First check if PyInstaller is installed

##### How to Install PyInstaller

To install PyInstaller, follow these steps:

###### 1. Ensure Python is Installed
First, make sure you have Python installed on your computer. You can check this by running the following command in your terminal or command prompt:

```bash
python --version
```

If Python is not installed, you can download and install it from the [official Python website](https://www.python.org/downloads/).

###### 2. Install PyInstaller Using pip
Open your terminal or command prompt and enter the following command to install PyInstaller:

```bash
pip install pyinstaller
```

###### 3. Verify the Installation
After the installation is complete, you can verify that PyInstaller was installed successfully by running:

```bash
pyinstaller --version
```

###### 4. Using PyInstaller
Once installed, you can use PyInstaller to package your Python scripts. For example, the following command will package `.spec` into an executable file:

```bash
pyinstaller mcd_viewer.spec
```

###### Additional Notes
- If you encounter permission issues during installation, you can try using the `--user` option:
  ```bash
  pip install --user pyinstaller
  ```
- Ensure that your pip is up to date by running:
  ```bash
  pip install --upgrade pip
  ```

> [!NOTE]
>
> Please note thatmcd_viewer is released under the **GPLv3, not Public Domain**!
>

**Here is an overview of most features:**

Perform operations such as adding, deleting, and exporting content in the MCD.

**Menu Usage**

1. Double-click the left mouse button to open the folder
2. right-click on a file or blank space to bring up the menu.

- Add File
- Delete File
- Extract File
- Add New Folder
- Delete Folder

=======
# mcdviewer
mcd_viewer is a PlayStation 2 memory card manager for use with .mc2 files created by the PSXMemCard GEN2
>>>>>>> e3415f59060ceac2d1da32714e0c9ca5f8a19c24
