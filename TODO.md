* Find a way to decide initial threshould
    - Fourier
    - Find "basin" with brute force
        + Get histogram
        + Subtract each bin untill 60% of bins are empty
        + Get location of left side of right peak
        + Use it as threshold location
    - 128 cutoff actually works well