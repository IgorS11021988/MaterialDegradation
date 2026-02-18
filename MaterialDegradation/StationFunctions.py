import numpy as np


# Вспомогательные функции
def funADNuT(alphaRT, bRT, TDegMat, rCRT):  # Мультипликативная корректировка по температуре
    return np.exp(-alphaRT * (TDegMat - bRT)) + rCRT


def funNuEMat(nuMat, nuMatDeg, NuAll):
    # Вычисляем число молей материала в возбужденном состоянии
    nuEMat = NuAll - nuMatDeg - nuMat

    # Вычисляем и возвращаем число и относительное число молей материала в возбужденном состоянии
    return (nuEMat, nuEMat / NuAll)


def funMuMat(nuEMat, rNuEMat,
             CMuDegMat, sMuDeg,
             betaMu2, betaMu3):  # Приведенные химические потенциалы исходного и деградированного материала
    # Определяем приведенное число молей молекул в возбужденном состоянии
    kNuEMat = 1 + betaMu2 * rNuEMat + betaMu3 * np.power(rNuEMat, 2)

    # Определяем химические потенциалы
    muMat = nuEMat * kNuEMat * CMuDegMat  # Химический потенциал недеградированного материала
    muMatDeg = muMat - sMuDeg  # Химический потенциал деградированного материала

    # Выводим результат
    return (muMat, muMatDeg)


# Функции для свойств веществ и процессов
def funADNu(rNuEMat, TDegMat, muMatDeg, ADNuMat0, ADNuMatDeg0,
            alphaADNuMatT, alphaADNuMatDegT, bADNuMatT, bADNuMatDegT, rCADNuMatT, rCADNuMatDegT,
            betaADNuMatT2, betaADNuMatDegT2, betaADNuMatT3, betaADNuMatDegT3,
            betaADNuMatDeg1, betaADNuMatDeg2, betaADNuMatDeg3):  # Функция сопротивления
    # Определяем корректировку сопротивления двойных слоев через температуру
    aTDNup = funADNuT(alphaADNuMatT, bADNuMatT, TDegMat, rCADNuMatT)
    aTDNun = funADNuT(alphaADNuMatDegT, bADNuMatDegT, TDegMat, rCADNuMatDegT)

    # Добавляем довесочные члены к корректировкам сопротивления двойных слоев через температуру
    aTDNup += betaADNuMatT2 * np.power(aTDNup, 2) + betaADNuMatT3 * np.power(aTDNup, 3)
    aTDNun += betaADNuMatDegT2 * np.power(aTDNun, 2) + betaADNuMatDegT3 * np.power(aTDNun, 3)

    # Определяем корректировочный концентрационный коэффициент
    kADNuMatDeg = 1 + betaADNuMatDeg1 * rNuEMat + betaADNuMatDeg2 * np.power(rNuEMat, 2) + betaADNuMatDeg3 * np.power(rNuEMat, 3)

    # Добавляем вентильный коэффициент
    cNuDeg = (np.sign(muMatDeg) + 1) / 2

    # Выводим результат
    return np.array([ADNuMat0 / aTDNup, ADNuMatDeg0 * kADNuMatDeg * cNuDeg / aTDNun], dtype=np.double)
