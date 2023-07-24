#############################################################################################################################################################################################
## Coalexicon | CLX | Symbol/Unit Manager
## SPDX-FileCopyrightText: © 2020 Alexander Heinrich <alexander.heinrich@wsu.edu>
## SPDX-License-Identifier: BSD-3-Clause
##
## This program functions as an interactive interface and repository for managing and computing various quantities and units of measurement. Its GUI is constructed by the tkinter 
## module, though all other modules are relatively optional. Much of the code relies on iterative loops and global values to process and maintain data. Most of these global values
## are categorized by the number of elements they contain; thus, any iteration over a global value can share indices with others in that category. Much of the data woven throughout
## the program, such as symbol definitions and unit conversions, are editable within the GUI, allowing the program to be continually modified.
## 
## The overarching purposes of the Coalexicon--to assist in education and practical application as a symbolic dictionary and scientific toolset--are spread into two applications. 
## The first, called Symbol Manager, is designed to organize and standardize the symbols used in mathematics and the physical sciences. It allows multiple variants of the program to
## be loaded as independent databases, and multiple sorting methods are available to browse and adjust various data. The second application, called Unit Manager, is designed as a
## computational sandbox for common units of measurement. It produces and saves information relating to any specified set of units, including SI prefixes and numerical conversions.
#############################################################################################################################################################################################

#############################################################################################################################################################################################
## Imports
import tkinter as tk # Essential for the GUI.
from tkinter import ttk # Used to set scrollbar colors.
from tkinter import font # Used to set a default font.
from functools import partial # Used for interactive font styles.
from time import sleep # Used for troubleshooting and delaying script execution.
from fractions import Fraction # Used in simplifying fractional exponents.

#############################################################################################################################################################################################
## Global datasets
current_unit_list = [] # Holds a mutable list of elements of positive_numerator_list and negative_numerator_list. Ex=["m", "m", "-s", "-s"]
current_unit_name = [] # Holds a unique keyname for the current unit, given by name_creator. Ex=['meter_squared_per_second_squared']
current_display = [] # Holds a list of all strings that are processed for the main display. Ex=["1.23×10⁻¹", "MeV", "s⁻¹"]
display_list = [] # Holds an organized list of current units. Ex=["g", "m³", "C⁻²", "s⁻²"]
favorites_list = [] # Holds a mutable list of the current saved favorites. Ex=[<consolidated>, <units>, <denominator prefixes>, <numerator prefixes>, <value>]

current_value = 1 # Holds and initializes the total numerical value of the current units, not including current prefixes.
entry_unit_index = 7 # Holds and initializes an index to assist the entry of non-base units.
application_index = 1 # Designates the currently toggled application, which could be Unit Manager or Symbol Manager.
textbox_index = 1 # Tracks the current textbox in the lower subframe.

current_window_size = (900, 600) # Holds and initializes the current window size. Ex=(<width>, <height>)
current_database_file = "database_clx.txt" # Holds and initializes the filename of the current database.
current_category = "All" # Holds and initializes the name of the current category.
current_sort = "Name" # Holds and initializes the name of the current sorting method.
index_type = "Index" # Holds and initializes the sorting method for Symbols. Possible options are ["Primary", "Secondary", "Index"].

unit_names = ["candela", "coulomb", "gram", "kelvin", "meter", "mole", "second", "1"] # Indexed, immutable list of names of base units.
exponent_codes = [] # Mutable list of exponent symbols from 0 to x. Does not share an index with any other set.
exponent_symbols = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "¹⁰"] # Immutable exponent symbols from 0 to 9.
positive_denominator_exponent_array = [] # Indexed, closed numerical array, corresponding to positive exponents of base units. Ex=[0, 0, 2, 0, 4, 0, 0, 0, 0]
exponent_array, exponent_tuple_array = [], [] # Initializes the global form of exponent_tuple_array and its temporary form.

positive_numerator_symbols = ["cd", "C", "g", "K", "m", "mol", "s", "1"] # Indexed, mutable list of positive unit symbols.
negative_numerator_symbols = ["-cd", "-C", "-g", "-K", "-m", "-mol", "-s", "1"] # Indexed, mutable list of negative unit symbols.
positive_denominator_symbols = ["_cd", "_C", "_g", "_K", "_m", "_mol", "_s", "1"] # Indexed, mutable list of positive unit symbols.
numerator_value_list = [0, 0, 0, 0, 0, 0, 0, 0] # Initializes an indexed, mutable array that corresponds to the prefix value of all units in the numerator.
denominator_value_list = [0, 0, 0, 0, 0, 0, 0, 0]  # Initializes an indexed, mutable array that corresponds to the prefix value of all units in the denominator.
positive_numerator_custom_array = [] # Initializes an indexed, mutable array that corresponds to positive exponents of base and user-defined units. Ex=[0, 0, 0, 0, 0, 0, 0, 0, 2]
negative_numerator_custom_array = [] # Initializes an indexed, mutable array that corresponds to negative exponents of base and user-defined units. Ex=[0, 0, 0, 0, 0, 0, 0, 0, 0]
positive_denominator_custom_array = [] # Initializes an indexed, mutable array that corresponds to positive exponents of base and user-defined units. Ex=[0, 0, 0, 0, 0, 0, 0, 0, 2]
exponent_array_custom, exponent_tuple_array_custom = [], [] # Initializes the global form of exponent_tuple_array_custom and its temporary form.

current_unit_consolidated = [] # Holds a mutable list of units with respective exponents, given by consolidate_current_unit_list. Ex=["m²", "s⁻²"]
current_unit_custom = [] # Holds a mutable list of base and non-base units with respective exponents. Ex=["eV", "s⁻¹"]
current_unit_reduced = [] # Holds current base and non-base units without exponents. Ex=["eV", "s"]
compound_units_list = [] # Holds lists of each unit, prefix, and numerator. Ex=[["eV", "M", 1], ["s⁻¹", "k", 100]]
significand_order_units = [] # Holds current_unit_custom and the significand and order of current_value. # Ex=["1.23", 1000, ["eV", "s⁻¹"]]
units_exponents_totals = [] # Holds a list of current units, associated values, and multiplicity. Ex=[["s²", "s", 2, 2], ["eV", "eV", 1, 1000000]]

current_database_list = [] # Holds sorted data of the current database and category. Ex=[("<Name>", ["<Primary>", "<Secondary>", "<Other>", "<Units>", "<Index>", "<Category>"])]
notation_database_dictionary = {} # Holds the current database in a dictionary. Ex={"distance": ["d", "0", "l;s;r", "m", "d", "quantity"]}
notation_database_list = [] # Holds the current database in a list of tuples. Ex=[("distance", ["d", "0", "l;s;r", "m", "d", "quantity"])]
notation_database_quantities = [] # Holds saved quantities in a list of tuples. Ex=[("distance", ["d", "0", "l;s;r", "m", "d", "quantity"])]
notation_database_constants = [] # Holds saved constants in a list of tuples. Ex=[("Planck constant", ["h", "ℏ", "0", "g⸱m²⸱s⁻¹", "h", "constant"]}]
notation_database_modifiers = [] # Holds saved modifiers in a list of tuples. Ex=[("average", ["̅", "⟨ ⟩", "0", "0", "0", "modifier"])]
notation_database_other = []  # Holds saved uncategorized entries in a list of tuples. Ex=[("field", ["₣", "0", "0", "0", "F", "other"])]
notation_database_search = [] # Holds results of the current search. Ex=[("field", ["₣", "0", "0", "0", "F", "other"])]
conversion_database = {} # Holds a selection of non-base units for conversion to base units.
unit_database = {} # Holds information about particular combinations of base units.
cell_dictionary = {} # Initializes a dictionary of key-value pairs. Ex={'Name1': [<tkinter.Entry object .!frame2.!frame.!entry>, ₣]'}

#############################################################################################################################################################################################
## Functions
def print_sets(function=True):
    """ Optional. Called for troubleshooting and procedural insight. Optional. """
    print('print_sets():')  
    print(f'current_unit_list:                 {current_unit_list}')
    print(f'current_unit_name:                 {current_unit_name}')
    print(f'current_display:                   {current_display}')
    #print(f'positive_numerator_custom_array:   {positive_numerator_custom_array}')
    #print(f'negative_numerator_custom_array:   {negative_numerator_custom_array}')
    #print(f'numerator_value_list:             {numerator_value_list}')
    #print(f'denominator_value_list:           {denominator_value_list}')
    print(f'units_exponents_totals:            {units_exponents_totals}')
    #print(f'positive_numerator_symbols:        {positive_numerator_symbols}')
    #print(f'exponent_array_custom:             {exponent_array_custom}')
    #print(f'negative_numerator_symbols:        {negative_numerator_symbols}')
    print(f'current_value:                     {current_value}')
    if function:
        print(f"{'-'*98}\n")

def main_units():
    """ Calls a series of primary functions to process current data and update the GUI display. Called by entry_unit(), update_units_and_values(),
        invert(), clear(), and favorites_trigger(). Two new lines signify the end of a main_units() call. """
    print("main_units():\n") # Optional.
    consolidate_current_unit_list() # Updates current_unit_consolidated, current_unit_custom, positive_numerator_custom_array, and negative_numerator_custom_array.
    name = name_creator() # Updates and returns current_unit_name.
    unit_data_finder(name) # Updates conversions and quantities displays.
    prefix_finder() # Updates units_exponents_totals and current_unit_reduced.
    units_exponents_totals_to_compound_units_list() # Processes data for display.
    current_unit_custom_to_significand_order_units() # Processes data for display.
    significand_order_units_to_current_display() # Processes data for display.
    set_current_display() # Updates current unit display.
    print_sets(False) # Optional.
    print(f"\n{'-'*98}") # Optional.

def load_notes():
    """ Loads saved notes for the lower subframe. """
    print("load_notes():") # Optional.
    notes_index = 1
    with open("database_notes.txt", 'r', encoding='utf-8') as notes: # Loads previous notes from a text file.
        for line in notes.readlines():
            if line.strip() == ">>": # Arbitrary trigger defined for the database_notes.txt file.
                notes_index += 1
                continue
            if notes_index == 1:
                textbox = textbox_1
            elif notes_index == 2:
                textbox = textbox_2
                notes = textbox_1.get('1.0', 'end') # Removes whitespace from textbox_1.
                textbox_1.delete('1.0', 'end')
                textbox_1.insert('end', notes.strip())
            elif notes_index == 3:
                textbox = textbox_3
                notes = textbox_2.get('1.0', 'end') # Removes whitespace from textbox_2.
                textbox_2.delete('1.0', 'end')
                textbox_2.insert('end', notes.strip())
            textbox.insert('end', line.strip())
            textbox.insert('end', "\n")
        notes = textbox.get('1.0', 'end') # Removes whitespace from textbox_3.
        textbox.delete('1.0', 'end')
        textbox.insert('end', notes.strip())
    notes_toggle()
    print() # Optional.

def load_units():
    """ Converts an existing text file to a global dictionary of saved values. ={"} """
    print("load_units():") # Optional.
    global unit_database
    unit_database.clear() # Prepares the global list for updating.
    with open("database_units.txt", 'r', encoding='utf-8') as database:
        units_list = list(zip(*(line.strip().split('\t') for line in database)))
    names_list = list(units_list[0]) # Produces a list of unit names from the specified text file.
    data_list = [] # Initializes a list of lists from the specified text file.
    for i in range(len(units_list)-1): # Produces a list of lists from the specified text file.
        data_list.append(list(units_list[i+1]))
    for i in range(len(names_list)):
        column_data = [] # Ex=['d', '0', 'l;s;r', 'm']
        for j in range(len(data_list)):
            column_data.append(data_list[j][i])
        unit_database[names_list[i]] = column_data
    conversion_database.clear()
    with open("database_conversions.txt", 'r', encoding='utf-8') as database:
        conversions_list = list(zip(*(line.strip().split('\t') for line in database)))
    names_list = list(conversions_list[0]) # Produces a list of units from the specified text file.
    convert_list = [string.replace("'", "") for string in conversions_list[1]]
    convert_list = [string.strip("[]").split(", ") for string in convert_list]
    value_list = [float(string) for string in conversions_list[2]]
    data_list = []
    data_list.append(convert_list)
    data_list.append(value_list)
    for i in range(len(names_list)):
        column_data = [] # Ex=['d', '0', 'l;s;r', 'm']
        for j in range(len(data_list)):
            column_data.append(data_list[j][i])
        conversion_database[names_list[i]] = column_data
    print() # Optional.

def save_command():
    """ Opens a text file and calls the current application's save routine. """
    with open("database_notes.txt", 'w', encoding='utf-8') as notes:
        print(textbox_1.get('1.0', 'end'), file=notes)
        print(">>", file=notes)
        print(textbox_2.get('1.0', 'end'), file=notes)
        print(">>", file=notes)
        print(textbox_3.get('1.0', 'end'), file=notes)
    if application_index == 1:
        save_units()
    else:
        save_symbols()

def save_units():
    """ Saves data within the Unit Manager application. """
    print("save_units():") # Optional.
    global unit_database
    with open("database_units.txt", 'w', encoding='utf-8') as database:
        for name in unit_database: # Assumes notation_database_dictionary.
            name_and_data = f"{name}" # Initializes the string of tab-spaced values.
            for data in unit_database[name]:
                name_and_data = f"{name_and_data}\t{data}"
            print(name_and_data, file=database)
    sleep(0.5) # Optional, though errors may occur otherwise.
    print() # Optional.

def data_return(event, cell):
    """ Updates the database with the current entry. Called when return/enter has been pressed in Unit Manager. """
    global unit_database
    print(f"data_return():") # Optional.
    data = cell.get()  # Gets text/data from the specified cell.
    new_list = []
    if current_unit_name[0] not in unit_database:
        unit_database[current_unit_name[0]] = ["", ""]
    if str(cell) == ".!frame.!frame.!entry": # Updates the Common Conversions entry for the current unit.
        old_data, new_data = list(unit_database[current_unit_name[0]])[1], str(data)
        new_list.append(new_data)
        new_list.append(old_data)
    else: # Updates the Related Quantities entry for the current unit.
        old_data, new_data = list(unit_database[current_unit_name[0]])[0], str(data)
        new_list.append(old_data)
        new_list.append(new_data)
    unit_database[current_unit_name[0]] = new_list
    print() # Optional.

def entry_unit(event, unit, operator):
    """ Adds or removes a user-defined unit from current_unit_list, positive_numerator_symbols, and negative_numerator_symbols. 
        For the operator variable, "×" corresponds to multiplication, and ÷ corresponds to division. """
    print("entry_unit():\n") # Optional.
    #print(f"event: {event}\nunit: {unit}\noperator: {operator}") # Optional
    global entry_unit_index, current_value
    if event:
        unit = unit_entry.get()
        root.focus()
    if unit: # Prevents errors following a null entry.
        if unit == "C" and current_database_file == "database_iso.txt":
            index = positive_numerator_symbols.index(unit)
            update_units_and_values(index, operator, convert=True)
        else: # True for units, as opposed to keywords.
            if "." in unit or unit.isdigit(): # Multiplies or divides the current value by the entry value.
                #print(f"old current_value: {current_value}")
                if operator == "×":
                    current_value *= float(unit)
                else:
                    current_value /= float(unit)
                #print(f"new current_value: {current_value}")
                main_units()
            else: # True for "÷". Adds the unit to the global list of base and non-base units.
                if unit not in positive_numerator_symbols:
                    negative_numerator_unit, positive_denominator_unit = "-" + unit, "_" + unit
                    positive_numerator_symbols.append(unit)
                    negative_numerator_symbols.append(negative_numerator_unit)
                    positive_denominator_symbols.append(positive_denominator_unit)
                    numerator_value_list.append(0)
                    denominator_value_list.append(0)
                    entry_unit_index += 1
                    update_units_and_values(entry_unit_index, operator)
                else:
                    index = positive_numerator_symbols.index(unit)
                    update_units_and_values(index, operator)

def populate_exponent_codes():
    """ Handles errors by lengthening the global list of exponents. """
    #print(f"populate_exponent_codes():") # Optional.
    #print(f"exponent_codes: {exponent_codes}") # Optional.
    global exponent_codes
    zero_to_nine = ["\u2070", "\u00b9", "\u00b2", "\u00b3", "\u2074", "\u2075", "\u2076", "\u2077", "\u2078", "\u2079"]
    if (len(exponent_codes) == 0) and (len(current_unit_list) < len(exponent_codes)+10):
        exponent_codes = zero_to_nine
    else:
        if (len(current_unit_list) > len(exponent_codes)+10):
            exponent_codes = zero_to_nine
            for i in range(10):
                if len(current_unit_list) >= 10 * i:
                        if i != 0:
                            for j in range(10):
                                exponent_codes.append(zero_to_nine[i] + zero_to_nine[j])
                else:
                    break
        else:    
            for i in range(10):
                if len(exponent_codes) == 10 * i:
                    for j in range(10):
                        exponent_codes.append(zero_to_nine[i] + zero_to_nine[j])
                    break

