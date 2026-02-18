import numpy as np
from matplotlib.pyplot import show

from MathProtEnergyProcSynDatas.TimesMoments import LinearTimesMoments
from MathProtEnergyProcSynDatas.Indicate import PlotGraphicIndicate, SaveDynamicToFileIndicate
from MathProtEnergyProcSynDatas.File import DynamicSaveAndSaveGraphics


# Функция расчета динамики
def InputArrayCreate(Pars,  # Параметры

                     integrateAttributes  # Аттрибуты интегрирования
                     ):  # Формирование массивов входных параметров
    # Корректируем частотные характеристики
    Pars["fvAlpha"] *= 2 * np.pi

    # Начальное состояние
    Pars["TDegMat0"] += Pars["Tokr"]  # Начальная температура сождержимого литий-ионного элемента, град С
    Pars["TMat0"] += Pars["Tokr"]  # Начальная температура корпуса литий-ионного элемента, град С

    # Корректируем температуры
    Pars[["TDegMat0", "TMat0", "Tokr", "bADNuMatT", "bADNuMatDegT"]] += 273.15

    # Рассчитываем общее число молей
    Pars["NuAll"] = Pars["nuMat0"] + Pars["nuMatDeg0"]

    # Массив параметров
    systemParameters = Pars[["fvAlpha",  # Частота колебаний внешнего потока, Гц
                             "AvAlpha",  # Амплитуда колебаний внешнего потока, А
                             "Tokr",  # Температура окружающей среды, град С
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
                             ]].to_numpy()

    # Массив начальных состояний
    stateCoordinates0 = Pars[["nuMat0", "nuMatDeg0"]].to_numpy()
    reducedTemp0 = Pars[["TDegMat0", "TMat0"]].to_numpy()

    # Моменты времени
    Tints = np.array(integrateAttributes["Tint"], dtype=np.double)  # Времена интегрирования
    NPoints = np.array(integrateAttributes["NPoints"], dtype=np.int32)  # Числа точек интегрирования
    ts = LinearTimesMoments(Tints,  # Времена интегрирования
                            NPoints  # Числа точек интегрирования
                            )

    # Возвращаем исходные данные динамики системы
    return (Tints,
            stateCoordinates0,
            reducedTemp0,
            systemParameters,
            ts)


def OutputValues(dyns, fileName,
                 sep, dec, index,
                 plotGraphics=False  # Необходимость построения графиков
                 ):
    # Получаем величины из кортежа
    (t, nuMat, nuMatDeg,
     TDegMat, TMat, vAlpha) = dyns

    # Заголовки и динамики
    dynamicsHeaders = {"Time": t.reshape(-1,),
                       "nuMat": nuMat.reshape(-1,),
                       "nuMatDeg": nuMatDeg.reshape(-1,),
                       "TDegMat": TDegMat.reshape(-1,),
                       "TMat": TMat.reshape(-1,),
                       "vAlpha": vAlpha.reshape(-1,)
                       }

    # Одиночные графики на полотне
    oneTimeValueGraphics = [{"values": vAlpha,  # Величины в моменты времени
                             "graphName": "Скорость деформации маериала",  # Имя полотна
                             "yAxesName": "Скорость деформации, рад/с",  # Имя оси ординат
                             "graphFileBaseName": "VExtStream"  # Имя файла графика
                             }]

    # Группы графиков на полотне
    timesValuesGraphics = [{"listValues": [TDegMat, TMat],  # Список величин в моменты времени
                            "listValuesNames": ["Деградирующийся материал",
                                                "Недеградирующийся материал"],  # Список имен величин (в моменты времени)
                            "graphName": "Температуры материалов",  # Имя полотна
                            "yAxesName": "Температура, град С",  # Имя оси
                            "graphFileBaseName": "MaterialTemperature"  # Имя файла графика
                            },

                           {"listValues": [nuMat, nuMatDeg],  # Список величин в моменты времени
                            "listValuesNames": ["Недеградированный материал",
                                                "Деградированный материал"],  # Список имен величин (в моменты времени)
                            "graphName": "Числа молей материалов",  # Имя полотна
                            "yAxesName": "Число молей",  # Имя оси
                            "graphFileBaseName": "MaterialMoles"  # Имя файла графика
                            }]

    # Сохраняем динамику в .csv файл и отображаем графики
    DynamicSaveAndSaveGraphics(dynamicsHeaders,  # Словарь динамик с заголовками
                               fileName,  # Имя файла динамик

                               t,  # Моменты времени
                               oneTimeValueGraphics,  # Один график на одном полотне
                               timesValuesGraphics,  # Несколько графиков на одном полотне

                               plotGraphics,  # Необходимость построения графиков

                               sep, dec,   # Разделители (csv и десятичный соответственно)

                               saveDynamicIndicator=SaveDynamicToFileIndicate,  # Индикатор сохранения динамики
                               saveGraphicIndicator=PlotGraphicIndicate,  # Индикатор отображения графиков
                               index=index  # Индекс динамики
                               )
  show()
