from itsdangerous import URLSafeTimedSerializer
from functools import reduce

SECRET_KEY_CONFIRMATION = 'rV2426fsxwNSem15019LaB1ss30mayCddmsg999'
SECRET_KEY_RESET = 'hf7mN6123Gbz08Ghnsfdh67G34Fdvvasj90a112'

SPECIAL_CONFIRMATION_SALT = 'hsdT56NdbsaI89nMdsa66nsdSdvvzxc'
SPECIAL_RESET_SALT = 'hh72NS6324hfsn423msdl9123hsdjgk'

def generate_email_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY_CONFIRMATION)
    return serializer.dumps(email, salt=SPECIAL_CONFIRMATION_SALT)


def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY_RESET)
    return serializer.dumps(email, salt=SPECIAL_RESET_SALT)


def confirm_email_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY_CONFIRMATION)

    try:
        email = serializer.loads(token, salt=SPECIAL_CONFIRMATION_SALT, max_age=expiration)
    except:
        raise Exception("There is a problem with entered token or smth else i dont know)")
    return email


def reset_password_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY_RESET)

    try:
        email = serializer.loads(token, salt=SPECIAL_RESET_SALT, max_age=expiration)
    except:
        raise Exception("There is a problem with entered token or smth else i dont know)")
    return email

# url = 'http://127.0.0.1:5000'
#
# rul_reg = url + "/registration"
# print(rul_reg)
# lists = [1,2,3,4,5,6,7,8,9,10,11,12]
# a = list(map(lambda x: x*2, lists))
# print(a)
#
# aquarium_creatures = [
# 	{"name": "sammy", "species": "shark", "tank number": 11, "type": "fish"},
# 	{"name": "ashley", "species": "crab", "tank number": 25, "type": "shellfish"},
# 	{"name": "jo", "species": "guppy", "tank number": 18, "type": "fish"},
# 	{"name": "jackie", "species": "lobster", "tank number": 21, "type": "shellfish"},
# 	{"name": "charlie", "species": "clownfish", "tank number": 12, "type": "fish"},
# 	{"name": "olly", "species": "green turtle", "tank number": 34, "type": "turtle"}
# ]
#
# def assign_to_tank(aquarium_creatures, new_tank_number):
#     def apply(x):
#         x["tank_number"] = new_tank_number
#         return x
#     return map(apply, aquarium_creatures)
#
# assign_tanks = assign_to_tank(aquarium_creatures, 42)
# print(list(assign_tanks))
#
# base_numbers = [2, 4, 6, 8, 10]
# powers = [1, 2, 3, 4, 5]
#
# numbers_powers = list(map(pow, base_numbers, powers))
# print(numbers_powers)
#
# # Python filter() function example
# def filterdata(x):
#     if x>5:
#         return x
# # Calling function
# result = filter(filterdata,(1,2,6))
# # Displaying result
# print(list(result))
#
#
# def custom_sum(first, second):
#     return first + second
#
# result = reduce(custom_sum, base_numbers)
# print(result)
#
# Nums = [ n for n in range(1,100)]
# print(Nums)
#
# nums_2 = [n for n in Nums if n < 5]
# print(nums_2)
#
#
#
# dict_nums = {num: num**2 for num in Nums if num < 15}
# print(dict_nums)

# class roma1:
#     def __init__(self, name):
#         self.name = "Roma"
#
#     def __hash__(self):
#         return hash(self.name)
#
# class roma2:
#     def __init__(self, name):
#         self.name = "Roma"
#
#     def __hash__(self):
#         return hash(self.name)
#
# roma10 = roma1("Roma")
# roma20 = roma2("Roma")
#
# if roma10.__hash__() == roma20.__hash__():
#     print("Error: Roma", roma10.__hash__(), roma20.__hash__())
