import streamlit as st

st.set_page_config(page_title="TuringContent-Data", page_icon="💾")

st.markdown("# 💾 Data")
option = st.selectbox(
    ' ',
    ('글을 선택해주세요.','데이터 전처리 (2022.08.25)', '수학대왕 2022 결산 (2022-12-22)',))
if option == ' ':
    st.markdown("""""")

from PIL import Image
image = Image.open('drp2.png')

if option == '데이터 전처리 (2022.08.25)':
    col1, col2 = st.columns([1, 5], gap="small")
    with col1:
        st.image(image, width=120)
    with col2:
        st.markdown(""" 
         ## Athena, Presto를 이용한 데이터 전처리
         ### Dominic
         """)

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
if option == '수학대왕 2022 결산 (2022-12-22)' :
    col1, col2 = st.columns([1, 5], gap="small")
    with col1:
        st.image(image, width=120)
    with col2:
        st.markdown(""" 
             ## 2022년의 수학대왕을 대표하는 숫자들을 소개합니다.
             ### Dominic
             """)
    st.markdown("""
    ### 1. 얼마나 많은 학생이 수학대왕으로 공부하나요?
    수학대왕 전체 가입자 수는 **80만 명**으로, 2022년 초, 중, 고 학생 수인 **500만 명**의 **16%**가 수학대왕을 사용하고 있어요. 작년(**19만 명**)보다 **3배** 이상 증가한 수치예요.\\
    수학대왕의 메인 서비스인 고등을 살펴보면 고등 전체 가입자 수는 **43만 명**으로, 2022년 고등학교 학생 수인 **130만 명**의 **33%**가 수학대왕을 사용하고 있어요.
    ### 2. 언제 가장 많은 학생이 수학대왕으로 공부하나요?
    가장 많은 학생이 수학대왕으로 공부한 날은 **6월 26일**로, 여러 학교의 **1학기 기말고사 기간**이었어요.\\
    또한 **오후 9시**에 가장 많은 학생이 수학대왕으로 공부하고 있어요. 학원, 야간 자율 학습 또는 과외 이후 **배운 내용을 정리**하고 **하루를 마무리**하는 데 수학대왕이 도움이 된 것 같아 기뻐요.
    ### 3. 어떤 학생들이 수학대왕을 가장 많이 사용하나요?
    학교급별로 살펴보면 **고등학교와 중학교는 1학년, 초등학교는 6학년**이 가장 많이 수학대왕을 사용하고 있어요. 모두 새로운 시작을 성공적으로 하기 위해 수학대왕과 함께하고 있어요.\\
    지역(광역자치단체)별로 살펴보면 **경기도**의 학생들이 가장 많이 수학대왕과 함께 공부하고 있어요. 다음으로는 **서울특별시**와 **경상남도**의 학생들이 가장 많이 수학대왕과 함께 공부하고 있어요.
    ### 4. 수학대왕으로 얼마나 많이 공부하나요?
    수학대왕으로 푼 문제는 **2,200만 개**로 문제집 기준 **2.2만 권**의 분량이에요. 작년(**400만 개**)보다 **5배** 이상 증가한 수치예요.\\
    또한 수학대왕으로 강의를 시청한 시간은 **4.8억 초**(**약 5,600일**)로 작년(**1.6억 초**)보다 **3배** 이상 수치가 증가했어요.
    ### 5. 어떤 단원을 가장 많이 공부하나요?
    문제 기준으로 고등학생은 **지수함수와 로그함수**, 중학생은 **소인수분해**, 초등학생은 **분수의 나눗셈** 단원의 문제를 가장 많이 풀고 있어요.\\
    또한 강의 기준으로 고등학생은 **유리함수와 무리함수**, 중학생은 **소인수분해** 단원의 강의를 가장 많이 시청하고 있어요.
    ### 6. 수학대왕의 새로운 학습콘텐츠는 어떤 것이 있나요?
    올해에는 다음 네 가지 학습콘텐츠를 새로 출시했어요.
    * **초등 수학 문제**
    * 개념을 제대로 이해하고 있는지 쉽고 빠르게 확인할 수 있는 **OX 문제**
    * 내신 및 모의고사, 수능 고득점을 위한 **킬러 문제**
    * 등하교, 쉬는 시간 또는 자기 전 편하게 볼 수 있는 문제 해설 **Clips**

    ## 수학대왕의 여정은 내년에도 계속됩니다!
    앞으로도 학생들의 **더 나은 학습 경험**을 위해 다음과 같이 **유용하고 편리한 학습콘텐츠**를 출시할 예정이에요.
    * 모바일 환경에서 필요한 내용을 빠르고 편리하게 볼 수 있는 **개념집**
    * 모의고사에 겁먹지 않기 위한 **미니모의고사**

    ### 누구나 최고의 교육을 누릴 수 있도록 수학대왕이 함께합니다.""")



#
#  st.sidebar.markdown("### Map Layers")
#         selected_layers = [
#             layer
#             for layer_name, layer in ALL_LAYERS.items()
#             if st.sidebar.checkbox(layer_name, True)
# page_names_to_funcs = {
#     "안녕하세요" : intro,
#     "반갑습니다": Info,
#     "또와주세요": intro,
#     "감사합니다": intro
# }
#
# demo_name = st.sidebar.selectbox("튜링 콘텐츠팀 블로그", page_names_to_funcs.keys())
# page_names_to_funcs[demo_name]()



