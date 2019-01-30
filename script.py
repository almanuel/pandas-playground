#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

spreadsheet_path = 'data/empleadores.xlsx'
output_path='merge.csv'

# cantidad de hojas a mergear. Se leen en orden, desde la primera. 
cant_hojas = 4

# Repeated columns
def clean_dup_columns(df, sep=None):
	cols = ['Clientes', 'Domicilio', 'Razon Social', 'Email', 'Teléfono', 'Cuit', 'Origen', 'Total De Empleados', 'Comentarios', 'Miembro De La Cepit']
	for c in cols:
		left = c + '_x'
		right = c + '_y'
		if left in df.columns and right in df.columns:
			s = pd.Series()
			for index, row in df.iterrows():
				value_left = str(row[left]).lower() if not pd.isna(row[left]) else ''
				value_right = str(row[right]).lower() if not pd.isna(row[left]) else ''

				if (value_left == value_right):
					value = value_left

				elif (value_left not in value_right and value_right not in value_left):
					if pd.notnull(row[left]):
						value = value_left
						if pd.notnull(row[right]):
							value += sep + value_right
					elif pd.notnull(row[right]):
						value = value_right

				else:
					value = max([value_left, value_right], key=len)
				
				s.at[index] = value.title() if value != 'nan' else ''

			df[c] = s
			df = df.drop([left, right], axis=1)
	return df



#encoding=None
encoding='utf-8-sig'

# Load from Excel
print('Loading spreadsheets from ' + spreadsheet_path)
hojas = list()
for i in range(cant_hojas):
	hojas.append(pd.read_excel(spreadsheet_path, sheet_name=i, encoding=encoding))


print('Sanitazing dataframes')
for h in hojas:
	h.columns = h.columns.str.title()
	h.Empresa = h.Empresa.str.title()
	h.Empresa = h.Empresa.str.strip()
	h = h.sort_values(by=['Empresa'])
	

print('Merging dataframes')
copy = False
sep=' | '
m = hojas[0]
for i in range(cant_hojas-1):
	m = m.merge(hojas[i+1], how='outer', on='Empresa', copy=copy)
	m = clean_dup_columns(m, sep)


print('Sorting rows and columns')
m = m.sort_values(by=['Empresa'])
cols = ['Empresa', 'Razon Social', 'Cuit', 'Domicilio', 'Domicilio \nCentral/Legal', 
 'Titular Tandil', 'Miembro De La Cepit', 'Tenemos Afiliados?', 'Total De Empleados', 'Cantidad Empleados Tandil', 'Persona De Contacto', 'Origen', 'Tecnologias', 'Informaticos Local', 'Ubicación Sede Central', 'A Qué Se Dedica', 'Actividades', 'Sector', 'Tecnologías', 'Rango De Cobertura (Local, Nacional, Etc.)', 'Clientes', 'Fundacion', 'Teléfono', 'Tel 2', 'Email', 
 'Web', 'Comentarios',
]
m = m[cols]


print('Saving merge at '+ output_path)
m.to_csv(path_or_buf=output_path)