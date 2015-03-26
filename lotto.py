import random


class RepeatedBallValues(Exception):
    pass


class BallOutOfRange(Exception):
    pass


class LottoGame():

    def __init__(self, balls, ticket_price, prizes={}):
        self.balls = balls
        self.ticket_price = ticket_price
        self.prizes = prizes

    @property
    def repeatable(self):
        for ball in self.balls:
            if not self.balls[ball]['repeatable']:
                return False
        return True

    @property
    def max_prize(self):
        return self.prizes[max(self.prizes.keys())]

    def validate_ticket(self, ticket):

        def check_range(ball, number):
            if ball[1]['min'] <= number <= ball[1]['max']:
                return True

        def check_repeatability(balls):
            for ball in balls:
                if not ball[1]['repeatable']:
                    return False
            return True


        balls = list(self.balls.items())
        repeatable = check_repeatability(balls)
        numbers = []
        for number in ticket:
            for ball in balls:
                if not check_range(ball, number):
                    raise BallOutOfRange
                if repeatable:
                    break
                else:
                    if ticket.count(ball[0]) > 1 and ball[1]['repeatable'] is False:
                        raise RepeatedBallValues
        return True

    def quickpick(self):
        numbers = []
        balls = list(self.balls.items())
        balls.sort()
        for num, ball in balls:
            if ball['repeatable']:
                numbers.append(random.randint(ball['min'], ball['max']))
            else:
                selected = None
                while selected is None:
                    number = random.randint(ball['min'], ball['max'])
                    if number not in numbers:
                        selected = number
                numbers.append(selected)
        if not self.repeatable:
            numbers.sort()
        return tuple(numbers)

    def evaluate_ticket(self, ticket, winner):
        if self.validate_ticket(ticket):
            if self.prizes.get('all') is not None:
                if ticket == winner:
                    return self.prizes['all']
            else:
                if not self.repeatable:
                    hits = 0
                    for ball in ticket:
                        if ball in winner:
                            hits += 1
                    return self.prizes.get(hits, 0)


def class_based_lotto_sim(game, tickets_sold, rollover=False, rollover_amount=0):
    winner = game.quickpick()
    tickets = [game.quickpick() for ticket in range(0, tickets_sold)]
    winners = 0
    payouts = 0
    for t in tickets:
        prize = game.evaluate_ticket(t, winner)
        if prize is not None:
            if prize == game.max_prize:
                winners += 1
            else:
                payouts += prize
    income = game.ticket_price * tickets_sold
    net = income - payouts
    if winners == 1:
        net -= game.max_prize + rollover_amount
    elif winners > 1:
        net -= game.max_prize + rollover_amount
    else:
        rollover_jackpot =
    return tickets_sold, winners, net


def class_year_sim(numlottos, game):
    total_wins = 0
    total_net = 0
    total_tickets = 0
    for lotto in range(0, numlottos):
        tickets, winners, net = class_based_lotto_sim(game, random.randint(1000, 100000))
        total_wins += winners
        total_net += net
        total_tickets += tickets
    print("total tickets {}, total wins {}, total net {}".format(total_tickets,
                                                                 total_wins,
                                                                 total_net))

balls = {1: {'max': 9, 'min': 1, 'repeatable': True},
         2: {'max': 9, 'min': 1, 'repeatable': True},
         3: {'max': 9, 'min': 1, 'repeatable': True},
         4: {'max': 9, 'min': 1, 'repeatable': True}}

nr_balls = {1: {'max': 55, 'min': 1, 'repeatable': False},
            2: {'max': 55, 'min': 1, 'repeatable': False},
            3: {'max': 55, 'min': 1, 'repeatable': False},
            4: {'max': 55, 'min': 1, 'repeatable': False},
            5: {'max': 55, 'min': 1, 'repeatable': False}}

empire_prizes = {'all': 100}

prizes = {5: 100,
          4: 10}

empire = LottoGame(balls, 0.1, empire_prizes)
five_ball = LottoGame(nr_balls, 0.1, prizes)

if __name__ == '__main__':
    ticket = empire.quickpick()
    empire.evaluate_ticket(ticket, ticket)
    # class_year_sim(365, empire)
    ticket = five_ball.quickpick()
    close_ticket = [1] + list(ticket[1:])
    not_close_ticket = [1, 1] + list(ticket[2:])
    bad_ticket = [1, 2] + list(ticket[2:])
    print(five_ball.evaluate_ticket(ticket, ticket))
    print(five_ball.evaluate_ticket(close_ticket, ticket))
    # print(five_ball.evaluate_ticket(not_close_ticket, ticket))
    print(five_ball.evaluate_ticket(bad_ticket, ticket))
    class_year_sim(365, five_ball)