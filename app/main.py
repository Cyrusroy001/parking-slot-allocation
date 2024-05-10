from flask import Flask, render_template, jsonify, request
import requests
from utils import flatten_df
app = Flask(__name__)

# Import libs
import os
import pandas as pd

# TODO
# response = requests.get(f'https://api.thingspeak.com/channels/{channelID}/feeds.csv?api_key={readAPIKey}')
# if response.status_code != 200:
#     print("Error: Status code is not 200")
#     print(response.status_code)

# Path to the CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), 'data', 'SPSIRDATA.csv')

# declare global variables
DATA = pd.DataFrame()
try:
    # Read the CSV file
    DATA = pd.read_csv(csv_file_path)
    DATA.rename(columns={'field1': 'SlotID', 'field2': 'Availability', 'created_at': 'Timestamp'}, inplace=True)
    DATA['Timestamp'] = pd.to_datetime(DATA['Timestamp'])
    DATA = DATA.groupby('SlotID').apply(lambda x: x.loc[x['Timestamp'].idxmax()]).reset_index(drop=True)
    print("---------Cloud Data---------")
    print(DATA)
except Exception as e:
    print("error | reading data, ", e)


# Define endpoints

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
        

@app.route('/getLotData', methods=['GET'])
def get_lot_data():
    global DATA
    print("data: ", DATA)
    _res=flatten_df(DATA)
    return jsonify(_res)


@app.route('/bookSlot', methods=['POST'])
def book_slot():
    global DATA

    try:
        json_data = request.get_json()
        lot_number = json_data.get("lotNumber")

        # processing
        # Check if slot exists
        if 'IR' + lot_number in DATA['SlotID'].values:
            # Check if slot is available
            check_result = DATA[(DATA['SlotID'] == 'IR' + lot_number) & (DATA['Availability'] == 0)]
            print(check_result)
            if not check_result.empty:
                print("here")
                # Slot available, book it
                # Update table
                DATA.loc[(DATA['SlotID'] == 'IR' + lot_number) & (DATA['Availability'] == 0), 'Availability'] = 2
                response = {'success': True}
                return jsonify(response), 200
            else:
                raise Exception("Slot: ", lot_number, " is not available!")
        else:
            raise Exception("Slot: ", lot_number, " does not exist!")
    except Exception as e:
        response = {'success': False, 'message': str(e)}
        return jsonify(response), 400


if __name__ == "__main__":
    app.run(debug=True)
