import numpy as np


# Имена параметров динамик переменных параметров системы
UParametersSystemParametersNames = ["fvAlpha",  # Частота колебаний внешнего потока, Гц
                                    "AvAlpha"  # Амплитуда колебаний внешнего потока, А
                                    ]

# Имена прочих параметров системы
otherSystemParametersNames = ["Tokr",  # Температура окружающей среды, град С
                              "sMuDeg",  # Пороговый химический потенциал разрушения, В
                              "CMuDegMat",  # Коэффициент химического потенциала деградирующегося материала, Дж/моль^2
                              "nuMats",  # Характерное число молей
                              "NuAll",  # Общее число молей материала
                              "ADNuMat0",  # Коэффициент перестройки расположения атомов, См
                              "ADNuMatDeg0",  # Коэффициент деградации материала, См
                              "KDegMat",  # Коэффициент теплопередачи деградируемого материала недеградированному, Вт/К
                              "CQDegMat",  # Теплоемкость деградируемого материала, Дж/К
                              "KMat",  # Коэффициент теплоотдачи недеградируемого материала, Вт/К
                              "CQMat",  # Теплоемкость недеградируемого материала, Дж/К
                              "alphaADNuMatT",  # Экспоненциальный коэффициент перестройки расположения атомов по температуре, 1/К
                              "alphaADNuMatDegT",  # Экспоненциальный коэффициент дегарадции материала по температуре, 1/К
                              "bADNuMatT",  # Граничная температура по коэффициенту перестройки расположения атомов, град С
                              "bADNuMatDegT",  # Граничная температура по коэффициенту деградации материала, град С
                              "rCADNuMatT",  # Постоянный коэффициент температурной зависимости коэффициента перестройки расположения атомов
                              "rCADNuMatDegT",  # Постоянный коэффициент температурной зависимости дегарадации материала

                              "betaADNuMatDeg1",
                              "betaADNuMatDeg2",
                              "betaADNuMatDeg3",
                              "betaMu2",
                              "betaMu3",
                              "betaADNuMatT2",
                              "betaADNuMatDegT2",
                              "betaADNuMatT3",
                              "betaADNuMatDegT3"
                              ]


# Функция условий протекания процессов
def fU(t,  # Моменты времени
       systemParameters  # Параметры системы
       ):
    # Выделяем параметры динамики
    [OmegaVAlpha,  # Частота колебаний внешнего потока
     AvAlpha  # Амплитуда колебаний внешнего потока
     ] = systemParameters[0:len(UParametersSystemParametersNames)]  # Постоянная составляющая тока

    # Прочие параметры системы
    otherSystemParameters = systemParameters[len(UParametersSystemParametersNames)::]

    # Рассчитываем поток вещества
    vAlpha = np.abs(AvAlpha * OmegaVAlpha * np.sin(OmegaVAlpha * t))  # Учитываем колебания

    # Выводим результат
    return (vAlpha, otherSystemParameters)


# Функция параметров вместе с условиями протекания процессов
def fUPar(t,  # Моменты времени
          systemParameters  # Параметры системы
          ):
    # Выделяем параметры динамики и отдельно свойства веществ и процессов
    (USystemParameters,
     otherSystemParameters
     ) = fU(np.array([t], dtype=np.double),  # Моменты времени
            systemParameters  # Параметры системы
            )

    # Выводим результат
    return np.hstack([USystemParameters,
                      otherSystemParameters])