def update_units_and_values(button_index, operator, convert=False):
    """ Calls prefix_value_tuple() and updates current_unit_list, numerator_value_list, denominator_value_list, and current_value. 
        This is a fundamental function that runs immediately after any unit is entered. def entry_unit(event, unit, operator): """
    print("update_units_and_values():") # Optional.
    global numerator_value_list, denominator_value_list, current_value
    #print(f"button_index: {button_index}\noperator: {operator}") # Optional.
    if button_index == 1 and current_database_file == "database_iso.txt" and not convert:
            entry_unit("", "A", operator)
    else:
        prefix_tuple = prefix_value_tuple(button_index) # Produces a tuple that contains a prefix symbol and its value. Ex=("M", 1000000)
        #print(f"numerator_value_list: {numerator_value_list}\ndenominator_value_list: {denominator_value_list}\n") # Optional.
        if fraction_button.config('relief')[-1] == 'raised': # Adds or removes a numerator from the exponent of the specified unit.
            if operator == "×":
                if numerator_value_list[button_index] == 0: # Updates the prefix value of the numerator for a previous value of zero.
                    numerator_value_list[button_index] = prefix_tuple # Sets the prefix value for the entered unit.
                else: # Updates the prefix value from a nonzero value.
                    numerator_value_list[button_index] *= prefix_tuple # Updates the prefix value for the entered unit.
                if negative_numerator_symbols[button_index] in current_unit_list: # Removes the symbol from current_unit_list.
                    current_unit_list.remove(negative_numerator_symbols[button_index])
                    if negative_numerator_symbols[button_index] not in current_unit_list: # Only true for an exponent of zero. Moves leftover value to current_value.
                        if denominator_value_list[button_index] == 0: # Initializes denominator_value_list for computation.
                            denominator_value_list[button_index] = 1
                        leftover_value = numerator_value_list[button_index] / denominator_value_list[button_index]
                        current_value *= leftover_value
                        numerator_value_list[button_index] *= 0 # Resets the prefix counter for that unit.
                        denominator_value_list[button_index] *= 0
                else: # Adds the symbol to current_unit_list.
                    current_unit_list.append(positive_numerator_symbols[button_index])
            else: # True for "÷".
                if denominator_value_list[button_index] == 0: # Updates denominator_value_list.
                    denominator_value_list[button_index] = prefix_tuple
                else:
                    denominator_value_list[button_index] *= prefix_tuple
                if positive_numerator_symbols[button_index] in current_unit_list: # Removes the symbol from current_unit_list.
                    current_unit_list.remove(positive_numerator_symbols[button_index])
                    if positive_numerator_symbols[button_index] not in current_unit_list: # Updates current_value if necessary.
                        if numerator_value_list[button_index] == 0: # Initializes denominator_value_list for computation.
                            numerator_value_list[button_index] = 1
                        leftover_value = numerator_value_list[button_index] / denominator_value_list[button_index]
                        current_value *= leftover_value
                        numerator_value_list[button_index] *= 0 # Resets the prefix counter for that unit.
                        denominator_value_list[button_index] *= 0
                else: # Adds the symbol to current_unit_list.
                    current_unit_list.append(negative_numerator_symbols[button_index])
        else: # Adds or removes a denominator from the exponent of the specified unit.
            if operator == "×":
                current_unit_list.append(positive_denominator_symbols[button_index])
                if positive_numerator_symbols[button_index] not in current_unit_list and negative_numerator_symbols[button_index] not in current_unit_list:
                    current_unit_list.append(positive_numerator_symbols[button_index])
            else: # True for "÷".
                if positive_denominator_symbols[button_index] in current_unit_list: # Removes a denominator element from the current list.
                    positive_unit = positive_denominator_symbols[button_index].replace("_", "")
                    negative_unit = "-" + positive_unit
                    denominator_count = current_unit_list.count(positive_denominator_symbols[button_index])
                    if (denominator_count == 1) and ((current_unit_list.count(positive_unit) == 1) or (current_unit_list.count(negative_unit) == 1)):
                        try:
                            current_unit_list.remove(positive_numerator_symbols[button_index])
                            #print(True) # Optional.
                        except:
                            current_unit_list.remove(negative_numerator_symbols[button_index])
                            #print(False) # Optional.
                    current_unit_list.remove(positive_denominator_symbols[button_index])
        print() # Optional.
        main_units()

def consolidate_current_unit_list():
    """ Uses current_unit_list to build current_unit_consolidated, current_unit_custom, positive_numerator_custom_array, and negative_numerator_custom_array.
        It converts duplicate units to a single unit with a nonzero exponent and converts ("simplifies") user-defined units to their base equivalent for naming and
        data recollection. <×/÷> """
    print("consolidate_current_unit_list():") # Optional.
    positive_numerator_list, negative_numerator_list = [], [] # Initializes simplified exponent arrays to be saved globally as <±>_numerator_exponent_array.
    positive_denominator_list = [] # Initializes simplified exponent arrays to be saved globally as positive_denominator_exponent_array.
    positive_numerator_custom, negative_numerator_custom = [], [] # Initializes the unsimplified numerator exponent arrays.
    positive_denominator_custom = [] # Initializes an unsimplified denominator exponent array.
    units, units_display = [], [] # Initializes the simplified and unsimplified lists of current units with respective exponents for current_unit_consolidated.
    temporary_unit_list = current_unit_list[:] # Initializes a copy of the current unit list.
    if len(positive_numerator_symbols) > 8: # Checks for entry_unit occurances and converts to base units, if applicable.
        for i in range(len(positive_numerator_symbols)-8): # Iterates over each non-base unit in positive_numerator_symbols.
            #print(f"positive_numerator_symbols[i]: {positive_numerator_symbols[i]}") # Optional.
            positive_equivalent = entry_data_finder(positive_numerator_symbols[(-1)-i]) # Checks for existing positive data and returns a list. Ex=["cd", "-m", "-m"]
            negative_equivalent = entry_data_finder(negative_numerator_symbols[(-1)-i]) # Checks for existing negative data and returns a list. Ex=["-cd", "m", "m"]
            if positive_equivalent: # Replaces entry_unit with positive_equivalent, if applicable.
                while positive_numerator_symbols[-1-i] in temporary_unit_list: # Looks for each occurance of entry_unit in current_unit_list.
                    if positive_equivalent[0] != "1": # Accounts for non-base units that are equal to unity.
                        temporary_unit_list.remove(positive_numerator_symbols[-1-i])
                        temporary_unit_list.extend(positive_equivalent)
                    else:
                        temporary_unit_list.remove(positive_numerator_symbols[-1-i])
            if negative_equivalent: # Replaces entry_unit with negative_equivalent, if applicable.
                while negative_numerator_symbols[-1-i] in temporary_unit_list: # Looks for each occurance of entry_unit in current_unit_list.
                    temporary_unit_list.remove(negative_numerator_symbols[-1-i])
                    if positive_equivalent[0] != "1": # Accounts for non-base units that are equal to unity.
                        temporary_unit_list.extend(negative_equivalent)
        for j in range(7): # Iterates over all base units to simplify temporary_unit_list.
            while positive_numerator_symbols[j] in temporary_unit_list and negative_numerator_symbols[j] in temporary_unit_list:
                temporary_unit_list.remove(positive_numerator_symbols[j])
                temporary_unit_list.remove(negative_numerator_symbols[j])
    for i in range(len(positive_numerator_symbols)): # Searches current_unit_list for base units and adds the count to the respective list.
        positive_numerator_list.append(temporary_unit_list.count(positive_numerator_symbols[i]))
        negative_numerator_list.append(temporary_unit_list.count(negative_numerator_symbols[i]))
        positive_denominator_list.append(temporary_unit_list.count(positive_denominator_symbols[i]))
        fractional_exponent_to_tuple(positive_numerator_list[i], negative_numerator_list[i], positive_denominator_list[i], "base") # Updates exponent_tuple_array[i].
        positive_numerator_custom.append(current_unit_list.count(positive_numerator_symbols[i]))
        negative_numerator_custom.append(current_unit_list.count(negative_numerator_symbols[i]))
        positive_denominator_custom.append(current_unit_list.count(positive_denominator_symbols[i]))
        fractional_exponent_to_tuple(positive_numerator_custom[i], negative_numerator_custom[i], positive_denominator_custom[i], "custom") # Updates exponent_tuple_array[i].
    positive_numerator_custom_array.clear()
    negative_numerator_custom_array.clear()
    positive_numerator_custom_array.extend(positive_numerator_custom) # Updates a global list.
    negative_numerator_custom_array.extend(negative_numerator_custom) # Updates a global list.
    print() # Optional.

def fractional_exponent_to_tuple(positive_numerator, negative_numerator, positive_denominator, input_list):
    """ Simplifies the exponent of each unit an populates a list of lists with two elements: the numerator and denominator of each respective exponent. """
    #print("fractional_exponent_to_tuple():") # Optional.
    #print(f"positive_numerator: {positive_numerator}\nnegative_numerator: {negative_numerator}\npositive_denominator: {positive_denominator}\ninput_list: {input_list}") # Optional.
    if positive_numerator: # Returns numerator to be multiplied by the denominator.
        numerator = Fraction(positive_numerator, 1)
    elif negative_numerator: # Returns numerator to be multiplied by the denominator.
        numerator = Fraction(-negative_numerator, 1)
    else:
        numerator = Fraction(0, 1)
    if positive_denominator: # Returns denominator to be multiplied by the numerator.
        denominator = Fraction(1, positive_denominator+1)
    else:
        denominator = Fraction(1, 1)
    final_numerator, final_denominator = (numerator * denominator).numerator, (numerator * denominator).denominator
    #print(f"(numerator, denominator): ({numerator}, {denominator})") # Optional.
    exponent_list = [final_numerator, final_denominator]
    if input_list == "base":
        exponent_tuple_array.append(exponent_list)
    else: # True for "custom".
        exponent_tuple_array_custom.append(exponent_list)

def name_creator():
    """ Generates a name for the current unit that may correspond to a database entry in unit_data_finder. """
    print("name_creator():") # Optional.
    global exponent_array, exponent_array_custom
    #print(f"exponent_tuple_array: {exponent_tuple_array}") # Ex=[[0, 1], [0, 1], [0, 1], [0, 1], [3, 2], [0, 1], [0, 1], [0, 1]] # Optional.
    #print(f"exponent_tuple_array_custom: {exponent_tuple_array_custom}") # Ex=[[0, 1], [0, 1], [0, 1], [0, 1], [3, 2], [0, 1], [0, 1], [0, 1]] # Optional.
    negative_name_list, negative_name_list, exponent_numerator_array, exponent_numerator_custom_array, units_display, counter = [], [], [], [], [], int(0)
    for i in range(len(exponent_tuple_array)):
        exponent_numerator_array.append(exponent_tuple_array[i][0])
    for i in range(len(exponent_tuple_array_custom)):
        exponent_numerator_custom_array.append(exponent_tuple_array_custom[i][0])
    if any(exponent_numerator_array) or any(exponent_numerator_custom_array): # False for unity.
        name_list, positive_name_list, negative_name_list = [], [], [] # Clears unit name and initializes temporary lists.
        for i in range(len(exponent_tuple_array_custom)): # Cycles through each base and non-base unit in the current list.
            if len(positive_numerator_symbols) > 8: # Optional. Moves non-base units in front of base units.
                if i + 8 >= len(positive_numerator_symbols):
                    i = counter
                    counter = int(counter) + 1
                else:
                    i += 8
            populate_exponent_codes()
            if exponent_tuple_array_custom[i] != [0, 1]: # Specifies nonzero exponents. Ex=-2
                if exponent_tuple_array_custom[i][0] > 0: # Specifies positive exponents. Ex=2
                    if exponent_tuple_array_custom[i][1] == 1: # Specifies positive integer exponents.
                        if exponent_tuple_array_custom[i][0] == 1:
                            units_display.append(positive_numerator_symbols[i])
                        else:
                            #print(f"positive_numerator_symbols: {positive_numerator_symbols}) # Optional
                            #print(exponent_codes: {exponent_codes}\nexponent_tuple_array_custom: {exponent_tuple_array_custom}") # Optional
                            #print(i) # Optional.
                            display_unit = positive_numerator_symbols[i] + exponent_codes[exponent_tuple_array_custom[i][0]]
                            units_display.append(display_unit)
                    else: # Specifies positive fractional exponents of base units. True if exponent_tuple_array_custom[i][1] != 1.
                        display_unit = positive_numerator_symbols[i] + exponent_codes[exponent_tuple_array_custom[i][0]]
                        display_unit = display_unit + "\u141F" + exponent_codes[exponent_tuple_array_custom[i][1]]
                        units_display.append(display_unit)
                else: # Specifies negative exponents. Ex=-2
                    exponent_tuple_array_custom[i][0] *= -1
                    if exponent_tuple_array_custom[i][1] == 1: # Specifies negative integer exponents.
                        display_unit = positive_numerator_symbols[i] + "\u207B" + exponent_codes[exponent_tuple_array_custom[i][0]]
                    else: # Specifies negative fractional exponents of base units. True if exponent_tuple_array_custom[i][1] != 1.
                        display_unit = positive_numerator_symbols[i] + "\u207B" + exponent_codes[exponent_tuple_array_custom[i][0]]
                        display_unit = display_unit + "\u141F" + exponent_codes[exponent_tuple_array_custom[i][1]]
                    units_display.append(display_unit)
        for i in range(len(exponent_tuple_array)): # Cycles through each base and non-base unit in the current list.
            if exponent_tuple_array[i] != [0, 1]: # Specifies nonzero exponents. Ex=-2
                if i < 8: # Specifies base units.
                    database = unit_names
                else: # Specifies non-base units.
                    database = positive_numerator_symbols
                if exponent_tuple_array[i][0] > 0: # Specifies positive exponents. Ex=2
                    if exponent_tuple_array[i][1] == 1: # Specifies positive integer exponents.
                        if exponent_tuple_array[i][0] == 1: # Accounts for all exponents that simplify to [1, 1].
                            positive_name_list.append(database[i])
                        else: # Accounts for [X, 1].
                            if exponent_tuple_array[i][0] == 2:
                                positive_name_list.append(f"{database[i]}_squared")
                            elif exponent_tuple_array[i][0] == 3:
                                positive_name_list.append(f"{database[i]}_cubed")
                            else:
                                positive_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}")
                    else: # Specifies positive fractional exponents of base units. True if exponent_tuple_array[i][1] != 1.
                        if exponent_tuple_array[i][1] == 2: # Accounts for [X, 2].
                            if exponent_tuple_array[i][0] == 2:
                                positive_name_list.append(f"{database[i]}")
                            elif exponent_tuple_array[i][0] == 4:
                                positive_name_list.append(f"{database[i]}_squared")
                            elif exponent_tuple_array[i][0] == 6:
                                positive_name_list.append(f"{database[i]}_cubed")
                            else:
                                positive_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}/2")
                        elif exponent_tuple_array[i][1] == 3: # Accounts for [X, 3].
                            if exponent_tuple_array[i][0] == 3:
                                positive_name_list.append(f"{database[i]}")
                            elif exponent_tuple_array[i][0] == 6:
                                positive_name_list.append(f"{database[i]}_squared")
                            else:
                                positive_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}/3")
                        else: # Accounts for [X, Y].
                            positive_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}/{exponent_tuple_array[i][1]}")
                    positive_name_list.append("_")
                else: # Specifies negative exponents. Ex=-2
                    exponent_tuple_array[i][0] *= -1
                    if exponent_tuple_array[i][1] == 1: # Specifies negative integer exponents.
                        if exponent_tuple_array[i][0] == 1: # Accounts for [1, 1].
                            negative_name_list.append(database[i])
                        else: # Accounts for [X, 1].
                            if exponent_tuple_array[i][0] == 2:
                                negative_name_list.append(f"{database[i]}_squared")
                            elif exponent_tuple_array[i][0] == 3:
                                negative_name_list.append(f"{database[i]}_cubed")
                            else:
                                negative_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}")
                    else: # Specifies negative fractional exponents of base units. True if exponent_tuple_array[i][1] != 1.
                        if exponent_tuple_array[i][1] == 2: # Accounts for [X, 2].
                            if exponent_tuple_array[i][0] == 2:
                                negative_name_list.append(f"{database[i]}")
                            elif exponent_tuple_array[i][0] == 4:
                                negative_name_list.append(f"{database[i]}_squared")
                            elif exponent_tuple_array[i][0] == 6:
                                negative_name_list.append(f"{database[i]}_cubed")
                            else:
                                negative_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}/2")
                        elif exponent_tuple_array[i][1] == 3: # Accounts for [X, 3].
                            if exponent_tuple_array[i][0] == 3:
                                negative_name_list.append(f"{database[i]}")
                            elif exponent_tuple_array[i][0] == 6:
                                negative_name_list.append(f"{database[i]}_squared")
                            else:
                                negative_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}/3") # Adds the unit and exponent placeholder to the current name
                        else: # Accounts for [X, Y].
                            negative_name_list.append(f"{database[i]}_{exponent_tuple_array[i][0]}/{exponent_tuple_array[i][1]}")
                    negative_name_list.append("_")
        name_list.clear()
        if negative_name_list:
            positive_name_list.append("per_")
        if positive_name_list and negative_name_list: # Adds a trailing underscore if negative exponents are present.
            name_list.extend(positive_name_list)
            try:
                del negative_name_list[-1]
                name_list.extend(negative_name_list)
            except:
                name_list.extend(negative_name_list)
        elif positive_name_list:
            del positive_name_list[-1]
            name_list.extend(positive_name_list)
        else:
            try:
                del negative_name_list[-1]
                name_list.extend(negative_name_list)
            except:
                name_list.extend(negative_name_list)
        unit_name = "".join(name_list)
    if not any(exponent_numerator_array):
        unit_name = "one" # Sets the default value to unity.
    positive_units_display, negative_units_display = [], [] # Initializes temporary lists to sort units with positive and negative exponents.
    for i in range(len(units_display)):
        if "⁻" in units_display[i]:
            negative_units_display.append(units_display[i])
        else:
            positive_units_display.append(units_display[i])
    units_display.clear()
    units_display.extend(positive_units_display)
    units_display.extend(negative_units_display)
    current_unit_custom.clear()
    current_unit_custom.extend(units_display)
    current_unit_consolidated.clear() # Initializes a global list for updating.
    if units_display: # Verifies that the current unit is not one.
        current_unit_consolidated.extend(units_display) # Updates a global list.
    else: # True if the current unit is one.
        current_unit_consolidated.extend("1") # Updates a global list.
    current_unit_name.clear()
    current_unit_name.append(unit_name) # Updates a global list.
    exponent_array, exponent_array_custom = exponent_tuple_array, exponent_tuple_array_custom # Updates global values.
    exponent_tuple_array.clear()
    exponent_tuple_array_custom.clear()
    print() # Optional.
    return unit_name

