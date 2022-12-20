import streamlit as st
st.set_page_config(page_title="TuringContent", page_icon="🏠")
def intro():
    import streamlit as st
    from PIL import Image
    image = Image.open('Untitled.png')

    col1, col2 = st.columns([1,5], gap="small")
    with col1:
        st.image(image, width=100)
    with col2:
        st.write("# 튜링 콘텐츠팀 블로그")

    st.markdown("""
    튜링 콘텐츠팀 블로그입니다.\\
    앞으로 수학, 교육, 콘텐츠 데이터와 관련된 내용을 추가할 예정입니다.\\
    많은 관심 부탁드립니다.
    """)



#
#
#     st.markdown(
#         """
#         ### 0️⃣ 시작
#
#  **가입 시 입력한 데이터가 DB에 없는 사용자의 데이터**를 파악하기 위해
# * 설정한 기간 내 가입한 사용자들이 실행한 가장 첫 이벤트 이후 알 수 있는 정보로 없는 데이터셋 구축
#
# 해당 DB가 athena에 스냅샷 형태로 저장되어 있어
# * [Athena docs](https://docs.aws.amazon.com/athena/latest/ug/extracting-data-from-JSON.html)
# * [Presto docs](https://prestodb.io/docs/current/index.html)
# 를 참고했다.
#
# Athena와 Presto의 차이가 궁금해 찾아보니 다음과 같다고 한다.[(stackshare 링크)](https://stackshare.io/stackups/amazon-athena-vs-presto)
# * Athena : Query S3 Using SQL
# * Presto : Distributed SQL Query Engine for Big Data
#
#
# ---
# ### 1️⃣ 전개
# 1. 설정한 기간 내 가입한 고등학생 사용자 중에서 적어도 한 문제를 푼 사용자의 수를 조회
# 	* 가입 시각이 UTC 기준이라 KST로 변환하는 과정이 필요하다.
#       * evnet_time이 2022-08-24 08:00:00.000000+00과 같은 timezone형식으로 되어있어 KST로 변환하기 위해 date_parse 함수를 사용하였다.
#       * 만약 date_parse 함수를 사용하지 않는다면 다음과 같은 방법으로도 할 수 있다.""")
#     st.code('''--Athena
# select
#     date_trunc('year', from_iso8601_timestamp(concat(substring(event_time, 1,10), 'T',SUBSTR(event_time, 12, 8)))) as year,
#     date_trunc('month', from_iso8601_timestamp(concat(substring(event_time, 1,10), 'T',SUBSTR(event_time, 12, 8)))) as month
# from eventtable''', language='sql')
#     st.markdown("""	* Postgresql에서는 '2022-08-24'로 하면 date로 인식하는데 Athena에서는 cast 함수를 통한 변환이 필요하다.
# 	  * 나는 timestamp로 변환하여 사용했다.
#     * 위의 두 가지를 합하여 다음과 같은 느낌으로 작성하였다.""")
#     st.code('''-- Athena
# -- UTC -> KST 변환
# select
#   date_add('HOUR', 9, date_parse(substring(event_time, 1, 19), '%Y-%m-%d %H:%i:%s'))
# from eventtable
# where date_add('HOUR', 9, date_parse(substring(event_time, 1, 19), '%Y-%m-%d %H:%i:%s'))  between cast('시작일시 및 시작시각' as timestamp) and cast('종료일시 및 종료시각' as timestamp)
#         ''', language='sql')
#     st.markdown("""* 관련 내용이 있는 문서는 다음과 같다.
#         * [Athena - date_parse](https://aws.amazon.com/ko/premiumsupport/knowledge-center/query-table-athena-timestamp-empty/)
#         * [Athena - date_add](https://docs.aws.amazon.com/ko_kr/redshift/latest/dg/r_DATEADD_function.html)
# 2. 사용자별로 가장 첫 이벤트를 했을 때를 찾기
# 	* 서브쿼리를 이용하여 user_id로 group by하여 min(event_time)을 구하고, where 절을 사용하여 원본 테이블에 있는 이벤트의 user_id, event_time과 같은 것만 남겼다.
# 3. 찾은 가장 첫 이벤트에 대하여 사용자별 데이터 복구 및 데이터셋 구축
# 	* 데이터를 복구하기 위해 없는 데이터 값을 유추할 수 있는 JSON 형식의 데이터를 슬라이싱하였다.
#       * 데이터별로 리스트의 개수가 일정하지 않아 정말 힘들었다.
#       * 관련 내용이 있는 문서는 다음과 같다.
#         * [Presto - JSON Functions and Operators](https://prestodb.io/docs/current/functions/json.html)
#     * 이후 슬라이싱한 데이터를 Excel에 옮겨와 if 함수를 열심히 작성하여 요청받은 데이터셋을 구축하였다.
#
# ---
# ### 2️⃣ 회고
# 1. 위와 같은 방법으로 쿼리를 짜고 돌렸더니 조회하는데 최소 1분정도 걸렸고, BE팀원에게 들은 바로는 쿼리 한 번 돌리는데 메모리를 9.7GB나 잡아먹는다고 한다.
# 	* 쓸데없이 메모리를 잡아먹지 않도록 join이 최소화되도록 확인이 필요하다.
#     * Athena의 특성을 이용한 쿼리인지 확인 및 최적화가 필요하다.
#       * _날짜(date) 별로 파티셔닝 되어있어 date 기준으로 where 또는 group by 문은 빠르게 수행됨_
# 2. JSON 형식의 데이터를 자유롭게 핸들링하고 싶은데, 그렇지 못하여 같은 쿼리를 수십번 돌렸다.
# 	* JSON 형식에 대한 공부가 필요하다.
#       * filtering, sorting하는 방법도 모르니 정말 힘들었다.
#     * SQL로 JSON을 핸들링하거나 csv파일로 가져와 pandas를 이용하여 핸들링할 수 있도록 해야겠다.
#       * 그런데 아직 pandas로 JSON을 핸들링하는 방법을 정확히 알지 못한다. 이 또한 공부가 필요하다.
# 3. 쿼리 결과를 excel로 가져와 함수를 통해 최종 데이터셋을 구축하였는데, 이 함수연산 또한 쿼리를 통해 할 수 있으면 더욱 효율적일 것 같다.)
#
#
#     """
#     )

