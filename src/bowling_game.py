class Game:

    def __init__(self):
        self._frames = []

        for i in range(10): self._frames.append([[], ""])
        self._frame = 0
        self._score = 0


    def roll(self, pins) -> None:
        if self._frame == 10: raise IndexError("10 frames already have done")
        if pins > 10: raise ValueError("A roll cannot score more than 10 points")
        if pins < 0: raise ValueError("Pins can't be a negative number")

        self._frames[self._frame][0].append(pins)

        if self._frame == 9:
            if len(self._frames[self._frame][0]) == 2:
                if pins + self._frames[self._frame][0][0] < 10:
                    self._frame += 1
            elif len(self._frames[self._frame][0]) == 3:
                self._frame += 1
        else:
            if len(self._frames[self._frame][0]) == 2:
                if pins + self._frames[self._frame][0][0] < 10:
                    self._frames[self._frame][1] = "open"
                elif pins + self._frames[self._frame][0][0] == 10:
                    self._frames[self._frame][1] = "spare"
                else:
                    raise ValueError("Got more than 10 pins down in 1 frame")
                self._frame += 1
            else:
                if pins == 10:
                    self._frames[self._frame][1] = "strike"

                    self._frame += 1

    def score(self) -> int:
        for i in range(9):
            if self._frames[i][1] == "strike":
                self._score += 10 + sum((self._frames[i + 1][0] + (self._frames[i + 2][0] if i < 8 else []))[:2])
            elif self._frames[i][1] == "spare":
                self._score += 10 + self._frames[i + 1][0][0]
            else:
                self._score += sum(self._frames[i][0])

        self._score += sum(self._frames[9][0])

        return self._score


if __name__ == "__main__":
    game = Game()
    game.roll(10)
    game.roll(4)
    game.roll(4)

    print(game.score())
