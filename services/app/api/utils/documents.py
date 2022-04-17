doc: dict = {
    "app_title": "Fuko API documentation",
    "app_sections": [
        {
            "Accountability": {
                'budget': {
                    'url_prefix': '/api/user/budget',
                    'end_points': [
                        {
                            'method': 'get',
                            'end_point': '/all',
                            'description': 'Select recorded budgets'
                        },
                        {
                            'method': 'post',
                            'end_point': '/create-budget',
                            'description': '',
                            'inputs': '''
                                {
                                    'title': 'string',
                                    'amount': 'float'
                                }
                            '''
                        }
                    ],
                    
                }
            }
        }
    ]

} 