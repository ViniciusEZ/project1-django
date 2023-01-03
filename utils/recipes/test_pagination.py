from unittest import TestCase
from utils.recipes.pagination import make_pagination_range # noqa 


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)
        
        
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        # Current_page = 1 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)
        
        # Current_page = 2 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)
        
        # Current_page = 3 - qtd_page = 4 - middle page = 2
        #Here the range should change
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2,3,4,5], pagination)
        
        
        # Current_page = 4 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3,4,5,6], pagination)
        
        
    def test_make_sure_middle_ranges_are_correct(self):
        # Current_page = 3 - qtd_page = 4 - middle page = 2
        #Here the range should change
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2,3,4,5], pagination)
        
        
        # Current_page = 4 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3,4,5,6], pagination)
        
        
         # Current_page = 10 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9,10,11,12], pagination)
        
        
         # Current_page = 10 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=13,
        )['pagination']
        self.assertEqual([12,13,14,15], pagination)
        
        
        
    def test_make_pagination_range_is_static_when_last_page_is_the_next(self):
        # Current_page = 18 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)
        
        # Current_page = 19 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)
        
        
        # Current_page = 20 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)
        
        
        # Current_page = 21 - qtd_page = 4 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)
        
        
        
        