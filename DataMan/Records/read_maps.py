"""These correlate the read-in fields and their locations.
    These values can be adjusted to reflect changes in the
    excel workbook layout. Additional maps may be created
    to add layouts or formats.

    DO NOT CHANGE THE KEYS. THESE MUST MATCH THE KEYS USED IN VIEWS.
    #"""

read_in_map_MS = {
	'sheetType':'Mass spec',
	'wsIn':'Input', #name of Input worksheet
	'in_section':'B34:H{}', #Where the samples are defined (as rows)
	'start_loc':'C34', #Required field for first row (empty if empty file)
	'sample_name':2, #Within a row, required sample name (empty only at the end)
	'storage_location':0, #within a row, (not intended to be tray pos)
	'date_global':True,#date will either be absolute or in row
	'date_created':'J5', #cell if absolute, index if in row
	'organism':'J2', #absolute cell
	'comments_row':{ #Any extra information
		#Format: 'Heading: ':row index
		'Concentration: ':5,
	},
	'comments_gen':{ #Information not on the row
		#Format: 'Heading: ':cell 
		'Notebook code: ':'J4',
	},
	
	'experiment_global':False, #Are all samples of the same experiment?
	'experiment_loc':1, #Input row index if local, or cell

	#Input sheet dataset information
	'setting_loc':5, #Input row coordinate
	'data_type_loc':'I3', #Input sheet cells
	'instrument_type_loc':'I3',
	'inst_code':'J3',
	'date_loc':'J5',

	#Worklist fields (about dataset, different rows)
	'wsWL':'Worklist',
	'wlrowNumInit':1, #one less than the row to start on
	#				with reference to the worklist sheet
	'dataset_name':4,#worklist row coordinate
	'file_location':5,
	'file_name':4, #worklist row index (optionally same as dataset)
	'file_extension_from_excel':False, #If the extension is specified or assumed
	'file_extension':'', #absolute (or cell if specified)
}

read_in_map_gen = {
	'sheetType':'General',

	'wsIn':'Input', #name of Input worksheet
	'in_section':'B34:{}{}', #Where the samples are defined (as rows)
	'start_loc':'C34', #Required field for first row (empty if empty file)
	'sample_name':1, #Within a row, required sample name (empty only at the end)
	'storage_location':8, #within a row, (not intended to be tray pos)
	'date_global':False,#date will either be absolute or in row
	'date_created':6, #cell if absolute, index if in row
	'organism':'J2', #absolute cell
	'comments_row':{ #Any extra information
		#Format: 'Heading: ':row index
		'Concentration: ':5,
	},
	'comments_gen':{ #Information not on the row
		#Format: 'Heading: ':cell 
		'Notebook code: ':'J4',
	},
	
	'experiment_global':True, #Are all samples of the same experiment?
	'experiment_loc':'C2', #input row index or cell if global

	#Input sheet dataset information
	'setting_loc':5, #Input row coordinate
	'data_type_loc':'I3', #Input sheet cells
	'instrument_type_loc':'J3',
	'inst_code':'J4',
	'date_loc':'J5',

	#Worklist fields (about dataset, different rows)
	'wsWL':'Worklist',
	'wlrowNumInit':1, #one less than the row to start on
	#				with reference to the worklist sheet
	'dataset_name':4,#worklist row coordinate
	'file_location':5,
	'file_name':4, #worklist row index (optionally same as dataset)
	'file_extension_from_excel':True, #If the extension is specified or assumed
	'file_extension':'A7', #absolute (or cell if specified)
}