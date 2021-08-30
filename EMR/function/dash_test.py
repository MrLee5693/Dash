# %%
import os
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

os.chdir('/home/zhghddl13/EMR/function')
#sys.path.append('../')

Diagnosis = pd.read_csv('../File/Diagnosis_named.csv')
Vital = pd.read_csv('../File/Vital_named_cleaned.csv')

Beauty = pd.read_csv('../File/Beauty.csv')
Beauty["Label"] = Beauty["Label"].astype(str)
Beauty_visit = Beauty.sort_values('Beauty_Count', ascending=False)
Beauty_charge = Beauty.sort_values('Price', ascending=False)

# %%
app = dash.Dash(__name__)

app.layout = html.Div([
    # ---상단---
    # 1. 왼쪽 상단, 오른쪽 상단 전체
    html.Div(children=[

        # 1.1) 왼쪽 상단 - 선택 박스(제목:H2 박스)
        html.Div(
            # 1.1-1) 박스 내용
            children=[
                # 제목
                html.H2('질병 통계'),
                # 드롭다운 1 : 견종 선택
                dcc.Dropdown(
                    id='breed',
                    options=[{'label': i, 'value': i}
                            for i in Diagnosis['Name'].unique()],
                    placeholder='견종을 선택하세요♥ (미 선택 시 견종 구분 없이 전체 통계)'),
                # 드롭다운 2 : 성별 선택
                dcc.Dropdown(
                    id='sex',
                    options=[
                        {'label': '남자', 'value': 1},
                        {'label': '여자', 'value': 2},
                        {'label': '중성화 남자', 'value': 3},
                        {'label': '중성화 여자', 'value': 4}],
                    placeholder='성별을 선택하세요♥ (미 선택 시 성별 구분 없이 전체 통계)'),
                # 드롭다운 3 : 나이 선택
                dcc.Dropdown(
                    id='year',
                    placeholder='나이를 선택하세요♥ (미 선택 시 나이 구분 없이 전체 통계)'),
                # 드롭다운 4 : 질병 대분류, 소분류
                dcc.Dropdown(
                    id='diagnosis_category',
                    options=[
                        {'label': '대분류로 보기', 'value': 1}],
                    placeholder='분류를 선택하세요♥ (미 선택 시 소분류(질병)으로 통계)'),
#                 html.H6('유둥스', style={'margin-top': '0px', 'margin-bottom': '0px', 'color': '#FDF3F3','textAlign': 'center'}),
#                 html.H6('짤수짤수', style={'margin-top': '0px', 'margin-bottom': '20px', 'color': '#FDF3F3','textAlign': 'center'})
                ],
            # 1.1-2) 박스 스타일
            style={'width': '30%',
                   'height': '270px',
                   'backgroundColor': '#FDF3F3',
                   'display': 'inline-block',
                   'float': 'left'}),

        # 1.2) 오른쪽 상단 - 성별분포 및 나이분포
        html.Div(
            # 1.2-1) 박스 내용
            children=[
                dcc.Graph(id='sex_ratio', style={'display': 'none'}),
                dcc.Graph(id='year_ratio', style={'display': 'none'})
                ],
            # 1.2-2) 박스 스타일
            style={'width': '70%',
                   'display': 'inline-block',
                   'float': 'left'})
    
    # 상단 전체 스타일 설정
    ], style={'width': '100%','display': 'inline-block'}),
    

    # --- 하단 ---
    html.Div([

        # 결과물 표시전에 로딩 표시 띄우기
        dcc.Loading(id='loading',
                    children=[
                        dcc.Store(id='result-value'),
                        # 2. 왼쪽 하단, 오른쪽 하단 전체
                        html.Div([
                            # 2.1) 왼쪽 하단 - 데이터 테이블(소분류)
                            html.Div(
                                # 2.1-1) 데이터 테이블 내용
                                children=[
                                    dt.DataTable(
                                        id='result-table',
                                        columns=[{'name': i, "id": i}
                                                 for i in ["Diagnosis", "Counts", "%"]],
                                        style_table={'minwidth': '43.5%', },
                                        style_cell={'maxWidth': 0, },
                                        style_data_conditional=[{'if': {'state': 'selected'},
                                                                 'backgroundColor': '#E4F1FB','border': '1.5px solid #B2CDFF'}]
                                    ),
                                ],
                                #2.1-2) 데이터 테이블 스타일
                                style={'width': '30%',
                                       'display': 'inline-block',
                                       'float': 'left'} 
                            ), 

                            # 2.2) 오른쪽 하단 - 확률 및 년도별 질병 그래프
                            html.Div(
                                # 2.2-1) 그래프 내용
                                children=[
                                    dcc.Graph(id='result-graph'),
                                    dcc.Graph(id='diagnosis-year'),
                                ],
                                # 2.2-2) 그래프 스타일
                                style={'width': '70%',
                                       'display': 'inline-block',
                                       'float': 'left'}
                            ),

                        ], style={'width': '100%', 'display': 'inline-block'}),

                    ],
                    type="circle",),
    ]),

    # --- 최하단 ---
    dcc.Graph(id='vital-graph',
              figure=px.scatter(Vital.groupby(['Name', '_Month'], as_index=False).mean(), x = "_Month", y="VT_BW", color="Name", title='월별 몸무게 평균')),
    dcc.Graph(id='vital-describe',
              figure=px.bar(Vital.groupby(['Name', 'Sex'], as_index=False).mean(), y = 'VT_BW', color='Name', hover_name='Sex', title = '성별 몸무게 평균')),
    
        
    
    # 3. 미용/호텔
    # 3.1) 미용
    html.Div([
        # 탭
        dcc.Tabs(
            children=[
                # 탭1 - 방문횟수
                dcc.Tab(label='미용방문횟수',
                        children=[
                            dcc.Graph(id='beauty-visit',
                                figure=px.bar(Beauty_visit, x='Label', y='Beauty_Count', title='미용방문횟수'))
                        ]),
                # 탭2 - 요금
                dcc.Tab(label='미용요금',
                        children=[
                            dcc.Graph(id='beauty-charge',
                                figure=px.bar(Beauty_charge, x='Label', y='Price', title='미용요금'))
                        ])
            ],
            style={'width': '90%',
                   'display': 'inline-block',
                   'margin': '20px 5% 20px'})
    ])
    
   
])


