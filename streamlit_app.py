import streamlit as st
import pandas as pd

st.title('튜링 콘텐츠팀 블로그')

st.header('st.button')

if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')


st.write('### asdasd ')

st.write('## asdasd ')

st.write('# asdasd ')

st.write('* asdasd')


st.write('Hello, *World!* :sunglasses:')

df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })
st.write(df)

st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

import numpy as np
import altair as alt

df2 = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])
c = alt.Chart(df2).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.write(c)


st.latex(r'''
S_{n} = \displaystyle\sum_{k=1}^{n} a_k
''')