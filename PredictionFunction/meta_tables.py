from PredictionFunction.PredictionFiles.LosTacos.bergen import (
    location_function as bergen_function,
)
from PredictionFunction.PredictionFiles.LosTacos.fredrikstad import (
    location_function as fredrikstad_function,
)
from PredictionFunction.PredictionFiles.LosTacos.karl_johan import (
    location_function as karl_johan_function,
)
from PredictionFunction.PredictionFiles.LosTacos.oslo_city import (
    location_function as oslo_city_function,
)
from PredictionFunction.PredictionFiles.LosTacos.oslo_lokka import (
    location_function as oslo_lokka_function,
)
from PredictionFunction.PredictionFiles.LosTacos.oslo_smestad import (
    location_function as oslo_smestad_function,
)
from PredictionFunction.PredictionFiles.LosTacos.oslo_steenstrom import (
    location_function as oslo_steenstrom_function,
)
from PredictionFunction.PredictionFiles.LosTacos.oslo_storo import (
    location_function as oslo_storo_function,
)
from PredictionFunction.PredictionFiles.LosTacos.oslo_torggata import (
    location_function as oslo_torggata_function,
)
from PredictionFunction.PredictionFiles.LosTacos.sandnes import (
    location_function as sandnes_function,
)
from PredictionFunction.PredictionFiles.LosTacos.stavanger import (
    location_function as stavanger_function,
)
from PredictionFunction.PredictionFiles.Fisketorget.fisketorget_restaurant import (
    location_function as restaurant_function,
)
from PredictionFunction.PredictionFiles.Fisketorget.fisketorget_utsalg import (
    location_function as fisketorget_utsalg_function,
)
from PredictionFunction.PredictionFiles.LosTacos.trondheim import (
    location_function as trondheim_function,
)
from PredictionFunction.PredictionFiles.Burgerheim.asane_storesenter import(
    location_function as asane_storesenter_function
)
from PredictionFunction.PredictionFiles.LosTacos.Alexander import(
    location_function as alexander_function
)
from PredictionFunction.PredictionFiles.LosTacos.bjorvika import(
    location_function as bjorvika_function
)
from PredictionFunction.PredictionFiles.Broker.restaurantdrift import(
    location_function as restaurantdrift_function
)
# from PredictionFunction.PredictionFiles.yips.pedersgata_restaurant import(
#     location_function as pedersgata_restaurant_function
# )
# from PredictionFunction.PredictionFiles.yips.pedersgata_take_away import(
#     location_function as pedersgata_takeaway_function
# )


# This is a datatable showing which city each restaurant locations is in
data = [
    {"Restaurant": "Oslo Storo", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Oslo City", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Oslo Torggata", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Karl Johan", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Fredrikstad", "City": "Fredrikstad", "Company": "Los Tacos"},
    {"Restaurant": "Oslo Lokka", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Stavanger", "City": "Stavanger", "Company": "Los Tacos"},
    {"Restaurant": "Bergen", "City": "Bergen", "Company": "Los Tacos"},
    {"Restaurant": "Oslo Steen_Strom", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Oslo Smestad", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Sandnes", "City": "Stavanger", "Company": "Los Tacos"},
    {"Restaurant": "Alexander Kielland", "City": "Oslo", "Company": "Los Tacos"},
    {"Restaurant": "Bjørvika", "City": "Oslo", "Company": "Los Tacos"},
    # {
    #     "Restaurant": "Restaurant",
    #     "City": "Stavanger",
    #     "Company": "Fisketorget",
    #     "Parent Restaurant": "Fisketorget Stavanger",
    # },
    # {
    #     "Restaurant": "Fisketorget Utsalg",
    #     "City": "Stavanger",
    #     "Company": "Fisketorget",
    #     "Parent Restaurant": "Fisketorget Stavanger",
    # },
    {
        "Restaurant": "Trondheim",
        "City": "Trondheim",
        "Company": "Los Tacos",
        "Alcohol Reference": "Karl Johan",
        "Food Reference": "Stavanger",
        "Alcohol City": "Oslo",
        "Food City": "Stavanger",
    },
    # {
    #     "Restaurant": "Åsane Storsenter",
    #     "City": "Asane",
    #     "Company": "Burgerheim",
    #     "Parent Restaurant": "",
    # },
    {
        "Restaurant": "Restaurantdrift AS",
        "City": "Oslo",
        "Company": "The Broker",
        "Parent Restaurant": "",
    },
    # {"Restaurant": "Pedersgata Restaurant", "City": "Stavanger", "Company": "Yips"},
    # {"Restaurant": "Pedersgata Take-away", "City": "Stavanger", "Company": "Yips"},
]
location_specific_dictionary = {
    "Stavanger": stavanger_function,
    "Bergen": bergen_function,
    "Fredrikstad": fredrikstad_function,
    "Oslo Lokka": oslo_lokka_function,
    "Oslo Smestad": oslo_smestad_function,
    "Oslo Torggata": oslo_torggata_function,
    "Oslo Storo": oslo_storo_function,
    "Oslo City": oslo_city_function,
    "Oslo Steen_Strom": oslo_steenstrom_function,
    "Karl Johan": karl_johan_function,
    "Sandnes": sandnes_function,
    "Restaurant": restaurant_function,
    "Fisketorget Utsalg": fisketorget_utsalg_function,
    "Trondheim": trondheim_function,
    "Åsane Storsenter":asane_storesenter_function,
    "Alexander Kielland":alexander_function,
    "Bjørvika":bjorvika_function,
    "Restaurantdrift AS":restaurantdrift_function
    # "Pedersgata Restaurant": pedersgata_restaurant_function,
    # "Pedersgata Take-away": pedersgata_takeaway_function
}
# OBS! for Drammen and Fredrikstad i had trouble finding good weather data, so used Oslo
weather_locations = {
    "Stavanger": {"source_id": "SN44560", "lat": "58.969976", "lon": "5.733107"},
    "Bergen": {"source_id": "SN50540", "lat": "60.391263", "lon": "5.322054"},
    "Fredrikstad": {"source_id": "SN18700", "lat": "59.913868", "lon": "10.752245"},
    # "Drammen": {"source_id": "SN18700", "lat": "59.913868", "lon": "10.752245"},
    "Oslo": {"source_id": "SN18700", "lat": "59.913868", "lon": "10.752245"},
    "Trondheim": {"source_id": "SN68860", "lat": "63.4107", "lon": "10.4538"},
}
