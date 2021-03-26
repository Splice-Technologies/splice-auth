import uuid


class UserUtils(object):
    @staticmethod
    def generate_uuid4():
        return uuid.uuid4().hex