# %%

# @app.callback(
#     Output('vital-graph', 'figure'),
#     Input('breed', 'value')
# )
# def update_vital_df(breed):
#     return px.scatter(Vital.groupby(['Name', 'Sex', '_Month'], as_index=False).mean(), x = "_Month", y="VT_BW", color="Name", hover_name='Sex')
    
    
# 견종을 넣으면 나이의 options와 value를 만들어줌
@app.callback(
    Output('year', 'options'),
    Output('year', 'value'),
    [Input('breed', 'value')])

def update_year_dropdown(value):
    options = [
        {'label': i, 'value': i}
        for i in sorted(Diagnosis.query(f'Name == "{value}" and _Year <= 30')['_Year'].unique())
    ]
    return options, None


# 데이터를 넣어주면 데이터 테이블 - 소분류 (왼쪽 하단) 생성
@app.callback(
    Output('result-table', 'data'),
    [Input('result-value', 'data')]
)
def update_table(result_value):
    return result_value


# 데이터를 넣어주면 데이터 테이블의 bar-chart (오른쪽 하단 1번) 생성
@app.callback(
    Output('result-graph', 'figure'),
    Input('result-value', 'data')
)
def update_graph(result_value):
    if len(result_value) == 0:
        return px.bar()
    return px.bar(result_value, x='Diagnosis', y='%', title=f'상위 {len(result_value)}개 bar-chart')



# 견종, 나이를 선택 했을 때 - 성별분포(오른쪽 상단 1번) 생성
@app.callback(
    Output('sex_ratio', 'figure'),
    Output('sex_ratio', 'style'),
    Input('breed', 'value'),
    Input('year', 'value')
)
def update_sex_ratio_graph(breed, year):   
    display = {'width': '35%', 'display': 'inline-block', 'float': 'middle'}
    
    if breed is not None and year is None:
        sex_count = Diagnosis.query(f'Name == "{breed}" and _Year <= 30').groupby([
            'Sex']).count()['Name']
        pie_chart = px.pie(names=sex_count.index, values=sex_count, title=f'《견종: {breed}》의 성별 분포', height=300)
        # 차트 색상 변경 하려면 이걸로
