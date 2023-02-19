# Installation

###  1. Install PostreSQL DBMS
I have a local installation but the easiest way is described by the [link](https://hevodata.com/learn/docker-postgresql/#3steps)
###  2. Add env variables in your OS:
We need 5 env variables:
```bash
EXPORT POSTGRES_USER = ..;
EXPORT POSTGRES_PASSWORD = ..;
EXPORT POSTGRES_DB = ..;
EXPORT POSTGRES_SERVER = ..; # optional, localhost is default
EXPORT POSTGRES_PORT = ..; # optional, 5432 is default
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

http://127.0.0.1:8000/docs

# About architecture
## Top level architecture:
![top](https://disk.yandex.ru/i/owTB1rXAWL1xPA)

### Calculations plan

1. Calculation of raw data every hour.

2. The calculation of the table depends on the needs of the business. For example when RAW calculation ends it can trigger ODS calculation. We take all raw data in which the value of the created_at field is greater than the last one uploaded by us (stored in the CTL technical table)
## Future architecture:
![future](https://disk.yandex.ru/i/AmgLxJEuUMQpgw)