#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 07:55:56 2017

Class documents

a. Data Structure Class (Vertex):
 attributes:
    Vertex.name : The user name : e.g. Vertex.name = "2"
    Vertex.neighbors : The list of 1st degree neighbors 
    Vertex.neighbors_d : A dictionary contains the neighbors of degree D as key, and the degree as value 
    Vertex.neighbors_d2 : A dictionary contains degree as key, and the neigbhors of degree as a value list
    Vertex.self_purchase : A FIFO queue with fixed length of T contains the latest purchase history of this user.
    			   Each element is [eadin_index, timestamp,amount of purchases, Name]
    Vertex.neig_purchase : A FIFO queue with fixed length of T contains the latest purchase history of all neighboring users of degree D
    			   Each element is [eadin_index, timestamp,amount of purchases, Name]
    Vertex.ave : The average amount of purchases in the latest T purchases from the neighboring users of degree D
    Vertex.sd : The standard deviation of purchases in the latest T purchases from the neighboring users of degree D
 functions : 
    Vertex.add_neighbor(neighbor) : A function adding another vertex into Vertex.neighbors
    Vertex.add_neighbors(neigbhors) : A function adding a list of  vertices into  Vertex.neighbors
    Vertex.add_nd(neighbor,degree) : A function adding a vertex as the neighbor of degree into the Vertex.neighbors_d and Vertex.neighbors_d2
    Vertex.rm_nd(neighbor) : A function removing a vertex from Vertex.neighbors_d and Vertex.neighbors_d2
    Vertex.rm_neighbor(neighbor)  : A function removing a vertex from  Vertex.neighbors
    Vertex.rm_neighbors(neighbors) : A function removing a list of vertices from  Vertex.neighbors
    Vertex.add_order(readin_index,timestamp,amount) : A function adding an element into the Vertex.self_purchase
    Vertex.add_neig_purchase(neighbor,readin_index,timestamp,amount) : A function adding an element into Vertex.neig_purchase
b. Data Structure Class (Graph):
 attributes :
    Graph.vertices : A dictionary of vetices : Name of the vertex as key, the vertex as value
 functions :    
    Graph.add_vertex(vertex): A function adding a vertex into Graph.vertices
    Graph.add_vertices(vertex) :  A function adding a list of  vertices into Graph.vertices
    Graph.add_edge(vertex1,vertex2) : Adding the neighbor relationship between vertex1 and vertex 2
    Graph.add_edges(vertex_list) : Adding the neighbor relationships for a list of two vertices
    Graph.rm_edge(vertex1,vertex2) : removing the neighbor relationship between vertex1 and vertex 2
    Graph.rm_edges(vertex_list): removing the neighbor relationships for a list of two vertices
    Graph.add_order(name,readin_index,timestamp,amount) : adding an element of purchase into the Vertices[name].self_purchase
    Graph.add_neig_purchase(neig_name,idname,read_index,timestamp,amount) : adding an element of purchase into the Vertices[name].neig_purchase
    Graph.adjacencyList : A function to create a adjacency list to represent the Graph network

