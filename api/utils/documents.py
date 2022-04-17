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
                        },
                        {
                            'method': 'post',
                            'end_point': '/save-budget-details/<int:budget_id>',
                            'description': '',
                            'inputs': '''
                                {
                                    'title': 'string',
                                    'amount': 'float',
                                    'description': 'string'
                                }
                            '''
                        },
                        {
                            'method': 'get',
                            'end_point': '/get-budget-details/<int:budget_id>',
                            'description': '',
                        }
                    ],
                    
                },

                'dept': {
                    'url_prefix': '/api/user/account/dept',
                    'end_points': [
                        {
                            'method': 'post',
                            'end_point': '/add-borrower-to-notebook',
                            'description': '',
                            'inputs': '''
                                { 'name': 'string' }
                            '''
                        },
                        {
                            'method': 'post',
                            'end_point': '/search-user',
                            'description': '',
                            'inputs': '''
                                { 'name': 'string' }
                            '''
                        },
                        {
                            'method': 'get',
                            'end_point': '/retrieve',
                            'description': '',
                        },
                         {
                            'method': 'post',
                            'end_point': '/add-dept/<int:note_id>',
                            'description': '',
                            'inputs': '''
                                { 'amount': float, description: 'string' }
                            '''
                        },
                         {
                            'method': 'get',
                            'end_point': '/retrieve-date/<int:dept_note_id>',
                            'description': 'Retrieve current month',
                            
                        },
                    ]
                }
            }
        }
    ]

} 