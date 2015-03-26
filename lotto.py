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
        self.jackpot_rollover = 0

    @property
    def max_prize(self):
        prize_keys = self.prizes.keys()
        if all(isinstance(x, int) for x in prize_keys):
            return self.prizes[max(prize_keys)]
        else:
            return 'variable'

    @property
    def gametype(self):
        repeatability = [self.balls[ball]['repeatable'] for ball in self.balls]
        if True in repeatability and False in repeatability:
            return 'mixed'
        elif True in repeatability:
            return 'repeatable'
        else:
            return 'nonrepeatable'

    @property
    def repeatables(self):
        return [(ball, self.balls[ball]) for ball in self.balls
                if self.balls[ball]['repeatable'] is True]

    @property
    def nonrepeatables(self):
        return [(ball, self.balls[ball]) for ball in self.balls
                if self.balls[ball]['repeatable'] is False]

    def validate_ticket(self, ticket):

        def check_range(ball_no, number):
            ball = self.balls[ball_no]
            if ball['min'] <= number <= ball['max']:
                return True
            else:
                return False

        for ball_no, number in enumerate(ticket, start=1):
            if not check_range(ball_no, number):
                raise BallOutOfRange
        if self.gametype == 'repeatable':
            return True
        elif self.gametype == 'nonrepeatable' or self.gametype == 'mixed':
            nonrepeatable_indicies = [ball[0] for ball in self.nonrepeatables]
            nonrepeatable_numbers = [ticket[i-1] for i in nonrepeatable_indicies]
            for number in nonrepeatable_numbers:
                if nonrepeatable_numbers.count(number) > 1:
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
        if self.gametype == 'nonrepeatable':
            numbers.sort()
        return tuple(numbers)

    def evaluate_ticket(self, ticket, winner):
        if self.validate_ticket(ticket):
            if self.gametype == 'repeatable':
                if ticket == winner:
                    return self.max_prize
                else:
                    return 0
            elif self.gametype == 'nonrepeatable':
                hits = 0
                for ball in ticket:
                    if ball in winner:
                        hits += 1
                return self.prizes.get(hits, 0)
            elif self.gametype == 'mixed':
                nonrepeatable_indicies = [ball[0] - 1 for ball in self.nonrepeatables]
                repeatable_indicies = [ball[0] - 1 for ball in self.repeatables]
                hits = 0
                for i in nonrepeatable_indicies:
                    if ticket[i] == winner[i]:
                        hits += 1
                repeatable_hits = 0
                for i in repeatable_indicies:
                    if ticket[i] == winner[i]:
                        repeatable_hits += 1
                if repeatable_hits == 0:
                    return self.prizes.get(hits, 0)
                else:
                    key = "{}+{}".format(hits, repeatable_hits)
                    return self.prizes.get(key, 0)


def class_based_lotto_sim(game, tickets_sold):
    winner = game.quickpick()
    tickets = [game.quickpick() for ticket in range(0, tickets_sold)]
    winners = 0
    payouts = 0
    if game.max_prize != 'variable':
        max_prize = game.max_prize
    else:
        max_prize = game.prizes.get(len(winner), 0)
    for t in tickets:
        prize = game.evaluate_ticket(t, winner)
        if prize is not None:
            if prize == max_prize:
                winners += 1
            else:
                payouts += prize
    income = game.ticket_price * tickets_sold
    if winners > 0:
        jackpot = max_prize + game.jackpot_rollover + income/2.0
        payouts += jackpot
        game.jackpot_rollover = 0
    else:
        game.jackpot_rollover += income/2.0
    net = income - payouts
    print("Jackpot Rollover: {}".format(game.jackpot_rollover))
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