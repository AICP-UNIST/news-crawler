# pip setting (auto requirements freeze)

To automatically update the requirements.txt file every time you install a package using pip, you can create a shell script or batch file that wraps the pip install command and updates the requirements.txt file.

Here's how to create the script for different platforms:

# For macOS and Linux

Create a new file named `pip_install.sh` in your project's root directory with the following content:

```
#!/bin/bash
pip install "$@"
pip freeze > requirements.txt
```

Give the script execute permissions:

```
chmod +x pip_install.sh
```

Now, you can use this script to install packages and automatically update the requirements.txt file:

```
./pip_install.sh package_name
```

# For Windows

Create a new file named `pip_install.bat` in your project's root directory with the following content:

```
@echo off
pip install %*
pip freeze > requirements.txt
```

Now, you can use this script to install packages and automatically update the requirements.txt file:

```
pip_install.bat package_name
```

By using these scripts, you can ensure that your requirements.txt file is always up-to-date with the packages installed in your virtual environment. Remember to replace package_name with the actual package name you want to install when running the script.
