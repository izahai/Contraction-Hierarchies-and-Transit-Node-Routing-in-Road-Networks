import json
import csv

class PathQuery:
    def __init__(self, list_path):
        self.list_path = list_path

    def search_by_route_id(self, route_id):
        return [rv for rv in self.list_path if rv.get_route_id() == route_id]

    def search_by_route_var_id(self, route_var_id):
        return [rv for rv in self.list_path if rv.get_route_var_id() == route_var_id]

    def search_by_lat(self, lat):
        return [rv for rv in self.list_path if rv.get_lat() == lat]

    def search_by_lng(self, lng):
        return [rv for rv in self.list_path if rv.get_lng() == lng]

    def output_as_csv(self, list_output):
        fields = ['route_id', 'route_var_id', 'lat', 'lng']
        filename = "output_path.csv"
        with open(filename, 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for data in list_output:
                # Assuming the data objects have attributes matching the fields
                writer.writerow({
                    'route_id': data.route_id,
                    'route_var_id': data.route_var_id,
                    'lat': data.lat,
                    'lng': data.lng
                })

    def output_as_json(self, list_output):
        with open('output_path.json', 'w', encoding='utf8') as fout:
            for data in list_output:
                # Assuming the data objects have attributes matching the JSON structure
                json.dump({
                    'route_id': data.route_id,
                    'route_var_id': data.route_var_id,
                    'lat': data.lat,
                    'lng': data.lng
                }, fout, ensure_ascii=False)
                fout.write('\n')