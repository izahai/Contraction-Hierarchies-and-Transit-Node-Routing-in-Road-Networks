class RouteVar:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, route_id, route_var_id, route_var_name, route_var_short_name, 
                 route_no, start_stop, end_stop, distance, outbound, running_time):
        self.route_id = route_id
        self.route_var_id = route_var_id        
        self.route_var_name = route_var_name
        self.route_var_short_name = route_var_short_name
        self.route_no = route_no
        self.start_stop = start_stop 
        self.end_stop = end_stop
        self.distance = distance
        self.outbound = outbound
        self.running_time = running_time

    def __str__(self):
        return f"RouteVar(route_id={self.route_id}, route_var_id={self.route_var_id}, route_var_name={self.route_var_name}, route_var_short_name={self.route_var_short_name}, route_no={self.route_no}, start_stop={self.start_stop}, end_stop={self.end_stop}, distance={self.distance}, outbound={self.outbound}, running_time={self.running_time})"

    def set_route_id(self, x : int):
        self.route_id = x

    def set_route_var_id(self, x : int):
        self.route_var_id = x

    def set_route_var_name(self, x : str):
        self.route_var_name = x

    def set_route_var_short_name(self, x : str):
        self.route_var_short_name = x

    def set_route_no(self, x : str):
        self.route_no = x

    def set_start_stop(self, x : str):
        self.start_stop = x

    def set_distance(self, x : float):
        self.distance = x

    def set_outbound(self, x : bool):
        self.outbound = x

    def set_running_time(self, x : int):
        self.running_time = x
        
    def get_route_id(self) -> int:
        return self.route_id

    def get_route_var_id(self) -> int:
        return self.route_var_id

    def get_route_var_name(self) -> str:
        return self.route_var_name
     
    def get_route_var_short_name(self) -> str:
        return self.route_var_short_name
     
    def get_route_no(self) -> str:
        return self.route_no
     
    def get_start_stop(self) -> str:
        return self.start_stop
     
    def get_end_stop(self) -> str:
        return self.end_stop
     
    def get_distance(self) -> float:
        return self.distance
     
    def get_outbound(self) -> bool:
        return self.outbound
     
    def get_running_time(self) -> int:
        return self.running_time