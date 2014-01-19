# Random weather generator.  Gives the user a choice of climate and season
# to generate a forecast.

import random
from math import floor

clim_list = {"1":"Tropical rainforest", "2":"Desert", "3":"Temperate coastal",
             "4":"Temperate continental", "5":"Steppe", "6":"Taiga", "7":"Tundra"}

# Parameters for different climates.

# In order (from zero), the parameters are
# 0. Variability in temperature (hoping for around 2 stdev)
# 1. Windiness (rated from 1 to 10, arbitrary numbers)
# 2. Data for winter: [average high, high minus low minus 5, chance of precipitation]
# 3. Data for spring
# 4. Data for summer
# 5. Data for fall

params_trop = [5, 5, [86,7,.48], [89,8,.5], [88,7,.42], [88,8,.52]] # Singapore
params_desert = [13, 3, [68,17,.13], [85,20,.06], [106,17,.14], [89,7,.08]] # Phoenix
params_coast = [11, 2, [47,5,.59], [59,12,.47], [76,15,.16], [60,9,.42]] # Seattle
params_cont = [19, 7, [32,9,.35], [59,7,.37], [84,11,.32], [63,12,.33]] # Chicago
params_steppe = [22, 10, [37,19,.17], [58,21,.32], [87,24,.31], [61,22,.23]] # Rapid City
params_taiga = [12, 5, [-7,9,.38], [33,16,.17], [70,20,.31], [34,5,.43]] # Yellowknife
params_tundra = [26, 8, [-7,8,.15], [9,9,.17], [47,7,.29], [21,3,.39]] # Barrow

param_list = {"1":params_trop, "2":params_desert, "3":params_coast,
              "4":params_cont, "5":params_steppe, "6":params_taiga,
              "7":params_tundra}

# Function definitions

def getSeason():
    options = {"1":"spring", "2":"summer", "3":"fall", "4":"winter"}
    print("""  1. Spring
  2. Summer
  3. Fall
  4. Winter""")
    while True:
        season = input("Please select a season: ")
        if season in options:
            return options[season]
        else:
            print("Invalid option.")

def windchill(temp,windspeed):
# Wind chill is undefined for the below parameters
    if temp > 50 or windspeed < 3:
        return 0
# Formula straight from NOAA
    else:
        return temp - floor(35.74 + .6215*temp - 35.75*windspeed**0.16 + .4275*temp*windspeed**0.16)

def heatindex(temp,humid):
    if temp < 80 or humid < 40:
        return 0
    else:
# Thanks again, NOAA.
        return floor(-42.379 + 2.0490*temp + 10.1433*humid - .224755*temp*humid - 6.83783e-3*temp**2 - 5.481717e-2*humid**2 + 1.22874e-3*temp**2*humid + 8.5282e-4*temp*humid**2 - 1.99e-6*temp**2*humid**2) - temp

def forecast(climate, season):
# Climate is identified by number, while season is identified by string
    params = param_list[climate]
    if season == "spring":
        temps = params[3]
    elif season == "summer":
        temps = params[4]
    elif season == "fall":
        temps = params[5]
    else:
        temps = params[2]
# Setting a lot of variables so that this is readable.
    tempvar = params[0]
    windy = params[1]
    avghigh = temps[0]
    lowdiff = temps[1]
    precip = temps[2]
# The randomization magic starts here.
    random.seed()
# Let's assume that temperature are normally distributed.
    high = floor(random.normalvariate(avghigh, .4 * tempvar))
# Makes sure that the difference between high and low is always at least 5
    tempdiff = floor(random.normalvariate(lowdiff, .25 * tempvar))
    low = high - 5 - (0 if tempdiff < 0 else tempdiff)
# Let's make up some reasonable numbers for these other variables
    wind = floor(windy * random.uniform(0,5))
    raining = True if precip > random.random() else False
# Chances of precipitation should be expressed in multiples of 10 percent
    chanceofrain = 0 if not raining else 10 * floor(random.normalvariate(8, 2))
# It should be more humid if it is raining
    humidity = floor(100 * (random.normalvariate(.3 + precip/2, .15) if not raining else random.normalvariate(.8 + precip/4, .1)))
# Air pressure depends on temperature and humidity.  Want this to two decimal places.
    barometer = floor(100 * (29.5 + high/200 + humidity/500 + random.uniform(0,.05)))
    currently = random.randrange(low,high)
# "Feels like" temperature will come from the added effects of wind chill and heat index.
    feels = currently - windchill(currently,wind) + heatindex(currently,humidity)
    print("  Forecast for " + clim_list[str(climate)].lower() + " during " + season + ":")
    print("Current temperature: " + str(currently) + " F")
    print("Feels like: " + str(feels) + " F")
    print("Wind speed: " + str(wind) + " mph")
    print("Humidity: " + str(100 if humidity > 100 else humidity) + "%")
    print("Air pressure: " + str(barometer/100) + " in")
    print("High today: " + str(high) + " F")
    print("Low today: " + str(low) + " F")
    if raining:
        print("There is a " + str(100 if chanceofrain > 100 else chanceofrain) + "% chance of " + ("rain." if currently > 35 else "snow."))

####
# Execution begins here
####

print("Welcome to the random weather generator!")
for i in range(1,8):
    print("  " + str(i) + ". " + clim_list[str(i)])
print("Any other inputs will exit this program.")

climate = input("Please select an option: ")
if climate in {"1", "2", "3", "4", "5", "6", "7"}:
    season = getSeason()
    forecast(climate, season)
print("Thank you for using the random weather generator!")
