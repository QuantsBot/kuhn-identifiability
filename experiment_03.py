import random  # カード配布・Bet・同点時の判定に使う乱数を読み込む
import math  # 観測の起こりやすさを対数で計算するために読み込む

random.seed(42)  # 同じコードで結果を再現できるように乱数の出発点を固定する

cards = ["J", "Q", "K"]  # 使用するカードをリストに入れる
strategies = {  # 相手のカードごとのBet確率を、戦略別に保存する
    "A": {"J": 0.2, "Q": 0.4, "K": 0.8},  # 戦略AのBet確率
    "B": {"J": 0.5, "Q": 0.4, "K": 0.5},  # 戦略BのBet確率
}  # 戦略の辞書を閉じる

observed_probs = {  # 前回求めた「自分のカード別のBet確率」を保存する
    "A": {"J": 0.60, "Q": 0.50, "K": 0.30},  # 相手が戦略Aの場合
    "B": {"J": 0.45, "Q": 0.50, "K": 0.45},  # 相手が戦略Bの場合
}  # 観測確率の辞書を閉じる

repeats = 200  # 各戦略について、判定実験を200セット繰り返す

for mode in ["全カード", "Qだけ"]:  # 判断に使う情報を2通りに変える
    print(f"\n観測条件：{mode}")  # 現在の観測条件を表示する

    for n in [10, 100, 1000]:  # 1セットの対戦回数を変える
        correct = 0  # 正しく戦略を当てたセット数を0に戻す

        for true_name, strategy in strategies.items():  # 本当の戦略名と設定を取り出す
            for _ in range(repeats):  # 同じ条件で判定実験を繰り返す
                score = 0.0  # 正ならA、負ならBを支持するスコアを初期化する

                for _ in range(n):  # 同じ相手とn回対戦して観測を集める
                    opponent_card, own_card = random.sample(cards, 2)  # 重複なしで2枚配る
                    bet = random.random() < strategy[opponent_card]  # 相手がBetしたかを決める

                    if mode == "Qだけ" and own_card != "Q":  # Q限定で、自分のカードがQでなければ
                        continue  # この対戦の観測を判断に使わず、次の対戦へ進む

                    p_a = observed_probs["A"][own_card]  # Aだった場合のBet確率を取り出す
                    p_b = observed_probs["B"][own_card]  # Bだった場合のBet確率を取り出す

                    if bet:  # 観測した行動がBetなら
                        score += math.log(p_a / p_b)  # Betの起こりやすさの比を対数で加算する
                    else:  # 観測した行動がCheckなら
                        score += math.log((1 - p_a) / (1 - p_b))  # Checkの確率を使って加算する

                if score > 0:  # 観測全体がAで起こりやすかったなら
                    prediction = "A"  # Aと予測する
                elif score < 0:  # 観測全体がBで起こりやすかったなら
                    prediction = "B"  # Bと予測する
                else:  # AとBの起こりやすさが同じなら
                    prediction = random.choice(["A", "B"])  # 手がかりがないので等確率で選ぶ

                if prediction == true_name:  # 予測した戦略が本当の戦略と一致したら
                    correct += 1  # 正解したセット数を1増やす

        accuracy = correct / (2 * repeats)  # A・Bそれぞれ200セット、計400セットでの正解率
        print(f"対戦回数={n:4d}, 正解率={accuracy:.3f}")  # 対戦回数と正解率を表示する