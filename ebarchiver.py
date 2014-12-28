import ebdatabase
import argparse
import zipfile
import os

# parse command line args
parser = argparse.ArgumentParser(description='Intelligently creates/updates a zip archive.')

parser.add_argument('--input', '-i', required=True, nargs=1, type=str, help='ebackup directory to export.')
parser.add_argument('--output', '-o', required=True, nargs=1, type=str, help='File path to export to.')

args = vars(parser.parse_args())

input = args['input'][0]
output = args['output'][0]

# open db
db = ebdatabase.Database(input)

# keep compressed db in separate file
compresseddb = ebdatabase.Database(input, dbname='db.compressed.dat')

if not os.path.exists(output):
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        pass

# append new messages to archive
with zipfile.ZipFile(output, 'a', compression=zipfile.ZIP_DEFLATED) as z:
    # compare dbs and add
    dirty = False
    for uid in db.uids():
        if not compresseddb.contains(uid):
            path = db.relpath(uid)
            compresseddb.add(uid, path)

            z.writestr(path, db.rawMessageByUID(uid))

            print 'Writing uid={} to archive.'.format(str(uid))

            dirty = True