from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo" : {
                "title" : "some title about animes",
                "content" : "some content about animes"
            }

        }


class UserSchema(BaseModel):
    fullname : str = Field(default = None)
    email : EmailStr = Field(default = None)
    password : bytes = Field(default = None)
    hasPenis : bool = Field(default = None)
    PhotoURL : str = Field(default = None)
    class Config:
        the_schema = {
            "user_demo": {
                "fullname":"deez",
                "email":"deez@nutz.com",
                "password":"123",
                "hasPenis":True,
                "PhotoURL":"https://inilinkphotocoy.com/jpegorsomething"
            }
        }



class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default = None)
    password : bytes = Field(default = None)
    class Config:
        the_schema = {
            "user_demo": {
                "email":"deez@nutz.com",
                "password":"123"

            }

        }

class getComponent(BaseModel):
    id : int = Field(default=None)
    name : str = Field(default=None)
    desc : str = Field(default=None)
    example : str = Field(default=None)
    class Config:
        the_schema = {
            "getComp_demo": {
                "id":"0",
                "name":"cable",
                "desc":"some stuff",
                "example":"cable.com"
            }

        }


class ForumSchema(BaseModel):
    title : str = Field(default=None)
    category : str = Field(default=None)
    location : str = Field(default=None)
    content : str = Field(default=None)
    imageUrl : str = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo" : {
                "title" : "some title about animes",
                "category" : "anime gelud",
                "location" : "isekai",
                "content" : "some content about animes",
                "imageUrl" : "jpg.jpg"
            }

        }



class CommentSchema (BaseModel):
    comment : str = Field(default=None)
    forumID : int = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo" : {
                "comment" : "Bang info lokasi",
                "forumID" : 1
            }

        }


class ReplySchema (BaseModel):
    comment : str = Field(default=None)
    replyFrom : int = Field(default=None)
    forumID : int = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo" : {
                "comment" : "Bang info lokasi",
                "replyFrom" : 1,
                "forumID" : 1
            }

        }