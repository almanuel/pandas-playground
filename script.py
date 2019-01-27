#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

#encoding=None
encoding='utf-8-sig'

# Load from Excel
oja1 = pd.read_excel('empleadores.xlsx', sheet_name=0, encoding=encoding)
hoja2 = pd.read_excel('empleadores.xlsx', sheet_name=1, encoding=encoding)
pio = pd.read_excel('empleadores.xlsx', sheet_name=2, encoding=encoding)
mar = pd.read_excel('empleadores.xlsx', sheet_name=3, encoding=encoding)

# Title Case en headers de columa
pio.columns = pio.columns.str.title()
mar.columns = mar.columns.str.title()

# Title Case en valores columna Empresa
pio.Empresa = pio.Empresa.str.title()
mar.Empresa = mar.Empresa.str.title()

# Ordenar por Empresa
hoja1 = hoja1.sort_values(by=['Empresa'])
hoja2 = hoja2.sort_values(by=['Empresa'])
pio   = pio.sort_values(by=['Empresa'])
mar   = mar.sort_values(by=['Empresa'])

# No funciona aun.
# m  = pd.merge_asof(hoja1, hoja2, on='Empresa') 
# m2 = pd.merge_asof(m, pio, on='Empresa') 
# m3 = pd.merge_asof(m2, mar, on='Empresa') 

# TODO hacer que no copie columnas iguales generando
#      por ej columnas cuit_x, cuit_y en resultado de merge.

copy = False
m  = hoja1.merge(hoja2, how='outer', on='Empresa', copy=copy)
m2 = m.merge(pio, how='outer', on='Empresa', copy=copy)
m3 = m2.merge(mar, how='outer', on='Empresa', copy=copy)

m3 = m3.sort_values(by=['Empresa'])

m3.to_csv(path_or_buf='merge.csv')

