import requests
from time import sleep

class Peter:

    def __init__(self, endpoint, params):
        """
            The __init__ method is a constructor, called when a new object is created.
            It initializes the object's attributes. 'self' refers to the instance itself.
        """
        self.endpoint = endpoint
        self.params = params

    def display_info(self):
        print("Display Attributes: ")
        print(f"Parms: {self.params}, url: {self.endpoint}")

    def get_data(self, params):
        print(f"visit: {self.endpoint}\nwith: {params}")
        r = requests.get(self.endpoint, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data

    def get_courseCode_years(self, 
            quarter=None,
            department = None,
            courseNumber = None
        ):
        """
            Get all years a Course Code has appeared
            params = {
                'department': 'MATH',
                'courseNumber': '130A',
                'quarter': 'Fall',
                'Year': None
                }
            Returns: Years (list)
        """
        # Option to use self.params for pass args for new params
        params = self.params.copy()
        if quarter:
            params['quarter'] = quarter
            self.params = quarter
        if department:
            params['department'] = department
        if courseNumber:
            params['courseNumber'] = courseNumber 
            
        # Check if Params are valid for returning all Years 
        if ('year' not in params.keys()) \
            or ('year' in params.keys() and params['year'] == None):
            data = self.get_data(params)

            years = []
            for item in data['data']['sectionList']:
                years.append(item['year'])
            years = set(years) # drop dupelicats

            # typecast to sort chronologically
            years_list = [int(item) for item in years]
            years_list.sort()
            return years_list

        else:
            print(f"""You have year set to {self.params['year']}.
                Set 'year' param to None to find all valid years for specific Course Number
                """
            )
            return []
    
    def get_grades_for_courseNumber_by_years(self,
            quarter=None,
            department = None,
            courseNumber = None
        ):
        
        # Option to use self.params for pass args for new params
        params = self.params.copy()
        if quarter:
            params['quarter'] = quarter
        if department:
            params['department'] = department
        if courseNumber:
            params['courseNumber'] = courseNumber 
        
        # Check if Params are valid for returning all Years 
        if ('year' not in params.keys()) \
            or ('year' in params.keys() and params['year'] == None):
            years = self.get_courseCode_years(
                department=params['department'],
                courseNumber=params['courseNumber']
            )
            print(f"""Get class {params['courseNumber']} grades\n
                for years: {years}
                """
            )
            raw_data = []
            for year in years: 
                params['year'] = str(year)
                print(f"getting course: {params['courseNumber']} {params['quarter']}-{params['year']}")
                data = self.get_data(params)

                # this is gpa data aggregated
                raw_data.append(
                    {
                        'courseNumber': params['courseNumber'],
                        'year': int(data['data']['sectionList'][0]['year']),
                        'quarter': data['data']['sectionList'][0]['quarter'],
                        'gpa': data['data']['gradeDistribution']['averageGPA'] # add +1
                    }
                )
                sleep(1)
            return raw_data
    

    def get_grades_by_sectionCode_by_year(self, 
            year,
            quarter=None,
            department=None,
            courseNumber=None              
        ):

        data = []
        print(f"for year: {year}")

        params_sectin_code_by_year = self.params.copy()
        if quarter:
            params_sectin_code_by_year['quarter'] = quarter
        if department:
            params_sectin_code_by_year['department'] = department
        if courseNumber:
            params_sectin_code_by_year['courseNumber'] = courseNumber 
        params_sectin_code_by_year['year'] = year        

        base_data = self.get_data(params_sectin_code_by_year)

        # --- Step 1: Extract section codes from the response ---
        section_list = base_data.get('data', {}).get('sectionList', [])
        section_codes = [s['sectionCode'] for s in section_list]
        print(f"Found {len(section_codes)} sections: {section_codes}")

        # --- Step 2: Get GPA for each section Code ---
        print(f"Get GPA for each sectionCode: ")

        all_section_data = []
        for code in section_codes:
            params_with_section = params_sectin_code_by_year.copy()
            params_with_section['sectionCode'] = code
            params_with_section['year'] = year

            section_data = self.get_data(params_with_section)

            all_section_data.append(
                {
                    'sectionCode': code,
                    'data': section_data
                })

        print(f"format return data ")
        for item in all_section_data:
            iter_dic = {
                'courseNumber': params_with_section['courseNumber'],
                'year': int(item['data']['data']['sectionList'][0]['year']),
                'quarter': item['data']['data']['sectionList'][0]['quarter'],
                'sectionCode': item['sectionCode'],
                'gpa': item['data']['data']['gradeDistribution']['averageGPA']
            }
            data.append(iter_dic)
       
        return data



if __name__ == "__main__":

    peter = Peter(
        # endpoint url
        endpoint = "https://anteaterapi.com/v2/rest/grades/aggregate",
        # params: Year=None means we will aggregate Math130A for Fall quarter
        params = {
            'department': 'MATH',
            'courseNumber': '130A',
            'quarter': 'Fall'
        }
    )

    # Example Usage:
    # Get Years a courseCode was offered
    # w/ self.params
    my_years = peter.get_courseCode_years()
    print(f"This course code has beem offered during these years: {my_years}")
    
    # # pass function args
    # my_years = peter.get_courseCode_years(
    #         department='MATH', 
    #         courseNumber='121A'
    #     )
    
    # Get Average GPA of a courseNumber for every year
    # note: this is an aggregate of all the courseNumbers 
    # my_data = peter.get_grades_for_courseNumber_by_years(department='MATH', courseNumber='121A')
    # print(my_data)
    # print()

    # Get GPA of specific sectionCode
    # my_data = peter.get_grades_by_sectionCode_by_year(2024, department='MATH', courseNumber='121A')
    # print(my_data)
