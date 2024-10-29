import json
import csv
from RouteVar import RouteVar

class RouteVarQuery:
    def __init__(self, list_route_var):
        self.list_route_var = list_route_var

    def search_by_route_id(self, route_id):
        return [rv for rv in self.list_route_var if rv.get_route_id() == route_id]

    def search_by_route_var_id(self, route_var_id):
        return [rv for rv in self.list_route_var if rv.get_route_var_id() == route_var_id]

    def search_by_route_var_name(self, route_var_name):
        return [rv for rv in self.list_route_var if rv.get_route_var_name() == route_var_name]

    def search_by_route_var_short_name(self, route_var_short_name):
        return [rv for rv in self.list_route_var if rv.get_route_var_short_name() == route_var_short_name]

    def search_by_route_no(self, route_no):
        return [rv for rv in self.list_route_var if rv.get_route_no() == route_no]

    def search_by_start_stop(self, start_stop):
        return [rv for rv in self.list_route_var if rv.get_start_stop() == start_stop]

    def search_by_end_stop(self, end_stop):
        return [rv for rv in self.list_route_var if rv.get_end_stop() == end_stop]

    def search_by_distance(self, distance):
        return [rv for rv in self.list_route_var if rv.get_distance() == distance]

    def search_by_outbound(self, outbound):
        return [rv for rv in self.list_route_var if rv.get_outbound() == outbound]

    def search_by_running_time(self, running_time):
        return [rv for rv in self.list_route_var if rv.get_running_time() == running_time]

    def output_as_csv(self, list_output):
        fields = ['route_id', 'route_var_id', 'route_var_name', 'route_var_short_name', 'route_no', 
                  'start_stop', 'end_stop', 'distance', 'outbound', 'running_time']
        filename = "output_var_route.csv"
        with open(filename, 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for data in list_output:
                writer.writerow(data.__dict__)
    
    def output_as_json(self, list_output):
        with open('output_var_route.json', 'w', encoding='utf8') as fout:
            for data in list_output:
                json.dump(data.__dict__, fout, ensure_ascii=False)
                fout.write('\n')