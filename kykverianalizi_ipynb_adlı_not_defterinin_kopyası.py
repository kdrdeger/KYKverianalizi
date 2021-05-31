# -*- coding: utf-8 -*-
"""Untitled0.ipynb adlı not defterinin kopyası

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NMPNLxGehF7kPgC8BIN4jsxMvZUxl46f
"""

from google.colab import drive
drive.mount('/content/drive/') 
#mount drive ı colaba sanal disk olarak eklemektir.Mount işlemi bir kez yapılır.

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/My Drive/Colab Notebooks'

!ls

import pandas as pd

df = pd.read_csv("KYK.csv")

df.head(20)

df.shape

df = df.drop("Unnamed: 0", axis = 1)

df['text'] = df['text'].str.replace(r'http\S+', '')

df.head(10)

df['text'] = df['text'].str.replace(r'@\S+', '')

df.head(10)

df['text'] = df['text'].str.replace(r'#\S+', '')

df.head(10)

df['text'] = df['text'].str.replace('gt', '')

df['text'].head()

df['text'] = df['text'].str.replace('[^\w\s]','')

df.head()

df.tail()

df['text'] = df['text'].str.replace('\d','')

df.head()

!pip install nltk

import nltk

nltk.download("stopwords")

from nltk.corpus import stopwords

sw = stopwords.words("turkish")

sw

df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))

df.head()

pd.Series(" ".join(df['text']).split()).value_counts()

silenebilecek_kelimeler = pd.Series(" ".join(df['text']).split()).value_counts()[-10:]

pd.Series(" ".join(df['text']).split()).value_counts()[-10:]

nltk.download("punkt")

!pip install textblob

import textblob
from textblob import TextBlob

TextBlob(df['text'][0]).words

df['text'].apply(lambda x: TextBlob(x).words)

from snowballstemmer import TurkishStemmer
turkStem = TurkishStemmer()

df['text'].apply(lambda x: " ".join([turkStem.stemWord(i) for i in x.split()]))

df['text']

freq_df = df["text"].apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()

freq_df.columns = ["kelimeler", "frekanslar"]
print(freq_df.head())

import matplotlib.pyplot as plt

print("En sık geçen kelimelerin görselleştirilmesi : \n")
a = freq_df[freq_df.frekanslar > freq_df.frekanslar.mean() + freq_df.frekanslar.std()]
plt.bar(a["kelimeler"].head(5), a["frekanslar"].head(5))
plt.show()

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

text = " ".join(i for i in df.text)
print("Kelime bulutunun oluşturulması : \n")
wordcloud = WordCloud(background_color = "white").generate(text)
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()

df["text"]

df.to_csv('KYK_temiz.csv')

df=pd.read_csv("KYK_temiz.csv")

df.shape

dftrain = pd.read_csv("makineöğrenmesi.csv")

dftrain.head()

dftrain.shape

dftrain.groupby("category").size()

dftrain['labels'] = pd.factorize(dftrain.category)[0]

dftrain.groupby(["category", "labels"]).size()

dftrain

model_df = dftrain[["text", "labels"]]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(model_df["text"], model_df["labels"], test_size = 0.2, random_state = 4)

X_train.shape

y_train.shape

X_test.shape

y_test.shape

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

train_vectors = vectorizer.fit_transform(X_train)
test_vectors = vectorizer.transform(X_test)
print(train_vectors.shape, test_vectors.shape)

print(train_vectors)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import seaborn as sns

clf = MultinomialNB()
clf.fit(train_vectors, y_train)
prediction = clf.predict(test_vectors)
print("Naive Bayes ::\n", confusion_matrix(y_test, prediction),"\n")
print(accuracy_score(y_test, prediction))

LogicReg = LogisticRegression()
LogicReg.fit(train_vectors, y_train)
prediction = LogicReg.predict(test_vectors)
print("Logistic Regression ::\n", confusion_matrix(y_test, prediction),"\n")
print(accuracy_score(y_test, prediction))

dTmodel = DecisionTreeClassifier()
dTmodel.fit(train_vectors, y_train)
prediction = dTmodel.predict(test_vectors)
print("DecisionTree ::\n", confusion_matrix(y_test, prediction),"\n")
print(accuracy_score(y_test, prediction))

rForest = RandomForestClassifier()
rForest.fit(train_vectors,y_train)
prediction=rForest.predict(test_vectors)
print("RandomForest ::\n",confusion_matrix(y_test,prediction),"\n")
print(accuracy_score(y_test, prediction))

grBoosting = GradientBoostingClassifier()
grBoosting.fit(train_vectors, y_train)
prediction = grBoosting.predict(test_vectors)
print("GradientBoosting ::\n", confusion_matrix(y_test, prediction), "\n")
print(accuracy_score(y_test, prediction))

xgboost = XGBClassifier()
xgboost.fit(train_vectors,y_train)
prediction=xgboost.predict(test_vectors)
print("xgboost ::\n",confusion_matrix(y_test,prediction), "\n")
print(accuracy_score(y_test, prediction))

scores = cross_val_score(clf, train_vectors, y_train, cv = 5)
print("Accuracy for Naive Bayes: mean: {0:.2f} 2sd: {1:.2f}".format(scores.mean(),scores.std() * 2))
print("Scores::",scores)
print("\n")

scores2 = cross_val_score(LogicReg, train_vectors, y_train, cv = 5)
print("Accuracy for Logistic Regression: mean: {0:.2f} 2sd: {1:.2f}".format(scores2.mean(),scores2.std() * 2))
print("Scores::",scores2)
print("\n")

