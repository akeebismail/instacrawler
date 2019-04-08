from functools import wraps
from time import sleep
import random
import re

from kibb.exceptions import RetryException


def instagram_int(string):
    return int(string.replace(',',''))

def retry(attempt=10, wait=10):
    def wrap(func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RetryException:
                if attempt > 1:
                    sleep(wait)
                    return retry(attempt - 1, wait)(func)(*args, **kwargs)
                else:
                    exc = RetryException()
                    exc.__cause__ = None
                    raise exc
        return wrapped_f
    return wrap


def randomized_sleep(average= 1):
    _min, _max = average * 1/2, average * 3/2
    sleep(random.uniform(_min, _max))


def validate_posts(dict_posts):
    '''
        The validator is to verify if the posts are fetched wrong.
        Ex. the content got messed up or duplicated.
    '''
    posts = dict_posts.values()
    contents = [post['datetime'] for post in posts]
    # assert len(set(contents)) == len(contents)
    if len(set(contents)) == len(contents):
        print('These post data should be correct.')


def get_parsed_mentions(raw_text):
    regex = re.compile(r"@([\w\.]+)")
    regex.findall(raw_text)
    return regex.findall(raw_text)


def get_parsed_hashtags(raw_text):
    regex = re.compile(r"#(\w+)")
    regex.findall(raw_text)
    return regex.findall(raw_text)