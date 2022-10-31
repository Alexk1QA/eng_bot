import requests
from DB import db2
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/102.0.0.0 Safari/537.36"
}


#  ----------------------------------------------------------------------#
#  ------------------------------ create DB -----------------------------#
#  ----------------------------------------------------------------------#

#


def type_used_cars():
    used_cars = db2.DB(["type_used_cars", "transport_type", "type_value", "not_need", "not_need_2"])
    used_cars.create_sm()
    transport = (requests.get(f"https://developers.ria.com/auto/categories/?api_key=0700hMiViMYsSFf6bhrG8nTK99LG9tKYEh4bwC1W", headers=headers)).json()

    for item in transport:
        used_cars.insert_data(item)

    return transport


type_used_cars()
# #
# # # типы кузова
# # body_types = db2.DB(["car_body_types", "body_type", "body_value"])
# # body_types.create_sm()
# #
# #
# # def car_body_types():
# #     transport_type = (requests.get("https://developers.ria.com/auto/categories/gearboxes?"
# #                                    "api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0", headers=headers)).json()
# #     result_bodytypes = dict()
# #     for items in transport_type:
# #         id = items["value"]
# #         bodytypes = requests.get(f"https://developers.ria.com/auto/categories/{id}/bodystyles?api_key=Mvw"
# #                                  f"yZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0", headers=headers).json()
# #         for items in bodytypes:
# #             id_bodycar = items["value"]
# #             result_bodytypes[items['name']] = id_bodycar
# #             body_types.insert_data(items)
# #     return result_bodytypes
# # #
# # #
# # print("Типы кузова : \n", car_body_types())
# # #
# # #
# #
# #
# # марки авто
# car_brands = db2.DB(["car_brand_types", "brand_type", "brand_value", "not_need", "not_need_2"])
# car_brands.create_sm()
#
#
# def car_brand():
#     transport_type = (requests.get("https://developers.ria.com/auto/categories/gearboxes?"
#                                    "api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0", headers=headers)).json()
#     result_brands = dict()
#     for items in transport_type:
#         id = items["value"]
#         brands = requests.get(f"https://developers.ria.com/auto/categories/{id}/marks?api_key=MvwyZnYWyRXWAhv4Y"
#                               f"6jox89jd50F4XAJH5UEzGR0", headers=headers).json()
#         for items in brands:
#             id_brand = items["value"]
#             result_brands[items['name']] = id_brand
#             car_brands.insert_data(items)
#     return result_brands
#
#
# print("Марки авто : \n", car_brand())
#
# #
# #
# # модели авто


def models_used_auto():
    # db2.cursor.execute(f"""SELECT * FROM type_used_cars""")
    # result = db2.cursor.fetchall()
    #
    # list_ = []
    #
    # for items in result:
    #     list_.append(dict(name=f'{items[0]}', value=f'{items[1]}'))
    #
    # print(list_)
    #
    # marka = [
    #     {"name": "Acura", "value": 98},
    #     {"name": "Aixam", "value": 2},
    #     {"name": "Alfa Romeo", "value": 3}
    # ]
    #
    # # models = (
    # #     requests.get(f"https://developers.ria.com/auto/categories/2/marks/9/models?api_key={os.getenv('API_KEY')}",
    # #                  headers=headers)).json()
    # # result_brands = dict()
    # for j in marka:
    #     for i in list_:
    #         type_ = i["value"]
    #         marka_ = j["value"]
    #         models = (requests.get(
    #             f"https://developers.ria.com/auto/categories/{type_}/marks/{marka_}/models?api_key={os.getenv('API_KEY')}",
    #             headers=headers)).json()
    #         print(f"---{models}")
    #         if len(models) != 0:


    list_ = {"name":'Яблоко', "value": 'Apple'}

    car_models = db2.DB([f"words", "rus_name", "eng_name", "", ""])
    car_models.create_sm()
    car_models.insert_data(list_)


                # db_name = j["name"].replace(" ", "_")
                # # db_name.replace(" ", "_")
                # print(db_name)
                # car_models = db2.DB([f"{db_name}", "rus_name", "eng_name", "", ""])
                # car_models.create_sm()
                # for items in models:
                #     car_models.insert_data(items)
                    # print(f"Marka : {j['name']}, Model : {items['name']}, Type : {i['name']}")


models_used_auto()

# # области
# def regions():
#     region = requests.get(f"https://developers.ria.com/auto/states?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0",
#                           headers=headers).json()
#     return region
#
#
# print("Области : \n", regions())
#
#
# # города
# def cities():
#     region = requests.get(f"https://developers.ria.com/auto/states?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0",
#                           headers=headers).json()
#     result_regions = dict()
#     for items in region:
#         region_id = items["value"]
#         region_name = items["name"]
#         city = requests.get(
#             f"https://developers.ria.com/auto/states/{region_id}/cities?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0",
#             headers=headers).json()
#         for items in city:
#             id_city = items["value"]
#             result_regions[items['name']] = id_city
#     return result_regions
#
#
# # print("Города : \n", cities())
#
#
# # типы привода
# def drive_types():
#     for items in type_used_cars():
#         transport_id = items["value"]
#         drives_type = requests.get(f"https://developers.ria.com/auto/categories/{transport_id}/driverTypes?"
#                                    f"api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0", headers=headers).json()
#         if len(drives_type) == 0:
#             return f"Привода в {items['name']} нет !"
#         else:
#             return drives_type
#
#
# print("Типы привода : \n", drive_types())
#
#
# # типы топлива
# def fuel_types():
#     fuel_type = requests.get(f"https://developers.ria.com/auto/type?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0",
#                              headers=headers).json()
#     return fuel_type
#
#
# print("Типы топлива : \n", fuel_types())
#
#
# # коробки передач
# def gearboxes():
#     for items in type_used_cars():
#         id = items["value"]
#         name = items["name"]
#         url_gearbox = f"https://developers.ria.com/auto/categories/{id}/gearboxes?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4" \
#                       f"XAJH5UEzGR0"
#         gearbox_type = requests.get(f"{url_gearbox}", headers=headers)
#         result_gearbox = gearbox_type.json()
#         if len(result_gearbox) == 0:
#             return f"Коробок передач у {name} нет!"
#         else:
#             return result_gearbox
#
#
# print("коробки передач : \n", gearboxes())
#
#
# # опции
# def options():
#     for items in type_used_cars():
#         id = items["value"]
#         name = items["name"]
#         url_options = f"https://developers.ria.com/auto/categories/{id}/options?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH" \
#                       f"5UEzGR0"
#         options_type = requests.get(f"{url_options}", headers=headers)
#         result_options = options_type.json()
#         if len(result_options) == 0:
#             return f"Коробок передач у {name} нет!"
#         else:
#             return result_options
#
#
# print("опции: \n", options())
#
#
# # цвета
# def colors():
#     url_colors = "https://developers.ria.com/auto/colors?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0"
#     colors = requests.get(f"{url_colors}", headers=headers)
#     result_colors = colors.json()
#     return result_colors
#
#
# print("цвета : \n", colors())
#
#
# # страна производитель
# def producing_country():
#     url_countries = "https://developers.ria.com/auto/countries?api_key=MvwyZnYWyRXWAhv4Y6jox89jd50F4XAJH5UEzGR0"
#     countries = requests.get(f"{url_countries}", headers=headers)
#     result_countries = countries.json()
#     return result_countries
#
#
# print("страна производитель : \n", producing_country())
