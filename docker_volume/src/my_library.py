import requests
import pandas as pd
import schedule
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#### The function returns the data generated from an API call (url_base + query_url) and status of request ####
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

#### Get data api, put data in dataframe, organize dataframe and save dataframe ####
def data_api_to_dataframe(url_base, url_query, filename, list_index_json = [], timestamp_bool = False, boolean_column_name = None, boolean_column_bool = False, column_dict_name = None, column_dict_replace = True):

    # call the api and put the data in the dictionary
    if timestamp_bool == True:
        
        time_api_call = timestamp()

    status, data = make_request(url_base, url_query)

    # check connection api
    if status != 200:

        print("Error API")
    
    else:

        # organize data into a dataframe
        for index_json in list_index_json:
            
            data = data[index_json]

        df = dictionnary_to_dataframe(data)

        # organize dataframe
        if boolean_column_name != None:
            
            df = select_in_boolean_column(df, boolean_column_name, boolean_column_bool)

        if column_dict_name != None:
            
            df = dictonnary_to_multi_columns(df, column_dict_name, column_dict_replace)

        # add timestamp
        if timestamp_bool == True:
            
            df["timestamp"] = time_api_call

        # save dataset
        df.to_parquet(filename + ".gzip", compression="gzip")
    
    return df, status

#### Merge two dataframe and save the result ####
def creation_df_final(params_url1, params_url2, filename_df_final):

    df1, status_1 = data_api_to_dataframe(params_url1["url_base"], params_url1["url_query"], params_url1["filename"], params_url1["list_index_json"], params_url1["timestamp_bool"], params_url1["boolean_column_name"], params_url1["boolean_column_bool"], params_url1["column_dict_name"], params_url1["column_dict_replace"])
    
    df2, status_2 = data_api_to_dataframe(params_url2["url_base"], params_url2["url_query"], params_url2["filename"], params_url2["list_index_json"], params_url2["timestamp_bool"], params_url2["boolean_column_name"], params_url2["boolean_column_bool"], params_url2["column_dict_name"], params_url2["column_dict_replace"])
    
    # check connection api
    if status_2 != 200 or status_1 != 200:

        print("Error API")

    else:

        # merge df_price and df_currency_code (inner join)
        df_final = df1.merge(df2, left_index = True, right_index = True)

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
        df_final.to_parquet(filename_df_final + ".gzip", compression="gzip")