c. Functinal Class (Anomaly_detec)
  attributes :
   Anomaly_detec.network : A graph class to save the social network
   Anomaly_detec.anomaly : A list of anomalic purchases (Flagged) events
   Anomaly_detec.D : Degree of neighbors : the more degree, the slower the code run
   Anomaly_detec.T : The number of latest purchases within the neighboring network to assess the current purchases
   Anomaly_detec.flag_dyn(default [False,filepath] : Whether write the flagged event dynamically into the filepath while reading and update the stream log
   				                     This won't overwrite the exist file, but write new line at the end of the file
  functions : 
   Anomaly.write_anomaly(filepath): Write the Anomaly_detec.anomaly into filepath
   Anomaly.read_batch(batch) : Read the batch logs from batch file, save into  Anomaly_detec.network
   Anomaly.init_neighb_D(name): For Vertex with name, use BFS to search all the neigbhors of degree d and update the Vertex.neighbors_d, and Vertex.neighbors_d2
   Anomaly.update_ave_sd(name) : For Vertex with name, update the average and standard deviation using the Vertex.neig_purchase (The neighbor network purchases)
   Anomaly.init_ave_sd_id(name) : Initialize and update all the attributes for Vertex (name)
   Anomaly.init_ave_sd_all :  Initialize and update all the attributes for all vertices within the network
   Anomaly.add_ave_sd_np_id(name,added_vertices) : Update attributes: Vertex.neig_purchase, Vertex.ave, Vertex.sd using assuming the added_vertices were added into the neighbor network
   Anomaly.read_flag_stream(stream) : Read stream log from stream, update the network dynamically when an event was readin
   
@author: Jingbo Liu jingbo.liu2013@gmail.com
"""
import json
import numpy as np
from collections import deque


class Vertex:
    def __init__(self, vertex,T):
        self.name = vertex
        self.neighbors = []
        self.neighbors_d = {} ## dictionary {name: degree}
        self.neighbors_d2 ={} ## dictionary {degree : [name1,name2...]}
        self.self_purchase = deque(T * [[0,'1900-00-00 00:00:00','0',self.name]], T)  ## FIFO queue with max length T
        self.neig_purchase = deque(T *[[0,'1900-00-00 00:00:00','0','0']],T)  ## FIFO queue with max length T
        self.ave = 0  ## average purchase in the D degree network
        self.sd = 0   ## Standard deviation in the D degree network

    def add_neighbor(self, neighbor):
        if isinstance(neighbor, Vertex):
            if neighbor.name not in self.neighbors:
                self.neighbors.append(neighbor.name)
                neighbor.neighbors.append(self.name)
                self.neighbors = sorted(self.neighbors)
                neighbor.neighbors = sorted(neighbor.neighbors)
        else:
            return False
        
    def add_neighbors(self, neighbors):
        for neighbor in neighbors:
            if isinstance(neighbor, Vertex):
                if neighbor.name not in self.neighbors:
                    self.neighbors.append(neighbor.name)
                    neighbor.neighbors.append(self.name)
                    self.neighbors = sorted(self.neighbors)
                    neighbor.neighbors = sorted(neighbor.neighbors)
            else:
                return False
 
    def add_nd(self, nname,ndegree):
        self.neighbors_d[nname] = ndegree
        if ndegree in self.neighbors_d2:
            self.neighbors_d2[ndegree].append(nname)
        else:
            self.neighbors_d2[ndegree] = [nname]
        return 
    def rm_nd(self,nname):
        self.neighbors_d2[self.neighbors_d[nname]].remove(nname)
        del self.neighbors_d[nname]
        return 
           
    def rm_neighbor(self, neighbor):
        if isinstance(neighbor, Vertex):
            if neighbor.name in self.neighbors:
                self.neighbors.remove(neighbor.name)
                neighbor.neighbors.remove(self.name)
                self.neighbors = sorted(self.neighbors)
                neighbor.neighbors = sorted(neighbor.neighbors)
        else:
            return False
        
    def rm_neighbors(self, neighbors):
        for neighbor in neighbors:
            if isinstance(neighbor, Vertex):
                if neighbor.name in self.neighbors:
                    self.neighbors.remove(neighbor.name)
                    neighbor.neighbors.remove(self.name)
                    self.neighbors = sorted(self.neighbors)
                    neighbor.neighbors = sorted(neighbor.neighbors)
            else:
                return False
    def add_order(self, read_index,timestamp,amount):
        self.self_purchase.append([read_index,timestamp,amount,self.name])
    def add_neig_purchase(self,neig_name,read_index,timestamp,amount) : 
        self.neig_purchase.append([read_index,timestamp,amount,neig_name])

    def __repr__(self):
        return str(self.neighbors) + "\n" + str(self.self_purchase)

class Graph:
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            self.vertices[vertex.name] = vertex

    def add_vertices(self, vertices):
        for vertex in vertices:
            if isinstance(vertex, Vertex):
                self.vertices[vertex.name] = vertex
            
    def add_edge(self, vertex_from, vertex_to):
        if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
            vertex_from.add_neighbor(vertex_to)
            if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
                self.vertices[vertex_from.name] = vertex_from
                self.vertices[vertex_to.name] = vertex_to
                
    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0],edge[1])          
    
    def rm_edge(self, vertex_from, vertex_to):
        if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
            vertex_from.rm_neighbor(vertex_to)
            if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
                self.vertices[vertex_from.name] = vertex_from
                self.vertices[vertex_to.name] = vertex_to
    def rm_edges(self, edges):
        for edge in edges:
            self.rm_edge(edge[0],edge[1])          

    def add_order(self, idname,index,timestamp,amount):
        if(timestamp >= self.vertices[idname].self_purchase[-1][1]):
            self.vertices[idname].add_order(index,timestamp,amount) 
        
    def add_neig_purchase(self,neig_name,idname,read_index,timestamp,amount) :
        if(timestamp >= self.vertices[neig_name].neig_purchase[-1][1]):
            self.vertices[neig_name].neig_purchase.append([read_index,timestamp,amount,idname])
        
    
    def adjacencyList(self):
        if len(self.vertices) >= 1:
                return [str(key) + ":" + str(self.vertices[key].neighbors) + 
                        str(self.vertices[key].self_purchase) 
                        for key in self.vertices.keys()]  
        else:
            return dict()

        
def graph(g,index):
    """ Function to print a graph as adjacency list. """
    adjlist = g.adjacencyList()
    for temindex in index:
        print(adjlist[temindex])
    return  "\n" 



class Anomaly_detec:
    def __init__(self):
        self.network = Graph()
        self.anomaly = []  # List of strings ## Flagged event to output 
        self.D = 2 ## Default
        self.T = 50 ## Default the lastest number of transaction 
        self.flag_dyn = [False,""]  ## Whether write to the flag file dynamically 
                               ## while reading stream log
    
    def write_anomaly(self,outfile):
        f = open(outfile,"w")
        for i in range(len(self.anomaly)):
            f.write(self.anomaly[i] + "\n")
        f.close()
        print("Saved flagged event in " + outfile)
    
    def read_batch(self,batch):
        with open(batch) as f:
            first_line = json.loads(f.readline())
#            self.D = int(first_line["D"])
#            self.T = int(first_line["T"])
            read_index = 0
            for line in f:
                try:
                    parseline = json.loads(line)
                    read_index = read_index + 1
                except: 
                    print("This line can't be parsed in Json" + line)
                    break
                ## event type purchase, befriend unfriend
                event_type = parseline["event_type"]
                if event_type == "purchase" :
                    cid = parseline["id"]
                    ctimestamp = parseline["timestamp"]
                    camount = parseline["amount"]
                    ## Check if new user : add in the network
                    ## Or update the history
                    if cid not in self.network.vertices:
                        newuser = Vertex(cid,self.T)
                        newuser.add_order(read_index,ctimestamp,camount)
                        self.network.add_vertex(newuser)
                    else : 
                        self.network.add_order(cid,read_index,ctimestamp,
                                     camount)                      
                if event_type == "befriend" :
                    cid1 = parseline["id1"]
                    cid2 = parseline["id2"]
#                    print("connecting " + str(cid1) + " and " +str(cid2))
                    ## check if new user : add in the network and befriend
                    if cid1 not in self.network.vertices and cid2 not in \
                    self.network.vertices :
                        newuser1 = Vertex(cid1,self.T)
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertices([newuser1,newuser2])
                        self.network.add_edge(newuser1,newuser2)
                    elif cid1 not in self.network.vertices:
                        newuser1 = Vertex(cid1,self.T)
                        self.network.add_vertex(newuser1)
                        self.network.add_edge(newuser1,
                                              self.network.vertices[cid2])
                    elif cid2 not in self.network.vertices:
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertex(newuser2)
                        self.network.add_edge(self.network.vertices[cid1],
                                              newuser2)
                    else:
                        self.network.add_edge(self.network.vertices[cid1],
                                              self.network.vertices[cid2])    
                   
                if event_type == "unfriend" :
                    cid1 = parseline["id1"]
                    cid2 = parseline["id2"]
#                    print("disconnecting " + str(cid1) + " and " +str(cid2))
                    ## check if new user : add in the network and unfriend
                    if cid1 not in self.network.vertices and cid2 not in \
                    self.network.vertices :
                        newuser1 = Vertex(cid1,self.T)
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertices([newuser1,newuser2])
                       
                    elif cid1 not in self.network.vertices:
                        newuser1 = Vertex(cid1,self.T)
                        self.network.add_vertex(newuser1)
                        self.network.rm_edge(newuser1,
                                              self.network.vertices[cid2])
                    elif cid2 not in self.network.vertices:
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertex(newuser2)
                        self.network.rm_edge(self.network.vertices[cid1],
                                              newuser2)
                    else:
                        self.network.rm_edge(self.network.vertices[cid1],
                                              self.network.vertices[cid2])  
                        
    ## For each id, use BFS to search and initialized the D degree neighbors for one vertex        
    def init_neighb_D(self,vid):
        D = self.D
        T = self.T
        ## Add current name to dict for BFS 
        self.network.vertices[vid].add_nd(vid,0)
        next_layer = self.network.vertices[vid].neighbors
        Degree = 1
        while Degree <= D and next_layer:
            tem_next = next_layer[:]
            next_layer = []
            for neighbid in tem_next:
                if neighbid not in self.network.vertices[vid].neighbors_d:    
                    self.network.vertices[vid].add_nd(neighbid,Degree) ## Update current id
                    next_layer.extend(self.network.vertices[neighbid].neighbors)
            ## Remove the redudant next layer and element already in neighbors_d
            next_layer = list(set(next_layer))
            tem_next = next_layer[:]
            next_layer = [tem for tem in tem_next if tem not in self.network.vertices[vid].neighbors_d]
            Degree = Degree + 1
        ## Delete self
        self.network.vertices[vid].rm_nd(vid)
        ## update neighbors_d2 
        c_neighbors_d = self.network.vertices[vid].neighbors_d
        keys = list(c_neighbors_d.keys())
        values = np.array(list(c_neighbors_d.values()))
        neighbors_d2 ={}
        for d in range(1,self.D + 1):
            ## Get the keys with value equal i
            update_keys_index = np.where(values == d)[0]
            neighbors_d2[d] = [keys[temi] for temi in update_keys_index]
        self.network.vertices[vid].neighbors_d2 = neighbors_d2
        return 
    ## Update AVE and SD, need the updated neig_purchase
    def update_ave_sd(self,vid):
        neig_purchase = list(self.network.vertices[vid].neig_purchase)       
        amount_list = [float(x[2]) for x in neig_purchase if x[0] != 0]    
        if len(amount_list) >=1:
    #        print(amount_list)
            self.network.vertices[vid].ave = np.mean(amount_list)
            self.network.vertices[vid].sd = np.std(amount_list)
        return
    def init_ave_sd_id(self,vid):
        D = self.D
        T = self.T
    ## update the neighbors_d attribute for current vid
        self.init_neighb_D(vid)  
        nid_D = list(self.network.vertices[vid].neighbors_d)
        D_purchased = []
        for i in nid_D:
            D_purchased.extend(list(self.network.vertices[i].self_purchase))
        ## In the D degree network 
        ## Sort the purchased item by 1st time stamp then readin index
        D_purchased = sorted(D_purchased,key=lambda x : (x[1],x[0]))
        ## Get the latest purchases and save in neig_purchase
        self.network.vertices[vid].neig_purchase = D_purchased[-self.T:]
     ## update ave and sd attribute for current vid   
        self.update_ave_sd(vid)
        return 
    def add_ave_sd_np_id(self,nid,add_ids): ## add_ids is a list
        D = self.D
        T = self.T
        D_purchased = []
        D_purchased = list(self.network.vertices[nid].neig_purchase)   
        [D_purchased.extend(list(self.network.vertices[add_id].self_purchase)) 
                                 for add_id in add_ids]
        D_purchased = sorted(D_purchased,key=lambda x : (x[1],x[0]))
        self.network.vertices[nid].neig_purchase = D_purchased[-self.T:]
        self.update_ave_sd(nid)
        
    def init_ave_sd_all(self) :
        keys = list(self.network.vertices.keys())
        for keyi in keys:
#            print("initialing %s "%(keyi))
            self.init_ave_sd_id(keyi)
        return keys

### Read Stream Log update the social network, and flag the large purchase
    def read_flag_stream(self,stream):
        if self.flag_dyn[0] == True :
            print("Saved flagged event in " + self.flag_dyn[1])
        with open(stream) as f:
            read_index = 0
            for line in f:
                try: 
                    parseline = json.loads(line)
                    read_index = read_index + 1
                except: 
                    print("Current Jason line can'be parse " + line)
                    break
                ## event type purchase, befriend unfriend
                event_type = parseline["event_type"]
                if event_type == "purchase" :
                    cid = parseline["id"]
                    ctimestamp = parseline["timestamp"]
                    camount = parseline["amount"]
                    
                    ## Check if new user : add in the network
                    ## Or update the history and flag large purchase
                    if cid not in self.network.vertices:
                        newuser = Vertex(cid,self.T)
                        newuser.add_order(read_index,ctimestamp,camount)
                        self.network.add_vertex(newuser)
                    else : 
                        c_neig_buy = self.network.vertices[cid].neig_purchase
                        n_neig_buy = len([float(x[2]) for x in \
                                    c_neig_buy if x[0] != 0] )
                        if float(camount) > self.network.vertices[cid].ave +\
                                3* self.network.vertices[cid].sd and \
                                n_neig_buy >= 2:
                            cmean = str(self.network.vertices[cid].ave)
                            csd = str(self.network.vertices[cid].sd)
                            anomaly_str="{\"event_type\":\"%s\", \"timestamp\":\
\"%s\", \"id\":\" %s\", \"amount\":\" %s\", \"mean\":\" %.2f\", \"sd\":\" %.2f\"}"%( 
event_type,ctimestamp,cid,camount,float(cmean),float(csd))
                            print("Flag " + anomaly_str)
                            self.anomaly.append(anomaly_str)
                            if self.flag_dyn[0] == True :
                                f_flag = open(self.flag_dyn[1],"a+")
                                f_flag.write(anomaly_str + "\n")
                                f_flag.close()
                        ## update self_purchase attribute
                        self.network.add_order(cid,read_index,ctimestamp,
                                     camount)
                        ## update neig_purchase attributes for neighbors_d
                        nid_D = list(self.network.vertices[cid].neighbors_d.keys())
                        for iid in nid_D:
                            self.network.add_neig_purchase(iid,cid,
                                            read_index,ctimestamp,camount)
                            self.update_ave_sd(iid)                        
                        
                if event_type == "befriend" :
                    cid1 = parseline["id1"]
                    cid2 = parseline["id2"]
#                    print("connecting " + str(cid1) + " and " +str(cid2))
                    ## check if new user : add in the network and befriend
                    if cid1 not in self.network.vertices and cid2 not in \
                    self.network.vertices :
                        newuser1 = Vertex(cid1,self.T)
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertices([newuser1,newuser2])
                        self.network.add_edge(newuser1,newuser2)
                    elif cid1 not in self.network.vertices:
                        newuser1 = Vertex(cid1,self.T)
                        self.network.add_vertex(newuser1)
                        self.network.add_edge(newuser1,
                                              self.network.vertices[cid2])
                        ## Update D degree neighbors layer by layer
                        c_neighbors_d = self.network.vertices[cid2].neighbors_d2.copy()
                        c_neighbors_d[0] = cid2
                        for d in range(self.D): ## d degree
                            ## Get the keys with value equal i
                            for keyi in c_neighbors_d[d]:
                                self.network.vertices[keyi].add_nd(cid1,d+1)
                                self.add_ave_sd_np_id(keyi,[cid1]) ## Update ave and sd  neig_purchases
        
                                                      
                    elif cid2 not in self.network.vertices:
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertex(newuser2)
                        self.network.add_edge(self.network.vertices[cid1],
                                              newuser2)
                        ## Update D degree neighbors layer by layer
                        c_neighbors_d = self.network.vertices[cid1].neighbors_d2.copy()
                        c_neighbors_d[0] = cid1
                        for d in range(self.D): ## d degree
                            ## Get the keys with value equal i
                            for keyi in c_neighbors_d[d]:
                                self.network.vertices[keyi].add_nd(cid2,d+1)
                                self.add_ave_sd_np_id(keyi,[cid2]) ## Update ave and sd  neig_purchases                   

                    else:
                        self.network.add_edge(self.network.vertices[cid1],
                                              self.network.vertices[cid2])    
                        ## Update D degree neighbors layer by layer
                        c_neighbors_d1 = self.network.vertices[cid1].neighbors_d2.copy()
                        c_neighbors_d1[0] = [cid1]
                        c_neighbors_d2 = self.network.vertices[cid2].neighbors_d2.copy()
                        c_neighbors_d2[0] = [cid2]

                        for d in range(self.D):
                            ## Get the keys with value equal i
                            ## Update cid1 and its networks(without cid2)
                            for key1 in c_neighbors_d1[d]:   ## IDs in each degree
                                for d2 in range(self.D -d):  ## Degress of 2 to add in
                                    for key2_add in c_neighbors_d2[d2]:
#                                        print(key2_add)
                                        self.network.vertices[key1].add_nd(
                                                key2_add,d2+1 + d)
                                        self.add_ave_sd_np_id(key1,key2_add)
                                
                            ## Update cid2 and its networks(without cid1)
                            for key2 in c_neighbors_d2[d]:   ## IDs in each degree
                                for d1 in range(self.D -d):  ## Degress of 2 to add in
                                    for key1_add in c_neighbors_d1[d1]:
                                        self.network.vertices[key2].add_nd(
                                                key1_add,d1+1 + d)
                                        self.add_ave_sd_np_id(key2,key1_add)                      

## After unfriend, the network structure changes, but the purchase impact can't be affected
                if event_type == "unfriend" :
                    cid1 = parseline["id1"]
                    cid2 = parseline["id2"]
#                    print("disconnecting " + str(cid1) + " and " +str(cid2))
                    ## check if new user : add in the network and unfriend
                    if cid1 not in self.network.vertices and cid2 not in \
                    self.network.vertices :
                        newuser1 = Vertex(cid1,self.T)
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertices([newuser1,newuser2])
                       
                    elif cid1 not in self.network.vertices:
                        newuser1 = Vertex(cid1,self.T)
                        self.network.add_vertex(newuser1)
                        self.network.rm_edge(newuser1,
                                              self.network.vertices[cid2])
                    elif cid2 not in self.network.vertices:
                        newuser2 = Vertex(cid2,self.T)
                        self.network.add_vertex(newuser2)
                        self.network.rm_edge(self.network.vertices[cid1],
                                              newuser2)
                    else:
                        if cid2 not in self.network.vertices[cid1].neighbors:
                            print(cid1," and ",cid2," are not friends")
                        else :    
                            self.network.rm_edge(self.network.vertices[cid1],
                                              self.network.vertices[cid2])            
                        ## Update D degree neighbors layer by layer
                            c_neighbors_d1 = self.network.vertices[cid1].neighbors_d2.copy()
                            c_neighbors_d1[0] = [cid1]
                            c_neighbors_d2 = self.network.vertices[cid2].neighbors_d2.copy()
                            c_neighbors_d2[0] = [cid2]
                            for d in range(self.D):
                            ## Get the keys with value equal i
                            ## Update cid1 and its networks(without cid2)
                                for key1 in c_neighbors_d1[d]:   ## IDs in each degree
                                    for d2 in range(self.D -d):  ## Degress of 2 to remove in
                                        for key2_rm in c_neighbors_d2[d2]:
                                            if key2_rm != key1 :
#                                            print(key1,key2_rm,cid1,cid2,d2,d)
                                                self.network.vertices[key1].rm_nd(
                                                key2_rm)
                    
                            ## Update cid2 and its networks(without cid1)
                                for key2 in c_neighbors_d2[d]:   ## IDs in each degree
                                    for d1 in range(self.D -d):  ## Degress of 2 to rm in
                                        for key1_rm in c_neighbors_d1[d1]:
                                            if key1_rm != key2 :
#                                                print(key2,key1_rm,cid1,cid2,d1,d)
                                                self.network.vertices[key2].rm_nd(
                                                key1_rm)
  
        if self.flag_dyn[0] == True :
            print("Saved flagged event in " + self.flag_dyn[1])
