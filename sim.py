import lotto

empire_balls = {1: {'max': 9, 'min': 1, 'repeatable': True},
                2: {'max': 9, 'min': 1, 'repeatable': True},
                3: {'max': 9, 'min': 1, 'repeatable': True},
                4: {'max': 9, 'min': 1, 'repeatable': True}}

overload_balls = {1: {'max': 55, 'min': 1, 'repeatable': False},
                  2: {'max': 55, 'min': 1, 'repeatable': False},
                  3: {'max': 55, 'min': 1, 'repeatable': False},
                  4: {'max': 55, 'min': 1, 'repeatable': False},
                  5: {'max': 55, 'min': 1, 'repeatable': False},
                  6: {'max': 50, 'min': 1, 'repeatable': True},
                  }

empire_prizes = {4: 100}

overload_prizes = {6: 250,
                   5: 100,
                   '4+1': 100,
                   4: 10,
                   '3+1': 10,
                   3: 1}

empire = lotto.LottoGame(empire_balls,
                         0.1,
                         empire_prizes)

overload = lotto.LottoGame(overload_balls,
                           0.1,
                           overload_prizes)


lotto.class_year_sim(500, overload)

