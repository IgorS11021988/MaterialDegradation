from MathProtEnergyProc import NonEqSystemQ
from MathProtEnergyProc import NonEqSystemQDyn
from MathProtEnergyProc.IntegrateDyn import standartIntegrateDyn

from .MaterialDegradationFunctionStation import MaterialDegradationStateFunction
from .MaterialDegradationFunctionCharacteristics import MaterialDegradationCharacteristicsFunction
from .fU import fU


# Функция расчета динамики
def MaterialDegradationStructureDynamic(integrateMethod  # Метод интегрирования дифференциальных уравнений
                                        ):  # Структура для расчета одной динамики
    # Описываем структуру литий-ионного элемента
    stateCoordinatesNames = ["nuMat", "nuMatDeg"]  # Имена координат состояния
    processCoordinatesNames = ["dnuMatp", "dnuMatn"]  # Имена координат процессов
    energyPowersNames = ["EnPowDegMat", "EnPowMat", "EnPowOkr"]  # Имена энергетических степеней свободы
    reducedTemperaturesEnergyPowersNames = ["TDegMat", "TMat"]  # Имена приведенных температур энергетических степеней свободы
    energyPowersBetNames = []  # Имена взаимодействий между энергетическими степенями свободы
    heatTransfersNames = ["QDegMatMat", "QMatExp"]  # Имена потоков переноса теплоты
    heatTransfersOutputEnergyPowersNames = ["EnPowDegMat", "EnPowMat"]  # Имена энергетических степеней свободы, с которых уходит теплота
    heatTransfersInputEnergyPowersNames = ["EnPowMat", "EnPowOkr"]  # Имена энергетических степеней свободы, на которые приходит теплота
    stateCoordinatesStreamsNames = ["nuMat"]  # Имена координат состояния, изменяемых в результате внешних потоков
    heatEnergyPowersStreamsNames = []  # Имена потоков теплоты на энергетические степени свободы
    stateFunction = MaterialDegradationStateFunction  # Функция состояния
    stateCoordinatesVarBalanceNames = []  # Имена переменных коэффициентов матрицы баланса по координатам состояния
    processCoordinatesVarBalanceNames = []  # Имена переменных коэффициентов матрицы баланса по координатам процессов
    energyPowersVarTemperatureNames = ["EnPowDegMat", "EnPowMat", "EnPowOkr"]  # Имена переменных температур энергетических степеней свободы
    stateCoordinatesVarPotentialsInterNames = ["nuMat", "nuMatDeg"]  # Имена переменных потенциалов взаимодействия по координатам состояния
    energyPowersVarPotentialsInterNames = ["EnPowDegMat", "EnPowDegMat"]  # Имена переменных потенциалов взаимодействия по энергетическим степеням свободы
    stateCoordinatesVarPotentialsInterBetNames = []  # Имена переменных потенциалов взаимодействия для взаимодействий между энергетическими степенями свободы по координатам состояния
    energyPowersVarPotentialsInterBetNames = []  # Имена переменных потенциалов взаимодействия для взаимодействий между энергетическими степенями свободы по энергетическим степеням свободы
    energyPowersVarBetaNames = []  # Имена переменных долей распределения некомпенсированной теплоты энергетических степеней свободы
    processCoordinatesVarBetaNames = []  # Имена переменных долей распределения некомпенсированной теплоты координат процессов
    reducedTemperaturesEnergyPowersVarInvHeatCapacityNames = ["TDegMat", "TMat"]  # Имена переменных коэффициентов обратных теплоемкостей по отношению к приведенным температурам
    energyPowersVarInvHeatCapacityNames = ["EnPowDegMat", "EnPowMat"]  # Имена переменных коэффициентов обратных теплоемкостей по отношению к энергетическим степеням свободы
    reducedTemperaturesEnergyPowersVarHeatEffectNames = ["TDegMat", "TDegMat"]  # Имена переменных коэффициентов обратных теплоемкостей по отношению к приведенным температурам
    stateCoordinatesVarHeatEffectNames = ["nuMat", "nuMatDeg"]  # Имена переменных коэффициентов обратных теплоемкостей по отношению к координатам состояния
    varKineticPCPCNames = ["dnuMatp", "dnuMatn"]  # Имена сопряженностей между собой координат процессов
    varKineticPCPCAffNames = ["dnuMatp", "dnuMatn"]  # Имена сопряженностей между собой термодинамических сил
    varKineticPCHeatNames = []  # Имена сопряженностей координат процессов с теплопереносами
    varKineticPCHeatAffNames = []  # Имена сопряженностей термодинамических сил с теплопереносами
    varKineticHeatPCNames = []  # Имена сопряженностей теплопереносов с координатами процессов
    varKineticHeatPCAffNames = []  # Имена сопряженностей теплопереносов с термодинамическими силами
    varKineticHeatHeatNames = ["QDegMatMat", "QMatExp"]  # Имена сопряженностей между собой перенесенных теплот
    varKineticHeatHeatAffNames = ["QDegMatMat", "QMatExp"]  # Имена сопряженностей между собой термодинамических сил по переносу теплот
    stateCoordinatesVarStreamsNames = ["nuMat"]  # Имена переменных внешних потоков
    heatEnergyPowersVarStreamsNames = []  # Имена переменных внешних потоков теплоты

    # Литий-ионный аккумулятор
    MatDeg = NonEqSystemQ(stateCoordinatesNames,  # Имена координат состояния
                          processCoordinatesNames,  # Имена координат процессов
                          energyPowersNames,  # Имена энергетических степеней свободы
                          reducedTemperaturesEnergyPowersNames,  # Имена приведенных температур энергетических степеней свободы
                          energyPowersBetNames,  # Имена взаимодействий между энергетическими степенями свободы
                          heatTransfersNames,  # Имена потоков переноса теплоты
                          heatTransfersOutputEnergyPowersNames,  # Имена энергетических степеней свободы, с которых уходит теплота
                          heatTransfersInputEnergyPowersNames,  # Имена энергетических степеней свободы, на которые приходит теплота

                          stateCoordinatesStreamsNames,  # Имена координат состояния, изменяемых в результате внешних потоков
                          heatEnergyPowersStreamsNames,  # Имена потоков теплоты на энергетические степени свободы

                          stateFunction,  # Функция состояния

                          stateCoordinatesVarBalanceNames,  # Имена переменных коэффициентов матрицы баланса по координатам состояния
                          processCoordinatesVarBalanceNames,  # Имена переменных коэффициентов матрицы баланса по координатам процессов
                          energyPowersVarTemperatureNames,  # Имена переменных температур энергетических степеней свободы
                          stateCoordinatesVarPotentialsInterNames,  # Имена переменных потенциалов взаимодействия по координатам состояния
                          energyPowersVarPotentialsInterNames,  # Имена переменных потенциалов взаимодействия по энергетическим степеням свободы
                          stateCoordinatesVarPotentialsInterBetNames,  # Имена переменных потенциалов взаимодействия для взаимодействий между энергетическими степенями свободы по координатам состояния
                          energyPowersVarPotentialsInterBetNames,  # Имена переменных потенциалов взаимодействия для взаимодействий между энергетическими степенями свободы по энергетическим степеням свободы
                          energyPowersVarBetaNames,  # Имена переменных долей распределения некомпенсированной теплоты энергетических степеней свободы
                          processCoordinatesVarBetaNames,  # Имена переменных долей распределения некомпенсированной теплоты координат процессов
                          reducedTemperaturesEnergyPowersVarInvHeatCapacityNames,  # Имена переменных коэффициентов обратных теплоемкостей по отношению к приведенным температурам
                          energyPowersVarInvHeatCapacityNames,  # Имена переменных коэффициентов обратных теплоемкостей по отношению к энергетическим степеням свободы
                          reducedTemperaturesEnergyPowersVarHeatEffectNames,  # Имена переменных коэффициентов обратных теплоемкостей по отношению к приведенным температурам
                          stateCoordinatesVarHeatEffectNames,  # Имена переменных коэффициентов обратных теплоемкостей по отношению к координатам состояния

                          varKineticPCPCNames,  # Имена сопряженностей между собой координат процессов
                          varKineticPCPCAffNames,  # Имена сопряженностей между собой термодинамических сил
                          varKineticPCHeatNames,  # Имена сопряженностей координат процессов с теплопереносами
                          varKineticPCHeatAffNames,  # Имена сопряженностей термодинамических сил с теплопереносами
                          varKineticHeatPCNames,  # Имена сопряженностей теплопереносов с координатами процессов
                          varKineticHeatPCAffNames,  # Имена сопряженностей теплопереносов с термодинамическими силами
                          varKineticHeatHeatNames,  # Имена сопряженностей между собой перенесенных теплот
                          varKineticHeatHeatAffNames,  # Имена сопряженностей между собой термодинамических сил по переносу теплот

                          stateCoordinatesVarStreamsNames,  # Имена переменных внешних потоков
                          heatEnergyPowersVarStreamsNames  # Имена переменных внешних потоков теплоты
                          )

    # Задаем связь между коордиинатами состояния и процессами
    MatDeg.SetBalanceStateCoordinatesConstElement("nuMat", "dnuMatp", 1)
    MatDeg.SetBalanceStateCoordinatesConstElement("nuMatDeg", "dnuMatn", 1)

    # Задаем доли распределения некомпенсированной теплоты
    MatDeg.SetBetaConstElement("EnPowDegMat", "dnuMatp", 1.0)
    MatDeg.SetBetaConstElement("EnPowDegMat", "dnuMatn", 1.0)

    # Задаем класс динамики системы
    integDynamic = standartIntegrateDyn(method=integrateMethod)
    return NonEqSystemQDyn(MatDeg,  # деградация материала
                           fU,  # Функция условий протекания процессов
                           MaterialDegradationCharacteristicsFunction,  # Функция внешних параметров
                           integDynamic  # Метод интегрирования дифференциальных уравнений
                           )
