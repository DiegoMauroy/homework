import requests
import pandas as pd
import schedule

#### The function returns the data generated from an API call to url_base + query_url + status of request ####
#### Data are in a dictonnary ####
def make_request(url_base, query_url):

    response = requests.get(url_base + query_url)

    if response.status_code == 200:

        data = response.json()
        return response.status_code, data

    else:

        return response.status_code, 0
    
#### The function asks for the username and password and checks if they match the username and password provided in the configuration file ####
def verification_user(user_name, password):

    user_name_input = input("Veuillez entrer votre nom d'utilisateur : ")
    password_input = input("Veuillez entrer votre mot de passe : ")

    if user_name == user_name_input and password == password_input:

        return True
    
    else:

        print("Mot de passe et/ou nom d'utilisateur incorrect(s)")
        return False
    
#### Transforms a dictionnary into a dataframe ####
def dictionnary_to_dataframe(data, transpose=True):

    df = pd.DataFrame(data)

    if transpose:
        
        df = df.T

    return df

#### Transforms a dictionary column into several columns ####
def dictonnary_to_multi_columns(df, col, replace):

    for index, row in df.iterrows():

        for ky, value in row[col].items():
            
            df.at[index, col + "_" + ky] = value
    
    if replace:

        df = df.drop([col], axis = 1)
    
    return df

#### Selects the rows of the dataframe where col == bool ####
#### col is the name of a boolean column ####
#### bool is a boolean ####
def select_in_boolean_column(df, col, bool):

    df_reduce = df[df[col] == bool]

    return df_reduce

#### Get timestamp ####
def timestamp():

    return pd.Timestamp.now(tz = "UTC")

#### Excute periodicaly the function fct ####
#### args contains the params of fct ####
#### w (week), h (hour), m (minute) are the period ####
#### only the smallest non-zero time unit is considered ####
def resample(fct, *args, w=0, h=0, m=0):

    if m != 0:

        schedule.every(m).minutes.do(fct, *args)
    
    elif h != 0:

        schedule.every(h).hours.do(fct, *args)
    
    elif w != 0:

        schedule.every(w).weeks.do(fct, *args)

    fct(*args)
    while True:

        schedule.run_pending()

#### Principal function to creat df_final ####
def creation_df_final(url_base, url_query1, url_query2):

    # call api and recover data "currencies"
    status_currencies_code, data_currency_code = make_request(url_base, url_query1)

    # check connection api
    if status_currencies_code != 200:

        print("Error API")
    
    else:

        # organize data into a dataframe
        df_currency_code = dictionnary_to_dataframe(data_currency_code["data"]["currencies"])

        # Reduce the dataset to rows where "altcoing" == False
        df_currency_code = select_in_boolean_column(df_currency_code, "altcoin", False)

        # save dataset
        df_currency_code.to_parquet("data/df_currency_code.gzip", compression='gzip')
    
    # call api and recover data "ticker-all-currencies"
    time_api_call = timestamp()
    status_price, data_price = make_request(url_base, url_query2)

    # check connection api
    if status_price != 200:

        print("Error API")
    
    else:

        # organize data into a dataframe
        df_price = dictionnary_to_dataframe(data_price)
        df_price = dictonnary_to_multi_columns(df_price, "rates", True)

        # add timestamp
        df_price["timestamp"] = time_api_call

        # save dataset
        df_price.to_parquet("data/df_price.gzip", compression='gzip')
    
    # check connection api
    if status_price != 200 or status_currencies_code != 200:

        print("Error API")

    else:

        # merge df_price and df_currency_code (inner join)
        df_final = df_currency_code.merge(df_price, left_index = True, right_index = True)

        # data quality (dtypes, number of nan in each column, duplicate rows removed)
        """
        print(df_final.dtypes)
        nbr_nan = pd.DataFrame(index = df_final.columns)
        for col in df_final.columns:

            nbr_nan.at[col, "nbr_nan"] = df_final[col].isna().sum()

        print(nbr_nan)
        df_final.drop_duplicates(inplace=True)
        """

        # define a timestamp index
        df_final["abréviation"] = df_final.index
        df_final.set_index("timestamp", inplace = True)

        # save dataset
        df_final.to_parquet("data/df_final.gzip", compression='gzip')