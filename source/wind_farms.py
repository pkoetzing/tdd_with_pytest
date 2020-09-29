import csv
from source.external_dependency import magic_full_load_hours


class WindFarms:

    def __init__(self):
        self.data = list()
        self.parameter = [
            'Name', 'Country', 'Commissioning Year',
            'Capacity MW', 'Annual Production GWh']
        self.count = 0

    def add(self, farm: dict):
        for item in self.data:
            if item['Name'] == farm['Name']:
                raise ValueError(
                    f'Wind farm {farm["Name"]} already exists!')
        for key in farm.keys():
            if key not in self.parameter:
                raise KeyError(f'Unknown key {key}')
        self.data.append(farm)
        self.count += 1

    def get_parameter(self, name, parameter):
        if parameter not in self.parameter:
            raise KeyError('Unknown parameter {parameter}')
        for item in self.data:
            if item['Name'] == name:
                if parameter in item:
                    return item.get(parameter, None)

    def update(self, farm: dict):
        for key in farm.keys():
            if key not in self.parameter:
                raise KeyError(f'Unknown key {key}')
        for index, item in enumerate(self.data):
            if item['Name'] == farm['Name']:
                self.data[index] = {**self.data[index], **farm}
                return
        raise ValueError(f'Unknown wind farm {farm["Name"]}')

    def remove(self, name: str):
        for index, item in enumerate(self.data):
            if item['Name'] == name:
                del self.data[index]
                self.count -= 1
                return
        raise ValueError(f'Unknown wind farm {name}')

    def to_csv(self, filename: str):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=self.parameter)
            writer.writeheader()
            for item in self.data:
                writer.writerow(item)

    def forecast_production(self):
        for item in self.data:
            flh = magic_full_load_hours(
                item['Country'], item['Commissioning Year'])
            item['Annual Production GWh'] = flh * item['Capacity MW'] / 1000
