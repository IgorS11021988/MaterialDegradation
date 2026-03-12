import numpy as np

from MathProtEnergyProcBase.IndexFunctions import GetIndex, GetIndexes

from .StationFunction import stateCoordinatesNames, reducedTemperaturesEnergyPowersNames, USystemParametersNames
from .fU import fU


# Индексы координат состояния
nuMatInd = GetIndex(stateCoordinatesNames, "nuMat")  # Индекс числа молей недеградированного материала
nuMatDegInd = GetIndex(stateCoordinatesNames, "nuMatDeg")  # Индекс числа молей деградированного материала

# Индексы приведенных температур
TDegMatInd = GetIndex(reducedTemperaturesEnergyPowersNames, "TDegMat")  # # Температура деградирующегося материала
TMatInd = GetIndex(reducedTemperaturesEnergyPowersNames, "TMat")  # Температура недеградирующегося материала

# Индексы переменных параметров системы
vAlphaInd = GetIndex(USystemParametersNames, "vAlpha")  # Индекс потока вещества


# Функция состояния для литий-ионного аккумулятора
def CharacteristicsFunction(t,  # Моменты времени
                            stateCoordinates,  # Координаты состояния
                            reducedTemp,  # Приведенные температуры
                            systemParameters  # Параметры системы
                            ):
    # Получаем динамику тока
    (USystemParameters, _) = fU(t,  # Моменты времени
                                systemParameters  # Параметры системы
                                )
    vAlpha = USystemParameters[:, vAlphaInd]  # Поток вещества в текущие моменты времени

    # Получаем координаты состояния
    nuMat = stateCoordinates[:, nuMatInd]  # Число молей недеградированного материала
    nuMatDeg = stateCoordinates[:, nuMatDegInd]  # Число молей деградированного материала

    # Температуры материала
    TDegMat = reducedTemp[:, TDegMatInd] - 273.15  # Температура деградирующегося материала
    TMat = reducedTemp[:, TMatInd] - 273.15  # Температура недеградирующегося материала

    # Выводим результат
    return (t.reshape(-1,), nuMat, nuMatDeg, TDegMat, TMat, vAlpha)
