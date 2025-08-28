import os
import datetime
import pytz

POSTS_DIR = 'content/news/'

def prompt_for_input(prompt, default=""):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default

current_date = datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%dT%H:%M:%S%z")

title = prompt_for_input("Enter the title of the post", "")
date = current_date
draft = prompt_for_input("Is this a draft? (true/false)", "true")
tags = prompt_for_input("Enter the tags (comma separated)", "").split(",")
#categories = prompt_for_input("Enter the categories (comma separated)", "").split(",")

tags_list = ', '.join(['"{}"'.format(t.strip()) for t in tags if t.strip()])
categories_list = ', '.join(['"{}"'.format(c.strip()) for c in locals().get('categories', []) if c.strip()])

front_matter = f"""---
title: "{title}"
date: {date}
draft: {draft}
tags: [{tags_list}]
#categories: [{categories_list}]
---
"""

print("\nEnter the body of the post (type 'exit' to finish):")
body = ""
while True:
    line = input()
    if line.strip().lower() == 'exit':
        break
    body += line + "\n"

post_content = front_matter + "\n" + body

file_name = f"{title.lower().replace(' ', '-')}.md"
post_path = os.path.join(POSTS_DIR, file_name)

os.makedirs(POSTS_DIR, exist_ok=True)
with open(post_path, 'w') as post_file:
    post_file.write(post_content)

print(f"\nNew post created: {post_path}")

