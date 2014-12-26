import time

import os

import email
from email.utils import parsedate


# writes a message to a file
def write_message(basedir, message):
    messageString = message.as_string()
    timestamp = time.gmtime(time.mktime(parsedate(message['Date'])))

    path = basedir + os.sep + str(timestamp.tm_year) + os.sep + str(timestamp.tm_mon) + os.sep + str(timestamp.tm_mday) + os.sep

    if not os.path.exists(path):
        os.makedirs(path)

    path += '{}.{}.{}'.format(str(timestamp.tm_hour), str(timestamp.tm_min), str(timestamp.tm_sec))

    index = 0
    while os.path.exists('{}_{}.message'.format(path, str(index))):
        index += 1

    path = '{}_{}.message'.format(path, str(index))

    with open(path, "wb") as wf:
        wf.write(messageString)

    return path


# Takes a message string to a message. If the message is invalid,
# returns None.
def to_message(messageString):
    message = email.message_from_string(messageString)

    if message['Date'] is None:
        return None

    date = parsedate(message['Date'])
    if date is None:
        return None

    return message