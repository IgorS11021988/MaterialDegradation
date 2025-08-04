import numpy as np

from .fvAlphaCharge import fvAlphaCharge


# Функция состояния для литий-ионного аккумулятора
def CharacteristicsFunction(t,  # Моменты времени
                            stateCoordinates,  # Координаты состояния
                            reducedTemp,  # Приведенные температуры
                            systemParameters  # Параметры системы
                            ):
    # Получаем динамику тока
    (vAlpha, otherSystemParameters) = fvAlphaCharge(np.array(t, dtype=np.double),  # Моменты времени
                                                    systemParameters  # Параметры системы
                                                    )
    vAlpha = np.array(vAlpha, dtype=np.double).reshape(-1)  # Приводим потоки к одномерному массиву

    # Получаем координаты состояния
    nuMat = stateCoordinates[:, 0]  # Число молей недеградированного материала
    nuMatDeg = stateCoordinates[:, 1]  # Число молей деградированного материала

    # Температуры материала
    TDegMat = reducedTemp[:, 0] - 273.15  # Температура деградирующегося материала
    TMat = reducedTemp[:, 1] - 273.15  # Температура недеградирующегося материала

    # Выводим результат
    return (t, nuMat, nuMatDeg, TDegMat, TMat, vAlpha)
