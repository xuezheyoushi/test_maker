* Find a way to decide initial threshold
    - Fourier
    - Find "basin" with brute force
        + Get histogram
        + Subtract each bin until 60% of bins are empty
        + Get location of left side of right peak
        + Use it as threshold location
    - 128 cutoff actually works well
    - Gaussian Adaptive

* Get the form
    - Find tables
        + Find contours
        + Approximate contours into geometric shapes
        + Identify convex, rectangular contours
        + Sort these contours by size and use the largest n approximations as the tables
    - Find orientation of the tables
        + Establish four edges
        + For each edge, find an offset to the outer side by taking `x = x-min+1.056(x-max - x-min)`, `y` alike.
        + Find the mid point of each new edge. Traverse the square (4% of the distance between opposing edges).
        + The side with brighter square is the right side
        + Define all edges by counterclockwise orientation
        + Do perspective transformation. Four corners are (764,307) (49,307) (49,1128) (764,1128). Canvas size is 785 by 1240.

* Read the form
    - Corp datamatrix region
    - Scan datamatrix
    - Segment form
        + 87-227, 266-406, 446-586, 624-764
        + 306-1126
    - Corp each grid
    - Clean edges of each grid
    - Find the last letter in each grid
    - Read the letter
    - Write to object