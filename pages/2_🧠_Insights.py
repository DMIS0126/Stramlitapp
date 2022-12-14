import streamlit as st
import time
import numpy as np

import streamlit as st



st.set_page_config(page_title="TuringContent-Insights", page_icon="๐ง ")
st.markdown("# ๐ง  Insights")



with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(0)
    st.success("Done!")
st.markdown(
    """
    ### 0๏ธโฃ ์์

**๊ฐ์ ์ ์๋ ฅํ ๋ฐ์ดํฐ๊ฐ DB์ ์๋ ์ฌ์ฉ์์ ๋ฐ์ดํฐ**๋ฅผ ํ์ํ๊ธฐ ์ํด
* ์ค์ ํ ๊ธฐ๊ฐ ๋ด ๊ฐ์ํ ์ฌ์ฉ์๋ค์ด ์คํํ ๊ฐ์ฅ ์ฒซ ์ด๋ฒคํธ ์ดํ ์ ์ ์๋ ์ ๋ณด๋ก ์๋ ๋ฐ์ดํฐ์ ๊ตฌ์ถ

ํด๋น DB๊ฐ athena์ ์ค๋์ท ํํ๋ก ์ ์ฅ๋์ด ์์ด 
* [Athena docs](https://docs.aws.amazon.com/athena/latest/ug/extracting-data-from-JSON.html)
* [Presto docs](https://prestodb.io/docs/current/index.html)
๋ฅผ ์ฐธ๊ณ ํ๋ค.

Athena์ Presto์ ์ฐจ์ด๊ฐ ๊ถ๊ธํด ์ฐพ์๋ณด๋ ๋ค์๊ณผ ๊ฐ๋ค๊ณ  ํ๋ค.[(stackshare ๋งํฌ)](https://stackshare.io/stackups/amazon-athena-vs-presto)
* Athena : Query S3 Using SQL
* Presto : Distributed SQL Query Engine for Big Data


---
### 1๏ธโฃ ์ ๊ฐ
1. ์ค์ ํ ๊ธฐ๊ฐ ๋ด ๊ฐ์ํ ๊ณ ๋ฑํ์ ์ฌ์ฉ์ ์ค์์ ์ ์ด๋ ํ ๋ฌธ์ ๋ฅผ ํผ ์ฌ์ฉ์์ ์๋ฅผ ์กฐํ
	* ๊ฐ์ ์๊ฐ์ด UTC ๊ธฐ์ค์ด๋ผ KST๋ก ๋ณํํ๋ ๊ณผ์ ์ด ํ์ํ๋ค.
      * evnet_time์ด 2022-08-24 08:00:00.000000+00๊ณผ ๊ฐ์ timezoneํ์์ผ๋ก ๋์ด์์ด KST๋ก ๋ณํํ๊ธฐ ์ํด date_parse ํจ์๋ฅผ ์ฌ์ฉํ์๋ค.
      * ๋ง์ฝ date_parse ํจ์๋ฅผ ์ฌ์ฉํ์ง ์๋๋ค๋ฉด ๋ค์๊ณผ ๊ฐ์ ๋ฐฉ๋ฒ์ผ๋ก๋ ํ  ์ ์๋ค.""")
st.code('''--Athena
select 
    date_trunc('year', from_iso8601_timestamp(concat(substring(event_time, 1,10), 'T',SUBSTR(event_time, 12, 8)))) as year, 
    date_trunc('month', from_iso8601_timestamp(concat(substring(event_time, 1,10), 'T',SUBSTR(event_time, 12, 8)))) as month
from eventtable''', language='sql')
st.markdown("""	* Postgresql์์๋ '2022-08-24'๋ก ํ๋ฉด date๋ก ์ธ์ํ๋๋ฐ Athena์์๋ cast ํจ์๋ฅผ ํตํ ๋ณํ์ด ํ์ํ๋ค.
	  * ๋๋ timestamp๋ก ๋ณํํ์ฌ ์ฌ์ฉํ๋ค.
    * ์์ ๋ ๊ฐ์ง๋ฅผ ํฉํ์ฌ ๋ค์๊ณผ ๊ฐ์ ๋๋์ผ๋ก ์์ฑํ์๋ค.""")
st.code('''-- Athena 
-- UTC -> KST ๋ณํ
select 
  date_add('HOUR', 9, date_parse(substring(event_time, 1, 19), '%Y-%m-%d %H:%i:%s')) 
from eventtable
where date_add('HOUR', 9, date_parse(substring(event_time, 1, 19), '%Y-%m-%d %H:%i:%s'))  between cast('์์์ผ์ ๋ฐ ์์์๊ฐ' as timestamp) and cast('์ข๋ฃ์ผ์ ๋ฐ ์ข๋ฃ์๊ฐ' as timestamp) 
        ''', language='sql')
