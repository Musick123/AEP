# Navigation labels
# Used to define:
    # Paths between locations
    # Maps appearing on 
    # Positions on those maps 
    # Buttons for navigating (when viewing background)

# Note: Paths are one way routes, so a new path to B from A should also
# have a new path from B back to A (perhaps with different tests) if needed

# Important Note:
# Label names should include the prefix like _navigation
# It is stripped off and stored in the NavigationEvent as name


            ###############################################
            #                                             #
            #               Town Junctions                #
            #                                             #
            ###############################################


label junction_1_navigation:
    event register navigation:
        path 'junction_2' 100
        path 'bridge' 50
        path 'petrol' 50
        path 'scrap' 100
        path 'farm' 200
    return

label junction_2_navigation:
    event register navigation:
        path 'junction_1' 100
        path 'junction_3' 100
        path 'hifi' 50
        path 'motel' 50
    return

label junction_3_navigation:
    event register navigation:
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

label bridge_navigation:
    event register navigation:
        path 'junction_1' 50
    return

            ###############################################
            #                                             #
            #                 The Church                  #
            #                                             #
            ###############################################

label church_navigation:
    event register navigation:
        on_map ["town","church"]
        path 'junction_3' 100
        path 'forest' 50
        path:
            'church_sanctum'
            25
            simp "False" # will be test for bushes removed
    return

label church_sanctum_navigation:
    event register navigation:
        on_map ["church"]
        path 'church' 25
        path:
            'church_gate'
            25
            simp "False" # will be test for dimensional gate opened
    return

label church_gate_navigation:
    event register navigation:
        on_map ["church"]
        path 'church_sanctum' 25
    return


            ###############################################
            #                                             #
            #                  The Farm                   #
            #                                             #
            ###############################################

label farm_navigation:
    event register navigation:
        on_map ["town","farm"]
        path 'junction_1' 200
        path:
            'farm_shop'
            25
            simp "True" # will be test for opening times
        path 'farm_barn' 25
    return

label farm_shop_navigation:
    event register navigation:
        on_map ["farm"]
        path 'farm' 25
        path:
            'farm_bedroom'
            25
            simp "False" # test allowed
    return

label farm_barn_navigation:
    event register navigation:
        on_map ["farm"]
        path 'farm' 25
    return

label farm_bedroom_navigation:
    event register navigation:
        on_map ["farm"]
        path 'farm_shop' 25
    return


            ###############################################
            #                                             #
            #                 The Forest                  #
            #                                             #
            ###############################################

label forest_navigation:
    event register navigation:
        path 'church' 50
        path 'junction_3' 100
    return

            ###############################################
            #                                             #
            #               The HiFi Shop                 #
            #                                             #
            ###############################################

label hifi_navigation:
    event register navigation:
        on_map ["town","hifi"]
        path 'junction_2' 50
        path:
            'hifi_shop'
            25
            simp "True" # will be various tests
    return

label hifi_shop_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi' 25
        path 'hifi_toilet' 25
        path:
            'hifi_office'
            simp "False" # will be tested
        path:
            'hifi_living'
            simp "False" # will be tested
    return

label hifi_toilet_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi_shop' 25
    return

label hifi_office_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi_shop' 25
        path:
            'hifi_storage'
            simp "False" # will be tested
    return

label hifi_storage_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi_office' 25
    return

label hifi_living_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi_shop' 25
        path 'hifi_bedroom' 25
        path 'hifi_bath' 25
    return

label hifi_bath_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi_living' 25
    return

label hifi_bedroom_navigation:
    event register navigation:
        on_map ["hifi"]
        path 'hifi_living' 25
    return

            ###############################################
            #                                             #
            #                 The Motel                   #
            #                                             #
            ###############################################

label motel_navigation:
    event register navigation:
        on_map ["town","motel"]
        path 'junction_2' 50
        path 'motel_lobby' 25
    return

label motel_lobby_navigation:
    event register navigation:
        on_map ["motel"]
        path 'motel' 25
    return

# TODO: Motel sub rooms

            ###############################################
            #                                             #
            #             The Petrol Station              #
            #                                             #
            ############################################### 

label petrol_navigation:
    event register navigation:
        on_map ["town","petrol"]
        path 'junction_1' 50
        path 'scrap' 50
        path:
            'petrol_shop'
            25
            simp "True" # will be test for opening times etc
    return

