import csv
from cluster import *
from pylab import *

class dbscanner:
    
    dataSet = []
    count = 0
    visited = []
    member = []
    Clusters = []
    cluster_dic = {}
    
    def dbscan(self,D,eps,MinPts,rawDataPath):
        self.dataSet = D

        title(r'cluster', fontsize=18)
        xlabel(r'longitude',fontsize=17)
        ylabel(r'latitude', fontsize=17)
        
        C = -1
        Noise = cluster('Noise')
        noise_marker = []
        
        for i, point in enumerate(D):
            if point not in self.visited:
                self.visited.append(point)
                NeighbourPoints = self.regionQuery(point, eps)
                
                if len(NeighbourPoints) < MinPts:
                    Noise.addPoint(point)
                    noise_marker.append(i)
                else:
                    name = 'Cluster'+str(self.count)
                    C = cluster(name)
                    self.count += 1
                    self.expandCluster(point,NeighbourPoints,C,eps,MinPts)
                    
                    plot(C.getY(),C.getX(),'o',markersize=15,label=name)
                    clustered_points = C.getPoints()
                    for i in range(len(clustered_points)):
                        self.cluster_dic[str(clustered_points[i])] = name
                    hold(True)

            if i%2==0:
                plot([D[i][1], D[i - 1][1]], [D[i][0], D[i - 1][0]])

        if len(Noise.getPoints())!=0:
            plot(Noise.getY(),Noise.getX(),'*',markersize=15,label='Noise')

        hold(False)
        legend(loc='lower left')
        plt.axis('equal')
        grid(False)
        self._assign_cluster_label(self.cluster_dic,rawDataPath)



    def expandCluster(self,point,NeighbourPoints,C,eps,MinPts):
        # expand the cluster if condition satisfied
        C.addPoint(point)
        
        for p in NeighbourPoints:
            if p not in self.visited:
                self.visited.append(p)
                np = self.regionQuery(p,eps)
                if len(np) >= MinPts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)

            for c in self.Clusters:
                if not c.has(p):
                    if not C.has(p):
                        C.addPoint(p)

            if len(self.Clusters) == 0:
                if not C.has(p):
                    C.addPoint(p)

        self.Clusters.append(C)

                    

    def regionQuery(self,P,eps):
        # check how many neighbours are nearby
        result = []
        for d in self.dataSet:
            if (((d[0]-P[0])**2+(d[1]-P[1])**2)**0.5)<=eps:
                result.append(d)
        return result



    def _assign_cluster_label(self, d, rawDataPath):
        # after the data clustering, label different data with there belonged cluster or noise
        pairPath = rawDataPath
        dest1 = rawDataPath[:rawDataPath.rfind('\\')]
        dest2 = '\\withClusterLabel'
        dest3 = rawDataPath[rawDataPath.rfind('\\'):-4]
        labelledPairPath = dest1 + dest2 + dest3 + "_labelled.csv"
        with open(pairPath, 'rb') as f:
            with open(labelledPairPath, 'wb') as g:
                writer = csv.writer(g)
                r = csv.reader(f)
                for line in r:
                    key = str([float(line[3]), float(line[4])])
                    if key in d:
                        new_line = line[0], line[1], line[2], line[3], line[4], line[5], d[key]
                        writer.writerow(new_line)
                    else:
                        new_line = line[0], line[1], line[2], line[3], line[4], line[5], 'Noise'
                        writer.writerow(new_line)
                g.flush()
                g.close()
            f.flush()
            f.close()