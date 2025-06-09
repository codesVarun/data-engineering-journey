def test_transform_continent_data_empty():
    from scripts.transform import transform_continent_data
    df1, df2 = transform_continent_data([])
    assert df1.empty
    assert df2.empty