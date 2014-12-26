import os

import ebfunc


# Keeps track of all email.
class Database:
    # version string appended to db file -- not used at the moment
    __version = '0.1.0'

    def __init__(self, account):
        self.account = account.strip(os.sep)

        self._path = account + os.sep + 'db.dat'
        if not os.path.exists(account):
            os.makedirs(account)

        # create database if one doesn't exist
        if not os.path.exists(self._path):
            with open(self._path, 'wb') as wf:
                wf.write(':version {}'.format(str(Database.__version)))

        # read in values
        self._map = {}
        with open(self._path, 'rb') as rf:
            for line in rf:
                if line.split()[0] == ':version':
                    continue

                (uid, p) = line.split()

                if uid in self._map:
                    print 'Corrupt database file, attempting recover.'
                else:
                    self._map[uid] = p

    # returns True if the database has a Message for the specified UID
    def contains(self, uid):
        return uid in self._map

    # retrieves all Messages, sorted by uid
    def all(self):
        return [self.messageByUID(uid) for uid in sorted((uid for uid in self._map))]

    # retrieves all raw messages, sorted by uid
    def allRaw(self):
        return [self.rawMessageByUID(uid) for uid in sorted((uid for uid in self._map))]

    # retrieves Message by UID
    def messageByUID(self, uid):
        struid = str(uid)

        if struid in self._map:
            return self.messageByPath(self._map[struid])

        return None

    #  retrieves Message by path
    def messageByPath(self, path):
        if os.path.exists(path):
            with open(path, 'rb') as rf:
                return ebfunc.to_message(rf.read())

        return None

    # retrieves raw message by uid
    def rawMessageByUID(self, uid):
        struid = str(uid)

        if struid in self._map:
            return self.rawMessageByPath(self._map[struid])

        return None

    # retrieves raw message by path
    def rawMessageByPath(self, path):
        if os.path.exists(path):
            with open(path, 'rb') as rf:
                return rf.read()

        return None

    # adds a Message to the db
    def add(self, uid, path):
        if uid in self._map:
            raise Exception('Entry for UID already exists.')

        with open(self._path, 'ab') as wf:
            # seek to the file's end
            wf.seek(0, 2)

            wf.write('\n')
            wf.write('{} {}'.format(str(uid), path))

        self._map[uid] = path