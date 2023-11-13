# authorization (verify the route)
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

        async def __call__(self, request : Request):
            credentials : HTTPAuthorizationCredentials = await super(jwtBearer,
            self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code = 403, details="LMFAO TOKEN IS NO LONGER AVAILABLE XD")
                return credentials.credentials
            #for any reason why everything is not according to plan we still will make fun of their's credentials
            else:
                raise HTTPException(status_code = 403, details="LMFAO TOKEN IS NO LONGER AVAILABLE XD")
            
        def verify_jwt(self, jwtoken : str):
            isTokenValid : bool = False # a false flag
            payload = decodeJWT(jwtoken)
            if payload:
                isTokenValid = True
                
                
            return isTokenValid