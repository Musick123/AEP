
init python:

    # borrowed from:
    # www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
    #
    # Could be improved... does not seem to ignore routes that extend 
    # beyond a 'found' distance to target

    import heapq

    class Vertex:
        def __init__(self, node):
            self.id = node
            self.adjacent = {}
            # Set distance to infinity for all nodes
            self.distance = 10000
            # Mark all nodes unvisited        
            self.visited = False  
            # Predecessor
            self.previous = None

        def add_neighbor(self, neighbor, weight=0):
            self.adjacent[neighbor] = weight

        def get_connections(self):
            return self.adjacent.keys()  

        def get_id(self):
            return self.id

        def get_weight(self, neighbor):
            return self.adjacent[neighbor]

        def set_distance(self, dist):
            self.distance = dist

        def get_distance(self):
            return self.distance

        def set_previous(self, prev):
            self.previous = prev

        def set_visited(self):
            self.visited = True

        def __str__(self):
            return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    class Graph:
        def __init__(self):
            self.vert_dict = {}
            self.num_vertices = 0

        def __iter__(self):
            return iter(self.vert_dict.values())

        def add_vertex(self, node):
            if not node in self.vert_dict:
                self.num_vertices += 1
                self.vert_dict[node] = Vertex(node)

        def get_vertex(self, n):
            if n in self.vert_dict:
                return self.vert_dict[n]
            else:
                return None

        def add_edge(self, frm, to, cost = 0):
            if frm not in self.vert_dict:
                self.add_vertex(frm)
            if to not in self.vert_dict:
                self.add_vertex(to)

            self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
            # self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

        def get_vertices(self):
            return self.vert_dict.keys()

        def set_previous(self, current):
            self.previous = current

        def get_previous(self, current):
            return self.previous

    def shortest(v, path):
        ''' make shortest path from v.previous'''
        if v.previous:
            path.append(v.previous.get_id())
            shortest(v.previous, path)
        return

    def dijkstra(aGraph, start, target):
        # print '''Dijkstra's shortest path'''
        # Set the distance for the start node to zero 
        start.set_distance(0)

        # Put tuple pair into the priority queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph]
        heapq.heapify(unvisited_queue)

        while len(unvisited_queue):
            # Pops a vertex with the smallest distance 
            uv = heapq.heappop(unvisited_queue)
            current = uv[1]
            current.set_visited()

            #for next in v.adjacent:
            for next in current.adjacent:
                # if visited, skip
                if next.visited:
                    continue
                new_dist = current.get_distance() + current.get_weight(next)
                
                if new_dist < next.get_distance():
                    next.set_distance(new_dist)
                    next.set_previous(current)

            # Rebuild heap
            # 1. Pop every item
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
            # 2. Put all vertices not visited into the queue
            unvisited_queue = [
                (v.get_distance(),v) for v in aGraph if not v.visited]
            heapq.heapify(unvisited_queue)



    def get_shortest_path(end=None, start=None):
        """
        Return a list of locations (including start and end) touched upon
        while moving from start to end - else None
        """

        if not start:

            start = current.location

        # First get the locations and their (open) paths
        # We do this each time as paths may open or close between calls

        eh = globals()[ eh_init_values['ref'] ]

        locs = { k.name : [
                    (j.destination, j.distance) for j in k.get_paths()]
                 for k in eh.navigation }

        if not start in locs.keys():

            raise ValueError, "{} is not a known location".format(start)

        if not end in locs.keys():

            raise ValueError, "{} is not a known location".format(end)


        g = Graph()

        for name, paths in locs.items():

            g.add_vertex(name)

            for path in paths:

                g.add_edge( name, path[0], path[1] )

        # for v in g:
        #     for w in v.get_connections():
        #         vid = v.get_id()
        #         wid = w.get_id()
        #         print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))

        dijkstra(g, g.get_vertex(start), g.get_vertex(end)) 

        target = g.get_vertex(end)
        path = [target.get_id()]
        shortest(target, path)
        # print ('The shortest path : %s' %(path[::-1]))

        return path[::-1] if path[-1] == start else None

