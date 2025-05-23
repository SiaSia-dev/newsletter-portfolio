# Ce script nettoie le fichier CSV contenant les posts LinkedIn en supprimant les doublons basés sur le titre et la date de publication.
# Il conserve la première occurrence de chaque doublon.

import pandas as pd

# Charger le CSV
df = pd.read_csv('linkedin_posts.csv')

# Afficher le nombre d'entrées avant nettoyage
print(f"Nombre d'entrées avant nettoyage: {len(df)}")

# Supprimer les doublons en conservant la première occurrence
df_clean = df.drop_duplicates(subset=['title', 'scheduled_time'], keep='first')

# Afficher le nombre d'entrées après nettoyage
print(f"Nombre d'entrées après nettoyage: {len(df_clean)}")

# Sauvegarder le fichier nettoyé
df_clean.to_csv('linkedin_posts_clean.csv', index=False)

# Pour remplacer l'original, décommentez la ligne suivante
# df_clean.to_csv('linkedin_posts.csv', index=False)