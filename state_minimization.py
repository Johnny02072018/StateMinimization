# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 20:58:49 2018

@author: johnn
"""
from __future__ import print_function
import numpy as np
import itertools

#########################################################################################################################
# ------------------------------------------read flowtable from txt file-----------------------------------------------------
# this part reads in a flowtable, users need to enter the number of input on line 19
# this flowtable is broke into next_state_flow_table and output_flow_table
##########################################################################################################################
f = open("C:\Users\johnn\Desktop\Final_Project\example1.txt",'r') # Make sure the txt file's directory is here
lines = f.readlines()       #read in all lines in the txt file
f.close                     # close the opened file
target = lines[1:len(lines)]# don't include the solution line, when build the input flowtable
input_amount = 8            # User input_______amount of input___________________________________

next_state_flow_table=np.chararray([len(target),input_amount])       # Break the flowtable into next_state_flow_table
for i in range(0,len(target)):
    next_state_flow_table[i] = target[i].split()

output_flow_table=np.chararray([len(target),input_amount])          # and the output table
for i in range(0,len(target)):
    for j in range(0,input_amount):
        output_flow_table[i][j] = target[i][j*4]
#########################################################################################################################


###############################################################################################################################
# -------------------------------------Function of test if two states are incompatible-----------------------------------------
# if two states are incompatible return a true, alternatively I can make it output a "X" symbol if necessary
# This function can absolutely determine if two states are incompatible; but it can't gurantee two state are compatible
# if it returns true, we need to check the next state flow table to make the decision. EXAMPLE: "dg","ef",
###############################################################################################################################

#-------------------------------------------------------------------------------------------------------------------------
# This funtion only take output flow table state as inputs, not next state flow table
def incompatible(state_1,state_2):
    count = 0
    for i in range(1,len(state_1)):         # check how many pair of states that have different outputs while neither is "-"
        if(state_1[i] != "-" and state_2[i] != "-" and state_1[i] != state_2[i]):
            count = count + 1
    if(count == 0):
        return False
    else:
        return True
# Keep in mind that "dg" and "ef" are not return incompatible in this function, but they will need to be updated
# after checking conditionaly compatibility
        
#state_1 = output_flow_table[6]              # Test Line
#state_2 = output_flow_table[7]              # Test Line      
#incompatible_True_or_False = incompatible(state_1,state_2)  # Note: true here means two states are incompatible
#if(incompatible_True_or_False == True):
#    print("Two states are incompatible!!!!!!!!!!!!!")  
#elif(incompatible_True_or_False == False):
#    print("Two states are compatible")    
#-------------------------------------------------------------------------------------------------------------------------        
#########################################################################################################################


#########################################################################################################################
# -------------------------------------Function of test if two states are compatible----------------------------
# if two states are compatible return a true, alternatively I can make it output a "~" symbol if necessary
# This function can absolutely determine if two states are compatible; 
##################################################################################################################

# --------------------------------------------------------------------------------------------------------------------
# This function take output flow table as the first two inputs, and next state flow table as the last two inputs
# --------------------------------------------------------------------------------------------------------------------   
# inputs are a complete state row which includes the first state variable
# inputs are output_state_1, output_state_2,next_state_1,next_state_2
def compatible(state_1,state_2,state_11,state_22):
    count = 0
    if(incompatible(state_1,state_2) == False):         # ensure two states are not incompatible
#        print("Two states are not incompatible!!!!!!!!!!!!")
        for i in range(1,len(state_11)):                # find how many pair of next state are not "-"
            if(state_11[i] != "-" and state_22[i] != "-"):
                count = count + 1
#                print(i)
    
    elif(incompatible(state_1,state_2) == True):        # if two states are incompatible, they can't be compatible, return compatible == false
        return False
#    print("o count: ", count)    
    
    if( count == 0):        # if there is no pair with both "-", the external two states are surely compatible
        return True
    elif(count != 0):       # if there are pairs that have both "-"s, make sure the pair are either the same, or the same pair as external states
        count_0 = 0
        for i in range(1,len(state_11)):
            if(state_11[i] != "-" and state_22[i] != "-"):
                if(state_11[i] == state_22[i]):
                    count_0 = count_0 + 1
                elif(state_11[i] == state_11[0] and state_22[i] == state_22[0]):
                    count_0 = count_0 + 1
                elif(state_11[i] == state_22[0] and state_22[i] == state_11[0]):
                    count_0 = count_0 + 1  
#        print("count: ", count)
#        print("count_0: ",count_0)
        if(count == count_0):                # if all the pairs with both non "-" are compatible pairs, the external states are compatible
            return True
        else:
            return False
        
#state_1 = output_flow_table[0]              # Test Line
#state_2 = output_flow_table[1]              # Test Line
#state_11 = next_state_flow_table[0]
#state_22 = next_state_flow_table[1]
####state_11[1] = "-"      # Test for no conflict in next state table
####state_11[3] = "-"
####state_11[5] = "-"
####state_11[6] = "-" 
#compatible_True_or_False = compatible(state_1,state_2,state_11,state_22)  # Note: true here means two states are incompatible
###
#if(compatible_True_or_False == True):
#    print("Two states are compatible!!!!!!!!!!!!!")  
#elif(compatible_True_or_False == False):
#    print("Two states are incompatible")      
# ---------------------------------------------------------------------------------------------------------------------
#######################################################################################################################
    

#########################################################################################################################
# -------------------------------------Function of test if two states are conditional compatible----------------------------
# if two states are compatible return a true, alternatively I can make it output a "~" symbol if necessary
# This function can absolutely determine if two states are compatible; 
##################################################################################################################
# This function return True if and only if two states are conditional compatible; return false for both incompatible
# and compatible
# inputs are a complete state row which includes the first state variable
# inputs are output_state_1, output_state_2,next_state_1,next_state_2
def conditional_compatible(state_1,state_2,state_11,state_22):
    if(incompatible(state_1,state_2) == False):
        if(compatible(state_1,state_2,state_11,state_22) == False):
            result = []
            for i in range(1,len(state_11)):
                if(state_11[i] != "-" and state_22[i] != "-"):
#                    if(state_11[i] != state_22[i]):
#                        result = np.append(result,state_11[i])
#                        result = np.append(result,state_22[i])
                    if(state_11[i] != state_22[i] and (state_11[i] != state_11[0] or state_22[i] != state_22[0]) and (state_11[i] != state_22[0] or state_22[i] != state_11[0])  ):
                        result = np.append(result,state_11[i])
                        result = np.append(result,state_22[i])
            return result                
            return result                
        else: 
            return False
    else:
        return False
#
#state_1 = output_flow_table[0]              # Test Line
#state_2 = output_flow_table[4]
#state_11 = next_state_flow_table[0]
#state_22 = next_state_flow_table[4]
#conditional_compatible_True_or_False = conditional_compatible(state_1,state_2,state_11,state_22)
#######################################################################################################################
#                Build the adjacency matrix to find the index of conditionaly compatibles (alternate approach)
####################################################################################################################### 
# input: next_state_flow_table, output_flow_table; output: compatibility index table
# The first approach uses index to refer to output_flow_table output row directly to find out compatibility; then 
# go throught the adjacency matrix to find the right place to place compatible integers
def compatible_states_index_table(next_state_flow_table,output_flow_table):
    # -------------------------------------- Initialize compatible_index_table---------------------------------------------
    rows= len(next_state_flow_table)        
    columns = len(next_state_flow_table)
    
    compatible_table_adjacency_1st=np.zeros([rows,columns]) # build a adjacency matrix to find conditional compatibles
    for i in range(0,len(next_state_flow_table)):           
        for j in range(0,len(next_state_flow_table)):
            if( i<= j ):
                compatible_table_adjacency_1st[i][j] = -1
            elif(i>j):
                compatible_table_adjacency_1st[i,j] = -100
    # -----------------------------------------------------------------------------------------------------------------------
            
    # --------------------------------------- Checking for entries ---------------------------------------------------------- 
    for i in range(0,compatible_table_adjacency_1st.shape[0]):
        for j in range(0,compatible_table_adjacency_1st.shape[1]):
            if(compatible_table_adjacency_1st[j][i] != -1):            
#                print(j)
#                print(i)
#                print("------------------")
                state_num_1 = output_flow_table[j][1:output_flow_table.shape[1]]  # shape[1] is the column amount
                state_num_2 = output_flow_table[i][1:output_flow_table.shape[1]]  # shape[0] is the row amount
                
                if(incompatible(state_num_1,state_num_2) == True):      # check if these two states are incompatible
                    compatible_table_adjacency_1st[j][i] = -2   
                # note: I can add a elif condition to replace integer for compatibles with some integers if necessary
#                elif(compatible(output_flow_table[j],output_flow_table[i],next_state_flow_table[j],next_state_flow_table[i]) == True):
#                    compatible_table_adjacency_1st[j][i] = -100
                elif(incompatible(state_num_1,state_num_2) == False):   # here need to compare previous assignment of index values  
                    previous_max = np.max(compatible_table_adjacency_1st)
                    if(previous_max >= 0):
                        compatible_table_adjacency_1st[j][i] = previous_max + 1
                    elif(previous_max < 0):
                        compatible_table_adjacency_1st[j][i] = 0      
    return compatible_table_adjacency_1st


A_table_11 = compatible_states_index_table(next_state_flow_table,output_flow_table)  # Test Lines
# in this A_table_1, -1 represents the upper half of the compatibility table which are the "*", -2 represents the incompatibles,
# a postive integer represents its index of compatibility, -100 represents the compatible states
# -----------------------------------------------------------------------------------------------------------------------            
        
        
#######################################################################################################################
#                Build the adjacency matrix to find the index of conditionaly compatibles (alternate approach)
#######################################################################################################################            
#input: next_state_flow_table, next_state_flow_table. output:
# the second approach uses two reference index table to refer to the two states we are comapring, this will help to pick 
# the two states for the other adjacency matrix, all the other parts are the same
def compatible_states_index_table_2nd(next_state_flow_table,output_flow_table):
    # --------------------------------------- Build Compatibility Table --------------------------------------------------------
    rows= len(next_state_flow_table)        # Initialize compatible_index_table
    columns = len(next_state_flow_table)
    #
    compatible_table_index_1st = np.chararray((rows, columns))          # the first index table is used to define the index for the first state
    for i in range(0,len(next_state_flow_table)):
        for j in range(0,len(next_state_flow_table)):
            if( i<= j ):
                compatible_table_index_1st[i][j] = "*"
            elif(i>j):
                compatible_table_index_1st[i,j] = next_state_flow_table[j][0]
    #
    compatible_table_index_2nd = np.chararray((rows, columns))          # the second index talbe is used to define the index for the second state
    for i in range(0,len(next_state_flow_table)):
        for j in range(0,len(next_state_flow_table)):
            if( i<= j ):
                compatible_table_index_2nd[i][j] = "*"
            elif(i>j):
                compatible_table_index_2nd[i][j] = next_state_flow_table[i][0]
    
    
    ## -------------------------------------- Initialize compatible_index_table---------------------------------------------
    #rows= len(next_state_flow_table)        
    #columns = len(next_state_flow_table)
    #
    compatible_table_adjacency_1st=np.zeros([rows,columns]) # build a adjacency matrix to find conditional compatibles
    for i in range(0,len(next_state_flow_table)):           
        for j in range(0,len(next_state_flow_table)):
            if( i<= j ):
                compatible_table_adjacency_1st[i][j] = -1
            elif(i>j):
                compatible_table_adjacency_1st[i,j] = -100
    #
    ## -----------------------------------------------------------------------------------------------------------------------
                
    ## --------------------------------------- Checking for entries ---------------------------------------------------------- 
    for i in range(0,compatible_table_adjacency_1st.shape[0]):
        for j in range(0,compatible_table_adjacency_1st.shape[1]):
            if(compatible_table_adjacency_1st[j][i] != -1):
    #            print(j)
    #            print(i)
    #            print("---------")
                state_num_1_index = compatible_table_index_1st[j][i]    # find the first state of pair of states ---a
                state_num_2_index = compatible_table_index_2nd[j][i]    # find the first state of pair of states ---a
                for i_bot in range(0,len(output_flow_table)):               # find output from output flow table
                    if(output_flow_table[i_bot][0] == state_num_1_index):
                        state_num_1 = output_flow_table[i_bot][1:output_flow_table.shape[1]]
                    elif(next_state_flow_table[i_bot][0] == state_num_2_index):
                        state_num_2 = output_flow_table[i_bot][1:output_flow_table.shape[1]]
    #            
                if(incompatible(state_num_1,state_num_2) == True):      # check if these two states are incompatible
                    compatible_table_adjacency_1st[j][i] = -2
                
                # note: I can add a elif condition to replace integer for compatibles with some integers if necessary
#                elif(compatible(output_flow_table[j],output_flow_table[i],next_state_flow_table[j],next_state_flow_table[i]) == True):
#                    compatible_table_adjacency_1st[j][i] = -100
                elif(incompatible(state_num_1,state_num_2) == False):   # here need to compare previous assignment of index values  
                    previous_max = np.max(compatible_table_adjacency_1st)
    #            #    print(previous_max)
                    if(previous_max >= 0):
                        compatible_table_adjacency_1st[j][i] = previous_max + 1
                    elif(previous_max < 0):
                        compatible_table_adjacency_1st[j][i] = 0
    return(compatible_table_adjacency_1st, compatible_table_index_1st, compatible_table_index_2nd)
    ## -----------------------------------------------------------------------------------------------------------------------            
#[A_table_12,A_table_12_0,A_table_12_1] = compatible_states_index_table_2nd(next_state_flow_table,output_flow_table)  # Test Lines
###############################################################################################################################
                    
###############################################################################################################################    
#        Build the square matrix for finding the maximal compatibles
###############################################################################################################################
# This function will return a squre index table, which includes all the possible compatible pair of states, if a pair of state is
# conditonal compatible, its required states pairs will be listed as 1 in the corresponding column. If a pair of states are absolute 
# compatible, all row entries are "0"s. If a pair of states are incompatible for sure, their row will be filled with "-1"s

# inputs: the first adjaency matrix returned from the compatible_states_index_table function, output_flow_table, next_state_flow_table
# outputs: the square index table which tells all the possible compatible pairs and conditional pairs
def square_index_table(A_table_12,output_flow_table,next_state_flow_table):
    lenth_of_square_index_table = 0             # initialize the second square index table which covers all the condtional compatible pairs and compatible pairs
    for i in range(0,A_table_12.shape[0]):
        for j in range(0,A_table_12.shape[1]):
            if(A_table_12[i][j] >= 0):
                lenth_of_square_index_table = lenth_of_square_index_table + 1
    square_index_table = np.zeros([lenth_of_square_index_table,lenth_of_square_index_table])
    
    for i_top in range(0,lenth_of_square_index_table):      # go through all the non-negative integers to find which two are compatibles, conditional compatibles, or incompatibles
        for i in range(0,A_table_12.shape[0]):
            for j in range(0,A_table_12.shape[1]):
                if(A_table_12[j,i] == i_top):
#                    print("i_top: ",i_top)
#                    print("i: ",i)
#                    print("j: ",j)
                    
                    state_1 = output_flow_table[i]      # find the output state variables from the output_flow_table
                    state_2 = output_flow_table[j]
                    state_11 = next_state_flow_table[i] # find the next state variables from the next_state_flow_table
                    state_22 = next_state_flow_table[j]
#                    print("state 1: ")
#                    print(state_1)
#                    print("state 2: ")
#                    print(state_2)
#                    print("state 11: ")
#                    print(state_11)
#                    print("state 22: ")
#                    print(state_22)
                    conditional_compatible_True_or_False = conditional_compatible(state_1,state_2,state_11,state_22) # find all the required states, if two states are conditional compatible with each other
    #                compatible_True_or_False = compatible(state_1,state_2,state_11,state_22)
#                    print("conditional_compatible_True_or_False: ")
#                    print(conditional_compatible_True_or_False)
                    
                    if(conditional_compatible_True_or_False != False):      # This math equation will check if all the required states are compatible, if the required states are in-compatible, it means this current state can't be compatible
                        for i_0_bottom in range(0,len(conditional_compatible_True_or_False)/2):
                            check_0 = conditional_compatible_True_or_False[i_0_bottom*2]
                            check_1 = conditional_compatible_True_or_False[i_0_bottom*2+1]
                            for i_1_bottom in range(0,output_flow_table.shape[0]):
                                if(check_0 == output_flow_table[i_1_bottom][0]):
                                    check_0_parameter = i_1_bottom
    #                                print("check_0_parameter", check_0_parameter)
                                elif(check_1 == output_flow_table[i_1_bottom][0]):
                                    check_1_parameter = i_1_bottom
    #                                print("check_1_parameter", check_1_parameter)
#                            print("check_0_parameter", check_0_parameter)
#                            print("check_1_parameter", check_1_parameter)
    #                        print("A_table_12[check_0_parameter,check_1_parameter]")
    #                        print(A_table_12[check_0_parameter,check_1_parameter])
                            if(check_0_parameter > check_1_parameter):  # notice that, we are dealing with the lower half of the index table, so its x-direction index is always smaller than y-direction index
                                if(A_table_12[check_0_parameter,check_1_parameter] >=0 ):
    #                                print("YES")
    #                                print("A_table_12[check_0_parameter,check_1_parameter]")
    #                                print(int(A_table_12[check_0_parameter,check_1_parameter]))
                                    square_index_table[i_top,int(A_table_12[check_0_parameter,check_1_parameter])] = 1
                                elif(A_table_12[check_0_parameter,check_1_parameter] < 0 ):
                                    square_index_table[i_top,:] = -1
                            elif(check_1_parameter > check_0_parameter):
                                if(A_table_12[check_1_parameter,check_0_parameter]>=0):
    #                                print("No")
                                    square_index_table[i_top,int(A_table_12[check_1_parameter,check_0_parameter])] = 1
                                elif(A_table_12[check_1_parameter,check_0_parameter]>=0):
                                    square_index_table[i_top,:] = -1
                  
    for i in range(0,square_index_table.shape[0]):      # ensure a pair state that is neither compatible or non-conditional compatible is filled with -1
        for j in range(0,square_index_table.shape[1]):
            if(square_index_table[i,j] == -1):
                square_index_table[i,:] = -1
    return square_index_table

#A_table_12= compatible_states_index_table(next_state_flow_table,output_flow_table)      # Test Lines
#A_square_index_table = square_index_table(A_table_12,output_flow_table,next_state_flow_table)
###############################################################################################################################

###############################################################################################################################
#                                Find Maximal Compatibles
###############################################################################################################################
# This function will update the first adjacency list first, then find all the maximal compatibles from the right to the left from the first
# adjacency matrix. It starts find all the possible sublist, and all the intersecting list, and add them to the maximal compatible list
# finally update the the maximal compatibles by removing the duplicates and subsets
# inputs: first adjacency list, the square index matrix, next_state_flow_talbe, output_flow_table
# output: a list of list which represents the maximal compatibles.
    
def intersection(lst1, lst2):   # set up this function to find the intersecting item of two maximal compatible lists
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
def find_maximal_compatibles(A_table_12,square_index_table,next_state_flow_table,output_flow_table):
    A_table_12= compatible_states_index_table(next_state_flow_table,output_flow_table)  # input next_state_flow_table, and output_flow_table to generate the first adjacency matrix
    A_square_index_table = square_index_table(A_table_12,output_flow_table,next_state_flow_table) # This square table is used for find the prime compatibles, it also helps to update the first adjacency mapping matrix   
    for i_top in range(0,A_square_index_table.shape[0]):        # Update the matrix by removing the in-conditional pairs
        for j_top in range(0,A_square_index_table.shape[1]):
            if(A_square_index_table[i_top,j_top] == -1):
                # find incompatible pair---index is i_top
                for i in range(0,A_table_12.shape[0]):
                    for j in range(0,A_table_12.shape[1]):
                        if(A_table_12[i,j] == i_top):
                            A_table_12[i,j] = -2
                            
    ## start finding maximal compatibles                        
    M = np.array([])    # find the very first maximal comaptible list
    for i in range(0,A_table_12.shape[0]):
        for j in range(0,A_table_12.shape[1]):
            if(A_table_12[i,j] == np.max(A_table_12)):
                M = [j,i] # find the first list, such that M = {f,g}={5,6}  
    #A_table_12[M[1],M[0]] = -3 # tried to remove the first maximal compatibles, but it is not sufficient to do so, because I can still remove it when I check the intersection between every sublist pairs in the maximal compatible pairs            
    maximal_compatibles = []        # initialize maximal compatibles
    maximal_compatibles.append(M)   # add the the first sublist M(first compatibles) to the maximal compatibles list
#    print("maximal compatibiles original: ",maximal_compatibles)
    
    for i in range(A_table_12.shape[1]-1,-1,-1):    # go through the column from the right side to the left side
        for j in range(A_table_12.shape[0]-1,-1,-1): # go through the bottom row to the top row
            if(A_table_12[j,i] >= 0 ):               # find all compatible locations
#                print("useful terms: ",A_table_12[j,i])
#                print("column number: ", i)
                S_i_column = i    # indicate the column of one entry that need to be compared(the e in Se)
#                print("S_i_column: ",S_i_column)
                
                new_list_1 = [i,j]
#                print("new_list_1: ", new_list_1)
                maximal_compatibles.append(new_list_1)
#                print("maximal_compatibles: ", maximal_compatibles)
                
                S_i =[]     # the actual items in the sublist(such that Se = h, S_i contains h here)
                for i_1 in range(0,A_table_12.shape[0]):    
                    if(A_table_12[i_1,S_i_column] >= 0 ):    # find all possible rows for the sublists by appending S_i
                        S_i.append(i_1)
#                print("S_i: ", S_i)
    #
                for i_2 in range(0,len(maximal_compatibles)):
                    if(len(intersection( maximal_compatibles[i_2],S_i )) >=2 ):
#                        print("intersection amount: ",len(intersection( maximal_compatibles[i_2],S_i )))
#                        print("intersections are: ",intersection( maximal_compatibles[i_2],S_i ))
                        new_list_0 = intersection( maximal_compatibles[i_2],S_i )
                        new_list_0.append(S_i_column)
                        new_list_0.sort()
#                        print("updated lists----------------------: ", new_list_0)
                        maximal_compatibles.append(new_list_0)
#                print("--------------------------------------------------------------------------------------------------")
    
#    print("Maxiaml Compatibles updates: ",maximal_compatibles)
    
    maximal_compatibles.sort()      # remove the duplicate list
    maximal_compatibles = list(maximal_compatibles for maximal_compatibles,_ in itertools.groupby(maximal_compatibles))
#    print("------------------------: ", maximal_compatibles)
    
    
    # remove all subsets
    maximal_compatibles_copy = maximal_compatibles[:]
    for m in maximal_compatibles:
        for n in maximal_compatibles:
            if set(m).issubset(set(n)) and m != n:
                maximal_compatibles_copy.remove(m)
                break
    
#    print("Final Maximal Compatibles is:", maximal_compatibles_copy)
    return maximal_compatibles_copy

# set up this function to better visualize the maximal compatible in character representation rather than the index values
def char_represent_maximal_compatibles(maximal_compatibles_for_next):
    for i in range(0,len(maximal_compatibles_for_next)):
        for j in range(0,len(maximal_compatibles_for_next[i])):
            if(maximal_compatibles_for_next[i][j]==0):
                maximal_compatibles_for_next[i][j] = "a"
            elif(maximal_compatibles_for_next[i][j]==1):
                maximal_compatibles_for_next[i][j] = "b"
            elif(maximal_compatibles_for_next[i][j]==2):
                maximal_compatibles_for_next[i][j] = "c"
            elif(maximal_compatibles_for_next[i][j]==3):
                maximal_compatibles_for_next[i][j] = "d"
            elif(maximal_compatibles_for_next[i][j]==4):
                maximal_compatibles_for_next[i][j] = "e"
            elif(maximal_compatibles_for_next[i][j]==5):
                maximal_compatibles_for_next[i][j] = "f"
            elif(maximal_compatibles_for_next[i][j]==6):
                maximal_compatibles_for_next[i][j] = "g"
            elif(maximal_compatibles_for_next[i][j]==7):
                maximal_compatibles_for_next[i][j] = "h"
    return maximal_compatibles_for_next
            


A_table_12= compatible_states_index_table(next_state_flow_table,output_flow_table)      # Test Lines
A_square_index_table = square_index_table(A_table_12,output_flow_table,next_state_flow_table)
maximal_compatibles_for_next = find_maximal_compatibles(A_table_12,square_index_table,next_state_flow_table,output_flow_table)
maximal_compatibles = char_represent_maximal_compatibles(maximal_compatibles_for_next)         
# -----------------------------------------------------------------------------------------------------------------------------
# Attempt to find solution for a specific example-----------------Not Approved
#A_table_12= compatible_states_index_table(next_state_flow_table,output_flow_table)      # Test Lines
#A_square_index_table = square_index_table(A_table_12,output_flow_table,next_state_flow_table)    
#for i_top in range(0,A_square_index_table.shape[0]):        # Update the matrix by removing the in-conditional pairs
#    for j_top in range(0,A_square_index_table.shape[1]):
#        if(A_square_index_table[i_top,j_top] == -1):
#            # find incompatible pair---index is i_top
#            for i in range(0,A_table_12.shape[0]):
#                for j in range(0,A_table_12.shape[1]):
#                    if(A_table_12[i,j] == i_top):
#                        A_table_12[i,j] = -2
#            
#c_list = np.array([])
#for i in range(0,A_table_12.shape[1]):
#    for j in range(0,A_table_12.shape[0]):
#        if(A_table_12[j,i] == np.max(A_table_12)):
#            c_list = [i,j]      # get {f,g}
#
#print("c_list",c_list)
#A_table_12[c_list[1],c_list[0]] = -3
#
#for i in range(0,A_table_12.shape[1]):
#    for j in range(0,A_table_12.shape[0]):
#        if(A_table_12[j,i] == np.max(A_table_12)):
#            print("i column is: ", i)
#            for k in range(0,A_table_12.shape[0]):
#                if(A_table_12[k,i] > 0):
#                    S_i = [k]
#                    index_result = i
#
#print("index_result: ", index_result)                                        
#print("S_i: ",S_i)       
#intersection_c_list_and_S_i = [val for val in c_list if val in S_i]   # find intersection of c_list and Si
#if(len(intersection_c_list_and_S_i) == 0):
#    new_list = np.append(S_i,index_result) 
#new_list = np.sort(new_list) # get {e,h}
# ----------------------------------------------------------------------------------------------------------------------------   

# ----------------------------------------------------------------------------------------------------------------------------------------------------
#               Attemped to remove subset and repeated sublist concurrently(failed)
# -----------------------------------------------------------------------------------------------------------------------------------------------------            
#            for i_3 in range(0,len(S_i)):
#                new_list_1.append(S_i[i_3])
#                print("new_list_1: ", new_list_1)
#            new_list_1.append(S_i_column)
#            print("new_list_1: ", new_list_1)
#            new_list_1.sort()
#            print("new_list_1: ", new_list_1)
##            maximal_compatibles.append(new_list_1)
#            maximal_compatibles.append(new_list_1)
#            print("new_list_1 updated: ", new_list_1)   
#            print("Final Maxiaml Compatibles: ", maximal_compatibles)
#            
#            maximal_compatibles.append(S_i)
##            for i_2 in range(0,len(maximal_compatibles)):   # trying to compare the current compare list(c-list) to every sublist in the current maximal compatible list
#                if(intersection( maximal_compatibles[i_2],S_i ) >=0 ):  # first check if two list have intersection
#                    new_list_0 = intersection( maximal_compatibles[i_2],S_i )
#                    new_list_0.append(S_i_column)
#                    new_list_0.sort()
#            print("new_list_0: ", new_list_0)
#            maximal_compatibles.append(new_list_0) # adding new maximal compatible list to the existing maximal compatible list
#            print("maximal compatibles: ", maximal_compatibles)
#            index_to_remove = np.array([])      # trying to remove the identical sublists
#            index_to_remove = index_to_remove.astype(np.int64)  
#            for i_3 in range(0,len(maximal_compatibles)-1):
#                list_1 = maximal_compatibles[i_3]
#                for j_3 in range(i_3+1,len(maximal_compatibles)):
#                    list_2 = maximal_compatibles[j_3]
#                    if(list_1 == list_2):
#                        index_to_remove = np.append(index_to_remove,i_3)
#            print("index_to_remove: ",index_to_remove)





## start finding maximal compatibles                        
#M = np.array([])    # find the very first maximal comaptible list
#for i in range(0,A_table_12.shape[0]):
#    for j in range(0,A_table_12.shape[1]):
#        if(A_table_12[i,j] == np.max(A_table_12)):
#            M = [j,i] # find the first list, such that M = {f,g}={5,6}  
##A_table_12[M[1],M[0]] = -3 # tried to remove the first maximal compatibles, but it is not sufficient to do so, because I can still remove it when I check the intersection between every sublist pairs in the maximal compatible pairs            
#maximal_compatibles = []        # initialize maximal compatibles
#maximal_compatibles.append(M)   # add the the first sublist M(first compatibles) to the maximal compatibles list
#
#for i in range(A_table_12.shape[1]-1,-1,-1):    # go through the column from the right side to the left side
#    for j in range(A_table_12.shape[0]-1,-1,-1): # go through the bottom row to the top row
#        if(A_table_12[j,i] > 0 ):               # find all compatible locations
#            print("useful terms: ",A_table_12[j,i])
#            print("column number: ", i)
#            S_i_column = i    # indicate the column of one entry that need to be compared(the e in Se)
#            print("S_i_column: ",S_i_column)
#            S_i =[S_i_column]     # the actual items in the sublist(such that Se = h, S_i contains h here)
#            for i_1 in range(0,A_table_12.shape[0]):    
#                if(A_table_12[i_1,S_i_column] >= 0 ):    # find all possible rows for the sublists by appending S_i
#                    S_i.append(i_1)
#            print("S_i: ", S_i)
#            maximal_compatibles.append(S_i)
##            for i_2 in range(0,len(maximal_compatibles)):   # trying to compare the current compare list(c-list) to every sublist in the current maximal compatible list
#                if(intersection( maximal_compatibles[i_2],S_i ) >=0 ):  # first check if two list have intersection
#                    new_list_0 = intersection( maximal_compatibles[i_2],S_i )
#                    new_list_0.append(S_i_column)
#                    new_list_0.sort()
#            print("new_list_0: ", new_list_0)
#            maximal_compatibles.append(new_list_0) # adding new maximal compatible list to the existing maximal compatible list
#            print("maximal compatibles: ", maximal_compatibles)
#            index_to_remove = np.array([])      # trying to remove the identical sublists
#            index_to_remove = index_to_remove.astype(np.int64)  
#            for i_3 in range(0,len(maximal_compatibles)-1):
#                list_1 = maximal_compatibles[i_3]
#                for j_3 in range(i_3+1,len(maximal_compatibles)):
#                    list_2 = maximal_compatibles[j_3]
#                    if(list_1 == list_2):
#                        index_to_remove = np.append(index_to_remove,i_3)
#            print("index_to_remove: ",index_to_remove)

# need to remove all the identical sublist from the existing maximal compatible list; should use the pop operation for
# list operation.
# need to figure this part out, because it is not removing all identical sublists, 
# and also need to consider to remove the sublist
# the idea is to compare any two list, find the amount of intersection, if the intersection amount is equal to one
# of the list, the shorter list's index will be recored, and after jump out of the loop, these terms will be removed
# by its corresponding index.            

#            if(len(index_to_remove) >0 ):
#                maximal_compatibles.pop(index_to_remove[0])
#            print("updated maximal compatibles: ", maximal_compatibles)
#
#                        
##            for i_4 in range(len(index_to_remove),0):    
##                maximal_compatibles.delete(index_to_remove[i_4])
##            print("Good")
##                
#                
#            print("----------------------------------------------")
#            
#            
#            
            
            
## check if two lists intersect
#a = [1,2,3]
#b = [3,4,5]
##c = any(i in a for i in b)
## Python program to illustrate the intersection
## of two lists in most simple way

# 
## Driver Code
#lst1 = [4, 9, 1, 17, 11, 26, 28, 54, 69]
#lst2 = [9, 9, 74, 21, 45, 11, 63, 28, 26]
#print(intersection(lst1, lst2))



#S_i_0 = np.array([])
#for i in range(0,A_table_12.shape[0]):
#    if(A_table_12[i,M[0]-1]>0):
#        S_i_0 = i
#new_maximal_compatibles_0 = [M[0]-1, S_i_0]
#maximal_compatibles.append(new_maximal_compatibles_0)

#S_i_1 = []
#new_maximal_compatibles_1 = []
#for i in range(0,A_table_12.shape[0]):
#    if(A_table_12[i,M[0]-2]>0):
#        print("i",i)
#        S_i_1 = np.append(S_i_1,i)
#new_maximal_compatibles_1=np.append(new_maximal_compatibles_1,S_i_1)
#new_maximal_compatibles_1=np.append(new_maximal_compatibles_1,M[0]-2)
#new_maximal_compatibles_1=np.sort(new_maximal_compatibles_1)
#maximal_compatibles.append(new_maximal_compatibles_1)

#S_i_1 = []
#new_maximal_compatibles_1 = []
#for i in range(0,A_table_12.shape[0]):
#    if(A_table_12[i,M[0]-2]>0):
#        print("i",i)
#        S_i_1.append(i)
#new_maximal_compatibles_1.append(M[0]-2)
#new_maximal_compatibles_1.extend(S_i_1)
#maximal_compatibles.append(new_maximal_compatibles_1)





#for i in range(A_table_12.shape[0]-1,0,-1):
#    for j in range(A_table_12.shape[1]-1,0,-1):
#        if()
#        print("--------------------------------------")
#        print("i",i)
#        print("j",j)
#----------------------------------------------------------------------------------------------------------------------------------------------------          
######################################################################################################################################################## 


######################################################################################################################################################## 
#                                       Set up Covering Problem
######################################################################################################################################################## 






















