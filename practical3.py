from pymlmc import mlmc_test, mlmc_plot
import matplotlib.pyplot as plt
import numpy
import numpy.random
from math import sqrt
import copy

class CallType(object):
    def __init__(self, name, M, N, L, Eps):
        self.name = name
        self.M = M # refinement cost factor
        self.N = N # samples for convergence tests
        self.L = L # levels for convergence tests
        self.Eps = Eps

# these will determine at evaluation what algorithm to use  - for now only biased Algo 2 
eps = [50,20,10,5, 2, 1]
# eps = [50,20,10]
# eps = [50]
calltypes = [CallType("Biased", 3, 10000, 5, eps)] #,
             #CallType("Unbiased",    4, 2000000, 5, [1, 2, 5, 10,20, 50])] 

def tau_leaping_simulation(Lambda, Zeta, Z0, hf, hc, T, M):
    assert len(Lambda) == Zeta.shape[1]
    
    K  = len(Lambda) # number of reactions 
    Zc = copy.deepcopy(Z0)
    Zf = copy.deepcopy(Z0)
    tn = 0 
    A1 = numpy.zeros(K)
    A2 = numpy.zeros(K)
    A3 = numpy.zeros(K)
    sample1 = numpy.zeros(K)
    sample2 = numpy.zeros(K)
    sample3 = numpy.zeros(K)
    
    while(tn < T):
        Zc = numpy.maximum(Zc, 0)
        ZcTn = copy.deepcopy(Zc)
        
        for j in range(M):
            for k in range(K):
                # for every reaction k 
                A1[k] = min(Lambda[k](Zf), Lambda[k](ZcTn))
                A2[k] = Lambda[k](Zf) - A1[k]
                A3[k] = Lambda[k](ZcTn) - A1[k]
                                
                sample1[k] = numpy.random.poisson(A1[k]*hf)
                sample2[k] = numpy.random.poisson(A2[k]*hf)
                sample3[k] = numpy.random.poisson(A3[k]*hf)
                
            Zf = Zf + numpy.squeeze(numpy.asarray( Zeta.dot(sample1 + sample2 )))
            Zc = Zc + numpy.squeeze(numpy.asarray( Zeta.dot(sample1 + sample3 )))
            
            Zf = numpy.maximum(Zf, 0)
        tn = tn + hc
    return Zf[2], Zc[2] # restric ourself to the D-state


def opre_tau_leaping(l,N,calltype,randn=numpy.random.randn):
    '''
        mlmc_fn: the user low-level routine for level l estimator. Its interface is

        (sums, cost) = mlmc_fn(l, N, *args, **kwargs)

        Inputs:  l: level
                 N: number of samples
                 *args, **kwargs: optional additional user variables

        Outputs: sums[0]: sum(Y)
                sums[1]: sum(Y**2)
                sums[2]: sum(Y**3)
                sums[3]: sum(Y**4)
                sums[4]: sum(P_l)
                sums[5]: sum(P_l**2)
                    where Y are iid samples with expected value
                        E[P_0]            on level 0
                        E[P_l - P_{l-1}]  on level l > 0
                cost: user-defined computational cost of N samples
    '''
    sums = numpy.zeros(6)
    M = calltype.M # refinement factor
    T   = 1.0  # interval
    l += 2
    
    nf = M**(l+2)
    hf = T/nf
    
    nc = max(nf/M, 1)
    hc = T/nc
    Z0 = numpy.array([0,0,0])
    
    if calltype.name == "Biased":
        Lambda = [lambda Z: 25, 
                  lambda Z: 1000*Z[0], 
                  lambda Z: 0.001*Z[1]*(Z[1]-1), 
                  lambda Z: 0.1*Z[0], 
                  lambda Z: Z[1]]
        
        Zeta = numpy.matrix([numpy.array([1,0,0]),
               numpy.array([0,1,0]),
               numpy.array([0,-2,1]),
               numpy.array([-1,0,0]),
               numpy.array([0,-1,0])]).transpose()
    else: 
        pass 
    
    for i in range(N):
        Zf, Zc = tau_leaping_simulation(Lambda, Zeta, Z0, hf, hc, T, M)
        if l==0:
            Zc = numpy.array([0])
        Zd = Zf - Zc 
        sums += numpy.array([Zd, Zd**2, Zd**3, Zd**4, Zf, Zf**2])
        
        
    cost = N*nf # cost defined as number of fine timesteps
    return (sums, cost)

if __name__ == "__main__":
    N0 = 1000 # initial samples on coarse levels
    Lmin = 2  # minimum refinement level
    Lmax = 6  # maximum refinement level

    
    for (i, calltype) in enumerate(calltypes):
        def opre_l(l, N):
            return opre_tau_leaping(l, N, calltype)

        filename = "opre_gbm%d.txt" % (i+1)
        logfile = open(filename, "w")
        print('\n ---- ' + calltype.name + ' Tau-leaping ---- \n')
        mlmc_test(opre_l, calltype.N, calltype.L, N0, calltype.Eps, Lmin, Lmax, logfile)
        del logfile
        mlmc_plot(filename, nvert=3)
        plt.savefig(filename.replace('.txt', '.eps'))
        plt.show()
