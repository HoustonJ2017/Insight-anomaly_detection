# Insight-anomaly_detection
# Table of Contents
    1. Summary of code challenges 
    2. The libaray necessary to run the code
    3. Documents for the defined classes : 


 1.  Summary of code challenges :

	a. python 3.5 was used for this challenge.

	b. undirected graph was selected to represent the social networks, which is a dictionary for all the vertices. For each vertice, additional attributes were added for fast update purpose : name (int), neighbors(list), neighbors of degree d (dict), self purchase historay of length T (FIFO queue of length T), and purchase history of length T for neighbors of degree d (FIFO queue of length T)  
	
	c. To initialize and update all attributes in the network, I use BFS to find the nearest neighbors of degree d, and update attributes, which has a complexity of O(V + E) for degree of 1.
	
	d. For the streaming update (when reading in one line from stream log), the initialized attributes in the network was used to update the affected vertices. The time complexity is O(Size of degree d neighbors).  

	e. Three major classes were used for implement this anmoaly detection and they are saved in the file (/src/anomaly_detec.py) : Detailed documents can be found in section 3 below.

	f. The order of prcesses in process_log.py :

	   (1) Create a new Class Anomaly_detec

	   (2) Set the desired D (Degree) and T (Latest T Transactions with in the network) (Defaul D = 1, T = 10)

	   (3) Read batchlog file

	   (4) Initialize the network with all the attributes updated

	   (5) Read stream file and update the corresponding attributes in the network dynamically

	   (6) Either write the flagged event dynamically to output file or write to the output file after update all the stream file. 


2. The libaray necessary to run the code : 

   (a) used "json" library in the code, which can be download here (https://github.com/python/cpython/blob/3.6/Lib/json/__init__.py)
   
   (b) used the standard "numpy" library for mean and sd calculation. (https://pypi.python.org/pypi/numpy/1.6.1)
   
   (c) used the module deque from "collection" (FIFO queue with fixed length of T) (https://docs.python.org/2/library/collections.html)
   
   (d) used "timeit" module to do the speed test of each individual process (https://github.com/python/cpython/blob/2.7/Lib/timeit.py)
   
   (e) used "sys" module to get the system argument from command line 

3. Class documents

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
   
