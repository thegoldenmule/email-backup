import imaplib
import os
import sys
import ebfunc
import ebdatabase
import argparse


parser = argparse.ArgumentParser(description='For archiving email.')
parser.add_argument('email', metavar='EMAIL', type=str, help='Email address, only gmail currently supported.')
parser.add_argument('password', metavar='PASSWORD', type=str, help='Account password.')
parser.add_argument('path', metavar='PATH', type=str, help='Output directory.')

args = vars(parser.parse_args())

email = args['email']
password = args['password']
path = args['path'] + os.sep + email

ids = []

# load database
db = ebdatabase.Database(path)

# connect
mail = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    mail.login(email, password)
except:
    print sys.exc_info()[1]
    exit(1)

mail.select()
(result, data) = mail.uid('search', None, "ALL")

if result != 'OK':
    print 'Could not fetch : {} : {}'.format(result, data)
    exit()

ids = data[0].split()
errors = []
written = 0

print 'Retrieved {} headers.'.format(str(len(ids)))

while len(ids) > 0:
    id = ids.pop(0)

    if db.contains(id):
        continue

    (fetchResult, fetchData) = mail.uid('fetch', id, '(RFC822)')

    if fetchResult != 'OK':
        errorMsg = '{} fetch error : {} : {}.'.format(str(id), fetchResult, fetchData)

        print errorMsg
        errors.append(errorMsg)
    else:
        message = ebfunc.to_message(fetchData[0][1])

        if message is None:
            errorMsg = '{} parse error.'.format(str(id))

            print errorMsg
            errors.append(errorMsg)
        else:
            path = ebfunc.write_message(path, message)

            if path is not None:
                db.add(id, path)

            print 'Added message {}.'.format(str(id))

            written += 1


with open('log.txt', 'w') as f:
    for errorMsg in errors:
        f.write(errorMsg)
        f.write('\n')

print '{} new emails written.'.format(written)