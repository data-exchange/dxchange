function read_DataExchange_volume, base_file

  read_datadarkexchange_hdf, base_file, darks
  read_datawhiteexchange_hdf, base_file, whites
  read_dataexchange_hdf, base_file, projections

dSize = SIZE(darks)
ndarks = dSize[3]
wSize = SIZE(whites)
nwhites = wSize[3]

; Average the darks
if (ndarks gt 1) then begin
  dark = total(darks, 3)/ndarks
endif else begin
  dark = float(darks)
endelse

; Average the whites
if (nwhites gt 1) then begin
  white = total(whites, 3)/nwhites
endif else begin
  white = float(whites)
endelse

white_minus_dark = white - dark

; Correct each projection
for i=0, nprojections-1 do begin
  print, 'Correcting projection ', i
  projections[0,0,i] = 10000 * ((projections[*,*,i]-dark)/(white_minus_dark)) + 0.5
endfor

return, projections

end

