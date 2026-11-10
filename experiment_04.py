import math
import random

random.seed(42)

cards = ["J", "Q", "K"]
strategies = {
    "A": {"J": 0.2, "Q": 0.4, "K": 0.8},
    "B": {"J": 0.5, "Q": 0.4, "K": 0.5},
}
observed_probs = {
    "A": {"J": 0.60, "Q": 0.50, "K": 0.30},
    "B": {"J": 0.45, "Q": 0.50, "K": 0.45},
}

modes = {
    "Jだけ": ["J"],
    "Qだけ": ["Q"],
    "Kだけ": ["K"],
    "J+K": ["J", "K"],
    "全カード": cards,
}
repeats = 200
sample_sizes = [10, 100, 1000]

for mode, allowed_cards in modes.items():
    print(f"\n観測条件：{mode}")

    for sample_size in sample_sizes:
        correct = 0
        total_deals = 0

        for true_name, strategy in strategies.items():
            for _ in range(repeats):
                score = 0.0
                accepted = 0
                deals = 0

                while accepted < sample_size:
                    opponent_card, own_card = random.sample(cards, 2)
                    bet = random.random() < strategy[opponent_card]
                    deals += 1

                    if own_card not in allowed_cards:
                        continue

                    accepted += 1
                    p_a = observed_probs["A"][own_card]
                    p_b = observed_probs["B"][own_card]

                    if bet:
                        score += math.log(p_a / p_b)
                    else:
                        score += math.log((1 - p_a) / (1 - p_b))

                total_deals += deals

                if score > 0:
                    prediction = "A"
                elif score < 0:
                    prediction = "B"
                else:
                    prediction = random.choice(["A", "B"])

                if prediction == true_name:
                    correct += 1

        classifications = 2 * repeats
        accuracy = correct / classifications
        average_deals = total_deals / classifications
        print(
            f"有効観測={sample_size:4d}, "
            f"正解率={accuracy:.3f}, "
            f"平均配布回数/判定={average_deals:.1f}"
        )