from .states import WaveStates


class Scorer:
    def __init__(self, number_enemies: int, remaining_time: float):
        self.number_enemies = number_enemies
        self.remaining_time = remaining_time
        self.original_number_enemies = number_enemies
        self.original_remaining_time = remaining_time
        self.wave = 1
        self.wave_state = WaveStates.INIT
        self.player_has_shot: int = 0

    def update(
        self, current_wave_number_enemies: int, current_wave_time: float
    ) -> WaveStates:
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

    def get_player_current_score(self) -> int:
        return self.player_has_shot

    def next_wave(self, user_choice: int) -> None:
        """
        - placeholder for next wave
        - 2 choices are presented to the player:
            - increased number of enemies, same allocated time
            - same number of enemies, decreased allocated time

        :param user_choice: _description_
        :type user_choice: _type_
        """
        self.wave += 1
        if user_choice == 1:
            self.number_enemies = self.original_number_enemies + 1
            self.remaining_time = self.original_remaining_time
        elif user_choice == 2:
            self.remaining_time = self.original_remaining_time - 1
            self.number_enemies = self.original_number_enemies
        self.original_number_enemies = self.number_enemies
        self.original_remaining_time = self.remaining_time
        print(self)

    def __repr__(self) -> str:
        return f"state: {self.wave_state}, wave #: {self.wave}, # ast: ({self.number_enemies}), time:{self.remaining_time}"
