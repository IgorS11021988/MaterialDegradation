import numpy as np

from .fvAlphaCharge import fvAlphaCharge


# Функция условий протекания процессов
def fU(t,  # Моменты времени
       systemParameters  # Параметры системы
       ):
    # Выделяем параметры динамики и отдельно свойства веществ и процессов
    (vAlpha, otherSystemParameters) = fvAlphaCharge(np.array([t], dtype=np.double),  # Моменты времени
                                                    systemParameters  # Параметры системы
                                                    )

    # Выводим результат
    return np.hstack((vAlpha, otherSystemParameters))
