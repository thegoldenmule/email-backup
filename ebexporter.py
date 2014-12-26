import argparse
import ebdatabase
import zipfile

parser = argparse.ArgumentParser(description='Exports ebackup archive as Mailbox (mbox) file.')

parser.add_argument('--input', '-i', required=True, nargs=1, type=str, help='ebackup directory to export.')
parser.add_argument('--output', '-o', required=True, nargs=1, type=str, help='File path to export to.')

args = vars(parser.parse_args())

input = args['input'][0]
output = args['output'][0]

print 'Gathering messages.'

db = ebdatabase.Database(input)
messages = db.allRaw()

print 'Writing Mailbox.'

with open(output, 'wb') as wf:
    for rawMessage in messages:
        wf.writelines(rawMessage)

print 'Mailbox written to {}.'.format(output)

print 'Compressing Mailbox.'

zippath = output + '.zip'

with zipfile.ZipFile(zippath, 'w', allowZip64=True) as z:
    z.write(output)

print 'Compressed Mailbox written to {}.'.format(zippath)