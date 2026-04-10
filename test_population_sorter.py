"""
Unit tests for population_sorter module.

Uses pytest fixtures and parametrize to test:
- read_population_data()
- sort_by_area()
- sort_by_population()
"""

import pytest

from population_sorter import (
    read_population_data,
    sort_by_area,
    sort_by_population,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_data():
    """Return a small in-memory list of country dicts for sorting tests."""
    return [
        {"country": "Russia", "area": 17098242, "population": 145934462},
        {"country": "China", "area": 9596960, "population": 1411750000},
        {"country": "India", "area": 3287263, "population": 1380004385},
        {"country": "Germany", "area": 357114, "population": 83783942},
        {"country": "Bangladesh", "area": 147570, "population": 164689383},
    ]


@pytest.fixture
def valid_txt_file(tmp_path):
    """Create a temporary valid .txt file and return its path."""
    content = (
        "Russia, 17098242, 145934462\n"
        "China, 9596960, 1411750000\n"
        "India, 3287263, 1380004385\n"
        "Germany, 357114, 83783942\n"
        "Bangladesh, 147570, 164689383\n"
    )
    filepath = tmp_path / "test_data.txt"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


@pytest.fixture
def empty_txt_file(tmp_path):
    """Create a temporary empty .txt file and return its path."""
    filepath = tmp_path / "empty.txt"
    filepath.write_text("", encoding="utf-8")
    return str(filepath)


@pytest.fixture
def invalid_format_file(tmp_path):
    """Create a .txt file with a badly formatted line."""
    content = "Russia, 17098242\n"  # missing population column
    filepath = tmp_path / "invalid.txt"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


@pytest.fixture
def invalid_numeric_file(tmp_path):
    """Create a .txt file where area/population are not numbers."""
    content = "Russia, big, many\n"
    filepath = tmp_path / "invalid_num.txt"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


# ---------------------------------------------------------------------------
# Tests for read_population_data
# ---------------------------------------------------------------------------

class TestReadPopulationData:
    """Tests for the read_population_data function."""

    def test_returns_list(self, valid_txt_file):
        """Result should be a list."""
        result = read_population_data(valid_txt_file)
        assert isinstance(result, list)

    def test_correct_number_of_records(self, valid_txt_file):
        """Should parse all 5 lines from the file."""
        result = read_population_data(valid_txt_file)
        assert len(result) == 5

    def test_record_has_required_keys(self, valid_txt_file):
        """Each record must contain 'country', 'area', 'population'."""
        result = read_population_data(valid_txt_file)
        for record in result:
            assert "country" in record
            assert "area" in record
            assert "population" in record

    def test_area_is_int(self, valid_txt_file):
        """Area value must be an integer."""
        result = read_population_data(valid_txt_file)
        for record in result:
            assert isinstance(record["area"], int)

    def test_population_is_int(self, valid_txt_file):
        """Population value must be an integer."""
        result = read_population_data(valid_txt_file)
        for record in result:
            assert isinstance(record["population"], int)

    def test_empty_file_returns_empty_list(self, empty_txt_file):
        """An empty file should produce an empty list."""
        result = read_population_data(empty_txt_file)
        assert result == []

    def test_file_not_found_raises(self, tmp_path):
        """Should raise FileNotFoundError for a missing file."""
        missing = str(tmp_path / "nonexistent.txt")
        with pytest.raises(FileNotFoundError):
            read_population_data(missing)

    def test_invalid_format_raises_value_error(self, invalid_format_file):
        """Should raise ValueError when a line has wrong column count."""
        with pytest.raises(ValueError, match="invalid format"):
            read_population_data(invalid_format_file)

    def test_invalid_numeric_raises_value_error(self, invalid_numeric_file):
        """Should raise ValueError when area/population are not numeric."""
        with pytest.raises(ValueError, match="non-numeric"):
            read_population_data(invalid_numeric_file)

    def test_first_record_country_name(self, valid_txt_file):
        """First record should be Russia."""
        result = read_population_data(valid_txt_file)
        assert result[0]["country"] == "Russia"


# ---------------------------------------------------------------------------
# Tests for sort_by_area — parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ascending, expected_first, expected_last", [
    (False, "Russia", "Bangladesh"),   # descending: biggest area first
    (True, "Bangladesh", "Russia"),    # ascending: smallest area first
])
def test_sort_by_area_order(sample_data, ascending, expected_first,
                            expected_last):
    """sort_by_area should correctly order countries by area."""
    result = sort_by_area(sample_data, ascending=ascending)
    assert result[0]["country"] == expected_first
    assert result[-1]["country"] == expected_last


def test_sort_by_area_does_not_mutate(sample_data):
    """sort_by_area must not modify the original list."""
    original = [dict(r) for r in sample_data]
    sort_by_area(sample_data)
    assert sample_data == original


def test_sort_by_area_returns_all_records(sample_data):
    """sort_by_area should return the same number of records."""
    result = sort_by_area(sample_data)
    assert len(result) == len(sample_data)


@pytest.mark.parametrize("ascending", [True, False])
def test_sort_by_area_empty_list(ascending):
    """sort_by_area on an empty list should return an empty list."""
    assert sort_by_area([], ascending=ascending) == []


@pytest.mark.parametrize("ascending", [True, False])
def test_sort_by_area_single_record(ascending):
    """sort_by_area with a single element should return that same element."""
    data = [{"country": "X", "area": 100, "population": 1000}]
    result = sort_by_area(data, ascending=ascending)
    assert result == data


# ---------------------------------------------------------------------------
# Tests for sort_by_population — parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ascending, expected_first, expected_last", [
    (False, "China", "Germany"),        # descending: most populated first
    (True, "Germany", "China"),         # ascending: least populated first
])
def test_sort_by_population_order(sample_data, ascending, expected_first,
                                  expected_last):
    """sort_by_population should correctly order countries by population."""
    result = sort_by_population(sample_data, ascending=ascending)
    assert result[0]["country"] == expected_first
    assert result[-1]["country"] == expected_last


def test_sort_by_population_does_not_mutate(sample_data):
    """sort_by_population must not modify the original list."""
    original = [dict(r) for r in sample_data]
    sort_by_population(sample_data)
    assert sample_data == original


def test_sort_by_population_returns_all_records(sample_data):
    """sort_by_population should return the same number of records."""
    result = sort_by_population(sample_data)
    assert len(result) == len(sample_data)


@pytest.mark.parametrize("ascending", [True, False])
def test_sort_by_population_empty_list(ascending):
    """sort_by_population on an empty list should return an empty list."""
    assert sort_by_population([], ascending=ascending) == []


@pytest.mark.parametrize("ascending", [True, False])
def test_sort_by_population_single_record(ascending):
    """sort_by_population with a single element should return it unchanged."""
    data = [{"country": "X", "area": 100, "population": 1000}]
    result = sort_by_population(data, ascending=ascending)
    assert result == data
