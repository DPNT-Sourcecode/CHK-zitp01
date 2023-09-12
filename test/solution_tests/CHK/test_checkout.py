from solutions.CHK import checkout_solution

class TestCheckout():
    def test_invalid_input(self):
        assert checkout_solution.checkout("1?42") == -1
        assert checkout_solution.checkout("9FNA") == -1

    def test_checkout(self):
        assert checkout_solution.checkout("ABCE") == 140

    def test_checkout_empty_basket(self):
        assert checkout_solution.checkout("") == 0

    def test_checkout_with_duplicates(self):
        assert checkout_solution.checkout("ABCCAD") == 185

    def test_checkout_with_mv_offers1(self):
        assert checkout_solution.checkout("AAABDBB") == 220

    def test_checkout_with_mv_offers2(self):
        assert checkout_solution.checkout("AAABDABAB") == 290

    def test_checkout_with_gof_offers(self):
        assert checkout_solution.checkout("EEB") == 80
    
    def test_checkout_with_mv_and_gof_offers(self):
        assert checkout_solution.checkout("EAEBAA") == 210