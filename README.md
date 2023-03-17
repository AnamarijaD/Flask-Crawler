# Flask-Crawler
REST API project for retrieving, storing and scraping data using Python Flask framework and MongoDB

## Installation

Install needed libraries

```bash
  pip install flask
  pip install bs4
  pip install pandas
  pip install numpy
```


## Running application

Run flask-crawler with flask

```bash
  flask run
```

## API Reference

#### Get all crawler_data items

```http
  GET /api/crawler
```



#### Scrape data from website and storing it into mongodb

```http
  POST /api/crawler/trigger
```


#### Filter pricing_data items

```http
  GET /api/pricing_data
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `product_name`      | `string` | **Not Required**. Name of item to fetch |
| `therapeutic_area`      | `string` | **Not Required**. Area of item to fetch |
| `mnf`      | `string` | **Not Required**. Medical necessity form of item to fetch |
| `route_of_administration`      | `string` | **Not Required**. Usage of item to fetch |


#### Retrieve data from pricing_data.xlsx file and store it 

```http
  GET /api/pricing_data/process
```

