"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a distribution price prediction.
"""
from pricePredicitonAgent import *
from auctionSimulator.hw4.pricePrediction.margDistSCPP import *

class margDistPredictionAgent(pricePredictionAgent):
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 margDistPricePrediction = None,
                 name = "Anonymous"):
        super(margDistPredictionAgent,self).__init__(m    = m,
                                                     v    = v,
                                                     l    = l,
                                                     vmin = vmin,
                                                     vmax = vmax,
                                                     name = name,
                                                     pricePrediction = margDistPricePrediction)
            
    @staticmethod
    def predictionType():
        return "margDistSCPP"
    
    @staticmethod
    def type():
        return "margDistPredictionAgent"
    
    def printSummary(self,args={}):
        """
        Print a summary of the agent's state to standard output.
        """
        super(margDistPredictionAgent,self).printSummary()
        
        assert 'margDistPricePrediction' in args or self.pricePrediction != None,\
            "Must specify a price prediction"
            
        pricePrediction = None
        
        if 'margDistPricePrediction' in args:
            
            assert isinstance(args['margDistPricePrediction'],margDistSCPP) or\
                isinstance(args['margDistPricePrediction'], tuple),\
                    "args['margDistPricePrediction'] must be a margDistSCPP or numpy.ndarray"
                    
            if isinstance(args['margDistPricePrediction'], margDistSCPP):
                
                pricePredicton = args['margDistPricePrediciton']
                
            elif isinstance(args['margDistPricePrediction'], tuple):
                
                pricePrediction = margDistSCPP(args['margDistPricePrediction'])
                
            else:
                print 'Should never get here'
                raise AssertionError
                
        else:
            pricePrediction = self.pricePrediction
            
        bundles = self.allBundles(self.m)
        
        valuation = self.valuation(bundles = bundles,
                                   v       = self.v,
                                   l       = self.l )
        
        expectePriceVector = pricePrediction.expectedPrices
        
        print 'Expected Price Vector = {0}'
        
        
    def bid(self, args={}):
        """
        Interface to bid.
        Accepts an argument of margDistPrediction which
        will take precidence over any stored prediction
        """
        
        bundles = self.allBundles(self.m)
        
        if 'margDistPrediction' in args:
            if isinstance(args['margDistPrediction'], margDistSCPP):
                
                return self.SS({'margDistPrediction':args['margDistPrediction'],
                                'bundles':self.allBundles(self.m),
                                'l':self.l,
                                'valuation': simYW.valuation(bundles,self.v,self.l)})
                
            elif isinstance(args['margDistPrediction'],tuple):
                
                return self.SS({'margDistPrediction':margDistSCPP(args['margDistPrediction']),
                                'bundles':self.allBundles(self.m),
                                'l':self.l,
                                'valuation': simYW.valuation(bundles,self.v,self.l)})
                
            else:
                print '----ERROR----'
                print 'pointPredictionAgent::bid'
                print 'unkown pointPricePrediction type'
                raise AssertionError
            
        else:
            assert isinstance(self.pricePrediction,pointSCPP),\
                "Must specify a price prediction to bid."
            return self.SS({'pointPricePrediction':self.pricePrediction,
                            'bundles':self.allBundles(self.m),
                            'l':self.l,
                            'valuation':simYW.valuation(bundles,self.v,self.l)})
                             
                
            
                                
        
                                   
                
                
                
                
                