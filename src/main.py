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

    # queries api
    url_query = 'api/currencies'
    url = 'bitcoinaverage/ticker-all-currencies/'

    # verification user
    user_identified = False
    while user_identified == False:
    
        user_identified = verification_user(user_name, password)
    
    if user_identified == True: # not a necessary condition, but just to be sure

        resample(creation_df_final, url_base, url_query, url, w=0, h=0, m=10)