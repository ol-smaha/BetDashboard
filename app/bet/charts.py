import json

from bet.constants import get_result_color


class MorrisChartDonut:
    """ For #morris_donut in 'static/vendor/charts/morris-bundle/Morrisjs.js' """

    def __init__(self, input_data):
        self.json_data = self.to_json_data(input_data)

    @staticmethod
    def to_json_data(input_data: dict):
        """
        Example input data:
            {
                'Doe': 80,
                'Moe': 20,
            }
        Example output data (json):
            '[
                {"value": 80, "label": "Doe"},
                {"value": 20, "label": "Moe"}
            ]'
        value: block percent
        label: block name
        """

        data = []
        for name, count in input_data.items():
            row_dict = {
                'value': count or 0,
                'label': name
            }
            data.append(row_dict)
        try:
            json_data = json.dumps(data)
            return json_data
        except Exception as e:
            print(e)
            return '[]'


class MorrisChartLine:
    """ For #morris_line in 'static/vendor/charts/morris-bundle/Morrisjs.js' """

    def __init__(self, input_data):
        self.json_data = self.to_json_data(input_data)

    @staticmethod
    def to_json_data(input_data: dict):
        """
        Example input data:
            {
                2006: {win: 10, drawn: 20, lose: 40},  # one graph line
                2007: {win: 65, drawn: None, lose: 110},
                2008: {win: 40, drawn: 180, lose: 95},
            }
        Example output data (json):
            '[
                {"x": "2006", "win": 10, "drawn": 20, "lose": 40},
                {"x": "2007", "win": 65, "lose": 110},
                {"x": "2007", "win": 40, "drawn": 180, "lose": 95}
            ]'
        x: point on horizontal line 'x' in graphs
        name1, name2, name3, (etc): point to generate graphs line

        one name = one graph line
        """

        data = []
        for x, values_dict in input_data.items():
            row_dict = {}
            row_dict.update({'x': x})

            clean_values_dict = {}
            for key, value in values_dict.items():
                if value is not None:
                    clean_values_dict.update({key: value})

            row_dict.update(clean_values_dict)
            data.append(row_dict)

        try:
            json_data = json.dumps(data)
            return json_data
        except Exception as e:
            print(e)
            return '[]'


class MorrisChartArea(MorrisChartLine):
    """ For #morris_area in 'static/vendor/charts/morris-bundle/Morrisjs.js' """


class MorrisChartStacked:
    """ For #morris_stacked in 'static/vendor/charts/morris-bundle/Morrisjs.js' """

    def __init__(self, input_data):
        self.json_data = self.to_json_data(input_data)

    @staticmethod
    def to_json_data(input_data: dict):
        """
        Example input data:
            {
                2006: {win: 10, drawn: 20, lose: 40},  # one stack vertical block
                2007: {win: 65, drawn: None, lose: 110},
                2008: {win: 40, drawn: 180, lose: 95},
            }
        Example output data (json):
            '[
                {"x": "2006", "win": 10, "drawn": 20, "lose": 40},
                {"x": "2007", "win": 65, "lose": 110},
                {"x": "2007", "win": 40, "drawn": 180, "lose": 95}
            ]'
        x: point on horizontal line 'x' in graphs
        name1, name2, name3, (etc): point to generate graphs line
        """

        data = []
        for x, values_dict in input_data.items():
            row_dict = {}
            row_dict.update({'x': x})

            clean_values_dict = {}
            for key, value in values_dict.items():
                if value:
                    clean_values_dict.update({key: value})

            row_dict.update(clean_values_dict)
            data.append(row_dict)

        try:
            json_data = json.dumps(data)
            return json_data
        except Exception as e:
            print(e)
            return '[]'


class MorrisChartBar(MorrisChartStacked):
    """ For #morris_bar in 'static/vendor/charts/morris-bundle/Morrisjs.js' """


class CalendarDashboard:
    """ For #calendar_bet in 'static/vendor/full-calendar/js/calendar.js' """

    def __init__(self, input_data):
        self.json_data = self.to_json_data(input_data)

    @staticmethod
    def to_json_data(input_data: dict):
        """
        Example input data:
            {
                2018-03-12: [{result: 'Виграш', amount: 100, coefficient: 1.5, profit: 50}],
                2018-03-13: [{result: 'Програш', amount: 200, coefficient: 1.5, profit: -200}],
                2018-03-14: [{result: 'Повернення', amount: 100, coefficient: 2, profit: 0}],
            }
        Example output data (json):
            '[
                {"title": "WIN 50 (100 * 1.5)", "start": "2018-03-12", "backgroundColor": '#ffc108'},
                {"title": "LOSE -200 (200 * 1.5)", "start": "2018-03-13", "backgroundColor": '#25d5f2'},
                {"title": "DRAWN 0 (100 * 2)", "start": "2018-03-14", "backgroundColor": '#ef172c'}
            ]'
        x: point on horizontal line 'x' in graphs
        name1, name2, name3, (etc): point to generate graphs line
        """

        data = []
        for date, objects in input_data.items():
            for obj in objects:
                pre_title = "+" if obj.get('profit') > 0 else ''
                row_dict = {
                    'start': date,
                    'backgroundColor': get_result_color(obj.get('result')),
                    'borderColor': get_result_color(obj.get('result')),
                    'title': f"{pre_title}{obj.get('profit')}",
                }
                data.append(row_dict)

        try:
            json_data = json.dumps(data)
            return json_data
        except Exception as e:
            print(e)
            return '[]'
