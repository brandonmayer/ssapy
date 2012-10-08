"""
An agent to bid local marginal revenue given a joint distribution
"""

from ssapy.agents.margDistPredictionAgent import margDistPredictionAgent
import ssapy.agents.agentFactory

import numpy
import matplotlib.pyplot as plt

class localBid(margDistPredictionAgent):
    def __init__(self,**kwargs):
        #put import in init to avoid circlular imports when
        #agentFactory imports localbid
        from ssapy.agents.agentFactory import agentFactory
        
        super(localBid, self).__init__(**kwargs)
        
    @staticmethod
    def type():
        return "localBid"
    
    @staticmethod
    def SS(**kwargs):
        
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("localBid.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("localBid.SS(...) - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("localBid.SS(...) - must specify l (target number of time slots)")
        
        samples = kwargs.get('samples')
        
        viz = kwargs.get('viz',False)

        
        if samples is None:
            
            pricePrediction = kwargs.get('pricePrediction')
        
            if pricePrediction == None:
                raise KeyError("localBid.SS(...) - must specify pricePrediction")
        
            nSamples = kwargs.get('nSamples', 10000)
            
            samples = pricePrediction.sample(n_samples = nSamples)
                       
        n_itr = kwargs.get('n_itr', 100)
            
        initialBidderType = kwargs.get('initialBidder','straightMU8')
        
        
        #to avoid circular import (NameError exception)
        initialBidder = ssapy.agents.agentFactory.agentFactory(agentType = initialBidderType,
                                                               m = bundles.shape[1])
            
        bids = initialBidder.SS(pricePrediction = pricePrediction,
                                bundles = bundles,
                                valuation = valuation,
                                l = l)
            
        del initialBidder
            
          
        verbose = kwargs.get('verbose',False)
        
        if viz and samples.shape[1] == 3:
            from mpl_toolkits.mplot3d import axes3d
    
        bundleValueDict = dict([(tuple(b),v) for b, v in zip(bundles,valuation)])
        
        del valuation
        
        for itr in xrange(n_itr):
            
            if verbose:
                print "itr = {0}, bid = {1}".format(itr,bids)
                
            if viz:
                if samples.shape[1] == 2:
                    plt.figure()
                    plt.plot(samples[:,0],samples[:,1],'go', markersize =  10)
                    plt.plot(bids[0],bids[1],'ro', markersize = 10)
                    plt.axvline(x = bids[0], ymin=0, ymax = bids[1], color = 'b')
                    plt.axvline(x = bids[0], ymin = bids[1], color = 'r')
                    plt.axhline(y = bids[1], xmin = 0, xmax = bids[0], color = 'b')
                    plt.axhline(y = bids[1], xmin = bids[0], color = 'r')
                    
                    plt.show()
                elif samples.shape[1] == 3:
                    fig = plt.figure()
                    ax = fig.gca(projection='3d')
                    ax.plot(samples[:,0],samples[:,1],samples[:,2],'go')
                    ax.plot([bids[0]], [bids[1]], [bids[2]],'bo')
                    
                    
                    plt.show()
                    
            for bidIdx in xrange(bids.shape[0]):
                
                goodsWon = samples <= bids
            
                newBid = 0.0
                for bundle in bundles[bundles[:,bidIdx] == True]:
                    
                    bundleCopy = bundle.copy()
                    bundleCopy[bidIdx] = False
                    
                    v1 = bundleValueDict[tuple(bundle)]
                    v0 = bundleValueDict[tuple(bundleCopy)]

                    p = numpy.float( numpy.count_nonzero( numpy.all(numpy.delete(goodsWon,bidIdx,1) == numpy.delete(bundle,bidIdx),1) ) ) / nSamples                    

                    if p > 1.0:
                        raise ValueError("p > 1.0")
                    elif p < 0.0:
                        raise ValueError("p < 0.0")
#                    bids[bidIdx] = (v1 - v0)*p
                    newBid += (v1 - v0)*p
                    
                    if verbose:
                        print ''
                        print "bid index = {0}".format(bidIdx)
                        print "bundle    = {0}".format(bundle)
                        print "v1        = {0}".format(v1)
                        print "v0        = {0}".format(v0)
                        print "p         = {0}".format(p)    
                        print "new Bid   = {0}".format(newBid)
                    
                bids[bidIdx] = newBid
                      
        return bids
    

        
if __name__ == "__main__":
    from simYW import simYW
    from sklearn.datasets import make_blobs
    import sklearn
    from ssapy.pricePrediction.jointGMM import jointGMM
    m=3
    
#    p1 = numpy.random.random(50)
#    p1 /= sum(p1)
#    
#    p2 = numpy.random.random(50)
#    p2 /= sum(p2)
    
    v, l = simYW.randomValueVector(0, 50, m, l = 1)
    
    print "v = {0}".format(v)
    print "l = {0}".format(l)
    
    bundles = simYW.allBundles(nGoods=m)
    
    valuation = simYW.valuation(bundles, v,l)
    
    pricePrediction = jointGMM(n_components=3)
    
#    x,y = make_blobs(n_samples=1000,centers = [[5,5],[15,20],[20,30]], n_features = 2)

#    x,y = make_blobs(n_samples=1000, centers = [5,5], n_features = 2)
    
    x,y = make_blobs(n_samples=1000, centers = [5,5,5], n_features = 3)
    
    pricePrediction.fit(x)
    
    bids = localBid.SS(bundles = bundles,
                       valuation = valuation,
                       pricePrediction=pricePrediction,
                       l = l,
                       verbose = True,
                       nSamples = 1000,
                       viz = True)
    
    print bids
    
    
    
    
    
    
    
                    
                    
        
        
        