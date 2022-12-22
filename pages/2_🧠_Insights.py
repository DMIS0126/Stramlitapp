import streamlit as st
import time
import numpy as np

import streamlit as st



st.set_page_config(page_title="TuringContent-Insights", page_icon="🧠")
st.markdown("# 🧠 Insights")



with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(0)
    st.success("Done!")
st.markdown(
    """
    ### 0️⃣ 시작

**가입 시 입력한 데이터가 DB에 없는 사용자의 데이터**를 파악하기 위해
* 설정한 기간 내 가입한 사용자들이 실행한 가장 첫 이벤트 이후 알 수 있는 정보로 없는 데이터셋 구축

해당 DB가 athena에 스냅샷 형태로 저장되어 있어 
* [Athena docs](https://docs.aws.amazon.com/athena/latest/ug/extracting-data-from-JSON.html)
* [Presto docs](https://prestodb.io/docs/current/index.html)
를 참고했다.

Athena와 Presto의 차이가 궁금해 찾아보니 다음과 같다고 한다.[(stackshare 링크)](https://stackshare.io/stackups/amazon-athena-vs-presto)
* Athena : Query S3 Using SQL
* Presto : Distributed SQL Query Engine for Big Data


---
### 1️⃣ 전개
1. 설정한 기간 내 가입한 고등학생 사용자 중에서 적어도 한 문제를 푼 사용자의 수를 조회
	* 가입 시각이 UTC 기준이라 KST로 변환하는 과정이 필요하다.
      * evnet_time이 2022-08-24 08:00:00.000000+00과 같은 timezone형식으로 되어있어 KST로 변환하기 위해 date_parse 함수를 사용하였다.
      * 만약 date_parse 함수를 사용하지 않는다면 다음과 같은 방법으로도 할 수 있다.""")
st.code('''--Athena
select 
    date_trunc('year', from_iso8601_timestamp(concat(substring(event_time, 1,10), 'T',SUBSTR(event_time, 12, 8)))) as year, 
    date_trunc('month', from_iso8601_timestamp(concat(substring(event_time, 1,10), 'T',SUBSTR(event_time, 12, 8)))) as month
from eventtable''', language='sql')
st.markdown("""	* Postgresql에서는 '2022-08-24'로 하면 date로 인식하는데 Athena에서는 cast 함수를 통한 변환이 필요하다.
	  * 나는 timestamp로 변환하여 사용했다.
    * 위의 두 가지를 합하여 다음과 같은 느낌으로 작성하였다.""")
st.code('''-- Athena 
-- UTC -> KST 변환
select 
  date_add('HOUR', 9, date_parse(substring(event_time, 1, 19), '%Y-%m-%d %H:%i:%s')) 
from eventtable
where date_add('HOUR', 9, date_parse(substring(event_time, 1, 19), '%Y-%m-%d %H:%i:%s'))  between cast('시작일시 및 시작시각' as timestamp) and cast('종료일시 및 종료시각' as timestamp) 
        ''', language='sql')
st.markdown("""* 관련 내용이 있는 문서는 다음과 같다.
        * [Athena - date_parse](https://aws.amazon.com/ko/premiumsupport/knowledge-center/query-table-athena-timestamp-empty/) 
        * [Athena - date_add](https://docs.aws.amazon.com/ko_kr/redshift/latest/dg/r_DATEADD_function.html)
2. 사용자별로 가장 첫 이벤트를 했을 때를 찾기
	* 서브쿼리를 이용하여 user_id로 group by하여 min(event_time)을 구하고, where 절을 사용하여 원본 테이블에 있는 이벤트의 user_id, event_time과 같은 것만 남겼다.
3. 찾은 가장 첫 이벤트에 대하여 사용자별 데이터 복구 및 데이터셋 구축
	* 데이터를 복구하기 위해 없는 데이터 값을 유추할 수 있는 JSON 형식의 데이터를 슬라이싱하였다.
      * 데이터별로 리스트의 개수가 일정하지 않아 정말 힘들었다.
      * 관련 내용이 있는 문서는 다음과 같다.
        * [Presto - JSON Functions and Operators](https://prestodb.io/docs/current/functions/json.html)
    * 이후 슬라이싱한 데이터를 Excel에 옮겨와 if 함수를 열심히 작성하여 요청받은 데이터셋을 구축하였다.

---
### 2️⃣ 회고
1. 위와 같은 방법으로 쿼리를 짜고 돌렸더니 조회하는데 최소 1분정도 걸렸고, BE팀원에게 들은 바로는 쿼리 한 번 돌리는데 메모리를 9.7GB나 잡아먹는다고 한다.
	* 쓸데없이 메모리를 잡아먹지 않도록 join이 최소화되도록 확인이 필요하다.
    * Athena의 특성을 이용한 쿼리인지 확인 및 최적화가 필요하다.
      * _날짜(date) 별로 파티셔닝 되어있어 date 기준으로 where 또는 group by 문은 빠르게 수행됨_
2. JSON 형식의 데이터를 자유롭게 핸들링하고 싶은데, 그렇지 못하여 같은 쿼리를 수십번 돌렸다.
	* JSON 형식에 대한 공부가 필요하다.
      * filtering, sorting하는 방법도 모르니 정말 힘들었다.
    * SQL로 JSON을 핸들링하거나 csv파일로 가져와 pandas를 이용하여 핸들링할 수 있도록 해야겠다.
      * 그런데 아직 pandas로 JSON을 핸들링하는 방법을 정확히 알지 못한다. 이 또한 공부가 필요하다.
3. 쿼리 결과를 excel로 가져와 함수를 통해 최종 데이터셋을 구축하였는데, 이 함수연산 또한 쿼리를 통해 할 수 있으면 더욱 효율적일 것 같다.)


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