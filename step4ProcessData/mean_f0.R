mean_f0<- function(file_name) {
    
  df <- read.csv(file_name, header = FALSE)
  cur = paste(df[1,1],df[1,2], sep = "")
  print (cur)
}