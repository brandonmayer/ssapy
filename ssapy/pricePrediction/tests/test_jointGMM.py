import unittest
import numpy

from ssapy.pricePrediction.jointGMM import jointGMM, expectedSurplus_
from ssapy import listBundles, msListRevenue

class test_jointGMM(unittest.TestCase):
    def test_expectedSurplus(self):
        """
        [20,15] -> (45 - 35)*.1
        [20,20] -> (45 -40)*.4
        [30,15] -> (20 - 5)*.1
        [30,20] -> (20 - 20)*.4
        Expected Surplus = 3.5
        """
        samples = numpy.zeros((1000,2))
        samples[:100,:] = numpy.asarray([20,15])
        samples[100:500,:] = numpy.asarray([20,20])
        samples[500:600,:] = numpy.asarray([30,15])
        samples[600:,:] = numpy.asarray([30,20])
        
        m=2
        l = 1
        v = [45,20]
        bundles = listBundles(m)
        revenue = msListRevenue(bundles, v, l)
        bids = numpy.asarray([25.,25.])
        
        bundleRevenueDict = {}
        for b,r in zip(bundles,revenue):
            bundleRevenueDict[tuple(b)] = r
        
        numpy.testing.assert_equal(expectedSurplus_(bundleRevenueDict, bids, samples), 
                                   3.5,'test_expetedSurplus failed.',True)
        
#    def test_sample(self):
#        gmm = jointGMM()
#        gmm.means_ = [[ 48.41402471,  30.5908699 ],
#                      [ 42.93731853,  34.58536048],
#                      [ 38.72492684,  24.16033562],
#                      [ 41.4871379 ,  27.43753048],
#                      [ 45.15150561,  14.50717192],
#                      [ 39.71479352,  31.18738702],
#                      [ 45.41463378,  26.41640807],
#                      [ 49.45902817,  23.53030799],
#                      [ 46.11180899,  39.16310403],
#                      [ 32.78321124,  23.72181697],
#                      [ 41.58839008,  20.92660492],
#                      [ 38.57483844,  15.41527355],
#                      [ 29.87387647,  18.39325022],
#                      [ 36.96699902,  34.83455367],
#                      [ 46.89898057,  33.22991496],
#                      [ 39.30686975,  40.42007866],
#                      [ 43.94138924,  25.95430248],
#                      [ 47.07110218,  20.10626734]]
#        gmm.covars_ = [[[  1.29656216,   2.45266345],
#                        [  2.45266345,  29.71094679]],
#                       [[  6.80848574,  -1.42711381],
#                        [ -1.42711381,   7.00887001]],
#                       [[ 12.40465323,  -5.53359661],
#                        [ -5.53359661,  31.09824363]],
#                       [[  9.38159391,   2.116949  ],
#                        [  2.116949  ,  24.70753018]],
#                       [[  4.6911179 ,   0.17465264],
#                        [  0.17465264,  21.45504305]],
#                       [[ 25.19870698, -25.31172571],
#                        [-25.31172571,  26.20189918]],
#                       [[  3.53077432,  -3.27734521],
#                        [ -3.27734521,  27.05114751]],
#                       [[  0.49687415,   0.09528951],
#                        [  0.09528951,  63.75057013]],  
#                       [[  4.72963058,   1.66127273],
#                        [  1.66127273,   4.07866752]],  
#                       [[ 10.59324755,   5.04773267],
#                        [  5.04773267,  32.03164901]],
#                       [[  7.936722  ,  -1.79034109],
#                        [ -1.79034109,  33.81745405]],
#                       [[ 17.55899819,   6.05534456],
#                        [  6.05534456,  22.7125158 ]],
#                       [[ 34.7837725 ,  19.43484339],
#                        [ 19.43484339,  43.34268261]],
#                       [[ 14.10886376,   0.20447547],
#                        [  0.20447547,   9.2484    ]],
#                       [[  2.80453047,   2.34447133],
#                        [  2.34447133,  13.38485029]],
#                       [[ 20.73527187,   0.74032769],
#                        [  0.74032769,   2.21729856]],
#                       [[  5.61343209,  -0.95496488],
#                        [ -0.95496488,  31.67488688]],
#                       [[  2.09208383,  -1.91572869],
#                        [ -1.91572869,  35.2069763 ]]]
#
#        gmm.weights_ = [ 0.06410558,  0.06779558,  0.04325746,  0.04129004,  0.02871967,
#        0.11101513,  0.05664961,  0.11412986,  0.04675616,  0.04103483,
#        0.05252711,  0.03388091,  0.01707661,  0.05589717,  0.0437608 ,
#        0.0667707 ,  0.04780162,  0.06753115]
#        
#        gmm.weights_ = numpy.atleast_1d(gmm.weights_)
#        gmm.covars_  = numpy.atleast_3d(gmm.covars_)
#        gmm.means_   = numpy.atleast_2d(gmm.means_)
#        
##        gmm.sample(n_samples = 10000)
#        
#        gmm.heatMap()
#        pass
#    
    def test_cdf(self):
        means = numpy.atleast_2d([[3,5] ,[18,10]])
        covars = []
        covars.append(numpy.eye(2,2))
        covars.append(numpy.eye(2,2)*4)
        covars = numpy.array(covars)
        weights = [0.3,0.7]
        weights = numpy.array(weights)
        
        jgmm = jointGMM(n_components = 2)
        jgmm.weights_ = weights
        jgmm.means_ = means
        jgmm.covars_ = covars
        
        N = 100
        xmin = 0
        xmax = 30
        xx, ds = numpy.linspace(xmin, xmax, N, retstep = True)
    
        p = numpy.zeros((N,N))
        
        c_fnc = numpy.zeros((N,N))
        c_apprx = numpy.zeros((N,N))
        
        for i, x1 in enumerate(xx):
            for j, x2 in enumerate(xx):
                p[i,j] = numpy.exp(jgmm.score(numpy.atleast_2d([x1,x2])))*ds*ds
                c_apprx[i,j] = numpy.sum(p[:i,:j])
                c_fnc[i,j] = jgmm.cdf(-numpy.inf,[x1,x2])
                
        viz = True  
        if viz:
            import matplotlib.pyplot as plt
            plt.figure()
            plt.pcolor(p.T)
            plt.figure()
            plt.pcolor(c_apprx.T)
            plt.colorbar()
            plt.figure()
            plt.pcolor(c_fnc.T)
            plt.colorbar()
            plt.show()
            
        numpy.testing.assert_array_almost_equal(c_fnc, c_apprx, err_msg = "approximate and analytical cdf don't match" )
        
        
        
                
        
        
if __name__ == "__main__":
    unittest.main()