import json
import time
from object.RouteVar import RouteVar
from object.Path import Path
from object.Stop import Stop
from object.StopQuery import StopQuery
from object.PathQuery import PathQuery
from build import Coordinate

def read_route_var():
    list_data = []
    with open('json/vars.json', 'r', encoding="utf8") as fin:
        data = fin.read()
        for l in data.splitlines():
            list_data.append(json.loads(l))
    list_route_var = []
    for data in list_data:
        for obj_data in data:
            list_route_var.append(RouteVar(obj_data['RouteId'], obj_data['RouteVarId'], obj_data['RouteVarName'], obj_data['RouteVarShortName'], obj_data['RouteNo'], obj_data['StartStop'], obj_data['EndStop'], obj_data['Distance'], obj_data['Outbound'], obj_data['RunningTime']))
    return list_route_var

def read_path():
    list_data = []
    with open('json/paths.json', 'r', encoding='utf8') as fin:
        data = fin.read()
        for obj in data.splitlines():
            list_data.append(json.loads(obj))
    list_path = []
    for data in list_data:
        list_lat = []
        for obj in data['lat']:
            list_lat.append(obj)
        i = 0
        for obj in data['lng']:
            list_path.append(Path(list_lat[i], obj, data['RouteId'], data['RouteVarId']))
            i = i + 1
    return list_path

def read_stop():
    list_data = []
    with open('json/stops.json', 'r', encoding='utf8') as fin:
        data = fin.read()
        for obj in data.splitlines():
            list_data.append(json.loads(obj))
    list_stop = []
    for data in list_data:
        for obj_data in data['Stops']:
            list_stop.append(Stop(obj_data['StopId'], obj_data['Code'], obj_data['Name'], obj_data['StopType'], obj_data['Zone'], obj_data['Ward'], obj_data['AddressNo'], obj_data['Street'], obj_data['SupportDisability'], obj_data['Status'], obj_data['Lng'], obj_data['Lat'], obj_data['Search'], obj_data['Routes'], data['RouteId'], data['RouteVarId']))
    return list_stop

def compress_stop_id(list_stop):
    return list({v.get_stop_id() for v in list_stop})

def get_list_id(list_stop_id):
    list_id = {}
    for i in range(len(list_stop_id)):
        list_id[list_stop_id[i]] = i
    return list_id

def read_edge_from_route_var(list_route_var, list_stop, list_path, list_id):
    print("    ---> Build edge from raw data...")
    list_edge = []
    num_edge = 0
    for route_var in list_route_var:
        list_stop_id = StopQuery(StopQuery(list_stop).search_by_route_id(str(route_var.get_route_id()))).search_by_route_var_id(str(route_var.get_route_var_id()))
        list_path_id = PathQuery(PathQuery(list_path).search_by_route_id(str(route_var.get_route_id()))).search_by_route_var_id(str(route_var.get_route_var_id()))
        speed = route_var.get_distance() / (route_var.get_running_time() * 60.00)
        u = list_id[list_stop_id[0].get_stop_id()]
        j = 0
        for stop in list_stop_id[1:]:
            v = list_id[stop.get_stop_id()]
            y, x = Coordinate.convert_lng_lat_to_xy(stop.get_lng(), stop.get_lat())
            min_dist = float('inf')
            ind = j
            for j1 in range(j, len(list_path_id)):
                y1, x1 = Coordinate.convert_lng_lat_to_xy(list_path_id[j1].get_lng(), list_path_id[j1].get_lat())
                cur_dist = Coordinate.get_distance(x, y, x1, y1)
                if cur_dist < min_dist:
                    min_dist = cur_dist
                    ind = j1
            list_coor = []
            list_coor.append((list_path_id[j].get_lat(), list_path_id[j].get_lng()))
            dist = 0
            while j < ind:
                y1, x1 = Coordinate.convert_lng_lat_to_xy(list_path_id[j].get_lng(), list_path_id[j].get_lat())
                y2, x2 = Coordinate.convert_lng_lat_to_xy(list_path_id[j+1].get_lng(), list_path_id[j+1].get_lat())
                dist = dist + Coordinate.get_distance(x1, y1, x2, y2)
                list_coor.append((list_path_id[j+1].get_lat(), list_path_id[j+1].get_lng()))
                j = j + 1
            time = int((dist / speed) * 1000)  # s --> ms
            found = False
            for i, edge in enumerate(list_edge):
                if edge[0] == u and edge[1] == v:
                    if time < edge[2]:  # Compare current edge's dist/speed with the one in list_edge
                        prev_idx = edge[3]
                        list_edge[i] = (u, v, time, prev_idx, dist, list_coor)  # Replace with the new edge if condition is met
                    found = True
                    break
            if not found:
                list_edge.append((u, v, time, num_edge, dist, list_coor))
                num_edge = num_edge + 1
            u = v
        
        with open('storage/edge.txt', 'w') as f:
            for idx, edge in enumerate(list_edge):
                f.write(f"{edge[0]} {edge[1]} {edge[2]} {edge[3]} {edge[4]} {edge[5]}\n")
                # (from, to, time, index, distance, coordinates)
    print(" ~ :) Done")
    return list_edge

def read_edge_from_file(filename):
    print("    ---> Build edge from refined data...")
    ls_edge = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(' ', 5)  # Split first 5 elements separately
            u, v, w, idx, d = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), float(parts[4])
            coordinates_str = parts[5].strip()[1:-1]  # Remove leading and trailing square brackets
            coordinates_list = coordinates_str.split('), (')
            coordinates = [tuple(map(float, coord.replace('(', '').replace(')', '').split(', '))) for coord in coordinates_list]

            ls_edge.append((u, v, w, idx, d, coordinates))
    return ls_edge