scores3 = cross_val_score(dTmodel,train_vectors,y_train,cv=5)
print("Accuracy for Decision Tree: mean: {0:.2f} 2sd: {1:.2f}".format(scores3.mean(),scores3.std() * 2))
print("Scores::",scores3)
print("\n")

scores4 = cross_val_score(rForest,train_vectors,y_train,cv=5)
print("Accuracy for Random Forest: mean: {0:.2f} 2sd: {1:.2f}".format(scores4.mean(),scores4.std() * 2))
print("Scores::",scores4)
print("\n")

scores5 = cross_val_score(grBoosting,train_vectors,y_train,cv=5)
print("Accuracy for Gradient Boosting: mean: {0:.2f} 2sd: {1:.2f}".format(scores5.mean(),scores5.std() * 2))
print("Scores::",scores5)
print("\n")

scores6 = cross_val_score(xgboost, train_vectors, y_train,cv = 5)
print("Accuracy for Xgboost: mean: {0:.2f} 2sd: {1:.2f}".format(scores6.mean(),scores6.std() * 2))
print("Scores::",scores6)
print("\n")

methods = ["Naive Bayes", "Logistic Regression", "Decision Tree", "Random Forest", "Gradient Boosting", "XGBoost"]
accuracy = [scores.mean(), scores2.mean(), scores3.mean(), scores4.mean(), scores5.mean(), scores6.mean()]

sns.set()
plt.figure(figsize = (16, 9))
plt.ylabel("Uygulanan Algoritmalar")
plt.xlabel("Başarı")
sns.barplot(x = accuracy, y = methods, palette = "vlag")


for line in range(len(methods)):
     plt.text(0.65, line-0.15, "{:.2f}%".format(accuracy[line]*100), horizontalalignment = 'left', size = 'large', color = "black")

test_vectors_ = vectorizer.transform(df["text"].astype('U').values)
print(test_vectors_.shape)

print(test_vectors_)

predicted = LogicReg.predict(test_vectors_)
tahmin = pd.DataFrame(predicted)
tahmin.rename(columns = {0:'tahmin'}, inplace = True)
df["tahmin_logistic"] = tahmin    ###### logistic regresyon tahmin

df.head(20)

df.loc[df['tahmin_logistic'] == 0, ['tahmin_category_logistic']] = 'burs'
df.loc[df['tahmin_logistic'] == 1, ['tahmin_category_logistic']] = 'tepki'
df.loc[df['tahmin_logistic'] == 2, ['tahmin_category_logistic']] = 'bağımsız'
df.loc[df['tahmin_logistic'] == 3, ['tahmin_category_logistic']] = 'borç' ##tablo ekleme

df.head(20)

df.groupby("tahmin_category_logistic").size()

predicted = clf.predict(test_vectors_)
tahmin = pd.DataFrame(predicted)
tahmin.rename(columns = {0:'tahmin'}, inplace = True)
df["tahmin_naive_bayes"] = tahmin ### naive bayes

df.head(20)

df.loc[df['tahmin_naive_bayes'] == 0, ['tahmin_category_nb']] = 'burs'
df.loc[df['tahmin_naive_bayes'] == 1, ['tahmin_category_nb']] = 'tepki'
df.loc[df['tahmin_naive_bayes'] == 2, ['tahmin_category_nb']] = 'bağımsız'
df.loc[df['tahmin_naive_bayes'] == 3, ['tahmin_category_nb']] = 'borç'

df.groupby("tahmin_category_nb").size() ### tahmin yönetimine göre toplan tweet dağılımları

pd.set_option("max_colwidth", None)
df.head(20)

df.to_csv("kategorileştirilmiştablo.csv")

### duygu analizi

df.shape

data = pd.DataFrame(df["text"])

data.head()

data["text"] = data["text"].apply(lambda r: str(r))

!pip install transformers

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model = AutoModelForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
sa= pipeline("sentiment-analysis", tokenizer = tokenizer, model = model)

sentiment_list = []
for i in data["text"]:
    sentiment_list.append(sa(i))

sentiment_list

spredict_list = []
for i in range(0, len(sentiment_list)):
    spredict_list.append(sentiment_list[i][0])

spredict_list

spredict_list = pd.DataFrame(spredict_list)

spredict_list.head()

data["label"] = spredict_list["label"]
data["score"] = spredict_list["score"]

data.head(10)

data.groupby("label").size()

df.head()

data.head()

df["sentiment"] = data["label"]

df.head()

grup_logis = df.groupby(["tahmin_category_logistic", "sentiment"]).size()

grup_logis = pd.DataFrame(grup_logis).reset_index()

grup_logis

grup_logis.rename(columns = {0:'tweet_sayisi'}, inplace = True)

sns.catplot(x = "tahmin_category_logistic", y = "tweet_sayisi", hue = "sentiment", kind = "bar", data = grup_logis)

grup_nb = df.groupby(["tahmin_category_nb", "sentiment"]).size()

grup_nb = pd.DataFrame(grup_nb).reset_index()

grup_nb

grup_nb.rename(columns = {0:'tweet_sayisi'}, inplace = True)

sns.catplot(x = "tahmin_category_nb", y = "tweet_sayisi", hue = "sentiment", kind = "bar", data = grup_nb)

df.to_csv("duyguanalizi.csv")