def prefix_finder():
    """ Called by main_units() to update units_exponents_totals and current_unit_reduced. """
    print("prefix_finder():") # Optional.
    global units_exponents_totals
    #print(f"old units_exponents_totals: {units_exponents_totals}") # Optional.
    units_exponents_totals.clear() # Initializes list for data collection.
    current_unit_reduced.clear() # Initializes list for exponent removal.
    symbols_indexes_exponents, counter = [], 0
    current_unit_reduced.extend(current_unit_custom[:]) # Initializes list for exponent removal.
    for i in range(len(current_unit_custom)): # Removes numerical exponents and produces a list of their values. Ex=["m²", "s⁻²"]
        symbol_index_exponent = [current_unit_custom[i]] # Initializes a list of data. Ex=["m²"]
        #print(f"current_unit_custom: {current_unit_custom}") # Optional.
        if "ᐟ" in current_unit_custom[i]:
            symbol_index_exponent.append(4) # Unknown. Removal seemed to cause an error.
            symbol_index_exponent.append(1)
        else:
            for j in range(len(exponent_symbols)): # Removes numerical exponents. range=10
                number = current_unit_reduced[i].count(exponent_symbols[j])
                #print(f"old current_unit_reduced[i]: {current_unit_reduced[i]}") # Optional.
                current_unit_reduced[i] = current_unit_reduced[i].replace(exponent_symbols[j], "", number)
                #print(f"new current_unit_reduced[i]: {current_unit_reduced[i]}") # Optional.
            if current_unit_reduced[i][-1] == "⁻": # Removes minus sign.
                current_unit_reduced[i] = current_unit_reduced[i].replace("⁻", "")
                if current_unit_reduced[i] in positive_numerator_symbols:
                    index = positive_numerator_symbols.index(current_unit_reduced[i])
                    exponent = negative_numerator_custom_array[index]
                    symbol_index_exponent.append(index)
                    symbol_index_exponent.append(exponent)
            else:
                if current_unit_reduced[i] in positive_numerator_symbols:
                    index = positive_numerator_symbols.index(current_unit_reduced[i])
                    exponent = positive_numerator_custom_array[index] # exponent_tuple_array[index][0]
                    symbol_index_exponent.append(index)
                    symbol_index_exponent.append(exponent)
        symbols_indexes_exponents.append(symbol_index_exponent)
    #print(f"numerator_value_list: {numerator_value_list}\ndenominator_value_list: {denominator_value_list}") # Optional.
    for i in range(len(positive_numerator_symbols)): # Finds optimal units with respect to the exponent of each current unit.
        if len(positive_numerator_symbols) > 8: # Optional. Moves non-base units in front of base units.
            if i + 8 >= len(positive_numerator_symbols):
                i = counter
                counter = int(counter) + 1
            else:
                i += 8
        #print(f"positive_numerator_symbols[i]: {positive_numerator_symbols[i]}") # Optional.
        for j in range(len(symbols_indexes_exponents)): # The index j corresponds to each unit in symbols_indexes_exponents.
            if symbols_indexes_exponents[j][1] == i: # Targets units with nonzero exponents. The index i corresponds to a particular unit in positive_numerator_symbols.
                units_exponent_total = [symbols_indexes_exponents[j][0], positive_numerator_symbols[i], symbols_indexes_exponents[j][2]] # Ex=['s⁻²', 's', 2]
                if numerator_value_list[i] != 0 and denominator_value_list[i] != 0: # Calculates total value for each unit.
                    #print(f"negative_numerator_custom_array: {negative_numerator_custom_array}") # Optional.
                    if negative_numerator_custom_array[i] == 0:
                        total_value = numerator_value_list[i] / denominator_value_list[i]
                    else:
                        total_value = denominator_value_list[i] / numerator_value_list[i]
                elif numerator_value_list[i] != 0:
                    total_value = numerator_value_list[i]
                elif denominator_value_list[i] != 0:
                    total_value = denominator_value_list[i]
                else:
                    total_value = 1
                units_exponent_total.append(total_value) # Adds the total.  # Ex=['s⁻²', 's', 2, 1000000]
                units_exponents_totals.append(units_exponent_total)
            else:
                continue
    #print(f"new units_exponents_totals: {units_exponents_totals}") # Optional.
    print() # Optional.

def units_exponents_totals_to_compound_units_list():
    """ Looks at units_exponents_totals to determine compound prefixes, output compound_units_list, and update current_value. """
    print("units_exponents_totals_to_compound_units_list():") # Optional.
    global current_value, compound_units_list
    compound_units_list.clear()
    relative_total = 0
    for i in range(len(units_exponents_totals)): # Looks through all current units.
        compound_unit_list = [units_exponents_totals[i][0]] # Adds the unit and associated exponent to a temporary list for compound_units_list.
        if units_exponents_totals[i][2] != 0: # Prevents a possible error. Might be optional.
            relative_total = units_exponents_totals[i][3] ** (1 / units_exponents_totals[i][2])
        if len(str(units_exponents_totals[i][3])) > 12: # Fixes rounding errors for 
            if str(units_exponents_totals[i][3])[10] == "9" and str(units_exponents_totals[i][3][11]) == "9":
                units_exponents_totals[i][3] += (units_exponents_totals[i][3] / 100000000000)
        if (relative_total + (relative_total / 100000000000)) >= (10 ** 24): # True if the unit's value corresponds to that of the repespective prefix.
            compound_unit_list.append("Y")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 24) ** units_exponents_totals[i][2])
        elif (10 ** 21) <= (relative_total + (relative_total / 100000000000)) < (10 ** 24):
            compound_unit_list.append("Z")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 21) ** units_exponents_totals[i][2])
        elif (10 ** 18) <= (relative_total + (relative_total / 100000000000)) < (10 ** 21):
            compound_unit_list.append("E")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 18) ** units_exponents_totals[i][2])
        elif (10 ** 15) <= (relative_total + (relative_total / 100000000000)) < (10 ** 18):
            compound_unit_list.append("P")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 15) ** units_exponents_totals[i][2])
        elif (10 ** 12) <= (relative_total + (relative_total / 100000000000)) < (10 ** 15):
            compound_unit_list.append("T")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 12) ** units_exponents_totals[i][2])
        elif (10 ** 9) <= (relative_total + (relative_total / 100000000000)) < (10 ** 12):
            compound_unit_list.append("G")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 9) ** units_exponents_totals[i][2])
        elif (10 ** 6) <= (relative_total + (relative_total / 100000000000)) < (10 ** 9):
            compound_unit_list.append("M")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 6) ** units_exponents_totals[i][2])
        elif (10 ** 3) <= (relative_total + (relative_total / 100000000000)) < (10 ** 6):
            compound_unit_list.append("k")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 3) ** units_exponents_totals[i][2])
        elif (10 ** 2) <= (relative_total + (relative_total / 100000000000)) < (10 ** 3):
            compound_unit_list.append("h")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 2) ** units_exponents_totals[i][2])
        elif (10 ** 1) <= (relative_total + (relative_total / 100000000000)) < (10 ** 2):
            compound_unit_list.append("da")
            leftover_value = units_exponents_totals[i][3] / ((10 ** 1) ** units_exponents_totals[i][2])
        elif (10 ** -2) < (relative_total - (relative_total / 100000000000)) <= (10 ** -1):
            compound_unit_list.append("d")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -1) ** units_exponents_totals[i][2])
        elif (10 ** -3) < (relative_total - (relative_total / 100000000000)) <= (10 ** -2):
            compound_unit_list.append("c")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -2) ** units_exponents_totals[i][2])
        elif (10 ** -6) < (relative_total - (relative_total / 100000000000)) <= (10 ** -3):
            compound_unit_list.append("m")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -3) ** units_exponents_totals[i][2])
        elif (10 ** -9) < (relative_total - (relative_total / 100000000000)) <= (10 ** -6):
            compound_unit_list.append("μ")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -6) ** units_exponents_totals[i][2])
        elif (10 ** -12) < (relative_total - (relative_total / 100000000000)) <= (10 ** -9):
            compound_unit_list.append("n")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -9) ** units_exponents_totals[i][2])
        elif (10 ** -15) < (relative_total - (relative_total / 100000000000)) <= (10 ** -12):
            compound_unit_list.append("p")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -12) ** units_exponents_totals[i][2])
        elif (10 ** -18) < (relative_total - (relative_total / 100000000000)) <= (10 ** -15):
            compound_unit_list.append("f")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -15) ** units_exponents_totals[i][2])
        elif (10 ** -21) < (relative_total - (relative_total / 100000000000)) <= (10 ** -18):
            compound_unit_list.append("a")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -18) ** units_exponents_totals[i][2])
        elif (10 ** -24) < (relative_total - (relative_total / 100000000000)) <= (10 ** -21):
            compound_unit_list.append("z")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -21) ** units_exponents_totals[i][2])
        elif (10 ** -27) < (relative_total - (relative_total / 100000000000)) <= (10 ** -24):
            compound_unit_list.append("y")
            leftover_value = units_exponents_totals[i][3] / ((10 ** -24) ** units_exponents_totals[i][2])
        else: # True if units_exponents_totals[i][3] is in the interval (10², 10⁻²).
            compound_unit_list.append("")
            leftover_value = units_exponents_totals[i][3]
        if len(str(leftover_value)) > 12:
            if str(leftover_value)[10] == "9" and str(leftover_value)[11] == "9":
                leftover_value += (leftover_value / 100000000000)
        if "⁻" in units_exponents_totals[i][0]: # Updates the global value for a negative exponent.
            current_value /= leftover_value
        else: # Updates the global value for a positive exponent.
            current_value *= leftover_value # Sometimes results in unnecessarily long floating decimal values.
        compound_units_list.append(compound_unit_list) # Adds the current unit data to compound_units_list.
        #print(f"original value: {units_exponents_totals[i][3]}\nleftover_value: {leftover_value}\ncurrent_value: {current_value}") # Optional.
    #print(f"compound_units_list: {compound_units_list}\n") # Optional.
    print() # Optional.

def current_unit_custom_to_significand_order_units():
    """ Looks at compound_units_list and current_value to output significand_order_units. """
    print("current_unit_custom_to_significand_order_units():") # Optional.
    global significand_order_units, compound_units_list, current_value
    significand, order = 1, 1 # Initializes values.
    if len(str(current_value)) > 12: # Accounts for rounding errors.
            if str(current_value)[10] == "9" and str(current_value)[11] == "9":
                current_value += (current_value / 100000000000)
    if 0.99999 <= current_value <= 1.00001: # True if the value is approximately 1.
        for i in range(30):
            next = current_value * (10 ** (i + 1))
            if next >= 10:
                order = 10 ** (-i)
                break
        significand = current_value / order
    elif current_value < 0.99999:
        for i in range(30):
            next = current_value * (10 ** (i + 1))
            if next > 0.99999:
                order = 10 ** (-(i + 1))
                break
            else:
                continue
        significand = current_value / order
    else:
        for i in range(30):
            next = current_value / (10 ** i)
            if next < 10:
                order = 10 ** i
                break
            else:
                continue
        significand = current_value / order
    if len(str(significand)) < 5:
        significand += 0.001
    elif str(significand)[4] == "5" or str(significand)[4] == "6" or str(significand)[4] == "7" or str(significand)[4] == "8" or str(significand)[4] == "9":
        significand += 0.01 # Rounds up to the nearest hundredth.
    significand = str(significand)[0] + str(significand)[1] + str(significand)[2] + str(significand)[3]
    if significand == "1" or significand == "1.0" or significand == "1.00": # True for unity and approximate unity.
        significand = ""
    significand_order_units = [significand, order, compound_units_list]
    #print(f"significand_order_units: {significand_order_units}") # Optional.
    print()  # Optional.

def significand_order_units_to_current_display():
    """ Writes the current value in scientific notation and attaches current prefixes to their respective units. """
    print("significand_order_units_to_current_display():") # Optional.
    global significand_order_units, current_display
    current_display.clear()
    significand, order, units = significand_order_units[0], significand_order_units[1], significand_order_units[2]
    total_value = "" # Initializes a temporary value for current_display[0].
    if significand != "": # True when the significand is not 1.
        #print(f"significand: {significand}") # Optional.
        if significand[2] == "0" and significand[3] == "0": # Simplifies integer significands.
            total_value += significand[0]
        else:
            total_value += significand # Adds the significand to the temporary string.
    if order >= 1: # Calculates a positive exponent.
        order = str(int(order))
        exponent = order.count("0")
        populate_exponent_codes()
        if exponent == 0: # True if the order is 1.
            total_value += "" # Adds nothing to the temporary string.
        else: # Continues looking for the proper exponent.
            if total_value: # True if the significand is not 1.
                total_value += "×" # Adds the order to the temporary string.
            if 2 <= exponent <= 9:
                for i in range(8):
                    if exponent == (i+2):
                        magnitude = "10" + exponent_codes[i+2]
                        total_value += magnitude
            elif 10 <= exponent <= 19:
                for i in range(10):
                    if exponent == (i+10):
                        magnitude = "10" + exponent_codes[1] + exponent_codes[i]
                        total_value += magnitude
            elif 20 <= exponent <= 29:
                for i in range(10):
                    if exponent == (i+20):
                        magnitude = "10" + exponent_codes[2] + exponent_codes[i]
                        total_value += magnitude
            elif 30 <= exponent <= 39:
                for i in range(10):
                    if exponent ==  (i+30):
                        magnitude = "10" + exponent_codes[3] + exponent_codes[i]
                        total_value += magnitude
            else:
                total_value += "10"
    else: # Calculates a negative exponent.
        order = str(order)
        if "e" in order: # Accounts for "#e-#" notation.
            if order[-2] == "0":
                exponent = int(order[-1])
            else:
                exponent = int(order[-2] + order[-1])
        else:
            exponent = order.count("0")
        #print(f"exponent: {exponent}") # Optional.
        if exponent == 0: # True if the order is 1.
            total_value += "" # Adds nothing to the temporary string.
        else: # Continues looking for the proper exponent.
            if total_value: # True if the significand is not 1.
                total_value += "×" # Adds the order to the temporary string.
            if 2 <= exponent <= 9:
                for i in range(8):
                    if exponent == (i+2):
                        magnitude = "10⁻" + exponent_codes[i+2]
                        total_value += magnitude
            elif 10 <= exponent <= 19:
                for i in range(10):
                    if exponent == (i+10):
                        magnitude = "10⁻" + exponent_codes[1] + exponent_codes[i]
                        total_value += magnitude
            elif 20 <= exponent <= 29:
                for i in range(10):
                    if exponent == (i+20):
                        magnitude = "10⁻" + exponent_codes[2] + exponent_codes[i]
                        total_value += magnitude
            elif 30 <= exponent <= 39:
                for i in range(10):
                    if exponent ==  (i+30):
                        magnitude = "10⁻" + exponent_codes[3] + exponent_codes[i]
                        total_value += magnitude
            else:
                total_value += "10⁻¹"
    #print(f"total_value: {total_value}") # Optional.
    current_display.append(total_value) # Adds the current numerical value in scientific notation.
    for i in range(len(units)):
        unit = units[i][1] + units[i][0]
        current_display.append(unit) # Adds each unit to the list.
    print() # Optional.

def set_current_display():
    """ Sets the main unit display using nonzero values from current_display. """
    print("set_current_display():") # Optional.
    global current_display, display_list
    nonzero_current_display, nonzero_unit_display = [], [] # Initializes lists of nonzero elements of current_display and unit_display.
    display_list, temporary_list = [], [] # Initializes the final display list and a temporary display list.
    if len(current_display) == 0: # Allows for values_button to be toggled at startup.
        current_display.append("")
    for i in range(len(current_display)): # Builds a list of nonzero elements of current_display.
        if current_display[i] != "":
            nonzero_current_display.append(current_display[i])
            if i != 0:
                nonzero_unit_display.append(current_display[i])
    if values_button.config('relief')[-1] == 'sunken': # Shows numerical values.
        if current_display[0] == "": # It might be alright to write "if not current_display[0]".
            temporary_list = ["1"]
            temporary_list.extend(nonzero_current_display)
        else:
            temporary_list = nonzero_current_display
    else: # Hides numerical values.
        if not current_unit_list:
            temporary_list = ["1"]
        else:
            temporary_list = nonzero_unit_display
    #print(f"temporary_list: {temporary_list}") # Optional.
    for i in range(len(temporary_list)): # Organizes the display.
        if temporary_list[i][0].isdigit(): # Places numbers first.
            display_list.append(temporary_list[i])
        else:
            if "⁻" not in temporary_list[i]: # Places units with positive exponents second.
                display_list.append(temporary_list[i])
    for i in range(len(temporary_list)):
        if not temporary_list[i][0].isdigit(): # Places units with negative exponents third.
            if "⁻" in temporary_list[i]:
                display_list.append(temporary_list[i])
    display.set(display_list)
    print() # Optional.

def display_trigger(event):
    """ Sends the units in the current display to the textbox in the lower subframe. Called by clicking inside the display frame. """
    print("display_trigger():\n") # Optional.
    global textbox_index
    if textbox_index == 1:
        textbox = textbox_1
    elif textbox_index == 2:
        textbox = textbox_2
    elif textbox_index == 3:
        textbox = textbox_3
    if display_list:
        display_unit_string = display_list[0]
        if len(display_list) > 1:
            for i in range(len(display_list)-1):
                display_unit_string = f"{display_unit_string}⸱{display_list[i+1]}"
        if textbox.get('-1.0', 'end') != "\n":
            textbox.insert('end', "\n")
        textbox.insert('end', display_unit_string)

def conversions_trigger():
    """ Called when conversions_button is pressed. Copies data from the current unit to the textbox. """
    print("conversions_trigger():\n") # Optional.
    if conversions_text.get().strip():
        unit_data_finder(current_unit_name[0], 1)

