import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Math", page_icon="📖")

st.markdown("# Math")


option = st.selectbox(
    '글을 선택해주세요.',
    ('문제 생산 자동화 (2022.12.20)', '아토믹 개념 주소화 (2022.12.23)',))
if option == '문제 생산 자동화 (2022.12.20)':
    st.markdown("""
    ## 🏭문제 생산 자동화

#### 초등 수학

- **[알고리즘으로 커버 가능한 유닛 시트](https://docs.google.com/spreadsheets/d/1Oz_wXThgKzRc-s2vQvMk-ag7g6mJVo3a4aMlawctVJo/edit#gid=0)**

![](https://raw.githubusercontent.com/sharosoo-image/upload/master/images/image.png)
- **Unit D 커버 가능 기준**
  - 쎈 문제집을 기준으로 하나의 unit D에 알고리즘으로 해결 가능한 유형이 3개 이상일 때
  - 유형이 커버 가능하다는 것은 한 유형에서 적어도 하나의 문제를 코드로 작성 가능할 때
  - 그림이 필요한 유형 제외
- **최소 생성 가능 문제수**
  - 유닛 74개 x 유형 3개 x 20문제 = 4440문제
    - 유형 3개 = 한 유닛 당 평균 3개의 유형이 존재한다고 가정


#### 중학 수학

  - **[알고리즘으로 커버 가능한 유닛 시트](https://docs.google.com/spreadsheets/d/1Oz_wXThgKzRc-s2vQvMk-ag7g6mJVo3a4aMlawctVJo/edit#gid=1138368730)**

![중학수학 커버 가능 유닛](https://user-images.githubusercontent.com/98881555/183082346-be36c526-d5f3-409b-9a72-d195bbfd3703.png)

  - **Unit D 커버 가능 기준**
    - 쎈 문제집을 기준으로 하나의 unit D에 속한 유형의 절반 이상을 알고리즘으로 해결 가능할 때
    - 유형이 커버 가능하다는 것은 한 유형에서 적어도 하나의 문제를 코드로 작성 가능할 때
    - 그림이 필요한 유형 제외

  - **최소 생성 가능 문제수**
    - 유닛 76개 x 유형 5개 x 20문제 = 7600문제
      - 유형 5개 = 한 유닛 당 평균 10개의 유형이 존재하며 그 중 절반 이상의 유형을 커버 가능해야하므로 

#### 문제 자동 생성 작성 방법
  
  - **latex 형태의 문자열 작성 방법**
    - https://peps.python.org/pep-0498/
    - `f"{n}"`: 변수 n의 값이 출력된다
      - n이 10인 경우, `10`이 출력됨
    - `f"{{ n }}"`: 중괄호와 문자 n이 출력된다
      - n이 10이라도, `{n}`이 출력됨
    - `f"{{{n}}}`: 중괄호와 변수 n이 출력된다
      - n이 10인 경우, `{10}`이 출력됨
    - latex 함수 중, t나 n, b로 시작하는 경우 슬래쉬를 `\\`처럼 한번 더 입력한다.
      - `\times`라고 입력 하는 경우 `\t`가 인식 되지 않음.
      - `\\times`라고 입력한다.
""")
if option == '아토믹 개념 주소화 (2022.12.23)':
    st.write('abs')
if option == 'Mobile phone':
    st.write('qweqwe')

# st.sidebar.header("Mapping Demo")
# st.write(
#     """This demo shows how to use
# [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
# to display geospatial data."""
# )
#
#
# @st.experimental_memo
# def from_data_file(filename):
#     url = (
#         "http://raw.githubusercontent.com/streamlit/"
#         "example-data/master/hello/v1/%s" % filename
#     )
#     return pd.read_json(url)
#
#
# try:
#     ALL_LAYERS = {
#         "Bike Rentals": pdk.Layer(
#             "HexagonLayer",
#             data=from_data_file("bike_rental_stats.json"),
#             get_position=["lon", "lat"],
#             radius=200,
#             elevation_scale=4,
#             elevation_range=[0, 1000],
#             extruded=True,
#         ),
#         "Bart Stop Exits": pdk.Layer(
#             "ScatterplotLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_color=[200, 30, 0, 160],
#             get_radius="[exits]",
#             radius_scale=0.05,
#         ),
#         "Bart Stop Names": pdk.Layer(
#             "TextLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_text="name",
#             get_color=[0, 0, 0, 200],
#             get_size=15,
#             get_alignment_baseline="'bottom'",
#         ),
#         "Outbound Flow": pdk.Layer(
#             "ArcLayer",
#             data=from_data_file("bart_path_stats.json"),
#             get_source_position=["lon", "lat"],
#             get_target_position=["lon2", "lat2"],
#             get_source_color=[200, 30, 0, 160],
#             get_target_color=[200, 30, 0, 160],
#             auto_highlight=True,
#             width_scale=0.0001,
#             get_width="outbound",
#             width_min_pixels=3,
#             width_max_pixels=30,
#         ),
#     }
#     st.sidebar.markdown("### Map Layers")
#     selected_layers = [
#         layer
#         for layer_name, layer in ALL_LAYERS.items()
#         if st.sidebar.checkbox(layer_name, True)
#     ]
#     if selected_layers:
#         st.pydeck_chart(
#             pdk.Deck(
#                 map_style="mapbox://styles/mapbox/light-v9",
#                 initial_view_state={
#                     "latitude": 37.76,
#                     "longitude": -122.4,
#                     "zoom": 11,
#                     "pitch": 50,
#                 },
#                 layers=selected_layers,
#             )
#         )
#     else:
#         st.error("Please choose at least one layer above.")
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )