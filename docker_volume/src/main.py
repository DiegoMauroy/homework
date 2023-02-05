from my_library import *
import configparser

#### Main ####
if __name__ == "__main__":

    # Read config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    user_name = config['DEFAULT']['user_name']
    password = config['DEFAULT']['password']
    url_base = config['DEFAULT']['url_base']
    folder_drive_id = config['DRIVE']['id_folder_drive']

    # queries api
    url_query = 'api/currencies'
    url = 'bitcoinaverage/ticker-all-currencies/'

    # drive api
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    # verification user
    user_identified = False
    while user_identified == False:
    
        user_identified = verification_user(user_name, password)
    
    if user_identified == True: # not a necessary condition, but just to be sure

        params_url1 = {"url_base" : url_base, 
                       "url_query" : url_query, 
                       "filename" : "data/df_currency_code", 
                       "list_index_json": ["data", "currencies"], 
                       "timestamp_bool" : False, 
                       "boolean_column_name" : "altcoin", 
                       "boolean_column_bool" : False, 
                       "column_dict_name" : None, 
                       "column_dict_replace" : True,
                       "save_parquet" : True,
                       "save_sql" : True,
                       "save_csv" : True}
        params_url2 = {"url_base" : url_base, 
                       "url_query" : url, 
                       "filename" : "data/df_price", 
                       "list_index_json": [], 
                       "timestamp_bool" : True, 
                       "boolean_column_name" : None, 
                       "boolean_column_bool" : False, 
                       "column_dict_name" : "rates", 
                       "column_dict_replace" : True,
                       "save_parquet" : True,
                       "save_sql" : True,
                       "save_csv" : True}
        
        resample(creation_df_final, params_url1, params_url2, True, True, True, "data/df_final", folder_drive_id, drive, w=0, h=0, m=10)