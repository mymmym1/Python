tempMonth6mean <- function(){
  newframe = data.frame()
  for(l in 1:153){
    if(file[l,]$Month == 6){
      newframe = rbind(newframe, file[l,])
    }
  }
  tempmean = mean(newframe$Temp)
  tempmean
}