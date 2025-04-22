# newz-aware

The growing problem in today's media is that almost every media outlet has some side of political bias to it. There is hardly any media website/channel that is 'neutral' in the true sense. Each one of them is split between either Right or Left. And this really creates an issue for the readers who are not, at the first glance, aware of the biases. This not only causes misunderstanding but also, on its extreme, can cause situations like riots.

Our idea was to help a reader understand and be aware of the kind of bias they are consuming. To do this, we thought of using predictive modeling to detect the bias of media sources. The data that we are using is centric to the political discourse in the USA. It is a crowdsourced dataset that has opinions of both sides (democrats and republicans) on a number of news articles. After building the model. We built a Flask App which fetches the latest news updates from News API (newsapi.org) and displays it along with the bias predicted.

For now, we don't believe it's perfect and we hope to improve and make it better in the future. Possible improvements could be, a more accurate model, a better UI that may also have separate categories for news portals, or different categories for according to the biases.

## Model

The Colab notebook can also be seen here: https://colab.research.google.com/drive/1jJodHw2iRdnTw_c0obmLNZPg1fPbNlcn?usp=sharing

Dataset for bias detection: https://deepblue.lib.umich.edu/data/concern/data_sets/8w32r569d?locale=en

There were seven fields in the dataset:

    1) Url
    2) News Type: Has three possible values: other (remember that the articles are sampled from those that are predicted to be political based on our classifiers and so there are false positives we remove based on this label), News, or Opinion.
    3) Perceived (whether the worker was looking at the blinded or unblinded version. perceived=1 means unblinded version)
    4) Primary topic identified by the worker (If "None", the primary topic is not captured by our list of 14 topics)
    5) Secondary topic (If "None", there is no secondary topic or the secondary topic is not captured by our list)
    6) Democratic party  vote
    7) Republican vote

Most of which were not of use to our purpose so we remove all columns except `Url`, `democrat.vote`, `republican.vote`

The votes have 5 possible values `['Negative', 'SomewhatNegative', 'Neutral', 'SomewhatPositive', 'Positive']` which we then label as `[-2,-1,0,1,2]`

Both of the votes are then merged into a single field in the following manner: `bias = democrat.vote - republican.vote`
So a more positive value points to a democrat bias and vice versa. So now the new labels were like this: `[-4,-3,-2,-1,0,1,2,3,4]`
We, then, again relabeled them as `[0,0,0,1,1,1,2,2,2]` where 0 corresponds to Right bias, 1 corresponds to Neutral and 2 corresponds to Left bias.
The model is then trained using these three labels.

## Setting up:

1. We recommend creating a virtual environment using `virtualenv`

2. Then all the requirements must be installed using `pip3 install -r requirements.txt`

3. You may have to download nltk.corpus.stopwords seperately. Use the following code:
    `import nltk`
    `nltk.download('stopwords')`

4. You may also have to download en_core_web_sm model seperately. Use the following code:
    `python -m spacy download en_core_web_sm`

5. One must run the `app.py` to get the website running. The rest of the directory structure is as follows:

    `static/` and `template/` folders are for the Flask app.

    `data.py` contains code to preprocess and scrape the dataset.

    `predicter.py` is the prediction module that can be used to predict for new data.

    `naiveBayesModel.pkl` and `tfidf_for_bias.pkl` are the saved prediction model and TF-IDF vectorizer, respectively.

    `TrainingData/` contains the data used for training, both raw and processed.
    
    `NaiveBayesmodelPrep.ipynb` is the notebook used for training the model on colab.
