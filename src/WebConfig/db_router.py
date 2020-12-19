# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
DEFAULT_DB = 'default'


class KulloDbRouter(object):

    def db_for_read(self, model, **hints):
        try:
            return model.KulloMeta.db_name
        except:
            return DEFAULT_DB

    def db_for_write(self, model, **hints):
        try:
            return model.KulloMeta.db_name
        except:
            return DEFAULT_DB

    def allow_relation(self, obj1, obj2, **hints):
        db1 = DEFAULT_DB
        db2 = DEFAULT_DB

        try:
            db1 = obj1.KulloMeta.db_name
        except:
            pass
        try:
            db2 = obj2.KulloMeta.db_name
        except:
            pass

        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        try:
            return db == DEFAULT_DB
        except:
            return True
