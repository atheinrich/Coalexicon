# Coalexicon
Interactive repository and dimensional analysis suite for numerical quantities used in physics. Requires a minimum of Python 3.8 and the following packages: tkinter, functools, time, and fractions.

# General Operation
-  Press "Switch" to switch applications between Symbol Manager and Unit Manager.
-  Press "Enter" in a textbox to submit a value, then click "Save" to retain it.

# Notepad
-  The Notepad is always present at the bottom of the application. It may be edited manually through database_notes.
-  Press "←" or "→" to move between each of the three pages.
-  Press "✗" to clear the current page.

# Symbol Manager
-  This application is an interactive repository with various sorting methods. Its entries may be edited manually through database_clx, database_iso, and database_custom.
-  Use the "Preset" menu to select a system of conventions. The default is "CLX," which primarily differs from "SI/ISO" in its use of grams and coulombs in place of kilograms and amperes.
-  Use the "Category" menu to select which quantities to view.
-  Use the "Sort" menu to select a sorting method.
-  Use the search bar and the "🔍" button to search entries by name.
-  Use the empty box at the bottom of the "Name" column to create a new entry.

# Unit Manager
-  This application is a dimensional analysis suite. Its entries may be edited manually through database_conversions and database_units. Switch the "Preset" in Symbol Manager to "SI/ISO" to work in base units of kilograms and amperes.
-  Press "×" or "÷" beneath a unit to add it to the current set of units, which is displayed in the window at the top left.
-  Click inside this display window to copy the current set to the Notepad.
-  Enter non-base units or numbers in the entry box on the right. Supported units are listed in database_conversions. Numerical entries support the "#e#" convention. Enter "theme" to change the background.
-  Toggle fractional powers by pressing "uˣ" on the left prior to "×" or "÷."
-  Add an SI prefix to a unit by selecting a prefix button prior to "×" or "÷."
-  Recall a saved set of units by selecting it in the Favorites list.
-  Press "Common Conversions" or "Related Quantities" to copy the respective data to the Notepad.
-  Press "Clear" to remove the current set of units.
-  Press "Invert" to transform the current set of units to its multiplicative inverse.
-  Press "Convert to Values" to replace all prefixes in the current set of units by their numerical values.
- Press "Convert to Base" to replace all non-base units in the current set of units by their equivalent units and values in the current "Preset."
- Press "Favorites" to add or remove the current set of units to the Favorites list.
- Press "Values" to toggle the visibility of numbers in the display window.

# Known Issues
-  When creating a new entry in Symbol Manager, proper behavior depends on the order in which actions are taken. It is best to write the name and press enter before editing the other cells.
-  Removing entries from Symbol Manager is only possible by editing the database file, such as database_clx or database_iso. This must also be done to set the "Category" for a new entry.
-  The scroll bar in Symbol Manager does not automatically account for shorter lists, requiring the user to scroll to the top of the list before the scroll bar can adjust.
-  Certain processes in Unit Manager lead to the duplication of units in the Favorites list, wherein only one can be removed in the application. This may be fixed manually by editing database_favorites.
-  Fractional units do not always behave as intended.
-  The "#e#" convention in Unit Manager does not always behave well with division.
