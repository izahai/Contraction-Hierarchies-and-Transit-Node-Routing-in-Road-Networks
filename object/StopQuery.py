import json
import csv
class StopQuery:
    def __init__(self, list_stop):
        self.list_stop = list_stop

    def search_by_stop_id(self, stop_id):
        return [rv for rv in self.list_stop if rv.get_stop_id() == stop_id]

    def search_by_code(self, code):
        return [rv for rv in self.list_stop if rv.get_code() == code]

    def search_by_name(self, name):
        return [rv for rv in self.list_stop if rv.get_name() == name]

    def search_by_stop_type(self, stop_type):
        return [rv for rv in self.list_stop if rv.get_stop_type() == stop_type]

    def search_by_zone(self, zone):
        return [rv for rv in self.list_stop if rv.get_zone() == zone]

    def search_by_ward(self, ward):
        return [rv for rv in self.list_stop if rv.get_ward() == ward]

    def search_by_address_no(self, address_no):
        return [rv for rv in self.list_stop if rv.get_address_no() == address_no]

    def search_by_street(self, street):
        return [rv for rv in self.list_stop if rv.get_street() == street]

    def search_by_support_disability(self, support_disability):
        return [rv for rv in self.list_stop if rv.get_support_disability() == support_disability]

    def search_by_status(self, status):
        return [rv for rv in self.list_stop if rv.get_status() == status]

    def search_by_lng(self, lng):
        return [rv for rv in self.list_stop if rv.get_lng() == lng]

    def search_by_lat(self, lat):
        return [rv for rv in self.list_stop if rv.get_lat() == lat]

    def search_by_routes(self, routes):
        return [rv for rv in self.list_stop if rv.get_routes() == routes]

    def search_by_search(self, search):
        return [rv for rv in self.list_stop if rv.get_search() == search]

    def search_by_route_id(self, route_id):
        return [rv for rv in self.list_stop if rv.get_route_id() == route_id]

    def search_by_route_var_id(self, route_var_id):
        return [rv for rv in self.list_stop if rv.get_route_var_id() == route_var_id]

    def output_as_json(self, list_output):
        with open('output_stop.json', 'w', encoding='utf8') as fout:
            for data in list_output:
                json.dump(data.__dict__, fout, ensure_ascii=False)
                fout.write('\n')

    def output_as_csv(self, list_output):
        fields = ['stop_id', 'code', 'name', 'stop_type', 'zone', 'ward', 'address_no', 
                  'street', 'support_disability', 'status', 'lng', 'lat', 'routes', 'search', 
                  'route_id', 'route_var_id']
        filename = "output_stop.csv"
        with open(filename, 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for data in list_output:
                writer.writerow(data.__dict__)

