#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Modules externes
import os
import re
import logging
import csv
import json
from chardet import detect

#Modules maison
from Alma_Apis_Interface import Alma_Apis_Users
from logs import logs

SERVICE = "Modification_PrimId_en_masse"

LOGS_LEVEL = 'DEBUG'
LOGS_DIR = os.getenv('LOGS_PATH')


FILE_NAME = 'test'
IN_FILE = '/media/sf_Partage_LouxBox/{}.csv'.format(FILE_NAME)
# IN_FILE = './test.csv'



#Init logger
logs.init_logs(LOGS_DIR,SERVICE,LOGS_LEVEL)
log_module = logging.getLogger(SERVICE)


# get file encoding type
def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def change_user_prim_id(barcode,newprimId):
    institutions_list = ['NETWORK','UB','UBM','IEP','INP','BXSA']
    # institutions_list = ['NETWORK','UB','BXSA']
    for institution in institutions_list :
        api_key = os.getenv("PROD_{}_USER_API".format(institution))
        api = Alma_Apis_Users.AlmaUsers(apikey=api_key, region='EU', service='test')
        status, user = api.get_user(barcode,user_id_type='BARCODE',user_view='brief',accept='json')
        if status == "Success":
            user['primary_id'] = new_prim_id
            status_update,result_update = api.update_user(barcode,
                                                        "user_group,job_category,pin_number,preferred_language,campus_code,rs_libraries,user_title,library_notices",
                                                        json.dumps(user),
                                                        accept='json',
                                                        content_type='json')
            if status_update == "Success":
                log_module.info("{} :: {} :: Succes :: Traitement du lecteur réussi".format(barcode,institution))
            else :
                log_module.info("{} :: {} :: Error :: {}".format(barcode,institution,user))

        elif status == "Error" :
            log_module.info("{} :: {} :: Error :: {}".format(barcode,institution,user))

  
log_module.info("DEBUT DU TRAITEMENT")
###Ouverture du fichier
# ###################### 
from_codec = get_encoding_type(IN_FILE)
with open(IN_FILE, 'r', encoding=from_codec, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    log_module.info("Fichier {} ouvert avec succés".format(IN_FILE))
    headers = next(reader)
    # We read the file
    for row in reader:
        if len(row) < 2:
            continue
        barcode = row[0]
        new_prim_id = row[1]
        log_module.info("Traitement du CB {}".format(barcode))
        change_user_prim_id(barcode,new_prim_id)
        # log_module.info("{} :: Succes :: L'exemplaire est maintenant rattaché à la Holding {}".format(barcode,new_holding_id))
log_module.info("FIN DU DEPLACEMENT DES EXEMPLAIRES")

log_module.info("FIN DU TRAITEMENT")

                    