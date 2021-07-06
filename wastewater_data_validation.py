# a program that validates the wastewater data between western and ontarios data sheets
import pandas as pd
import numpy as np

# open data sheets, needs to be alterd depending on user directory
western_data = pd.read_excel(r'/Users/simonarts/Desktop/Western_Work/WastewaterData.xlsx')
ontario_datasample = pd.read_excel(r'/Users/simonarts/Desktop/Western_Work/OntarioDataTemplate_ODM_Western.xlsx', sheet_name='6 - Sample')
ontario_datameasure = pd.read_excel(r'/Users/simonarts/Desktop/Western_Work/OntarioDataTemplate_ODM_Western.xlsx', sheet_name='7 - WWMeasure')

        
def check_measurements():
    
    
    file = open("WasteWater_Validation.txt","r+") #clear any exsisting data
    file.truncate(0)
    file.close()
        
    # if six measurements were taken for that day and location instead of three then a skip must be added in order to not double count samples
    skip_count = 0
    
    for index, rows in western_data.iterrows(): #iterate through the western data sheet
        # create a list for each type of viral load being measured in the ontario sheet
        o_ppmov_list = []
        o_n1_list = []
        o_n2_list = []
         
        # create a list for each type of viral load being measured in the ontario sheet
        ppmov_list = [rows['PMMoV (1)'], rows['PMMoV (2)'], rows['PMMoV (3)']]
        n1_list = [rows['N1 (1)'], rows['N1 (2)'], rows['N1 (3)']]
        n2_list = [rows['N2 (1)'], rows['N2 (2)'], rows['N2 (3)']]
        
        #iterate throuhh the ontario data sheet in order to het measurements for the corrseponding western sample
        get_values_from_o(ontario_datameasure[ontario_datameasure.sampleID == index + 1 + skip_count], o_ppmov_list, o_n1_list, o_n2_list)
        
        if index > 151: #temporary clause since the western sheet has more data points then the ontario sheet
            break
        
        if pd.isnull(rows['PMMoV (4)']) and pd.isnull(rows['N1 (4)']) and pd.isnull(rows['N2 (4)']): #if only three samples are present
            
            #check if data points are equal
            validate_data_lists(ppmov_list,  o_ppmov_list, index + 1 + skip_count) 
            validate_data_lists(n1_list, o_n1_list, index + 1 + skip_count)
            validate_data_lists(n2_list, o_n2_list, index + 1 + skip_count)
            
            if skip_count != 0:
                skip_count += 1
                
        else: # if six samples are present
            # add the six samples to the western lists
            ppmov_list += [rows['PMMoV (4)'], rows['PMMoV (5)'], rows['PMMoV (6)']]
            n1_list += [rows['N1 (4)'], rows['N1 (5)'], rows['N1 (6)']]
            n2_list += [rows['N2 (4)'], rows['N2 (5)'], rows['N2 (6)']]
            
            # add the six samples to the ontario list
            get_values_from_o(ontario_datameasure[ontario_datameasure.sampleID == index + 2 + skip_count], o_ppmov_list, o_n1_list, o_n2_list)  
            
            # check if points are equal
            validate_data_lists(ppmov_list,  o_ppmov_list, index + 2 + skip_count)
            validate_data_lists(n1_list, o_n1_list, index + 2 + skip_count)
            validate_data_lists(n2_list, o_n2_list, index + 2 + skip_count)
            skip_count += 1

def get_values_from_o(sheet, l1, l2, l3):
    
    c = 0 #counter in order to determine what viral load it is
    
    for i, r in sheet.iterrows():   
        
        if c < 3: #ppmov
            l1.append(r['value'])
            c += 1
            continue
            
        if c < 6: #N1
            l2.append(r['value'])
            c += 1
            continue
            
        if c < 9: #N2
            l3.append(r['value'])
            c += 1
            continue
        
        if c == 9:
            c = 0
            break

def validate_data_lists(l1, l2, ID):
    
    if l1 != l2: #if not equal
        
        intro = 'ERROR, sample ID: ' + str(ID) + ' does not match with the Western Data sheet.\n' 
        western = 'Western Data: ' + str(l1) + '\n'
        ontario = 'Ontario Data: ' + str(l2) + '\n'
        
        fobj = open('WasteWater_Validation.txt', 'a')
        fobj.write(intro)
        fobj.write(western)
        fobj.write(ontario)
        fobj.write('\n')
        fobj.close()

        
        
