import API_key
import requests


# This program uses the CoinMarketCap API to fetch data regarding both cash currencies and cryptocurrencies.
# This allows the user to find out core information of any currency like exchange rates/prices, market cap
# and changes in volume/price measured in percent.


def get_currency_id(currency_one):

    # as specified by the CoinMarketCap API documentation, we need to set up parameter and header dictionaries
    # that will be passed as input for the URL request so that the API knows what currency and type of data we
    # are interested in fetching
    headers = {
        "X-CMC_PRO_API_KEY": API_key.KEY,
        "Accepts": "application/json"
    }
    parameters = {
        "symbol": [currency_one]
    }

    base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"  # url for requesting id data

    # get the id data in .json format and index for the id field
    id_data = requests.get(base_url, params=parameters, headers=headers).json()
    # index the data for the id number of the currency the user is searching for
    id_data = id_data['data'][0]['id']

    return id_data


def get_currency_data(currency_one, currency_two):

    id_number = get_currency_id(currency_one)
    id_string = str(id_number)

    headers = {
        "X-CMC_PRO_API_KEY": API_key.KEY,
        "Accepts": "application/json"
    }
    parameters = {
        "id": id_number,
        "convert": currency_two
    }

    base_url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"  # url for requesting price data

    # make the url request and fetch the currency data in .json format (effectively a python dictionary)
    currency_data = requests.get(base_url, params=parameters, headers=headers).json()
    # index the data for information regarding the specified currency the user wants to convert to
    currency_data = currency_data["data"][id_string]["quote"][currency_two]

    return currency_data


def print_currency_data(data, currency_one, currency_two):

    # loop through the data set and print the info with the correct formatting
    for key, value in data.items():
        key = key.replace("_", " ").title()
        if "Percent" in key:
            key = key.replace("Percent", "Price")
        if type(value) == float or type(value) == int:
            if "Change" in key or "Dominance" in key:
                print(f"{key} for {currency_one}: {value:,.2f}%")
            elif "Price" in key:
                print(f"{key}/Exchange Rate for {currency_one}: {currency_two} {value:,.2f}")
            else:
                print(f"{key} for {currency_one}: {currency_two} {value:,.2f}")
        else:
            print(f"{key}: {value:}")


def main():

    print()
    currency_one = input("Enter the ticker symbol (e.g: BTC) of a currency you want to know about: ").upper().strip()
    currency_two = input("Enter the ticker symbol of the currency you want to convert to: ").upper().strip()
    print()
    print(f"Price and exchange rate data for {currency_one} in terms of {currency_two}: \n")

    # make an API call to fetch the relevant data and then print it
    data = (get_currency_data(currency_one, currency_two))
    print_currency_data(data, currency_one, currency_two)

    if event_loop():
        main()


def event_loop():

    print()
    use_again = input("Do you want to find out more information about other currencies? "
                      "Enter yes or no: ").upper().strip()

    while True:
        if use_again == "YES":
            return True
        elif use_again == "NO":
            return False
        else:
            use_again = input("Invalid input, please enter either yes or no: ").upper().strip()


main()
