class Shipper:

    def __init__(self, shipper_id=None, shipper_name='', phone=''):
        self.shipper_id = shipper_id
        self.shipper_name = shipper_name
        self.phone = phone

    def serialize(self):
        return {
            'shipper_id': self.shipper_id,
            'shipper_phone': self.phone,
            'shipper_name': self.shipper_name
        }