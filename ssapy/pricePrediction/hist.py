import matplotlib.pyplot as plt

import numpy
 
from ssapy.pricePrediction.margDistSCPP import margDistSCPP

class hist(object):
    """
    An object to compute and hold self confirming price predictions
    using the bayesian update equations.
    NOTE: EVERY GOOD WILL HAVE THE SAME PRICE RANGE!!!!
    """
    def __init__(self, m = 5, minPrice = 0, maxPrice = 50, delta = 1):
        self.m = m
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.delta = delta
        # binEdges is 1d x price range
        self.binEdges = numpy.arange(minPrice,maxPrice+delta,delta)
        
        #counts is mD x price range
        self.counts = numpy.zeros((m,len(self.binEdges)-1))
        
    def binFromVal(self, val):
        if val < self.minPrice or val > self.maxPrice:
            raise ValueError("val = {0} not in histogram range".format(val))
        
        lowerBound = numpy.nonzero(self.binEdges < val)[0]
        
        if len(lowerBound) == 0:
            return 0
        else:
            return lowerBound[-1]
        
    def frequency(self,goodId,val):
        if goodId < 0 or goodId > self.m - 1:
            raise ValueError("goodID = {0} out of bounds".format(goodId))
        
        binIdx = self.binFromVal(val)
        return self.counts[goodId][binIdx]
        
    def upcount(self, goodId, val, mag = 1):
        if goodId < 0 or goodId > self.m - 1:
            raise ValueError("goodID = {0} out of bounds".format(goodId))
        
        binIdx = self.binFromVal(val)
        self.counts[goodId][binIdx]+=mag
        return
    
    def p(self,goodId):
        """
        Return a numpy array of probabilities from the counts
        """       
        a = self.area(goodId)
        
        return numpy.array(self.counts[goodId],dtype='float64')/a
                
    def area(self,goodId):
        if goodId < 0 or goodId > self.m - 1:
            raise ValueError("goodID = {0} out of bounds".format(goodId))
        
        a = 0.0
        for i in xrange(len(self.binEdges)):
            a += self.counts[goodId][i]*self.delta
            
        return a
                    
    def savenpz(self,filename):
        numpy.savez(filename,m=self.m,binEdges = self.binEdges, counts = self.counts)
        
    def saveCountsTxt(self,filename):
        numpy.savetxt(filename, self.counts)
    
    def saveBinEdgesTxt(self,filename):
        numpy.savetxt(filename, self.binEdges)
        
    def bayesMargDistSCPP(self):
        """
        Return a MargDistSCPP with distribution
        according to dirichlet formulation where alpha = [1 ... 1] 
        """
        tempDist = []
        for c in self.counts:
            tempDist.append( (numpy.atleast_1d((1 + c)/(len(c) + numpy.sum(c))), 
                          numpy.atleast_1d(self.binEdges)) )
            
        return margDistSCPP(tempDist)
                
    def graphPdf(self,**kwargs):
        """
        Function to plot the data using matplot lib
        """
        numpy.testing.assert_(len(self.binEdges),len(self.counts))
        
        if 'colorStyles' in kwargs:    
            numpy.testing.assert_(len(kwargs['colorStyles']), len(self.binEdges))
            
            colorStyles = kwargs['colorStyles']
        else:
            #pick some random colors
            cmap = plt.cm.get_cmap('hsv')
            colorStyles = [cmap(i) for i in numpy.linspace(0,0.9,len(self.counts))]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        for i in xrange(len(self.counts)):
            ax.plot(.5*(self.binEdges[i][:-1]+self.binEdges[i][1:]),self.counts[i],c=colorStyles[i],label='Slot {0}'.format(i))
            
        if 'xlabel' in kwargs:
            plt.xlabel(kwargs['xlabel'])
        else:
            plt.xlabel('Prices')
            
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'])
        else:
            plt.ylabel('Probability')
        
        if 'title' in kwargs:
            plt.title(kwargs['title'])
        else:
            plt.title('Price Distribution')
            

        leg = ax.legend(loc='best',fancybox=True)
        leg.get_frame().set_alpha(0.5)
        
        plt.show()
        
        