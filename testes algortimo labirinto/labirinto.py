import sknw
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import argparse
import cv2

#Open Maze image
img = cv2.imread("img_eroded.png")
kernel = np.ones((1,1),np.uint8)

#Convert to GrayScaledImage
grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

retval, threshold = cv2.threshold(grayscaled, 10, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
retval, threshold2 = cv2.threshold(threshold, 10, 255, cv2.THRESH_BINARY_INV)
threshold2[threshold2 == 255] = 1

#Skeletonize the Thresholded Image
skel = skeletonize(threshold2)

#Build Graph from skeleton
graph = sknw.build_sknw(skel, multi=False)
G = nx.Graph(graph)

#plt.imshow(img, cmap='gray')
plt.axis('off')

#for (s,e) in graph.edges():
#        ps = graph[s][e]['pts']
#        plt.plot(ps[:,1], -ps[:,0], 'red')

#print(graph.edges())
print(nx.shortest_path(G, source=0, target=4))

#Draw Edges by 'pts'
i = 0
while i < (len(nx.shortest_path(G, source=0, target=4)) - 1):
    ps = graph[nx.shortest_path(G, source=0, target=4)[i]][nx.shortest_path(G, source=0, target=4)[i + 1]]['pts']
    plt.plot(ps[:,1], -ps[:,0], 'red')
    i += 1

#Draw Node by 'o'   
node, nodes = graph.node, graph.nodes()
ps = np.array([node[i]['o'] for i in nodes])
#print(ps[1])
#print(ps[18])
#plt.plot(ps[:,1], -ps[:,0], 'g.')
plt.savefig('Shortest.jpg')