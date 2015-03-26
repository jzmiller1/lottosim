import random

def quickpick():
    return [random.randint(0, 9) for ball in range(0, 4)]

def lottosim(tickets_sold, ticket_cost, jackpot):
    winner = [random.randint(0, 9) for ball in range(0, 4)]
    tickets = [quickpick() for ticket in range(0, tickets_sold)]
    winners = 0
    for t in tickets:
        if t == winner:
            winners += 1
    income = ticket_cost * tickets_sold
    payouts = winners * jackpot
    net = income - payouts
    # print("{} collected, {} jackpot winners, {} net".format(income,
    #                                                         winners,
    #                                                         net))
    return tickets_sold, winners, net

def yearsim(numlottos):
    total_wins = 0
    total_net = 0
    total_tickets = 0
    for lotto in range(0, numlottos):
        tickets, winners, net = lottosim(random.randint(100, 10000),
                                0.1,
                                100)
        total_wins += winners
        total_net += net
        total_tickets += tickets
    print("total tickets {}, total wins {}, total net {}".format(total_tickets,
                                                                 total_wins,
                                                                 total_net))