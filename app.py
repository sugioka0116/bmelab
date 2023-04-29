import streamlit as st
import re
import pandas as pd

st.title('Convert to CSV')

uploaded_file = st.file_uploader('File upload', type='txt')

if 'stress' not in st.session_state:
    st.session_state['stress'] = []

if 'increment' not in st.session_state:
    st.session_state['increment'] = []

if st.button('Show input result'):
    st.session_state['stress'] = []
    st.session_state['increment'] = []
    text = uploaded_file.readlines()[2:]
    text_line = []
    for i in range(0, len(text)):
        text_change = text[i].decode('utf-8')
        text_line.append(text_change)
    curve_max = re.sub(r'\D', '', text_line[-8])

    regex = r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
    for i in range(int(curve_max)):
        xy_1 = re.findall(regex, text_line[7+9*i])
        xy_2 = re.findall(regex, text_line[8+9*i])
        st.session_state['increment'].append(xy_1[0])
        st.session_state['increment'].append(xy_2[0])
        st.session_state['stress'].append(xy_1[1])
        st.session_state['stress'].append(xy_2[1])


stress_series = pd.Series(st.session_state['stress'])
increment_series = pd.Series(st.session_state['increment'])
df = pd.DataFrame()
df['Increment'] = increment_series
df['Von Mises Stress'] = stress_series
st.subheader('Input result')
st.dataframe(df)


if 'order' not in st.session_state:
    st.session_state['order'] = []

if 'num' not in st.session_state:
    st.session_state['num'] = 0

for i in range(len(st.session_state['stress'])):
    if st.button(str(i)):
        st.session_state['num'] = i

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

st.write('Output order')
st.write(st.session_state['order'])

stress_new = [st.session_state['stress'][i] for i in st.session_state['order']]
st.write('Output preview')
st.write(stress_new)

stress_new_series = pd.Series(stress_new)

df_new = pd.DataFrame()
df_new['Von Mises Stress'] = stress_new_series


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df_new)

st.download_button('download', csv, 'out.csv')
