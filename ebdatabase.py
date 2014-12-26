import os

import ebfunc


class Database:
    __version = '0.1.0'

    def __init__(self, account):
        self.account = account

        self._path = account + os.sep + 'db.dat'
        if not os.path.exists(account):
            os.makedirs(account)

        if not os.path.exists(self._path):
            with open(self._path, 'wb') as wf:
                wf.write(':version {}'.format(str(Database.__version)))

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

    def contains(self, uid):
        return uid in self._map

    def messageByUID(self, uid):
        if uid in self._map:
            return self.messageByPath(self._map[uid])

        return None

    def messageByPath(self, path):
        if os.path.exists(path):
            with open(path, 'rb') as rf:
                return ebfunc.to_message(rf.read)

        return None

    def add(self, uid, path):
        if uid in self._map:
            raise Exception('Entry for UID already exists.')

        with open(self._path, 'ab') as wf:
            # seek to the file's end
            wf.seek(0, 2)

            wf.write('\n')
            wf.write('{} {}'.format(str(uid), path))

        self._map[uid] = path