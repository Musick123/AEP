# Location labels
# Just used to define paths between different areas

# Note: Paths are one way routes, so a new path to B from A should also
# have a new path from B back to A (perhaps with different tests) if needed

# Important Note:
# Label names should include the prefix _location
# It is stripped off and stored in the LocationEvent as name


            ###############################################
            #                                             #
            #               Town Junctions                #
            #                                             #
            ###############################################


label junction_1_location:
    event register location:
        path 'junction_2' 100
        path 'bridge' 50
        path 'petrol' 50
        path 'scrap' 100
        path 'farm' 200
    return

label junction_2_location:
    event register location:
        path 'junction_1' 100
        path 'junction_3' 100
        path 'hifi' 50
        path 'motel' 50
    return

label junction_3_location:
    event register location:
        path 'junction_2' 100
        path 'church' 100
        path 'theater' 100
        path 'villa' 100
        path 'forest' 100
    return



            ###############################################
            #                                             #
            #                 The Bridge                  #
            #                                             #
            ###############################################

label bridge_location:
    event register location:
        path 'junction_1' 50
    return

            ###############################################
            #                                             #
            #                 The Church                  #
            #                                             #
            ###############################################

label church_location:
    event register location:
        path 'junction_3' 100
        path 'forest' 50
        path:
            'church_sanctum'
            25
            simp "False" # will be test for bushes removed
    return

label church_sanctum_location:
    event register location:
        on_map "church"
        path 'church' 25
        path:
            'church_gate'
            25
            simp "False" # will be test for dimensional gate opened
    return

label church_gate_location:
    event register location:
        path 'church_sanctum' 25
        on_map "church"
    return


            ###############################################
            #                                             #
            #                  The Farm                   #
            #                                             #
            ###############################################

label farm_location:
    event register location:
        path 'junction_1' 200
        path:
            'farm_shop'
            25
            simp "True" # will be test for opening times
        path 'farm_barn' 25
    return

label farm_shop_location:
    event register location:
        on_map "farm"
        path 'farm' 25
        path:
            'farm_bedroom'
            25
            simp "False" # test allowed
    return

label farm_barn_location:
    event register location:
        on_map "farm"
        path 'farm' 25
    return

label farm_bedroom_location:
    event register location:
        on_map "farm"
        path 'farm_shop' 25
    return


            ###############################################
            #                                             #
            #                 The Forest                  #
            #                                             #
            ###############################################

label forest_location:
    event register location:
        path 'church' 50
        path 'junction_3' 100
    return

            ###############################################
            #                                             #
            #               The HiFi Shop                 #
            #                                             #
            ###############################################

label hifi_location:
    event register location:
        path 'junction_2' 50
        path:
            'hifi_shop'
            25
            simp "True" # will be various tests
    return

label hifi_shop_location:
    event register location:
        on_map "hifi"
        path 'hifi' 25
        path 'hifi_toilet' 25
        path:
            'hifi_office'
            simp "False" # will be tested
        path:
            'hifi_living'
            simp "False" # will be tested
    return

label hifi_toilet_location:
    event register location:
        on_map "hifi"
        path 'hifi_shop' 25
    return

label hifi_office_location:
    event register location:
        on_map "hifi"
        path 'hifi_shop' 25
        path:
            'hifi_storage'
            simp "False" # will be tested
    return

label hifi_storage_location:
    event register location:
        on_map "hifi"
        path 'hifi_office' 25
    return

label hifi_living_location:
    event register location:
        on_map "hifi"
        path 'hifi_shop' 25
        path 'hifi_bedroom' 25
        path 'hifi_bath' 25
    return

label hifi_bath_location:
    event register location:
        on_map "hifi"
        path 'hifi_living' 25
    return

label hifi_bedroom_location:
    event register location:
        on_map "hifi"
        path 'hifi_living' 25
    return

            ###############################################
            #                                             #
            #                 The Motel                   #
            #                                             #
            ###############################################

label motel_location:
    event register location:
        path 'junction_2' 50
        path 'motel_lobby' 25
    return

label motel_lobby_location:
    event register location:
        on_map "motel"
        path 'motel' 25
    return

