# LOGGINGSFACTORY

## Installation

> pip install loggingsfactory

## Usage

### Import

```python
from loggingsfactory.logging import Loggers
```

### Initialization

#### Loguru

- Method 1
  ```python
  loggers = Loggers(appname="myapp")
  ```
- Method 2
  ```python
  loggers = Loggers(appname="myapp", debug=True)
  ```
- Method 3: not required, but can be done if auto switching of logger type is required for different environments
  ```python
  loggers = Loggers(
      appname="myapp",
      debug=True,
      host="https://elasticsearch.com:9201",
      index="appindex",
      username="user1"
      pw="userpw"
    )
  ```

#### Elasticseach

```python
loggers = Loggers(
    appname="myapp",
    debug=False,
    host="https://elasticsearch.com:9201",
    index="appindex",
    username="user1"
    pw="userpw"
  )
```

#### AsyncElasticseach

```python
loggers = Loggers(
    appname="myapp",
    debug=False,
    useasync=True,
    host="https://elasticsearch.com:9201",
    index="appindex",
    username="user1"
    pw="userpw"
  )
```

### Log usage

#### Loguru & Elasticsearch

- Using default logging data

  - function name will be the function that is calling the log

    ```python
    def test_log():
        loggers.log("info", "log data")
    ```

    ```
    {
        "log": "log data",
        "version": "1.0",
        "logger_level": "INFO",
        "functional_name": "test_log",
        "app_name": "myapp",
        "timestamp": "2020-01-01T00:00:00.000Z",
    }
    ```

- Using custom function name

  ```python
  def test_log():
      loggers.log("info", "log data", "somefunctionname")
  ```

  ```
  {
      "log": "log data",
      "version": "1.0",
      "logger_level": "INFO",
      "functional_name": "somefunctionname",
      "app_name": "myapp",
      "timestamp": "2020-01-01T00:00:00.000Z",
  }
  ```

- Using custom log data format

  ```python
  custom_log_data = {
    "custom_log": "this is a custom log"
  }

  def test_log():
      loggers.log("info", custom_log_data, None, True)
  ```

  ```
  {
      "custom_log": "this is a custom log"
  }
  ```

- Using default logging data with custom date format

  ```python
  date = "2022/04/27"

  def test_log():
      loggers.log("info", "log data", None, False, date)
  ```

  ```
  {
      "log": "log data",
      "version": "1.0",
      "logger_level": "INFO",
      "functional_name": "test_log",
      "app_name": "myapp",
      "timestamp": "2022/04/27",
  }
  ```

#### Loguru & AsyncElasticsearch

- Using default logging data

  - function name will be the function that is calling the log

    ```python
    async def test_log():
        loggers.async_log("info", "log data")
    ```

    ```
    {
        "log": "log data",
        "version": "1.0",
        "logger_level": "INFO",
        "functional_name": "test_log",
        "app_name": "myapp",
        "timestamp": "2020-01-01T00:00:00.000Z",
    }
    ```

- Using custom function name

  ```python
  async def test_log():
      loggers.async_log("info", "log data", "somefunctionname")
  ```

  ```
  {
      "log": "log data",
      "version": "1.0",
      "logger_level": "INFO",
      "functional_name": "somefunctionname",
      "app_name": "myapp",
      "timestamp": "2020-01-01T00:00:00.000Z",
  }
  ```

- Using custom log data format

  ```python
  custom_log_data = {
    "custom_log": "this is a custom log"
  }

  async def test_log():
      loggers.async_log("info", custom_log_data, None, True)
  ```

  ```
  {
      "custom_log": "this is a custom log"
  }
  ```

- Using default logging data with custom date format

  ```python
  date = "2022/04/27"

  async def test_log():
      loggers.async_log("info", "log data", None, False, date)
  ```

  ```
  {
      "log": "log data",
      "version": "1.0",
      "logger_level": "INFO",
      "functional_name": "test_log",
      "app_name": "myapp",
      "timestamp": "2022/04/27",
  }
  ```

### Query usage

#### Elasticsearch

- Using default query payload
  ```python
  def get_data():
      return loggers.query()
  ```
- Using custom query payload

  ```python
  custom_payload = {
      "query": {
          "bool": {
              "filter": [
                  {
                      "bool": {
                          "should": [{"match_phrase": {"app_name.keyword": "myapp"}}],
                          "minimum_should_match": 1,
                      }
                  },
                  {
                      "range": {
                          "timestamp": {
                              "gte": "2021-09-24T02:58:43.647Z",
                              "lte": "2022-09-24T02:58:43.647Z",
                              "format": "strict_date_optional_time",
                          }
                      }
                  },
              ]
          }
      }
  }

  def get_data():
      return loggers.query(custom_payload)
  ```

#### AsyncElasticsearch

- Using default query payload
  ```python
  async def get_data():
      return await loggers.async_query()
  ```
- Using custom query payload

  ```python
  custom_payload = {
      "query": {
          "bool": {
              "filter": [
                  {
                      "bool": {
                          "should": [{"match_phrase": {"app_name.keyword": "myapp"}}],
                          "minimum_should_match": 1,
                      }
                  },
                  {
                      "range": {
                          "timestamp": {
                              "gte": "2021-09-24T02:58:43.647Z",
                              "lte": "2022-09-24T02:58:43.647Z",
                              "format": "strict_date_optional_time",
                          }
                      }
                  },
              ]
          }
      }
  }

  async def get_data():
      return await loggers.async_query(custom_payload)
  ```

### SQL Query usage

#### Elasticsearch & AsyncElasticsearch

- Using query payload

  - supports only synchronous

  ```python
  query_statement = "SELECT * FROM appindex"

  def get_data():
      return loggers.sql_query(query_statement)
  ```
