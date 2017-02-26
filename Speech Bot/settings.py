from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def getProperty(propertyKey):
    return os.environ.get(propertyKey);
