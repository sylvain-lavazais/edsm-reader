import json
from datetime import datetime


class Body:
    _key: dict
    _system_key: dict
    _name: str
    _type: str
    _sub_type: str
    _discovery: dict
    _update_time: datetime
    _materials: dict
    _solid_composition: dict
    _atmosphere_composition: dict
    _parents: dict
    _belts: dict
    _rings: dict
    _properties: dict

    @property
    def key(self) -> dict:
        return self._key

    @key.setter
    def key(self, value: dict):
        self._key = value

    @property
    def system_key(self) -> dict:
        return self._system_key

    @system_key.setter
    def system_key(self, value: dict):
        self._system_key = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def sub_type(self) -> str:
        return self._sub_type

    @sub_type.setter
    def sub_type(self, value: str):
        self.sub_type = value

    @property
    def discovery(self) -> dict:
        return self._discovery

    @discovery.setter
    def discovery(self, value: dict):
        self._discovery = value

    @property
    def update_time(self) -> datetime:
        return self._update_time

    @update_time.setter
    def update_time(self, value: datetime):
        self._update_time = value

    @property
    def materials(self) -> dict:
        return self._materials

    @materials.setter
    def materials(self, value: dict):
        self._materials = value

    @property
    def solid_composition(self) -> dict:
        return self._solid_composition

    @solid_composition.setter
    def solid_composition(self, value: dict):
        self._solid_composition = value

    @property
    def atmosphere_composition(self) -> dict:
        return self._atmosphere_composition

    @atmosphere_composition.setter
    def atmosphere_composition(self, value: dict):
        self._atmosphere_composition = value

    @property
    def parents(self) -> dict:
        return self._parents

    @parents.setter
    def parents(self, value: dict):
        self._parents = value

    @property
    def belts(self) -> dict:
        return self._belts

    @belts.setter
    def belts(self, value: dict):
        self._belts = value

    @property
    def rings(self) -> dict:
        return self._rings

    @rings.setter
    def rings(self, value: dict):
        self._rings = value

    @property
    def properties(self) -> dict:
        return self._properties

    @properties.setter
    def properties(self, value: dict):
        self._properties = value

    def __init__(self, dict_from_db: dict = None,
                 key: dict = None,
                 system_key: dict = None,
                 name: str = None,
                 body_type: str = None,
                 sub_type: str = None,
                 discovery: dict = None,
                 update_time: datetime = None,
                 materials: dict = None,
                 solid_composition: dict = None,
                 atmosphere_composition: dict = None,
                 parents: dict = None,
                 belts: dict = None,
                 rings: dict = None,
                 properties: dict = None):
        if dict_from_db is not None:
            key = dict_from_db.get('key', None)
            system_key = dict_from_db.get('system_key', None)
            name = dict_from_db.get('name', None)
            body_type = dict_from_db.get('type', None)
            sub_type = dict_from_db.get('sub_type', None)
            discovery = dict_from_db.get('discovery', None)
            update_time = dict_from_db.get('update_time', None)
            materials = dict_from_db.get('materials', None)
            solid_composition = dict_from_db.get('solid_composition', None)
            atmosphere_composition = dict_from_db.get('atmosphere_composition', None)
            parents = dict_from_db.get('parents', None)
            belts = dict_from_db.get('belts', None)
            rings = dict_from_db.get('rings', None)
            properties = dict_from_db.get('properties', None)
        self._key = key
        self._system_key = system_key
        self._name = name
        self._type = body_type
        self._sub_type = sub_type
        self._discovery = discovery
        self._update_time = update_time
        self._materials = materials
        self._solid_composition = solid_composition
        self._atmosphere_composition = atmosphere_composition
        self._parents = parents
        self._belts = belts
        self._rings = rings
        self._properties = properties

    def to_dict(self):
        return {
                'key'                   : self._key,
                'system_key'            : self._system_key,
                'name'                  : self._name,
                'type'                  : self._type,
                'sub_type'              : self._sub_type,
                'discovery'             : self._discovery,
                'update_time'           : self._update_time,
                'materials'             : self._materials,
                'solid_composition'     : self._solid_composition,
                'atmosphere_composition': self._atmosphere_composition,
                'parents'               : self._parents,
                'belts'                 : self._belts,
                'rings'                 : self._rings,
                'properties'            : self._properties,
        }

    def to_dict_for_db(self):
        return {
                'key'                   : json.dumps(self._key),
                'system_key'            : json.dumps(self._system_key),
                'name'                  : self._name,
                'type'                  : self._type,
                'sub_type'              : self._sub_type,
                'discovery'             : json.dumps(self._discovery),
                'update_time'           : self._update_time,
                'materials'             : json.dumps(self._materials),
                'solid_composition'     : json.dumps(self._solid_composition),
                'atmosphere_composition': json.dumps(self._atmosphere_composition),
                'parents'               : json.dumps(self._parents),
                'belts'                 : json.dumps(self._belts),
                'rings'                 : json.dumps(self._rings),
                'properties'            : json.dumps(self._properties),
        }


def body_from_edsm(edsm_res: dict) -> Body:
    key = {'id': edsm_res['id'], 'id64': edsm_res['id64']}
    name = edsm_res.get('name', None)
    body_type = edsm_res.get('type', None)
    sub_type = edsm_res.get('subType', None)
    discovery = edsm_res.get('discovery', None)
    materials = edsm_res.get('materials', None)
    solid_composition = edsm_res.get('solidComposition', None)
    atmosphere_composition = edsm_res.get('atmosphereComposition', None)
    parents = edsm_res.get('parents', None)
    belts = edsm_res.get('belts', None)
    rings = edsm_res.get('rings', None)
    properties = {
            'body_id'                         : edsm_res.get('bodyId', None),
            'distance_to_arrival'             : edsm_res.get('distanceToArrival', None),
            'is_landable'                     : edsm_res.get('isLandable', None),
            'gravity'                         : edsm_res.get('gravity', None),
            'earth_masses'                    : edsm_res.get('earthMasses', None),
            'radius'                          : edsm_res.get('radius', None),
            'surface_temperature'             : edsm_res.get('surfaceTemperature', None),
            'surface_pressure'                : edsm_res.get('surfacePressure', None),
            'volcanism_type'                  : edsm_res.get('volcanismType', None),
            'atmosphere_type'                 : edsm_res.get('atmosphereType', None),
            'terraforming_state'              : edsm_res.get('terraformingState', None),
            'orbital_period'                  : edsm_res.get('orbitalPeriod', None),
            'semi_major_axis'                 : edsm_res.get('semiMajorAxis', None),
            'orbital_eccentricity'            : edsm_res.get('orbitalEccentricity', None),
            'orbital_inclination'             : edsm_res.get('orbitalInclination', None),
            'arg_of_periapsis'                : edsm_res.get('argOfPeriapsis', None),
            'rotational_period'               : edsm_res.get('rotationalPeriod', None),
            'rotational_period_tidally_locked': edsm_res.get('rotationalPeriodTidallyLocked',
                                                             None),
            'axial_tilt'                      : edsm_res.get('axialTilt', None),
            'reserve_level'                   : edsm_res.get('reserveLevel', None),
    }
    return Body(key=key,
                name=name,
                body_type=body_type,
                sub_type=sub_type,
                discovery=discovery,
                materials=materials,
                solid_composition=solid_composition,
                atmosphere_composition=atmosphere_composition,
                parents=parents,
                belts=belts,
                rings=rings,
                properties=properties)
