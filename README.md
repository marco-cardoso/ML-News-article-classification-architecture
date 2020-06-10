# `Project goal`

Create a machine learning solution to automatically
classify texts from news websites over a few categories :

<ul>
    <li>Politics</li>
    <li>Environment</li>
    <li>Science</li>
    <li>Global Development</li>
    <li>Sport</li>
    <li>Culture</li>
    <li>Lifestyle</li>
    <li>Tech</li>
    <li>Business</li>
</ul>


### Steps

<ul>
    <li>Create a scraper to download news from The Guardian website</li>
    <li>Analyse the downloaded data</li>
    <li>Create and evaluate a NLP solution to classify the articles</li>
    <li>Create a Flask API and webpage to allow users to use the model using a browser</li>
    <li>Deploy the API on AWS</li>
</ul>

#### Create a scraper to download news from The Guardian website

The guardian website was used due to its simplicity to download the data from. The URLs follow a clear pattern : 'https://www.theguardian.com/{category}/{year}/{month}/{day}/'. Also, all the articles from a specific category and date are showed in a single URL. 
