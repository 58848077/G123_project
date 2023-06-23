# G123 Project
## :page_with_curl:	 Project Description
The G123 Project is a project that enables users to access stock information, including symbol, date, open price, close price, and volume, and stock statistics through the API endpoints.

Stock information (symbols, dates, opening prices, closing prices, and volumes) is retrieved from [AlphaVantage](https://www.alphavantage.co/documentation/#dailyadj) and inserted into a database for storage.

## :page_with_curl:	 Tech Stack
| Name | Version | Explanation |
| --- | --- | --- |
| python | 3.9.6 |
| Django | 4.0 | I primarily use Django and DRF (Django REST framework) for developing APIs, so I am more familiar with these technologies.
| djangorestframework | 3.14 | Same as above.
| python-dotenv | 1.0.0| To load .env file.
| requests | 2.31.0 | To call an API endpoint.
| sqlite3 | | Lightweight, perfect for small projects.

## :sunglasses:	Store API Key Securely
To securely store the API Key, we store it in the `.env` file. The `.env` file on the local machine is not pushed to GitHub. Instead, there is a `sample.env` file that contains all the variables. Users can add the variables from the `sample.env` file to the `.env` file.

## :globe_with_meridians: Installation and Launch
1. Clone this [repository](https://github.com/58848077/G123_project.git):

    ```
    git clone https://github.com/58848077/G123_project.git
    ```

2. Move to the G123_project folder:
    
    ```
    cd G123_project
    ```

3. Install the libraries:
   
   ```
   pip install -r requirements.txt
   ```

4. Create an `.env` file in root folder and add the variables. See `sample.env` for assistance.

5. Run the following command to start the server:

    ```
    sudo docker compose up --build
    ```

6. To update the financial data, please run the following command:

    ```
    python3 get_raw_data.py
    ```

* The project use `8000` as the port.

    ```
    localhost:8000/
    ```

## :globe_with_meridians: Perform ORM Model Migration
We use Django ORM to manipulate the database. Here are the steps to migrate the models after modifying the ORM models:

1. Navigate to the `financial` folder.

    ```
    cd financial/
    ```

2. If there are any changes in `models.py`, create migration files: 

    ```
    python3 manage.py makemigrations
    ```

3. Migrate the database: 

    ```
    python3 manage.py migrate
    ```

* Please note that due to the use of Django ORM for database operations, the original `model.py` file that was supposed to be located in the root folder will be moved to `financial/fin_data/models.py`.


# :round_pushpin: API Endpoints
## :pushpin: Get Financial Data
### Endpoint

    GET localhost:8000/api/financial_data

### Query(all queries are optional)

| Query | Type | Description |
| --- | --- | --- |
| symbol | str | IBM or AAPL(Apple Inc.) |
| start_date | str | yyyy-mm-dd |
| end_date | str | yyyy-mm-dd |
| limit | int | limit of records can be retrieved for single page. |
| page | int | total number of pages. |

### Response

    {
        "data": [
            {
                "symbol": "foo",
                "open_price": 123.45,
                "close_price": 135.79,
                "date": "2023-06-31",
                "volume": 99999999
            },
            ...
        ],
        "pagination": {
            "count": 0,
            "page": 1,
            "limit": 5,
            "pages": 0,
        },
        "info": {
            "error": ""
        }
    }

### Sample
#### Sample Request
    curl -X GET http://localhost:8000/api/financial_data/?symbol=AAPL&start_date=2023-06-01&end_date=2023-06-20&limit=3&page=3
#### Sample Response
    {
        "data":[
            {
                "symbol":"AAPL",
                "open_price":183.96,
                "close_price":186.01,
                "date":"2023-06-15",
                "volume":65433166
            },
            {
                "symbol":"AAPL",
                "open_price":186.73,
                "close_price":184.92,
                "date":"2023-06-16",
                "volume":101256225
            },{
                "symbol":"AAPL",
                "open_price":184.41,
                "close_price":185.01,
                "date":"2023-06-20",
                "volume":49799092
            }
        ],
        "pagination":{
            "count":6,
            "page":2,
            "limit":3,
            "pages":2
        },
        "info":{
            "error":""
        }
    }

#### Sample Error Request 
    curl -X GET http://localhost:8000/api/financial_data/?symbol=AAPL&start_date=2023-0s6-01&end_date=2023-0620&limit=30&page=300

#### Sample Error Response 
    {
        "data":[],
        "pagination":{
            "count":0,
            "page":0,
            "limit":0,
            "pages":0
        },
        "info":{
            "error":"start_date(2023-0s6-01), length/format error, format should be yyyy-mm-dd. end_date(2023-0620), length/format error, format should be yyyy-mm-dd. "
        }
    }


## :pushpin: Get Statistics
### Endpoint

    GET localhost:8000/api/statistics

### Query(all queries are required)

| Query | Type | Description |
| --- | --- | --- |
| symbol | str | IBM or AAPL(Apple Inc.) |
| start_date | str | yyyy-mm-dd |
| end_date | str | yyyy-mm-dd |

### Response

    {
        "data":{
            "start_date":"2023-04-31",
            "end_date":"2023-06-31",
            "symbol":"foo",
            "average_daily_open_price":135.79,
            "average_daily_close_price":123.21,
            "average_daily_volume":99999999,
        },
        "info":{
            "error":""
        }
    }

### Sample
#### Sample Request
    curl -X GET http://localhost:8000/api/statistics/?symbol=IBM&start_date=2023-06-01&end_date=2023-06-23
#### Sample Response
    {
        "data":{
            "start_date":"2023-06-01",
            "end_date":"2023-06-23",
            "symbol":"IBM",
            "average_daily_open_price":136.25,
            "average_daily_close_price":135.99,
            "average_daily_volume":5001925
        },
        "info":{
            "error":""
        }
    }


#### Sample Error Request 
    curl -X GET http://localhost:8000/api/statistics/

#### Sample Error Response 
    {
        "data":{
            "start_date":"2023-06-01",
            "end_date":"2023-06-23",
            "symbol":"IBM",
            "average_daily_open_price":0,
            "average_daily_close_price":0,
            "average_daily_volume":0
        },
        "info":{
            "error":"Query parameter(s) required: symbol, start_date, end_date, please check again."
        }
    }
