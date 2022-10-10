SELECT_SYNC_DATA = '''
    select key, sync_date, type from "sync-state-following" where key=%(key)s
    '''
INSERT_SYNC_DATA = '''
    insert into "sync-state-following" ("key", sync_date, type) 
    values (%(key)s, %(sync_date)s, %(type)s)
    '''
UPDATE_SYNC_DATA_DATE = '''
    update "sync-state-following" set sync_date = %(sync_date)s where key = %(key)s
    '''