# TODO: Motel sub rooms

            ###############################################
            #                                             #
            #             The Petrol Station              #
            #                                             #
            ############################################### 

label petrol_location:
    event register location:
        path 'junction_1' 50
        path 'scrap' 50
        path:
            'petrol_shop'
            25
            simp "True" # will be test for opening times etc
    return

label petrol_shop_location:
    event register location:
        on_map "petrol"
        path 'petrol' 25
        path 'petrol_toilet' 25
        path 'petrol_storage' 25
    return

label petrol_toilet_location:
    event register location:
        on_map "petrol"
        path 'petrol_shop' 25
    return

label petrol_storage_location:
    event register location:
        on_map "petrol"
        path 'petrol_shop' 25
    return

            ###############################################
            #                                             #
            #                The ScrapYard                #
            #                                             #
            ###############################################

label scrap_location:
    event register location:
        on_map "petrol"
        path 'petrol' 50
        path 'junction_1' 50
    return

            ###############################################
            #                                             #
            #                 The Theater                 #
            #                                             #
            ############################################### 

label theater_location:
    event register location:
        path 'junction_3' 100
        path 'theater_north_1' 25
        path 'theater_south_3' 25
    return

label theater_north_1_location:
    event register location:
        on_map "theater"
        path 'theater' 25
        path 'theater_north_2' 25
        path 'theater_backstage' 25
    return

label theater_north_2_location:
    event register location:
        on_map "theater"
        path 'theater_north_1' 25
        path 'theater_north_3' 25
        path 'theater_stage' 25
    return

label theater_north_3_location:
    event register location:
        on_map "theater"
        path 'theater_north_2' 25
        path 'theater_audience' 25
    return

label theater_south_1_location:
    event register location:
        on_map "theater"
        path 'theater_south_2' 25
        # path 'theater_toilet' 25 if door unlocked
    return

label theater_south_2_location:
    event register location:
        on_map "theater"
        path 'theater_south_1' 25
        path 'theater_south_3' 25
    return

label theater_south_3_location:
    event register location:
        on_map "theater"
        path 'theater' 25
        path 'theater_south_2' 25
    return

label theater_audience_location:
    event register location:
        on_map "theater"
        path 'theater_stage' 25
        path 'theater_north_3' 25
    return

label theater_stage_location:
    event register location:
        on_map "theater"
        path 'theater_backstage' 25
        path 'theater_audience' 25
        path 'theater_north_2' 25
    return

label theater_backstage_location:
    event register location:
        on_map "theater"
        path 'theater_storage' 25
        path 'theater_stage' 25
        path 'theater_north_1' 25
    return

label theater_storage_location:
    event register location:
        on_map "theater"
        path 'theater_backstage' 25
    return

            ###############################################
            #                                             #
            #        The Villa of Hilda Wittberg          #
            #                                             #
            ###############################################

label villa_location:
    event register location:
        path:
            'villa_parking' 
            25
            simp "False" # will be test for illusion removed
    return

label villa_parking_location:
    event register location:
        on_map "villa"
        path 'villa' 25
        path 'villa_wall' 25
    return

label villa_wall_location:
    event register location:
        on_map "villa"
        path 'villa_parking' 25
        path:
            'villa_pool' 
            25
            simp "False" # will be test hole drilled and char is rat
    return

label villa_pool_location:
    event register location:
        on_map "villa"
        path 'villa_wall' 25
    return

# TODO: Find out what Villa looks like as pdf is confusing
#       with saloon and pool being indistinct

# label villa_hall_location:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_saloon_location:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_guest_location:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_bath_location:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_kitchen_location:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_bedroom_location:
#     event register location:
#         path 'villa_wall' 25
#     return

# label villa_cellar_location:
#     event register location:
#         path 'villa_wall' 25
#     return


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

            start = current_location

        # First get the locations and their (open) paths
        # We do this each time as paths may open or close between calls

        eh = globals()[ eh_init_values['ref'] ]

        locs = { k.name : [
                    (j.destination, j.distance) for j in k.get_paths()]
                 for k in eh.location }

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

