from celery import Celery
import openai
import polars as pl
from pathlib import Path
import os
import random_name
import backoff
import dotenv
import time

import rethinkdb as r

rdb = r.RethinkDB()
conn = rdb.connect(host='localhost', port=28015)

dotenv.load_dotenv()

app = Celery('tasks', backend='redis://localhost:6379/0', broker='amqp://guest:guest@localhost//')


def sum2(x, y):
    return x + y


@backoff.on_exception(backoff.expo, exception=openai.error.RateLimitError)
def generate_answer(prompt: str, model: str = None):
    import random

    if model is None:
        models = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
        idx = random.randint(0, 4)
        if idx >= 1 and idx <= 2:
            pos = 1
        elif idx >= 3 and idx <= 4:
            pos = 2
        else:
            pos = 0
        model = models[pos]
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You’re a kind helpful assistant"}, {"role": "user", "content": prompt}],
        api_key=os.environ.get("OPENAI_API_KEY"),
        max_tokens=1024,
        temperature=1.0,
    )
    try:
        return response["choices"][0]["message"]["content"].strip()
    except IndexError:
        return ""

@app.task
def add_request(table_id, data):
    print('ewrwer')
    return rdb.db('meetingsBook').table(str(table_id)).insert(
        {'result': 'sxsxs1111'
         }).run(conn)


__all__ = ["add_request"]


