"""
Спринт 2. Проект спринта: модуль фитнес-трекера.
Ученик когороты 46 Каверин Егор
Связь: caverineg@yandex.ru
"""


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: type,
                duration: float,
                distance: float,
                speed: float,
                calories: float
                ) -> None:
        self.training_type = training_type
        self.duration = "%.3f" % duration
        self.distance = "%.3f" % distance
        self.speed = "%.3f" % speed
        self.calories = "%.3f" % calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '\
                f'Длительность: {self.duration} ч.; '\
                f'Дистанция: {self.distance} км; '\
                f'Ср. скорость: {self.speed} км/ч; '\
                f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""
    #Константы
    LEN_STEP = 0.65 #Длина шага
    M_IN_KM = 1000 #Количество метров в километре
    MIN_IN_H = 60 #Количество минут в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Создания объектов сообщений"""
        return InfoMessage(
            training_type = type(self).__name__,
            duration = self.duration,
            distance = self.get_distance(),
            speed = self.get_mean_speed(),
            calories = self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (coeff_calorie_1 * super().get_mean_speed() - coeff_calorie_2)\
               * self.weight / self.M_IN_KM * self.duration * super().MIN_IN_H


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                height: int
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        return (coeff_calorie_1 * self.weight + \
               (super().get_mean_speed() // self.height)\
               * coeff_calorie_2 * self.weight)\
               * self.duration * super().MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""
    #Константы
    LEN_STEP = 1.38 #Длинга гребка

    def __init__(self,
            action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int,
            ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / \
               super().M_IN_KM / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        return (self.get_mean_speed() + coeff_calorie_1) * \
                coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code = {'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking,
            'Swimming': Swimming,
            'Running': Running,
            'SportsWalking': SportsWalking
    }
    return code[workout_type](*data)

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ] 

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
