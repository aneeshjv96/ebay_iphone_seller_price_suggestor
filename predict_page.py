from pyexpat import model
import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('ebay_pickle.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor_loaded = data['model']
le_screensize = data['le_screensize']
le_storage_capacity = data['le_storage_capacity']
le_camera_resolution = data['le_camera_resolution']
le_model_name = data['le_model_name']
le_lock_status = data['le_lock_status']
le_condition = data['le_condition']

def show_predict_page():
    st.title('iPhone seller price suggestor app')

    st.write("""## Input the details of your phone""")
    st.write("""### - Made by Vinayak Aneesh! using ebay scraped data""")

    screensize = (

        6.1, 4.7, 5.8, 5.5, 6.5, 4.0, 6.7, 5.4, 3.5, 0.0
    )

    storage_capacity = (

        0.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0
    )
    model_name = (
        'NA',
        'XR',
        '8',
        '11',
        '7',
        'XS',
        '11 Pro',
        'X',
        '11 Pro Max',
        '6s',
        '8 Plus',
        '6',
        'SE (2nd Generation)',
        'SE',
        '7 Plus',
        'XS Max',
        '12',
        '6s Plus',
        '12 Pro',
        '12 Pro Max',
        '12 mini',
        '5s',
        '13 Pro Max',
        '6 Plus',
        '13 Pro',
        '5',
        '5c',
        '13',
        '(1st Generation)',
        '13 mini')

    camera_resolution = (

        12.0, 0.0, 8.0
    )
    lock_status = (
        '0', 'Factory Unlocked', 'Network Unlocked',
       'Network Locked', 'Unlocked', 'Fully Unlocked'
    )

    condition = (
        'NA',
        'Used: An item that has been used previously. The item may have some signs of cosmetic wear, but is ...  Read moreabout the conditionUsed: An item that has been used previously. The item may have some signs of cosmetic wear, but is fully operational and functions as intended. This item may be a floor model or store return that has been used. See the seller’s listing for full details and description of any imperfections. See all condition definitionsopens in a new window or tab ',
        'For parts or not working: An item that does not function as intended and is not fully operational. ...  Read moreabout the conditionFor parts or not working: An item that does not function as intended and is not fully operational. This includes items that are defective in ways that render them difficult to use, items that require service or repair, or items missing essential components. See the seller’s listing for full details. See all condition definitionsopens in a new window or tab '
        )



    screensize = st.selectbox('Screen Size (0 if unknown)', screensize)
    storage_capacity = st.selectbox("Storage Capacity", storage_capacity)
    camera_resolution = st.selectbox("Camera Resolution in MP", camera_resolution)
    model_name  = st.selectbox("Model Name - select from dropdown menu", model_name)
    lock_status = st.selectbox("Locked / Unlocked status - 0 if unknown", lock_status)
    condition = st.selectbox("Condition of phone (NA - New)", condition)

    ok = st.button("Calculate price of phone")
    
    if ok:

        X = np.array([[screensize, storage_capacity, camera_resolution, model_name, lock_status, condition ]])

        print('test')
        X[:,3] = le_model_name.transform(X[:,3])
        X[:,4] = le_lock_status.transform(X[:,4])
        X[:,5] = le_condition.transform(X[:,5])
        
        #X = X.astype(float)

        price = regressor_loaded.predict(X)
        base = 50

        final_price = base* np.round(price/base)

        percentage = 0.075

        low_limit = np.round(final_price*(1-percentage),0)
        upper_limit = np.round(final_price*(1+percentage),0)

        st.write(f"The estimated range for selling can be between:")
        st.subheader(f'${low_limit[0]}')
        st.write(f'and')
        st.subheader(f'${upper_limit[0]}')
        st.subheader(f'------------------------------------')
        st.write('For your iPhone 📱')
        