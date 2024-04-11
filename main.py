#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from  tqdm import tqdm
import re
import requests
from bs4 import BeautifulSoup 

old_projects_url = "https://vrindavansanap.github.io/projects.html"
admin_sdk_creds_path = "/Users/vrindavan/Documents/secrets/mini-projects-8a5f2-firebase-adminsdk-3vk7x-a3dd6d1410.json"

cred = credentials.Certificate(admin_sdk_creds_path)
firebase_admin.initialize_app(cred)
db = firestore.client()
response = requests.get(old_projects_url)
soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article")

for article in tqdm(articles): 

  project_obj = {}
  project_name = article.find("h3").text.strip()
  project_name = re.sub(r'\s+', ' ', project_name)
  project_desc = article.find("p").text.strip()
  project_desc = re.sub(r'\s+', ' ', project_desc)
  a_tags = article.find_all('a')
  demo_link = a_tags[0].get("href")
  source_link = a_tags[1].get("href")
  project_obj['project_name'] = project_name
  project_obj['project_desc'] = project_desc 
  project_obj['demo_link'] = demo_link 
  project_obj['source_link'] = source_link 
 
  project_ref = db.collection("projects").document(project_name)
  project_ref.set(project_obj)

  print(project_obj)
