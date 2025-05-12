import models.sv_contact_form
import models.sv_user

def setup_all_db_tables():
    tables = {}
    tables['users'] = models.sv_user.setup_db() # TODO Sandra to mislim da je smisleno razbiti na users setup in product setup kot je ze anrejeno v contacts :)
    tables['contact'] = models.sv_contact_form.setup_db()
    return tables # returns all the tables that were initilized 
