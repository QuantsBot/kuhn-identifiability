from fractions import Fraction #少数の丸め誤差を避けて、分数で計算する
cards = ["J","Q","K"]

strategies = {
    "A": {
        "J": Fraction("0.2"),
        "Q": Fraction("0.4"),
        "K": Fraction("0.8"),
    },
    "B": {
        "J": Fraction("0.5"),
        "Q": Fraction("0.4"),
        "K": Fraction("0.5"),
    },

}
for own_card in cards:
    results = {}

    for name ,strategy in strategies.items():
        bet_probability = Fraction(0)

        for opponent_card in cards:
            if opponent_card != own_card:
                bet_probability += (
                    Fraction(1,2) * strategy[opponent_card]
                )

        results[name] = bet_probability

    print(
        f"{own_card}: "
        f"A={float(results['A']):.2f},"
        f"B={float(results['B']):.2f},"
        f"equal={results['A'] == results['B']}"
    )
    
