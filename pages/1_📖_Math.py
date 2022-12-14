import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="TuringContent-Math", page_icon="π")

st.markdown("# π Math")


option = st.selectbox(
    ' ',
    ('κΈμ μ νν΄μ£ΌμΈμ.','λ¬Έμ  μμ° μλν (2022.12.20)', 'μν λ―Ή κ°λ μ£Όμν (2022.12.23)',))
if option == ' ':
    st.markdown("""""")
if option == 'λ¬Έμ  μμ° μλν (2022.12.20)':
    st.markdown("""
    ## π­λ¬Έμ  μμ° μλν

#### μ΄λ± μν

- **[μκ³ λ¦¬μ¦μΌλ‘ μ»€λ² κ°λ₯ν μ λ μνΈ](https://docs.google.com/spreadsheets/d/1Oz_wXThgKzRc-s2vQvMk-ag7g6mJVo3a4aMlawctVJo/edit#gid=0)**

![](https://raw.githubusercontent.com/sharosoo-image/upload/master/images/image.png)
- **Unit D μ»€λ² κ°λ₯ κΈ°μ€**
  - μ λ¬Έμ μ§μ κΈ°μ€μΌλ‘ νλμ unit Dμ μκ³ λ¦¬μ¦μΌλ‘ ν΄κ²° κ°λ₯ν μ νμ΄ 3κ° μ΄μμΌ λ
  - μ νμ΄ μ»€λ² κ°λ₯νλ€λ κ²μ ν μ νμμ μ μ΄λ νλμ λ¬Έμ λ₯Ό μ½λλ‘ μμ± κ°λ₯ν  λ
  - κ·Έλ¦Όμ΄ νμν μ ν μ μΈ
- **μ΅μ μμ± κ°λ₯ λ¬Έμ μ**
  - μ λ 74κ° x μ ν 3κ° x 20λ¬Έμ  = 4440λ¬Έμ 
    - μ ν 3κ° = ν μ λ λΉ νκ·  3κ°μ μ νμ΄ μ‘΄μ¬νλ€κ³  κ°μ 


#### μ€ν μν

  - **[μκ³ λ¦¬μ¦μΌλ‘ μ»€λ² κ°λ₯ν μ λ μνΈ](https://docs.google.com/spreadsheets/d/1Oz_wXThgKzRc-s2vQvMk-ag7g6mJVo3a4aMlawctVJo/edit#gid=1138368730)**

![μ€νμν μ»€λ² κ°λ₯ μ λ](https://user-images.githubusercontent.com/98881555/183082346-be36c526-d5f3-409b-9a72-d195bbfd3703.png)

  - **Unit D μ»€λ² κ°λ₯ κΈ°μ€**
    - μ λ¬Έμ μ§μ κΈ°μ€μΌλ‘ νλμ unit Dμ μν μ νμ μ λ° μ΄μμ μκ³ λ¦¬μ¦μΌλ‘ ν΄κ²° κ°λ₯ν  λ
    - μ νμ΄ μ»€λ² κ°λ₯νλ€λ κ²μ ν μ νμμ μ μ΄λ νλμ λ¬Έμ λ₯Ό μ½λλ‘ μμ± κ°λ₯ν  λ
    - κ·Έλ¦Όμ΄ νμν μ ν μ μΈ

  - **μ΅μ μμ± κ°λ₯ λ¬Έμ μ**
    - μ λ 76κ° x μ ν 5κ° x 20λ¬Έμ  = 7600λ¬Έμ 
      - μ ν 5κ° = ν μ λ λΉ νκ·  10κ°μ μ νμ΄ μ‘΄μ¬νλ©° κ·Έ μ€ μ λ° μ΄μμ μ νμ μ»€λ² κ°λ₯ν΄μΌνλ―λ‘ 

#### λ¬Έμ  μλ μμ± μμ± λ°©λ²
  
  - **latex ννμ λ¬Έμμ΄ μμ± λ°©λ²**
    - https://peps.python.org/pep-0498/
    - `f"{n}"`: λ³μ nμ κ°μ΄ μΆλ ₯λλ€
      - nμ΄ 10μΈ κ²½μ°, `10`μ΄ μΆλ ₯λ¨
    - `f"{{ n }}"`: μ€κ΄νΈμ λ¬Έμ nμ΄ μΆλ ₯λλ€
      - nμ΄ 10μ΄λΌλ, `{n}`μ΄ μΆλ ₯λ¨
    - `f"{{{n}}}`: μ€κ΄νΈμ λ³μ nμ΄ μΆλ ₯λλ€
      - nμ΄ 10μΈ κ²½μ°, `{10}`μ΄ μΆλ ₯λ¨
    - latex ν¨μ μ€, tλ n, bλ‘ μμνλ κ²½μ° μ¬λμ¬λ₯Ό `\\`μ²λΌ νλ² λ μλ ₯νλ€.
      - `\times`λΌκ³  μλ ₯ νλ κ²½μ° `\t`κ° μΈμ λμ§ μμ.
      - `\\times`λΌκ³  μλ ₯νλ€.
""")
if option == 'μν λ―Ή κ°λ μ£Όμν (2022.12.23)':
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