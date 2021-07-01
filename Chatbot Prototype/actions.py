from typing import Any, Text, Dict,Union, List ## Datatypes

from rasa_sdk import Action, Tracker  ##
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionReverted, FollowupAction
import requests
import time
import re
import json
import pandas as pd


class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        camera = tracker.get_slot('camera')
        ram = tracker.get_slot('RAM')
        battery = tracker.get_slot('battery')

        dispatcher.utter_message(text='Here are your search results')
        dispatcher.utter_message(text='The features you entered: ' + str(camera) + ", " + str(ram) + ", " + str(battery))
        return []
########################

class ActionShowLatestNews(Action):

    def name(self) -> Text:
        return "action_show_latest_news"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        dispatcher.utter_message(text='Here the latest news for your category')
        dispatcher.utter_message(template='utter_select_next')
        return []

class ProductSearchForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "product_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('category') == 'phone':
            return ["ram","battery","camera","budget"]
        elif tracker.get_slot('category') == 'laptop':
            return ["ram","battery_backup","storage_capacity","budget"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {"ram":[self.from_text()],
        "camera":[self.from_text()],
        "battery":[self.from_text()],
        "budget":[self.from_text()],
        "battery_backup":[self.from_text()],
        "storage_capacity":[self.from_text()]
        }


    def validate_battery_backup(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            battery_backup_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_backup_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_backup_int < 50:
            return {"battery_backup":battery_backup_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery_backup")

            return {"battery_backup":None}

    def validate_storage_capacity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            storage_capacity_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            storage_capacity_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if storage_capacity_int < 2000:
            return {"storage_capacity":storage_capacity_int}
        else:
            dispatcher.utter_message(template="utter_wrong_storage_capacity")

            return {"storage_capacity":None}

    def validate_ram(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            ram_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            ram_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if ram_int < 50:
            return {"ram":ram_int}
        else:
            dispatcher.utter_message(template="utter_wrong_ram")

            return {"ram":None}

    def validate_camera(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            camera_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            camera_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if camera_int < 150:
            return {"camera":camera_int}
        else:
            dispatcher.utter_message(template="utter_wrong_camera")

            return {"camera":None}

    def validate_budget(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # i want the ram
        try:
            budget_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            budget_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if budget_int < 450000:
            return {"budget":budget_int}
        else:
            dispatcher.utter_message(template="utter_wrong_budget")

            return {"budget":None}

    def validate_battery(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            battery_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_int < 8000:
            return {"battery":battery_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery")

            return {"battery":None}


    
    # USED FOR DOCS: do not rename without updating in docs
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot('category') == 'phone':
            ram =tracker.get_slot('ram')
            camera =tracker.get_slot('camera')
            battery=tracker.get_slot('battery')
            budget =tracker.get_slot('budget')

            df = pd.read_csv('./files/phones_02.csv', encoding='latin1')

            df['ram'] = pd.to_numeric(df['ram'])
            df['back_camera_megapixel'] = pd.to_numeric(df['back_camera_megapixel'])
            df['price_usd'] = pd.to_numeric(df['price_usd'])
            df['battery_mah'] = pd.to_numeric(df['battery_mah'])


            record = df[(df['ram'] >= ram) & (df['back_camera_megapixel'] == camera) & (df['battery_mah'] >= battery) & (df['price_usd'] <= budget)]

            if len(record['ram']) != 0:
                text = 'Please find your searched items here.........\n'
                for indices, row in record.iterrows():
                    _ram = row['ram']
                    _camera = row['back_camera_megapixel']
                    _battery = row['battery_mah']
                    _price = row['price_usd']
                    _product_name = row['product_name']
                    _url = row['product_url']
                    _rating = row['user_rating']

                    text = 'Mobile: {}  \nPrice: {}PKR \nRating: {} \nLink:{}   \n'.format(_product_name, _price,_rating ,_url )
                    # print(text)
                    dispatcher.utter_message(text)
            else:
                text = 'No Match Found\nSorry for inconvinence'
                dispatcher.utter_message(text)
        #     f = open('./files/myJson.json', encoding = 'UTF-8') 
        #     data = json.load(f)
        #     # print(data[1:5])
        #     # oem =''
        #     # model = ''
        #     # memory_iternal =''
        #     # battery = ''
        #     def getPhones():
        #         text = 'Please find your searched items here.........\n'
        #         for i in range(1,10678):
        #             try:
        #                 if '4000' in (re.findall(r'[0-9]+', data[i]['battery'])) and '{}GB '.format(ram) in data[i]['memory_internal']  and '{} MP'.format(camera) in data[i]['main_camera_single']:
        #                     oem = data[i]['oem']
        #                     model = data[i]['model']
        #                     memory_iternal = data[i]['memory_internal']
        #                     battery = data[i]['battery']
        #                     main_camera_single = data[i]['main_camera_single']
        #                     body_weight = data[i]['body_weight']
        #                     display_type = data[i]['display_type']

        #                     text = text + 'Mobile: {}  {} \nSpecs: {}  {}  {}  {}  {} \n'.format(oem, model, memory_iternal, battery,main_camera_single,body_weight,display_type) 
        #             except():
        #                 print('Error')
        #         return text
            
        #     dispatcher.utter_message(getPhones())
        #     # dispatcher.utter_message(text="""Please find your searched items here......... Phones..\nFilters: \nRam: {} GB     Camera: {} MP\nBattery: {} mah      Budget: {}$ """.format(ram, camera, battery, budget))
        #     f.close()
        # elif tracker.get_slot('category') == 'laptop':
        #     ram =tracker.get_slot('ram')
        #     storage_capacity =tracker.get_slot('storage_capacity')
        #     battery_backup=tracker.get_slot('battery_backup')
        #     budget =tracker.get_slot('budget')
        #     dispatcher.utter_message(text="""Please find your searched items here......... Laptops..\nFilters: \nRam: {} GB     Storage: {} GB/TB\nBattery Time: {} hours      Budget: {}$""".format(ram, storage_capacity, battery_backup, budget))
        # dispatcher.utter_message(text="""Please find your searched items here......... Phones..\nFilters: \nRam: {} GB     Camera: {} MP\nBattery: {} mah      Budget: {}$ """.format(ram, camera, battery, budget))
            # f.close()
        # elif tracker.get_slot('category') == 'laptop':
        #     ram =tracker.get_slot('ram')
        #     storage_capacity =tracker.get_slot('storage_capacity')
        #     battery_backup=tracker.get_slot('battery_backup')
        #     budget =tracker.get_slot('budget')
        #     dispatcher.utter_message(text="""Please find your searched items here......... Laptops..\nFilters: \nRam: {} GB     Storage: {} GB/TB\nBattery Time: {} hours      Budget: {}$""".format(ram, storage_capacity, battery_backup, budget))

        dispatcher.utter_message(template='utter_select_next')

        return [SlotSet('ram',None),SlotSet('camera',None),SlotSet('battery_backup',None),
        SlotSet('battery',None),SlotSet('storage_capacity',None),SlotSet('budget',None)]

class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_fallback")

        return []

class YourResidence(Action):

    def name(self) -> Text:
        return "action_your_residence"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        dispatcher.utter_message(template="utter_residence")

        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]


class ActionCheckWeather(Action):

    def name(self)-> Text:
        return "action_get_weather"
    
    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message.get('text')
        message = message.lower()
        loc = ''
        cities = open('./files/cities.txt','r', encoding="utf8")
        for city in cities:
            count = message.find(city.strip().lower())   
            if count >=0:
                loc = city[:-1]
                print(loc)
                break

        # tracker.slots['location'] = loc
        api_key = 'ea97f7b2410b9e80ef6dfe1d8764a3a2'
        # loc = tracker.get_slot('location')
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(loc, api_key)).json()
        print(current)
        country = current['sys']['country']
        city = current['name']
        condition = current['weather'][0]['main']
        temperature_c = current['main']['temp']
        humidity = current['main']['humidity']
        wind_mph = current['wind']['speed']
        response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        dispatcher.utter_message(response)
        
        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name')), SlotSet('location', loc)]


class ActionGetTime(Action):

    def name(self)-> Text:
        return "action_get_time"
    
    def run(self, dispatcher, tracker, domain):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        response = """The current time is {}""".format(current_time)
        dispatcher.utter_message(response)
        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]


class ActionGetJoke(Action):

    def name(self) -> Text:
        return "action_get_joke"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_joke")

        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]


class ActionCovidDetails(Action):

    def name(self)-> Text:
        return "action_covid_details"
    
    def run(self, dispatcher, tracker, domain):
        Country = ''
        NewConfirmed = ''
        TotalConfirmed = ''
        NewDeaths = ''
        TotalDeaths = ''
        NewRecovered = ''
        TotalRecovered = ''
        Date = ''

        message = tracker.latest_message.get('text')
        message = message.lower()
        usr_country = ''
        country_file = open('./files/countries.txt','r', encoding="utf8")
        for item in country_file:
            count = message.find(item.strip().lower())   
            if count >=0:
                usr_country = item[:-1].capitalize() 
                break
        # tracker.slots['country'] = usr_country
        print(usr_country)

        if usr_country == '':
            dispatcher.utter_message(template = 'utter_country_not_found')
            return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]

        url = "https://api.covid19api.com/summary"
        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)
        for index in range(1,len(parsed['Countries'])):
            if (parsed['Countries'][index]['Country']== usr_country):
                Country = parsed['Countries'][index]['Country']
                NewConfirmed = parsed['Countries'][index]['NewConfirmed']
                TotalConfirmed = parsed['Countries'][index]['TotalConfirmed']
                NewDeaths = parsed['Countries'][index]['NewDeaths']
                TotalDeaths = parsed['Countries'][index]['TotalDeaths']
                NewRecovered = parsed['Countries'][index]['NewRecovered']
                TotalRecovered = parsed['Countries'][index]['TotalRecovered']
                Date = parsed['Countries'][index]['Date']
                break

        response = """ The Total New Confirmed cases in {} on {} are {} which makes the total count to {} whereas, \nnew death are {} which makes the total death count {}. There are indeed postive news {} patients recovered today making total recovery count to {}""".format(Country,Date[:-10],NewConfirmed,TotalConfirmed,NewDeaths,TotalDeaths,NewRecovered,TotalRecovered)
        dispatcher.utter_message(response)
        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name')), SlotSet('country',usr_country)]

class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_Goodbye"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_goodbye")

        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]

class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_usbSearch"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_csv('./files/usb_data.csv')
        text = 'Please find your searched items here.....\n'

        for indices, row in df.iterrows():
            _Details = row['Product Details']
            _Brand = row['Brand']
            _Price = float(row['Price'][1:])
            _Price = int(_Price * 156.85)
            _Url = row['Link']
            _Rating = row['Ratings']

            text =  'Brand: {} \nPrice: {}PKR \nUser Rating: {}  \nDeatils: {} \nLink: {}'.format(_Brand, _Price,_Rating ,_Details ,_Url)
            dispatcher.utter_message(text)
        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]


class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_sdSearch"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_csv('./files/sd card data.csv')
        text = 'Please find your searched items here.....\n'

        for indices, row in df.iterrows():
            _Details = row['Product Details']
            _Brand = row['Brand']
            _Price = float(row['Price'][1:])
            _Price = int(_Price * 156.85)
            _Url = row['Link']
            _Rating = row['Ratings']

            text =  'Brand: {} \nPrice: {}PKR \nUser Rating: {}  \nDeatils: {} \nLink: {}'.format(_Brand, _Price,_Rating ,_Details ,_Url)
            dispatcher.utter_message(text)
        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]