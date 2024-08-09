# Spotify songs analysis with lyrics

Database contains almost **300.000** records, It was created by me, in the steps presented in **dataset-creator.jpynb**. Around **~32.000** rows have its own unique **Lyrics** scraped from **genius.com**. However every row contains features like:<br>

- **Song Name**
- **Release Date**
- **Album Popularity**
- **Artist Popularity**
- **Song Popularity**
- **Artist Genres**
- **Language of Lyrics**
- **Duration**
- **Whether it is a solo song or with someone**
- Other technical features f.ex. **Loudness**, **Danceability**, **Liveness**, ...

<img src="db_management/other/ERD_songs.JPG">


One of the main purposes of this analysis is to see how different technical features vary across different **genres**, **languages** and other factors.<br><br>
Next thing that would be nice is checking how the **dictionary of words changes with years** in songs across different genres, what are the **most common words** in genres across years, and maybe find some other interesting aspects.<br>

# Data Cleaning

The data I've created was not exactly clean, I had to perform steps, where some of them were:

- Mapping the genres
- Dealing with missing data
- Simple feature engineering
- Finding the not obvious duplicates

# EDA

Next, I could take a deeper look into the dataset, checking the distributions, unique values and some simple relations between features.<br><br>
Some interesting insights were found, after I checked how the songs were changing in terms of technical features across the years. I investigated some of the changes, but **one of them was the most interesting and worrying.**

### Decreasing Valence (sentiment) Across Years
It looks like songs nowadays are getting more and more negative in terms of the sentiment.

<img src="figures/valence_levels.png">

I also investigated the average sentiment across the genres, and I found out that the **Raggae** is the most positive genre!

<img src="figures/valence_genres.png">

### Where do the songs come out usually?

Another interesting find was about the distribution of songs releases across the weekdays! **Friday seems to be the most popular day**

<img src="figures/days_releases.png">

# Lyrics Analysis

I also wanted really badly to see some trends or changes across the lyrics of different genres, so I investigated:

1. **The most frequent words across genres**

Rap seem to be filled with curse words, other genres on the other hand with love and expressions like "la la", "oh oh", ...

<img src="figures/word_clouds.png">

2. **The change in terms of curse words across the years**

The most worrying aspect is the increasing frequency of the curse words in songs over the years.

<img src="figures/curse_words_over_time.jpg">

# Clustering

I decided to perform clusterization on the data in order to find some groups of the songs that may be related in some technical way (The clusterization was based only on Spotify technical features).
As the data was quite memory exhaustive, I decided to go for KMeans algorythm, not only checking for the optimal amount of clusters via **Elbow Method**, but also using the algorythm to separate the groups.

### Elbow Method Results

It showed the most optimal number of clusters, equal 5.
<img src="figures/elbow_method.png">

### PCA Dimension Reduction

I reduced the dimensions to 3, keeping ~54% of the explainable variance in order to visualize the data and prevent the dimension curse.

### Clusterization Results

The perspective may be misleading, however the most populated cluster is the yellow (4th) one.

<img src="figures/cluster_3d.png">

### Clusters Interpretation

That's what I can say about the groups:

- **Cluster No. 0:**<br>Songs in this cluster are **little less energic**, and they are **varied in sentiment and acoustic** - (non-electronic) instruments. **Almost all of them are with lyrics** (no soundtracks) and in majority they are **quite danceable**.<br><br>
- **Cluster No. 1:**<br>This group being **the smallest cluster**, is found to have **the majority of electronic beats**, the songs are **the least danceable**, about **half of them are without the words** and they have **the least energy**. They are also **the most negative songs** from all the clusters.<br><br>
- **Cluster No. 2:**<br>From the aspects that make this group unique, we can notice **the most energic** songs, around **a half of them are live records**, they also have a **high tempo**.<br><br>
- **Cluster No. 3:**<br>This group is **quite energic**, **fully acoustic**, **the longest in duration** on average, **mostly danceable**, however with mostly **negative sentiment**.<br><br>
- **Cluster No. 4:**<br>The largest cluster, which have **the most danceable** songs with **lots of energy** and the **most positive sentiment**.

<img src="figures/cluster_distribution.png">