label petrol_shop_navigation:
    event register navigation:
        on_map ["petrol"]
        path 'petrol' 25
        path 'petrol_toilet' 25
        path 'petrol_storage' 25
    return

label petrol_toilet_navigation:
    event register navigation:
        on_map ["petrol"]
        path 'petrol_shop' 25
    return

label petrol_storage_navigation:
    event register navigation:
        on_map ["petrol"]
        path 'petrol_shop' 25
    return

            ###############################################
            #                                             #
            #                The ScrapYard                #
            #                                             #
            ###############################################

label scrap_navigation:
    event register navigation:
        on_map "petrol"
        path 'petrol' 50
        path 'junction_1' 50
    return

            ###############################################
            #                                             #
            #                 The Theater                 #
            #                                             #
            ############################################### 

label theater_navigation:
    event register navigation:
        on_map ["town","theater"]
        path 'junction_3' 100
        path 'theater_north_1' 25
        path 'theater_south_3' 25
        arrow 'junction_3' 'right' 1230
        arrow 'theater_north_1' 'up' 740
        arrow 'theater_south_3'
    return

label theater_north_1_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater' 25
        path 'theater_north_2' 25
        path 'theater_backstage' 25
        arrow 'theater'
        arrow 'theater_north_2' 'right' 1230
        arrow 'theater_backstage' 'up' 680 450
    return

label theater_north_2_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_north_1' 25
        path 'theater_north_3' 25
        path 'theater_stage' 25
        arrow 'theater_north_1'
        arrow 'theater_north_3' 'right' 1230
        arrow 'theater_stage' 'up' 300
    return

label theater_north_3_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_north_2' 25
        path 'theater_audience' 25
        arrow 'theater_north_2' 25
        arrow 'theater_audience' 'up' 860
    return

label theater_south_1_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_south_2' 25
        arrow 'theater_south_2' 'right' 1230
        # path 'theater_toilet' 25 if door unlocked
    return

label theater_south_2_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_south_1' 25
        path 'theater_south_3' 25
        arrow 'theater_south_1' 'left'
        arrow 'theater_south_3' 'right' 1230
    return

label theater_south_3_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater' 25
        path 'theater_south_2' 25
        arrow 'theater' 'right' 1230
        arrow 'theater_south_2'
    return

label theater_audience_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_stage' 25
        path 'theater_north_3' 25
        arrow 'theater_stage' 'up' 560 120
        arrow 'theater_north_3'
    return

label theater_stage_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_backstage' 25
        path 'theater_audience' 25
        path 'theater_north_2' 25
        arrow 'theater_backstage' 'up' 900 300
        arrow 'theater_audience' 'down' 640 670
        arrow 'theater_north_2'
    return

label theater_backstage_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_storage' 25
        path 'theater_stage' 25
        path 'theater_north_1' 25
        arrow 'theater_storage' 'up' 200 250
        arrow 'theater_stage' 'right' 1230
        arrow 'theater_north_1' 'down' 640 670
    return

label theater_storage_navigation:
    event register navigation:
        on_map ["theater"]
        path 'theater_backstage' 25
        arrow 'theater_backstage'
    return

            ###############################################
            #                                             #
            #        The Villa of Hilda Wittberg          #
            #                                             #
            ###############################################

label villa_navigation:
    event register navigation:
        on_map ["town","villa"]
        path:
            'villa_parking' 
            25
            simp "False" # will be test for illusion removed
    return

label villa_parking_navigation:
    event register navigation:
        on_map ["villa"]
        path 'villa' 25
        path 'villa_wall' 25
    return

label villa_wall_navigation:
    event register navigation:
        on_map ["villa"]
        path 'villa_parking' 25
        path:
            'villa_pool' 
            25
            simp "False" # will be test hole drilled and char is rat
    return

label villa_pool_navigation:
    event register navigation:
        on_map ["villa"]
        path 'villa_wall' 25
    return

# TODO: Find out what Villa looks like as pdf is confusing
#       with saloon and pool being indistinct

# label villa_hall_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

# label villa_saloon_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

# label villa_guest_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

# label villa_bath_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

# label villa_kitchen_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

# label villa_bedroom_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

# label villa_cellar_navigation:
#     event register navigation:
#         path 'villa_wall' 25
#     return

