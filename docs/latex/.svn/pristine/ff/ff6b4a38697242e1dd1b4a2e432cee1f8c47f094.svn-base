pro read_DataDarkExchange_hdf, file, data
  file_id=H5F_OPEN(file)
  dataset_id = H5D_OPEN(file_id,'/exchange/data_dark')
  data = H5D_Read(dataset_id)
  H5D_CLOSE, dataset_id
  H5F_CLOSE, file_id
end