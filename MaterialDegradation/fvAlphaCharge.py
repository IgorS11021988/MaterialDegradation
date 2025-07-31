import numpy as np


# Функция условий протекания процессов
def fvAlphaCharge(t,  # Моменты времени
                  systemParameters  # Параметры системы
                  ):
    # Выделяем параметры динамики
    [OmegaVAlpha,  # Частота колебаний внешнего потока
     AvAlpha  # Амплитуда колебаний внешнего потока
     ] = systemParameters[0:2]

    # Прочие параметры системы
    otherSystemParameters = systemParameters[2::]

    # Рассчитываем ток во внешней цепи
    vAlpha = np.abs(AvAlpha * OmegaVAlpha * np.sin(OmegaVAlpha * t))  # Учитываем колебания

    # Выводим результат
    return (vAlpha, otherSystemParameters)
