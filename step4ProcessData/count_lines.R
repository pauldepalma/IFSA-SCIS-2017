count_lines<- function() {
    
    #vector of files names in repository
    repos = "../f0Repos"
    file_vec <- list.files(path = repos)
    for (i in 1:length(file_vec)){
      file_vec[i] = paste(repos,"/",file_vec[i],sep="")
}
  for (file in file_vec){
    print (file)
  }

      

    
     # monitor <- read.csv(nweFile, header = TRUE)
            
    
}