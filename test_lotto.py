import unittest
import lotto


class TestGame(unittest.TestCase):
    def setUp(self):
        self.empire_balls = {1: {'max': 9, 'min': 1, 'repeatable': True},
                             2: {'max': 9, 'min': 1, 'repeatable': True},
                             3: {'max': 9, 'min': 1, 'repeatable': True},
                             4: {'max': 9, 'min': 1, 'repeatable': True}}

        self.five_ball_balls = {1: {'max': 55, 'min': 1, 'repeatable': False},
                                2: {'max': 55, 'min': 1, 'repeatable': False},
                                3: {'max': 55, 'min': 1, 'repeatable': False},
                                4: {'max': 55, 'min': 1, 'repeatable': False},
                                5: {'max': 55, 'min': 1, 'repeatable': False}}

        self.overload_balls = {1: {'max': 55, 'min': 1, 'repeatable': False},
                               2: {'max': 55, 'min': 1, 'repeatable': False},
                               3: {'max': 55, 'min': 1, 'repeatable': False},
                               4: {'max': 55, 'min': 1, 'repeatable': False},
                               5: {'max': 55, 'min': 1, 'repeatable': False},
                               6: {'max': 50, 'min': 1, 'repeatable': True},
                               }

        self.empire_prizes = {4: 100}

        self.five_ball_prizes = {5: 100,
                                 4: 10,
                                 3: 1}

        self.overload_prizes = {5: 100,
                                '4+1': 100,
                                4: 10,
                                '3+1': 10,
                                3: 1}

        self.empire = lotto.LottoGame(self.empire_balls,
                                      0.1,
                                      self.empire_prizes)
        self.five_ball = lotto.LottoGame(self.five_ball_balls,
                                         0.1,
                                         self.five_ball_prizes)
        self.overload = lotto.LottoGame(self.overload_balls,
                                        0.1,
                                        self.overload_prizes)

    def test_max_prize(self):
        self.assertEquals(self.empire.max_prize, 100)
        self.assertEquals(self.five_ball.max_prize, 100)
        self.assertEquals(self.overload.max_prize, 'variable')

    def test_gametype(self):
        self.assertEquals(self.empire.gametype, 'repeatable')
        self.assertEquals(self.five_ball.gametype, 'nonrepeatable')
        self.assertEquals(self.overload.gametype, 'mixed')

    def test_repeatables(self):
        self.assertEquals(self.empire.repeatables,
                          [(1, {'max': 9, 'min': 1, 'repeatable': True}),
                           (2, {'max': 9, 'min': 1, 'repeatable': True}),
                           (3, {'max': 9, 'min': 1, 'repeatable': True}),
                           (4, {'max': 9, 'min': 1, 'repeatable': True})])
        self.assertEquals(self.five_ball.repeatables, [])
        self.assertEquals(self.overload.repeatables,
                          [(6, {'max': 50, 'min': 1, 'repeatable': True})])

    def test_nonrepeatables(self):
        self.assertEquals(self.empire.nonrepeatables, [])
        self.assertEquals(self.five_ball.nonrepeatables,
                          [(1, {'max': 55, 'min': 1, 'repeatable': False}),
                           (2, {'max': 55, 'min': 1, 'repeatable': False}),
                           (3, {'max': 55, 'min': 1, 'repeatable': False}),
                           (4, {'max': 55, 'min': 1, 'repeatable': False}),
                           (5, {'max': 55, 'min': 1, 'repeatable': False})])
        self.assertEquals(self.overload.nonrepeatables,
                          [(1, {'max': 55, 'min': 1, 'repeatable': False}),
                           (2, {'max': 55, 'min': 1, 'repeatable': False}),
                           (3, {'max': 55, 'min': 1, 'repeatable': False}),
                           (4, {'max': 55, 'min': 1, 'repeatable': False}),
                           (5, {'max': 55, 'min': 1, 'repeatable': False})])

    def test_validate_ticket(self):
        self.assertTrue(self.empire.validate_ticket((1, 2, 3, 4)))
        self.assertTrue(self.empire.validate_ticket((1, 1, 1, 1)))
        self.assertRaises(lotto.BallOutOfRange,
                          self.empire.validate_ticket,
                          (1, 100, 3, 4))
        self.assertTrue(self.five_ball.validate_ticket((1, 2, 3, 4, 5)))
        self.assertRaises(lotto.RepeatedBallValues,
                          self.five_ball.validate_ticket,
                          (1, 1, 1, 1, 1))
        self.assertRaises(lotto.BallOutOfRange,
                          self.five_ball.validate_ticket,
                          (1, 100, 3, 4, 5))
        self.assertTrue(self.overload.validate_ticket((1, 2, 3, 4, 5, 3)))
        self.assertRaises(lotto.RepeatedBallValues,
                          self.overload.validate_ticket,
                          (1, 1, 1, 1, 1, 1))
        self.assertRaises(lotto.BallOutOfRange,
                          self.overload.validate_ticket,
                          (1, 100, 3, 4, 5, 1))

    def test_quickpick(self):
        ticket = self.empire.quickpick()
        self.assertTrue(self.empire.validate_ticket(ticket))
        ticket = self.five_ball.quickpick()
        self.assertTrue(self.five_ball.validate_ticket(ticket))
        ticket = self.overload.quickpick()
        self.assertTrue(self.overload.validate_ticket(ticket))

    def test_evaluate_ticket(self):
        # TEST EMPIRE
        ticket = (1, 1, 1, 1)
        losing_ticket = (1, 1, 1, 2)
        self.assertEquals(self.empire.evaluate_ticket(ticket, ticket),
                          self.empire.max_prize)
        self.assertEquals(self.empire.evaluate_ticket(losing_ticket, ticket),
                          0)
        # TEST FIVE BALL
        ticket = (1, 2, 3, 4, 5)
        ticket_45 = (1, 2, 3, 4, 10)
        ticket_35 = (1, 2, 3, 10, 11)
        losing_ticket = (7, 8, 9, 10, 11)
        # TEST JACKPOT WIN (5/5)
        self.assertEquals(self.five_ball.evaluate_ticket(ticket, ticket),
                          self.five_ball.max_prize)
        # TEST (4/5)
        self.assertEquals(self.five_ball.evaluate_ticket(ticket_45, ticket),
                          self.five_ball.prizes[4])
        # TEST (3/5)
        self.assertEquals(self.five_ball.evaluate_ticket(ticket_35, ticket),
                          self.five_ball.prizes[3])
        # TEST LOSS
        self.assertEquals(self.five_ball.evaluate_ticket(losing_ticket, ticket),
                          0)
        # TEST OVERLOAD
        ticket = (1, 2, 3, 4, 5, 6)
        ticket_5 = (1, 2, 3, 4, 5, 10)
        ticket_5_complex = (1, 2, 3, 4, 5, 1)
        ticket_4 = (1, 2, 3, 4, 10, 11)
        ticket_4p1 = (1, 2, 3, 4, 10, 6)
        ticket_3 = (1, 2, 3, 10, 11, 12)
        ticket_3p1 = (1, 2, 3, 54, 55, 6)
        losing_ticket = (7, 8, 9, 10, 11, 12)
        # # TEST JACKPOT WIN (5/5)
        # self.assertEquals(self.overload.evaluate_ticket(ticket, ticket),
        #                   self.overload.max_prize)
        # TEST (5/6)
        self.assertEquals(self.overload.evaluate_ticket(ticket_5, ticket),
                          self.overload.prizes[5])
        # TEST (5/6) COMPLEX
        self.assertEquals(self.overload.evaluate_ticket(ticket_5_complex, ticket),
                          self.overload.prizes[5])
        # TEST (4+1)
        self.assertEquals(self.overload.evaluate_ticket(ticket_4p1, ticket),
                          self.overload.prizes['4+1'])
        # TEST (4/6)
        self.assertEquals(self.overload.evaluate_ticket(ticket_4, ticket),
                          self.overload.prizes[4])
        # TEST (3+1)
        self.assertEquals(self.overload.evaluate_ticket(ticket_3p1, ticket),
                          self.overload.prizes['3+1'])
        # TEST (3/6)
        self.assertEquals(self.overload.evaluate_ticket(ticket_3, ticket),
                          self.overload.prizes[3])
        # TEST LOSS
        self.assertEquals(self.overload.evaluate_ticket(losing_ticket, ticket),
                          0)

    def tearDown(self):
        pass

