import requests

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