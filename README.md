# `ML News article classification architecture`

In order to help journalists to write articles faster and reduce errors when choosing an article 
category this project was created. It's the entire solution to make this feature work in a production environment.
The base model was trained using the data from the guardian website. The main focus of this project is the 
architecture, given the fact that the ML solution for the problem "News classification" is relatively simple. 

Currently, the API is able to classify texts from the following categories :

<ul>
    <li>Politics</li>
    <li>Environment</li>
    <li>Science</li>
    <li>Global Development</li>
    <li>Sport</li>
    <li>Culture</li>
    <li>Lifestyle</li>
    <li>Business</li>
</ul>

A simple EDA was conducted, you can look at the results in :

https://github.com/marco-cardoso/news-classifier/blob/master/notebooks/eda.ipynb

The notebook with the base model results is available at :

https://github.com/marco-cardoso/news-classifier/blob/master/notebooks/ml.ipynb


If you want to test the model, copy an article from any news website and paste in the webpage : http://3.131.248.252:8080


## `Scraper`

The Guardian website was used due to its simplicity to download the data from. 
The URLs follow a clear pattern : 'https://www.theguardian.com/{category}/{year}/{month}/{day}/'. 
Also, all the articles from a specific category and date are showed in a single URL.

If you want to run the scraper to get the data to train the model the script is available at :

https://github.com/marco-cardoso/news-classifier/blob/master/packages/news_classifier/news_classifier/scraper/scraper.py


The following attributes are downloaded :

<ul>
    <li>Article category</li>
    <li>Article title</li>
    <li>Article content</li>
    <li>Article topics</li>
 </ul>
 
## `ML model`


#### `Feature engineer`

The only performed transformation over the data is the transformer TfidVectorizer.

#### `Best model`

To get the best model it was used the TPOT package to conduct an informative search. After several hours,
at the end of its execution the resulting estimator was : 

    LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001)
    

## `System architecture`

### `Overview`

![alt text](https://github.com/marco-cardoso/news-classifier/blob/master/news_classifier_arch.jpg)


<ul>
    <li>Nginx container - Responsible to handle the requests and send them to the Flask API </li>
    <li>Flask container - Responsible to serve the webpage and the ML model</li>
    <li>CRON container - Responsible to update the model with new articles from the guardian website daily</li>
    <li>Mongo container - Where the articles are stored and loaded by the CRON routine to train the model</li>
    <li>MLFlow container - Responsible to store the metrics from the latest model produced by the CRON container</li>
</ul>

### `Modularization`

It was decided to separate the app in two python packages : A module with everything related to the API and another with the 
functions related to ML and the jupyter notebooks.

Docker uses them to build the containers. 

Both are available at : https://github.com/marco-cardoso/news-classifier/tree/master/packages 

The flask container uses the API package to run the flask app using gunicorn as server and the ML package (news_classifier) to
use the method to load the ML model from S3. The CRON container uses just the last one to fetch the data from mongo/train the 
model and generate the evaluation metrics.

### `Stored metrics`

In order to evaluate the model a KFold is performed using 5 folds. For each fold, the accuracy, precision, recall and f1 score are calculated.
MLFlow saves them and their mean and standard deviation. 

https://github.com/marco-cardoso/news-classifier/blob/master/packages/news_classifier/news_classifier/models/evaluate.py


## `Docker`

Requirements
<ul>
    <li>At least dockver v19.03.12 </li>
    <li>At least docker-compose v1.26.2</li>
    <li>An AWS account with an IAM user that has full access to S3.</li>
</ul>

Environment variables

<ul>
    <li>AWS_S3_BUCKET_NAME - Your AWS S3 bucket name to save the ML models in </li>
    <li>AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY with full access to the above bucket</li>
</ul>

After the requirements are satisfied open a terminal in the project root folder and type :

    docker-compose up --build
    
## `Warning`

Ideally, the best architecture would be a separated instance for MLFLOW, MONGO, and CRON containers. With more
attention to the last one, given the fact that is responsible to load thousands of MongoDB documents and train
the latest model, using a lot of RAM memory and CPU power. Nonetheless, this architecture was chosen for simplicity and to
reduce the costs on AWS, since only one instance is enough due to the low amount of user requests.
