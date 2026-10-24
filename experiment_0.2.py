import random
random.seed(42)

cards = ["J","Q","K"]

strategies ={
    "A":{"J":0.2,"Q":0.4,"K":0.8},
    "B":{"J":0.5,"Q":0.4,"K":0.5},
}

trials = 10000

for name, strategy in strategies.items():
    counts = {"J":0,"Q":0,"K":0}
    bet_counts = {"J":0,"Q":0,"K":0}

    for _ in range(trials):
        opponent_card, own_card = random.sample(cards,2)
        counts[own_card] += 1

        if random.random()<strategy[opponent_card]:
            bet_counts[own_card] += 1  # Betした回数を1増やす
    print(f"戦略{name}")  # 今の戦略名を表示する


    for own_card in cards:  # 自分のカード別に結果を表示する
            if counts[own_card] == 0:  # そのカードが一度も配られなかった場合
                print(f"{own_card}: 観測なし")
                continue  # 次のカードへ進む

            rate = bet_counts[own_card] / counts[own_card]  # Betの割合を求める

            print(
                f"{own_card}: "
                f"回数={counts[own_card]}, "
                f"Bet回数={bet_counts[own_card]}, "
                f"Bet割合={rate:.4f}"
            )
        