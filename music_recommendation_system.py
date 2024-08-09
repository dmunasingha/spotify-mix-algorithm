import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Sample data
# User-item interaction matrix (rows: users, columns: items)
user_item_matrix = pd.DataFrame({
    'Song1': [5, 4, 0, 0],
    'Song2': [0, 0, 3, 4],
    'Song3': [0, 0, 0, 0],
    'Song4': [1, 1, 0, 0],
    'Song5': [0, 0, 2, 3],
    'Song6': [0, 0, 0, 0]
}, index=['User1', 'User2', 'User3', 'User4'])

# Content-based data (features for each song)
track_features = pd.DataFrame({
    'Song1': ['Rock, Upbeat'],
    'Song2': ['Jazz, Relaxing'],
    'Song3': ['Pop, Dance'],
    'Song4': ['Classical, Calm'],
    'Song5': ['Pop, Dance'],
    'Song6': ['Rock, Upbeat']
}).T
track_features.columns = ['Features']

# User profile (songs the user likes)
user_profile = ['Rock, Upbeat', 'Pop, Dance']

# Collaborative Filtering


def collaborative_filtering(user_item_matrix):
    # Compute similarity between users
    user_similarity = cosine_similarity(user_item_matrix.fillna(0))
    np.fill_diagonal(user_similarity, 0)
    return user_similarity


def get_recommendations_collaborative(user_index, user_item_matrix, user_similarity):
    similar_users = user_similarity[user_index]
    similar_users_index = np.argsort(similar_users)[::-1]
    recommendations = user_item_matrix.iloc[similar_users_index].mean(axis=0)
    recommendations = recommendations[user_item_matrix.iloc[user_index] == 0]
    return recommendations.sort_values(ascending=False)

# Content-Based Filtering


def content_based_filtering(track_features, user_profile):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(
        track_features['Features'].tolist() + user_profile)
    cosine_similarities = linear_kernel(
        tfidf_matrix[-len(user_profile):], tfidf_matrix[:-len(user_profile)])
    recommendations = np.argsort(cosine_similarities.mean(axis=0))[::-1]
    return recommendations


# Calculate collaborative filtering recommendations
user_similarity = collaborative_filtering(user_item_matrix)
user_index = 0  # Index for 'User1'
collaborative_recommendations = get_recommendations_collaborative(
    user_index, user_item_matrix, user_similarity)

# Calculate content-based filtering recommendations
content_based_recommendations = content_based_filtering(
    track_features, user_profile)

# Display results
print("Collaborative Filtering Recommendations:")
print(collaborative_recommendations)

print("\nContent-Based Filtering Recommendations:")
print(track_features.index[content_based_recommendations])
