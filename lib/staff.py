#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import io
import struct

"""
Simple Type Attribute File Format (STAFF)

Staffable types:
 - None, False, True
 - Numbers: int, float, complex
 - Sequences: list, tuple, set, str
 - dict
"""

VERSION = 0

NoneType = type(None)
types = {
    NoneType: 0,
    bool: 1,
    int: 2,
    float: 3,
    complex: 4,
    str: 5,
    list: 6,
    tuple: 7,
    set: 8,
    dict: 9
}

rtypes = {v: k for k,v in types.items()}

SEQ_END = object()

class VersionMismatch(Exception):
    pass

class UnstaffableType(Exception):
    pass

class InvalidType(Exception):
    pass

def dumps(value, buf=None):
    if buf is None:
        buf = bytearray()
        buf.append(VERSION)
    
    type_ = type(value)
    if not type_ in types:
        raise UnstaffableType(f"Value of type {type_} cannot be staffed")
    
    id_ = types[type_]
    closing = 0x80 | id_
    
    buf.append(id_)
    if type_ == NoneType:
        pass
    
    elif type_ == bool:
        buf.append(int(value))
        
    elif type_ == int:
        buf.extend(struct.pack(">i", value))
    
    elif type_ == float:
        buf.extend(struct.pack(">f", value))
    
    elif type_ == complex:
        buf.extend(struct.pack(">ff", value.real, value.imag))
    
    elif type_ == str:
        buf.extend(value.encode("utf-8"))
        buf.append(closing)
    
    elif type_ in [list, tuple, set]:
        for elmt in value:
            dumps(elmt, buf)
        buf.append(closing)
    
    elif type_ == dict:
        for k, v in value.items():
            dumps(k, buf)
            dumps(v, buf)
        
        buf.append(closing)
    
    return bytes(buf)

def loads(buf):
    if type(buf) == bytes:
        buf = io.BytesIO(buf)
        version = buf.read(1)[0]
        if version != VERSION:
            raise VersionMismatch(f"Using version {VERSION} but value was encoded in version {version}")
    
    id_ = buf.read(1)[0]
    
    if id_ & 0x80:
        return SEQ_END
    
    if not id_ in rtypes:
        raise InvalidType(f"Invalid type {id_}. Value cannot be unstaffed")
    
    type_ = rtypes[id_]
    closing = 0x80 | id_
    
    value = None
    
    if type_ == NoneType:
        pass
    
    elif type_ == bool:
        value = bool(buf.read(1)[0])
        
    elif type_ == int:
        value = struct.unpack(">i", buf.read(4))[0]
    
    elif type_ == float:
        value = struct.unpack(">f", buf.read(4))[0]
    
    elif type_ == complex:
        real, imag = struct.unpack(">ff", buf.read(8))
        value = complex(real, imag)
    
    elif type_ == str:
        s = b""
        while True:
            c = buf.read(1)
            if c[0] == closing:
                break
            s += c
        
        value = s.decode("utf-8")
    
    elif type_ in [list, tuple, set]:
        value = []
        while True:
            val = loads(buf)
            if val is SEQ_END: break
            value.append(val)
        
        value = type_(value)
    
    elif type_ == dict:
        value = {}
        while True:
            k = loads(buf)
            if k is SEQ_END: break
            v = loads(buf)
            value[k] = v
    
    return value