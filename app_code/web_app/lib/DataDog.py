from datadog import initialize, api
import os

class DataDog:

    def __init__(self):
        # Getting keys from environment variables
        api_key = os.environ.get('datadog_api_key')
        app_key = os.environ.get('datadog_app_key')
        options = {
            'api_key': api_key[8:-2],
            'app_key': app_key[8:-2]
        }
        initialize(**options)

    # Create DataDog Event
    def create_event(self, project_name):
        title = "New Project Created!"
        tags = ['action:new_project']
        result = api.Event.create(title=title, text=project_name, tags=tags)

        if result['status'] == 'ok':
            return {'result': 'ok'}
        else:
            return {'result': 'failed'}

    # Create Synthetic Test
    def create_test(self, name, description, location, frequency, url, method):
        request = {"method": method, "url": url, "timeout": 30}
        api_check_options = {"tick_every": frequency, "min_failure_duration": 0, "min_location_failed": 1}
        assertions = [
            {"operator": "lessThan", "type": "responseTime", "target": 2000},
            {"operator": "is", "type": "statusCode", "target": 200},
            {"operator": "contains", "property": "content-type", "type": "header", "target": "text/html"}
        ]
        config = {
            "request": request,
            "assertions": assertions
        }
        location_list = self.get_available_locations(location)
        response = api.Synthetics.create_test(name=name, type='api', config=config, options=api_check_options,
                                              locations=location_list, message=description)
        if 'errors' in response:
            result = {'result': 'failed', 'error': response['errors']}
        else:
            result = {'result': 'ok'}
        return result

    # Get available regions for Synthetic tests. Values for pass region variable - US, EU, Asia, all
    def get_available_locations(self, region):
        result = api.Synthetics.get_locations()
        location_list = []
        if region is not 'all':
            for location in result['locations']:
                if location['region'] == region:
                    location_list.append(location['name'])
        else:
            for location in result['locations']:
                location_list.append(location['name'])
        return location_list
