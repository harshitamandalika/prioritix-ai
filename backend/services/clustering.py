from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster(texts, k=6):
    X = TfidfVectorizer(stop_words="english").fit_transform(texts)
    return KMeans(n_clusters=k, random_state=42).fit_predict(X)