st.markdown("""* ๊ด๋ จ ๋ด์ฉ์ด ์๋ ๋ฌธ์๋ ๋ค์๊ณผ ๊ฐ๋ค.
        * [Athena - date_parse](https://aws.amazon.com/ko/premiumsupport/knowledge-center/query-table-athena-timestamp-empty/) 
        * [Athena - date_add](https://docs.aws.amazon.com/ko_kr/redshift/latest/dg/r_DATEADD_function.html)
2. ์ฌ์ฉ์๋ณ๋ก ๊ฐ์ฅ ์ฒซ ์ด๋ฒคํธ๋ฅผ ํ์ ๋๋ฅผ ์ฐพ๊ธฐ
	* ์๋ธ์ฟผ๋ฆฌ๋ฅผ ์ด์ฉํ์ฌ user_id๋ก group byํ์ฌ min(event_time)์ ๊ตฌํ๊ณ , where ์ ์ ์ฌ์ฉํ์ฌ ์๋ณธ ํ์ด๋ธ์ ์๋ ์ด๋ฒคํธ์ user_id, event_time๊ณผ ๊ฐ์ ๊ฒ๋ง ๋จ๊ฒผ๋ค.
3. ์ฐพ์ ๊ฐ์ฅ ์ฒซ ์ด๋ฒคํธ์ ๋ํ์ฌ ์ฌ์ฉ์๋ณ ๋ฐ์ดํฐ ๋ณต๊ตฌ ๋ฐ ๋ฐ์ดํฐ์ ๊ตฌ์ถ
	* ๋ฐ์ดํฐ๋ฅผ ๋ณต๊ตฌํ๊ธฐ ์ํด ์๋ ๋ฐ์ดํฐ ๊ฐ์ ์ ์ถํ  ์ ์๋ JSON ํ์์ ๋ฐ์ดํฐ๋ฅผ ์ฌ๋ผ์ด์ฑํ์๋ค.
      * ๋ฐ์ดํฐ๋ณ๋ก ๋ฆฌ์คํธ์ ๊ฐ์๊ฐ ์ผ์ ํ์ง ์์ ์ ๋ง ํ๋ค์๋ค.
      * ๊ด๋ จ ๋ด์ฉ์ด ์๋ ๋ฌธ์๋ ๋ค์๊ณผ ๊ฐ๋ค.
        * [Presto - JSON Functions and Operators](https://prestodb.io/docs/current/functions/json.html)
    * ์ดํ ์ฌ๋ผ์ด์ฑํ ๋ฐ์ดํฐ๋ฅผ Excel์ ์ฎ๊ฒจ์ if ํจ์๋ฅผ ์ด์ฌํ ์์ฑํ์ฌ ์์ฒญ๋ฐ์ ๋ฐ์ดํฐ์์ ๊ตฌ์ถํ์๋ค.

---
### 2๏ธโฃ ํ๊ณ 
1. ์์ ๊ฐ์ ๋ฐฉ๋ฒ์ผ๋ก ์ฟผ๋ฆฌ๋ฅผ ์ง๊ณ  ๋๋ ธ๋๋ ์กฐํํ๋๋ฐ ์ต์ 1๋ถ์ ๋ ๊ฑธ๋ ธ๊ณ , BEํ์์๊ฒ ๋ค์ ๋ฐ๋ก๋ ์ฟผ๋ฆฌ ํ ๋ฒ ๋๋ฆฌ๋๋ฐ ๋ฉ๋ชจ๋ฆฌ๋ฅผ 9.7GB๋ ์ก์๋จน๋๋ค๊ณ  ํ๋ค.
	* ์ธ๋ฐ์์ด ๋ฉ๋ชจ๋ฆฌ๋ฅผ ์ก์๋จน์ง ์๋๋ก join์ด ์ต์ํ๋๋๋ก ํ์ธ์ด ํ์ํ๋ค.
    * Athena์ ํน์ฑ์ ์ด์ฉํ ์ฟผ๋ฆฌ์ธ์ง ํ์ธ ๋ฐ ์ต์ ํ๊ฐ ํ์ํ๋ค.
      * _๋ ์ง(date) ๋ณ๋ก ํํฐ์๋ ๋์ด์์ด date ๊ธฐ์ค์ผ๋ก where ๋๋ group by ๋ฌธ์ ๋น ๋ฅด๊ฒ ์ํ๋จ_
2. JSON ํ์์ ๋ฐ์ดํฐ๋ฅผ ์์ ๋กญ๊ฒ ํธ๋ค๋งํ๊ณ  ์ถ์๋ฐ, ๊ทธ๋ ์ง ๋ชปํ์ฌ ๊ฐ์ ์ฟผ๋ฆฌ๋ฅผ ์์ญ๋ฒ ๋๋ ธ๋ค.
	* JSON ํ์์ ๋ํ ๊ณต๋ถ๊ฐ ํ์ํ๋ค.
      * filtering, sortingํ๋ ๋ฐฉ๋ฒ๋ ๋ชจ๋ฅด๋ ์ ๋ง ํ๋ค์๋ค.
    * SQL๋ก JSON์ ํธ๋ค๋งํ๊ฑฐ๋ csvํ์ผ๋ก ๊ฐ์ ธ์ pandas๋ฅผ ์ด์ฉํ์ฌ ํธ๋ค๋งํ  ์ ์๋๋ก ํด์ผ๊ฒ ๋ค.
      * ๊ทธ๋ฐ๋ฐ ์์ง pandas๋ก JSON์ ํธ๋ค๋งํ๋ ๋ฐฉ๋ฒ์ ์ ํํ ์์ง ๋ชปํ๋ค. ์ด ๋ํ ๊ณต๋ถ๊ฐ ํ์ํ๋ค.
3. ์ฟผ๋ฆฌ ๊ฒฐ๊ณผ๋ฅผ excel๋ก ๊ฐ์ ธ์ ํจ์๋ฅผ ํตํด ์ต์ข ๋ฐ์ดํฐ์์ ๊ตฌ์ถํ์๋๋ฐ, ์ด ํจ์์ฐ์ฐ ๋ํ ์ฟผ๋ฆฌ๋ฅผ ํตํด ํ  ์ ์์ผ๋ฉด ๋์ฑ ํจ์จ์ ์ผ ๊ฒ ๊ฐ๋ค.)


    """
                )


st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")