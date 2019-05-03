# SmartStocks
Smart Stocks is Stock traders dashboard Application created using Django Framework with postgres as the database.

## Features 
* Stock prices of over 8000 companies as listed on NASDAQ. 

* Implemented independent jenkins job which update stock prices of all the companies daily at 5:00 PM

*  Implemented independent jenkins job which updates Machine Learning models only of the companies which have been visited by the user. Updates every Monday at 7:00 AM

* The price predictions generated are real-time. The model takes into account the latest 60 days stock prices to make a dynamic prediction.

* Recent News of a particular stock are readily available right below the price prediction so that
user can make an informed decision based on the current news and trends.

* Implemented Continous Delivery using Rundeck 

* 

* Implemented Neural Networks with LSTM nodes for predictions using keras. With the structure : 60 - 50 - 50 - 1. The hidden layers are the LSTM nodes. Input and Ouput layers are Dense Nodes.





### Project Structure
![Project Structure](images/Smart_Stocks_Overview)


### Home Page
![Home](images/website_home.png)

### Dashboard
![DashBoard](images/website_dashboard.png)

### Stocks List
![Stocks List](images/website_stock_list.png)

### Stock Detail
![Stock Detail](images/website_stock_detail.png)

### Transaction
![Transaction](images/website_transaction.png)

### Stock Updater
![Stock Updater](images/jenkins_stock_updater.png)

### Model Updater
![Model Updater](images/jenkins_model_updater.png)



## CI/CD

### Jenkins Pipeline
![DashBoard](images/jenkins_pipeline.png)


### Rundeck
![DashBoard](images/rundeck_deploy.png)


### Kibana logs
![DashBoard](images/kibana_compose_logs.png)

### Metric Beat 
![DashBoard](images/kibana_metric_beat.png)