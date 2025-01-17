# Home assignment

Description -> https://github.com/source-ag/assignment-software-engineering/blob/main/assignment.md

# Installation

###  1. Install PostreSQL DBMS
I have a local installation but the easiest way is described by the [link](https://hevodata.com/learn/docker-postgresql/#3steps)
###  2. Add env variables in your OS:
We need to add 5 env variables: 
```bash
export POSTGRES_USER=..;
export POSTGRES_PASSWORD=..;
export POSTGRES_DB=..;
export POSTGRES_SERVER=..; # optional, localhost is default
export POSTGRES_PORT=..; # optional, 5432 is default
```
###  3. Create python virtual env
```bash
python3 -m venv .env # create
```
```bash
source .env/bin/activate # activate
```

###  4. Install requirenments

```bash
pip install -r requirements.txt
```

### 5. Run app
```bash
uvicorn main:app --reload
```
# API doc

In target architecture we should use AirFlow (or similar lib) for scheduling our calculations.  
But now we have two main endpoits:

[raw recalculation](https://github.com/Draqneel/source_assigment/blob/de9a00d03c9623a9d04653bac043dbdcd4038ff3/main.py#L45)  
[ods recalculation (relational layer)](https://github.com/Draqneel/source_assigment/blob/de9a00d03c9623a9d04653bac043dbdcd4038ff3/main.py#L55)  

example: [GET] -> http://127.0.0.1:8000/raw/ws_source_meteo/raw_meteo/recalculation

After we can run calculations of our aggregates:  

[Expose the latest weather conditions (i.e. show what's happening now)](https://github.com/Draqneel/source_assigment/blob/main/main.py#L66)  
[Expose the development of the weather parameters over the last 24h in 15 min increments](https://github.com/Draqneel/source_assigment/blob/main/main.py#L103)  
[Expose the average for each of the weather parameters for the last 24h](https://github.com/Draqneel/source_assigment/blob/main/main.py#L76)  
[Expose the development of the weather parameters over the last 7 days in 1 day increments (average per day)](https://github.com/Draqneel/source_assigment/blob/main/main.py#L94)  
[Expose the average of the weather parameters over the last 7 days](https://github.com/Draqneel/source_assigment/blob/main/main.py#L85)  

# Test cases
We have tests only for tools currently (you can find it in project structure).  
Also, for example, we can create tests for aggregations, storing mock data, download it in temp tables and
run aggregation queries under this table.


# Project structure

```bash
├── LICENSE
├── README.md
├── __init__.py
├── configs  # directory contains configuration info
│   ├── __init__.py
│   ├── db_conf.py  # database conn
│   └── etl_conf.py  # searching raw data for etl
├── data
│   ├── may  # main directory for data
├── database.py  # init file for SqlAlchemy db conn
├── etl  # directory contains business logic with structure layer/source_system/process
│   ├── __init__.py
│   ├── ods
│   │   ├── __init__.py
│   │   └── ws_source_meteo
│   │       ├── __init__.py
│   │       └── fact_meteo_snp
│   │           ├── __init__.py
│   │           ├── aggregations.py 
│   │           ├── loader.py
│   │           └── schema.py
│   └── raw
│       ├── __init__.py
│       └── ws_source_meteo
│           ├── __init__.py
│           └── raw_meteo
│               ├── __init__.py
│               ├── loader.py
│               └── schema.py
├── git_staff
│   ├── Future.jpg
│   └── Source.jpg
├── tests 
│   ├── __init__.py
│   ├── test_tools.py
│   ├── mock_data 
├── main.py
├── models.py  # entities desc
├── requirements.txt
└── tools.py  # reusable code


```

# About architecture
## Top level architecture:
![top](https://github.com/Draqneel/source_assigment/blob/main/git_staff/Source.jpg?raw=true)

### Calculations plan

1. Calculation plan depends on data amounts, currently we can recalculate data every 5 min on single machine.  
2. In the future, when the system have to process significantly more data,  we should create a pipeline in which the data gets into RAW instantly (almost). 
   And we can plan calculations based on the needs of the business, the amount of data and the reliability of the data source.
3. The calculation of the table depends on the needs of the business too. For example when RAW calculation ends it can trigger ODS calculation. 
   We take all raw data in which the value of the created_at field is greater than the last one uploaded by us (stored in the CTL technical table).
4. Aggregations should be stored in Views or a separate in-memory storage.    
## Future architecture:
![future](https://github.com/Draqneel/source_assigment/blob/main/git_staff/Future.jpeg?raw=true)