#         pie_chart = px.pie(names=sex_count.index, values=sex_count, title=f'{breed} 성별 분포', height=300).update_layout(paper_bgcolor="#FDF3F3")
        return pie_chart, display

    elif breed is None and year is not None:
        sex_count = Diagnosis.query(f'_Year == {year} and _Year <= 30').groupby([
            'Sex']).count()['Name']
        pie_chart = px.pie(names=sex_count.index, values=sex_count, title=f'《나이: {year}살》의 성별 분포', height=300)
        return pie_chart, display
    
    elif breed is not None and year is not None:
        sex_count = Diagnosis.query(f'Name == "{breed}" and _Year == {year} and _Year <= 30').groupby([
            'Sex']).count()['Name']
        pie_chart = px.pie(names=sex_count.index, values=sex_count, title=f'《견종: {breed}｜나이: {year}살》의 성별 분포', height=300)
        return pie_chart, display
    
    else :
        sex_count = Diagnosis.query('_Year <= 30').groupby(['Sex']).count()['Name']
        pie_chart = px.pie(names=sex_count.index, values=sex_count, title=f'《Total》 성별 분포', height=300)
        return pie_chart, display
    


# 견종, 성별 선택 했을 때 - 나이 분포(오른쪽 상단 2번) 생성
@app.callback(
    Output('year_ratio', 'figure'),
    Output('year_ratio', 'style'),
    Input('breed', 'value'),
    Input('sex', 'value'),
)
def update_year_ratio_graph(breed, sex):
    if sex is not None:
        # 표 제목에 들어갈 라벨
        sex_label = {1: '남', 2: '여', 3: '중성화 남', 4: '중성화 여'}[sex]
    display = {'width': '65%', 'display': 'inline-block', 'float': 'middle'}

    if breed is not None and sex is None:
        year_count = Diagnosis.query(f'Name == "{breed}" and _Year <= 30').groupby([
            '_Year']).count()['Name']
        return px.bar(year_count, title=f'《성별: {breed}》의 나이 분포', height=300), display
    elif breed is None and sex is not None:
        year_count = Diagnosis.query(f'Sex == {sex}  and _Year <= 30').groupby([
            '_Year']).count()['Name']
        return px.bar(year_count, title=f'《성별: {sex_label}》의 나이 분포', height=300), display
    elif breed is not None and sex is not None:
        year_count = Diagnosis.query(f'Name == "{breed}" and Sex == {sex}  and _Year <= 30').groupby([
            '_Year']).count()['Name']
        return px.bar(year_count, title=f'《견종: {breed}｜성별: {sex_label}》의 나이 분포', height=300), display
    else:
        year_count = Diagnosis.query('_Year <= 30').groupby(['_Year']).count()['Name']
        return px.bar(year_count, title='《Total》 나이 분포', height=300), display
    

# 견종, 성별 선택 후에 나오는 [데이터 테이블(왼쪽 하단)의 active_cell]을 클릭 했을 때 - 나이별 질병 그래프(오른쪽 하단 2번) 생성
# active_cell : callback에 연결해서 사용
@app.callback(
    Output('diagnosis-year', 'figure'),
    Output('result-table', 'active_cell'),
    dash.dependencies.Input('breed', 'value'),
    dash.dependencies.Input('sex', 'value'),
    dash.dependencies.Input('result-table', 'active_cell'),
    dash.dependencies.Input('result-table', 'data'),
    Input('diagnosis_category','value')
)
def update_diagnosis_year_graph(breed, sex, active_cell, data, diagnosis_category):
    diagnosis = data[active_cell['row']
                     ]['Diagnosis'] if data and active_cell else None

    if diagnosis_category == None:
        if sex is not None:#표에 표시할 성별 라벨
            sex_label = {1: '남', 2: '여', 3: '중성화 남', 4: '중성화 여'}[sex]
        else :
            sex_label = sex
           
        if diagnosis is None:
            return px.line(), None
        
        if breed is not None and sex is not None:
            d = Diagnosis.query(f'Name == "{breed}" and Sex == {sex} and Diagnosis == "{diagnosis}" and _Year <= 30').groupby(
                ['_Year'], as_index=False).count()[['_Year', 'Diagnosis']]
            d_size = Diagnosis.query(f'Name == "{breed}" and Sex == {sex} and _Year <= 30').groupby(
                ['_Year'], as_index=False).count()[['_Year', 'Diagnosis']]
            
        elif breed is not None and sex is None:
            d = Diagnosis.query(f'Name == "{breed}" and Diagnosis == "{diagnosis}" and _Year <= 30').groupby(
                ['_Year','Sex'], as_index=False).count()[['_Year','Sex', 'Diagnosis']]
            d_size = Diagnosis.query(f'Name == "{breed}" and _Year <= 30').groupby(
                ['_Year','Sex'], as_index=False).count()[['_Year','Sex' ,'Diagnosis']]
            d["Diagnosis"] /= d_size["Diagnosis"]
            line_chart= px.line(d, x='_Year', y='Diagnosis', color='Sex', 
                                title=f'《견종: {breed}｜성별: {sex_label}｜질병: {diagnosis}》의 연도별 그래프')
            return line_chart, None
            
        elif breed is None and sex is not None:
            d = Diagnosis.query(f'Sex == {sex} and Diagnosis == "{diagnosis}" and _Year <= 30').groupby(
                ['_Year','Name'], as_index=False).count()[['Name', '_Year', 'Diagnosis']]
            d_size = Diagnosis.query(f'Sex == {sex} and _Year <= 30').groupby(
                ['_Year','Name'], as_index=False).count()[['Name','_Year', 'Diagnosis']]
            
            d["Diagnosis"] /= d_size["Diagnosis"]
            line_chart= px.line(d, x='_Year', y='Diagnosis', color='Name', 
                                title=f'《견종: {breed}｜성별: {sex_label}｜질병: {diagnosis}》의 연도별 그래프')
