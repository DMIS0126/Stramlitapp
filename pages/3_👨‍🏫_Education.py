import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="TuringContent-Education", page_icon="👨‍🏫")
st.markdown("# 👨‍🏫 Education")


st.markdown("""# 2015 개정 교육과정 기반 성적산출 세미나

## 주관 : @gabin

## 일시 : 2022년 9월 1일

### 0️⃣ 현재 모의고사 및 수능의 수학영역 문제 구조

- 공통과목 : 22문제, 선택과목 : 8문제
- 2022년 기준 고1(2024년 수능 응시)도 선택과목으로 수학영역 응시하게 됩니다.

### 1️⃣ 백분위, 표준점수, 원점수의 관계

### 2️⃣ 여기서 질문 💁

1. 다른 선택과목을 선택한 두 학생이 같은 원점수를 받았다면, 표준점수도 같을까요?
    - 다릅니다.
        - 선택과목이 다르면 난이도가 다르기 때문에 표준점수는 달라질 수 있습니다.
2. 3월 모의고사와 6월 모의고사를 응시한 한 학생이 같은 원점수를 받았다면, 표준점수도 같을까요?
    - 다릅니다.
        - 각 모의고사의 난이도에 따라 표준점수는 달라질 수 있습니다.
3. 작년 수능 확통을 응시한 두 학생 A, B의 원점수가 96점이라면 표준점수도 같을까요?
    - 다릅니다.
        - 두 학생 모두 4점 문제 1개를 틀렸지만, A 학생이 선택과목 4점 문제를 틀리고, B 학생이 공통과목 4점 문제를 틀렸다면 표준점수는 달라질 수 있습니다.
        - 만약 두 학생 A, B가 공통과목 또는 선택과목의 4점 문제를 틀렸다면 표준점수는 같습니다.
4. 작년 수능 확통을 응시한 두 학생 A, B의 백분위가 96으로 같다면 모두 1등급이 찍혀야 하는데, A 학생은 1등급, B 학생은 2등급이 찍혔습니다. 어떻게 된 상황일까요?
    - 백분위는 소숫점 첫째자리에서 반올림합니다.
        - 따라서 A 학생이 96.4, B 학생이 95.6의 백분위를 받았다면, 위와 같은 상황이 벌어질 수 있습니다.
        - 이런 상황은 등급을 결정짓는 백분위(4, 11, 23, … )에서 일어납니다.
5. 작년 수능 A 학생은 확통, B 학생은 기하를 선택하였고, 두 학생 모두 표준점수 138점을 받았습니다. 이때 두 학생 A, B의 백분위와 등급은 같을까요?
- 같습니다.

### 3️⃣ 선택과목 시행에 따른 문제

- 확통 선택자가 최저 등급을 맞추지 못하는 상황이 빈번하게 일어납니다.
    - 미적, 기하 선택자가 수학 1, 2등급을 싹쓸이했습니다.
    - 관련 기사
        
        ![Untitled](2015%20%E1%84%80%E1%85%A2%E1%84%8C%E1%85%A5%E1%86%BC%20%E1%84%80%E1%85%AD%E1%84%8B%E1%85%B2%E1%86%A8%E1%84%80%E1%85%AA%E1%84%8C%E1%85%A5%E1%86%BC%20%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%89%E1%85%A5%E1%86%BC%E1%84%8C%E1%85%A5%E1%86%A8%E1%84%89%E1%85%A1%E1%86%AB%E1%84%8E%E1%85%AE%E1%86%AF%20%E1%84%89%E1%85%A6%E1%84%86%E1%85%B5%E1%84%82%E1%85%A1%20b4ec890cede54b0091a754b1ba55b753/Untitled.png)
        

### *️⃣ 참고자료"""

)



#
# st.markdown("# DataFrame Demo")
# st.sidebar.header("DataFrame Demo")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )
#
#
# @st.cache
# def get_UN_data():
#     AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")
#
#
# try:
#     df = get_UN_data()
#     countries = st.multiselect(
#         "Choose countries", list(df.index), ["China", "United States of America"]
#     )
#     if not countries:
#         st.error("Please select at least one country.")
#     else:
#         data = df.loc[countries]
#         data /= 1000000.0
#         st.write("### Gross Agricultural Production ($B)", data.sort_index())
#
#         data = data.T.reset_index()
#         data = pd.melt(data, id_vars=["index"]).rename(
#             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
#         )
#         chart = (
#             alt.Chart(data)
#             .mark_area(opacity=0.3)
#             .encode(
#                 x="year:T",
#                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#                 color="Region:N",
#             )
#         )
#         st.altair_chart(chart, use_container_width=True)
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )