import models.sv_contact_form
import models.sv_user
import models.sv_products
import models.sv_kosarica
import models.sv_qa
import models.sv_rate
import models.sv_poslovalnica


def setup_all_db_tables():
    tables = {}
    tables['users_and_employees'] = models.sv_user.setup_db()
    tables['contact'] = models.sv_contact_form.setup_db()
    tables['products'] = models.sv_products.setup_db()
    tables['kosarica'] = models.sv_kosarica.setup_db()
    tables['qa'] = models.sv_qa.setup_db()
    tables['rate'] = models.sv_rate.setup_db()
    tables['poslovalnice'] = models.sv_poslovalnica.setup_db()

    return tables # returns all the tables that were initilized 
