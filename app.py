import streamlit as st
import re
import pandas as pd

st.title('Convert to CSV')

uploaded_file = st.file_uploader('File upload', type='txt')

if 'stress1' not in st.session_state:
    st.session_state['stress1'] = []
if 'increment1' not in st.session_state:
    st.session_state['increment1'] = []
if 'stress2' not in st.session_state:
    st.session_state['stress2'] = []
if 'increment2' not in st.session_state:
    st.session_state['increment2'] = []
if 'nodelist' not in st.session_state:
    st.session_state['nodelist'] = []
if 'stress' not in st.session_state:
    st.session_state['stress'] = []

if st.button('Show input result'):
    text = uploaded_file.readlines()[2:]
    text_line = []
    for i in range(0, len(text)):
        text_change = text[i].decode('utf-8')
        text_line.append(text_change)
    curve_max = re.sub(r'\D', '', text_line[-8])

    regex = r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
    for i in range(int(curve_max)):
        node = re.sub(r'\D', '', text_line[3+9*i])
        st.session_state['nodelist'].append(node)
        xy_1 = re.findall(regex, text_line[7+9*i])
        xy_2 = re.findall(regex, text_line[8+9*i])
        st.session_state['increment1'].append(xy_1[0])
        st.session_state['increment2'].append(xy_2[0])
        st.session_state['stress1'].append(xy_1[1])
        st.session_state['stress2'].append(xy_2[1])

st.session_state['stress']\
    = st.session_state['stress1'] + st.session_state['stress2']

node_series = pd.Series(st.session_state['nodelist'])
stress1_series = pd.Series(st.session_state['stress1'])
increment1_series = pd.Series(st.session_state['increment1'])
stress2_series = pd.Series(st.session_state['stress2'])
increment2_series = pd.Series(st.session_state['increment2'])
df = pd.DataFrame()
df['Node'] = node_series
df['Increment 1'] = increment1_series
df['Von Mises Stress 1'] = stress1_series
df['Increment 2'] = increment2_series
df['Von Mises Stress 2'] = stress2_series
st.subheader('Input result')
st.dataframe(df)


if 'order' not in st.session_state:
    st.session_state['order'] = []
if 'num' not in st.session_state:
    st.session_state['num'] = 0

for i in range(len(st.session_state['stress1'])):
    if st.button('Node = ' + str(st.session_state['nodelist'][i])
                 + ' --- Increment = ' + str(st.session_state['increment1'][i])
                 + ' --- Stress = ' + str(st.session_state['stress1'][i])
                 + ' --- (' + str(i) + ')'):
        st.session_state['num'] = i

for i in range(len(st.session_state['stress2'])):
    if st.button('Node = ' + str(st.session_state['nodelist'][i])
                 + ' --- Increment = ' + str(st.session_state['increment2'][i])
                 + ' --- Stress = ' + str(st.session_state['stress2'][i])
                 + ' --- (' + str(i) + ')'):
        st.session_state['num'] = i + len(st.session_state['stress1'])

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Add'):
        st.session_state['order'].append(st.session_state['num'])

with col2:
    if st.button('Remove'):
        st.session_state['order'].remove(st.session_state['num'])

with col3:
    if st.button('Reset'):
        st.session_state['order'] = []

stress_new\
    = [st.session_state['stress'][i] for i in st.session_state['order']]
st.write('Output preview')
st.write(stress_new)

stress_new_series = pd.Series(stress_new)

df_new = pd.DataFrame()
df_new['Von Mises Stress'] = stress_new_series


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df_new)

st.download_button('download', csv, 'out.csv')