def quantities_trigger():
    """ Called when quantities_button is pressed. Copies data from the current unit to the textbox. """
    print("quantities_trigger():\n") # Optional.
    if quantities_text.get().strip():
        unit_data_finder(current_unit_name[0], 2)

def values_toggle():
    """ Called when values_button is pressed. Shows numerical data from current_display. """
    print("values_toggle():\n") # Optional.
    if values_button.config('relief')[-1] == 'sunken':
        values_button.config(relief="raised")
    else:
        values_button.config(relief='sunken')
    set_current_display()

def invert():
    """ Sets current_unit_list to its multiplicative inverse. """
    print("invert():\n") # Optional.
    global current_value
    invert_current_unit_list = []
    for i in range(len(negative_numerator_symbols)):
        for j in range(len(current_unit_list)):
            if current_unit_list[j] == negative_numerator_symbols[i]:
                invert_current_unit_list.append(positive_numerator_symbols[i])
    for i in range(len(positive_numerator_symbols)):
        for j in range(len(current_unit_list)):
            if current_unit_list[j] == positive_numerator_symbols[i]:
                invert_current_unit_list.append(negative_numerator_symbols[i])
    for i in range(len(current_unit_list)):
        if current_unit_list[i][0] == "_":
            invert_current_unit_list.append(current_unit_list[i])
            positive_unit, negative_unit = current_unit_list[i].replace("_", ""), current_unit_list[i].replace("-", "")
            if (positive_unit not in current_unit_list) and (negative_unit not in current_unit_list):
                invert_current_unit_list.append(negative_unit)
    current_unit_list.clear()
    current_unit_list.extend(invert_current_unit_list)
    current_value = current_value ** -1
    main_units()

def clear():
    """ Clears current_unit_list, current_display, numerator_value_list, denominator_value_list, and current_value. """
    print("clear():\n") # Optional.    
    global current_value
    current_unit_list.clear()
    current_display.clear()
    for i in range(len(numerator_value_list)):
        numerator_value_list[i] *= 0
    for i in range(len(denominator_value_list)):
        denominator_value_list[i] *= 0
    current_value = 1
    fraction_set(True)
    prefix_toggle()
    main_units()

def favorites_trigger(csv_units):
    """ Called whenever a saved favorite is toggled. Updates current_unit_list, positive_numerator_symbols, negative_numerator_symbols, numerator_value_list, and 
        denominator_value_list and increments entry_unit_index. Ex_csv_units=['m⁻¹', '-mi', '0;0;0;0;0;0;0;0;1;0', '0;0;0;0;0;0;0;0;0;0', '1.0']"""
    print("favorites_trigger():") # Optional.
    #print(f"old positive_numerator_symbols: {positive_numerator_symbols}\nold negative_numerator_symbols: {negative_numerator_symbols}") # Optional.
    global entry_unit_index, current_value, numerator_value_list, denominator_value_list
    del csv_units[0] # Removes the string of combined units.
    for i in range(len(csv_units)-3):# Adds non-base units to the global list of units.
        if (csv_units[i] not in positive_numerator_symbols) and (csv_units[i] not in negative_numerator_symbols) and (csv_units[i] not in positive_denominator_symbols):
            if csv_units[i][0] == "-": # Removes the negative symbol and adds the new unit positive_numerator_symbols and negative_numerator_symbols.
                temporary_positive_numerator_symbol = csv_units[i].replace("-", "")
                temporary_negative_numerator_symbol = csv_units[i]
                temporary_positive_denominator_symbol = "_" + temporary_positive_numerator_symbol
            else: # Adds the new unit to positive_numerator_symbols and negative_numerator_symbols.
                temporary_positive_numerator_symbol = csv_units[i]
                temporary_negative_numerator_symbol = "-" + temporary_positive_numerator_symbol
                temporary_positive_denominator_symbol = "_" + temporary_positive_numerator_symbol
            positive_numerator_symbols.append(temporary_positive_numerator_symbol)
            negative_numerator_symbols.append(temporary_negative_numerator_symbol)
            positive_denominator_symbols.append(temporary_positive_denominator_symbol)
            numerator_value_list.append(0) # Lengthens numerator_value_list by one element.
            denominator_value_list.append(0) # Lengthens denominator_value_list by one element.
            entry_unit_index += 1 # Keeps track of the index of non-base units.
    current_value = float(csv_units[-1]) # Loads the saved numerical value.
    del csv_units[-1] # Removes the numerical value from the saved list.
    numerator_value_list.clear() # Initializes the numerator prefix values for loading.
    new_numerator_list = csv_units[-1].split(';') # Generates a list of strings that correspond to each  prefix value in the numerator.
    for i in range(len(new_numerator_list)):
        if 0 <= float(new_numerator_list[i]) < 1 and float(new_numerator_list[i]) != 0.0:
            numerator_value_list.append(float(new_numerator_list[i]))
        else:
            numerator_value_list.append(int(new_numerator_list[i]))
    del csv_units[-1]
    denominator_value_list.clear() # Initializes the denominator prefix values for loading.
    new_denominator_list = csv_units[-1].split(';')
    for i in range(len(new_denominator_list)):
        if 0 <= float(new_denominator_list[i]) < 1 and float(new_denominator_list[i]) != 0.0:
            denominator_value_list.append(float(new_denominator_list[i]))
        else:
            denominator_value_list.append(int(new_denominator_list[i]))
    del csv_units[-1]
    while len(numerator_value_list) < len(positive_numerator_symbols):
        numerator_value_list.append(0)
        denominator_value_list.append(0)
    current_unit_list.clear() # Initializes the curent unit list for updating.
    current_unit_list.extend(csv_units) # Adds each saved unit to the current list.
    #print(f"new positive_numerator_symbols: {positive_numerator_symbols}\nnew negative_numerator_symbols: {negative_numerator_symbols}") # Optional.
    print() # Optional.
    main_units()

def favorites_update():
    """ Converts an existing text file to a global list of saved favorites, loads saved favorites, and calls favorites_buttons. """
    print("favorites_update():") # Optional.
    favorites_read = open('database_favorites.txt', 'r', encoding='utf-8') # Loads previous favorites from a text file.
    favorites_saved = favorites_read.readlines() # Produces a list of previous favorites.
    favorites_read = open('database_favorites.txt', 'w', encoding='utf-8') # Loads previous favorites for updating.
    favorites_list.clear() # Prepares the global list for updating.
    for save in favorites_saved: # Adds previous favorites to the global list as comma-separated values.
        units_saved = save.strip()
        favorites_list.append(units_saved)
    unit_consolidated = "⸱".join(current_unit_consolidated) # Converts the current unit for display.
    while len(numerator_value_list) < 15:
        numerator_value_list.append(0)
    while len(denominator_value_list) < 15:
        denominator_value_list.append(0)
    numerator_prefixes = ";".join([str(int) for int in numerator_value_list]) # Initializes the prefix values for saving.
    denominator_prefixes = ";".join([str(int) for int in denominator_value_list]) # Initializes the prefix values for saving.
    if current_unit_list: # True if the current unit is not one.
        if not unit_consolidated: # Produces a list of comma-separated values to be saved.
            unit_consolidated = "1"
            csv_unit_saved = f"{unit_consolidated}, {current_unit_list[0]}, {denominator_prefixes}, {numerator_prefixes}, {float(current_value)}"
        else: # Produces a list of comma-separated values to be saved.
            csv_unit_list = ", ".join(current_unit_list)
            csv_unit_saved = f"{unit_consolidated}, {csv_unit_list}, {denominator_prefixes}, {numerator_prefixes}, {float(current_value)}"
    if not current_unit_list: # True if the current unit is one.
        if not current_display: # True at startup.
            csv_unit_saved = ""
        else:
            csv_unit_saved = f"1, {denominator_prefixes}, {numerator_prefixes}, {float(current_value)}"
    if csv_unit_saved in favorites_list: # Checks if the current unit is already in favorites.
        favorites_list.remove(csv_unit_saved) # Removes current unit from the global list.
        print(f"Favorite removed: {unit_consolidated}") # Optional.
    else: # Adds current unit to the global list.
        if csv_unit_saved: # False at startup.
            favorites_list.append(csv_unit_saved)
            print(f"Favorite added: {unit_consolidated}") # Optional.
    for save in favorites_list: # Updates the text file.
        print(save, file=favorites_read)
    favorites_read.close() # Closes the updated text file.
    favorites.delete('1.0', 'end') # Prepares the favorites frame for updating.
    #favorites.insert('end', favorites_list) # Adds text to the favorites frame.
    print() # Optional.
    favorites_buttons() # Updates the favorites frame.

