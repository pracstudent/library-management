import csv
import pytest
from members import Helper

def test_add_and_list(tmp_path, capsys, monkeypatch):
    # 1. Set up temporary CSV file
    file = tmp_path / 'members.csv'
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','name','membership_date'])

    # 2. Change working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # 3. Simulate user input for add_member()
    inputs = iter(['M100','TestUser','2025-05-15'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    Helper.add_member()

    # 4. Capture output from list_members()
    Helper.list_members()
    captured = capsys.readouterr()

    # 5. Assert expected output
    assert 'M100: TestUser (2025-05-15)' in captured.out