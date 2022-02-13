# btseg

Library for transformation and treatment of images as time series, as well as a series of algorithms for clustering and regression applied to these series.


## Abstract

Within the category of tumors with primary location in the brain, gliomas are the most common and aggressive, with a high mortality rate. Identification of these tumors along with early treatment is the key to patient care.
This work proposes the transformation of images of these tumors into time series, descriptors of tumor shape, and the application of clustering algorithms for pattern analysis using DTW and Euclidean distances. The models used were
able to obtain a Silhouette coefficient of 0.58 using the DTW measure and 0.47 using the Euclidean distance. 48% of the instances were grouped into 3 clusters that describe similarities in tumor size and shape. These results are preliminary and still need to be discussed with domain experts to verify the patterns found

## Steps

1. Region selection
2. Gaussian blur
3. Canny edge
4. Dilate, Erode
5. Edge Descriptor (Time series transform)

## Clustering Algorithms

- HDBSCAN
  - Score metric: `Silhouette Score`
