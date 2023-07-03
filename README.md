# Required Software

* Python 3.8.10 - this is not the newest but it's stable and widely supported release of python (<https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe>)
  * Make sure pip, tcl/tk and python test suite features are installed
  * Make sure to "Add python to environment variables"
* VSCode - programming environment: <https://code.visualstudio.com/download>
  * or PyCharm IDE (<https://www.jetbrains.com/pycharm/>)

# Project Structure

* `Cardiomegaly` - main folder for your app
  * `Core` - the algorithm.
  * `App` - front-end of the application.
* `Tests` - An example python test, where you can test your code.
* `Scripts` - scripts used during development (e.g. for downloading the data)
* `Data` - This is where the Data will be cached

# Setup

* run `setup.bat`
  * This will check python is installed
  * setup the python virtual environment
  * Activate virtual environment
  * Downloaded required dependencies.
* run `python Scripts\download_data.py`
  * This will download the test data. It is very large so can take many hours.
  * You can change the location this is downloaded to by defining an environment variable called `CAREER_READY_CACHE` if you want to store it outside the checkout.
  * This can also be run in VS code see [Debugging](#debugging)
* Run the example tests: `run_tests.bat`
  * This will run the unit tests
  * This batch file also enabled test code coverage. After running this batch file you can
  * This can also be run in VS code see [Debugging](#debugging)
* Run the example application: `run_app.bat`
  * This will run the application.
  * This can also be run in VS code see [Debugging](#debugging)

# VSCode

For information on Visual Studio Code see: <https://code.visualstudio.com/> and [VSCode getting started series on YouTube](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5UgiQnBfvD7XgOMKs3O_G6)

When you open this project folder in VSCode you should see a popup message saying:
"This workspace has extension recommendations" you can review the recommendations and install them. We recommend installing these as they are helpful but they are optional.

## Terminal

VSCode very conveniently has a built in terminal. You can open this from the "Terminal Menu" and selecting "New Terminal", from the terminal you can run any terminal command. Such as any of the ones listed in the [Setup](#setup).
Once you have run setup.bat once you should find that the Terminal Prompt in VS Code has the prefix `(environment)` this indicates that the terminal is configured to work with your python project's virtual environment.

## Debugging

VSCode supports interactive debugging of python applications. This projects comes with configuration to run the application, test and data downloader with the debugger.
