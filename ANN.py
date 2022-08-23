# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 14:48:16 2021

@author: wi9632
"""
import numpy as np
import SetUpScenarios 
import Run_Simulations
import pandas as pd




# Generates the actions for single time slots and for the single building optimization scenario by using an ANN.
# Input:
# Output: schedule
def generateActionsForSingleTimeslotWithANN_SingleBuildingOptScenario (indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentDay ,pathForCreatingTheResultData_ANN, objective, usedDaySelectionMethod, dataScaler_InputFeatures, dataScaler_OutputLabels, trainedModel):
    import ICSimulation
    from joblib import dump, load


    #Reading of the price data
    df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_Days/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_Day' +  str(currentDay) + '.csv', sep =";")
    df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
    df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
    arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
    df_priceData['Timeslot'] = arrayTimeSlots
    df_priceData = df_priceData.set_index('Timeslot')

    #Reading outside temperature data
    df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_Days/Outside_Temperature_1Minute_Day' +  str(currentDay) + '.csv', sep =";")
    df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
    df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
    df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
    df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

    cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])

    #Create the price data
    df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
    df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
    df_priceData['Timeslot'] = arrayTimeSlots
    df_priceData = df_priceData.set_index('Timeslot')




    #Reading of the building data
    list_df_buildingData_BT1_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT1_mHP_EV_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT1]
    list_df_buildingData_BT2_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT2_mHP_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT2]
    list_df_buildingData_BT3_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT3_EV_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT3]
    list_df_buildingData_BT4_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT4_mHP_MFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT4]
    list_df_buildingData_BT5_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT5_BAT_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT5]



    list_df_buildingData_BT1 = list_df_buildingData_BT1_original.copy()
    list_df_buildingData_BT2 = list_df_buildingData_BT2_original.copy()
    list_df_buildingData_BT3 = list_df_buildingData_BT3_original.copy()
    list_df_buildingData_BT4 = list_df_buildingData_BT4_original.copy()
    list_df_buildingData_BT5 = list_df_buildingData_BT5_original.copy()



    #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
    for i in range (0, len(list_df_buildingData_BT1_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT1_original[i]:
            list_df_buildingData_BT1_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT2_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT2_original[i]:
            list_df_buildingData_BT2_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT3_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT3_original[i]:
            list_df_buildingData_BT3_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT4_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT4_original[i]:
            list_df_buildingData_BT4_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT5_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT5_original[i]:
            list_df_buildingData_BT5_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)



    #Adjust dataframes to the current time resolution and set new index "Timeslot"

    for i in range (0, len(list_df_buildingData_BT1_original)):
        list_df_buildingData_BT1_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT1_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT1 [i] = list_df_buildingData_BT1_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
        for j in range (0, len(list_df_buildingData_BT1[i]['Availability of the EV'])):
            if list_df_buildingData_BT1 [i]['Availability of the EV'] [j] > 0.1:
                list_df_buildingData_BT1 [i]['Availability of the EV'] [j] = 1.0
            if list_df_buildingData_BT1 [i]['Availability of the EV'] [j] < 0.1 and list_df_buildingData_BT1 [i]['Availability of the EV'] [j] >0.01:
                list_df_buildingData_BT1 [i]['Availability of the EV'] [j] = 0

        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT1 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT1 [i] = list_df_buildingData_BT1 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT2_original)):
        list_df_buildingData_BT2_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT2_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT2 [i] = list_df_buildingData_BT2_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT2 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT2 [i] = list_df_buildingData_BT2 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT3_original)):
        list_df_buildingData_BT3_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT3_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT3 [i] = list_df_buildingData_BT3_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
        for j in range (0, len(list_df_buildingData_BT3[i]['Availability of the EV'])):
            if list_df_buildingData_BT3 [i]['Availability of the EV'] [j] > 0.1:
                list_df_buildingData_BT3 [i]['Availability of the EV'] [j] = 1.0
            if list_df_buildingData_BT3 [i]['Availability of the EV'] [j] < 0.1 and list_df_buildingData_BT3 [i]['Availability of the EV'] [j] >0.01:
                list_df_buildingData_BT3 [i]['Availability of the EV'] [j] = 0

        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT3 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT3 [i] = list_df_buildingData_BT3 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT4_original)):
        list_df_buildingData_BT4_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT4_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT4 [i] = list_df_buildingData_BT4_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()


        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT4 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT4 [i] = list_df_buildingData_BT4 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT5_original)):
        list_df_buildingData_BT5_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT5_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT5 [i] = list_df_buildingData_BT5_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()


        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT5 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT5 [i] = list_df_buildingData_BT5 [i].set_index('Timeslot')



    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT1):
        decimalsForRounding = 2
        list_df_buildingData_BT1 [index]['Electricity [W]'] = list_df_buildingData_BT1 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT1 [index]['Space Heating [W]'] = list_df_buildingData_BT1 [index]['Space Heating [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT1 [index]['DHW [W]'] = list_df_buildingData_BT1 [index]['DHW [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT1 [index]['PV [nominal]'] = list_df_buildingData_BT1 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT2):
        decimalsForRounding = 2
        list_df_buildingData_BT2 [index]['Electricity [W]'] = list_df_buildingData_BT2 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT2 [index]['Space Heating [W]'] = list_df_buildingData_BT2 [index]['Space Heating [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT2 [index]['DHW [W]'] = list_df_buildingData_BT2 [index]['DHW [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT2 [index]['PV [nominal]'] = list_df_buildingData_BT2 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT3):
        decimalsForRounding = 2
        list_df_buildingData_BT3 [index]['Electricity [W]'] = list_df_buildingData_BT3 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT3 [index]['PV [nominal]'] = list_df_buildingData_BT3 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT4):
        decimalsForRounding = 2
        list_df_buildingData_BT4 [index]['Electricity [W]'] = list_df_buildingData_BT4 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT4 [index]['Space Heating [W]'] = list_df_buildingData_BT4 [index]['Space Heating [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT4 [index]['PV [nominal]'] = list_df_buildingData_BT4 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT5):
        decimalsForRounding = 2
        list_df_buildingData_BT5 [index]['Electricity [W]'] = list_df_buildingData_BT5 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT5 [index]['PV [nominal]'] = list_df_buildingData_BT5 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))




    # Create wind power profile for BT1
    list_windProfileNominal_BT1 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,index_BT1) for index_BT1 in range(0, SetUpScenarios.numberOfBuildings_BT1)]
    list_df_windPowerAssignedNominalPerBuilding_BT1 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT1 [i].index, 'Wind [nominal]':list_windProfileNominal_BT1[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT1)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT1)):
        del list_df_windPowerAssignedNominalPerBuilding_BT1[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT1[i].index +=1

    # Create wind power profile for BT2
    list_windProfileNominal_BT2 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + index_BT2) for index_BT2 in range(0, SetUpScenarios.numberOfBuildings_BT2)]
    list_df_windPowerAssignedNominalPerBuilding_BT2 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT2 [i].index, 'Wind [nominal]':list_windProfileNominal_BT2[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT2)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT2)):
        del list_df_windPowerAssignedNominalPerBuilding_BT2[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT2[i].index +=1


    # Create wind power profile for BT3
    list_windProfileNominal_BT3 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3) for index_BT3 in range(0, SetUpScenarios.numberOfBuildings_BT3)]
    list_df_windPowerAssignedNominalPerBuilding_BT3 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT3 [i].index, 'Wind [nominal]':list_windProfileNominal_BT3[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT3)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT3)):
        del list_df_windPowerAssignedNominalPerBuilding_BT3[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT3[i].index +=1


    # Create wind power profile for BT4
    list_windProfileNominal_BT4 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4) for index_BT4 in range(0, SetUpScenarios.numberOfBuildings_BT4)]
    list_df_windPowerAssignedNominalPerBuilding_BT4 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT4 [i].index, 'Wind [nominal]':list_windProfileNominal_BT4[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT4)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT4)):
        del list_df_windPowerAssignedNominalPerBuilding_BT4[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT4[i].index +=1


    # Create wind power profile for BT5
    list_windProfileNominal_BT5 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + SetUpScenarios.numberOfBuildings_BT4  + index_BT5) for index_BT5 in range(0, SetUpScenarios.numberOfBuildings_BT5)]
    list_df_windPowerAssignedNominalPerBuilding_BT5 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT5 [i].index, 'Wind [nominal]':list_windProfileNominal_BT5[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT5)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT5)):
        del list_df_windPowerAssignedNominalPerBuilding_BT5[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT5[i].index +=1


    #Create availability array for the EV of BT1
    availabilityOfTheEVCombined = np.zeros((SetUpScenarios.numberOfBuildings_WithEV, SetUpScenarios.numberOfTimeSlotsPerDay))
    for index_BT1 in range (0, SetUpScenarios.numberOfBuildings_BT1):
        for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerDay):
            availabilityOfTheEVCombined [index_BT1,index_timeslot_for_Availability] = list_df_buildingData_BT1 [index_BT1]['Availability of the EV'] [index_timeslot_for_Availability +1]


    list_energyConsumptionOfEVs_Joule_BT1 = np.zeros((SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerDay))


    for indexEV in range (0, SetUpScenarios.numberOfBuildings_BT1):
        list_energyConsumptionOfEVs_Joule_BT1[indexEV] = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEVCombined [indexEV],indexEV)

    list_df_energyConsumptionEV_Joule_BT1 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT1 [i].index, 'Energy':list_energyConsumptionOfEVs_Joule_BT1 [i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT1)]


    for i in range (0, len(list_energyConsumptionOfEVs_Joule_BT1)):
        del list_df_energyConsumptionEV_Joule_BT1 [i]['Timeslot']
        list_df_energyConsumptionEV_Joule_BT1[i].index +=1


    #Create availability array for the EV of BT3
    availabilityOfTheEVCombined = np.zeros((SetUpScenarios.numberOfBuildings_WithEV, SetUpScenarios.numberOfTimeSlotsPerDay))
    for index_BT3 in range (0, SetUpScenarios.numberOfBuildings_BT3):
        for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerDay):
            availabilityOfTheEVCombined [SetUpScenarios.numberOfBuildings_BT1 + index_BT3,index_timeslot_for_Availability] = list_df_buildingData_BT3 [index_BT3]['Availability of the EV'] [index_timeslot_for_Availability +1]


    list_energyConsumptionOfEVs_Joule_BT3 = np.zeros((SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerDay))


    for indexEV in range (0, SetUpScenarios.numberOfBuildings_BT3):
        list_energyConsumptionOfEVs_Joule_BT3[indexEV] = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEVCombined [SetUpScenarios.numberOfBuildings_BT1 + indexEV],SetUpScenarios.numberOfBuildings_BT1 + indexEV)

    list_df_energyConsumptionEV_Joule_BT3 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT3 [i].index, 'Energy':list_energyConsumptionOfEVs_Joule_BT3 [i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT3)]


    for i in range (0, len(list_energyConsumptionOfEVs_Joule_BT3)):
        del list_df_energyConsumptionEV_Joule_BT3 [i]['Timeslot']
        list_df_energyConsumptionEV_Joule_BT3[i].index +=1


    #Define arrays for storing the output values
    outputVector_heatGenerationCoefficientSpaceHeating = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_heatGenerationCoefficientDHW = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_chargingPowerEV = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_temperatureBufferStorage = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_volumeDHWTank  = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_SOC  = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)

    outputVector_chargingPowerBAT = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_disChargingPowerBAT = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_SOC_BAT  = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)


    if SetUpScenarios.numberOfBuildings_BT1 ==1:

            #Set up variables
            action_heatCoefficientSpaceHeating = 0
            action_heatCoefficientDHW = 0
            action_chargingPowerEV = 0

            help_actionPreviousTimeSlot_heatCoefficientSpaceHeating  = 0
            help_actionPreviousTimeSlot_heatCoefficientDHW  = 0

            help_statePreviousTimeSlot_temperatureBufferStorage = SetUpScenarios.initialBufferStorageTemperature
            help_statePreviousTimeSlot_usableVolumeDHWTank = SetUpScenarios.initialUsableVolumeDHWTank
            help_statePreviousTimeSlot_SOCOfTheEV = SetUpScenarios.initialSOC_EV

            help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual = 0
            help_countNumberOfStartHeatPump_HeatingDHW_Indiviual = 0
            help_countNumberOfStartHeatPump_Heating_Combined = 0
            helpCounterNumberOfRunningSlots_SpaceHeating = 0
            helpCounterNumberOfRunningSlots_DHW = 0
            helpCounterNumberOfRunningSlots_Combined = 0
            helpCounterNumberOfStandBySlots_SpaceHeating = 0
            helpCounterNumberOfStandBySlots_DHW = 0
            helpCounterNumberOfStandBySlots_Combined = 0
            helpCurrentPeakLoad = 0
            helpStartedHeatingHeatPump = False
            helpStoppedHeatingHeatPump = False
            startedHeatingSpaceHeatingCorrection_end = False
            startedHeatingDHWCorrection_end = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = False
            heatingStartedPhysicalLimit_BufferStorage = False
            heatingStartedPhysicalLimit_DHWTank = False
            heatPumpIsRunning = 0

            numberOfHeatPumpStartsReachedSoftLimit = False
            numberOfHeatPumpStartsReachedHardLimit = False
            state_indexCurrentTimeslot = 0
            state_outsideTemperature = 0
            state_PVGeneration = 0
            state_heatDemand = 0
            state_DHWDemand = 0
            state_electricityDemand = 0
            state_availabilityOfTheEV = 0
            state_priceForElectricity_CentsPerkWh = 0
            state_energyDemandEV = 0
            helpPVGenerationPreviousTimeSlot = 0
            electricalLoadPreviousTimeSlot = 0
            helpHypotheticalSOCDropNoCharging_PreviousTimeSlot  = 0

            correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC =0
            correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC =0
            correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC =0
            correctingStats_BT1_heatGenerationCoefficientDHW_sumOfDeviations_STSIC =0
            correctingStats_BT1_chargingPowerEV_numberOfTimeSlots_STSIC =0
            correctingStats_BT1_chargingPowerEV_sumOfDeviations_STSIC =0

            help_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
            help_bothStorageHeatedUp_lastTimeDHWOverruled = False


            #Calculate the COPs for the heat pump
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])
            df_copHeatPump =  pd.DataFrame({'Timeslot': list_df_buildingData_BT1 [0].index, 'COP_SpaceHeating':cop_heatPump_SpaceHeating, 'COP_DHW':cop_heatPump_DHW})



            for state_indexCurrentTimeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):


                # Assign values to the non-adjustable state variables (parameters)

                state_PVGeneration = list_df_buildingData_BT1 [indexOfBuildingsOverall_BT1 [0] - 1] ['PV [nominal]'] [ state_indexCurrentTimeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT1 [0] - 1)
                state_heatDemand  = list_df_buildingData_BT1 [indexOfBuildingsOverall_BT1 [0] - 1] ['Space Heating [W]'] [ state_indexCurrentTimeslot + 1 ]
                state_DHWDemand  = list_df_buildingData_BT1 [indexOfBuildingsOverall_BT1 [0] - 1] ['DHW [W]'] [ state_indexCurrentTimeslot  + 1 ]
                state_electricityDemand  = list_df_buildingData_BT1 [indexOfBuildingsOverall_BT1 [0] - 1] ['Electricity [W]'] [ state_indexCurrentTimeslot + 1 ]
                state_availabilityOfTheEV = list_df_buildingData_BT1 [indexOfBuildingsOverall_BT1 [0] - 1] ['Availability of the EV'] [ state_indexCurrentTimeslot + 1 ]

                state_outsideTemperature = df_outsideTemperatureData ['Temperature [C]'] [ state_indexCurrentTimeslot + 1 ]
                state_priceForElectricity_CentsPerkWh = df_priceData ['Price [Cent/kWh]'] [ state_indexCurrentTimeslot + 1 ]
                state_energyDemandEV =  list_df_energyConsumptionEV_Joule_BT1 [indexOfBuildingsOverall_BT1 [0] - 1] ['Energy'] [ state_indexCurrentTimeslot + 1]


                #Load trained ML method
                if usedDaySelectionMethod == 'Random':

                    # Currently used features in method trainSupvervisedML_SinlgeTimeSlots: MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
                    # Feature names translation from method trainSupvervisedML_SinlgeTimeSlots: 'timeslot': state_indexCurrentTimeslot, 'temperatureBufferStorage': help_statePreviousTimeSlot_usableVolumeDHWTank, 'usableVolumeDHWTank': help_statePreviousTimeSlot_usableVolumeDHWTank, 'simulationResult_SOCofEV': help_statePreviousTimeSlot_SOCOfTheEV, 'simulationResult_RESGeneration': state_PVGeneration, 'Space Heating [W]': state_heatDemand, 'DHW [W]':state_DHWDemand, 'Electricity [W]': state_electricityDemand, 'Availability of the EV': state_availabilityOfTheEV, 'Outside Temperature [C]': state_outsideTemperature, 'Price [Cent/kWh]': state_priceForElectricity_CentsPerkWh, 'numberOfStarts_HP':help_countNumberOfStartHeatPump_Heating_Combined, 'HP_isRunning' = heatPumpIsRunning

                    #Create vector with input features and scale it
                    if objective == 'Min_Costs':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, help_statePreviousTimeSlot_SOCOfTheEV, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_availabilityOfTheEV, state_outsideTemperature, state_priceForElectricity_CentsPerkWh, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))


                    if objective == 'Min_SurplusEnergy':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, help_statePreviousTimeSlot_SOCOfTheEV, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_availabilityOfTheEV, state_outsideTemperature,  help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))


                    if objective == 'Min_Peak':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, help_statePreviousTimeSlot_SOCOfTheEV, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_availabilityOfTheEV, state_outsideTemperature,  help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))




                    vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)
                    vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)



                    action_heatCoefficientSpaceHeating = vector_output_labels[0][0]
                    action_heatCoefficientDHW = vector_output_labels[0][1]
                    action_chargingPowerEV = vector_output_labels[0][2]



                overuleActions = True

                #Store current actions before passing through the single-time-slot internal controller (STSIC) for correction statistics
                action_heatCoefficientSpaceHeating_NotOverruled = action_heatCoefficientSpaceHeating
                action_heatCoefficientDHW_NotOverruled = action_heatCoefficientDHW
                action_chargingPowerEV_NotOverruled = action_chargingPowerEV


                # Pass values to the internal controller
                action_heatCoefficientSpaceHeating, action_heatCoefficientDHW, action_chargingPowerEV, state_temperatureBufferStorage, state_usableVolumeDHWTank, state_SOCOfTheEV, help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual, help_countNumberOfStartHeatPump_HeatingDHW_Indiviual, help_countNumberOfStartHeatPump_Heating_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW , helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit,helpHypotheticalSOCDropNoCharging, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled = ICSimulation.simulateTimeSlot_WithAddtionalController_BT1 (overuleActions, action_heatCoefficientSpaceHeating, action_heatCoefficientDHW, action_chargingPowerEV, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, help_statePreviousTimeSlot_SOCOfTheEV, help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual, help_countNumberOfStartHeatPump_HeatingDHW_Indiviual, help_countNumberOfStartHeatPump_Heating_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW ,helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, helpStoppedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, state_indexCurrentTimeslot, state_outsideTemperature, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_availabilityOfTheEV, state_priceForElectricity_CentsPerkWh, state_energyDemandEV,  df_copHeatPump ["COP_SpaceHeating"] [ state_indexCurrentTimeslot ],  df_copHeatPump ["COP_DHW"] [ state_indexCurrentTimeslot ], helpPVGenerationPreviousTimeSlot, electricalLoadPreviousTimeSlot, helpHypotheticalSOCDropNoCharging_PreviousTimeSlot, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled)


                #Calculate the correction statistics of the single-time-slot internal controller
                if action_heatCoefficientSpaceHeating != action_heatCoefficientSpaceHeating_NotOverruled:
                    correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC = correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC + abs(action_heatCoefficientSpaceHeating - action_heatCoefficientSpaceHeating_NotOverruled)
                if action_heatCoefficientDHW != action_heatCoefficientDHW_NotOverruled:
                    correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT1_heatGenerationCoefficientDHW_sumOfDeviations_STSIC = correctingStats_BT1_heatGenerationCoefficientDHW_sumOfDeviations_STSIC + abs(action_heatCoefficientDHW - action_heatCoefficientDHW_NotOverruled)
                if action_chargingPowerEV != action_chargingPowerEV_NotOverruled:
                    correctingStats_BT1_chargingPowerEV_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT1_chargingPowerEV_sumOfDeviations_STSIC = correctingStats_BT1_chargingPowerEV_sumOfDeviations_STSIC + abs(action_chargingPowerEV - action_chargingPowerEV_NotOverruled)


               #Assign values to the auxillary variabless

                if (help_actionPreviousTimeSlot_heatCoefficientSpaceHeating ==0 and help_actionPreviousTimeSlot_heatCoefficientDHW ==0) and (action_heatCoefficientSpaceHeating > 0.01 or action_heatCoefficientDHW > 0.01):
                    helpStartedHeatingHeatPump = True
                    helpStoppedHeatingHeatPump = False
                    help_countNumberOfStartHeatPump_Heating_Combined +=1
                if (help_actionPreviousTimeSlot_heatCoefficientSpaceHeating > 0.01 or help_actionPreviousTimeSlot_heatCoefficientDHW  > 0.01) and (action_heatCoefficientSpaceHeating ==0 and action_heatCoefficientDHW==0):
                    helpStartedHeatingHeatPump = False
                    helpStoppedHeatingHeatPump = True
                    if lastHeatingAfterHeatPumpStartsReachedHardLimitStarted ==True:
                        lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = True


                help_statePreviousTimeSlot_temperatureBufferStorage = state_temperatureBufferStorage
                help_statePreviousTimeSlot_usableVolumeDHWTank= state_usableVolumeDHWTank
                help_statePreviousTimeSlot_SOCOfTheEV = state_SOCOfTheEV
                help_actionPreviousTimeSlot_heatCoefficientSpaceHeating= action_heatCoefficientSpaceHeating
                help_actionPreviousTimeSlot_heatCoefficientDHW= action_heatCoefficientDHW
                helpPVGenerationPreviousTimeSlot = state_PVGeneration
                electricalLoadPreviousTimeSlot =  state_electricityDemand + (action_heatCoefficientSpaceHeating + action_heatCoefficientDHW)  *  SetUpScenarios.electricalPower_HP + action_chargingPowerEV


                if action_heatCoefficientSpaceHeating > 0.01:
                     helpCounterNumberOfRunningSlots_SpaceHeating  += 1
                     helpCounterNumberOfStandBySlots_SpaceHeating =0
                else :
                     helpCounterNumberOfRunningSlots_SpaceHeating =0
                     helpCounterNumberOfStandBySlots_SpaceHeating +=1
                if action_heatCoefficientDHW > 0.01:
                     helpCounterNumberOfRunningSlots_DHW += 1
                     helpCounterNumberOfStandBySlots_DHW =0
                else:
                     helpCounterNumberOfRunningSlots_DHW = 0
                     helpCounterNumberOfStandBySlots_DHW +=1
                if action_heatCoefficientSpaceHeating > 0.01 or action_heatCoefficientDHW > 0.01:
                    helpCounterNumberOfRunningSlots_Combined += 1
                    helpCounterNumberOfStandBySlots_Combined =0
                else :
                    helpCounterNumberOfRunningSlots_Combined =0
                    helpCounterNumberOfStandBySlots_Combined += 1


                if helpCounterNumberOfRunningSlots_Combined > 0:
                    heatPumpIsRunning = 1
                else:
                    heatPumpIsRunning = 0


                outputVector_heatGenerationCoefficientSpaceHeating [state_indexCurrentTimeslot] = action_heatCoefficientSpaceHeating
                outputVector_heatGenerationCoefficientDHW [state_indexCurrentTimeslot] = action_heatCoefficientDHW
                outputVector_chargingPowerEV  [state_indexCurrentTimeslot] = action_chargingPowerEV

                outputVector_temperatureBufferStorage  [state_indexCurrentTimeslot] =state_temperatureBufferStorage
                outputVector_volumeDHWTank [state_indexCurrentTimeslot] = state_usableVolumeDHWTank
                outputVector_SOC [state_indexCurrentTimeslot] = state_SOCOfTheEV


            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT1 = pd.DataFrame({'outputVector_heatGenerationCoefficientSpaceHeating': outputVector_heatGenerationCoefficientSpaceHeating[:],'outputVector_heatGenerationCoefficientDHW': outputVector_heatGenerationCoefficientDHW[:],'outputVector_chargingPowerEV': outputVector_chargingPowerEV[:], 'outputVector_temperatureBufferStorage': outputVector_temperatureBufferStorage[:], 'usableVolumeDHWTank': outputVector_volumeDHWTank[ :], 'outputVector_SOC': outputVector_SOC[:]})

            df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientSpaceHeating'].round(3)
            df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientDHW'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientDHW'].round(3)
            df_resultingProfiles_Preliminary_BT1 ['outputVector_chargingPowerEV'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_chargingPowerEV'].round(3)
            df_resultingProfiles_Preliminary_BT1 ['outputVector_temperatureBufferStorage'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_temperatureBufferStorage'].round(2)
            df_resultingProfiles_Preliminary_BT1 ['usableVolumeDHWTank'] = df_resultingProfiles_Preliminary_BT1 ['usableVolumeDHWTank'].round(2)
            df_resultingProfiles_Preliminary_BT1 ['outputVector_SOC'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_SOC'].round(2)
            df_resultingProfiles_Preliminary_BT1.index += 1
            df_resultingProfiles_Preliminary_BT1.index.name = 'timeslot'
            df_resultingProfiles_Preliminary_BT1.insert(0, 'time of day', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_Preliminary_BT1), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))

            df_resultingProfiles_Preliminary_BT1.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT1_HH" + str(indexOfBuildingsOverall_BT1 [0] ) + ".csv" , index=True,  sep =";")

            filename = pathForCreatingTheResultData_ANN + "/Correction Stats Preliminary.txt"
            with open(filename, 'w') as f:
                print("Correction results for the single-time-slot internal controller (STSIC)", file = f)
                print("", file = f)
                print("correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC: ", correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC: ", round(correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC, 2), file = f)
                print("correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC: ", correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT1_heatGenerationCoefficientDHW_sumOfDeviations_STSIC: ", round(correctingStats_BT1_heatGenerationCoefficientDHW_sumOfDeviations_STSIC, 2), file = f)
                print("correctingStats_BT1_chargingPowerEV_numberOfTimeSlots_STSIC: ", correctingStats_BT1_chargingPowerEV_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT1_chargingPowerEV_sumOfDeviations_STSIC: ", round(correctingStats_BT1_chargingPowerEV_sumOfDeviations_STSIC, 2), file = f)


            return outputVector_heatGenerationCoefficientSpaceHeating, outputVector_heatGenerationCoefficientDHW, outputVector_chargingPowerEV, outputVector_temperatureBufferStorage, outputVector_volumeDHWTank, outputVector_SOC



    #############################################################################################################################



    if SetUpScenarios.numberOfBuildings_BT2 ==1:
            #Set up variables
            action_heatCoefficientSpaceHeating = 0
            action_heatCoefficientDHW = 0

            help_actionPreviousTimeSlot_heatCoefficientSpaceHeating  = 0
            help_actionPreviousTimeSlot_heatCoefficientDHW  = 0

            help_statePreviousTimeSlot_temperatureBufferStorage = SetUpScenarios.initialBufferStorageTemperature
            help_statePreviousTimeSlot_usableVolumeDHWTank = SetUpScenarios.initialUsableVolumeDHWTank

            help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual = 0
            help_countNumberOfStartHeatPump_HeatingDHW_Indiviual = 0
            help_countNumberOfStartHeatPump_Heating_Combined = 0
            helpCounterNumberOfRunningSlots_SpaceHeating = 0
            helpCounterNumberOfRunningSlots_DHW = 0
            helpCounterNumberOfRunningSlots_Combined = 0
            helpCounterNumberOfStandBySlots_SpaceHeating = 0
            helpCounterNumberOfStandBySlots_DHW = 0
            helpCounterNumberOfStandBySlots_Combined = 0
            helpCurrentPeakLoad = 0
            helpStartedHeatingHeatPump = False
            helpStoppedHeatingHeatPump = False
            startedHeatingSpaceHeatingCorrection_end = False
            startedHeatingDHWCorrection_end = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = False
            heatingStartedPhysicalLimit_BufferStorage = False
            heatingStartedPhysicalLimit_DHWTank = False
            heatPumpIsRunning = 0

            numberOfHeatPumpStartsReachedSoftLimit = False
            numberOfHeatPumpStartsReachedHardLimit = False
            state_indexCurrentTimeslot = 0
            state_outsideTemperature = 0
            state_PVGeneration = 0
            state_heatDemand = 0
            state_DHWDemand = 0
            state_electricityDemand = 0
            state_priceForElectricity_CentsPerkWh = 0
            helpPVGenerationPreviousTimeSlot = 0
            electricalLoadPreviousTimeSlot = 0

            correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC =0
            correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC =0
            correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC =0
            correctingStats_BT2_heatGenerationCoefficientDHW_sumOfDeviations_STSIC =0

            help_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
            help_bothStorageHeatedUp_lastTimeDHWOverruled= False

            #Calculate the COPs for the heat pump
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])
            df_copHeatPump =  pd.DataFrame({'Timeslot': list_df_buildingData_BT2 [0].index, 'COP_SpaceHeating':cop_heatPump_SpaceHeating, 'COP_DHW':cop_heatPump_DHW})



            #Loop for generating the actions and the "inline" simulation (meaning the simulation necessary for generating the actions)
            for state_indexCurrentTimeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):


                #Load trained ML method
                if usedDaySelectionMethod == 'Random':

                    # Currently used features in method trainSupvervisedML_SinlgeTimeSlots:  = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]

                    # Feature names translation from method trainSupvervisedML_SinlgeTimeSlots: 'timeslot': state_indexCurrentTimeslot, 'temperatureBufferStorage': help_statePreviousTimeSlot_usableVolumeDHWTank, 'usableVolumeDHWTank': help_statePreviousTimeSlot_usableVolumeDHWTank, 'simulationResult_SOCofEV': help_statePreviousTimeSlot_SOCOfTheEV, 'simulationResult_RESGeneration': state_PVGeneration, 'Space Heating [W]': state_heatDemand, 'DHW [W]':state_DHWDemand, 'Electricity [W]': state_electricityDemand, 'Availability of the EV': state_availabilityOfTheEV, 'Outside Temperature [C]': state_outsideTemperature, 'Price [Cent/kWh]': state_priceForElectricity_CentsPerkWh, 'numberOfStarts_HP':help_countNumberOfStartHeatPump_Heating_Combined, 'HP_isRunning' = heatPumpIsRunning

                    #MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]


                    #Create vector with input features and scale it
                    if objective == 'Min_Costs':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_outsideTemperature, state_priceForElectricity_CentsPerkWh, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                    if objective == 'Min_SurplusEnergy':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_outsideTemperature, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                    if objective == 'Min_Peak':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_outsideTemperature, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))



                    vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)
                    vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)

                    print(f"vector_output_labels_scaled: {vector_output_labels_scaled}")
                    print(f"vector_output_labels: {vector_output_labels}")

                    #Assign action values to the variables of the simulation
                    action_heatCoefficientSpaceHeating = vector_output_labels[0][0]
                    action_heatCoefficientDHW = vector_output_labels[0][1]




                # Assign values to the non-adjustable state variables (parameters)

                state_PVGeneration = list_df_buildingData_BT2 [indexOfBuildingsOverall_BT2 [0] - 1] ['PV [nominal]'] [ state_indexCurrentTimeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT2 [0] - 1)
                state_heatDemand  = list_df_buildingData_BT2 [indexOfBuildingsOverall_BT2 [0] - 1] ['Space Heating [W]'] [ state_indexCurrentTimeslot + 1 ]
                state_DHWDemand  = list_df_buildingData_BT2 [indexOfBuildingsOverall_BT2 [0] - 1] ['DHW [W]'] [ state_indexCurrentTimeslot  + 1 ]
                state_electricityDemand  = list_df_buildingData_BT2 [indexOfBuildingsOverall_BT2 [0] - 1] ['Electricity [W]'] [ state_indexCurrentTimeslot + 1 ]

                state_outsideTemperature = df_outsideTemperatureData ['Temperature [C]'] [ state_indexCurrentTimeslot + 1 ]
                state_priceForElectricity_CentsPerkWh = df_priceData ['Price [Cent/kWh]'] [ state_indexCurrentTimeslot + 1 ]


                overuleActions = True

                #Store current actions before passing through the single-time-slot internal controller (STSIC) for correction statistics
                action_heatCoefficientSpaceHeating_NotOverruled = action_heatCoefficientSpaceHeating
                action_heatCoefficientDHW_NotOverruled = action_heatCoefficientDHW



                # Pass values to the internal controller


                action_heatCoefficientSpaceHeating, action_heatCoefficientDHW  , state_temperatureBufferStorage, state_usableVolumeDHWTank,  help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual, help_countNumberOfStartHeatPump_HeatingDHW_Indiviual, help_countNumberOfStartHeatPump_Heating_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW , helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit , lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled = ICSimulation.simulateTimeSlot_WithAddtionalController_BT2 (overuleActions, action_heatCoefficientSpaceHeating, action_heatCoefficientDHW, help_statePreviousTimeSlot_temperatureBufferStorage, help_statePreviousTimeSlot_usableVolumeDHWTank, help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual, help_countNumberOfStartHeatPump_HeatingDHW_Indiviual, help_countNumberOfStartHeatPump_Heating_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW ,helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, helpStoppedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, state_indexCurrentTimeslot, state_outsideTemperature, state_PVGeneration, state_heatDemand, state_DHWDemand, state_electricityDemand, state_priceForElectricity_CentsPerkWh ,  df_copHeatPump ["COP_SpaceHeating"] [ state_indexCurrentTimeslot ],  df_copHeatPump ["COP_DHW"] [ state_indexCurrentTimeslot ], helpPVGenerationPreviousTimeSlot, electricalLoadPreviousTimeSlot, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled)



                #Calculate the correction statistics of the single-time-slot internal controller
                if action_heatCoefficientSpaceHeating != action_heatCoefficientSpaceHeating_NotOverruled:
                    correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC = correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC + abs(action_heatCoefficientSpaceHeating - action_heatCoefficientSpaceHeating_NotOverruled)
                if action_heatCoefficientDHW != action_heatCoefficientDHW_NotOverruled:
                    correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT2_heatGenerationCoefficientDHW_sumOfDeviations_STSIC = correctingStats_BT2_heatGenerationCoefficientDHW_sumOfDeviations_STSIC + abs(action_heatCoefficientDHW - action_heatCoefficientDHW_NotOverruled)


               #Assign values to the auxillary variabless

                if (help_actionPreviousTimeSlot_heatCoefficientSpaceHeating ==0 and help_actionPreviousTimeSlot_heatCoefficientDHW ==0) and (action_heatCoefficientSpaceHeating > 0.01 or action_heatCoefficientDHW > 0.01):
                    helpStartedHeatingHeatPump = True
                    helpStoppedHeatingHeatPump = False
                    help_countNumberOfStartHeatPump_Heating_Combined +=1
                if (help_actionPreviousTimeSlot_heatCoefficientSpaceHeating > 0.01 or help_actionPreviousTimeSlot_heatCoefficientDHW  > 0.01) and (action_heatCoefficientSpaceHeating ==0 and action_heatCoefficientDHW==0):
                    helpStartedHeatingHeatPump = False
                    helpStoppedHeatingHeatPump = True
                    if lastHeatingAfterHeatPumpStartsReachedHardLimitStarted ==True:
                        lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = True


                help_statePreviousTimeSlot_temperatureBufferStorage = state_temperatureBufferStorage
                help_statePreviousTimeSlot_usableVolumeDHWTank= state_usableVolumeDHWTank
                help_actionPreviousTimeSlot_heatCoefficientSpaceHeating= action_heatCoefficientSpaceHeating
                help_actionPreviousTimeSlot_heatCoefficientDHW= action_heatCoefficientDHW
                helpPVGenerationPreviousTimeSlot = state_PVGeneration
                electricalLoadPreviousTimeSlot =  state_electricityDemand + (action_heatCoefficientSpaceHeating + action_heatCoefficientDHW)  *  SetUpScenarios.electricalPower_HP


                if action_heatCoefficientSpaceHeating > 0.01:
                     helpCounterNumberOfRunningSlots_SpaceHeating  += 1
                     helpCounterNumberOfStandBySlots_SpaceHeating =0
                else :
                     helpCounterNumberOfRunningSlots_SpaceHeating =0
                     helpCounterNumberOfStandBySlots_SpaceHeating +=1
                if action_heatCoefficientDHW > 0.01:
                     helpCounterNumberOfRunningSlots_DHW += 1
                     helpCounterNumberOfStandBySlots_DHW =0
                else:
                     helpCounterNumberOfRunningSlots_DHW = 0
                     helpCounterNumberOfStandBySlots_DHW +=1
                if action_heatCoefficientSpaceHeating > 0.01 or action_heatCoefficientDHW > 0.01:
                    helpCounterNumberOfRunningSlots_Combined += 1
                    helpCounterNumberOfStandBySlots_Combined =0
                else :
                    helpCounterNumberOfRunningSlots_Combined =0
                    helpCounterNumberOfStandBySlots_Combined +=1


                if helpCounterNumberOfRunningSlots_Combined > 0:
                    heatPumpIsRunning = 1
                else:
                    heatPumpIsRunning = 0


                outputVector_heatGenerationCoefficientSpaceHeating [state_indexCurrentTimeslot] = action_heatCoefficientSpaceHeating
                outputVector_heatGenerationCoefficientDHW [state_indexCurrentTimeslot] = action_heatCoefficientDHW

                outputVector_temperatureBufferStorage  [state_indexCurrentTimeslot] =state_temperatureBufferStorage
                outputVector_volumeDHWTank [state_indexCurrentTimeslot] = state_usableVolumeDHWTank

            df_resultingProfiles_Preliminary_BT2 = pd.DataFrame({'outputVector_heatGenerationCoefficientSpaceHeating': outputVector_heatGenerationCoefficientSpaceHeating[:],'outputVector_heatGenerationCoefficientDHW': outputVector_heatGenerationCoefficientDHW[:], 'outputVector_temperatureBufferStorage': outputVector_temperatureBufferStorage[:], 'usableVolumeDHWTank': outputVector_volumeDHWTank[ :]})

            df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientSpaceHeating'].round(3)
            df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientDHW'] = df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientDHW'].round(3)
            df_resultingProfiles_Preliminary_BT2 ['outputVector_temperatureBufferStorage'] = df_resultingProfiles_Preliminary_BT2 ['outputVector_temperatureBufferStorage'].round(3)
            df_resultingProfiles_Preliminary_BT2 ['usableVolumeDHWTank'] = df_resultingProfiles_Preliminary_BT2 ['usableVolumeDHWTank'].round(2)
            df_resultingProfiles_Preliminary_BT2.index += 1
            df_resultingProfiles_Preliminary_BT2.index.name = 'timeslot'
            df_resultingProfiles_Preliminary_BT2.insert(0, 'time of day', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_Preliminary_BT2), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))

            df_resultingProfiles_Preliminary_BT2.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT2_HH" + str(indexOfBuildingsOverall_BT2 [0] ) + ".csv" , index=True,  sep =";")

            filename = pathForCreatingTheResultData_ANN + "/Correction Stats Preliminary.txt"
            with open(filename, 'w') as f:
                print("Correction results for the single-time-slot internal controller (STSIC)", file = f)
                print("", file = f)
                print("correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC: ", correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC: ", round(correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC, 2), file = f)
                print("correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC: ", correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT2_heatGenerationCoefficientDHW_sumOfDeviations_STSIC: ", round(correctingStats_BT2_heatGenerationCoefficientDHW_sumOfDeviations_STSIC, 2), file = f)


            return outputVector_heatGenerationCoefficientSpaceHeating, outputVector_heatGenerationCoefficientDHW, outputVector_temperatureBufferStorage, outputVector_volumeDHWTank


   ##################################################################################################################################################################

    if SetUpScenarios.numberOfBuildings_BT3 ==1:

            #Set up variables
            action_chargingPowerEV = 0

            help_statePreviousTimeSlot_SOCOfTheEV = SetUpScenarios.initialSOC_EV

            helpCurrentPeakLoad = 0

            state_indexCurrentTimeslot = 0
            state_outsideTemperature = 0
            state_PVGeneration = 0
            state_electricityDemand = 0
            state_availabilityOfTheEV = 0
            state_priceForElectricity_CentsPerkWh = 0
            state_energyDemandEV = 0
            helpPVGenerationPreviousTimeSlot = 0
            electricalLoadPreviousTimeSlot = 0
            helpHypotheticalSOCDropNoCharging_PreviousTimeSlot  = 0

            correctingStats_BT3_chargingPowerEV_numberOfTimeSlots_STSIC =0
            correctingStats_BT3_chargingPowerEV_sumOfDeviations_STSIC =0


            #Loop for generating the actions and the "inline" simulation (meaning the simulation necessary for generating the actions)
            for state_indexCurrentTimeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):


                #Load trained ML method
                if usedDaySelectionMethod == 'Random':

                    # Currently used features in method trainSupvervisedML_SinlgeTimeSlots:MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]']]

                    # Feature names translation from method trainSupvervisedML_SinlgeTimeSlots: 'timeslot': state_indexCurrentTimeslot, 'temperatureBufferStorage': help_statePreviousTimeSlot_usableVolumeDHWTank, 'usableVolumeDHWTank': help_statePreviousTimeSlot_usableVolumeDHWTank, 'simulationResult_SOCofEV': help_statePreviousTimeSlot_SOCOfTheEV, 'simulationResult_RESGeneration': state_PVGeneration, 'Space Heating [W]': state_heatDemand, 'DHW [W]':state_DHWDemand, 'Electricity [W]': state_electricityDemand, 'Availability of the EV': state_availabilityOfTheEV, 'Outside Temperature [C]': state_outsideTemperature, 'Price [Cent/kWh]': state_priceForElectricity_CentsPerkWh, 'numberOfStarts_HP':help_countNumberOfStartHeatPump_Heating_Combined, 'HP_isRunning' = heatPumpIsRunning

                    #Create vector with input features and scale it
                    if objective == 'Min_Costs':
                        vector_input_features =  np.array([state_indexCurrentTimeslot,help_statePreviousTimeSlot_SOCOfTheEV, state_PVGeneration, state_electricityDemand, state_availabilityOfTheEV,state_outsideTemperature, state_priceForElectricity_CentsPerkWh])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                    if objective == 'Min_SurplusEnergy':
                        vector_input_features =  np.array([state_indexCurrentTimeslot,help_statePreviousTimeSlot_SOCOfTheEV, state_PVGeneration, state_electricityDemand, state_availabilityOfTheEV,state_outsideTemperature])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                    if objective == 'Min_Peak':
                        vector_input_features =  np.array([state_indexCurrentTimeslot,help_statePreviousTimeSlot_SOCOfTheEV, state_PVGeneration, state_electricityDemand, state_availabilityOfTheEV,state_outsideTemperature])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))



                    vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)
                    vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled.reshape(1, -1))


                    action_chargingPowerEV = vector_output_labels[0][0]




                # Assign values to the non-adjustable state variables (parameters)

                state_PVGeneration = list_df_buildingData_BT3 [indexOfBuildingsOverall_BT3[0] - 1] ['PV [nominal]'] [ state_indexCurrentTimeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT3 [0] - 1)
                state_electricityDemand  = list_df_buildingData_BT3 [indexOfBuildingsOverall_BT3[0] - 1] ['Electricity [W]'] [ state_indexCurrentTimeslot + 1 ]
                state_availabilityOfTheEV = list_df_buildingData_BT3 [indexOfBuildingsOverall_BT3[0] - 1] ['Availability of the EV'] [ state_indexCurrentTimeslot + 1 ]

                state_outsideTemperature = df_outsideTemperatureData ['Temperature [C]'] [ state_indexCurrentTimeslot + 1 ]
                state_priceForElectricity_CentsPerkWh = df_priceData ['Price [Cent/kWh]'] [ state_indexCurrentTimeslot + 1 ]
                state_energyDemandEV =  list_df_energyConsumptionEV_Joule_BT3 [indexOfBuildingsOverall_BT3[0] - 1] ['Energy'] [ state_indexCurrentTimeslot + 1]


                overuleActions = True

                #Store current actions before passing through the single-time-slot internal controller (STSIC) for correction statistics

                action_chargingPowerEV_NotOverruled = action_chargingPowerEV


                # Pass values to the internal controller TODO: Test internal controller
                action_chargingPowerEV, state_SOCOfTheEV , helpCurrentPeakLoad,helpHypotheticalSOCDropNoCharging = ICSimulation.simulateTimeSlot_WithAddtionalController_BT3 (overuleActions, action_chargingPowerEV, help_statePreviousTimeSlot_SOCOfTheEV,helpCurrentPeakLoad, state_indexCurrentTimeslot, state_outsideTemperature, state_PVGeneration, state_electricityDemand, state_availabilityOfTheEV, state_energyDemandEV, state_priceForElectricity_CentsPerkWh,  helpPVGenerationPreviousTimeSlot, electricalLoadPreviousTimeSlot, helpHypotheticalSOCDropNoCharging_PreviousTimeSlot)



                #Calculate the correction statistics of the single-time-slot internal controller
                if action_chargingPowerEV != action_chargingPowerEV_NotOverruled:
                    correctingStats_BT3_chargingPowerEV_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT3_chargingPowerEV_sumOfDeviations_STSIC = correctingStats_BT3_chargingPowerEV_sumOfDeviations_STSIC + abs(action_chargingPowerEV - action_chargingPowerEV_NotOverruled)


               #Assign values to the auxillary variabless


                help_statePreviousTimeSlot_SOCOfTheEV = state_SOCOfTheEV
                helpPVGenerationPreviousTimeSlot = state_PVGeneration
                electricalLoadPreviousTimeSlot =  state_electricityDemand  + action_chargingPowerEV

                outputVector_chargingPowerEV  [state_indexCurrentTimeslot] = action_chargingPowerEV
                outputVector_SOC [state_indexCurrentTimeslot] = state_SOCOfTheEV


            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT3 = pd.DataFrame({'outputVector_chargingPowerEV': outputVector_chargingPowerEV[:], 'outputVector_SOC': outputVector_SOC[:]})

            df_resultingProfiles_Preliminary_BT3 ['outputVector_chargingPowerEV'] = df_resultingProfiles_Preliminary_BT3 ['outputVector_chargingPowerEV'].round(3)
            df_resultingProfiles_Preliminary_BT3 ['outputVector_SOC'] = df_resultingProfiles_Preliminary_BT3 ['outputVector_SOC'].round(2)
            df_resultingProfiles_Preliminary_BT3.index += 1
            df_resultingProfiles_Preliminary_BT3.index.name = 'timeslot'
            df_resultingProfiles_Preliminary_BT3.insert(0, 'time of day', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_Preliminary_BT3), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))

            df_resultingProfiles_Preliminary_BT3.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT3_HH" + str(indexOfBuildingsOverall_BT3 [0] ) + ".csv" , index=True,  sep =";")

            filename = pathForCreatingTheResultData_ANN + "/Correction Stats Preliminary.txt"
            with open(filename, 'w') as f:
                print("Correction results for the single-time-slot internal controller (STSIC)", file = f)
                print("", file = f)
                print("correctingStats_BT3_chargingPowerEV_numberOfTimeSlots_STSIC: ", correctingStats_BT3_chargingPowerEV_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT3_chargingPowerEV_sumOfDeviations_STSIC: ", round(correctingStats_BT3_chargingPowerEV_sumOfDeviations_STSIC, 2), file = f)


            return outputVector_chargingPowerEV, outputVector_SOC


#######################################################################################################################################

    if SetUpScenarios.numberOfBuildings_BT4 ==1:

            #Set up variables
            action_heatCoefficientSpaceHeating = 0

            help_actionPreviousTimeSlot_heatCoefficientSpaceHeating  = 0

            help_statePreviousTimeSlot_temperatureBufferStorage = SetUpScenarios.initialBufferStorageTemperature

            help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual = 0
            help_countNumberOfStartHeatPump_Heating_Combined = 0
            helpCounterNumberOfRunningSlots_SpaceHeating = 0
            helpCounterNumberOfRunningSlots_Combined = 0
            helpCounterNumberOfStandBySlots_SpaceHeating = 0
            helpCounterNumberOfStandBySlots_Combined = 0
            helpCurrentPeakLoad = 0
            helpStartedHeatingHeatPump = False
            helpStoppedHeatingHeatPump = False
            startedHeatingSpaceHeatingCorrection_end = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = False
            heatingStartedPhysicalLimit_BufferStorage = False
            heatPumpIsRunning =0

            numberOfHeatPumpStartsReachedSoftLimit = False
            numberOfHeatPumpStartsReachedHardLimit = False
            state_indexCurrentTimeslot = 0
            state_outsideTemperature = 0
            state_PVGeneration = 0
            state_heatDemand = 0
            state_electricityDemand = 0
            state_priceForElectricity_CentsPerkWh = 0
            helpPVGenerationPreviousTimeSlot = 0
            electricalLoadPreviousTimeSlot = 0

            correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC =0
            correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC =0


            #Calculate the COPs for the heat pump
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])
            df_copHeatPump =  pd.DataFrame({'Timeslot': list_df_buildingData_BT4 [0].index, 'COP_SpaceHeating':cop_heatPump_SpaceHeating, 'COP_DHW':cop_heatPump_DHW})


            #Loop for generating the actions and the "inline" simulation (meaning the simulation necessary for generating the actions)
            for state_indexCurrentTimeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):


                #Load trained ML method
                if usedDaySelectionMethod == 'Random':

                    # Currently used features in method trainSupvervisedML_SinlgeTimeSlots:  = combined_df[['timeslot', 'temperatureBufferStorage', 'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]

                    # Feature names translation from method trainSupvervisedML_SinlgeTimeSlots: 'timeslot': state_indexCurrentTimeslot, 'temperatureBufferStorage': help_statePreviousTimeSlot_usableVolumeDHWTank, 'usableVolumeDHWTank': help_statePreviousTimeSlot_usableVolumeDHWTank, 'simulationResult_SOCofEV': help_statePreviousTimeSlot_SOCOfTheEV, 'simulationResult_RESGeneration': state_PVGeneration, 'Space Heating [W]': state_heatDemand, 'DHW [W]':state_DHWDemand, 'Electricity [W]': state_electricityDemand, 'Availability of the EV': state_availabilityOfTheEV, 'Outside Temperature [C]': state_outsideTemperature, 'Price [Cent/kWh]': state_priceForElectricity_CentsPerkWh, 'numberOfStarts_HP':help_countNumberOfStartHeatPump_Heating_Combined, 'HP_isRunning' = heatPumpIsRunning

                    #MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]


                    #Create vector with input features and scale it
                    if objective == 'Min_Costs':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, state_PVGeneration, state_heatDemand, state_electricityDemand, state_outsideTemperature, state_priceForElectricity_CentsPerkWh, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                    if objective == 'Min_SurplusEnergy':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, state_PVGeneration, state_heatDemand, state_electricityDemand, state_outsideTemperature, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                    if objective == 'Min_Peak':
                        vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_temperatureBufferStorage, state_PVGeneration, state_heatDemand, state_electricityDemand, state_outsideTemperature, help_countNumberOfStartHeatPump_Heating_Combined, heatPumpIsRunning])
                        vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))



                    vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)
                    vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled.reshape(1, -1))



                    #Assign action values to the variables of the simulation
                    action_heatCoefficientSpaceHeating = vector_output_labels[0][0]


                # Assign values to the non-adjustable state variables (parameters)

                state_PVGeneration = list_df_buildingData_BT4 [indexOfBuildingsOverall_BT4 [0] - 1] ['PV [nominal]'] [ state_indexCurrentTimeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT4 [0] - 1)
                state_heatDemand  = list_df_buildingData_BT4 [indexOfBuildingsOverall_BT4 [0] - 1] ['Space Heating [W]'] [ state_indexCurrentTimeslot + 1 ]
                state_electricityDemand  = list_df_buildingData_BT4 [indexOfBuildingsOverall_BT4 [0] - 1] ['Electricity [W]'] [ state_indexCurrentTimeslot + 1 ]

                state_outsideTemperature = df_outsideTemperatureData ['Temperature [C]'] [ state_indexCurrentTimeslot + 1 ]
                state_priceForElectricity_CentsPerkWh = df_priceData ['Price [Cent/kWh]'] [ state_indexCurrentTimeslot + 1 ]


                overuleActions = True

                #Store current actions before passing through the single-time-slot internal controller (STSIC) for correction statistics
                action_heatCoefficientSpaceHeating_NotOverruled = action_heatCoefficientSpaceHeating

                # Pass values to the internal controller TODO: Test internal controller
                action_heatCoefficientSpaceHeating, state_temperatureBufferStorage, help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual, help_countNumberOfStartHeatPump_Heating_Combined , helpCounterNumberOfRunningSlots_SpaceHeating  , helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating ,  helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, startedHeatingSpaceHeatingCorrection_end = ICSimulation.simulateTimeSlot_WithAddtionalController_BT4 (overuleActions, action_heatCoefficientSpaceHeating, help_statePreviousTimeSlot_temperatureBufferStorage, help_countNumberOfStartHeatPump_HeatingBufferStorage_Indiviual, help_countNumberOfStartHeatPump_Heating_Combined , helpCounterNumberOfRunningSlots_SpaceHeating ,  helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating  , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, helpStoppedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, state_indexCurrentTimeslot, state_outsideTemperature, state_PVGeneration, state_heatDemand, state_electricityDemand, state_priceForElectricity_CentsPerkWh,  df_copHeatPump ["COP_SpaceHeating"] [ state_indexCurrentTimeslot ], helpPVGenerationPreviousTimeSlot, electricalLoadPreviousTimeSlot, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, startedHeatingSpaceHeatingCorrection_end)


                #Calculate the correction statistics of the single-time-slot internal controller
                if action_heatCoefficientSpaceHeating != action_heatCoefficientSpaceHeating_NotOverruled:
                    correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC += 1
                    correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC = correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC + abs(action_heatCoefficientSpaceHeating - action_heatCoefficientSpaceHeating_NotOverruled)


               #Assign values to the auxillary variabless

                if (help_actionPreviousTimeSlot_heatCoefficientSpaceHeating ==0 ) and (action_heatCoefficientSpaceHeating > 0.01 ):
                    helpStartedHeatingHeatPump = True
                    helpStoppedHeatingHeatPump = False
                    help_countNumberOfStartHeatPump_Heating_Combined +=1
                if (help_actionPreviousTimeSlot_heatCoefficientSpaceHeating > 0.01) and (action_heatCoefficientSpaceHeating ==0):
                    helpStartedHeatingHeatPump = False
                    helpStoppedHeatingHeatPump = True
                    if lastHeatingAfterHeatPumpStartsReachedHardLimitStarted ==True:
                        lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = True


                help_statePreviousTimeSlot_temperatureBufferStorage = state_temperatureBufferStorage
                help_actionPreviousTimeSlot_heatCoefficientSpaceHeating= action_heatCoefficientSpaceHeating
                helpPVGenerationPreviousTimeSlot = state_PVGeneration
                electricalLoadPreviousTimeSlot =  state_electricityDemand + (action_heatCoefficientSpaceHeating )  *  SetUpScenarios.electricalPower_HP


                if action_heatCoefficientSpaceHeating > 0.01:
                     helpCounterNumberOfRunningSlots_SpaceHeating  += 1
                     helpCounterNumberOfStandBySlots_SpaceHeating =0
                else :
                     helpCounterNumberOfRunningSlots_SpaceHeating =0
                     helpCounterNumberOfStandBySlots_SpaceHeating +=1

                if action_heatCoefficientSpaceHeating > 0.01:
                    helpCounterNumberOfRunningSlots_Combined += 1
                    helpCounterNumberOfStandBySlots_Combined =0
                else :
                    helpCounterNumberOfRunningSlots_Combined =0
                    helpCounterNumberOfStandBySlots_Combined +=1

                if helpCounterNumberOfRunningSlots_Combined > 0:
                    heatPumpIsRunning = 1
                else:
                    heatPumpIsRunning = 0


                outputVector_heatGenerationCoefficientSpaceHeating [state_indexCurrentTimeslot] = action_heatCoefficientSpaceHeating

                outputVector_temperatureBufferStorage  [state_indexCurrentTimeslot] =state_temperatureBufferStorage



            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT4 = pd.DataFrame({'outputVector_heatGenerationCoefficientSpaceHeating': outputVector_heatGenerationCoefficientSpaceHeating[:], 'outputVector_temperatureBufferStorage': outputVector_temperatureBufferStorage[:]})

            df_resultingProfiles_Preliminary_BT4 ['outputVector_heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_Preliminary_BT4 ['outputVector_heatGenerationCoefficientSpaceHeating'].round(3)
            df_resultingProfiles_Preliminary_BT4 ['outputVector_temperatureBufferStorage'] = df_resultingProfiles_Preliminary_BT4 ['outputVector_temperatureBufferStorage'].round(2)
            df_resultingProfiles_Preliminary_BT4.index += 1
            df_resultingProfiles_Preliminary_BT4.index.name = 'timeslot'
            df_resultingProfiles_Preliminary_BT4.insert(0, 'time of day', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_Preliminary_BT4), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))

            df_resultingProfiles_Preliminary_BT4.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT4_HH" + str(indexOfBuildingsOverall_BT4 [0] ) + ".csv" , index=True,  sep =";")

            filename = pathForCreatingTheResultData_ANN + "/Correction Stats Preliminary.txt"
            with open(filename, 'w') as f:
                print("Correction results for the single-time-slot internal controller (STSIC)", file = f)
                print("", file = f)
                print("correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC: ", correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots_STSIC, file = f)
                print("correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC: ", round(correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfDeviations_STSIC,2), file = f)


            return outputVector_heatGenerationCoefficientSpaceHeating, outputVector_temperatureBufferStorage

    ##################################################################################################################################################################

    if SetUpScenarios.numberOfBuildings_BT5 == 1:

        # Set up variables
        action_chargingPowerBAT = 0
        action_disChargingPowerBAT = 0

        help_statePreviousTimeSlot_SOCOfTheBAT = SetUpScenarios.initialSOC_BAT

        helpCurrentPeakLoad = 0

        state_indexCurrentTimeslot = 0
        state_outsideTemperature = 0
        state_PVGeneration = 0
        state_electricityDemand = 0
        state_priceForElectricity_CentsPerkWh = 0
        helpPVGenerationPreviousTimeSlot = 0
        electricalLoadPreviousTimeSlot = 0

        correctingStats_BT5_action_chargingPowerBAT_numberOfTimeSlots_STSIC = 0
        correctingStats_BT5_chargingPowerBAT_sumOfDeviations_STSIC = 0
        correctingStats_BT5_action_disChargingPowerBAT_numberOfTimeSlots_STSIC = 0
        correctingStats_BT5_disChargingPowerBAT_sumOfDeviations_STSIC = 0



        # Loop for generating the actions and the "inline" simulation (meaning the simulation necessary for generating the actions)
        for state_indexCurrentTimeslot in range(0, SetUpScenarios.numberOfTimeSlotsPerDay):

            #Load trained ML method
            if usedDaySelectionMethod == 'Random':

                # Currently used features in method trainSupvervisedML_SinlgeTimeSlots:            MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofBAT', 'simulationResult_RESGeneration',  'Electricity [W]',  'Outside Temperature [C]']]

                # Feature names translation from method trainSupvervisedML_SinlgeTimeSlots: 'timeslot': state_indexCurrentTimeslot, 'simulationResult_SOCofBAT': help_statePreviousTimeSlot_SOCOfTheBAT,  'simulationResult_RESGeneration': state_PVGeneration,  'Electricity [W]': state_electricityDemand, 'Outside Temperature [C]': state_outsideTemperature, 'Price [Cent/kWh]': state_priceForElectricity_CentsPerkWh, 'numberOfStarts_HP':help_countNumberOfStartHeatPump_Heating_Combined

                #MLSupervised_output_data = combined_df[['chargingPowerBATcombinedVariable']]


                #Create vector with input features and scale it
                if objective == 'Min_Costs':
                    vector_input_features = np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_SOCOfTheBAT, state_PVGeneration, state_electricityDemand, state_outsideTemperature, state_priceForElectricity_CentsPerkWh])
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                if objective == 'Min_SurplusEnergy':
                    vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_SOCOfTheBAT, state_PVGeneration, state_electricityDemand, state_outsideTemperature])
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))

                if objective == 'Min_Peak':
                    vector_input_features =  np.array([state_indexCurrentTimeslot, help_statePreviousTimeSlot_SOCOfTheBAT, state_PVGeneration, state_electricityDemand, state_outsideTemperature])
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features.reshape(1, -1))


                vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled.reshape(1, -1))


                vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled.reshape(1, -1))



                #Assign action values to the variables of the simulation
                resultinValueMLMethod = vector_output_labels[0][0]

                if resultinValueMLMethod >= 0:
                    action_chargingPowerBAT = resultinValueMLMethod
                    action_disChargingPowerBAT = 0
                else:
                    action_chargingPowerBAT = 0
                    action_disChargingPowerBAT = (-1) * resultinValueMLMethod


            # Assign values to the non-adjustable state variables (parameters)

            state_PVGeneration = list_df_buildingData_BT5[indexOfBuildingsOverall_BT5 [0] - 1]['PV [nominal]'][state_indexCurrentTimeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings( indexOfBuildingsOverall_BT5[0] - 1)
            state_electricityDemand = list_df_buildingData_BT5[indexOfBuildingsOverall_BT5 [0] - 1]['Electricity [W]'][state_indexCurrentTimeslot + 1]

            state_outsideTemperature = df_outsideTemperatureData['Temperature [C]'][state_indexCurrentTimeslot + 1]
            state_priceForElectricity_CentsPerkWh = df_priceData['Price [Cent/kWh]'][state_indexCurrentTimeslot + 1]


            overruleActions = True

            # Store current actions before passing through the single-time-slot internal controller (STSIC) for correction statistics

            action_chargingPowerBAT_NotOverruled = action_chargingPowerBAT
            action_disChargingPowerBAT_NotOverruled = action_disChargingPowerBAT


            # Pass values to the internal controller
            action_chargingPowerBAT,action_disChargingPowerBAT, state_SOCofBAT,  helpCurrentPeakLoad = ICSimulation.simulateTimeSlot_WithAddtionalController_BT5(overruleActions, action_chargingPowerBAT, action_disChargingPowerBAT, help_statePreviousTimeSlot_SOCOfTheBAT, helpCurrentPeakLoad, state_indexCurrentTimeslot, state_outsideTemperature, state_PVGeneration, state_electricityDemand, state_priceForElectricity_CentsPerkWh, helpPVGenerationPreviousTimeSlot, electricalLoadPreviousTimeSlot)

            # Calculate the correction statistics of the single-time-slot internal controller
            if action_chargingPowerBAT != action_chargingPowerBAT_NotOverruled:
                correctingStats_BT5_action_chargingPowerBAT_numberOfTimeSlots_STSIC += 1
                correctingStats_BT5_chargingPowerBAT_sumOfDeviations_STSIC = correctingStats_BT5_chargingPowerBAT_sumOfDeviations_STSIC + abs(action_chargingPowerBAT - action_chargingPowerBAT_NotOverruled)


            if action_disChargingPowerBAT != action_disChargingPowerBAT_NotOverruled:
                correctingStats_BT5_action_disChargingPowerBAT_numberOfTimeSlots_STSIC += 1
                correctingStats_BT5_disChargingPowerBAT_sumOfDeviations_STSIC = correctingStats_BT5_disChargingPowerBAT_sumOfDeviations_STSIC + abs(action_disChargingPowerBAT - action_disChargingPowerBAT_NotOverruled)

            # Assign values to the auxillary variabless

            help_statePreviousTimeSlot_SOCOfTheBAT = state_SOCofBAT
            helpPVGenerationPreviousTimeSlot = state_PVGeneration
            electricalLoadPreviousTimeSlot = state_electricityDemand + action_chargingPowerBAT - action_disChargingPowerBAT

            outputVector_chargingPowerBAT[state_indexCurrentTimeslot] = action_chargingPowerBAT
            outputVector_disChargingPowerBAT[state_indexCurrentTimeslot] = action_disChargingPowerBAT
            outputVector_SOC_BAT[state_indexCurrentTimeslot] = state_SOCofBAT

        # Print the preliminary results
        df_resultingProfiles_Preliminary_BT5 = pd.DataFrame({'outputVector_chargingPowerBAT': outputVector_chargingPowerBAT[:], 'outputVector_disChargingPowerBAT': outputVector_disChargingPowerBAT[:],'outputVector_SOC_BAT': outputVector_SOC_BAT[:]})

        df_resultingProfiles_Preliminary_BT5['outputVector_chargingPowerBAT'] = df_resultingProfiles_Preliminary_BT5['outputVector_chargingPowerBAT'].round(3)
        df_resultingProfiles_Preliminary_BT5['outputVector_disChargingPowerBAT'] = df_resultingProfiles_Preliminary_BT5['outputVector_disChargingPowerBAT'].round(3)
        df_resultingProfiles_Preliminary_BT5['outputVector_SOC_BAT'] = df_resultingProfiles_Preliminary_BT5['outputVector_SOC_BAT'].round(2)
        df_resultingProfiles_Preliminary_BT5.index += 1
        df_resultingProfiles_Preliminary_BT5.index.name = 'timeslot'
        df_resultingProfiles_Preliminary_BT5.insert(0, 'time of day', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_Preliminary_BT5), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))

        df_resultingProfiles_Preliminary_BT5.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT5_HH" + str(indexOfBuildingsOverall_BT5[0] ) + ".csv",index=True, sep=";")

        filename = pathForCreatingTheResultData_ANN + "/Correction Stats Preliminary.txt"
        with open(filename, 'w') as f:
            print("Correction results for the single-time-slot internal controller (STSIC)", file=f)
            print("", file=f)
            print("correctingStats_BT5_action_chargingPowerBAT_numberOfTimeSlots_STSIC: ",correctingStats_BT5_action_chargingPowerBAT_numberOfTimeSlots_STSIC, file=f)
            print("correctingStats_BT5_chargingPowerBAT_sumOfDeviations_STSIC: ",round(correctingStats_BT5_chargingPowerBAT_sumOfDeviations_STSIC,2), file=f)
            print("correctingStats_BT5_action_disChargingPowerBAT_numberOfTimeSlots_STSIC: ",correctingStats_BT5_action_disChargingPowerBAT_numberOfTimeSlots_STSIC, file=f)
            print("correctingStats_BT5_disChargingPowerBAT_sumOfDeviations_STSIC: ",round(correctingStats_BT5_disChargingPowerBAT_sumOfDeviations_STSIC,2), file=f)

        return outputVector_chargingPowerBAT, outputVector_disChargingPowerBAT, outputVector_SOC_BAT


# Generates the actions for single time slots and for the single building optimization scenario by using an ANN.
# Input:
# Output: schedule
def generateActionsForMutipleTimeslotWithANN_SingleBuildingOptScenario (indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentDay ,pathForCreatingTheResultData_ANN, objective, usedDaySelectionMethod, dataScaler_InputFeatures, dataScaler_OutputLabels, trainedModel):
    import ICSimulation


    #Reading of the price data
    df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_Days/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_Day' +  str(currentDay) + '.csv', sep =";")
    df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
    df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
    arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
    df_priceData['Timeslot'] = arrayTimeSlots
    df_priceData = df_priceData.set_index('Timeslot')

    #Reading outside temperature data
    df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_Days/Outside_Temperature_1Minute_Day' +  str(currentDay) + '.csv', sep =";")
    df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
    df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
    df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
    df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

    cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])

    #Create the price data
    df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
    df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
    df_priceData['Timeslot'] = arrayTimeSlots
    df_priceData = df_priceData.set_index('Timeslot')


    #Reading of the building data
    list_df_buildingData_BT1_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT1_mHP_EV_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT1]
    list_df_buildingData_BT2_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT2_mHP_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT2]
    list_df_buildingData_BT3_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT3_EV_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT3]
    list_df_buildingData_BT4_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT4_mHP_MFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT4]
    list_df_buildingData_BT5_original= [pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT5_BAT_SFH_1Minute_Days/HH" + str(index) + "/HH" + str(index) + "_Day" + str(currentDay) +".csv", sep =";") for index in indexOfBuildingsOverall_BT5]


    list_df_buildingData_BT1 = list_df_buildingData_BT1_original.copy()
    list_df_buildingData_BT2 = list_df_buildingData_BT2_original.copy()
    list_df_buildingData_BT3 = list_df_buildingData_BT3_original.copy()
    list_df_buildingData_BT4 = list_df_buildingData_BT4_original.copy()
    list_df_buildingData_BT5 = list_df_buildingData_BT5_original.copy()



    #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
    for i in range (0, len(list_df_buildingData_BT1_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT1_original[i]:
            list_df_buildingData_BT1_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT2_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT2_original[i]:
            list_df_buildingData_BT2_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT3_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT3_original[i]:
            list_df_buildingData_BT3_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT4_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT4_original[i]:
            list_df_buildingData_BT4_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)
    for i in range (0, len(list_df_buildingData_BT5_original)):
        if 'Demand Electricity [W]' in list_df_buildingData_BT5_original[i]:
            list_df_buildingData_BT5_original[i].rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


    #Adjust dataframes to the current time resolution and set new index "Timeslot"

    for i in range (0, len(list_df_buildingData_BT1_original)):
        list_df_buildingData_BT1_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT1_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT1 [i] = list_df_buildingData_BT1_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
        for j in range (0, len(list_df_buildingData_BT1[i]['Availability of the EV'])):
            if list_df_buildingData_BT1 [i]['Availability of the EV'] [j] > 0.1:
                list_df_buildingData_BT1 [i]['Availability of the EV'] [j] = 1.0
            if list_df_buildingData_BT1 [i]['Availability of the EV'] [j] < 0.1 and list_df_buildingData_BT1 [i]['Availability of the EV'] [j] >0.01:
                list_df_buildingData_BT1 [i]['Availability of the EV'] [j] = 0

        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT1 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT1 [i] = list_df_buildingData_BT1 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT2_original)):
        list_df_buildingData_BT2_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT2_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT2 [i] = list_df_buildingData_BT2_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT2 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT2 [i] = list_df_buildingData_BT2 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT3_original)):
        list_df_buildingData_BT3_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT3_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT3 [i] = list_df_buildingData_BT3_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
        for j in range (0, len(list_df_buildingData_BT3[i]['Availability of the EV'])):
            if list_df_buildingData_BT3 [i]['Availability of the EV'] [j] > 0.1:
                list_df_buildingData_BT3 [i]['Availability of the EV'] [j] = 1.0
            if list_df_buildingData_BT3 [i]['Availability of the EV'] [j] < 0.1 and list_df_buildingData_BT3 [i]['Availability of the EV'] [j] >0.01:
                list_df_buildingData_BT3 [i]['Availability of the EV'] [j] = 0

        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT3 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT3 [i] = list_df_buildingData_BT3 [i].set_index('Timeslot')

    for i in range (0, len(list_df_buildingData_BT4_original)):
        list_df_buildingData_BT4_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT4_original[i]['Time'], format = '%d.%m.%Y %H:%M')
        list_df_buildingData_BT4 [i] = list_df_buildingData_BT4_original[i].set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()


        arrayTimeSlots = [k for k in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT4 [i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT4 [i] = list_df_buildingData_BT4 [i].set_index('Timeslot')

    for i in range(0, len(list_df_buildingData_BT5_original)):
        list_df_buildingData_BT5_original[i]['Time'] = pd.to_datetime(list_df_buildingData_BT5_original[i]['Time'],format='%d.%m.%Y %H:%M')
        list_df_buildingData_BT5[i] = list_df_buildingData_BT5_original[i].set_index('Time').resample(
            str(SetUpScenarios.timeResolution_InMinutes) + 'Min').mean()

        arrayTimeSlots = [k for k in range(1, SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
        list_df_buildingData_BT5[i]['Timeslot'] = arrayTimeSlots
        list_df_buildingData_BT5[i] = list_df_buildingData_BT5[i].set_index('Timeslot')


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT1):
        decimalsForRounding = 2
        list_df_buildingData_BT1 [index]['Electricity [W]'] = list_df_buildingData_BT1 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT1 [index]['Space Heating [W]'] = list_df_buildingData_BT1 [index]['Space Heating [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT1 [index]['DHW [W]'] = list_df_buildingData_BT1 [index]['DHW [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT1 [index]['PV [nominal]'] = list_df_buildingData_BT1 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT2):
        decimalsForRounding = 2
        list_df_buildingData_BT2 [index]['Electricity [W]'] = list_df_buildingData_BT2 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT2 [index]['Space Heating [W]'] = list_df_buildingData_BT2 [index]['Space Heating [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT2 [index]['DHW [W]'] = list_df_buildingData_BT2 [index]['DHW [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT2 [index]['PV [nominal]'] = list_df_buildingData_BT2 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT3):
        decimalsForRounding = 2
        list_df_buildingData_BT3 [index]['Electricity [W]'] = list_df_buildingData_BT3 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT3 [index]['PV [nominal]'] = list_df_buildingData_BT3 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


    #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT4):
        decimalsForRounding = 2
        list_df_buildingData_BT4 [index]['Electricity [W]'] = list_df_buildingData_BT4 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        list_df_buildingData_BT4 [index]['Space Heating [W]'] = list_df_buildingData_BT4 [index]['Space Heating [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT4 [index]['PV [nominal]'] = list_df_buildingData_BT4 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))


      #Round the values
    for index in range (0,  SetUpScenarios.numberOfBuildings_BT5):
        decimalsForRounding = 2
        list_df_buildingData_BT5 [index]['Electricity [W]'] = list_df_buildingData_BT5 [index]['Electricity [W]'].apply(lambda x: round(x, decimalsForRounding))
        decimalsForRounding = 4
        list_df_buildingData_BT5 [index]['PV [nominal]'] = list_df_buildingData_BT5 [index]['PV [nominal]'].apply(lambda x: round(x, decimalsForRounding))



    # Create wind power profile for BT1
    list_windProfileNominal_BT1 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,index_BT1) for index_BT1 in range(0, SetUpScenarios.numberOfBuildings_BT1)]
    list_df_windPowerAssignedNominalPerBuilding_BT1 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT1 [i].index, 'Wind [nominal]':list_windProfileNominal_BT1[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT1)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT1)):
        del list_df_windPowerAssignedNominalPerBuilding_BT1[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT1[i].index +=1

    # Create wind power profile for BT2
    list_windProfileNominal_BT2 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + index_BT2) for index_BT2 in range(0, SetUpScenarios.numberOfBuildings_BT2)]
    list_df_windPowerAssignedNominalPerBuilding_BT2 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT2 [i].index, 'Wind [nominal]':list_windProfileNominal_BT2[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT2)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT2)):
        del list_df_windPowerAssignedNominalPerBuilding_BT2[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT2[i].index +=1


    # Create wind power profile for BT3
    list_windProfileNominal_BT3 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3) for index_BT3 in range(0, SetUpScenarios.numberOfBuildings_BT3)]
    list_df_windPowerAssignedNominalPerBuilding_BT3 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT3 [i].index, 'Wind [nominal]':list_windProfileNominal_BT3[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT3)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT3)):
        del list_df_windPowerAssignedNominalPerBuilding_BT3[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT3[i].index +=1


    # Create wind power profile for BT4
    list_windProfileNominal_BT4 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3  + index_BT4) for index_BT4 in range(0, SetUpScenarios.numberOfBuildings_BT4)]
    list_df_windPowerAssignedNominalPerBuilding_BT4 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT4 [i].index, 'Wind [nominal]':list_windProfileNominal_BT4[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT4)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT4)):
        del list_df_windPowerAssignedNominalPerBuilding_BT4[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT4[i].index +=1

    # Create wind power profile for BT5
    list_windProfileNominal_BT5 = [SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentDay,SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + SetUpScenarios.numberOfBuildings_BT4 + index_BT5) for index_BT5 in range(0, SetUpScenarios.numberOfBuildings_BT5)]
    list_df_windPowerAssignedNominalPerBuilding_BT5 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT5 [i].index, 'Wind [nominal]':list_windProfileNominal_BT5[i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT5)]

    for i in range (0, len(list_df_windPowerAssignedNominalPerBuilding_BT5)):
        del list_df_windPowerAssignedNominalPerBuilding_BT5[i]['Timeslot']
        list_df_windPowerAssignedNominalPerBuilding_BT5[i].index +=1


    #Create availability array for the EV of BT1
    availabilityOfTheEVCombined = np.zeros((SetUpScenarios.numberOfBuildings_WithEV, SetUpScenarios.numberOfTimeSlotsPerDay))
    for index_BT1 in range (0, SetUpScenarios.numberOfBuildings_BT1):
        for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerDay):
            availabilityOfTheEVCombined [index_BT1,index_timeslot_for_Availability] = list_df_buildingData_BT1 [index_BT1]['Availability of the EV'] [index_timeslot_for_Availability +1]


    list_energyConsumptionOfEVs_Joule_BT1 = np.zeros((SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerDay))


    for indexEV in range (0, SetUpScenarios.numberOfBuildings_BT1):
        list_energyConsumptionOfEVs_Joule_BT1[indexEV] = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEVCombined [indexEV],indexEV)

    list_df_energyConsumptionEV_Joule_BT1 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT1 [i].index, 'Energy':list_energyConsumptionOfEVs_Joule_BT1 [i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT1)]


    for i in range (0, len(list_energyConsumptionOfEVs_Joule_BT1)):
        del list_df_energyConsumptionEV_Joule_BT1 [i]['Timeslot']
        list_df_energyConsumptionEV_Joule_BT1[i].index +=1


    #Create availability array for the EV of BT3
    availabilityOfTheEVCombined = np.zeros((SetUpScenarios.numberOfBuildings_WithEV, SetUpScenarios.numberOfTimeSlotsPerDay))
    for index_BT3 in range (0, SetUpScenarios.numberOfBuildings_BT3):
        for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerDay):
            availabilityOfTheEVCombined [SetUpScenarios.numberOfBuildings_BT1 + index_BT3,index_timeslot_for_Availability] = list_df_buildingData_BT3 [index_BT3]['Availability of the EV'] [index_timeslot_for_Availability +1]


    list_energyConsumptionOfEVs_Joule_BT3 = np.zeros((SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerDay))


    for indexEV in range (0, SetUpScenarios.numberOfBuildings_BT3):
        list_energyConsumptionOfEVs_Joule_BT3[indexEV] = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEVCombined [SetUpScenarios.numberOfBuildings_BT1 + indexEV],SetUpScenarios.numberOfBuildings_BT1 + indexEV)

    list_df_energyConsumptionEV_Joule_BT3 = [pd.DataFrame({'Timeslot': list_df_buildingData_BT3 [i].index, 'Energy':list_energyConsumptionOfEVs_Joule_BT3 [i] }) for i in range (0, SetUpScenarios.numberOfBuildings_BT3)]


    for i in range (0, len(list_energyConsumptionOfEVs_Joule_BT3)):
        del list_df_energyConsumptionEV_Joule_BT3 [i]['Timeslot']
        list_df_energyConsumptionEV_Joule_BT3[i].index +=1


    #Define arrays for storing the output values
    outputVector_heatGenerationCoefficientSpaceHeating = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_heatGenerationCoefficientDHW = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)
    outputVector_chargingPowerEV = np.zeros( SetUpScenarios.numberOfTimeSlotsPerDay)


    if SetUpScenarios.numberOfBuildings_BT1 ==1:

            #Calculate the COPs for the heat pump
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])
            df_copHeatPump =  pd.DataFrame({'Timeslot': list_df_buildingData_BT1 [0].index, 'COP_SpaceHeating':cop_heatPump_SpaceHeating, 'COP_DHW':cop_heatPump_DHW})


            #Load trained ML method
            if usedDaySelectionMethod == 'Random':

                # Currently used features in method trainSupvervisedML_SinlgeTimeSlots: combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Outside Temperature [C]']]

                #Create vector with input features and scale it
                if objective == 'Min_Costs':


                    df_new = df_outsideTemperatureData
                    df_new['Availability of the EV'] = list_df_buildingData_BT1[index]['Availability of the EV'].values
                    df_new['PV [nominal]'] = list_df_buildingData_BT1[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT1 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Availability of the EV','Temperature [C]','Price [Cent/kWh]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                if objective == 'Min_SurplusEnergy':

                    df_new = df_outsideTemperatureData
                    df_new['Availability of the EV'] = list_df_buildingData_BT1[index]['Availability of the EV'].values
                    df_new['PV [nominal]'] = list_df_buildingData_BT1[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT1 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Availability of the EV','Temperature [C]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    print(f"vector_input_features.shape: {vector_input_features.shape}")
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))

                if objective == 'Min_Peak':
                    df_new = df_outsideTemperatureData
                    df_new['Availability of the EV'] = list_df_buildingData_BT1[index]['Availability of the EV'].values
                    df_new['PV [nominal]'] = list_df_buildingData_BT1[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT1 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Availability of the EV','Temperature [C]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    print(f"vector_input_features.shape: {vector_input_features.shape}")
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)

                vector_output_labels_scaled = vector_output_labels_scaled.reshape(SetUpScenarios.numberOfTimeSlotsPerDay, len(vector_output_labels_scaled [0][0]))
                vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)

            outputVector_heatGenerationCoefficientSpaceHeating =  vector_output_labels[:, 0]
            outputVector_heatGenerationCoefficientDHW =  vector_output_labels[:, 1]
            outputVector_chargingPowerEV =  vector_output_labels[:, 2]

            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT1 = pd.DataFrame({'outputVector_heatGenerationCoefficientSpaceHeating':outputVector_heatGenerationCoefficientSpaceHeating[:],'outputVector_heatGenerationCoefficientDHW': outputVector_heatGenerationCoefficientDHW[:],'outputVector_chargingPowerEV': outputVector_chargingPowerEV[:]})

            df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientSpaceHeating'].round(3)
            df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientDHW'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_heatGenerationCoefficientDHW'].round(3)
            df_resultingProfiles_Preliminary_BT1 ['outputVector_chargingPowerEV'] = df_resultingProfiles_Preliminary_BT1 ['outputVector_chargingPowerEV'].round(3)

            df_resultingProfiles_Preliminary_BT1.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT1_HH" + str(indexOfBuildingsOverall_BT1 [0] ) + ".csv" , index=True,  sep =";")


            return outputVector_heatGenerationCoefficientSpaceHeating, outputVector_heatGenerationCoefficientDHW, outputVector_chargingPowerEV



    #############################################################################################################################

    if SetUpScenarios.numberOfBuildings_BT2 ==1:

            #Calculate the COPs for the heat pump
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])
            df_copHeatPump =  pd.DataFrame({'Timeslot': list_df_buildingData_BT2 [0].index, 'COP_SpaceHeating':cop_heatPump_SpaceHeating, 'COP_DHW':cop_heatPump_DHW})


            #Load trained ML method
            if usedDaySelectionMethod == 'Random':

                # Currently used features in method trainSupvervisedML_SinlgeTimeSlots: combined_df[['timeslot', 'simulationResult_RESGeneration', 'Outside Temperature [C]']]

                #Create vector with input features and scale it
                if objective == 'Min_Costs':


                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT2[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT2 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]', 'Temperature [C]','Price [Cent/kWh]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                if objective == 'Min_SurplusEnergy':

                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT2[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT2 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Temperature [C]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    print(f"vector_input_features.shape: {vector_input_features.shape}")
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))

                if objective == 'Min_Peak':
                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT2[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT2 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Temperature [C]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    print(f"vector_input_features.shape: {vector_input_features.shape}")
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)

                vector_output_labels_scaled = vector_output_labels_scaled.reshape(SetUpScenarios.numberOfTimeSlotsPerDay, len(vector_output_labels_scaled [0][0]))
                vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)

            outputVector_heatGenerationCoefficientSpaceHeating =  vector_output_labels[:, 0]
            outputVector_heatGenerationCoefficientDHW =  vector_output_labels[:, 1]

            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT2 = pd.DataFrame({'outputVector_heatGenerationCoefficientSpaceHeating':outputVector_heatGenerationCoefficientSpaceHeating[:],'outputVector_heatGenerationCoefficientDHW': outputVector_heatGenerationCoefficientDHW[:]})

            df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientSpaceHeating'].round(3)
            df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientDHW'] = df_resultingProfiles_Preliminary_BT2 ['outputVector_heatGenerationCoefficientDHW'].round(3)

            df_resultingProfiles_Preliminary_BT2.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT2_HH" + str(indexOfBuildingsOverall_BT2 [0] ) + ".csv" , index=True,  sep =";")


            return outputVector_heatGenerationCoefficientSpaceHeating, outputVector_heatGenerationCoefficientDHW


########################################################################################################################################
    if SetUpScenarios.numberOfBuildings_BT3 ==1:



            #Load trained ML method
            if usedDaySelectionMethod == 'Random':

                # Currently used features in method trainSupvervisedML_SinlgeTimeSlots: combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Outside Temperature [C]']]

                #Create vector with input features and scale it
                if objective == 'Min_Costs':


                    df_new = df_outsideTemperatureData
                    df_new['Availability of the EV'] = list_df_buildingData_BT3[index]['Availability of the EV'].values
                    df_new['PV [nominal]'] = list_df_buildingData_BT3[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT3 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Availability of the EV','Price [Cent/kWh]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                if objective == 'Min_SurplusEnergy':

                    df_new = df_outsideTemperatureData
                    df_new['Availability of the EV'] = list_df_buildingData_BT3[index]['Availability of the EV'].values
                    df_new['PV [nominal]'] = list_df_buildingData_BT3[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT3 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Availability of the EV'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    print(f"vector_input_features.shape: {vector_input_features.shape}")
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))

                if objective == 'Min_Peak':
                    df_new = df_outsideTemperatureData
                    df_new['Availability of the EV'] = list_df_buildingData_BT3[index]['Availability of the EV'].values
                    df_new['PV [nominal]'] = list_df_buildingData_BT3[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT3 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Availability of the EV'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    print(f"vector_input_features.shape: {vector_input_features.shape}")
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)

                vector_output_labels_scaled = vector_output_labels_scaled.reshape(SetUpScenarios.numberOfTimeSlotsPerDay, len(vector_output_labels_scaled [0][0]))
                vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)


            outputVector_chargingPowerEV =  vector_output_labels[:, 0]

            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT3 = pd.DataFrame({'outputVector_chargingPowerEV': outputVector_chargingPowerEV[:]})


            df_resultingProfiles_Preliminary_BT3 ['outputVector_chargingPowerEV'] = df_resultingProfiles_Preliminary_BT3 ['outputVector_chargingPowerEV'].round(3)

            df_resultingProfiles_Preliminary_BT3.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT3_HH" + str(indexOfBuildingsOverall_BT3 [0] ) + ".csv" , index=True,  sep =";")


            return  outputVector_chargingPowerEV






#######################################################################################################################################

    if SetUpScenarios.numberOfBuildings_BT4 ==1:

            #Calculate the COPs for the heat pump
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData["Temperature [C]"])
            df_copHeatPump =  pd.DataFrame({'Timeslot': list_df_buildingData_BT4 [0].index, 'COP_SpaceHeating':cop_heatPump_SpaceHeating, 'COP_DHW':cop_heatPump_DHW})


            #Load trained ML method
            if usedDaySelectionMethod == 'Random':

                # Currently used features in method trainSupvervisedML_SinlgeTimeSlots: combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Outside Temperature [C]']]

                #Create vector with input features and scale it
                if objective == 'Min_Costs':


                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT4[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT4 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Temperature [C]','Price [Cent/kWh]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                if objective == 'Min_SurplusEnergy':

                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT4[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT4 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Temperature [C]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray

                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))

                if objective == 'Min_Peak':
                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT4[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT4 [0] - 1)
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]','Temperature [C]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray

                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)

                vector_output_labels_scaled = vector_output_labels_scaled.reshape(SetUpScenarios.numberOfTimeSlotsPerDay, len(vector_output_labels_scaled [0][0]))
                vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)

            outputVector_heatGenerationCoefficientSpaceHeating =  vector_output_labels[:, 0]


            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT4 = pd.DataFrame({'outputVector_heatGenerationCoefficientSpaceHeating':outputVector_heatGenerationCoefficientSpaceHeating[:]})

            df_resultingProfiles_Preliminary_BT4 ['outputVector_heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_Preliminary_BT4 ['outputVector_heatGenerationCoefficientSpaceHeating'].round(3)
            df_resultingProfiles_Preliminary_BT4.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT4_HH" + str(indexOfBuildingsOverall_BT4 [0] ) + ".csv" , index=True,  sep =";")


            return outputVector_heatGenerationCoefficientSpaceHeating



########################################################################################################################################
    if SetUpScenarios.numberOfBuildings_BT5 ==1:


            #Load trained ML method
            if usedDaySelectionMethod == 'Random':

                # Currently used features in method trainSupvervisedML_SinlgeTimeSlots: combined_df[['timeslot', 'simulationResult_RESGeneration']]

                #Create vector with input features and scale it
                if objective == 'Min_Costs':

                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT5[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT5 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]', 'Price [Cent/kWh]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))

                if objective == 'Min_SurplusEnergy':

                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT5[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT5 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))

                if objective == 'Min_Peak':
                    df_new = df_outsideTemperatureData
                    df_new['PV [nominal]'] = list_df_buildingData_BT5[index]['PV [nominal]'].values * SetUpScenarios.determinePVPeakOfBuildings (indexOfBuildingsOverall_BT5 [0] - 1)
                    df_new['Price [Cent/kWh]'] = df_priceData['Price [Cent/kWh]'].values
                    df_new['timeslot'] = df_priceData.index

                    df_new = df_new.reindex([ 'timeslot', 'PV [nominal]'], axis=1)
                    numpyArray = df_new.to_numpy()
                    vector_input_features =  numpyArray
                    vector_input_features_scaled = dataScaler_InputFeatures.transform (vector_input_features )
                    vector_input_features_scaled = np.reshape(vector_input_features_scaled, (1, SetUpScenarios.numberOfTimeSlotsPerDay, len(numpyArray[0])))


                vector_output_labels_scaled = trainedModel.predict(vector_input_features_scaled)

                vector_output_labels_scaled = vector_output_labels_scaled.reshape(SetUpScenarios.numberOfTimeSlotsPerDay, len(vector_output_labels_scaled [0][0]))
                vector_output_labels = dataScaler_OutputLabels.inverse_transform (vector_output_labels_scaled)

            outputVector_chargingBATCombinedVariable =  vector_output_labels[:, 0]

            outputVector_chargingBAT = np.zeros(len(outputVector_chargingBATCombinedVariable))
            outputVector_disChargingBAT = np.zeros(len(outputVector_chargingBATCombinedVariable))

            for i in range (0, len(outputVector_chargingBAT)):
                if outputVector_chargingBATCombinedVariable [i] >= 0:
                    outputVector_chargingBAT [i] = outputVector_chargingBATCombinedVariable [i]
                else:
                    outputVector_disChargingBAT [i] = outputVector_chargingBATCombinedVariable [i] *(-1)


            #Print the preliminary results
            df_resultingProfiles_Preliminary_BT5 = pd.DataFrame({'outputVector_chargingBAT':outputVector_chargingBAT[:],'outputVector_disChargingBAT': outputVector_disChargingBAT[:]})

            df_resultingProfiles_Preliminary_BT5 ['outputVector_chargingBAT'] = df_resultingProfiles_Preliminary_BT5 ['outputVector_chargingBAT'].round(3)
            df_resultingProfiles_Preliminary_BT5 ['outputVector_disChargingBAT'] = df_resultingProfiles_Preliminary_BT5 ['outputVector_disChargingBAT'].round(3)

            df_resultingProfiles_Preliminary_BT5.to_csv(pathForCreatingTheResultData_ANN + "/Preliminary_BT5_HH" + str(indexOfBuildingsOverall_BT5 [0] ) + ".csv" , index=True,  sep =";")


            return outputVector_chargingBAT, outputVector_disChargingBAT






def trainSupervisedML_SingleTimeslot_SingleBuildingOptScenario (trainingData, objective, useNormalizedData, useStandardizedData, usedMLMethod, dayClusterName, pathForTheTrainedModels, practiseModeWithTestPredictions):
    from random import randrange
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_absolute_percentage_error
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import backend as K
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.model_selection import train_test_split
    from matplotlib import pyplot as plt

    numberOfTrainingDays = len(trainingData) * len(trainingData[0])


    if SetUpScenarios.numberOfBuildings_BT1 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT1/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT1/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV', 'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW', 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT1/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT1/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV', 'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW', 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT1/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT1/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV', 'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW', 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT2 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT2/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT2/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs','COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT2/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT2/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT2/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT2/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            # Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT3 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT3/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT3/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot',  'simulationResult_SOCofEV', 'simulationResult_RESGeneration',  'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]']]
            MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_SOCofEV', 'simulationResult_RESGeneration',  'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]']]
            MLSupervised_output_data = combined_df[['chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT3/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT3/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot',  'simulationResult_SOCofEV', 'simulationResult_RESGeneration',  'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]' ]]
            MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]']]
            MLSupervised_output_data = combined_df[[ 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT3/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT3/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]']]
            MLSupervised_output_data = combined_df[[ 'chargingPowerEV']]


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT4 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT4/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT4/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'COP (Space Heating)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'simulationResult_RESGeneration', 'Space Heating [W]',  'Electricity [W]',  'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage', 'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT4/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT4/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            #Choose input feature from ['timeslot', 'temperatureBufferStorage','simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage',  'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT4/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT4/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)
            MLSupvervised_input_data = combined_df[['timeslot', 'temperatureBufferStorage',  'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT5 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT5/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT5/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            # timeslot		chargingPowerBAT	disChargingPowerBAT	simulationResult_SOCofBAT simulationResult_RESGeneration	simulationResult_electricalLoad	simulationResult_SurplusPower	simulationResult_costs	Electricity [W]	Outside Temperature [C]	Price [Cent/kWh]

            MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofBAT', 'simulationResult_RESGeneration',  'Electricity [W]',  'Outside Temperature [C]']]
            MLSupervised_output_data = combined_df[['chargingPowerBAT', 'disChargingPowerBAT']]

            #Create a combined variable as output label
            array_ChargingPowerBat = MLSupervised_output_data['chargingPowerBAT'].to_numpy()
            array_disChargingPowerBat = MLSupervised_output_data['disChargingPowerBAT'].to_numpy()
            array_chargingPowerBatCombinedVariable = np.zeros(len(array_disChargingPowerBat))
            for i in range (0, len(array_disChargingPowerBat)):
                if array_ChargingPowerBat [i] >= array_disChargingPowerBat [i]:
                    array_chargingPowerBatCombinedVariable [i] = array_ChargingPowerBat [i]
                else:
                    array_chargingPowerBatCombinedVariable[i] = array_disChargingPowerBat[i] * (-1)
            MLSupervised_output_data_combinedVariable = pd.DataFrame(array_chargingPowerBatCombinedVariable, columns=['chargingPowerBATcombinedVariable'])


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data_combinedVariable.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT5/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT5/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            # timeslot		chargingPowerBAT	disChargingPowerBAT	simulationResult_SOCofBAT	simulationResult_energyLevelOfBAT		simulationResult_RESGeneration	simulationResult_electricalLoad	simulationResult_SurplusPower	simulationResult_costs	Electricity [W]	Outside Temperature [C]	Price [Cent/kWh]

            MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofBAT', 'simulationResult_RESGeneration',  'Electricity [W]',  'Outside Temperature [C]']]
            MLSupervised_output_data = combined_df[['chargingPowerBAT', 'disChargingPowerBAT']]

            #Create a combined variable as output label
            array_ChargingPowerBat = MLSupervised_output_data['chargingPowerBAT'].to_numpy()
            array_disChargingPowerBat = MLSupervised_output_data['disChargingPowerBAT'].to_numpy()
            array_chargingPowerBatCombinedVariable = np.zeros(len(array_disChargingPowerBat))
            for i in range (0, len(array_disChargingPowerBat)):
                if array_ChargingPowerBat [i] >= array_disChargingPowerBat [i]:
                    array_chargingPowerBatCombinedVariable [i] = array_ChargingPowerBat [i]
                else:
                    array_chargingPowerBatCombinedVariable[i] = array_disChargingPowerBat[i] * (-1)
            MLSupervised_output_data_combinedVariable = pd.DataFrame(array_chargingPowerBatCombinedVariable, columns=['chargingPowerBATcombinedVariable'])


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data_combinedVariable.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT5/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT5/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")
                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])
            combined_df = combined_df.sample(frac = 1)

            # timeslot		chargingPowerBAT	disChargingPowerBAT	simulationResult_SOCofBAT	simulationResult_energyLevelOfBAT		simulationResult_RESGeneration	simulationResult_electricalLoad	simulationResult_SurplusPower	simulationResult_costs	Electricity [W]	Outside Temperature [C]	Price [Cent/kWh]

            MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_SOCofBAT', 'simulationResult_RESGeneration',  'Electricity [W]',  'Outside Temperature [C]', 'Price [Cent/kWh]']]
            MLSupervised_output_data = combined_df[['chargingPowerBAT', 'disChargingPowerBAT']]

            #Create a combined variable as output label
            array_ChargingPowerBat = MLSupervised_output_data['chargingPowerBAT'].to_numpy()
            array_disChargingPowerBat = MLSupervised_output_data['disChargingPowerBAT'].to_numpy()
            array_chargingPowerBatCombinedVariable = np.zeros(len(array_disChargingPowerBat))
            for i in range (0, len(array_disChargingPowerBat)):
                if array_ChargingPowerBat [i] >= array_disChargingPowerBat [i]:
                    array_chargingPowerBatCombinedVariable [i] = array_ChargingPowerBat [i]
                else:
                    array_chargingPowerBatCombinedVariable[i] = array_disChargingPowerBat[i] * (-1)
            MLSupervised_output_data_combinedVariable = pd.DataFrame(array_chargingPowerBatCombinedVariable, columns=['chargingPowerBATcombinedVariable'])


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data_combinedVariable.values



    # standardize or normalize data
    if useNormalizedData==True:
        scaler_minmax_X = MinMaxScaler()
        MLSupvervised_input_data = scaler_minmax_X.fit_transform(MLSupvervised_input_data)

        scaler_minmax_Y = MinMaxScaler()
        MLSupervised_output_data = scaler_minmax_Y.fit_transform(MLSupervised_output_data)

        dataScaler_InputFeatures = scaler_minmax_X
        dataScaler_OutputLabels = scaler_minmax_Y

    if useStandardizedData==True:
        scaler_standardized_X = StandardScaler()
        MLSupvervised_input_data = scaler_standardized_X.fit_transform(MLSupvervised_input_data)

        scaler_standardized_Y = StandardScaler()
        MLSupervised_output_data = scaler_standardized_Y.fit_transform(MLSupervised_output_data)

        dataScaler_InputFeatures = scaler_standardized_X
        dataScaler_OutputLabels = scaler_standardized_Y


    index_X_Train_End = int(0.7 * len(MLSupvervised_input_data))
    index_X_Validation_End = int(0.9 * len(MLSupvervised_input_data))

    if practiseModeWithTestPredictions==False:
        index_X_Validation_End = int(1.0 * len(MLSupvervised_input_data))

    X_train = MLSupvervised_input_data [0: index_X_Train_End]
    X_valid = MLSupvervised_input_data [index_X_Train_End: index_X_Validation_End]
    X_test = MLSupvervised_input_data [index_X_Validation_End:]

    Y_train = MLSupervised_output_data [0: index_X_Train_End]
    Y_valid = MLSupervised_output_data [index_X_Train_End: index_X_Validation_End]
    Y_test = MLSupervised_output_data [index_X_Validation_End:]


    #Train the model
    optimizer_adam = tf.keras.optimizers.Adam(learning_rate= 0.001)

    numberOfInputFeatures = len(MLSupvervised_input_data[0])
    numberOfOutputNeurons = len(MLSupervised_output_data[0])

    #Train a Mulit Layer Perceptron
    if usedMLMethod == 'Multi_Layer_Perceptron' :

        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(numberOfInputFeatures,)),
            keras.layers.Dense(30, activation='relu'),
            keras.layers.Dense(50, activation='relu'),
            keras.layers.Dense(50, activation='relu'),
            keras.layers.Dense(10, activation='relu'),
            keras.layers.Dense(numberOfOutputNeurons, activation='relu')])

        pathOfTheFileForBestModel = pathForTheTrainedModels + "bestModelSingleTimeSlot_MLP" + dayClusterName + ".keras"
        callbacks = [  keras.callbacks.ModelCheckpoint(pathOfTheFileForBestModel,  save_best_only=True) ]

        model.compile(loss="mean_squared_error", optimizer=optimizer_adam, metrics=['mean_absolute_percentage_error'])
        history = model.fit(X_train, Y_train, epochs=5, batch_size=50, validation_data=(X_valid, Y_valid), callbacks=callbacks)

        # Predict the values from the test dataset
        model_best = keras.models.load_model(pathOfTheFileForBestModel)

        if practiseModeWithTestPredictions == True:
            Y_pred = model_best.predict(X_test)


    #Train a Random Forest
    if usedMLMethod == 'Random_Forest' :
        print("Called Random_Forest")
        import sklearn
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import cross_val_score
        from sklearn.model_selection import RepeatedKFold
        from sklearn.metrics import mean_squared_error
        X_train_valid = np.concatenate((X_train, X_valid))
        Y_train_valid = np.concatenate((Y_train, Y_valid))

        if SetUpScenarios.numberOfBuildings_BT3 ==1 or SetUpScenarios.numberOfBuildings_BT4 ==1 or SetUpScenarios.numberOfBuildings_BT5 ==1:
            Y_train_valid = Y_train_valid.ravel()

        # define the model
        changingParameter_max_samples = [ 1]
        changingParameter_max_features = [0.4,    1]
        changingParameter_n_estimators = [ 1000]
        changingParameter_max_depth =  [  3, None]
        numberOfDifferentConfigurations = len(changingParameter_max_samples) * len(changingParameter_max_features) * len(changingParameter_n_estimators) * len(changingParameter_max_depth)

        currentBestParameter_max_samples = -1
        currentBestParameter_max_features = -1
        currentBestParameter_n_estimators= -1
        currentBestParameter_max_depth = -1
        currentBestRMSE = 999999999

        rmse_forEachConfiguration = np.zeros(numberOfDifferentConfigurations )
        currentIndexLoop = 0


        #Loop for hyperparameter tuning on the validation dataset
        for max_samples_iteration in changingParameter_max_samples:
            for max_features_iteration in changingParameter_max_features:
                for n_estimators_iteration in changingParameter_n_estimators:
                    for max_depth_iteration in changingParameter_max_depth:

                        print(f"Run {currentIndexLoop + 1} from {numberOfDifferentConfigurations}")
                        model = RandomForestRegressor(n_estimators=n_estimators_iteration, max_samples=max_samples_iteration, max_features=max_features_iteration, criterion='squared_error', max_depth = max_depth_iteration )


                        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
                        n_scores = cross_val_score(model, X_train_valid, Y_train_valid, scoring='neg_mean_squared_error', cv=cv, n_jobs=-1, error_score='raise')
                        mean_rmse = round(n_scores.mean() * (-1), 3)
                        print(f"mean_rmse: {mean_rmse}")


                        #Check if the current configuration is better then the previously best configuration
                        if currentBestRMSE > mean_rmse:
                            currentBestRMSE = mean_rmse
                            currentBestParameter_max_samples = max_samples_iteration
                            currentBestParameter_max_features = max_features_iteration
                            currentBestParameter_n_estimators = n_estimators_iteration
                            currentBestParameter_max_depth = max_depth_iteration
                            bestTrainedModel = model
                        currentIndexLoop+=1
                        print("")

                        if currentIndexLoop == numberOfDifferentConfigurations:
                            #Print best results
                            print(f"Best Configuration")
                            print(f"currentBestParameter_max_samples: {currentBestParameter_max_samples}")
                            print(f"currentBestParameter_max_features: {currentBestParameter_max_features}")
                            print(f"currentBestParameter_n_estimators: {currentBestParameter_n_estimators}")
                            print(f"currentBestParameter_max_depth: {currentBestParameter_max_depth}")
                            print(f"currentBestRMSE: {currentBestRMSE}")

                            #Train tree with default values
                            model_default = RandomForestRegressor( )
                            cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
                            n_scores = cross_val_score(model_default, X_train_valid, Y_train_valid, scoring='neg_mean_squared_error', cv=cv, n_jobs=-1, error_score='raise')
                            mean_rmse_default = round(n_scores.mean() * (-1), 3)
                            print(f"mean_rmse Default: {mean_rmse_default}")
                            print(f"")


        #Check if the default configuration is best
        defaultConfigurationIsBest = False
        if mean_rmse_default <= currentBestRMSE:
            model_best = model_default
            defaultConfigurationIsBest = True
        else:
            model_best = RandomForestRegressor(n_estimators=currentBestParameter_n_estimators, max_samples=currentBestParameter_max_samples, max_features=currentBestParameter_max_features, criterion='squared_error', max_depth = currentBestParameter_max_depth )

        #Fit the model
        model_best.fit(X_train_valid, Y_train_valid)

        #predict the test data with the best configuration if desired:
        if practiseModeWithTestPredictions == True:
            Y_pred = model_best.predict(X_test)


        #Print best configuration of the random forest into a file
        import csv
        with open(pathForTheTrainedModels + 'Random_Forest_Best_Configuration_' + dayClusterName + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["currentBestParameter_max_samples", "currentBestParameter_max_features", "currentBestParameter_n_estimators", "currentBestParameter_max_depth", "Default config is best?"])
            writer.writerow([currentBestParameter_max_samples, currentBestParameter_max_features, currentBestParameter_n_estimators, currentBestParameter_max_depth, defaultConfigurationIsBest])


    if usedMLMethod == 'Gradient_Boosting' :
        import sklearn
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.model_selection import cross_val_score
        from sklearn.model_selection import RepeatedKFold
        from sklearn.metrics import mean_squared_error
        from sklearn.multioutput import MultiOutputRegressor

        X_train_valid = np.concatenate((X_train, X_valid))
        Y_train_valid = np.concatenate((Y_train, Y_valid))

        # define the model
        useHistogramBasedRegressor = False
        changingParameter_learning_rate = [0.1,  0.3]
        changingParameter_max_features = [0.2,    1]
        changingParameter_n_estimators = [100]
        changingParameter_max_depth =  [  7, None]
        numberOfDifferentConfigurations = len(changingParameter_learning_rate) * len(changingParameter_max_features) * len(changingParameter_n_estimators) * len(changingParameter_max_depth)

        currentBestParameter_learning_rate = -1
        currentBestParameter_max_features = -1
        currentBestParameter_n_estimators= -1
        currentBestParameter_max_depth = -1
        currentBestRMSE = 999999999

        rmse_forEachConfiguration = np.zeros(numberOfDifferentConfigurations )
        currentIndexLoop = 0


        #Loop for hyperparameter tuning on the validation dataset
        for learning_rate in changingParameter_learning_rate:
            for max_features_iteration in changingParameter_max_features:
                for n_estimators_iteration in changingParameter_n_estimators:
                    for max_depth_iteration in changingParameter_max_depth:

                        print(f"Run {currentIndexLoop + 1} from {numberOfDifferentConfigurations}")

                        model = MultiOutputRegressor(GradientBoostingRegressor(learning_rate = learning_rate, n_estimators=n_estimators_iteration,  max_features=max_features_iteration,  max_depth = max_depth_iteration ))

                        #Fit the model
                        #model.fit(X_train_valid, Y_train_valid)

                        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
                        n_scores = cross_val_score(model, X_train_valid, Y_train_valid, scoring='neg_mean_squared_error', cv=cv, n_jobs=-1, error_score='raise')
                        mean_rmse = round(n_scores.mean() * (-1), 3)
                        print(f"mean_rmse: {mean_rmse}")


                        #Check if the current configuration is better then the previously best configuration
                        if currentBestRMSE > mean_rmse:
                            currentBestRMSE = mean_rmse
                            currentBestParameter_learning_rate = learning_rate
                            currentBestParameter_max_features = max_features_iteration
                            currentBestParameter_n_estimators = n_estimators_iteration
                            currentBestParameter_max_depth = max_depth_iteration
                            bestTrainedModel = model
                        currentIndexLoop+=1
                        print("")

                        if currentIndexLoop == numberOfDifferentConfigurations:
                            #Print best results
                            print(f"Best Configuration")
                            print(f"currentBestParameter_learning_rate: {currentBestParameter_learning_rate}")
                            print(f"currentBestParameter_max_features: {currentBestParameter_max_features}")
                            print(f"currentBestParameter_n_estimators: {currentBestParameter_n_estimators}")
                            print(f"currentBestParameter_max_depth: {currentBestParameter_max_depth}")
                            print(f"currentBestRMSE: {currentBestRMSE}")

                            #Train tree with default values
                            model_default = MultiOutputRegressor(GradientBoostingRegressor())
                            cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
                            n_scores = cross_val_score(model_default, X_train_valid, Y_train_valid, scoring='neg_mean_squared_error', cv=cv, n_jobs=-1, error_score='raise')
                            mean_rmse_default = round(n_scores.mean() * (-1), 3)
                            print(f"mean_rmse Default: {mean_rmse}")
                            print(f"")


        #check if the default configuration is best
        defaultConfigurationIsBest = False
        if mean_rmse_default <= currentBestRMSE:
            defaultConfigurationIsBest = True
            model_best = model_default
        else:
            model_best = MultiOutputRegressor(GradientBoostingRegressor(learning_rate=currentBestParameter_learning_rate,  max_features=currentBestParameter_max_features, max_depth = currentBestParameter_max_depth ))

        #Train the model
        model_best.fit(X_train_valid, Y_train_valid)

        #predict the test data with the best configuration if desired:
        if practiseModeWithTestPredictions == True:
            model_best.fit(X_train_valid, Y_train_valid)
            Y_pred = model_best.predict(X_test)


        #Print best configuration to file
        import csv
        with open(pathForTheTrainedModels + 'Gradient_Boosting_Best_Configuration_' + dayClusterName+ '.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["currentBestParameter_learning_rate", "currentBestParameter_max_features", "currentBestParameter_n_estimators", "currentBestParameter_max_depth", "Default config is best?"])
            writer.writerow([currentBestParameter_learning_rate, currentBestParameter_max_features, currentBestParameter_n_estimators, str(currentBestParameter_max_depth), defaultConfigurationIsBest])


    # Rescale the results of the predictions in the test dataset if desired
    if practiseModeWithTestPredictions == True:
        Y_test_traInv = -1
        Y_pred_traInv = -1
        if useStandardizedData==True:
            if SetUpScenarios.numberOfBuildings_BT3 == 1 or SetUpScenarios.numberOfBuildings_BT4 ==1:
                Y_test_traInv = scaler_standardized_Y.inverse_transform(Y_test.reshape(-1,1))
                Y_pred_traInv = scaler_standardized_Y.inverse_transform(Y_pred.reshape(-1,1))
            else:
                Y_test_traInv = scaler_standardized_Y.inverse_transform(Y_test)
                Y_pred_traInv = scaler_standardized_Y.inverse_transform(Y_pred)

        if useNormalizedData==True:
            if SetUpScenarios.numberOfBuildings_BT3 == 1 or SetUpScenarios.numberOfBuildings_BT4 ==1:
                Y_test_traInv = scaler_minmax_Y.inverse_transform(Y_test.reshape(-1,1))
                Y_pred_traInv = scaler_minmax_Y.inverse_transform(Y_pred.reshape(-1,1))
            else:
                Y_test_traInv = scaler_minmax_Y.inverse_transform(Y_test)
                Y_pred_traInv = scaler_minmax_Y.inverse_transform(Y_pred)


        #  Calculate the error in the test dataset
        if useStandardizedData == True or useNormalizedData == True:
            rms = mean_squared_error(Y_test_traInv, Y_pred_traInv, squared=True)
            mape = mean_absolute_percentage_error(Y_test_traInv, Y_pred_traInv)

            print()
            print()
            print("Evaluation with the test data")
            print("Root Mean Squarred Error: ", rms)
            print("Mean Absolute Percentage Error:", mape)
            print()

        #Plot training results
        if usedMLMethod == 'Multi_Layer_Perceptron':
            plt.plot(history.history['mean_absolute_percentage_error'])
            plt.plot(history.history['val_mean_absolute_percentage_error'])
            plt.title('Mean absolute percentage error')
            plt.ylabel('Mean absolute percentage error')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            filename = pathForTheTrainedModels + "\Training_Results_MAPE.png"
            plt.savefig(filename, bbox_inches='tight', dpi=150)
            plt.clf()

            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('Loss function')
            plt.ylabel('Mean squared Error')
            plt.xlabel('epoch')
            plt.legend(['train', 'val'], loc='upper left')
            filename = pathForTheTrainedModels + "\Training_Results_MSE.png"
            plt.savefig(filename, bbox_inches='tight', dpi=150)
            plt.clf()

    return dataScaler_InputFeatures, dataScaler_OutputLabels, model_best

    #return MLSupvervised_input_data, MLSupervised_output_data, X_train, X_valid, X_test, Y_train, Y_valid, Y_test, Y_pred_traInv, Y_test_traInv



def trainRNN_MultipleTimeslot_SingleBuildingOptScenario (trainingData, objective, useNormalizedData, useStandardizedData, usedMLMethod, dayClusterName, practiseModeWithTestPredictions, perfectForecast):
    from random import randrange
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_absolute_percentage_error
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import backend as K
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.model_selection import train_test_split

    from matplotlib import pyplot as plt

    numberOfTrainingDays = len(trainingData) * len(trainingData[0])

    entireFolderNameForTheResultsOfTheRun = "C:/Users/wi9632/Desktop/Ergebnisse/DSM/ML Training Configurations/RNN/"


    #Read the training data
    if SetUpScenarios.numberOfBuildings_BT1 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT1/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT1/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV', 'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Outside Temperature [C]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW', 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT1/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT1/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV', 'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])


            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_SOCofEV', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Outside Temperature [C]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW', 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT1/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT1/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT1_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT1_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV', 'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW', 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT2 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT2/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT2/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs','COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Outside Temperature [C]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT2/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT2/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Outside Temperature [C]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT2/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT2/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT2_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT2_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)', 'COP (DHW)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            # Choose input feature from ['timeslot', 'temperatureBufferStorage', 'usableVolumeDHWTank', 'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Outside Temperature [C]', 'Price [Cent/kWh]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Outside Temperature [C]', 'Price [Cent/kWh]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating', 'heatGenerationCoefficientDHW']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT3 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT3/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT3/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot',  'simulationResult_SOCofEV', 'simulationResult_RESGeneration',  'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration',  'Availability of the EV']]

            MLSupervised_output_data = combined_df[['chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT3/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT3/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot',  'simulationResult_SOCofEV', 'simulationResult_RESGeneration',  'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]' ]]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration',  'Availability of the EV']]

            MLSupervised_output_data = combined_df[[ 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT3/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT3/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT3_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT3_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_energyLevelOfEV', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs', 'Energy Consumption of the EV'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Availability of the EV', 'Price [Cent/kWh]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration',  'Availability of the EV', 'Price [Cent/kWh]']]

            MLSupervised_output_data = combined_df[[ 'chargingPowerEV']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT4 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT4/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT4/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'COP (Space Heating)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot', 'temperatureBufferStorage', 'simulationResult_RESGeneration', 'Space Heating [W]',  'Electricity [W]',  'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Outside Temperature [C]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT4/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT4/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            #Choose input feature from ['timeslot', 'temperatureBufferStorage','simulationResult_RESGeneration', 'Space Heating [W]', 'DHW [W]', 'Electricity [W]', 'Availability of the EV', 'Outside Temperature [C]', 'Price [Cent/kWh]', 'numberOfStarts_HP', 'HP_isRunning']]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Outside Temperature [C]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT4/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT4/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT4_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT4_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day', 'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs',  'COP (Space Heating)'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration',  'Outside Temperature [C]', 'Price [Cent/kWh]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Space Heating [W]', 'Electricity [W]',  'Outside Temperature [C]', 'Price [Cent/kWh]']]

            MLSupervised_output_data = combined_df[['heatGenerationCoefficientSpaceHeating']]

            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data.values


    if SetUpScenarios.numberOfBuildings_BT5 ==1:
        df_collection_trainingDays = {}
        if objective == "Min_SurplusEnergy":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT5/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT5/Min_Surplus_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            # timeslot		chargingPowerBAT	disChargingPowerBAT	simulationResult_SOCofBAT simulationResult_RESGeneration	simulationResult_electricalLoad	simulationResult_SurplusPower	simulationResult_costs	Electricity [W]	Outside Temperature [C]	Price [Cent/kWh]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Electricity [W]']]

            MLSupervised_output_data = combined_df[['chargingPowerBAT', 'disChargingPowerBAT']]

            #Create a combined variable as output label
            array_ChargingPowerBat = MLSupervised_output_data['chargingPowerBAT'].to_numpy()
            array_disChargingPowerBat = MLSupervised_output_data['disChargingPowerBAT'].to_numpy()
            array_chargingPowerBatCombinedVariable = np.zeros(len(array_disChargingPowerBat))
            for i in range (0, len(array_disChargingPowerBat)):
                if array_ChargingPowerBat [i] >= array_disChargingPowerBat [i]:
                    array_chargingPowerBatCombinedVariable [i] = array_ChargingPowerBat [i]
                else:
                    array_chargingPowerBatCombinedVariable[i] = array_disChargingPowerBat[i] * (-1)
            MLSupervised_output_data_combinedVariable = pd.DataFrame(array_chargingPowerBatCombinedVariable, columns=['chargingPowerBATcombinedVariable'])


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data_combinedVariable.values

        if objective == "Min_Peak":
            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT5/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT5/Min_Peak_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")

                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            # timeslot		chargingPowerBAT	disChargingPowerBAT	simulationResult_SOCofBAT	simulationResult_energyLevelOfBAT		simulationResult_RESGeneration	simulationResult_electricalLoad	simulationResult_SurplusPower	simulationResult_costs	Electricity [W]	Outside Temperature [C]	Price [Cent/kWh]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Electricity [W]']]

            MLSupervised_output_data = combined_df[['chargingPowerBAT', 'disChargingPowerBAT']]

            #Create a combined variable as output label
            array_ChargingPowerBat = MLSupervised_output_data['chargingPowerBAT'].to_numpy()
            array_disChargingPowerBat = MLSupervised_output_data['disChargingPowerBAT'].to_numpy()
            array_chargingPowerBatCombinedVariable = np.zeros(len(array_disChargingPowerBat))
            for i in range (0, len(array_disChargingPowerBat)):
                if array_ChargingPowerBat [i] >= array_disChargingPowerBat [i]:
                    array_chargingPowerBatCombinedVariable [i] = array_ChargingPowerBat [i]
                else:
                    array_chargingPowerBatCombinedVariable[i] = array_disChargingPowerBat[i] * (-1)
            MLSupervised_output_data_combinedVariable = pd.DataFrame(array_chargingPowerBatCombinedVariable, columns=['chargingPowerBATcombinedVariable'])


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data_combinedVariable.values

        if objective == "Min_Costs":

            #Choos the training data days and building from the input array trainingData
            help_currentNumberOfTrainingDays= 0
            for indexBuilding in range (0, len(trainingData)):
               for indexTrainingDay in range (0, len(trainingData[0])):

                    #Read the training data
                    if SetUpScenarios.alternativeCaseScenario == True:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/A_Scenario/BT5/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"
                    if SetUpScenarios.alternativeCaseScenario == False:
                        pathForTrainingData = f"C:/Users/wi9632/Desktop/Daten/DSM/Training_Data/OptNoTargets/B_Scenario/BT5/Min_Costs_{SetUpScenarios.typeOfPriceData}_PV_{int(SetUpScenarios.averagePVPeak/1000)}kWp_{SetUpScenarios.timeResolution_InMinutes}Min/BT5_HH" + str(indexBuilding + 1)  + "/Day" + str(trainingData [indexBuilding][indexTrainingDay] + 1 ) + "/BT5_HH1.csv"

                    df_collection_trainingDays [help_currentNumberOfTrainingDays] = pd.read_csv(pathForTrainingData, sep=";")
                    df_collection_trainingDays[help_currentNumberOfTrainingDays].drop(['time of day',  'simulationResult_PVGeneration', 'simulationResult_electricalLoad', 'simulationResult_SurplusPower' , 'simulationResult_costs'], axis=1, inplace=True)
                    help_currentNumberOfTrainingDays += 1


            #Prepare the input data
            combined_df = pd.concat( [df_collection_trainingDays[indexTrainingDay] for indexTrainingDay in range (0, numberOfTrainingDays)])

            # timeslot		chargingPowerBAT	disChargingPowerBAT	simulationResult_SOCofBAT	simulationResult_energyLevelOfBAT		simulationResult_RESGeneration	simulationResult_electricalLoad	simulationResult_SurplusPower	simulationResult_costs	Electricity [W]	Outside Temperature [C]	Price [Cent/kWh]
            if perfectForecast == False:
                MLSupvervised_input_data = combined_df[['timeslot', 'simulationResult_RESGeneration', 'Price [Cent/kWh]']]
            if perfectForecast == True:
                MLSupvervised_input_data = combined_df[['timeslot',  'simulationResult_RESGeneration', 'Electricity [W]', 'Price [Cent/kWh]']]

            MLSupervised_output_data = combined_df[['chargingPowerBAT', 'disChargingPowerBAT']]

            #Create a combined variable as output label
            array_ChargingPowerBat = MLSupervised_output_data['chargingPowerBAT'].to_numpy()
            array_disChargingPowerBat = MLSupervised_output_data['disChargingPowerBAT'].to_numpy()
            array_chargingPowerBatCombinedVariable = np.zeros(len(array_disChargingPowerBat))
            for i in range (0, len(array_disChargingPowerBat)):
                if array_ChargingPowerBat [i] >= array_disChargingPowerBat [i]:
                    array_chargingPowerBatCombinedVariable [i] = array_ChargingPowerBat [i]
                else:
                    array_chargingPowerBatCombinedVariable[i] = array_disChargingPowerBat[i] * (-1)
            MLSupervised_output_data_combinedVariable = pd.DataFrame(array_chargingPowerBatCombinedVariable, columns=['chargingPowerBATcombinedVariable'])


            MLSupvervised_input_data = MLSupvervised_input_data.values
            MLSupervised_output_data = MLSupervised_output_data_combinedVariable.values

    ANN_input_data = MLSupvervised_input_data
    ANN_output_data = MLSupervised_output_data

    numberOfInputFeatures = len(ANN_input_data[0])
    numberOfOutputNeurons = len(ANN_output_data[0])



    # standardize or normalize data
    if useNormalizedData==True:
        scaler_minmax_X = MinMaxScaler()
        print(f"ANN_input_data.shape: {ANN_input_data.shape}")
        ANN_input_data = scaler_minmax_X.fit_transform(ANN_input_data)

        scaler_minmax_Y = MinMaxScaler()
        ANN_output_data = scaler_minmax_Y.fit_transform(ANN_output_data)

        dataScaler_InputFeatures = scaler_minmax_X
        dataScaler_OutputLabels = scaler_minmax_Y


    if useStandardizedData==True:
        scaler_standardized_X = StandardScaler()
        print(f"ANN_input_data.shape: {ANN_input_data.shape}")
        ANN_input_data = scaler_standardized_X.fit_transform(ANN_input_data)

        scaler_standardized_Y = StandardScaler()
        ANN_output_data = scaler_standardized_Y.fit_transform(ANN_output_data)

        dataScaler_InputFeatures = scaler_standardized_X
        dataScaler_OutputLabels = scaler_standardized_Y


    #create multidimensional array
    multidimensional_df_input =np.array_split(ANN_input_data,numberOfTrainingDays)
    multidimensional_array_input = np.stack(multidimensional_df_input)
    multidimensional_df_output =np.array_split(ANN_output_data,numberOfTrainingDays)
    multidimensional_array_output = np.stack(multidimensional_df_output)


    ANN_input_data = multidimensional_array_input
    ANN_output_data = multidimensional_array_output




    #Create training, validation and test datasets
    index_X_Train_End = int(0.7 * len(ANN_input_data))
    index_X_Validation_End = int(0.9 * len(ANN_input_data))
    if practiseModeWithTestPredictions==False:
        index_X_Validation_End = int(1.0 * len(MLSupvervised_input_data))


    X_train = ANN_input_data [0: index_X_Train_End]
    X_valid = ANN_input_data [index_X_Train_End: index_X_Validation_End]
    X_test = ANN_input_data [index_X_Validation_End:]

    Y_train = ANN_output_data [0: index_X_Train_End]
    Y_valid = ANN_output_data [index_X_Train_End: index_X_Validation_End]
    Y_test = ANN_output_data [index_X_Validation_End:]



    # Build the model and train it
    optimizer_adam = tf.keras.optimizers.Adam(lr= 0.001)

    if usedMLMethod=="RNN":

        model = keras.models.Sequential([
            keras.layers.SimpleRNN(10, return_sequences=True, input_shape=[None, numberOfInputFeatures]),
            keras.layers.SimpleRNN(10, return_sequences=True),
            keras.layers.Dense(numberOfOutputNeurons)
            ])


    if usedMLMethod=="LSTM":
        model = keras.models.Sequential([
            keras.layers.LSTM(10, return_sequences=True, input_shape=[None, numberOfInputFeatures]),
            keras.layers.LSTM(10, return_sequences=True),
            keras.layers.TimeDistributed(keras.layers.Dense(numberOfOutputNeurons))
            ])



    pathOfTheFileForBestModel = entireFolderNameForTheResultsOfTheRun + "bestModelMultipleTimeSlots_"+ usedMLMethod +".keras"
    callbacks = [  keras.callbacks.ModelCheckpoint(pathOfTheFileForBestModel,  save_best_only=True) ]


    model.compile(loss="mean_squared_error", optimizer=optimizer_adam, metrics=['mean_absolute_percentage_error'])
    history = model.fit(X_train, Y_train, epochs=5, batch_size=5, validation_data=(X_valid, Y_valid), callbacks=callbacks)

    # Predict the values from the test dataset if desired
    model_best = keras.models.load_model(pathOfTheFileForBestModel)
    if practiseModeWithTestPredictions == True:
        Y_pred = model_best.predict(X_test)
        print(f"X_test.shape: {X_test.shape}")
        print(f"Y_pred.shape: {Y_pred.shape}")

    # Rescale the results of the predictions in the test dataset
        Y_test_scaled = Y_test
        Y_pred_scaled = Y_pred

        if useStandardizedData==True:
            Y_test_2dimensional = scaler_standardized_Y.inverse_transform(Y_test.reshape(-1,numberOfOutputNeurons))
            Y_test =  Y_test_2dimensional.reshape((Y_test.shape[0], Y_test.shape[1], numberOfOutputNeurons))
            Y_pred_2dimensional = scaler_standardized_Y.inverse_transform(Y_pred.reshape(-1,numberOfOutputNeurons))
            Y_pred =  Y_pred_2dimensional.reshape((Y_pred.shape[0], Y_pred.shape[1], numberOfOutputNeurons))


        if useNormalizedData==True:

            Y_test_2dimensional = scaler_minmax_Y.inverse_transform(Y_test.reshape(-1,numberOfOutputNeurons))
            Y_test =  Y_test_2dimensional.reshape((Y_test.shape[0], Y_test.shape[1], numberOfOutputNeurons))
            Y_pred_2dimensional = scaler_minmax_Y.inverse_transform(Y_pred.reshape(-1,numberOfOutputNeurons))
            Y_pred =  Y_pred_2dimensional.reshape((Y_pred.shape[0], Y_pred.shape[1], numberOfOutputNeurons))






        # Calculate errors for every time slot of the multiple predictions

        abs_diff = np.abs(Y_pred - Y_test)
        abs_diff_perPredictedSequence = np.zeros((len (Y_test)))
        average_LoadValue_testData_perPredictedSequence = np.zeros((len (Y_test)))
        abs_diff_perPredictedTimeslot_ForEachSequence = np.zeros((len (Y_test)))
        absoluteError_Load_Ratio_allPredictedSequence = np.zeros((len (Y_test)))
        absoluteError_Load_Ratio_allPredictedTimeslots = np.zeros((len (Y_test)))

        mse_perPredictedSequence = np.zeros((len (Y_test)))
        rmse_perPredictedSequence = np.zeros((len(Y_test)))


        abs_diff_perPredictedSequence_scaled = np.zeros((len (Y_test)))
        average_LoadValue_testData_perPredictedSequence_scaled = np.zeros((len (Y_test)))
        abs_diff_perPredictedTimeslot_ForEachSequence_scaled = np.zeros((len (Y_test)))
        absoluteError_Load_Ratio_allPredictedSequence_scaled = np.zeros((len (Y_test)))
        absoluteError_Load_Ratio_allPredictedTimeslots_scaled = np.zeros((len (Y_test)))

        mse_perPredictedSequence_scaled = np.zeros((len (Y_test)))
        rmse_perPredictedSequence_scaled = np.zeros((len(Y_test)))



        abs_diff_scaled = np.abs(Y_pred_scaled - Y_test_scaled)



        abs_diff_scaled_combined = abs_diff_scaled.sum(axis=2)
        abs_diff_combined  = abs_diff.sum(axis=2)



        try:
            for i in range (0, len(Y_test)):
                for j in range (0, len(Y_test [0])):
                    abs_diff_perPredictedSequence_scaled [i] = abs_diff_perPredictedSequence_scaled [i] + abs_diff_scaled_combined [i][j]

                mse_perPredictedSequence_scaled [i] = mean_squared_error(Y_test_scaled[i] , Y_pred_scaled [i] )
                rmse_perPredictedSequence_scaled [i] = np.sqrt(mse_perPredictedSequence_scaled [i])
                abs_diff_perPredictedTimeslot_ForEachSequence_scaled [i] = abs_diff_perPredictedSequence [i] / len(Y_test_scaled [0])
                average_LoadValue_testData_perPredictedSequence_scaled [i] = np.mean (Y_test_scaled [i])
                absoluteError_Load_Ratio_allPredictedSequence_scaled [i] = abs_diff_perPredictedSequence_scaled [i] / average_LoadValue_testData_perPredictedSequence_scaled [i]
                absoluteError_Load_Ratio_allPredictedTimeslots_scaled [i] = abs_diff_perPredictedTimeslot_ForEachSequence_scaled [i]  / average_LoadValue_testData_perPredictedSequence_scaled [i]


            rmse_average_allPredictictedSequences_scaled  = np.mean (rmse_perPredictedSequence_scaled)
            absoluteAverageError_Load_Ratio_allPredictedSequence_scaled = np.mean (absoluteError_Load_Ratio_allPredictedSequence_scaled)
            absoluteAverageError_Load_Ratio_allPredictedTimeslots_scaled = np.mean (absoluteError_Load_Ratio_allPredictedTimeslots_scaled)
            absoluteAverageError_allPredictedSequences_scaled =  np.mean (abs_diff_perPredictedSequence_scaled)
            absoluteAverageError_allPredictedTimeslots_scaled =  np.mean (abs_diff_perPredictedTimeslot_ForEachSequence_scaled)



        except:
            print("Exception")
            rmse_average_allPredictictedSequences_scaled  = -1
            absoluteAverageError_Load_Ratio_allPredictedSequence_scaled = -1
            absoluteAverageError_Load_Ratio_allPredictedTimeslots_scaled = -1
            absoluteAverageError_allPredictedSequences_scaled= -1
            absoluteAverageError_allPredictedTimeslots_scaled = -1
            calculationOfAverageErrorWasNotPossible_scaled = True


        try:
            for i in range (0, len(Y_test)):
                for j in range (0, len(Y_test [0])):
                    abs_diff_perPredictedSequence [i] = abs_diff_perPredictedSequence [i] + abs_diff_scaled_combined [i][j]

                mse_perPredictedSequence [i] = mean_squared_error(Y_pred[i] , Y_test [i] )
                rmse_perPredictedSequence [i] = np.sqrt(mse_perPredictedSequence [i])
                abs_diff_perPredictedTimeslot_ForEachSequence [i] = abs_diff_perPredictedSequence [i] / len(Y_test [0])
                average_LoadValue_testData_perPredictedSequence [i] = np.mean (Y_test [i])
                absoluteError_Load_Ratio_allPredictedSequence [i] = abs_diff_perPredictedSequence [i] / average_LoadValue_testData_perPredictedSequence [i]
                absoluteError_Load_Ratio_allPredictedTimeslots [i] = abs_diff_perPredictedTimeslot_ForEachSequence [i]  / average_LoadValue_testData_perPredictedSequence [i]


            rmse_average_allPredictictedSequences  = np.mean (rmse_perPredictedSequence)
            absoluteAverageError_Load_Ratio_allPredictedSequence = np.mean (absoluteError_Load_Ratio_allPredictedSequence)
            absoluteAverageError_Load_Ratio_allPredictedTimeslots = np.mean (absoluteError_Load_Ratio_allPredictedTimeslots)
            absoluteAverageError_allPredictedSequences =  np.mean (abs_diff_perPredictedSequence)
            absoluteAverageError_allPredictedTimeslots =  np.mean (abs_diff_perPredictedTimeslot_ForEachSequence)



        except:
            print("Exception")
            rmse_average_allPredictictedSequences  = -1
            absoluteAverageError_Load_Ratio_allPredictedSequence = -1
            absoluteAverageError_Load_Ratio_allPredictedTimeslots = -1
            absoluteAverageError_allPredictedSequences= -1
            absoluteAverageError_allPredictedTimeslots = -1
            calculationOfAverageErrorWasNotPossible = True



        #Find the indices with the best, worst and mediocre predictions (based on RMSE)
        index_TimeSlot_BestPrediction = -1
        index_TimeSlot_WorstPrediction = -1
        index_TimeSlot_MediocrePrediction  = - 1
        currentError_BestPrediction = 999999999999
        currentError_WorstPrediction = 0
        currentDifference_MediocrePrediction = rmse_average_allPredictictedSequences * 2
        currentError_MediocrePrediction = 0


        for i in range (0, len(rmse_perPredictedSequence)):
            if rmse_perPredictedSequence [i] <= currentError_BestPrediction:
                currentError_BestPrediction = rmse_perPredictedSequence [i]
                index_TimeSlot_BestPrediction = i
            if rmse_perPredictedSequence [i] >= currentError_WorstPrediction:
                currentError_WorstPrediction = rmse_perPredictedSequence [i]
                index_TimeSlot_WorstPrediction = i
            if abs(rmse_perPredictedSequence [i] - rmse_average_allPredictictedSequences) <currentDifference_MediocrePrediction:
                index_TimeSlot_MediocrePrediction = i
                currentDifference_MediocrePrediction = abs(rmse_perPredictedSequence [i] - rmse_average_allPredictictedSequences)
                currentError_MediocrePrediction = rmse_perPredictedSequence [i]



        print("currentError_BestPrediction: ", round(currentError_BestPrediction,2))
        print("currentError_WorstPrediction: ", round(currentError_WorstPrediction,2))
        print("currentError_MediocrePrediction: ", round(currentError_MediocrePrediction,2))

        #Plot the mapping results
        import matplotlib.transforms as mtransforms

        resolutionOfFiguresDPI = 150

        if SetUpScenarios.numberOfBuildings_BT1 == 1 or SetUpScenarios.numberOfBuildings_BT2 == 1 or SetUpScenarios.numberOfBuildings_BT4==1:
            fig, ax = plt.subplots()
            ax.plot(Y_pred [index_TimeSlot_BestPrediction, :, 0], zorder=1)
            ax.plot(Y_test [index_TimeSlot_BestPrediction, :, 0], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            #ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Heating BufferStorage')
            plt.title('Test Mapping (Best)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_HeatingBufferStorage_Test_Best.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_WorstPrediction, :, 0], zorder=1)
            ax.plot(Y_test[index_TimeSlot_WorstPrediction, :, 0], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Heating BufferStorage')
            plt.title('Test Mapping (Worst)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_HeatingBufferStorage_Test_Worst.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_MediocrePrediction, :, 0], zorder=1)
            ax.plot(Y_test[index_TimeSlot_MediocrePrediction, :, 0], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Heating BufferStorage')
            plt.title('Test Mapping (Mediocre)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_HeatingBufferStorage_Test_Mediocre.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

        if SetUpScenarios.numberOfBuildings_BT1 == 1 or SetUpScenarios.numberOfBuildings_BT2 == 1:
            fig, ax = plt.subplots()
            ax.plot(Y_pred [index_TimeSlot_BestPrediction, :, 1], zorder=1)
            ax.plot(Y_test [index_TimeSlot_BestPrediction, :, 1], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            #ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Heating DHW')
            plt.title('Test Mapping (Best)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_HeatingDHW_Test_Best.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_WorstPrediction, :, 1], zorder=1)
            ax.plot(Y_test[index_TimeSlot_WorstPrediction, :, 1], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Heating DHW')
            plt.title('Test Mapping (Worst)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_HeatingDHW_Test_Worst.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_MediocrePrediction, :, 1], zorder=1)
            ax.plot(Y_test[index_TimeSlot_MediocrePrediction, :, 1], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Heating DHW')
            plt.title('Test Mapping (Mediocre)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_HeatingDHW_Test_Mediocre.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

        if SetUpScenarios.numberOfBuildings_BT1 == 1 or SetUpScenarios.numberOfBuildings_BT3 == 1:
            if SetUpScenarios.numberOfBuildings_BT1 == 1:
                indexPositionOfTheChargingTimeSeries = 2
            if SetUpScenarios.numberOfBuildings_BT3 == 1:
                indexPositionOfTheChargingTimeSeries =0
            fig, ax = plt.subplots()
            ax.plot(Y_pred [index_TimeSlot_BestPrediction, :, indexPositionOfTheChargingTimeSeries], zorder=1)
            ax.plot(Y_test [index_TimeSlot_BestPrediction, :, indexPositionOfTheChargingTimeSeries], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            #ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('EV Charging')
            plt.title('Test Mapping (Best)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_EVCharging_Test_Best.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_WorstPrediction, :, indexPositionOfTheChargingTimeSeries], zorder=1)
            ax.plot(Y_test[index_TimeSlot_WorstPrediction, :, indexPositionOfTheChargingTimeSeries], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('EV Charging')
            plt.title('Test Mapping (Worst)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_EVCharging_Test_Worst.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_MediocrePrediction, :, indexPositionOfTheChargingTimeSeries], zorder=1)
            ax.plot(Y_test[index_TimeSlot_MediocrePrediction, :, indexPositionOfTheChargingTimeSeries], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('EV Charging')
            plt.title('Test Mapping (Mediocre)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_EVCharging_Test_Mediocre.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()


        if SetUpScenarios.numberOfBuildings_BT5 == 1:
            fig, ax = plt.subplots()
            ax.plot(Y_pred [index_TimeSlot_BestPrediction, :, 0], zorder=1)
            ax.plot(Y_test [index_TimeSlot_BestPrediction, :, 0], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            #ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Charging Battery')
            plt.title('Test Mapping (Best)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_Charging Battery_Test_Best.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_WorstPrediction, :, 0], zorder=1)
            ax.plot(Y_test[index_TimeSlot_WorstPrediction, :, 0], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Charging Battery')
            plt.title('Test Mapping (Worst)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_Charging Battery_Test_Worst.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()

            fig, ax = plt.subplots()
            ax.plot(Y_pred[index_TimeSlot_MediocrePrediction, :, 0], zorder=1)
            ax.plot(Y_test[index_TimeSlot_MediocrePrediction, :, 0], zorder=0)
            trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
            # ax.text(0, -0.15, date_TimeSlot_BestPrediction_wholeDataframe_Beginning, transform=trans, va='top', ha='center', color='r')
            plt.xlabel('Timeslot')
            plt.ylabel('Charging Battery')
            plt.title('Test Mapping (Mediocre)')
            plt.legend(['prediction', 'actual'], loc='upper left')
            filename = entireFolderNameForTheResultsOfTheRun + "\Mapping_Charging Battery_Test_Mediocre.png"
            plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
            plt.clf()






















    #Plot training results
    plt.plot(history.history['mean_absolute_percentage_error'])
    plt.plot(history.history['val_mean_absolute_percentage_error'])
    plt.title('Mean absolute percentage error')
    plt.ylabel('Mean absolute percentage error')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    filename = entireFolderNameForTheResultsOfTheRun + "\Training_Results_MAPE.png"
    plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
    plt.clf()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Loss function')
    plt.ylabel('Mean squared Error')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    filename = entireFolderNameForTheResultsOfTheRun + "\Training_Results_MSE.png"
    plt.savefig(filename, bbox_inches='tight', dpi=resolutionOfFiguresDPI)
    plt.clf()





    #Save parameters of trained model

    return dataScaler_InputFeatures, dataScaler_OutputLabels, model_best


#This method clusters the days of the training data into 'numberOfClusters'. Only the days of the first building in the training data is used for building the clusters.
def clusterTrainingData(trainingData, clusteringMethod, numberOfClusters):
    import numpy as np
    #Possible global features for clustering: simulationResult_RESGeneration, Outside Temperature [C],	Price [Cent/kWh], Availability of the EV
    numberOfTrainingDays = len(trainingData [0])
    inputTimeSeries_sumPVNominal = np.zeros((numberOfTrainingDays, SetUpScenarios.numberOfTimeSlotsPerDay))
    inputTimeSeries_outSideTemperature = np.zeros((numberOfTrainingDays, SetUpScenarios.numberOfTimeSlotsPerDay))
    inputTimeSeries_Price = np.zeros((numberOfTrainingDays, SetUpScenarios.numberOfTimeSlotsPerDay))
    inputTimeSeries_sumAvailabilityOfEV = np.zeros((numberOfTrainingDays, SetUpScenarios.numberOfTimeSlotsPerDay))
    helpCounter_currentNumberOfTrainingDays = 0

    #Read the price and temperature data
    for indexBuildingTrainingData in range (0, len(trainingData)):
        for indexTrainingDay in range(0, len(trainingData[0])):
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_Days/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_Day' +  str(trainingData [indexBuildingTrainingData][indexTrainingDay] + 1 ) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_Days/Outside_Temperature_1Minute_Day' +   str(trainingData [indexBuildingTrainingData][indexTrainingDay] + 1 ) + '.csv', sep =";")

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')



            for index_timeslot in range(0, SetUpScenarios.numberOfTimeSlotsPerDay):
                inputTimeSeries_outSideTemperature [ indexTrainingDay] [index_timeslot] =  df_outsideTemperatureData.loc[index_timeslot+1, 'Temperature [C]']
                inputTimeSeries_Price [ indexTrainingDay] [index_timeslot] =  df_priceData.loc[index_timeslot+1, 'Price [Cent/kWh]']


    #Read the input data of the buildings
    helpIndexTrainingData = -1
    for index_BT1 in range (0, SetUpScenarios.numberOfBuildings_BT1):
        for indexTrainingDay in range(0, len(trainingData[0])):
            helpIndexTrainingData+=1

            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT1_mHP_EV_SFH_1Minute_Days/HH" + str(index_BT1 + 1) + "/HH" + str(index_BT1 + 1) + "_Day" + str(trainingData [index_BT1][indexTrainingDay] + 1 )  +".csv", sep =";")

            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            for i in range (0, len(df_buildingData['Availability of the EV'])):
                if df_buildingData['Availability of the EV'] [i] > 0.1:
                    df_buildingData['Availability of the EV'] [i] = 1.0
                if df_buildingData['Availability of the EV'] [i] < 0.1 and df_buildingData['Availability of the EV'] [i] >0.01:
                    df_buildingData['Availability of the EV'] [i] = 0.0

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            #Create availability array for the EV
            availabilityOfTheEV = np.zeros(( SetUpScenarios.numberOfTimeSlotsPerDay))
            for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerDay):
                availabilityOfTheEV [index_timeslot_for_Availability] = df_buildingData['Availability of the EV'] [index_timeslot_for_Availability +1]
            indexOfTheEV = index_BT1

            df_availabilityPatternEV = pd.DataFrame({'Timeslot': df_buildingData.index, 'Availability of the EV':df_buildingData['Availability of the EV'] })


            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):
                inputTimeSeries_sumPVNominal [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumPVNominal[indexTrainingDay][index_timeslot] + df_buildingData.loc[ index_timeslot + 1, 'PV [nominal]']
                inputTimeSeries_sumAvailabilityOfEV [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumAvailabilityOfEV [indexTrainingDay][index_timeslot] + df_availabilityPatternEV.loc[index_timeslot+1, 'Availability of the EV']


    for index_BT2 in range (0, SetUpScenarios.numberOfBuildings_BT2):
        for indexTrainingDay in range(0, len(trainingData[0])):
            helpIndexTrainingData += 1

            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT2_mHP_SFH_1Minute_Days/HH" + str(index_BT2 + 1) + "/HH" + str(index_BT2 + 1) + "_Day" + str(trainingData [index_BT2][indexTrainingDay] + 1 )  +".csv", sep =";")

            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')


            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):
                inputTimeSeries_sumPVNominal [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumPVNominal[indexTrainingDay][index_timeslot] + df_buildingData.loc[ index_timeslot + 1, 'PV [nominal]']

    for index_BT3 in range (0, SetUpScenarios.numberOfBuildings_BT3):
        for indexTrainingDay in range(0, len(trainingData[0])):
            helpIndexTrainingData+=1

            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT3_EV_SFH_1Minute_Days/HH" + str(index_BT3 + 1) + "/HH" + str(index_BT3 + 1) + "_Day" + str(trainingData [index_BT3][indexTrainingDay] + 1 )  +".csv", sep =";")

            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            for i in range (0, len(df_buildingData['Availability of the EV'])):
                if df_buildingData['Availability of the EV'] [i] > 0.1:
                    df_buildingData['Availability of the EV'] [i] = 1.0
                if df_buildingData['Availability of the EV'] [i] < 0.1 and df_buildingData['Availability of the EV'] [i] >0.01:
                    df_buildingData['Availability of the EV'] [i] = 0.0

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            #Create availability array for the EV
            availabilityOfTheEV = np.zeros(( SetUpScenarios.numberOfTimeSlotsPerDay))
            for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerDay):
                availabilityOfTheEV [index_timeslot_for_Availability] = df_buildingData['Availability of the EV'] [index_timeslot_for_Availability +1]
            indexOfTheEV = SetUpScenarios.numberOfBuildings_BT1 + index_BT3

            df_availabilityPatternEV = pd.DataFrame({'Timeslot': df_buildingData.index, 'Availability of the EV':df_buildingData['Availability of the EV'] })


            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):
                inputTimeSeries_sumPVNominal [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumPVNominal[indexTrainingDay][index_timeslot] + df_buildingData.loc[ index_timeslot + 1, 'PV [nominal]']
                inputTimeSeries_sumAvailabilityOfEV [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumAvailabilityOfEV [indexTrainingDay][index_timeslot] + df_availabilityPatternEV.loc[index_timeslot+1, 'Availability of the EV']



    for index_BT4 in range (0, SetUpScenarios.numberOfBuildings_BT4):
        for indexTrainingDay in range(0, len(trainingData[0])):
            helpIndexTrainingData +=1

            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT4_mHP_MFH_1Minute_Days/HH" + str(index_BT4 + 1) + "/HH" + str(index_BT4 + 1) + "_Day" + str(trainingData [index_BT4][indexTrainingDay] + 1 )  +".csv", sep =";")

            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):
                inputTimeSeries_sumPVNominal [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumPVNominal[indexTrainingDay][index_timeslot] + df_buildingData.loc[ index_timeslot + 1, 'PV [nominal]']

    for index_BT5 in range (0, SetUpScenarios.numberOfBuildings_BT5):
        for indexTrainingDay in range(0, len(trainingData[0])):
            helpIndexTrainingData+=1

            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT5_Bat_SFH_1Minute_Days/HH" + str(index_BT5 + 1) + "/HH" + str(index_BT5 + 1) + "_Day" + str(trainingData [index_BT5][indexTrainingDay] + 1 )  +".csv", sep =";")

            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerDay + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')


            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerDay):
                inputTimeSeries_sumPVNominal [indexTrainingDay] [index_timeslot] = inputTimeSeries_sumPVNominal[indexTrainingDay][index_timeslot] + df_buildingData.loc[ index_timeslot + 1, 'PV [nominal]']

    #TODO (Später): Erweiterung für BT6 und BT7

    #TODO: Continue (22.08.): Clustern und Klassifizieren der Trainingstage


    print("")



if __name__ == "__main__":
    from random import randrange
    import numpy as np

    useNormalizedData = False
    useStandardizedData = True

    #Assign days to the training and test data
    numberOfTrainingDays_Overall = 80
    numberOfBuildingsForTrainingData_Overall = 1
    numberOfTestDays_Oveall = 30
    numberOfBuildingsForTestData_Overall = 1
    numberOfBuildingDataOverall = 20


    trainingDays_Overall = np.zeros((numberOfBuildingsForTrainingData_Overall, numberOfTrainingDays_Overall))
    testDays_Overall = np.zeros((numberOfBuildingsForTestData_Overall, numberOfTestDays_Oveall))



    usedTestData = np.zeros((numberOfBuildingDataOverall,  365))
    indexTestDay = 0
    indexBuilding = 0
    while indexBuilding < numberOfBuildingsForTestData_Overall:
        while indexTestDay < numberOfTestDays_Oveall:
            # Choose the test data
            randomNumber_DayOfTheYear = randrange(365)

            while randomNumber_DayOfTheYear > 89 and randomNumber_DayOfTheYear < 273:
                randomNumber_DayOfTheYear = randrange(365)
            if usedTestData[indexBuilding][randomNumber_DayOfTheYear] == 0:
                usedTestData[indexBuilding][randomNumber_DayOfTheYear] = 1
                testDays_Overall [indexBuilding][indexTestDay] = randomNumber_DayOfTheYear
            elif usedTestData[indexBuilding][randomNumber_DayOfTheYear] == 1:
                continue
            indexTestDay = indexTestDay + 1

        indexBuilding = indexBuilding + 1


    print(f"testDays_Overall: {testDays_Overall}")

    usedTrainingData = np.zeros((numberOfBuildingDataOverall, 365 ))
    indexTrainingDay = 0
    indexBuilding = 0
    while indexBuilding < numberOfBuildingsForTrainingData_Overall:
        while indexTrainingDay < numberOfTrainingDays_Overall:
            # Choose the Training data
            randomNumber_DayOfTheYear = randrange(365)

            while randomNumber_DayOfTheYear > 89 and randomNumber_DayOfTheYear < 275:
                randomNumber_DayOfTheYear = randrange(365)
            if usedTrainingData[indexBuilding][randomNumber_DayOfTheYear] == 0 and usedTestData [indexBuilding][randomNumber_DayOfTheYear] == 0:
                usedTrainingData[indexBuilding][randomNumber_DayOfTheYear] = 1
                trainingDays_Overall [indexBuilding][indexTrainingDay] = randomNumber_DayOfTheYear
            elif usedTrainingData[indexBuilding][randomNumber_DayOfTheYear] == 1 or usedTestData [indexBuilding][randomNumber_DayOfTheYear] == 1:
                continue
            indexTrainingDay = indexTrainingDay + 1

        indexBuilding = indexBuilding + 1


    print(f"trainingDays_Overall: {trainingDays_Overall}")

    trainingDays_Overall = trainingDays_Overall.astype(int)
    testDays_Overall= testDays_Overall.astype(int)




    usedMLMethod = 'Multi_Layer_Perceptron'  # Options ['Multi_Layer_Perceptron'] ['Random_Forest'] ['Gradient_Boosting']
    trainSupervisedML_SingleTimeslot_SingleBuildingOptScenario (trainingDays_Overall, numberOfTrainingDays_Overall, "Min_Costs",useNormalizedData, useStandardizedData, usedMLMethod)

    method_ANN_ForSequencePrediction = "RNN"
    trainRNN_MultipleTimeslot_SingleBuildingOptScenario (usedTrainingData,numberOfTrainingDays_Overall, "Min_Costs", useNormalizedData, useStandardizedData, method_ANN_ForSequencePrediction)

