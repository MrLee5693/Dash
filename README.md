# EMR Dash Board
```
EMR
├── File
│   ├── Beauty.csv : 미용 정보 원본 파일
│   ├── Diagnosis.pkl : 진단명 원본 파일
│   ├── Diagnosis_named.csv : 진단명 전처리 파일
│   ├── Vaccine.csv : 백신 정보 원본 파일
│   ├── Vital.pkl : 체중 정보 원본 파일
│   ├── Vital_named_cleaned.csv : 진단명 전처리 파일
│   ├── 기관별_임상증상과_관련질병_영어_한글_윤정리20210724.xlsx : 제주대 교수님 파일
│   └── 통합용어정리.xlsx : 질병명 통합 엑셀 파일
├── function
│   ├── Beauty_DF.py : 미용 테이블 생성
│   ├── Chartlist_DF.py : 차트 테이블 생성
│   ├── dash_test.py : 대시보드 생성
│   ├── data_mapping.py : Diagnosis.pkl -> Diagnosis_named.csv 변환
│   ├── dbconfig.py : 파이썬과 MySQL 연동 시 필요한 정보 저장한 파일
│   ├── Diagnosis_DF.py : 진단 테이블 생성
│   ├── load_data.py : 연동할 때 필요한 정보(id, passwd)를 활용하여 데이터 로드
│   ├── mapping.py : 견종 딕셔너리를 통해 필요한 견종만 필터링하기 위해 활용
│   ├── mapping_dict.py : DB에 있는 견종 딕셔너리를 부르는 파일
│   ├── Vaccine_DF.py : 백신 테이블 생성
│   └── Vital_DF.py : 체중 테이블 생성
├── Jupyter File
│   ├── Beauty.ipynb : 미용 파일 생성
│   ├── Integration of disease names.ipynb : 질병 파일 생성 
│   ├── Upload DB.ipynb : 견종 명 DB에 업로드하는 파일
│   ├── Vaccine.ipynb : 백신 파일 생성
│   └── Vital_check.ipynb : 체중 파일 생성
└── Result
    └── *.csv : 견종 딕셔너리 파일

```



### Diagnosis_named.csv
![Diagnosis](https://user-images.githubusercontent.com/52459996/131270579-f87050a5-75bc-4478-aaed-fe9086aace63.PNG)

### Vital_named_cleaned.csv
![Vital](https://user-images.githubusercontent.com/52459996/131270909-8c684ea3-cfe8-4041-a403-d2408f859321.PNG)

### Code Example
```
python ./EMR/function/dash_test.py
```


[EMR 정리본](https://fortunate-euphonium-65b.notion.site/EMR-c9ae433a522c48c3929278d8e019dc5a)