# `News classifier`

In order to help journalists to write articles faster and reduce errors when choosing an article 
category this project was created. It's the entire infrastructure to make this feature to work. 
Data was acquired from the guardian website, a couple of experiments conducted to obtain the best
ML model for the problem and a simple webpage created to test the app. Also, a routine using apache
airflow was developed to daily update the ML model and save the new metrics in order to increase its efficiency.


You can use the webpage at : https://google.com

Currently the API is able to classify texts from the follow categories :

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

## `Requirements`

<ul>
    <li>Python 3.7</li>
    <li>Pip/Conda</li>
    <li>A python virtual environment with all project dependencies</li>
    <li>MongoDB</li>
    <li>In order to run the API you'll also have to be using a Linux machine due to apache airflow and gUnicorn</li>
</ul>

## `Environment variables`

Create the follow environment variables with the MongoDB settings :

<ul>
    <li>MONGO_HOST</li>
    <li>MONGO_PORT</li>
 </ul>


## `Scraper`

The guardian website was used due to its simplicity to download the data from. 
The URLs follow a clear pattern : 'https://www.theguardian.com/{category}/{year}/{month}/{day}/'. 
Also, all the articles from a specific category and date are showed in a single URL.

If you want to run the scraper to get the data and train the model the script is available at :

https://github.com/marco-cardoso/news-classifier/blob/master/src/news_classifier/scraper/scraper.py

To run simply use :

    python scraper.py

This will download ten thousand articles for each category. Be patient, the execution takes several hours to finish.
If you want to change the amount of articles you can change the value in code.

The follow attributes are downloaded :

<ul>
    <li>Article category</li>
    <li>Article title</li>
    <li>Article content</li>
    <li>Article topics</li>
 </ul>


## `Experiments`

### `EDA`

After downloading the articles a simple EDA was conducted, you can see the results at :

https://github.com/marco-cardoso/news-classifier/blob/master/notebooks/eda.ipynb

### `Machine learning `

The ML notebook with the executed experiments is available at :

https://github.com/marco-cardoso/news-classifier/blob/master/notebooks/eda.ipynb


#### `Feature engineer`

Two transformations are necessary to train the model : The TfidfVectorizer to tokenize the article texts and
the LabelEncoder to convert the target values in numerical values.

#### `Best model`

To get the best model it was used the TPOT package to conduct an informative search. After several hours,
at the end of its execution the result estimator was : 

    LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001)
    
## `API`

The API python package is available at :

https://github.com/marco-cardoso/news-classifier/tree/master/src/news_classifier/webapp

It was developed with Flask. To run in a production environment you need to use a Linux machine
to use with gUnicorn.