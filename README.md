# Belajar Analisis Data dengan Python :pray:

This project is made to accomplish data analysis course in dicoding platform
This project is using python with version of 3.12.2 and run on windows OS

## How to Run Dashboard

Run all commands in powershell

### Setup Environment
```Powershell
# Make submission dir as your cwd
cd path/to/submission

# Make sure you've installed latest version pip
py -m pip install --upgrade pip

# Install the virtual environment module
pip install virtualenv

# Create virtual environment, in this case I'm using name "myvirenvi" or you can give other name like you want or like it
py -m venv myvirenvi

# Make sure your execution policy is Unrestricted or just run this command:
Set-ExecutionPolicy Unrestricted -Force

# Active virtual environment
myvirenvi\Scripts\activate

# set back cwd to submission
cd path/to/submission

# Install the required library, by:
pip install -r requirements.txt
# or:
pip install pandas matplotlib seaborn streamlit babel

```

### Run Streamlit App
```Powershell
# set dashboard as cwd
cd dashboard

# run
streamlit run dashboard.py

# quit
ctrl+c
```

### To Close Virtual Environment
```Powershell
deactivate
```
