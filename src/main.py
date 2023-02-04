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

    # verification user
    user_identified = False
    while user_identified == False:
    
        user_identified = verification_user(user_name, password)
    
    if user_identified == True: # not a necessary condition, but just to be sure

        # call api and recover data "currencies"
        status_currencies, data_currency_code = make_request(url_base, url_query)

        # check connection api
        if status_currencies != 200:

            print("Error API")
