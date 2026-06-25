class Scorer:
    def __init__(self, number_enemies: int, remaining_time: float):
        self.number_enemies = number_enemies
        self.remaining_time = remaining_time
        self.wave = 1

    def next_wave(self, user_choice) -> None:
        """
        - placeholder for next wave
        - 2 choices are presented to the player:
            - increased number of enemies, same allocated time
            - same number of enemies, decreased allocated time

        :param user_choice: _description_
        :type user_choice: _type_
        """
        if user_choice == "enemy":
            self.number_enemies += 1
        elif user_choice == "time":
            self.remaining_time -= 10  # second
        self.wave += 1