#             line_chart= px.line(d, x='_Year', y='Diagnosis', color='Name',
#                                 title=f'견종: {breed}｜성별: {sex}｜▶{diagnosis}◀의 연도별 그래프').update_layout(paper_bgcolor="#FDF3F3")
            return line_chart, None
  
#         d["Diagnosis"] /= d_size["Diagnosis"]
        d.rename(columns={'Diagnosis': 'Count'}, inplace=True)
        line_chart = px.line(d, x='_Year', y='Count', 
                             title=f'《견종: {breed}｜성별: {sex_label}｜질병: {diagnosis}》 연도별 그래프')
        #색상 변경하고 싶으면
#         line_chart = px.line(d, x='_Year', y='Count',
#                              title=f'견종: {breed}｜성별: {sex}｜▶{diagnosis}◀ 연도별 그래프').update_layout(paper_bgcolor="#FDF3F3")
        return line_chart, None
    
    else :
        if sex is not None:
            sex_label = {1: '남', 2: '여', 3: '중성화 남', 4: '중성화 여'}[sex]
        else :
            sex_label = sex
            
        if diagnosis is None:
            return px.line(), None

        if breed is not None and sex is not None:
            d = Diagnosis.query(f'Name == "{breed}" and Sex == {sex} and 뿜빵이 == "{diagnosis}" and _Year <= 30').groupby(
                ['_Year'], as_index=False).count()[['_Year', 'Diagnosis']]
            d_size = Diagnosis.query(f'Name == "{breed}" and Sex == {sex} and _Year <= 30').groupby(
                ['_Year'], as_index=False).count()[['_Year', 'Diagnosis']]
   
                        
        elif breed is not None and sex is None:
            d = Diagnosis.query(f'Name == "{breed}" and 뿜빵이 == "{diagnosis}" and _Year <= 30').groupby(
                ['_Year','Sex'], as_index=False).count()[['_Year','Sex', 'Diagnosis']]
            d_size = Diagnosis.query(f'Name == "{breed}" and _Year <= 30').groupby(
                ['_Year','Sex'], as_index=False).count()[['_Year','Sex', 'Diagnosis']]
            d["Diagnosis"] /= d_size["Diagnosis"]
            line_chart = px.line(d, x='_Year', y='Diagnosis', color='Sex', 
                                 title=f'《견종: {breed}｜성별: {sex}｜대분류: {diagnosis}》의 연도별 그래프')

            return line_chart, None
            
        elif breed is None and sex is not None:
            d = Diagnosis.query(f'Sex == {sex} and 뿜빵이 == "{diagnosis}" and _Year <= 30').groupby(
                ['Name', '_Year'], as_index=False).count()[['Name', '_Year', 'Diagnosis']]
            d_size = Diagnosis.query(f'Sex == {sex} and _Year <= 30').groupby(
                ['Name','_Year'], as_index=False).count()[['Name','_Year', 'Diagnosis']]
            d["Diagnosis"] /= d_size["Diagnosis"]
            line_chart = px.line(d, x='_Year', y='Diagnosis', color='Name', 
                                 title=f'《견종: {breed}｜성별: {sex}｜대분류: {diagnosis}》의 연도별 그래프')
            #색상 변경하고 싶으면
#             line_chart = px.line(d, x='_Year', y='Diagnosis', color='Name', 
#                                  title=f'견종: {breed}｜성별: {sex}｜▶{diagnosis}◀의 연도별 그래프').update_layout(paper_bgcolor="#FDF3F3")
            return line_chart, None

