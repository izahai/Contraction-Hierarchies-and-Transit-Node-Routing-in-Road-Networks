class Path:
    def __init__(self, lat, lng, route_id, route_var_id):
        self.lat = lat
        self.lng = lng
        self.route_id = route_id
        self.route_var_id = route_var_id

    def get_lat(self) -> float:
        return self.lat

    def get_lng(self) -> float:
        return self.lng

    def get_route_id(self) -> str:
        return self.route_id

    def get_route_var_id(self) -> str:
        return self.route_var_id

    def set_lat(self, new_lat):
        self.lat = new_lat

    def set_lng(self, new_lng):
        self.lng = new_lng

    def set_route_id(self, new_route_id):
        self.route_id = new_route_id

    def set_route_var_id(self, new_route_var_id):
        self.route_var_id = new_route_var_id

    def __str__(self):
        info = [f"Coordinates: ({self.get_lat()}, {self.get_lng()})",
                f"RouteId: {self.get_route_id()}",
                f"RouteVarId: {self.get_route_var_id()}",
                ]
        return "\n".join(info)