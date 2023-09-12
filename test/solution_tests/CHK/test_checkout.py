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

    def test_checkout_with_duplicates2(self):
        assert checkout_solution.checkout("AAAAAAAA") == 330

    def test_checkout_with_duplicates3(self):
        assert checkout_solution.checkout("AAAAAAAAA") == 380

    def test_checkout_with_duplicates4(self):
        assert checkout_solution.checkout("AAAAAAAAAA") == 400 

    def test_checkout_with_mv_offers1(self):
        assert checkout_solution.checkout("AAABDBB") == 220

    def test_checkout_with_mv_offers2(self):
        assert checkout_solution.checkout("AAABDABAB") == 290

    def test_checkout_with_gof_offers1(self):
        assert checkout_solution.checkout("EE") == 80

    def test_checkout_with_gof_offers2(self):
        assert checkout_solution.checkout("EEB") == 80

    def test_checkout_with_gof_offers3(self):
        assert checkout_solution.checkout("BEBEEE") == 160

    def test_checkout_with_gof_offers4(self):
        assert checkout_solution.checkout("ABCDEABCDE") == 280

    def test_checkout_with_gof_offers5(self):
        assert checkout_solution.checkout("CCADDEEBBA") == 280
    
    def test_checkout_with_mv_and_gof_offers(self):
        assert checkout_solution.checkout("EAEBAA") == 210

    def test_checkout_with_mp_offers(self):
        assert checkout_solution.checkout("FFF") == 20