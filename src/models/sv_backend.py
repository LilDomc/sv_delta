import models.sv_contact_form
import models.sv_user
import models.sv_products
import models.sv_kosarica
import models.sv_qa

def setup_all_db_tables():
    tables = {}
    tables['users'] = models.sv_user.setup_db() # TODO Sandra to mislim da je smisleno razbiti na users setup in product setup kot je ze anrejeno v contacts :)
    tables['contact'] = models.sv_contact_form.setup_db()
    tables['products'] = models.sv_products.setup_db()
    tables['kosarica'] = models.sv_kosarica.setup_db()
    tables['qa'] = models.sv_qa.setup_db()

    return tables # returns all the tables that were initilized 
