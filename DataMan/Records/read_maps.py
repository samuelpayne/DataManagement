"""Project DataMan

These correlate the read-in fields and their locations.
    These values can be adjusted to reflect changes in the
    excel workbook layout. Additional maps may be created
    to add layouts or formats.

    DO NOT CHANGE THE KEYS. THESE MUST MATCH THE KEYS USED IN VIEWS.
    #"""

read_in_map_MS = {
	'sheetType':'Mass spec',
	'wsIn':'Input', #name of Input worksheet
	'variable_colums_TF': False, # the number of columns is set
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
	'in_section_lookup':'A34:H{}',
	'lookup_column':0,#where sample numbers are defined as used on worklists
	'lookup_exp':2,
	'lookup_sample':3,
	
	'experiment_global':False, #Are all samples of the same experiment?
	'experiment_loc':1, #Input row index if local, or cell

	#Input sheet dataset information
	'setting_loc':7, #Input row coordinate
	'data_type_loc':'I3', #Input sheet cells
	'instrument_type_loc':'I3',
	'inst_code':'J3',
	'date_loc':'J5',

	#Instrument Settings file upload
	#None are currently used
	'settings_sheet':'Methods',
	'settings_keyword_column':'B',
	'settings_file_column':'C',
	'settings_description':'E',

	'settings_file':6, #in wlrow
	#Worklist fields (about dataset, different rows)
	'wsWL':'Worklist',
	'wlrowNumInit':1, #one less than the row to start on
	#				with reference to the worklist sheet
	'wlRows':'A2:G{}', #Worklist rows to be processed
	'wl_sample_type':3,#If QC versus defined on input
	'wl_sample_num':2,
	'dataset_name':4,#worklist row coordinate
	'file_location':5,
	'file_name':4, #worklist row index (optionally same as dataset)
	'file_extension_from_excel':False, #If the extension is specified or assumed
	'file_extension':'', #absolute (or cell if specified)

	'missing_fields':['lead','storage_condition','storage_location','file_extension'],
}

read_in_map_gen = {
	'sheetType':'General',

	'exp_name':'C2',
	'lead':'C3',
	'description':'A4',
	'IRB':'C9',

	'wsIn':'Input', #name of Input worksheet
	'variable_colums_TF': True, # the number of columns is flexible
	#		meaning that users can add columns and views needs to format the section with rows and columns
	'in_section':'C18:{}{}', #Where the samples are defined (as rows)
	'start_loc':'C18', #Required field for first row (empty if empty file)
	'sample_name':1, #Within a row, required sample name (empty only at the end)
	'storage_location':8, #within a row, (not intended to be tray pos)
	'date_global':False,#date will either be absolute or in row
	'date_created':6, #cell if absolute, index if in row
	'organism':'J2', #absolute cell
	'comments_row':{ #Any extra information
		#Format: 'Heading: ':row index
		'Concentration: ':4,
	},
	'comments_gen':{ #Information not on the row
		#Format: 'Heading: ':cell 
		'Notebook code: ':'J5',
	},
	'in_section_lookup':'A18:H{}', #Which section contains the sample number,
	#								Name, and experiment name, and methods
	'lookup_column':0,
	'lookup_exp':2,
	'lookup_sample':3,
	
	'experiment_global':False, #Are all samples of the same experiment?
	'experiment_loc':0, #input row index or cell if global

	#Input sheet dataset information
	'setting_loc':7, #Input row coordinate
	'data_type_loc':'J3', #Input sheet cells
	'instrument_type_loc':'J3',
	'inst_code':'J4',
	'date_loc':'J6',
	
	#Instrument Settings file upload
	'settings_sheet':'Methods',
	'settings_keyword_column':'B',
	'settings_file_column':'C',
	'settings_description':'E',
	
	'settings_file':7,#relative to wlrow

	#Worklist fields (about dataset, different rows)
	'wsWL':'Worklist',
	'wlrowNumInit':1, #one less than the row to start on
	#				with reference to the worklist sheet
	'wlRows':'A2:M{}', #Worklist rows to be processed
	'wl_sample_type':3,#If QC versus defined on input
	'wl_sample_num':2,
	'dataset_name':4,#worklist row coordinate
	'file_location':10,
	'file_name':4, #worklist row index (optionally same as dataset)
	'file_extension_from_excel':True, #If the extension is specified or assumed
	'file_extension':11, #literal or relative to row

	#Individuals page
	'wsIndiv':'Individuals',
	'indivExp':'C2',
	'indivRows':'A11:{}{}',
	'indivID':1,
	'gender':2,
	'age':3,
	'health_status':4,
	'indivComments':5,
}