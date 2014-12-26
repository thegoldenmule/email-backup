import imaplib
import os
import sys
import ebfunc
import ebdatabase
import argparse


verbose = False


def disablelogs():
    verbose = False

def enablelogs():
    verbose = True

parser = argparse.ArgumentParser(description='Designed to run periodically, and backup email.')

parser.add_argument('--email', '-e', required=True, nargs=1, type=str, help='Email address, only IMAPv4 currently supported.')
parser.add_argument('--password', '-p', required=True, nargs=1, type=str, help='Account password.')
parser.add_argument('--imap', '-i', required=True, nargs=1, type=str, help='IMAP uri, eg - imap.gmail.com.')
parser.add_argument('--output', '-o', nargs=1, default='.', type=str, help='Output directory, defaults to the current directory.')
parser.add_argument('--verbose', action='store_const', const=enablelogs, default=disablelogs, help='Enables verbose logging.')

args = vars(parser.parse_args())

email = args['email'][0]
password = args['password'][0]
imap = args['imap'][0]
output = args['output'][0] + os.sep + email

ids = []

# load database
db = ebdatabase.Database(output)

# connect
mail = imaplib.IMAP4_SSL(imap)

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

if verbose:
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

            if verbose:
                print 'Added message {}.'.format(str(id))

            written += 1


with open('log.txt', 'w') as f:
    for errorMsg in errors:
        f.write(errorMsg)
        f.write('\n')

if verbose:
    print '{} new emails written.'.format(written)