def favorites_buttons():
    """ Populates a horizontal list of buttons that correspond to saved units. """
    print(f"favorites_buttons():") # Optional.
    for button in favorites.place_slaves(): # Prepares the favorites display for updating.
        button.place_forget() # Removes all prior buttons.
    button_0, button_1, button_2, button_3 = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar() # Initializes button labels.
    button_4, button_5, button_6, button_7 = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar() # Initializes button labels.
    button_8, button_9, button_10, button_11 = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar() # Initializes button labels.
    button_12, button_13, button_14, button_15 = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar() # Initializes button labels.
    favorite_button_0 = tk.Button(favorites, textvariable=button_0, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[0].split(", ")))
    favorite_button_0.bind('<Enter>', partial(font_config, favorite_button_0, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_0.bind('<Leave>', partial(font_config, favorite_button_0, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_1 = tk.Button(favorites, textvariable=button_1, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[1].split(", ")))
    favorite_button_1.bind('<Enter>', partial(font_config, favorite_button_1, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_1.bind('<Leave>', partial(font_config, favorite_button_1, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_2 = tk.Button(favorites, textvariable=button_2, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[2].split(", ")))
    favorite_button_2.bind('<Enter>', partial(font_config, favorite_button_2, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_2.bind('<Leave>', partial(font_config, favorite_button_2, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_3 = tk.Button(favorites, textvariable=button_3, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[3].split(", ")))
    favorite_button_3.bind('<Enter>', partial(font_config, favorite_button_3, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_3.bind('<Leave>', partial(font_config, favorite_button_3, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_4 = tk.Button(favorites, textvariable=button_4, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[4].split(", ")))
    favorite_button_4.bind('<Enter>', partial(font_config, favorite_button_4, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_4.bind('<Leave>', partial(font_config, favorite_button_4, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_5 = tk.Button(favorites, textvariable=button_5, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[5].split(", ")))
    favorite_button_5.bind('<Enter>', partial(font_config, favorite_button_5, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_5.bind('<Leave>', partial(font_config, favorite_button_5, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_6 = tk.Button(favorites, textvariable=button_6, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[6].split(", ")))
    favorite_button_6.bind('<Enter>', partial(font_config, favorite_button_6, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_6.bind('<Leave>', partial(font_config, favorite_button_6, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_7 = tk.Button(favorites, textvariable=button_7, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[7].split(", ")))
    favorite_button_7.bind('<Enter>', partial(font_config, favorite_button_7, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_7.bind('<Leave>', partial(font_config, favorite_button_7, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_8 = tk.Button(favorites, textvariable=button_8, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[8].split(", ")))
    favorite_button_8.bind('<Enter>', partial(font_config, favorite_button_8, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_8.bind('<Leave>', partial(font_config, favorite_button_8, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_9 = tk.Button(favorites, textvariable=button_9, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[9].split(", ")))
    favorite_button_9.bind('<Enter>', partial(font_config, favorite_button_9, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_9.bind('<Leave>', partial(font_config, favorite_button_9, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_10 = tk.Button(favorites, textvariable=button_10, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[10].split(", ")))
    favorite_button_10.bind('<Enter>', partial(font_config, favorite_button_10, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_10.bind('<Leave>', partial(font_config, favorite_button_10, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_11 = tk.Button(favorites, textvariable=button_11, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[11].split(", ")))
    favorite_button_11.bind('<Enter>', partial(font_config, favorite_button_11, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_11.bind('<Leave>', partial(font_config, favorite_button_11, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_12 = tk.Button(favorites, textvariable=button_12, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[12].split(", ")))
    favorite_button_12.bind('<Enter>', partial(font_config, favorite_button_12, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_12.bind('<Leave>', partial(font_config, favorite_button_12, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_13 = tk.Button(favorites, textvariable=button_13, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[13].split(", ")))
    favorite_button_13.bind('<Enter>', partial(font_config, favorite_button_13, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_13.bind('<Leave>', partial(font_config, favorite_button_13, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_14 = tk.Button(favorites, textvariable=button_14, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[14].split(", ")))
    favorite_button_14.bind('<Enter>', partial(font_config, favorite_button_14, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_14.bind('<Leave>', partial(font_config, favorite_button_14, f'Cambria {small_text}')) # Optional font automation.
    favorite_button_15 = tk.Button(favorites, textvariable=button_15, font=('Cambria', small_text), bg='#FAEDCB', command=lambda: favorites_trigger(favorites_list[15].split(", ")))
    favorite_button_15.bind('<Enter>', partial(font_config, favorite_button_15, f'Cambria {small_text} bold')) # Optional font automation.
    favorite_button_15.bind('<Leave>', partial(font_config, favorite_button_15, f'Cambria {small_text}')) # Optional font automation.
    if len(favorites_list) == 0:
        print("No favorites saved.") # Optional.
    if len(favorites_list) >= 1:
        csv_units = favorites_list[0].split(", ") # Specifies button_0 for labelling.
        button_0.set(csv_units[0]) # Sets unit_consolidated as the label of button_0.
        favorite_button_0.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_0) # Places the button in the favorites Text module.
    if len(favorites_list) >= 2:
        csv_units = favorites_list[1].split(", ") # Specifies button_1.
        button_1.set(csv_units[0]) # Sets unit_consolidated as the label of button_1.
        favorite_button_1.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_1) # Places the button in the favorites Text module.
    if len(favorites_list) >= 3:
        csv_units = favorites_list[2].split(", ") # Specifies button_2.
        button_2.set(csv_units[0]) # Sets unit_consolidated as the label of button_2.
        favorite_button_2.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_2) # Places the button in the favorites Text module.
    if len(favorites_list) >= 4:
        csv_units = favorites_list[3].split(", ") # Specifies button_3.
        button_3.set(csv_units[0]) # Sets unit_consolidated as the label of button_3.
        favorite_button_3.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_3) # Places the button in the favorites Text module.
    if len(favorites_list) >= 5:
        csv_units = favorites_list[4].split(", ") # Specifies button_4 for labelling.
        button_4.set(csv_units[0]) # Sets unit_consolidated as the label of button_4.
        favorite_button_4.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_4) # Places the button in the favorites Text module.
    if len(favorites_list) >= 6:
        csv_units = favorites_list[5].split(", ") # Specifies button_5.
        button_5.set(csv_units[0]) # Sets unit_consolidated as the label of button_5.
        favorite_button_5.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_5) # Places the button in the favorites Text module.
    if len(favorites_list) >= 7:
        csv_units = favorites_list[6].split(", ") # Specifies button_6.
        button_6.set(csv_units[0]) # Sets unit_consolidated as the label of button_6.
        favorite_button_6.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_6) # Places the button in the favorites Text module.
    if len(favorites_list) >= 8:
        csv_units = favorites_list[7].split(", ") # Specifies button_7.
        button_7.set(csv_units[0]) # Sets unit_consolidated as the label of button_7.
        favorite_button_7.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_7) # Places the button in the favorites Text module.
    if len(favorites_list) >= 9:
        csv_units = favorites_list[8].split(", ") # Specifies button_8 for labelling.
        button_8.set(csv_units[0]) # Sets unit_consolidated as the label of button_8.
        favorite_button_8.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_8) # Places the button in the favorites Text module.
    if len(favorites_list) >= 10:
        csv_units = favorites_list[9].split(", ") # Specifies button_9.
        button_9.set(csv_units[0]) # Sets unit_consolidated as the label of button_9.
        favorite_button_9.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_9) # Places the button in the favorites Text module.
    if len(favorites_list) >= 11:
        csv_units = favorites_list[10].split(", ") # Specifies button_10.
        button_10.set(csv_units[0]) # Sets unit_consolidated as the label of button_10.
        favorite_button_10.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_10) # Places the button in the favorites Text module.
    if len(favorites_list) >= 12:
        csv_units = favorites_list[11].split(", ") # Specifies button_11.
        button_11.set(csv_units[0]) # Sets unit_consolidated as the label of button_11.
        favorite_button_11.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_11) # Places the button in the favorites Text module.
    if len(favorites_list) >= 13:
        csv_units = favorites_list[12].split(", ") # Specifies button_12 for labelling.
        button_12.set(csv_units[0]) # Sets unit_consolidated as the label of button_12.
        favorite_button_12.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_12) # Places the button in the favorites Text module.
    if len(favorites_list) >= 14:
        csv_units = favorites_list[13].split(", ") # Specifies button_13.
        button_13.set(csv_units[0]) # Sets unit_consolidated as the label of button_13.
        favorite_button_13.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_13) # Places the button in the favorites Text module.
    if len(favorites_list) >= 15:
        csv_units = favorites_list[14].split(", ") # Specifies button_14.
        button_14.set(csv_units[0]) # Sets unit_consolidated as the label of button_14.
        favorite_button_14.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_14) # Places the button in the favorites Text module.
    if len(favorites_list) >= 16:
        csv_units = favorites_list[15].split(", ") # Specifies button_15.
        button_15.set(csv_units[0]) # Sets unit_consolidated as the label of button_15.
        favorite_button_15.place(relx=0, rely=0, relwidth=0.15, relheight=0.3) # Places a defined button in favorites_frame.
        favorites.window_create('end', window=favorite_button_15) # Places the button in the favorites Text module.
    if len(favorites_list) > 17:
        print("Favorites full! Implement more memory to continue.") # Optional.
    print() # Optional.
    if current_database_list: # False at startup.
        print("-"*98) # Optional.

def prefix_toggle(prefix=""):
    """ Toggles the selected prefix and unselects all others. """
    print("prefix_toggle():\n") # Optional.
    if prefix == "Y":
        if prefix_Y_button.config('relief')[-1] == 'sunken':
            prefix_Y_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_Y_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_Y_button.config(relief="raised")
    if prefix == "Z":
        if prefix_Z_button.config('relief')[-1] == 'sunken':
            prefix_Z_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_Z_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_Z_button.config(relief="raised")
    if prefix == "E":
        if prefix_E_button.config('relief')[-1] == 'sunken':
            prefix_E_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_E_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_E_button.config(relief="raised")
    if prefix == "P":
        if prefix_P_button.config('relief')[-1] == 'sunken':
            prefix_P_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_P_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_P_button.config(relief="raised")
    if prefix == "T":
        if prefix_T_button.config('relief')[-1] == 'sunken':
            prefix_T_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_T_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_T_button.config(relief="raised")
    if prefix == "G":
        if prefix_G_button.config('relief')[-1] == 'sunken':
            prefix_G_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_G_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_G_button.config(relief="raised")
    if prefix == "M":
        if prefix_M_button.config('relief')[-1] == 'sunken':
            prefix_M_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_M_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_M_button.config(relief="raised")
    if prefix == "k":
        if prefix_k_button.config('relief')[-1] == 'sunken':
            prefix_k_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_k_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_k_button.config(relief="raised")
    if prefix == "h":
        if prefix_h_button.config('relief')[-1] == 'sunken':
            prefix_h_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_h_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_h_button.config(relief="raised")
    if prefix == "da":
        if prefix_da_button.config('relief')[-1] == 'sunken':
            prefix_da_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_da_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_da_button.config(relief="raised")
    if prefix == "d":
        if prefix_d_button.config('relief')[-1] == 'sunken':
            prefix_d_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_d_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_d_button.config(relief="raised")
    if prefix == "c":
        if prefix_c_button.config('relief')[-1] == 'sunken':
            prefix_c_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_c_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_c_button.config(relief="raised")
    if prefix == "m":
        if prefix_m_button.config('relief')[-1] == 'sunken':
            prefix_m_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_m_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_m_button.config(relief="raised")
    if prefix == "μ":
        if prefix_u_button.config('relief')[-1] == 'sunken':
            prefix_u_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_u_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_u_button.config(relief="raised")
    if prefix == "n":
        if prefix_n_button.config('relief')[-1] == 'sunken':
            prefix_n_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_n_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_n_button.config(relief="raised")
    if prefix == "p":
        if prefix_p_button.config('relief')[-1] == 'sunken':
            prefix_p_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_p_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_p_button.config(relief="raised")
    if prefix == "f":
        if prefix_f_button.config('relief')[-1] == 'sunken':
            prefix_f_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_f_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_f_button.config(relief="raised")
    if prefix == "a":
        if prefix_a_button.config('relief')[-1] == 'sunken':
            prefix_a_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_a_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_a_button.config(relief="raised")
    if prefix == "z":
        if prefix_z_button.config('relief')[-1] == 'sunken':
            prefix_z_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_z_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_z_button.config(relief="raised")
    if prefix == "y":
        if prefix_y_button.config('relief')[-1] == 'sunken':
            prefix_y_button.config(relief="raised")
            prefix_button.config(relief="raised")
        else:
            prefix_y_button.config(relief='sunken')
            prefix_button.config(relief='sunken')
    else:
        prefix_y_button.config(relief="raised")
    if prefix == "":
        prefix_button.config(relief="raised")

def prefix_value_tuple(button_index):
    """ Checks the state of each prefix button and returns the symbol and associated value that corresponds to the button in the "on" position. """
    #print("prefix_value_tuple():\n") # Optional.
    if button_index == 2 and current_database_file == "database_iso.txt":
        kilogram_toggle = 1000
    else:
        kilogram_toggle = 1
    if prefix_Y_button.config('relief')[-1] == 'sunken':
        return (1000000000000000000000000*kilogram_toggle) # "Y"
    elif prefix_Z_button.config('relief')[-1] == 'sunken':
        return (1000000000000000000000*kilogram_toggle) # "Z"
    elif prefix_E_button.config('relief')[-1] == 'sunken':
        return (1000000000000000000*kilogram_toggle) # "E"
    elif prefix_P_button.config('relief')[-1] == 'sunken':
        return (1000000000000000*kilogram_toggle) # "P"
    elif prefix_T_button.config('relief')[-1] == 'sunken':
        return (1000000000000*kilogram_toggle) # "T"
    elif prefix_G_button.config('relief')[-1] == 'sunken':
        return (1000000000*kilogram_toggle) # "G"
    elif prefix_M_button.config('relief')[-1] == 'sunken':
        return (1000000*kilogram_toggle) # "M"
    elif prefix_k_button.config('relief')[-1] == 'sunken':
        return (1000*kilogram_toggle) # "k"
    elif prefix_h_button.config('relief')[-1] == 'sunken':
        return (100*kilogram_toggle) # "h"
    elif prefix_da_button.config('relief')[-1] == 'sunken':
        return (10*kilogram_toggle) # "da"
    elif prefix_d_button.config('relief')[-1] == 'sunken':
        return (0.1*kilogram_toggle) # "d"
    elif prefix_c_button.config('relief')[-1] == 'sunken':
        return (0.01*kilogram_toggle) # "c"
    elif prefix_m_button.config('relief')[-1] == 'sunken':
        return (0.001*kilogram_toggle) # "m"
    elif prefix_u_button.config('relief')[-1] == 'sunken':
        return (0.000001*kilogram_toggle) # "μ"
    elif prefix_n_button.config('relief')[-1] == 'sunken':
        return (0.000000001*kilogram_toggle) # "n 
    elif prefix_p_button.config('relief')[-1] == 'sunken':
        return (0.000000000001*kilogram_toggle) # "p"
    elif prefix_f_button.config('relief')[-1] == 'sunken':
        return (0.000000000000001*kilogram_toggle) # "f"
    elif prefix_a_button.config('relief')[-1] == 'sunken':
        return (0.000000000000000001*kilogram_toggle) # "a"
    elif prefix_z_button.config('relief')[-1] == 'sunken':
        return (0.000000000000000000001*kilogram_toggle) # "z"
    elif prefix_y_button.config('relief')[-1] == 'sunken':
        return (0.000000000000000000000001*kilogram_toggle) # "y"
    else:
        return (kilogram_toggle)

def entry_data_finder(unit_symbol):
    """ Searches for data corresponding to the current non-base unit and sends that data to consolidate_current_unit_list. Ex=["cd", "-m", "-m"] """
    global conversion_database
    if unit_symbol in conversion_database: # Returns a list of equivalent base units.
        return conversion_database[unit_symbol][0]
    else: # Returns zero if no data is found.
        print(f"No data found for {unit_symbol}.\n") # Optional.
        return 0

def unit_data_finder(unit_name, x=0):
    """ Searches for data corresponding to the current unit and sends that data to the quantities and conversions frames. """
    global unit_database
    if textbox_index == 1:
        textbox = textbox_1
    elif textbox_index == 2:
        textbox = textbox_2
    elif textbox_index == 3:
        textbox = textbox_3
    if unit_name in unit_database: # Updates conversions and quantities display.
        conversions.delete(0, 'end')
        conversions.insert(0, unit_database[unit_name][0])
        quantities.delete(0, 'end')
        quantities.insert(0, unit_database[unit_name][1])
        if x != 0 and textbox.get('-1.0', 'end') != "\n":
            textbox.insert('end', "\n")
        if x == 1: # True when triggered by conversions_button.
            textbox.insert('end', unit_database[unit_name][0])
        elif x == 2: # True when triggered by quantities_button.
            textbox.insert('end', unit_database[unit_name][1])
    else: # True if no unit data is found.
        conversions.delete(0, 'end')
        quantities.delete(0, 'end')

def window_size(resize=False):
    """ Automates widget configurations with respect to window size. """
    #print(f"window_size():") # Optional.
    #print(f"resize.width: {resize.width}\n") # Optional.
    global current_window_size
    if resize:
        current_window_size = (resize.width, resize.height)
    if current_window_size[0] >= 800: # Triggers maximum frame width.
        new_width = 800 / current_window_size[0] # Defines full size. A larger value results in a wider size.
        upper_subframe_A.place(relx=0.5, rely=0.1, relwidth=new_width, relheight=0.2, anchor='n')
        upper_subframe_B.place(relx=0.5, rely=0.1, relwidth=new_width, relheight=0.2, anchor='n')
        middle_subframe_A.place(relx=0.5, rely=0.35, relwidth=new_width, relheight=0.3, anchor='n')
        middle_subframe_B.place(relx=0.5, rely=0.35, relwidth=new_width, relheight=0.3, anchor='n')
        lower_subframe.place(relx=0.5, rely=0.7, relwidth=new_width, relheight=0.15, anchor='n')
        cell_scrollbar_B.pack(side='bottom', fill='x', padx=1000)
        search_label.config(text="Search:")
    else: # Frame width defined by window dimensions.
        upper_subframe_A.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.2, anchor='n')
        upper_subframe_B.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.2, anchor='n')
        middle_subframe_A.place(relx=0.5, rely=0.35, relwidth=1, relheight=0.3, anchor='n')
        middle_subframe_B.place(relx=0.5, rely=0.35, relwidth=1, relheight=0.3, anchor='n')
        lower_subframe.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.15, anchor='n')
        cell_scrollbar_B.pack(side='bottom', fill='x', padx=0)
        search_label.config(text="")
    if current_window_size[0] <= 675: # Triggers alternate button text.
        conversions_button.config(text='Conversions')
        quantities_button.config(text='Quantities')
        clear_button.config(text='✗')
        invert_button.config(text='f⁻¹') # Alternate symbol: 🗘.
        convert_button.config(text='k→10³')
        if preset_text.get() == "SI/ISO":
            base_button.config(text="u→kg")
        else:
            base_button.config(text='Å→m')
        favorites_button.config(text='★')
        values_button.config(text='#')
        prefix_button.config(font=('Cambria italic', mini_text))
        preset_label.config(text="")
        category_label.config(text="")
        sort_label.config(text="")
    else: # Triggers default button text.
        conversions_button.config(text='Common Conversions')
        quantities_button.config(text='Related Quantities')
        clear_button.config(text='Clear')
        invert_button.config(text='Invert')
        convert_button.config(text='Convert to Values')
        favorites_button.config(text='Favorites')
        values_button.config(text='Values')
        prefix_button.config(font=('Cambria italic', mini_text))
        preset_label.config(text="Preset:")
        category_label.config(text="Category:")
        sort_label.config(text="Sort:")
        if preset_text.get() == "SI/ISO":
            base_button.config(text="Convert to SI")
        else:
            base_button.config(text='Convert to Base')

def prefix_to_value(convert_to_base=False):
    """ Converts all prefixes to their numerical equivalent and multiplies the current value by each, then removes the prefixes from the numerator and denominator lists. 
        Called by convert_to_base() or convert_button. units_exponents_totals=[['s²', 's', 2, 2], ['eV', 'eV', 1, 1000000]] """
    print("prefix_to_value():") # Optional.
    global current_value
    for i in range(len(units_exponents_totals)):
        if units_exponents_totals[i][1] == "g" and current_database_file == "database_iso.txt":
            value = 1000 ** units_exponents_totals[i][2]
            current_value *= (units_exponents_totals[i][-1] / value)
        elif units_exponents_totals[i][1] == "-g" and current_database_file == "database_iso.txt":
            value = 1000 ** -(units_exponents_totals[i][2])
            current_value /= (units_exponents_totals[i][-1] / value)
        else:
            if "⁻" not in units_exponents_totals[i][0]: # Handles numerators.
                current_value *= units_exponents_totals[i][-1]
            else: # Handles denominators.
                current_value /= units_exponents_totals[i][-1]
    for i in range(len(numerator_value_list)):
        if i == 2 and current_database_file == "database_iso.txt" and numerator_value_list[i]:
            numerator_value_list[i] = value
        elif i == 2 and current_database_file == "database_iso.txt" and denominator_value_list[i]:
            denominator_value_list[i] = value
        else:
            if numerator_value_list[i]:
                numerator_value_list[i] = 1
            if denominator_value_list[i]:
                denominator_value_list[i] = 1
    if not convert_to_base:
        print() # Optional.
        main_units()
    
def convert_to_base():
    """ Converts any non-base units to base units. Calls prefix_to_value before converting non-base units. current_unit_list=['m', 'm', '-s', '-s'] """
    print("convert_to_base():\n") #  Optional.
    global current_value, current_unit_list, numerator_value_list, denominator_value_list
    prefix_to_value(True) # Merges all prefixes with the current value.
    temp_unit_list = current_unit_list[:] # Creates a copy of the current base and non-base units.
    convert = False
    for i in range(len(current_unit_list)):
        if current_unit_list[i] in conversion_database: # Converts non-base units in the current unit list to base units.
            if current_unit_list[i] == "A" and current_database_file == "database_iso.txt":
                continue
            else:
                convert = True
                temp_unit_list.remove(current_unit_list[i]) # Removes the non-base unit from the global list.
                temp_unit_list.extend(conversion_database[current_unit_list[i]][0]) # Adds the equivalent base units to the global list.
                for j in range(len(positive_numerator_symbols)): # Simplifies the global list.
                    while positive_numerator_symbols[j] in temp_unit_list and negative_numerator_symbols[j] in temp_unit_list:
                        temp_unit_list.remove(positive_numerator_symbols[j])
                        temp_unit_list.remove(negative_numerator_symbols[j])
                current_value *= conversion_database[current_unit_list[i]][1]
    current_unit_list = temp_unit_list 
    if current_database_file == "database_iso.txt" and convert: # convert_to_si()
        print() # Optional.
        main_units()
        print(f"convert_to_base():") # Optional.
        numerator_value_list[2] += (1000 ** current_unit_list.count("g"))
        denominator_value_list[2] += (1000 ** current_unit_list.count("-g"))
        current_value /= (1000 ** current_unit_list.count("g"))
        current_value *= (1000 ** current_unit_list.count("-g"))
        temp_unit_list = current_unit_list[:]
        for i in range(len(temp_unit_list)):
            if temp_unit_list[i] == "X": # Change to "C" for ISO variant.
                temp_unit_list.remove("C")
                if "-s" in temp_unit_list:
                    temp_unit_list.remove("-s")
                else:
                    temp_unit_list.append("s")
                temp_unit_list.append("A")
            elif temp_unit_list[i] == "-X": # Change to "C" for ISO variant.
                temp_unit_list.remove("-C")
                if "-s" in temp_unit_list:
                    temp_unit_list.remove("s")
                else:
                    temp_unit_list.append("-s")
                temp_unit_list.append("-A")
        current_unit_list = temp_unit_list 
        #print(f"current_unit_list: {current_unit_list}") # Optional.
    print() # Optional.
    main_units()

def font_config(widget, fontslant, event):
    """ Alters font properties when the cursor hovers over the respective widget. """
    if str(widget) == '.!frame.!button3' and str(event)[1] == 'E' and current_window_size[0] > 650:
        fontslant += ' italic' # Prevents '✗' from becoming italic.
    widget.configure(font=fontslant)
    
def raise_frame():
    """ Manages the alternation between applications. """
    global application_index
    if application_index == 0:
        upper_subframe_A.tkraise()
        middle_subframe_A.tkraise()
        application = "Unit Manager"
        application_index += 1
    else:
        upper_subframe_B.tkraise()
        middle_subframe_B.tkraise()
        application = "Symbol Manager"
        application_index -= 1
    if current_database_file == "database_clx.txt":
        database = "CLX"
    else:
        database = "SI/ISO"
    root.title(f"Coalexicon | {application} | {database}")
    sleep(0.01) # Optional.

def main_symbols():
    """ Called to update the Symbol Manager entry cells. """
    print(f"main_symbols():\n") # Optional.
    set_current_database_list()
    populate_cells()
    print() # Optional.
    print("-"*98) # Optional.

def load_symbols(database='database_clx.txt'):
    """ Converts an existing text file to a global dictionary of saved values. ={"} """
    print("load_symbols():") # Optional.
    global notation_database_dictionary, notation_database_list, notation_database_quantities, notation_database_constants, notation_database_modifiers, notation_database_other
    notation_database_dictionary.clear() # Prepares the global list for updating.
    notation_database_list.clear() # Prepares the global list for updating.
    notation_database_quantities.clear() # Prepares the global list for updating.
    notation_database_constants.clear() # Prepares the global list for updating.
    notation_database_modifiers.clear() # Prepares the global list for updating.
    notation_database_other.clear() # Prepares the global list for updating.
    with open(database, encoding='utf-8') as file:
        column_list = list(zip(*(line.strip().split('\t') for line in file)))
    column_names_list = list(column_list[0]) # Produces a list of names from the specified text file.
    column_data_list = [] # Initializes a list of lists from the specified text file.
    for i in range(len(column_list)-1): # Produces a list of lists from the specified text file.
        column_data_list.append(list(column_list[i+1]))
    for i in range(len(column_names_list)):
        column_data = [] # Ex=['d', '0', 'l;s;r', 'm']
        for j in range(len(column_data_list)):
            column_data.append(column_data_list[j][i])
        notation_database_dictionary[column_names_list[i]] = column_data
    notation_database_list = list(notation_database_dictionary.items()) # Produces a list variant of notation_database_dictionary.
    for i in range(len(notation_database_list)): # Populates notation_database_quantities, notation_database_modifiers, and notation_database_other.
        if notation_database_list[i][-1][-1] == "quantity": # Produces a list of quantities from notation_database_dictionary.
            notation_database_quantities.append(notation_database_list[i])
        elif notation_database_list[i][-1][-1] == "constant": # Produces a list of constants from notation_database_dictionary.
            notation_database_constants.append(notation_database_list[i])
        elif notation_database_list[i][-1][-1] == "modifier": # Produces a list of modifiers from notation_database_dictionary.
            notation_database_modifiers.append(notation_database_list[i])
        elif notation_database_list[i][-1][-1] == "general": # Produces a list of uncategorized entries from notation_database_dictionary.
            notation_database_other.append(notation_database_list[i])
    #print(f"notation_database_dictionary: {notation_database_dictionary}") # Optional.
    print() # Optional.

def save_symbols():
    """ Saves data within the Symbol Manager application. """
    global current_database_file
    print("save_symbols():") # Optional.
    #print(f"current_database_file: {current_database_file}") # Optional.
    with open(current_database_file, 'w', encoding='utf-8') as database:
        for name in notation_database_dictionary: # Assumes notation_database_dictionary.
            name_and_symbols = f"{name}"
            for symbol in notation_database_dictionary[name]: # Assumes notation_database_dictionary.
                name_and_symbols = f"{name_and_symbols}\t{symbol}"
            print(name_and_symbols, file=database)
    sleep(0.5) # Optional.
    print() # Optional.
    load_symbols(current_database_file)

def change_preset_text(*args):
    """ Loads the specified database and updates related labels and functions. """
    print(f"change_preset_text():\n") # Optional.
    global current_database_file
    if preset_text.get() == "CLX":
        current_database_file = "database_clx.txt"
        root.title("Coalexicon | Symbol Manager | CLX")
        load_symbols("database_clx.txt") # Loads the specified database.
        base_button.config(text="Convert to Base")
        gram_frame.config(text="g")
        coulomb_frame.config(text="C")
    elif preset_text.get() == "SI/ISO":
        current_database_file = "database_iso.txt"
        root.title("Coalexicon | Symbol Manager | SI/ISO")
        load_symbols("database_iso.txt") # Loads the specified database.
        base_button.config(text="Convert to SI")
        gram_frame.config(text="kg")
        coulomb_frame.config(text="A")
        window_size()
    elif preset_text.get() == "Custom":
        current_database_file = "database_custom.txt"
        load_symbols("database_custom.txt") # Loads the specified database.
    if current_category == "Search":
        search_names('', search_text)
    else:
        main_symbols()

def set_current_database_list():
    """ Updates Unit Manager to show entries of the specified category. Ex=[('<Name>', ['<Primary>', '<Secondary>', '<Other>', '<Units>', '<Index>', '<Category>'])]
        Allows changing the Symbol sorting method from Primary to Index. """
    print("set_current_database_list():") # Optional.
    global current_database_list
    if current_category == "All" or current_category == "All *":
        current_database_list = notation_database_list
    elif current_category == "Quantities":
        current_database_list = notation_database_quantities
    elif current_category == "Constants":
        current_database_list = notation_database_constants
    elif current_category == "Modifiers":
        current_database_list = notation_database_modifiers
    elif current_category == "Other":
        current_database_list = notation_database_other
    elif current_category == "Search":
        current_database_list = notation_database_search
    if current_sort == "Name" or current_sort == "Name *":
        current_database_list.sort()
    elif current_sort == "Symbol":
        if index_type == "Primary":
            current_database_list.sort(key=lambda x: x[1][0])
        elif index_type == "Secondary":
            current_database_list.sort(key=lambda x: x[1][1])
        else:
            current_database_list.sort(key=lambda x: x[1][0]) # Use x[1][-2] for Index or x[1][0] for Primary.
            symbol_database_list, null_database_list = [], [] # Initializes temporary lists.
            for row in range(len(current_database_list)): # Places entries with non-base units after those with base units.
                if current_database_list[row][1][0] == "0": # Use x[1][-2] for Index or x[1][0] for Primary.
                    null_database_list.append(current_database_list[row])
                else:
                    symbol_database_list.append(current_database_list[row])
            current_database_list = symbol_database_list + null_database_list
    elif current_sort == "Units":
        current_database_list.sort(key=lambda x: x[1][-3]) # Remove the following lines for legacy sorting.
        unit_database_list, nonunit_database_list = [], [] # Initializes temporary lists.
        for row in range(len(current_database_list)): # Places entries with non-base units after those with base units.
            if current_database_list[row][1][-3][0] == "1" or current_database_list[row][1][-3][0] == "<":
                nonunit_database_list.append(current_database_list[row])
            else:
                unit_database_list.append(current_database_list[row])
        current_database_list = unit_database_list + nonunit_database_list
    print() # Optional.

def change_category_text(*args):
    """ Handles minor tasks related to set_current_database_list() and change_preset_text(). Possible options are ["All", "Quantities", "Modifiers", "Other"]. """
    print("change_category_text():") # Optional.
    #print(f"category: {category_text.get()}") # Optional.
    global current_category
    current_category = category_text.get()
    print() # Optional.
    main_symbols()
    
def change_sort_text(*args):
    """ Handles minor tasks related to set_current_database_list() and change_preset_text(). Possible options are ["Name", "Symbol", "Units"]. """
    print("change_sort_text():") # Optional.
    #print(f"sorting: {sort_text.get()}") # Optional.
    global current_sort
    current_sort = sort_text.get()
    print() # Optional.
    main_symbols()

def populate_cells():
    """ Removes previous cells from Symbol Manager, creates row and column labels, and creates entry cells for Symbol Manager. """
    print(f"populate_cells():") # Optional.
    #print(f"cell_frame.winfo_children(): {cell_frame.winfo_children()}\n") # Optional.
    global current_database_list
    cell_frame.grid_forget() # Prepares the cells for updating.
    for widget in cell_frame.winfo_children(): # Prepares the cells for updating.
        widget.destroy() # Removes all previous cells.
    cell_dictionary.clear() # Prepares the cells for updating.
    cell_labels = ["", "Name", "Primary", "Secondary", "Other", "Units"] # Assists in creating column labels.
    for column in range(6): # Creates column labels.
        if column == 0:  # Sets blank space in the top left corner.
            label = tk.Label(cell_frame, width=2, text=cell_labels[column], font=f'Cambria {micro_text} bold italic', bg=cell_frame_color)
        else:
            label = tk.Label(cell_frame, width=10, text=cell_labels[column], font=f'Cambria {mini_text} bold italic', bg=cell_frame_color)
        label.grid(row=0, column=column, padx=0, pady=0)
    for row in range(len(current_database_list)): # Generates a row of cells for each entry in the current database.
        for column in range(6):
            if column == 0: # Creates row labels.
                label = tk.Label(cell_frame, width=0, text=str(row+1), font=f'Cambria {micro_text}', bg=cell_frame_color)
                label.grid(row=row+1, column=column, padx=0, pady=0)
            else: # Creates cells.
                entry_text = tk.StringVar() # Optional.
                if column == 1: # Creates a wide entry cell in the Name column.
                    entry = tk.Entry(cell_frame, textvariable=entry_text, width=30, justify='left') # width=25
                    entry.insert(0, current_database_list[row][0]) # Places a name in the cell.
                elif column == 5: # Creates a wide entry cell in the Units column.
                    entry = tk.Entry(cell_frame, textvariable=entry_text, width=19, justify='center') # width=24
                    entry.insert(0, current_database_list[row][1][column-2]) # Places a name in the cell.
                else: # Creates a slim entry cell in the Primary, Secondary, Other, and Units columns.
                    entry = tk.Entry(cell_frame, textvariable=entry_text, width=10, justify='center', background='#0d151c') # width=10
                    if current_database_list[row][1][column-2] != 0 and current_database_list[row][1][column-2] != "0": # Ignores absent data.
                        entry.insert(0, current_database_list[row][1][column-2]) # Places data in a cell.
                entry.configure({"background": "white"})
                entry.grid(row=row+1, column=column)  # Places the entry cell.
                cell = f"{cell_labels[column]}{row+1}"
                cell_dictionary[cell] = [entry] # Adds a key-value pair to the global cell_dictionaryionary. Ex[B1] = .!entry2
                entry.bind('<Return>', lambda event, cell=cell: cell_return(event, cell))
    try: # Accounts for an error with the search function.
        final_row = row+2
    except:
        final_row = 1
    finally: # Creates an empty row for new data entry.
        for column in range(6):
            if column == 0: # Creates row labels.
                label = tk.Label(cell_frame, width=0, text=str(final_row), font=f'Cambria {micro_text}', bg=cell_frame_color)
                label.grid(row=final_row, column=0, padx=0, pady=0)
            else: # Creates cells.
                entry_text = tk.StringVar() # Optional. entry_text.get()
                if column == 1: # Creates a wide entry cell in the Name column.
                    entry = tk.Entry(cell_frame, textvariable=entry_text, width=30, justify='left') # width=25
                elif column == 5: # Creates a wide entry cell in the Units column.
                    entry = tk.Entry(cell_frame, textvariable=entry_text, width=19, justify='center') # width=24
                else: # Creates a slim entry cell in the Primary, Secondary, Other, and Units columns.
                    entry = tk.Entry(cell_frame, textvariable=entry_text, width=10, justify='center', background='#0d151c') # width=10
                entry.configure({"background": "white"})
                entry.grid(row=final_row, column=column)  # Places the entry cell.
                cell = f"{cell_labels[column]}{final_row}"
                cell_dictionary[cell] = [entry] # Adds a key-value pair to the global cell_dictionaryionary. Ex[B1] = .!entry2
                entry.bind('<Return>', lambda event, cell=cell: cell_return(event, cell))
    #print() # Optional.

def cell_return(event, cell):
    """ Called when return/enter has been pressed. """
    print(f"cell_return():") # Optional.
    global current_database_list
    data = cell_dictionary[cell][0].get()  # Gets text/data from the specified cell.
    row, column = "", ""
    for character in cell: # Converts the cell identifier into a numerical row and lexical column.
        if character.isdigit():
            row = f"{row}{character}"
        else:
            column = f"{column}{character}"
    if column == "Name": # Sets the column index.
        column = 0
    elif column == "Primary":
        column = 1
    elif column == "Secondary":
        column = 2
    elif column == "Other":
        column = 3
    else: # True for "Units".
        column = 4
    append_list, counter = [], 1 # Initializes temporary data.
    try: # True for a row of pre-existing data.
        name = current_database_list[int(row)-1][0] # Finds the name that corresponds to the current row.
        if column == 0:
            notation_database_dictionary[data] = notation_database_dictionary.pop(name)
        else:
            if data.strip() == "": # Sets empty cells to zero.
                data = "0"
            for item in notation_database_dictionary[name]: # Finds and updates the specified column.
                if counter == column:
                    append_list.append(data)
                else:
                    append_list.append(item)
                counter += 1
            notation_database_dictionary[name] = append_list
    except: # True for a new row.
        if current_category == "Quantities":
            category = "quantity"
        elif current_category == "Constants":
            category = "constant"
        elif current_category == "Modifiers":
            category = "modifier"
        else:
            category = "general"
        if column == 0 and data.strip() != "":
            new_data = (data, ["0", "0", "0", "0", "0", category])
            current_database_list.append(new_data)
            notation_database_dictionary[data] = ["0", "0", "0", "0", "0", category]
    finally:
        try: # Optional.
            print(f"Selected entry: ['{name}': {append_list}]") # Optional.
        except: # Optional.
            print(f"Selected entry: ['{data}': {append_list}]") # Optional.
        #print(f"Cell ID: {cell}; Cell data: {data}") # Optional.
        print() # Optional.

def configure_cell_canvas(cell_canvas):
    """ Resets the scroll region to encompass the inner frame. """
    cell_canvas.configure(scrollregion=cell_canvas.bbox('all'))

def search_names(event, widget):
    """ Looks through the current database to find names that include the search term(s). """
    print(f"search_names():") # Optional.
    global current_database_list, current_category
    current_category = "Search"
    search_term = widget.get()
    search_list = []
    for key in notation_database_dictionary: # Searches names in the database for the specified entry.
        if search_term in key:
            row = [key]
            row.append(notation_database_dictionary[key])
            search_list.append(row)
    if not search_list: # Accounts for capitalized names.
        for key in notation_database_dictionary:
            if search_term.lower() in key.lower():
                row = [key]
                row.append(notation_database_dictionary[key])
                search_list.append(row)
    notation_database_search.clear()
    notation_database_search.extend(search_list)
    print() # Optional.
    main_symbols()

def font_config(widget, fontslant, event):
    """ Alters font properties when the cursor hovers over the respective widget. """
    if str(widget) == ".!frame.!button3" and str(event)[1] == 'E' and current_window_size[0] > 675: # Corrects for a font preference.
        fontslant = f"{fontslant} italic"
    widget.configure(font=fontslant)

def fraction_set(clear=False):
    """ Manages the state of fraction_button. """
    if clear:
        fraction_button.config(text="uˣ")
        fraction_button.config(relief='raised')
    else:
        if fraction_button.config('relief')[-1] == 'raised':
            fraction_button.config(text="u¹ᐟ ˣ")
            fraction_button.config(relief='sunken')
        else:
            fraction_button.config(text="uˣ")
            fraction_button.config(relief='raised')

def set_scroll(event, unset=False):
    """ Allows mousewheel scrolling within the cell frame in Symbol Manager. """
    if unset:
        cell_canvas.unbind_all("<MouseWheel>")
    else:
        cell_canvas.bind_all("<MouseWheel>", scroll_frame)

def scroll_frame(event):
    """ Allows mousewheel scrolling within the cell frame in Symbol Manager. """
    cell_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def notes_toggle(direction=""):
    """ Switches to one of three Notepad pages in the lower subframe. """
    global textbox_index
    if textbox_index == 1:
        textbox = textbox_1
    elif textbox_index == 2:
        textbox = textbox_2
    elif textbox_index == 3:
        textbox = textbox_3
    if direction == "←":
        if textbox_index > 1:
            textbox_index -= 1
        else:
            textbox_index = 3
    elif direction == "→":
        if textbox_index < 3:
            textbox_index += 1
        else:
            textbox_index = 1
    elif direction == "✗":
        if textbox_index == 1:
            textbox_1.delete('1.0', 'end')
        elif textbox_index == 2:
            textbox_2.delete('1.0', 'end')
        elif textbox_index == 3:
            textbox_3.delete('1.0', 'end')
    if textbox_index == 1:
        textbox_1.tkraise()
        textbox_1.focus()
    elif textbox_index == 2:
        textbox_2.tkraise()
        textbox_2.focus()
    elif textbox_index == 3:
        textbox_3.tkraise()
        textbox_3.focus()

#############################################################################################################################################################################################
## Main Frame (GUI Basis)
root = tk.Tk() # Initializes the GUI.
root.minsize(500, 500)
main_canvas = tk.Canvas(root, width=900, height=600)
main_canvas.bind('<Configure>', window_size)
main_canvas.pack(expand='yes', fill='both')

main_frame_background = tk.PhotoImage(file='./background_main.gif') # Sets background image and application icon.
main_frame_background_label = tk.Label(root, image=main_frame_background)
main_frame_background_label.place(relwidth=1, relheight=1)
main_frame_icon = tk.PhotoImage(file='./background_icon.png')
root.iconphoto(True, main_frame_icon)

white, dark_gray, medium_gray, light_gray = '#FFFFFF', '#1A1A1A', '#332B33', '#F0F0F0' # Defines colors.
blue, green, yellow, red, purple = '#C6DEF1', '#C9E4DE', '#FAEDCB', '#F2C6C6', '#665566' # Defines colors.
micro_text = 10
mini_text, small_text, medium_text, large_text = micro_text+1, micro_text+2, micro_text+3, micro_text+4
cell_frame_color = green

scrollbar_style_horizontal_dark, scrollbar_style_horizontal_light = ttk.Style(), ttk.Style() # Initializes custom scrollbars.
scrollbar_style_vertical_dark, scrollbar_style_vertical_light = ttk.Style(), ttk.Style() # Initializes custom scrollbars.
scrollbar_style_horizontal_dark.theme_use('clam') # Initializes dark horizontal scrollbars.
scrollbar_style_horizontal_light.theme_use('clam') # Initializes light horizontal scrollbars.
scrollbar_style_vertical_dark.theme_use('clam') # Initializes dark vertical scrollbars.
scrollbar_style_vertical_light.theme_use('clam') # Initializes light vertical scrollbars.
scrollbar_style_horizontal_dark.configure("Dark.Horizontal.TScrollbar", gripcount=0, background=medium_gray, darkcolor=medium_gray, lightcolor=purple, troughcolor=dark_gray, 
    bordercolor=dark_gray, arrowcolor=dark_gray, arrowsize=10)
scrollbar_style_horizontal_light.configure("Light.Horizontal.TScrollbar", gripcount=0, background=light_gray, darkcolor=dark_gray, lightcolor=white, troughcolor=white,
    bordercolor=white, active=blue, arrowcolor=medium_gray, arrowsize=10)
scrollbar_style_vertical_dark.configure("Dark.Vertical.TScrollbar", gripcount=0, background=cell_frame_color, darkcolor=dark_gray, lightcolor=cell_frame_color,
    troughcolor=cell_frame_color, bordercolor=cell_frame_color, active=blue, arrowcolor=medium_gray, arrowsize=13)
scrollbar_style_vertical_light.configure("Light.Vertical.TScrollbar", gripcount=0, background=light_gray, darkcolor=dark_gray, lightcolor=white, troughcolor=white,
    bordercolor=white, active=blue, arrowcolor=medium_gray, arrowsize=13)
scrollbar_style_horizontal_dark.map("Dark.Horizontal.TScrollbar", background=[('!active',medium_gray), ('active', light_gray), ('pressed', light_gray)]) # Default; hover; press.
scrollbar_style_horizontal_light.map("Light.Horizontal.TScrollbar", background=[('!active',light_gray), ('active', purple), ('pressed', purple)]) # Default; hover; press.
scrollbar_style_vertical_dark.map("Dark.Vertical.TScrollbar", background=[('!active',light_gray), ('active', purple), ('pressed', purple)]) # Default; hover; press.
scrollbar_style_vertical_light.map("Light.Vertical.TScrollbar", background=[('!active',light_gray), ('active', purple), ('pressed', purple)]) # Default; hover; press.

default_font = tk.font.nametofont('TkDefaultFont') # Sets default font.
default_font.config(family='Cambria', size=small_text)
root.option_add('*Font', default_font)

#############################################################################################################################################################################################
## Upper Subframe A (Unit Manager: Data and Operations)
upper_subframe_A = tk.Frame(root, bd=10) # Configures upper frame.
upper_subframe_A.place(relx=0.5, rely=0.1, relwidth=0.68, relheight=0.2, anchor='n')

upper_subframe_background_A = tk.PhotoImage(file='./background_frames.gif') # Configures foreground image.
upper_subframe_background_label_A = tk.Label(upper_subframe_A, image=upper_subframe_background_A)
upper_subframe_background_label_A.place(relx=-0.4, rely=-1, relwidth=2, relheight=3)

display = tk.StringVar() # Configures main unit display.
display_unit_frame = tk.Label(upper_subframe_A, font=('Cambria', large_text), bg=light_gray, textvariable=display)
display_unit_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1)
display_unit_frame.bind('<Button-1>', display_trigger)

conversions_button = tk.Button(upper_subframe_A, text='Common Conversions', font=('Cambria', small_text), bg=blue, command=conversions_trigger) # Configures conversions display.
conversions_button.place(relx=0.26, rely=0, relwidth=0.23, relheight=0.3)
conversions_frame = tk.Frame(upper_subframe_A, borderwidth=1, bg='white', relief='sunken')
conversions_text = tk.StringVar() # Optional. conversions_text.get()
conversions = tk.Entry(conversions_frame, textvariable=conversions_text, width=24, borderwidth=0, font=('Courier New', micro_text))
conversions_scrollbar = ttk.Scrollbar(conversions_frame, orient="horizontal", style="Light.Horizontal.TScrollbar", command=conversions.xview)
conversions.configure(xscrollcommand=conversions_scrollbar.set)
conversions.grid(row=0, column=0, padx=5, sticky="nsew")
conversions_scrollbar.grid(row=1, column=0, sticky="ew")
conversions_frame.grid_rowconfigure(0, weight=1)
conversions_frame.grid_columnconfigure(0, weight=1)
conversions_frame.place(relx=0.495, rely=0, relwidth=0.505, relheight=0.29)
conversions_button.bind('<Enter>', partial(font_config, conversions_button, f'Cambria {small_text} bold italic')) # Optional font automation.
conversions_button.bind('<Leave>', partial(font_config, conversions_button, f'Cambria {small_text}')) # Optional font automation.
conversions.bind('<Return>', lambda event, cell=conversions: data_return(event, cell))

quantities_button = tk.Button(upper_subframe_A, text='Related Quantities', font=('Cambria', small_text), bg=blue, command=quantities_trigger) # Configures quantities display.
quantities_button.place(relx=0.26, rely=0.35, relwidth=0.19, relheight=0.3)    
quantities_frame = tk.Frame(upper_subframe_A, borderwidth=1, bg='white', relief='sunken')
quantities_text = tk.StringVar() # Optional. conversions_text.get()
quantities = tk.Entry(quantities_frame, textvariable=quantities_text, width=24, borderwidth=0, font=('Courier New', micro_text))
quantities_scrollbar = ttk.Scrollbar(quantities_frame, orient="horizontal", style="Light.Horizontal.TScrollbar", command=quantities.xview)
quantities.configure(xscrollcommand=quantities_scrollbar.set)
quantities.grid(row=0, column=0, padx=5, sticky="nsew")
quantities_scrollbar.grid(row=1, column=0, sticky="ew")
quantities_frame.grid_rowconfigure(0, weight=1)
quantities_frame.grid_columnconfigure(0, weight=1)
quantities_frame.place(relx=0.455, rely=0.35, relwidth=0.545, relheight=0.29)
quantities_button.bind('<Enter>', partial(font_config, quantities_button, f'Cambria {small_text} bold italic')) # Optional font automation.
quantities_button.bind('<Leave>', partial(font_config, quantities_button, f'Cambria {small_text}')) # Optional font automation.
quantities.bind('<Return>', lambda event, cell=quantities: data_return(event, cell))

clear_button = tk.Button(upper_subframe_A, text='Clear', font=('Cambria', small_text), bg=red, command=clear) # Configures clear button.
clear_button.place(relx=0.26, rely=0.7, relwidth=0.075, relheight=0.3)
clear_button.bind('<Enter>', partial(font_config, clear_button, f'Cambria {small_text} bold')) # Optional font automation.
clear_button.bind('<Leave>', partial(font_config, clear_button, f'Cambria {small_text}')) # Optional font automation.

invert_button = tk.Button(upper_subframe_A, text='Invert', font=('Cambria', small_text), bg=green, command=invert) # Configures invert button.
invert_button.place(relx=0.34, rely=0.7, relwidth=0.085, relheight=0.3)
invert_button.bind('<Enter>', partial(font_config, invert_button, f'Cambria {small_text} bold italic')) # Optional font automation.
invert_button.bind('<Leave>', partial(font_config, invert_button, f'Cambria {small_text}')) # Optional font automation.

convert_button = tk.Button(upper_subframe_A, text='Convert to Values', font=('Cambria', small_text), bg=green, relief="raised", command=prefix_to_value) # Configures value conversion button.
convert_button.place(relx=0.43, rely=0.7, relwidth=0.185, relheight=0.3)
convert_button.bind('<Enter>', partial(font_config, convert_button, f'Cambria {small_text} bold italic')) # Optional font automation.
convert_button.bind('<Leave>', partial(font_config, convert_button, f'Cambria {small_text}')) # Optional font automation.

base_button = tk.Button(upper_subframe_A, text='Convert to Base', font=('Cambria', small_text), bg=green, relief="raised", command=convert_to_base) # Configures base conversion button.
base_button.place(relx=0.62, rely=0.7, relwidth=0.17, relheight=0.3)
base_button.bind('<Enter>', partial(font_config, base_button, f'Cambria {small_text} bold italic')) # Optional font automation.
base_button.bind('<Leave>', partial(font_config, base_button, f'Cambria {small_text}')) # Optional font automation.

favorites_button = tk.Button(upper_subframe_A, text='Favorites', font=('Cambria', small_text), bg=yellow, command=favorites_update) # Configures favorites button.
favorites_button.place(relx=0.795, rely=0.7, relwidth=0.11, relheight=0.3)
favorites_button.bind('<Enter>', partial(font_config, favorites_button, f'Cambria {small_text} bold italic')) # Optional font automation.
favorites_button.bind('<Leave>', partial(font_config, favorites_button, f'Cambria {small_text}')) # Optional font automation.

values_button = tk.Button(upper_subframe_A, text='Values', font=('Cambria', small_text), bg=yellow, relief="raised", command=values_toggle) # Configures values button.
values_button.place(relx=0.91, rely=0.7, relwidth=0.09, relheight=0.3) # 0.08
values_button.bind('<Enter>', partial(font_config, values_button, f'Cambria {small_text} bold italic')) # Optional font automation.
values_button.bind('<Leave>', partial(font_config, values_button, f'Cambria {small_text}')) # Optional font automation.

#############################################################################################################################################################################################
## Upper Subframe B (Symbol Manager: Banner and Menu)
upper_subframe_B = tk.Frame(root, bd=10) # Configures upper frame.
upper_subframe_B.place(relx=0.5, rely=0.1, relwidth=0.68, relheight=0.2, anchor='n')

upper_subframe_background_B = tk.PhotoImage(file='./background_frames.gif') # Configures foreground image.
upper_subframe_background_label_B = tk.Label(upper_subframe_B, image=upper_subframe_background_B)
upper_subframe_background_label_B.place(relx=-0.4, rely=-1, relwidth=2, relheight=3)

banner_frame = tk.Frame(upper_subframe_B) # Displays an image.
banner_frame.place(relx=0, rely=0, relwidth=1, relheight=0.625)
banner = tk.PhotoImage(file='./background_banner.gif')
banner_label = tk.Label(banner_frame, image=banner)
banner_label.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

preset_frame = tk.Frame(upper_subframe_B) # Configures the database dropdown menu.
preset_text = tk.StringVar(preset_frame)
preset_list = ["CLX"]
preset_text.set("CLX *") # Sets default preset.
preset_text.trace('w', change_preset_text)
preset_menu = tk.OptionMenu(preset_frame, preset_text, *preset_list)
preset_menu.config(bg=blue)
preset_menu.pack(side='right', fill='both')
preset_label = tk.Label(preset_frame, text="Preset:")
preset_label.pack(side='left')
preset_frame.place(relx=0, rely=0.7, relwidth=0.21, relheight=0.3)

category_frame = tk.Frame(upper_subframe_B) # Configures the category dropdown menu.
category_text = tk.StringVar(category_frame)
category_list = ["All", "Quantities", "Constants", "Modifiers", "Other"]
category_text.set("All *") # Sets default preset.
category_text.trace('w', change_category_text)
category_menu = tk.OptionMenu(category_frame, category_text, *category_list)
category_menu.config(bg=blue)
category_menu.pack(side='right', fill='both')
category_label = tk.Label(category_frame, text="Category:")
category_label.pack(side='left')
category_frame.place(relx=0.22, rely=0.7, relwidth=0.24, relheight=0.3)

sort_frame = tk.Frame(upper_subframe_B) # Configures the sorting dropdown menu.
sort_text = tk.StringVar(sort_frame)
sort_list = ["Name", "Symbol", "Units"]
sort_text.set("Name *") # Sets default preset.
sort_text.trace('w', change_sort_text)
sort_menu = tk.OptionMenu(sort_frame, sort_text, *sort_list)
sort_menu.config(bg=blue)
sort_menu.pack(side='right', fill='both')
sort_label = tk.Label(sort_frame, text="Sort:")
sort_label.pack(side='left')
sort_frame.place(relx=0.47, rely=0.7, relwidth=0.22, relheight=0.3)

search_frame = tk.Frame(upper_subframe_B) # Configures the search bar.
search_text = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_text, width=16)
search_entry.bind('<Return>', lambda event, search_text=search_text: search_names(event, search_text)) # Optional font automation.
search_button = tk.Button(search_frame, text='🔍', font=(f'Cambria {micro_text} bold'), bg=blue, command=lambda: search_names('', search_text))
search_label = tk.Label(search_frame, text="Search:")
search_button.pack(side='right', padx=2)
search_entry.pack(side='right')
search_label.pack(side='left')
search_frame.place(relx=0.7, rely=0.7, relwidth=0.3, relheight=0.3)
search_entry.focus_set()

#############################################################################################################################################################################################
## Middle Subframe A (Unit Manager: Units, Prefixes, and Favorites)
middle_subframe_A = tk.Frame(root, bd=10) # Configures middle frame.
middle_subframe_A.place(relx=0.5, rely=0.35, relwidth=0.68, relheight=0.300, anchor='n')

middle_subframe_background_A = tk.PhotoImage(file='./background_frames.gif') # Configures foreground image.
middle_subframe_background_label_A = tk.Label(middle_subframe_A, image=middle_subframe_background_A)
middle_subframe_background_label_A.place(relx=-0.4, rely=-0.4, relwidth=2, relheight=2)

unit_frame = tk.Label(middle_subframe_A, font=('Cambria italic', mini_text), bg=light_gray, text='Unit') # Configures fractional exponent toggle.
unit_frame.place(relx=0, rely=0, relwidth=0.1, relheight=0.15)
fraction_button = tk.Button(middle_subframe_A, text="uˣ", font=('Cambria italic', small_text), bg=blue, command=fraction_set)
fraction_button.bind('<Enter>', partial(font_config, fraction_button, f'Cambria {small_text} bold italic')) # Optional font automation.
fraction_button.bind('<Leave>', partial(font_config, fraction_button, f'Cambria {small_text} italic')) # Optional font automation.
fraction_button.place(relx=0, rely=0.15, relwidth=0.1, relheight=0.15)

candela_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='cd') # Configures candela buttons.
candela_frame.place(relx=0.1125, rely=0, relwidth=0.1, relheight=0.15)
candela_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(0, "×"))
candela_add.bind('<Enter>', partial(font_config, candela_add, f'Cambria {medium_text} bold')) # Optional font automation.
candela_add.bind('<Leave>', partial(font_config, candela_add, f'Cambria {medium_text}')) # Optional font automation.
candela_add.place(relx=0.1125, rely=0.15, relwidth=0.05, relheight=0.15)
candela_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(0, "÷"))
candela_sub.bind('<Enter>', partial(font_config, candela_sub, f'Cambria {medium_text} bold')) # Optional font automation.
candela_sub.bind('<Leave>', partial(font_config, candela_sub, f'Cambria {medium_text}')) # Optional font automation.
candela_sub.place(relx=0.1625, rely=0.15, relwidth=0.05, relheight=0.15)

coulomb_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='C') # Configures coulomb buttons.
coulomb_frame.place(relx=0.225, rely=0, relwidth=0.1, relheight=0.15)
coulomb_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(1, "×"))
coulomb_add.bind('<Enter>', partial(font_config, coulomb_add, f'Cambria {medium_text} bold')) # Optional font automation.
coulomb_add.bind('<Leave>', partial(font_config, coulomb_add, f'Cambria {medium_text}')) # Optional font automation.
coulomb_add.place(relx=0.225, rely=0.15, relwidth=0.05, relheight=0.15)
coulomb_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(1, "÷"))
coulomb_sub.bind('<Enter>', partial(font_config, coulomb_sub, f'Cambria {medium_text} bold')) # Optional font automation.
coulomb_sub.bind('<Leave>', partial(font_config, coulomb_sub, f'Cambria {medium_text}')) # Optional font automation.
coulomb_sub.place(relx=0.275, rely=0.15, relwidth=0.05, relheight=0.15)

gram_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='g') # Configures gram buttons.
gram_frame.place(relx=0.3375, rely=0, relwidth=0.1, relheight=0.15)
gram_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(2, "×"))
gram_add.bind('<Enter>', partial(font_config, gram_add, f'Cambria {medium_text} bold')) # Optional font automation.
gram_add.bind('<Leave>', partial(font_config, gram_add, f'Cambria {medium_text}')) # Optional font automation.
gram_add.place(relx=0.3375, rely=0.15, relwidth=0.05, relheight=0.15)
gram_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(2, "÷"))
gram_sub.bind('<Enter>', partial(font_config, gram_sub, f'Cambria {medium_text} bold')) # Optional font automation.
gram_sub.bind('<Leave>', partial(font_config, gram_sub, f'Cambria {medium_text}')) # Optional font automation.
gram_sub.place(relx=0.3875, rely=0.15, relwidth=0.05, relheight=0.15)

kelvin_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='K') # Configures kelvin buttons.
kelvin_frame.place(relx=0.45, rely=0, relwidth=0.1, relheight=0.15)
kelvin_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(3, "×"))
kelvin_add.bind('<Enter>', partial(font_config, kelvin_add, f'Cambria {medium_text} bold')) # Optional font automation.
kelvin_add.bind('<Leave>', partial(font_config, kelvin_add, f'Cambria {medium_text}')) # Optional font automation.
kelvin_add.place(relx=0.45, rely=0.15, relwidth=0.05, relheight=0.15)
kelvin_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(3, "÷"))
kelvin_sub.bind('<Enter>', partial(font_config, kelvin_sub, f'Cambria {medium_text} bold')) # Optional font automation.
kelvin_sub.bind('<Leave>', partial(font_config, kelvin_sub, f'Cambria {medium_text}')) # Optional font automation.
kelvin_sub.place(relx=0.5, rely=0.15, relwidth=0.05, relheight=0.15)

meter_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='m') # Configures meter buttons.
meter_frame.place(relx=0.5625, rely=0, relwidth=0.1, relheight=0.15)
meter_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(4, "×"))
meter_add.bind('<Enter>', partial(font_config, meter_add, f'Cambria {medium_text} bold')) # Optional font automation.
meter_add.bind('<Leave>', partial(font_config, meter_add, f'Cambria {medium_text}')) # Optional font automation.
meter_add.place(relx=0.5625, rely=0.15, relwidth=0.05, relheight=0.15)
meter_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(4, "÷"))
meter_sub.bind('<Enter>', partial(font_config, meter_sub, f'Cambria {medium_text} bold')) # Optional font automation.
meter_sub.bind('<Leave>', partial(font_config, meter_sub, f'Cambria {medium_text}')) # Optional font automation.
meter_sub.place(relx=0.6125, rely=0.15, relwidth=0.05, relheight=0.15)

mole_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='mol') # Configures mole buttons.
mole_frame.place(relx=0.675, rely=0, relwidth=0.1, relheight=0.15)
mole_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(5, "×"))
mole_add.bind('<Enter>', partial(font_config, mole_add, f'Cambria {medium_text} bold')) # Optional font automation.
mole_add.bind('<Leave>', partial(font_config, mole_add, f'Cambria {medium_text}')) # Optional font automation.
mole_add.place(relx=0.675, rely=0.15, relwidth=0.05, relheight=0.15)
mole_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(5, "÷"))
mole_sub.bind('<Enter>', partial(font_config, mole_sub, f'Cambria {medium_text} bold')) # Optional font automation.
mole_sub.bind('<Leave>', partial(font_config, mole_sub, f'Cambria {medium_text}')) # Optional font automation.
mole_sub.place(relx=0.725, rely=0.15, relwidth=0.05, relheight=0.15)

second_frame = tk.Label(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, text='s') # Configures second buttons.
second_frame.place(relx=0.7875, rely=0, relwidth=0.1, relheight=0.15)
second_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(6, "×"))
second_add.bind('<Enter>', partial(font_config, second_add, f'Cambria {medium_text} bold')) # Optional font automation.
second_add.bind('<Leave>', partial(font_config, second_add, f'Cambria {medium_text}')) # Optional font automation.
second_add.place(relx=0.7875, rely=0.15, relwidth=0.05, relheight=0.15)
second_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: update_units_and_values(6, "÷"))
second_sub.bind('<Enter>', partial(font_config, second_sub, f'Cambria {medium_text} bold')) # Optional font automation.
second_sub.bind('<Leave>', partial(font_config, second_sub, f'Cambria {medium_text}')) # Optional font automation.
second_sub.place(relx=0.8375, rely=0.15, relwidth=0.05, relheight=0.15)

unit_entry = tk.Entry(middle_subframe_A, font=('Cambria', small_text), bg=light_gray, justify='center') # Configures user-entry buttons.
unit_entry.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.15)
unit_entry.bind('<Return>', lambda event, unit="", state="×": entry_unit(event, unit, state)) # Optional font automation.
entry_add = tk.Button(middle_subframe_A, text="×", font=('Cambria', medium_text), bg=blue, command=lambda: entry_unit("", unit_entry.get(), "×"))
entry_add.bind('<Enter>', partial(font_config, entry_add, f'Cambria {medium_text} bold')) # Optional font automation.
entry_add.bind('<Leave>', partial(font_config, entry_add, f'Cambria {medium_text}')) # Optional font automation.
entry_add.place(relx=0.9, rely=0.15, relwidth=0.05, relheight=0.15)
entry_sub = tk.Button(middle_subframe_A, text="÷", font=('Cambria', medium_text), bg=blue, command=lambda: entry_unit("", unit_entry.get(), "÷"))
entry_sub.bind('<Enter>', partial(font_config, entry_sub, f'Cambria {medium_text} bold')) # Optional font automation.
entry_sub.bind('<Leave>', partial(font_config, entry_sub, f'Cambria {medium_text}')) # Optional font automation.
entry_sub.place(relx=0.95, rely=0.15, relwidth=0.05, relheight=0.15)

prefix_button = tk.Button(middle_subframe_A, text='Prefix', font=('Cambria italic', mini_text), bg=green, relief="raised", command=prefix_toggle) # Configures second buttons.
prefix_button.place(relx=0, rely=0.34, relwidth=0.1, relheight=0.15)
prefix_button.bind('<Enter>', partial(font_config, prefix_button, f'Cambria {mini_text} bold italic')) # Optional font automation.
prefix_button.bind('<Leave>', partial(font_config, prefix_button, f'Cambria {mini_text} italic')) # Optional font automation.
prefix_Y_button = tk.Button(middle_subframe_A, text='Y', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("Y")) # Configures Y button.
prefix_Y_button.place(relx=0.1125, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_Y_button.bind('<Enter>', partial(font_config, prefix_Y_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_Y_button.bind('<Leave>', partial(font_config, prefix_Y_button, f'Cambria {small_text}')) # Optional font automation.
prefix_Z_button = tk.Button(middle_subframe_A, text='Z', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("Z")) # Configures Z button.
prefix_Z_button.place(relx=0.156875, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_Z_button.bind('<Enter>', partial(font_config, prefix_Z_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_Z_button.bind('<Leave>', partial(font_config, prefix_Z_button, f'Cambria {small_text}')) # Optional font automation.
prefix_E_button = tk.Button(middle_subframe_A, text='E', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("E")) # Configures E button.
prefix_E_button.place(relx=0.20125, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_E_button.bind('<Enter>', partial(font_config, prefix_E_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_E_button.bind('<Leave>', partial(font_config, prefix_E_button, f'Cambria {small_text}')) # Optional font automation.
prefix_P_button = tk.Button(middle_subframe_A, text='P', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("P")) # Configures P button.
prefix_P_button.place(relx=0.245625, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_P_button.bind('<Enter>', partial(font_config, prefix_P_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_P_button.bind('<Leave>', partial(font_config, prefix_P_button, f'Cambria {small_text}')) # Optional font automation.
prefix_T_button = tk.Button(middle_subframe_A, text='T', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("T")) # Configures T button.
prefix_T_button.place(relx=0.29, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_T_button.bind('<Enter>', partial(font_config, prefix_T_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_T_button.bind('<Leave>', partial(font_config, prefix_T_button, f'Cambria {small_text}')) # Optional font automation.
prefix_G_button = tk.Button(middle_subframe_A, text='G', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("G")) # Configures G button.
prefix_G_button.place(relx=0.334375, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_G_button.bind('<Enter>', partial(font_config, prefix_G_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_G_button.bind('<Leave>', partial(font_config, prefix_G_button, f'Cambria {small_text}')) # Optional font automation.
prefix_M_button = tk.Button(middle_subframe_A, text='M', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("M")) # Configures M button.
prefix_M_button.place(relx=0.37875, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_M_button.bind('<Enter>', partial(font_config, prefix_M_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_M_button.bind('<Leave>', partial(font_config, prefix_M_button, f'Cambria {small_text}')) # Optional font automation.
prefix_k_button = tk.Button(middle_subframe_A, text='k', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("k")) # Configures k button.
prefix_k_button.place(relx=0.423125, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_k_button.bind('<Enter>', partial(font_config, prefix_k_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_k_button.bind('<Leave>', partial(font_config, prefix_k_button, f'Cambria {small_text}')) # Optional font automation.
prefix_h_button = tk.Button(middle_subframe_A, text='h', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("h")) # Configures h button.
prefix_h_button.place(relx=0.4675, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_h_button.bind('<Enter>', partial(font_config, prefix_h_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_h_button.bind('<Leave>', partial(font_config, prefix_h_button, f'Cambria {small_text}')) # Optional font automation.
prefix_da_button = tk.Button(middle_subframe_A, text='da', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("da")) # Configures h button.
prefix_da_button.place(relx=0.511875, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_da_button.bind('<Enter>', partial(font_config, prefix_da_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_da_button.bind('<Leave>', partial(font_config, prefix_da_button, f'Cambria {small_text}')) # Optional font automation.
prefix_d_button = tk.Button(middle_subframe_A, text='d', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("d")) # Configures c button.
prefix_d_button.place(relx=0.55625, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_d_button.bind('<Enter>', partial(font_config, prefix_d_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_d_button.bind('<Leave>', partial(font_config, prefix_d_button, f'Cambria {small_text}')) # Optional font automation.
prefix_c_button = tk.Button(middle_subframe_A, text='c', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("c")) # Configures c button.
prefix_c_button.place(relx=0.600625, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_c_button.bind('<Enter>', partial(font_config, prefix_c_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_c_button.bind('<Leave>', partial(font_config, prefix_c_button, f'Cambria {small_text}')) # Optional font automation.
prefix_m_button = tk.Button(middle_subframe_A, text='m', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("m")) # Configures m button.
prefix_m_button.place(relx=0.645, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_m_button.bind('<Enter>', partial(font_config, prefix_m_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_m_button.bind('<Leave>', partial(font_config, prefix_m_button, f'Cambria {small_text}')) # Optional font automation.
prefix_u_button = tk.Button(middle_subframe_A, text='μ', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("μ")) # Configures μ button.
prefix_u_button.place(relx=0.689375, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_u_button.bind('<Enter>', partial(font_config, prefix_u_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_u_button.bind('<Leave>', partial(font_config, prefix_u_button, f'Cambria {small_text}')) # Optional font automation.
prefix_n_button = tk.Button(middle_subframe_A, text='n', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("n")) # Configures n button.
prefix_n_button.place(relx=0.73375, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_n_button.bind('<Enter>', partial(font_config, prefix_n_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_n_button.bind('<Leave>', partial(font_config, prefix_n_button, f'Cambria {small_text}')) # Optional font automation.
prefix_p_button = tk.Button(middle_subframe_A, text='p', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("p")) # Configures p button.
prefix_p_button.place(relx=0.778125, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_p_button.bind('<Enter>', partial(font_config, prefix_p_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_p_button.bind('<Leave>', partial(font_config, prefix_p_button, f'Cambria {small_text}')) # Optional font automation.
prefix_f_button = tk.Button(middle_subframe_A, text='f', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("f")) # Configures f button.
prefix_f_button.place(relx=0.8225, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_f_button.bind('<Enter>', partial(font_config, prefix_f_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_f_button.bind('<Leave>', partial(font_config, prefix_f_button, f'Cambria {small_text}')) # Optional font automation.
prefix_a_button = tk.Button(middle_subframe_A, text='a', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("a")) # Configures a button.
prefix_a_button.place(relx=0.866875, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_a_button.bind('<Enter>', partial(font_config, prefix_a_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_a_button.bind('<Leave>', partial(font_config, prefix_a_button, f'Cambria {small_text}')) # Optional font automation.
prefix_z_button = tk.Button(middle_subframe_A, text='z', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("z")) # Configures z button.
prefix_z_button.place(relx=0.91125, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_z_button.bind('<Enter>', partial(font_config, prefix_z_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_z_button.bind('<Leave>', partial(font_config, prefix_z_button, f'Cambria {small_text}')) # Optional font automation.
prefix_y_button = tk.Button(middle_subframe_A, text='y', font=('Cambria', small_text), bg=green, relief="raised", command=lambda: prefix_toggle("y")) # Configures y button.
prefix_y_button.place(relx=0.955625, rely=0.34, relwidth=0.044375, relheight=0.15)
prefix_y_button.bind('<Enter>', partial(font_config, prefix_y_button, f'Cambria {small_text} bold')) # Optional font automation.
prefix_y_button.bind('<Leave>', partial(font_config, prefix_y_button, f'Cambria {small_text}')) # Optional font automation.

favorites_frame = tk.Frame(middle_subframe_A, borderwidth=0, relief='flat', bg=medium_gray) # Configures favorites repository.
favorites = tk.Text(favorites_frame, width=24, height=0, wrap="none", borderwidth=0, cursor='arrow', bg=medium_gray)
favorites.bind('<FocusIn>', lambda event: root.focus())
favorites_scrollbar = ttk.Scrollbar(favorites_frame, orient="horizontal", style="Dark.Horizontal.TScrollbar", command=favorites.xview)
favorites.configure(xscrollcommand=favorites_scrollbar.set)
favorites.grid(row=0, column=0, sticky="nsew")
favorites_scrollbar.grid(row=1, column=0, sticky="ew")
favorites_frame.grid_rowconfigure(0, weight=1)
favorites_frame.grid_columnconfigure(0, weight=1)
favorites_frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)

#############################################################################################################################################################################################
## Middle Subframe B (Symbol Manager: Symbols and Entry Cells)
middle_subframe_B = tk.Frame(root, bd=10) # Configures middle frame.
middle_subframe_B.place(relx=0.5, rely=0.35, relwidth=0.68, relheight=0.300, anchor='n')

middle_subframe_background_B = tk.PhotoImage(file='./background_frames.gif') # Configures foreground image.
middle_subframe_background_label_B = tk.Label(middle_subframe_B, image=middle_subframe_background_B)
middle_subframe_background_label_B.place(relx=-0.4, rely=-0.4, relwidth=2, relheight=2)

cell_canvas = tk.Canvas(middle_subframe_B, borderwidth=0, bg=cell_frame_color) # Creates a canvas to hold the entry cells and a scrollbar.
cell_canvas.bind('<Enter>', set_scroll)
cell_canvas.bind('<Leave>', lambda event, unset=True: set_scroll(unset))
cell_frame = tk.Frame(cell_canvas, bg=cell_frame_color) # Creates a frame for the entry cells.
cell_scrollbar_A = ttk.Scrollbar(cell_canvas, orient='vertical', style="Dark.Vertical.TScrollbar", command=cell_canvas.yview)
cell_scrollbar_B = ttk.Scrollbar(cell_canvas, orient='horizontal', style="Light.Horizontal.TScrollbar", command=cell_canvas.xview)
cell_canvas.config(yscrollcommand=cell_scrollbar_A.set, xscrollcommand=cell_scrollbar_B.set)
cell_scrollbar_A.pack(side='right', fill='y') # Sets the scrollbar.
cell_canvas.pack(side='left', fill='both', expand=True)
cell_canvas.create_window((0,0), window=cell_frame, anchor='nw')
cell_frame.bind('<Configure>', lambda event, canvas=cell_canvas: configure_cell_canvas(cell_canvas))

#############################################################################################################################################################################################
## Lower Subframe (Notepad)
lower_subframe = tk.Frame(root, bd=10) # Configures lower frame.
lower_subframe.place(relx=0.5, rely=0.7, relwidth=0.68, relheight=0.15, anchor='n')

lower_subframe_background = tk.PhotoImage(file='./background_frames.gif') # Configures foreground image.
lower_subframe_background_label = tk.Label(lower_subframe, image=lower_subframe_background)
lower_subframe_background_label.place(relx=-0.4, rely=-4, relwidth=2, relheight=10)

textbox_right_button = tk.Button(lower_subframe, text="←", font=(f'Cambria {small_text} bold'), bg=blue, relief='raised', command=lambda: notes_toggle("←"))
textbox_right_button.place(relx=0, rely=0, relwidth=0.044, relheight=0.333)
textbox_right_button.bind('<Enter>', partial(font_config, textbox_right_button, f'Cambria {medium_text} bold')) # Optional font automation.
textbox_right_button.bind('<Leave>', partial(font_config, textbox_right_button, f'Cambria {small_text} bold')) # Optional font automation.

textbox_left_button = tk.Button(lower_subframe, text="→", font=(f'Cambria {small_text} bold'), bg=green, relief='raised', command=lambda: notes_toggle("→"))
textbox_left_button.place(relx=0, rely=0.334, relwidth=0.044, relheight=0.333)
textbox_left_button.bind('<Enter>', partial(font_config, textbox_left_button, f'Cambria {medium_text} bold')) # Optional font automation.
textbox_left_button.bind('<Leave>', partial(font_config, textbox_left_button, f'Cambria {small_text} bold')) # Optional font automation.

textbox_clear_button = tk.Button(lower_subframe, text="✗", font=('Cambria', micro_text), bg=red, relief='raised', command=lambda: notes_toggle("✗"))
textbox_clear_button.place(relx=0, rely=0.667, relwidth=0.044, relheight=0.333)
textbox_clear_button.bind('<Enter>', partial(font_config, textbox_clear_button, f'Cambria {mini_text} bold')) # Optional font automation.
textbox_clear_button.bind('<Leave>', partial(font_config, textbox_clear_button, f'Cambria {micro_text}')) # Optional font automation.

textbox_1 = tk.Text(lower_subframe, font=('Cambria', small_text), wrap='word') # Configures textbox_1 display.
textbox_1_scrollbar = ttk.Scrollbar(textbox_1, orient='vertical', style="Light.Vertical.TScrollbar", command=textbox_1.yview)
textbox_1_scrollbar.place(relx=0.985, rely=0, relwidth=0.014, relheight=1)
textbox_1.place(relx=0.0426, rely=0, relwidth=0.952, relheight=1)

textbox_2 = tk.Text(lower_subframe, font=('Cambria', small_text), wrap='word') # Configures textbox_1 display.
textbox_2_scrollbar = ttk.Scrollbar(textbox_1, orient='vertical', style="Light.Vertical.TScrollbar", command=textbox_1.yview)
textbox_2_scrollbar.place(relx=0.985, rely=0, relwidth=0.014, relheight=1)
textbox_2.place(relx=0.0426, rely=0, relwidth=0.952, relheight=1)

textbox_3 = tk.Text(lower_subframe, font=('Cambria', small_text), wrap='word') # Configures textbox_1 display.
textbox_3_scrollbar = ttk.Scrollbar(textbox_1, orient='vertical', style="Light.Vertical.TScrollbar", command=textbox_1.yview)
textbox_3_scrollbar.place(relx=0.985, rely=0, relwidth=0.014, relheight=1)
textbox_3.place(relx=0.0426, rely=0, relwidth=0.952, relheight=1)

#############################################################################################################################################################################################
## Other (Utility)
switch_button = tk.Button(root, font=('Cambria', small_text), text='Switch', bg=blue, command=lambda: raise_frame()) # Configures application switch button.
switch_button.place(relx=0.3, rely=0.9, relwidth=0.12, relheight=0.05, anchor='n')
switch_button.bind('<Enter>', partial(font_config, switch_button, f'Cambria {small_text} bold italic')) # Optional font automation.
switch_button.bind('<Leave>', partial(font_config, switch_button, f'Cambria {small_text}')) # Optional font automation.

save_button = tk.Button(root, font=('Cambria', small_text), text='Save', bg=green, command=save_command) # Configures exit button.
save_button.place(relx=0.7, rely=0.9, relwidth=0.12, relheight=0.05, anchor='n')
save_button.bind('<Enter>', partial(font_config, save_button, f'Cambria {small_text} bold italic')) # Optional font automation.
save_button.bind('<Leave>', partial(font_config, save_button, f'Cambria {small_text}')) # Optional font automation.

close_button = tk.Button(root, font=('Cambria', small_text), text='Close', bg=red, command=root.destroy) # Configures exit button.
close_button.place(relx=0.5, rely=0.9, relwidth=0.12, relheight=0.05, anchor='n')
close_button.bind('<Enter>', partial(font_config, close_button, f'Cambria {small_text} bold italic')) # Optional font automation.
close_button.bind('<Leave>', partial(font_config, close_button, f'Cambria {small_text}')) # Optional font automation.

#############################################################################################################################################################################################
## Startup Commands
print(f"{'-'*98}\n{'-'*98}\nCoalexicon [CLX] Startup\nWelcome!\n\n{'-'*98}") # Optional.
favorites_update() # Loads saved favorites.
load_notes() # Loads notes.
load_units()  # Loads units for Unit Manager.
load_symbols() # Loads default symbol database for Symbol Manager.
main_symbols() # Creates cells and updates the display for Symbol Manager.
raise_frame() # Triggers the default application, as set by application_index.
print(f"{'-'*98}") # Optional.
root.mainloop() # Starts the GUI.

#############################################################################################################################################################################################