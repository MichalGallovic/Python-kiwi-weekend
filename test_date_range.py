from date_range import date_range

def test_date_range():
    expected = ['2019-01-01', '2019-01-02', '2019-01-03']
    for i, date in enumerate(date_range('2019-01-01', '2019-01-03')):
        assert expected[i] == date

def test_date_range_across_months():
    expected = ['2019-06-30', '2019-07-01']
    for i, date in enumerate(date_range('2019-06-30', '2019-07-01')):
        assert expected[i] == date