import numpy as np

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
    Pars["TDegMat"] += Pars["Tokr"]  # Начальная температура сождержимого литий-ионного элемента, град С
    Pars["TMat"] += Pars["Tokr"]  # Начальная температура корпуса литий-ионного элемента, град С

    # Корректируем температуры
    Pars[["TDegMat", "TMat", "Tokr", "bADNuMatT", "bADNuMatDegT"]] += 273.15

    # Рассчитываем общее число молей
    Pars["NuAll"] = Pars["nuMat"] + Pars["nuMatDeg"]

    #  Моменты времени
    Tints = integrateAttributes["Tint"].to_numpy()  # Времена интегрирования
    NPoints = np.array(integrateAttributes["NPoints"], dtype=np.int32)  # Числа точек интегрирования
    ts = LinearTimesMoments(Tints,  # Времена интегрирования
                            NPoints  # Числа точек интегрирования
                            )

    # Возвращаем исходные данные динамики системы
    return (Pars, Tints, ts)


# Обработка результатов моделирования динамик
def OutputValues(dyns, fileName,
                 sep, dec, index,
                 plotGraphics=False  # Необходимость построения графиков
                 ):
    # Получаем величины из кортежа
    (t, nuMat, nuMatDeg,
     TDegMat, TMat, vAlpha) = dyns

    # Заголовки и динамики
    dynamicsHeaders = {"Time": t,
                       "nuMat": nuMat,
                       "nuMatDeg": nuMatDeg,
                       "TDegMat": TDegMat,
                       "TMat": TMat,
                       "vAlpha": vAlpha
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
