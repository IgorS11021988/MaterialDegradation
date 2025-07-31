import numpy as np

from .MaterialDegradationFunctionsStation import funNuEMat, funMuMat, funADNu
from MathProtEnergyProc import NonEqSystemQBase

from MathProtEnergyProc.CorrectionModel import PosLinearFilter


# Функция состояния для литий-ионного аккумулятора
def MaterialDegradationStateFunction(stateCoordinates,
                                     reducedTemp,
                                     systemParameters):
    # получаем электрические заряды
    [nuMat,  # Число молей недеградированного материала
     nuMatDeg  # Число молей деградированного материала
     ] = stateCoordinates

    # Получаем температуру
    [TDegMat,  # Температура деградирующегося материала
     TMat  # Температура недеградирующегося материала
     ] = reducedTemp

    # Получаем параметры
    [vAlpha,  # Внешний поток
     Tokr,  # Температура окружающей среды
     sMuDeg,  # Пороговый химический потенциал разрушения
     CMuDegMat,  # Коэффициент химического потенциала деградирующегося материала
     nuMats,  # Характерное число молей
     NuAll,  # Общее число молей материала
     ADNuMat0,  # Коэффициент перестройки расположения атомов
     ADNuMatDeg0,  # Коэффициент деградации материала
     KDegMat,  # Коэффициент теплопередачи деградирующегося материала
     CQDegMat,  # Теплоемкость деградирующегося материала
     KMat,  # Коэффициент теплопередачи недеградирующегося материала
     CQMat,  # Теплоемкость недеградирующегося материала
     alphaADNuMatT,  # Экспоненциальный коэффициент перестройки расположения атомов по температуре
     alphaADNuMatDegT,  # Экспоненциальный коэффициент дегарадции материала по температуре
     bADNuMatT,  # Граничная температура по коэффициенту перестройки расположения атомов
     bADNuMatDegT,  # Граничная температура по коэффициенту деградации материала
     rCADNuMatT,  # Постоянный коэффициент температурной зависимости коэффициента перестройки расположения атомов
     rCADNuMatDegT,  # Постоянный коэффициент температурной зависимости дегарадации материала

     # Получаем довесочные коэффициенты
     betaADNuMatDeg1,
     betaADNuMatDeg2,
     betaADNuMatDeg3,
     betaMu2,
     betaMu3,
     betaADNuMatT2,
     betaADNuMatDegT2,
     betaADNuMatT3,
     betaADNuMatDegT3
     ] = systemParameters

    # Матрица баланса
    balanceMatrix = np.array([])

    # Рассчитываем корректировочный коэффициент потока
    kVAlpha = 1 - np.exp(-nuMat / nuMats)

    # Внешние потоки зарядов
    stateCoordinatesStreams = np.array([-vAlpha * kVAlpha], dtype=np.double)

    # Внешние потоки теплоты
    heatEnergyPowersStreams = np.array([])

    # Выводим температуры
    energyPowerTemperatures = np.array([TDegMat, TMat, Tokr], dtype=np.double)

    # Определяем число молей возбужденных молекул
    (nuEMat, rNuEMat) = funNuEMat(nuMat, nuMatDeg, NuAll)

    # Определяем химические потенциалы деградированного и недеградированного материала
    (muMat, muMatDeg) = funMuMat(nuEMat, rNuEMat,
                                 CMuDegMat, sMuDeg,
                                 betaMu2, betaMu3)

    # Потенциалы взаимодействия энергетических степеней свободы
    potentialInter = np.array([muMat, muMatDeg], dtype=np.double)

    # Потенциалы взаимодействия между энергетическими степенями свободы
    potentialInterBet = np.array([])

    # Доли распределения некомпенсированной теплоты
    beta = np.array([])

    # Определяем сопротивления двойных слоев и мембраны
    (ADNup, ADNun) = funADNu(rNuEMat, TDegMat, muMatDeg, ADNuMat0, ADNuMatDeg0,
                             alphaADNuMatT, alphaADNuMatDegT, bADNuMatT, bADNuMatDegT, rCADNuMatT, rCADNuMatDegT,
                             betaADNuMatT2, betaADNuMatDegT2, betaADNuMatT3, betaADNuMatDegT3,
                             betaADNuMatDeg1, betaADNuMatDeg2, betaADNuMatDeg3)

    # Главный блок кинетической матрицы по процессам
    ADNup = PosLinearFilter(ADNup)
    ADNun = PosLinearFilter(ADNun)
    kineticMatrixPCPC = np.array([ADNup, ADNun], dtype=np.double) * TDegMat / NonEqSystemQBase.GetTbase()

    # Перекрестные блоки кинетической матрицы по процессам
    kineticMatrixPCHeat = np.array([])
    kineticMatrixHeatPC = np.array([])

    # Главный блок кинетической матрицы по теплообмену
    KDegMat = PosLinearFilter(KDegMat)
    KMat = PosLinearFilter(KMat)
    kineticMatrixHeatHeat = np.array([KDegMat * TDegMat * TMat, KMat * TMat * Tokr], dtype=np.double) / NonEqSystemQBase.GetTbase()

    # Обратная теплоемкость литий-ионного аккумулятора
    invHeatCapacityMatrixCf = np.array([1 / CQDegMat, 1 / CQMat], dtype=np.double)

    # Приведенные тепловые эффекты литий-ионного аккумулятора
    heatEffectMatrixCf = potentialInter / CQDegMat

    # Выводим результат
    return (balanceMatrix,
            stateCoordinatesStreams,
            heatEnergyPowersStreams,
            energyPowerTemperatures,
            potentialInter,
            potentialInterBet,
            beta, kineticMatrixPCPC,
            kineticMatrixPCHeat,
            kineticMatrixHeatPC,
            kineticMatrixHeatHeat,
            invHeatCapacityMatrixCf,
            heatEffectMatrixCf)
