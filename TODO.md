* Find a way to decide initial threshould
    - Fourier
    - Find "basin" with brute force
        + Get histogram
        + Subtract each bin untill 60% of bins are empty
        + Get location of left side of right peak
        + Use it as threshold location
    - 128 cutoff actually works well

* Identify the orientation of the form
    - Find tables
        + Find contours
        + Approximate contours into geometric shapes
        + Identify convex, rectangular countours
        + Sort these contours by size and use the largest n approximations as the tables
    - Find orientation of the tables
        + Find the longer sides and the shorter sides
        + for each long line, find another line (in endpoint notation) by taking a 97%-3% weighted average with the other long side
        + find a mathematical function for the new lines
        + traverse the new lines and take the total number of bright points along them respectively
        + whichever is brighter is on the left side, and so is the edge it's closer to
        + by inward orientation, we can define "right" as the direction of the other side
        + but his inward orientation thing isn't working too well. we still need to convert the two lines into mathematical functions in the form of `y=ax+b` and compare the value of `b` to see which "side" the second is on compared to the first.
        + it turns out that the four points returned by `cv2.approxPolyDP` are always in counterclockwise direction. what a twist!