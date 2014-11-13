# tribe.extract
# Extracts social network data from an email mbox
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Nov 12 21:19:51 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: extract.py [] benjamin@bengfort.com $

"""
Extracts social network data from an email mbox
"""

##########################################################################
## Imports
##########################################################################

from mailbox import mbox
from datetime import datetime
from collections import Counter

##########################################################################
## MBoxReader
##########################################################################

class MBoxReader(object):

    def __init__(self, path):
        self.path  = path
        self.mbox  = mbox(path)
        self.start = None
        self.finit = None

    def __iter__(self):
        self.start = datetime.now()
        for msg in self.mbox:
            yield msg
        self.finit = datetime.now()

    def key_analysis(self):
        """
        Performs an analysis of keys in the emails
        """
        keys = Counter()
        for msg in self:
            for key in msg.keys():
                keys[key] += 1

        denom = float(len(self.mbox))
        return dict((key, (val/denom)*100) for key,val in keys.items())

    def extract(self):
        """
        Extracts the meta data from the MBox
        """
        for msg in self:

            source = msg.get('From', '').strip()
            if not source: continue

            # construct data output
            email = {
                "from": source,
                "to": [],
                "cc": [],
                "subject": msg.get('Subject', '').strip(),
                "date": msg.get('Date', '').strip(),
            }

            for to in msg.get('To', '').split(","):
                if to:
                    email['to'].append(to.strip())

            for cc in msg.get('Cc', '').split(","):
                if cc:
                    email['cc'].append(cc.strip())

            yield email

if __name__ == '__main__':
    import json
    reader = MBoxReader("fixtures/benjamin@bengfort.com.mbox")
    #print json.dumps(reader.key_analysis(), indent=2)
    with open('fixtures/links.json', 'w') as out:
        json.dump(list(reader.extract()), out)