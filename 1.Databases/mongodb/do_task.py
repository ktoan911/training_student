from training_db import TrainingMongoDB
import json

training_db = TrainingMongoDB()

# task 1
def insert_one_restaurant(file_name: str):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                restaurant = json.loads(line)
                training_db.insert_one_restaurant(restaurant)
    except FileNotFoundError as e:
        print(e)

#task 2
def insert_many_restaurants(file_name: str):
    restaurants = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                restaurant = json.loads(line)
                restaurants.append(restaurant)
            training_db.insert_many_restaurants(restaurants)
    except FileNotFoundError as e:
        print(e)

#task 3
def display_all_docs(training_db : TrainingMongoDB):
    return training_db.get_restaurants({})

#task 4
def display_specific_attr(training_db : TrainingMongoDB):
    list_rest = display_all_docs(training_db)
    for rest in list_rest:
        id = 'Restaurant ID: ' + rest['restaurant_id'] if rest['restaurant_id'] else ''
        name = ' Name: ' + rest['name'] if rest['name'] else ''
        borough = ' Borough: ' + rest['borough'] if rest['borough'] else ''
        cuisine = ' Cuisine: ' + rest['cuisine']   if rest['cuisine'] else ''
        print(id + name + borough + cuisine)

#Task 6
def find_docs_with_brough(borough: str):
    query = {"borough": borough}
    return training_db.get_restaurants(query)

#Task 7
def find_five_doc_with_brough_limit(borough: str, limit: int):
    query = {"borough": borough}
    return training_db.get_restaurants_limit(query, limit)

#Task 8
def find_next_five_doc_with_brough(borough: str, skip: int, limit: int):
    query = {"borough": borough}
    return training_db.get_restaurants_skip_limit(query, skip, limit)

#Task 9 // 90
def find_greater_than_grade(gt : int):
    query = {"grades.score": {"$gt": gt}}
    return training_db.get_restaurants(query)

#Task 10 // 80-100
def find_greater_less_than_grade():
    query = {"grades.score": {"$gt": 80, "$lt": 100}}
    return training_db.get_restaurants(query)

#Task 11
def find_langtitude_score():
    query = {
        "cuisine": {"$ne": "American"},
        "score": {"$gt": 70},
        "address.coord.0": {"$lt": -65.754168}  #latitude
    }
    return training_db.get_restaurants(query)

#Task 12
def find_borough_cuisine():
    query = {
        "borough": "Bronx",
        "cuisine": {"$in": ["American", "Chinese"]}  
    }
    return training_db.get_restaurants(query)

#Task 13
def find_restaurant_borough():
    query = {
        "borough": {"$in": ["Staten Island", "Queens", "Bronx", "Brooklyn"]}
    }
    list_rest = training_db.get_restaurants(query)
    for rest in list_rest:
        id = 'Restaurant ID: ' + rest['restaurant_id'] if rest['restaurant_id'] else ''
        name = ' Name: ' + rest['name'] if rest['name'] else ''
        borough = ' Borough: ' + rest['borough'] if rest['borough'] else ''
        cuisine = ' Cuisine: ' + rest['cuisine']   if rest['cuisine'] else ''
        print(id + name + borough + cuisine)

#Task 14
def find_restaurant_not_in_borough():
    query = {
        "borough": {"$nin": ["Staten Island", "Queens", "Bronx", "Brooklyn"]}
    }
    list_rest = training_db.get_restaurants(query)
    for rest in list_rest:
        id = 'Restaurant ID: ' + rest['restaurant_id'] if rest['restaurant_id'] else ''
        name = ' Name: ' + rest['name'] if rest['name'] else ''
        borough = ' Borough: ' + rest['borough'] if rest['borough'] else ''
        cuisine = ' Cuisine: ' + rest['cuisine']   if rest['cuisine'] else ''
        print(id + name + borough + cuisine)

#Task 15
def find_restaurant_coord():
    query = {
        "address.coord.1": {"$gt": 42, "$lt": 52}
    }
    list_rest = training_db.get_restaurants(query)
    for rest in list_rest:
        id = 'Restaurant ID: ' + rest['restaurant_id'] if rest['restaurant_id'] else ''
        name = ' Name: ' + rest['name'] if rest['name'] else ''
        borough = ' Borough: ' + rest['borough'] if rest['borough'] else ''
        cuisine = ' Cuisine: ' + rest['cuisine']   if rest['cuisine'] else ''
        print(id + name + borough + cuisine)

#Task 16
def check_have_street():
    query = {
        "address.street": {"$exists": False}
    }
    return False if len(list(training_db.get_restaurants(query))) > 0 else True

#Task 17
def update_grades_restaurant():
    _filter = {"restaurant_id": "00000001"}
    update_operation = {"$set": {"grades": "Five Star"}}
    training_db.update_many_restaurants(_filter, update_operation)

#Task 18
def update_borough_restaurant():
    _filter = {"borough": "Hai Ba Trung"}
    update_operation = {"$set": {"borough": "Hanoi"}}
    training_db.update_many_restaurants(_filter, update_operation)

#Task 19
def delete_restaurant_id(id: str):
    training_db.delete_one_restaurant(id)

#Task 20
def delete_restaurant_borough(borough: str):
    training_db.delete_many_restaurants_brough(borough)


if __name__ == '__main__':
    pass
    #insert_many_restaurants(r"D:\Training_A\TrainingStudents\1.Databases\mongodb\restaurants_import.json")
    # temp = find_borough_cuisine()
    # cnt = 0
    # for doc in temp:
    #     cnt += 1
    # print(cnt)


    
    
    

   