#         d["Diagnosis"] /= d_size["Diagnosis"]
        d.rename(columns={'Diagnosis': 'Count'}, inplace=True)
        line_chart = px.line(d, x='_Year', y='Count', 
                             title=f'《견종: {breed}｜성별: {sex_label}｜대분류: {diagnosis}》의 연도별 그래프')
        #색상 변경하고 싶으면
#         line_chart = px.line(d, x='_Year', y='Count', 
#                              title=f'견종: {breed}｜성별: {sex}｜▶{diagnosis}◀의 연도별 그래프').update_layout(paper_bgcolor="#FDF3F3")
        return line_chart, None


# 견종, 성별, 나이 넣었을 때 (소분류 : 질병) - 결과물(id:result-value)의 data 생성
@app.callback(
    dash.dependencies.Output('result-value', 'data'),
    dash.dependencies.Input('breed', 'value'),
    dash.dependencies.Input('sex', 'value'),
    dash.dependencies.Input('year', 'value'),
    Input('diagnosis_category','value')
)
def update_result(breed, sex, year, diagnosis_category):
    # 분류 선택 안하면 그냥 나오기
    if diagnosis_category == None:
        if (breed != None) and (sex == None) and (year == None):
            result = Diagnosis.query(f'Name == "{breed}" and _Year <= 30')[
                'Diagnosis'].value_counts().reset_index()
        elif (breed == None) and (sex != None) and (year == None):
            result = Diagnosis.query(f'Sex == {sex} and _Year <= 30')[
                'Diagnosis'].value_counts().reset_index()
        elif (breed == None) and (sex == None) and (year != None):
            result = Diagnosis.query(f'_Year == {year} and _Year <= 30')[
                'Diagnosis'].value_counts().reset_index()
        elif breed == None:
            result = Diagnosis.query(
                f'Sex == {sex} and _Year == {year} and _Year <= 30')['Diagnosis'].value_counts().reset_index()
        elif sex == None:
            result = Diagnosis.query(
                f'Name == "{breed}" and _Year == {year} and _Year <= 30')['Diagnosis'].value_counts().reset_index()
        elif year == None:
            result = Diagnosis.query(
                f'Name == "{breed}" and Sex == {sex} and _Year <= 30')['Diagnosis'].value_counts().reset_index()
        else:
            result = Diagnosis.query(
                f'Name == "{breed}" and Sex == {sex} and _Year == {year} and _Year <= 30')['Diagnosis'].value_counts().reset_index()
        result.columns = ["Diagnosis", "Counts"]
        result['%'] = [round(x/result['Counts'].sum()*100, ndigits=2)
                    for x in result['Counts']]
        return result.head(30).to_dict(orient='records')
    # 분류 선택 하면 소분류는 사라짐
    else:
        if (breed != None) and (sex == None) and (year == None):
            result = Diagnosis.query(f'Name == "{breed}" and _Year <= 30')[
                '뿜빵이'].value_counts().reset_index()
        elif (breed == None) and (sex != None) and (year == None):
            result = Diagnosis.query(f'Sex == {sex} and _Year <= 30')[
                '뿜빵이'].value_counts().reset_index()
        elif (breed == None) and (sex == None) and (year != None):
            result = Diagnosis.query(f'_Year == {year} and _Year <= 30')[
                '뿜빵이'].value_counts().reset_index()
        elif breed == None:
            result = Diagnosis.query(
                f'Sex == {sex} and _Year == {year} and _Year <= 30')['뿜빵이'].value_counts().reset_index()
        elif sex == None:
            result = Diagnosis.query(
                f'Name == "{breed}" and _Year == {year} and _Year <= 30')['뿜빵이'].value_counts().reset_index()
        elif year == None:
            result = Diagnosis.query(
                f'Name == "{breed}" and Sex == {sex} and _Year <= 30')['뿜빵이'].value_counts().reset_index()
        else:
            result = Diagnosis.query(
                f'Name == "{breed}" and Sex == {sex} and _Year == {year} and _Year <= 30')['뿜빵이'].value_counts().reset_index()
        result.columns = ["뿜빵이", "Counts"]
        result['%'] = [round(x/result['Counts'].sum()*100, ndigits=2)
                    for x in result['Counts']]
        result.rename(columns={"뿜빵이":"Diagnosis"},inplace=True)
        return result.head(30).to_dict(orient='records')


# %%
# 특정 포트 및 아이피 부여
if __name__ == '__main__':
    app.run_server(debug=True, port=5693, host='0.0.0.0')

