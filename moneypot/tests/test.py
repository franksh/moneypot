import unittest
import pandas as pd
from datetime import datetime



# class TestTickerAccessor(unittest.TestCase):

#     basic_test_data = pd.DataFrame([
#         [datetime(year=2020, month=1, day=1, hour=0, minute=0), 10, 12, 9, 11, 0],
#         [datetime(year=2020, month=1, day=1, hour=0, minute=15), 10, 12, 9, 11, 10],
#         [datetime(year=2020, month=1, day=1, hour=0, minute=30), 10, 12, 9, 11, 100],
#         [datetime(year=2020, month=1, day=1, hour=0, minute=45), 10, 12, 9, 11, 50],
#         [datetime(year=2020, month=1, day=1, hour=1, minute=0), 10, 12, 9, 11, 0],
#         [datetime(year=2020, month=1, day=1, hour=1, minute=0), 10, 12, 9, 11, 10],
#     ], columns=['time', 'open', 'high', 'low', 'close', 'volume'])


#     def test_min_columns(self):
#         """ Test that usage fails if not all base columns present"""
#         test_data = TestTickerAccessor.basic_test_data.copy()
#         # Check that validate works
#         test_data.ticker
#         # Check that it fails if columns are missing
#         test_data = test_data.drop('open', axis=1)
#         with self.assertRaises(AttributeError):
#             test_data.ticker

#     def test_resample(self):
#         test_data = TestTickerAccessor.basic_test_data.copy()
#         test_data.ticker.resample("5min")
#         test_data.ticker.resample("1H")
#         test_data.ticker.resample("1D")
#         test_data.ticker.resample("1W")



if __name__ == '__main__':
    unittest.main()
