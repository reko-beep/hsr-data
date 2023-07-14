import data_query.hsr_database.lc_insert_db as lc_db
import data_query.hsr_database.relic_insert_db as relic_db


def create_lightcone_db():
    lc_db.create_table_primary(lc_db.db_connect("lc"))
    lc_db.create_table_level_onlevel(lc_db.db_connect("lc"))
    lc_db.create_table_skilldeschash(lc_db.db_connect("lc"))
    lc_db.insert_data_primary(lc_db.db_connect("lc"))
    lc_db.insert_data_level_onlevel(lc_db.db_connect("lc"))
    lc_db.insert_data_skill_deschash(lc_db.db_connect("lc"))


def create_relic_db():
    relic_db.create_table_primary(relic_db.db_connect("relic"))
    relic_db.create_table_main_stat(relic_db.db_connect("relic"))
    relic_db.create_table_set_bonus(relic_db.db_connect("relic"))
    relic_db.create_table_sub_stat(relic_db.db_connect("relic"))
    relic_db.insert_data_primary(relic_db.db_connect("relic"))
    relic_db.insert_data_set_bonus(relic_db.db_connect("relic"))
    relic_db.insert_data_main_stat(relic_db.db_connect("relic"))
    relic_db.insert_data_sub_stat(relic_db.db_connect("relic"))


create_relic_db()
