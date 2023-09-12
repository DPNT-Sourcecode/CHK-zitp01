from solutions.CHK import checkout_solution


class TestCheckout():
    def test_checkout(self):
        assert checkout_solution.checkout("ABC") == 100

    def test_checkout_with_offers(self):
        assert checkout_solution.checkout("AAABDB") == 190