def Info():
    import streamlit as st
    # import pandas as pd
    # import pydeck as pdk
    from PIL import Image
    image = Image.open('Untitled.png')


    col1, col2 = st.columns([1, 5], gap="small")
    with col1:
        st.image(image, width=100)
    with col2:
        st.write("# 튜링 콘텐츠팀 블로그")


    tab1, tab2, tab3 = st.tabs(["Info", "Vision", "Contact"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
#
#     from urllib.error import URLError
#
#     st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
#     st.write(
#         """
#         This demo shows how to use
# [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
# to display geospatial data.
# """
#     )
#
#     @st.cache
#     def from_data_file(filename):
#         url = (
#             "http://raw.githubusercontent.com/streamlit/"
#             "example-data/master/hello/v1/%s" % filename
#         )
#         return pd.read_json(url)
#
#     try:
#         ALL_LAYERS = {
#             "Bike Rentals": pdk.Layer(
#                 "HexagonLayer",
#                 data=from_data_file("bike_rental_stats.json"),
#                 get_position=["lon", "lat"],
#                 radius=200,
#                 elevation_scale=4,
#                 elevation_range=[0, 1000],
#                 extruded=True,
#             ),
#             "Bart Stop Exits": pdk.Layer(
#                 "ScatterplotLayer",
#                 data=from_data_file("bart_stop_stats.json"),
#                 get_position=["lon", "lat"],
#                 get_color=[200, 30, 0, 160],
#                 get_radius="[exits]",
#                 radius_scale=0.05,
#             ),
#             "Bart Stop Names": pdk.Layer(
#                 "TextLayer",
#                 data=from_data_file("bart_stop_stats.json"),
#                 get_position=["lon", "lat"],
#                 get_text="name",
#                 get_color=[0, 0, 0, 200],
#                 get_size=15,
#                 get_alignment_baseline="'bottom'",
#             ),
#             "Outbound Flow": pdk.Layer(
#                 "ArcLayer",
#                 data=from_data_file("bart_path_stats.json"),
#                 get_source_position=["lon", "lat"],
#                 get_target_position=["lon2", "lat2"],
#                 get_source_color=[200, 30, 0, 160],
#                 get_target_color=[200, 30, 0, 160],
#                 auto_highlight=True,
#                 width_scale=0.0001,
#                 get_width="outbound",
#                 width_min_pixels=3,
#                 width_max_pixels=30,
#             ),
#         }
#         st.sidebar.markdown("### Map Layers")
#         selected_layers = [
#             layer
#             for layer_name, layer in ALL_LAYERS.items()
#             if st.sidebar.checkbox(layer_name, True)
#         ]
#         if selected_layers:
#             st.pydeck_chart(
#                 pdk.Deck(
#                     map_style="mapbox://styles/mapbox/light-v9",
#                     initial_view_state={
#                         "latitude": 37.76,
#                         "longitude": -122.4,
#                         "zoom": 11,
#                         "pitch": 50,
#                     },
#                     layers=selected_layers,
#                 )
#             )
#         else:
#             st.error("Please choose at least one layer above.")
#     except URLError as e:
#         st.error(
#             """
#             **This demo requires internet access.**
#
#             Connection error: %s
#         """
#             % e.reason
#         )

def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
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


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
"""
    )

    @st.cache
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "안녕하세요" : intro,
    "반갑습니다": Info,
    "또와주세요": intro,
    "감사합니다": intro
}

demo_name = st.sidebar.selectbox("튜링 콘텐츠팀 블로그", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()