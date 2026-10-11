@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

def test_insert_order(db_session):
    order = Order(customer_id=1, amount=50)
    db_session.add(order)
    db_session.commit()
    assert db_session.query(Order).count() == 1 


@pytest.mark.parametrize("amount,expected" [
    (600, "high"), (200, "medium"), (5, "low"),
])
def test_value(amount, expected):
    assert flag_value(amount) == expected


def test_fetch_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"id": 1}
        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda *a, **kw: MockResponse())
    result = fetch_data("url")
    assert result["id"] == 1