from rest_framework.response import Response

class CustomResponse(Response):
    
    def __init__(self,data=None,status=200):
        result={"data": data}
        return super().__init__(result, status)
