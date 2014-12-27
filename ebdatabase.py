import os
import datetime
import ebfunc


# Keeps track of all email.
class Database:
    def __init__(self, basedir):
        self.account = basedir.strip(os.sep)

        self._basepath = basedir
        self._path = self._basepath + os.sep + 'db.dat'
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        # this is where we write the last update string
        self._versionPosition = 0

        # create file if need be
        if not os.path.exists(self._path):
            f = open(self._path, 'wb')
            f.close()

        # read in values
        self._map = {}
        with open(self._path, 'rb') as rf:
            for line in rf:
                # find last updated
                if line.startswith(':'):
                    self._versionPosition = rf.tell() - len(line)
                    continue

                (uid, p) = line.split()

                if uid in self._map:
                    print 'Corrupt database file, attempting recover.'
                else:
                    self._map[uid] = p

        if self._versionPosition == 0:
            self._updateLastUpdated()

    # returns True if the database has a Message for the specified UID
    def contains(self, uid):
        return uid in self._map

    # retrieves all Messages, sorted by uid
    def all(self):
        return (self.messageByUID(uid) for uid in sorted((uid for uid in self._map)))

    # retrieves all raw messages, sorted by uid
    def allRaw(self):
        return (self.rawMessageByUID(uid) for uid in sorted((uid for uid in self._map)))

    # returns a path for a uid
    def path(self, uid):
        struid = str(uid)

        if struid in self._map:
            return self._map[struid]

        return None

    # retrieves Message by UID
    def messageByUID(self, uid):
        struid = str(uid)

        if struid in self._map:
            return self.messageByPath(self._map[struid])

        return None

    #  retrieves Message by path
    def messageByPath(self, path):
        path = self._basepath + os.sep + path

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
        path = self._basepath + os.sep + path

        if os.path.exists(path):
            with open(path, 'rb') as rf:
                return rf.read()

        return None

    # adds a Message to the db
    def add(self, uid, path):
        if uid in self._map:
            raise Exception('Entry for UID already exists.')

        with open(self._path, 'r+b') as wf:
            # begin writing on the last updated line
            wf.seek(self._versionPosition)

            # strip path to relative
            path = os.path.relpath(path, self._basepath)

            wf.write('{} {}\n'.format(str(uid), path))

            self._versionPosition = wf.tell()

        self._updateLastUpdated()
        self._map[uid] = path

    # updates the last updated field
    def _updateLastUpdated(self):
        with open(self._path, 'r+b') as wf:
            wf.seek(self._versionPosition)
            wf.write(': last updated {}'.format(datetime.datetime.utcnow()))