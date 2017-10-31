import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math

mu = 40662
variance = 4893.25
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)

mu1 = 19499
variance1 = 1322.63
sigma1 = math.sqrt(variance1)
x1 = np.linspace(mu1 - 3*sigma1, mu1 + 3*sigma1, 100)

mu2 = 30766.50
variance2 = 3317.66
sigma2 = math.sqrt(variance2)
x2 = np.linspace(mu2 - 3*sigma2, mu2 + 3*sigma2, 100)

plt.plot(x2,mlab.normpdf(x2, mu2, sigma2),'g')#,x1,mlab.normpdf(x1, mu1, sigma1),'b',x2,mlab.normpdf(x2, mu2, sigma2),'g')
plt.show()

	