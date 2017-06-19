from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from xgboost import XGBClassifier


class SklearnClassifierWrapper(object):
    def __init__(self, model, tfidf=False, ngram_n=1):
        """
        Classifier made up of a pipeline with a count vectorizer + given model
        :param model: a sklearn-like classifier (with fit, predict and predict_proba)
        :param tfidf: if True wil use TfidfVectorizer, otherwise CountVectorizer; defaults to False
        """
        vectorizer_class = TfidfVectorizer if tfidf else CountVectorizer
        vectorizer = vectorizer_class(
                preprocessor=lambda x: map(str, x),
                tokenizer=lambda x: x,
                ngram_range=(1, ngram_n))

        self.clf = Pipeline([('vectorizer', vectorizer), ('model', model)])
        self.name = "SklearnClassifierWrapper(tfidf=%s)" % tfidf

    def fit(self, X, y):
        self.clf.fit(X, y)
        return self

    def predict_proba(self, X):
        return self.clf.predict_proba(X)

    def predict(self, X):
        return self.clf.predict(X)

    def __str__(self):
        return self.name


class MultNB(SklearnClassifierWrapper):
    def __init__(self, tfidf=False, ngram_n=1):
        super(MultNB, self).__init__(MultinomialNB(), tfidf, ngram_n)
        self.name = "MultinomialNB(tfidf=%s, ngram_n=%s)" % (tfidf, ngram_n)


class BernNB(SklearnClassifierWrapper):
    def __init__(self, tfidf=False, ngram_n=1):
        super(BernNB, self).__init__(BernoulliNB(), tfidf, ngram_n)
        self.name = "BernoulliNB(tfidf=%s, ngram_n=%s)" % (tfidf, ngram_n)


class SVM(SklearnClassifierWrapper):
    def __init__(self, tfidf=False, ngram_n=1, kernel='linear'):
        super(SVM, self).__init__(SVC(kernel=kernel), tfidf, ngram_n)
        self.name = "SVC(tfidf=%s, ngram_n=%s, kernel=%s)" % (tfidf, ngram_n, kernel)


class XGB(SklearnClassifierWrapper):
    def __init__(self, tfidf=False, ngram_n=1):
        super(XGB, self).__init__(XGBClassifier(), tfidf, ngram_n)
        self.name = "XGBClassifier(tfidf=%s, ngram_n=%s)" % (tfidf, ngram_n)
