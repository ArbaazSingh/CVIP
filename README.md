HOUGH TRANSFORM TO DETECT CIRCLES

INTRODUCTION

This Project detects the boundary points of the object in a given image. By appliying Hough Transform techniques on an image, here we find the coordinates of location of the center and radius of the circular coins (objects) in the given image by finding the local maxima from an accumulator which helps in storing the values of the radii and coordinates of the coin circles. We have used techniques like threshold so as to obstruct the unwanted intensity values in the image like noise, convolution, Sobel edge detecting the edges of the coins and further using the gradient obtained to obtain smoother edges and morphological operations of opening and closing for removal of spurious edges. We have mainly used the algorithm given in textbook as a guideline, a few reference papers and other informative pages over the net for detecting the coins in the image. The algorithm was used along with the material provided by the TAs.
