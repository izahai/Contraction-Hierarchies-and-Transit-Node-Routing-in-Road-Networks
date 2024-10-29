class Stop:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, stop_id, code, name, stop_type, zone, ward, 
                 address_no, street, support_disability, status, lng, lat, 
                 search, routes, route_id, route_var_id):
        self.stop_id = stop_id
        self.code = code
        self.name = name
        self.stop_type = stop_type
        self.zone = zone
        self.ward = ward
        self.address_no = address_no
        self.street = street
        self.support_disability = support_disability
        self.status = status
        self.lng = lng
        self.lat = lat
        self.search = search
        self.routes = routes
        self.route_id = route_id
        self.route_var_id = route_var_id
    
    def get_stop_id(self) -> int:
        return self.stop_id

    def get_code(self) -> str:
        return self.code

    def get_name(self) -> str:
        return self.name

    def get_stop_type(self) -> str:
        return self.stop_type

    def get_zone(self) -> str:
        return self.zone

    def get_ward(self) -> str:
        return self.ward

    def get_address_no(self) -> str:
        return self.address_no
    
    def get_street(self) -> str:
        return self.street

    def get_support_disability(self) -> str:
        return self.support_disability

    def get_status(self) -> str:
        return self.status

    def get_lng(self) -> float:
        return self.lng

    def get_lat(self) -> float:
        return self.lat
    
    def get_routes(self) -> str:
        return self.routes
    
    def get_search(self) -> str:
        return self.search
    
    def get_route_id(self) -> str:
        return self.route_id
    
    def get_route_var_id(self) -> str:
        return self.route_var_id
    
    def set_stop_id(self, new_id):
        self.stop_id = new_id

    def set_code(self, new_code):
        self.code = new_code

    def set_name(self, new_name):
        self.name = new_name

    def set_stop_type(self, new_type):
        self.stop_type = new_type

    def set_zone(self, new_zone):
        self.zone = new_zone

    def set_ward(self, new_ward):
        self.ward = new_ward

    def set_address_no(self, new_address_no):
        self.address_no = new_address_no

    def set_street(self, new_street):
        self.street = new_street

    def set_supports_disability(self, new_support):
        self.support_disability = new_support

    def set_status(self, new_status):
        self.status = new_status

    def set_lng(self, new_lng):
        self.lng = new_lng

    def set_lat(self, new_lat):
        self.lat = new_lat

    def set_search(self, new_search):
        self.search = new_search

    def set_routes(self, new_routes):
        self.routes = new_routes
    
    def set_route_id(self, new_route_id):
        self.route_id = new_route_id
    
    def set_route_var_id(self, new_route_var):
        self.route_var_id = new_route_var

    def __str__(self):
        info = [
            f"Stop ID: {self.get_stop_id()}",
            f"Code: {self.get_code()}",
            f"Name: {self.get_name()}",
            f"Stop Type: {self.get_stop_type()}",
            f"Zone: {self.get_zone()}",
            f"Ward: {self.get_ward()}",
            f"Address: {self.get_address_no()} {self.get_street()}",
            f"Supports Disability Access: {self.get_support_disability()}",
            f"Status: {self.get_status()}",
            f"Longitude: {self.get_lng()}",
            f"Latitude: {self.get_lat()}",
            f"RouteId: {self.get_route_id()}",
            f"RouteVarId: {self.get_route_var_id()}",
        ]
        return "\n".join(info)