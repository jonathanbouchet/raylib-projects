from .states import WaveStates


class Scorer:
    def __init__(self, number_enemies: int, remaining_time: float):
        self.number_enemies = number_enemies
        self.remaining_time = remaining_time
        self.wave = 1
        self.wave_state = WaveStates.INIT

    def update(
        self, current_wave_number_enemies: int, current_wave_time: float
    ) -> WaveStates:
        # self.number_enemies = current_wave_number_enemies
        # self.remaining_time = current_wave_time

        if self.number_enemies == 0 and self.remaining_time > 0:
            self.wave_state = WaveStates.SUCCESS
        elif self.remaining_time <= 0 and self.number_enemies > 0:
            self.wave_state = WaveStates.FAIL
        else:
            self.wave_state = WaveStates.ONGOING
            self.number_enemies = current_wave_number_enemies
            self.remaining_time = current_wave_time
        return self.wave_state

    def get_wave_state(self) -> WaveStates:
        return self.wave_state

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
