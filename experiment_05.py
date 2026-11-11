cards = ["J", "Q", "K"]
rank = {card: index for index, card in enumerate(cards)}
strategies = {
    "A": {"J": 0.2, "Q": 0.4, "K": 0.8},
    "B": {"J": 0.5, "Q": 0.4, "K": 0.5},
}

fold_payoff = -1
call_win_payoff = 2
call_loss_payoff = -2


def posterior_opponent_probs(model, own_card):
    bet_probs = {
        card: model[card]
        for card in cards
        if card != own_card
    }
    total_bet_prob = sum(bet_probs.values())
    return {
        card: probability / total_bet_prob
        for card, probability in bet_probs.items()
    }


def best_response(model, own_card):
    posterior = posterior_opponent_probs(model, own_card)
    win_prob = sum(
        probability
        for opponent_card, probability in posterior.items()
        if rank[own_card] > rank[opponent_card]
    )
    call_value = (
        win_prob * call_win_payoff
        + (1 - win_prob) * call_loss_payoff
    )
    action = "Call" if call_value > fold_payoff else "Fold"
    return action, win_prob, call_value


def payoff(action, own_card, opponent_card):
    if action == "Fold":
        return fold_payoff
    if rank[own_card] > rank[opponent_card]:
        return call_win_payoff
    return call_loss_payoff


def expected_regret(true_name, assumed_name):
    true_model = strategies[true_name]
    assumed_model = strategies[assumed_name]
    regret = 0.0

    for own_card in cards:
        oracle_action, _, _ = best_response(true_model, own_card)
        chosen_action, _, _ = best_response(assumed_model, own_card)

        for opponent_card in cards:
            if opponent_card == own_card:
                continue

            deal_prob = 1 / len(cards) * 1 / (len(cards) - 1)
            bet_prob = true_model[opponent_card]
            regret += deal_prob * bet_prob * (
                payoff(oracle_action, own_card, opponent_card)
                - payoff(chosen_action, own_card, opponent_card)
            )

    return regret


print("判断場面：相手がBetした後のCall/Fold")
print(
    f"利得設定：Fold={fold_payoff}, "
    f"Call勝ち={call_win_payoff}, Call負け={call_loss_payoff}"
)
print("\n各モデルがBetを見たときに選ぶ行動")

for model_name, model in strategies.items():
    decisions = []
    for own_card in cards:
        action, win_prob, call_value = best_response(model, own_card)
        decisions.append(
            f"{own_card}: {action} "
            f"(勝率={win_prob:.2f}, Call期待利得={call_value:.2f})"
        )
    print(f"モデル{model_name}: " + ", ".join(decisions))

print("\n真の戦略と想定モデル別の期待損失")
for true_name in strategies:
    for assumed_name in strategies:
        regret = expected_regret(true_name, assumed_name)
        print(
            f"真={true_name}, 想定={assumed_name}, "
            f"1ハンド当たり={regret:.4f}, "
            f"1,000ハンド当たり={regret * 1000:.1f}チップ"
        )