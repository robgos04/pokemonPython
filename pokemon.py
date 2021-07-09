import requests
import enquiries
import os
import json
import datetime
import glob
path = '/Users/robertgosal/Documents/pokemonPython'
statusResponse = 1

#check file exist
def checkfile():
    if os.path.isfile('./pokemondata.txt') == False:
        f = open("pokemondata.txt", "a")

#gets current time
today = datetime.datetime.today()
#changing path to current path
os.chdir(path)

for root,directories,files in os.walk(path,topdown=False):
    if "pokemondata.txt" in files:
        #this is the last modified time
        t = os.stat(os.path.join(root, "pokemondata.txt"))[8]
        filetime = datetime.datetime.fromtimestamp(t) - today

        #checking if file is more than 7 days old or not, if yes then remove them
        if filetime.days <= -7:
            f = open("pokemondata.txt", "r")
            pokemonData = f.read()
            pokemonData = json.loads(pokemonData)
            newData = []
            newData = pokemonData
            os.remove(os.path.join(root, "pokemondata.txt"))
            for x in newData:
                save_pokemon(x['name'])

#Function for Save Pokemon locally
def save_pokemon(input_pokemon):
    response = requests.get("https://pokeapi.co/api/v2/pokemon/"+input_pokemon)
    
    if response.status_code == 404:
        print("There's no this pokemon")
    else:
        namePokemon = str(response.json()['forms'][0]['name'])
        idPokemon = str(response.json()['id'])
        locationResponse = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(response.json()['id'])+"/encounters")
        checkfile()
        pokemon = []
        f = open("pokemondata.txt", "r")
        dataFromFile = f.read()
        if dataFromFile != '':
            x = json.loads(dataFromFile)
            status = 0
            checkpokemon = namePokemon
            use = 'name'
            if input_pokemon.isdigit():
                checkpokemon = idPokemon
                use = 'id'
            for y in x:
                pokemon.append(y)
                if y[use] == checkpokemon:
                    status = 1
                    break

            if status == 0:
                data = {"id":idPokemon, "name":namePokemon, "data":response.json(), "location":locationResponse.json()}
                pokemon.append(data)
                os.remove("pokemondata.txt")
                f = open("pokemondata.txt", "a")
                f.write(json.dumps(pokemon))
                f.close()
                print("You save a Pokemon: "+namePokemon)
            else:
                print("You already have "+namePokemon)
        else:
            f = open("pokemondata.txt", "a")
            data = {"id":idPokemon, "name":namePokemon, "data":response.json(), "location":locationResponse.json()}
            pokemon.append(data)
            f.write(json.dumps(pokemon))
            f.close()
            print("You save a Pokemon: "+namePokemon) 

#Function for show Pokemon data
def show_pokemon(input_pokemon):
    f = open("pokemondata.txt", "r")
    pokemonData = f.read()
    pokemonData = json.loads(pokemonData)

    status = 0
    checkPokemon = "false"
    use = 'name'
    if input_pokemon.isdigit():
        use = 'id'
    for y in pokemonData:
        if y[use] != input_pokemon:
            status += 1
        else:
            checkPokemon = "true"
            break

    if checkPokemon == "true":
        thisPokemon = pokemonData[status]['data']
        print("\nPokemon ID: "+str(thisPokemon['id']))
        print("Pokemon Name: "+str(thisPokemon['forms'][0]['name']))
        print("Pokemon Type(s):")
        for x in thisPokemon['types']:
            print("- "+str(x['type']['name']))

        print("Pokemon Encounter location(s) and method(s):")
        statusLocation = 0
        for x in pokemonData[status]['location']:
            if "kanto" in x['location_area']['name']:
                statusLocation = 1
                print("* "+str(x['location_area']['name']))
        if statusLocation == 0:
            print("-")

        print("Pokemon stats:")
        for y in thisPokemon['stats']:
            print("- "+str(y['stat']['name'])+": "+str(y['base_stat'])) 
        print("\n")

#Function Show All Stored Pokemon
def showallPokemon():
    f = open("pokemondata.txt", "r")
    pokemonData = f.read()
    pokemonData = json.loads(pokemonData)
    for x in pokemonData:
        show_pokemon(x['name'])
    

#MAIN MENU
options = ['1. Save Pokemon', '2. Search Pokemon by ID/Name', '3. Display All Pokemon Data', '4. Exit']
choice = enquiries.choose('Choose one of these options: ', options)
print(choice)

if choice == '1. Save Pokemon':
    input_pokemon = input('Enter name/ID of Pokemon: ')
    save_pokemon(input_pokemon)    
elif choice == '2. Search Pokemon by ID/Name':
    input_pokemon = input('Enter name/ID of Pokemon: ')
    checkfile()
    f = open("pokemondata.txt", "r")
    pokemonData = f.read()
    if pokemonData != '':
        pokemonData = json.loads(pokemonData)
        
        status = 0
        use = 'name'
        if input_pokemon.isdigit():
            use = 'id'
        for y in pokemonData:
            if y[use] == input_pokemon:
                status = 1
                break

        if status == 1:
            show_pokemon(input_pokemon)
        else:
            save_pokemon(input_pokemon)
            show_pokemon(input_pokemon)
    else:
        save_pokemon(input_pokemon)
        show_pokemon(input_pokemon)
elif choice == '3. Display All Pokemon Data':
    showallPokemon()
elif choice == '4. Exit':
    exit()