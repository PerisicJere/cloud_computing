def is_spare(first_roll: int, second_roll: int) -> bool:
    return first_roll + second_roll == 10


def is_strike(first_roll: int) -> bool:
    return first_roll == 10


def strike_bonus(first_roll: int, second_roll: int) -> int:
    return 10 + first_roll + second_roll


def spare_bonus(first_roll: int) -> int:
    return 10 + first_roll


class Game:
    def __init__(self):
        self.game_score = 0
        self.rolls = []
        self.current_roll = 0

    def roll(self, pins: int) -> None:
        self.rolls.append(pins)
        self.current_roll = pins

    def score(self) -> int:
        frameIndex = 0
        for i in range(0, len(self.rolls), 2):
            if is_strike(self.rolls[frameIndex]) == 10:
                bonus = strike_bonus(
                    self.rolls[frameIndex + 1], self.rolls[frameIndex + 2]
                )
                self.game_score += bonus
                frameIndex += 1
            elif is_spare(self.rolls[frameIndex], self.rolls[frameIndex + 1]):
                bonus = spare_bonus(self.rolls[frameIndex + 2])
                self.game_score += bonus
                frameIndex += 2
            else:
                self.game_score += self.rolls[frameIndex] + self.rolls[frameIndex + 1]
                frameIndex += 2
        return self.game_score
