
from django.core.serializers.json import Serializer as JSON_Serializer
import json

class Serializer (JSON_Serializer):
    """
    Serialize database objects as nested dicts
    without model name and then by primary key.
    """
    def get_dump_object(self, obj):
        new_current = self._current
        coordinates = json.loads(self._current['coordinates'])
        revert_coordinates = coordinates

        """ if necessary revert coordinate (y,x to x,y)"""
        # revert_coordinates = []
        # for point in coordinates:
        #     revert_coordinates.append(point)
        #
        #     revert_coordinates.append([point[1],point[0]])

        new_current['coordinates'] = revert_coordinates
        return new_current