# How to use Inventech Analytics

## Clone the repository using git

Make sure you have git installed before the next step.

Open the console and digit the next command:

```
git clone https://github.com/jjgomezv2/InvenTech-Analytics.git
```

## Install python and pip

Before anything else, install python and pip.

## Installing The libraries

Open the folder where the project is located using the cd command after cloning. Then, digit the next command:

```
pip install -r requirements.txt
```

## Create a .env file for the openAI api key

Create a .env file in the main folder of the project "inventechanalyticsproject" called "openAI.env". Then, write the following line there, replacing the X with a valid openAI api key.

```
openAI_api_key = XXXXXXXXXX
```

## Run the local server

After installing the libraries, open the project folder in the console and digit the next command:

```
py manage.py runserver
```

or

```
python manage.py runserver
```

## Use Inventech Analytics

Access localhost to interact with Inventech Analytics. You can use the next link:

http://localhost:8000
